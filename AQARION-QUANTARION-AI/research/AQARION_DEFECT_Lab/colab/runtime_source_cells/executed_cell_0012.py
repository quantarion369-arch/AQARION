import copy
import csv
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch import nn

if "CandidateDefectLoss" not in globals():
    raise RuntimeError("Run the CandidateDefectLoss cell first.")


def run_width3_replication():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

    dtype = torch.float64
    seeds = tuple(range(372, 382))
    n, width, steps = 8, 3, 400
    learning_rate, ridge, noise = 0.01, 1e-4, 0.02

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = Path("aqarion_defect_results") / ("replication_" + stamp)
    output.mkdir(parents=True, exist_ok=False)

    config = {
        "seeds": list(seeds),
        "width": width,
        "weights": [0.0, 1.0],
        "steps": steps,
        "learning_rate": learning_rate,
        "ridge": ridge,
        "noise": noise,
        "torch_version": str(torch.__version__),
        "dtype": str(dtype),
        "evaluation": "new noise on the same eight states",
        "training_target": "noisy training observations",
    }
    (output / "config.json").write_text(
        json.dumps(config, indent=2), encoding="utf-8"
    )

    theta = torch.arange(n, dtype=dtype) * (2 * math.pi / n)
    clean = torch.stack(
        [
            theta.cos(), theta.sin(),
            (2 * theta).cos(), (2 * theta).sin(),
        ],
        dim=1,
    )
    successors = (torch.arange(n) + 1) % n
    K = torch.eye(n, dtype=dtype)[successors]
    state_eye = torch.eye(n, dtype=dtype)
    cluster_eye = torch.eye(width, dtype=dtype)

    class ReplicationAE(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(4, 16), nn.Tanh(), nn.Linear(16, width)
            )
            self.decoder = nn.Sequential(
                nn.Linear(width, 16), nn.Tanh(), nn.Linear(16, 4)
            )

        def forward(self, x):
            assignments = self.encoder(x).softmax(dim=-1)
            return self.decoder(assignments), assignments

    results = []

    print("START: frozen width-three replication")
    print("NEW_SEEDS:", seeds)
    print("CONFIGURATION_TUNING=NONE")
    print("EXPECTED_RUNS=20")

    for seed in seeds:
        torch.manual_seed(seed)
        generator = torch.Generator().manual_seed(seed + 10000)

        train_x = clean + noise * torch.randn(
            clean.shape, generator=generator, dtype=dtype
        )
        eval_target = clean.repeat(16, 1)
        eval_x = eval_target + noise * torch.randn(
            eval_target.shape, generator=generator, dtype=dtype
        )
        next_target = clean[successors].repeat(16, 1)

        initial = ReplicationAE().to(dtype=dtype)

        for weight in (0.0, 1.0):
            model = copy.deepcopy(initial)
            optimizer = torch.optim.Adam(
                model.parameters(), lr=learning_rate
            )
            defect_fn = CandidateDefectLoss(ridge=ridge)

            model.train()
            for step in range(steps):
                optimizer.zero_grad(set_to_none=True)
                reconstruction, assignments = model(train_x)

                reconstruction_loss = (
                    reconstruction - train_x
                ).square().mean()
                loss = (
                    reconstruction_loss
                    + weight * defect_fn(assignments, K)
                )

                if not torch.isfinite(loss).item():
                    raise RuntimeError(
                        f"Nonfinite loss: seed={seed}, weight={weight}"
                    )

                loss.backward()

                for parameter in model.parameters():
                    if parameter.grad is not None:
                        if not torch.isfinite(parameter.grad).all().item():
                            raise RuntimeError("Nonfinite gradient")

                optimizer.step()

            model.eval()
            with torch.no_grad():
                train_reconstruction, train_s = model(train_x)
                eval_reconstruction, eval_s = model(eval_x)

                latent_map = torch.linalg.solve(
                    train_s.T @ train_s + ridge * cluster_eye,
                    train_s.T @ train_s[successors],
                )
                predicted_s = eval_s @ latent_map
                predicted_next = model.decoder(predicted_s)

                projection = train_s @ torch.linalg.pinv(train_s)
                residual = (
                    (state_eye - projection) @ K @ projection
                )
                occupancy = torch.bincount(
                    train_s.argmax(dim=1), minlength=width
                ).tolist()

                row = {
                    "seed": seed,
                    "width": width,
                    "defect_weight": weight,
                    "train_recon_mse": (
                        train_reconstruction - train_x
                    ).square().mean().item(),
                    "eval_denoise_mse": (
                        eval_reconstruction - eval_target
                    ).square().mean().item(),
                    "decoded_next_mse": (
                        predicted_next - next_target
                    ).square().mean().item(),
                    "ridge_defect": defect_fn(train_s, K).item(),
                    "unridged_defect": residual.square().mean().item(),
                    "assignment_rank": int(
                        torch.linalg.matrix_rank(train_s).item()
                    ),
                    "hard_occupancy": ",".join(map(str, occupancy)),
                    "predicted_assignment_min": predicted_s.min().item(),
                    "predicted_row_sum_error": (
                        predicted_s.sum(dim=1) - 1
                    ).abs().max().item(),
                }

            for value in row.values():
                if isinstance(value, float) and not math.isfinite(value):
                    raise RuntimeError("Nonfinite evaluation metric")

            checkpoint = output / f"seed_{seed}_weight_{int(weight)}.pt"
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "config": config,
                    "seed": seed,
                    "weight": weight,
                    "metrics": row,
                    "train_x": train_x,
                    "eval_x": eval_x,
                    "clean": clean,
                    "koopman": K,
                    "latent_map": latent_map,
                },
                checkpoint,
            )

            results.append(row)
            print(
                f"seed={seed} weight={weight:g}"
                f" denoise={row['eval_denoise_mse']:.6f}"
                f" next={row['decoded_next_mse']:.6f}"
                f" defect={row['unridged_defect']:.6f}"
                f" occupancy={occupancy}",
                flush=True,
            )

    receipt = output / "results.csv"
    with receipt.open("x", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    print("\nPAIRED RESULTS: REGULARIZED MINUS BASELINE")
    differences = {
        "eval_denoise_mse": [],
        "decoded_next_mse": [],
        "unridged_defect": [],
    }

    for seed in seeds:
        baseline = next(
            r for r in results
            if r["seed"] == seed and r["defect_weight"] == 0
        )
        regularized = next(
            r for r in results
            if r["seed"] == seed and r["defect_weight"] == 1
        )
        deltas = {
            key: regularized[key] - baseline[key]
            for key in differences
        }
        for key, value in deltas.items():
            differences[key].append(value)

        print(
            f"seed={seed}"
            f" denoise_delta={deltas['eval_denoise_mse']:+.6f}"
            f" next_delta={deltas['decoded_next_mse']:+.6f}"
            f" defect_delta={deltas['unridged_defect']:+.6f}"
        )

    print("\nREPLICATION SUMMARY: NEW SEEDS ONLY")
    for key, values in differences.items():
        print(
            key,
            "improved_pairs=", sum(v < 0 for v in values),
            "of=", len(values),
            "mean_delta=", round(statistics.mean(values), 6),
            "median_delta=", round(statistics.median(values), 6),
            "min_delta=", round(min(values), 6),
            "max_delta=", round(max(values), 6),
        )

    for weight in (0.0, 1.0):
        group = [
            r for r in results if r["defect_weight"] == weight
        ]
        print(
            f"weight={weight:g}",
            "mean_next=",
            round(statistics.mean(r["decoded_next_mse"] for r in group), 6),
            "beats_zero_pairs=",
            sum(r["decoded_next_mse"] < 0.5 for r in group),
            "of=", len(group),
        )

    print("\nWIDTH3_REPLICATION=COMPLETE")
    print("RUNS:", len(results))
    print("CHECKPOINTS:", len(list(output.glob("*.pt"))))
    print("RESULT_DIRECTORY:", output)
    print("RESULT_CSV:", receipt)
    print("GENERALIZATION_TO_NEW_DYNAMICS=NOT_TESTED")
    print("SCIENTIFIC_BENEFIT=REQUIRES_REVIEW")
    print("HUGGING_FACE_FILES_CHANGED=NO")

    return results, output


replication_rows, replication_directory = run_width3_replication()