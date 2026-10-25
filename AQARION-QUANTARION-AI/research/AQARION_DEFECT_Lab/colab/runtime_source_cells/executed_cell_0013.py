import csv
import hashlib
import math
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch import nn


def run_checkpoint_audit():
    torch.set_num_threads(1)

    root = Path(
        "aqarion_defect_results/"
        "replication_20261025T025032399216Z"
    )
    if not root.is_dir():
        raise RuntimeError(
            "Replication directory is missing. "
            "Do not rerun training automatically."
        )

    expected = {
        f"seed_{seed}_weight_{weight}.pt"
        for seed in range(372, 382)
        for weight in (0, 1)
    }
    files = sorted(root.glob("*.pt"))
    if {p.name for p in files} != expected:
        raise RuntimeError("Expected exactly the 20 replication checkpoints.")

    def file_hash(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    before_hashes = {p.name: file_hash(p) for p in files}
    rows = []

    print("START: saved-checkpoint audit")
    print("TRAINING=NONE")
    print("HORIZONS=1,2,4,8")

    for path in files:
        checkpoint = torch.load(
            path, map_location="cpu", weights_only=True
        )
        config = checkpoint["config"]
        width = config["width"]
        ridge = config["ridge"]
        dtype = torch.float64

        class AuditAE(nn.Module):
            def __init__(self):
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Linear(4, 16),
                    nn.Tanh(),
                    nn.Linear(16, width),
                )
                self.decoder = nn.Sequential(
                    nn.Linear(width, 16),
                    nn.Tanh(),
                    nn.Linear(16, 4),
                )

            def forward(self, x):
                assignments = self.encoder(x).softmax(dim=-1)
                return self.decoder(assignments), assignments

        model = AuditAE().to(dtype=dtype)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()

        train_x = checkpoint["train_x"]
        eval_x = checkpoint["eval_x"]
        clean = checkpoint["clean"]
        K = checkpoint["koopman"]
        latent_map = checkpoint["latent_map"]

        n = clean.shape[0]
        if eval_x.shape[0] % n:
            raise RuntimeError("Unexpected evaluation ordering or size.")
        repeats = eval_x.shape[0] // n

        with torch.no_grad():
            _, S = model(train_x)
            _, eval_S = model(eval_x)

            P = S @ torch.linalg.pinv(S)
            Q = S @ torch.linalg.solve(
                S.T @ S + ridge * torch.eye(width, dtype=dtype),
                S.T,
            )
            identity = torch.eye(n, dtype=dtype)

            D = (identity - P) @ K @ P
            D_ridge = (identity - Q) @ K @ Q

            exact_loss = D.square().mean().item()
            ridge_loss = D_ridge.square().mean().item()

            projector_gap = torch.linalg.matrix_norm(P-Q).item()
            K_norm = torch.linalg.matrix_norm(K, ord=2).item()

            root_loss_gap = abs(
                math.sqrt(ridge_loss) - math.sqrt(exact_loss)
            )
            root_loss_bound = 2 * K_norm * projector_gap / n

            if root_loss_gap > root_loss_bound + 1e-10:
                raise RuntimeError(
                    f"Numerical discrepancy bound failed: {path.name}"
                )

            singular_values = torch.linalg.svdvals(S)
            rank = int(torch.linalg.matrix_rank(S).item())

            z = eval_S.clone()
            horizon_metrics = {}

            for horizon in range(1, 9):
                z = z @ latent_map

                if horizon not in (1, 2, 4, 8):
                    continue

                target_indices = (
                    torch.arange(n) + horizon
                ) % n
                target = clean[target_indices].repeat(repeats, 1)
                prediction = model.decoder(z)

                mse = (prediction-target).square().mean().item()
                minimum = z.min().item()
                row_sum_error = (
                    z.sum(dim=1)-1
                ).abs().max().item()

                if not all(
                    math.isfinite(v)
                    for v in (mse, minimum, row_sum_error)
                ):
                    raise RuntimeError("Nonfinite rollout metric")

                horizon_metrics[horizon] = (
                    mse, minimum, row_sum_error
                )

            recorded = checkpoint["metrics"]["decoded_next_mse"]
            reproduced = horizon_metrics[1][0]

            if not math.isclose(
                reproduced, recorded, rel_tol=1e-8, abs_tol=1e-10
            ):
                raise RuntimeError(
                    f"Saved one-step metric did not reproduce: {path.name}"
                )

            row = {
                "seed": checkpoint["seed"],
                "weight": checkpoint["weight"],
                "assignment_rank": rank,
                "smallest_singular_value": singular_values[-1].item(),
                "projector_gap_frobenius": projector_gap,
                "unridged_defect": exact_loss,
                "ridge_defect": ridge_loss,
                "root_loss_gap": root_loss_gap,
                "root_loss_bound": root_loss_bound,
            }

            for horizon, values in horizon_metrics.items():
                mse, minimum, row_sum_error = values
                row[f"mse_h{horizon}"] = mse
                row[f"assignment_min_h{horizon}"] = minimum
                row[f"row_sum_error_h{horizon}"] = row_sum_error

            rows.append(row)

            print(
                f"seed={row['seed']} weight={row['weight']:g}"
                f" h1={row['mse_h1']:.6f}"
                f" h2={row['mse_h2']:.6f}"
                f" h4={row['mse_h4']:.6f}"
                f" h8={row['mse_h8']:.6f}"
            )

    after_hashes = {p.name: file_hash(p) for p in files}
    if before_hashes != after_hashes:
        raise RuntimeError("Checkpoint bytes changed during audit.")

    print("\nROLLOUT SUMMARY")
    for horizon in (1, 2, 4, 8):
        paired_differences = []

        for seed in range(372, 382):
            baseline = next(
                r for r in rows
                if r["seed"] == seed and r["weight"] == 0
            )
            regularized = next(
                r for r in rows
                if r["seed"] == seed and r["weight"] == 1
            )
            paired_differences.append(
                regularized[f"mse_h{horizon}"]
                - baseline[f"mse_h{horizon}"]
            )

        for weight in (0.0, 1.0):
            group = [r for r in rows if r["weight"] == weight]
            errors = [r[f"mse_h{horizon}"] for r in group]

            print(
                f"horizon={horizon} weight={weight:g}"
                f" mean_mse={sum(errors)/len(errors):.6f}"
                f" beats_zero={sum(v < 0.5 for v in errors)}/10"
            )

        print(
            f"horizon={horizon}"
            f" regularized_improved_pairs="
            f"{sum(v < 0 for v in paired_differences)}/10"
        )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    receipt = root / f"checkpoint_audit_{stamp}.csv"

    with receipt.open("x", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print("\nCHECKPOINT_AUDIT=COMPLETE")
    print("ONE_STEP_REPRODUCTION=PASS")
    print("NUMERICAL_RIDGE_BOUND_CHECKS=PASS")
    print("CHECKPOINT_HASHES_UNCHANGED=PASS")
    print("MODELS_AUDITED:", len(rows))
    print("AUDIT_CSV:", receipt)
    print("GENERALIZATION_TO_NEW_DYNAMICS=NOT_TESTED")
    print("HUGGING_FACE_FILES_CHANGED=NO")


run_checkpoint_audit()