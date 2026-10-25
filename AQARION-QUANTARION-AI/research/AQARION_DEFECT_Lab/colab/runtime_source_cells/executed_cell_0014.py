import csv
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch import nn


def audit_ridge_components():
    torch.set_num_threads(1)

    root = Path(
        "aqarion_defect_results/"
        "replication_20261025T025032399216Z"
    )
    expected = {
        f"seed_{seed}_weight_{weight}.pt"
        for seed in range(372, 382)
        for weight in (0, 1)
    }
    files = sorted(root.glob("*.pt"))

    if {p.name for p in files} != expected:
        raise RuntimeError("Expected the 20 saved replication checkpoints.")

    rows = []
    print("START: ridge component decomposition")
    print("TRAINING=NONE")

    with torch.no_grad():
        for path in files:
            checkpoint = torch.load(
                path, map_location="cpu", weights_only=True
            )
            width = checkpoint["config"]["width"]
            ridge = checkpoint["config"]["ridge"]

            encoder = nn.Sequential(
                nn.Linear(4, 16),
                nn.Tanh(),
                nn.Linear(16, width),
            ).to(dtype=torch.float64)

            encoder_state = {
                name[len("encoder."):]: value
                for name, value in checkpoint["model_state_dict"].items()
                if name.startswith("encoder.")
            }
            encoder.load_state_dict(encoder_state)
            encoder.eval()

            S = encoder(checkpoint["train_x"]).softmax(dim=-1)
            K = checkpoint["koopman"]
            n = S.shape[0]

            identity = torch.eye(n, dtype=S.dtype)
            cluster_eye = torch.eye(width, dtype=S.dtype)

            P = S @ torch.linalg.pinv(S)
            Q = S @ torch.linalg.solve(
                S.T @ S + ridge * cluster_eye,
                S.T,
            )

            full = (identity-Q) @ K @ Q
            outside = (identity-P) @ K @ Q
            inside = (P-Q) @ K @ Q
            exact = (identity-P) @ K @ P

            assert torch.allclose(
                full, outside+inside, atol=1e-10, rtol=1e-8
            )

            full_loss = full.square().mean().item()
            outside_loss = outside.square().mean().item()
            inside_loss = inside.square().mean().item()
            exact_loss = exact.square().mean().item()

            assert abs(
                full_loss-outside_loss-inside_loss
            ) < 1e-10

            singular_values = torch.linalg.svdvals(S)

            row = {
                "seed": checkpoint["seed"],
                "weight": checkpoint["weight"],
                "ridge_loss": full_loss,
                "outside_component_loss": outside_loss,
                "inside_component_loss": inside_loss,
                "inside_fraction": (
                    inside_loss/full_loss if full_loss > 0 else 0.0
                ),
                "exact_defect_loss": exact_loss,
                "smallest_singular_value": singular_values[-1].item(),
                "projector_gap_frobenius": (
                    torch.linalg.matrix_norm(P-Q).item()
                ),
            }
            rows.append(row)

            print(
                f"seed={row['seed']} weight={row['weight']:g}"
                f" ridge={full_loss:.8f}"
                f" outside={outside_loss:.8f}"
                f" inside={inside_loss:.8e}"
                f" inside_percent={100*row['inside_fraction']:.4f}"
            )

    print("\nCOMPONENT SUMMARY")
    for weight in (0.0, 1.0):
        group = [r for r in rows if r["weight"] == weight]
        total_ridge = sum(r["ridge_loss"] for r in group)
        total_inside = sum(r["inside_component_loss"] for r in group)

        pooled_fraction = (
            total_inside/total_ridge if total_ridge > 0 else 0.0
        )
        maximum_fraction = max(r["inside_fraction"] for r in group)

        print(
            f"weight={weight:g}"
            f" pooled_inside_percent={100*pooled_fraction:.6f}"
            f" max_individual_inside_percent="
            f"{100*maximum_fraction:.6f}"
        )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    receipt = root / f"ridge_components_{stamp}.csv"

    with receipt.open("x", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print("\nRIDGE_COMPONENT_DECOMPOSITION=COMPLETE")
    print("DECOMPOSITION_IDENTITIES=PASS")
    print("CHECKPOINTS_REWRITTEN=NO")
    print("RESULT_CSV:", receipt)
    print("TRAINING_BEHAVIOR_DURING_OPTIMIZATION=NOT_RECONSTRUCTED")
    print("HUGGING_FACE_FILES_CHANGED=NO")


audit_ridge_components()