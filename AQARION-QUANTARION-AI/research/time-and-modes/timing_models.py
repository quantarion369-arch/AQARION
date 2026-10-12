"""Mechanical-displacement and series-RLC-current validation sweeps."""

import csv
import hashlib
import json
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp


OMEGA0 = 2 * np.pi
ZETA = 0.05
F0 = 1.0

L = 1.0
C = 1.0 / OMEGA0**2
R = 2 * ZETA * OMEGA0 * L
V0 = 1.0

RATIOS = np.linspace(0.5, 1.5, 41)
RTOL = 1e-8
ATOL = 1e-10
TOTAL_CYCLES = 100
MEASURE_CYCLES = 10
MEASURE_SAMPLES = 4001
MAX_RELATIVE_ERROR = 1e-3


def mechanical_rhs(t, state, omega_d):
    x, velocity = state
    return [
        velocity,
        F0 * np.cos(omega_d * t)
        - 2 * ZETA * OMEGA0 * velocity
        - OMEGA0**2 * x,
    ]


def rlc_rhs(t, state, omega_d):
    q, current = state
    return [
        current,
        (V0 * np.cos(omega_d * t) - R * current - q / C) / L,
    ]


def run_sweep(kind):
    rows = []

    for ratio in RATIOS:
        omega_d = float(ratio * OMEGA0)
        period = 2 * np.pi / omega_d
        end = TOTAL_CYCLES * period
        times = np.linspace(
            end - MEASURE_CYCLES * period,
            end,
            MEASURE_SAMPLES,
        )

        rhs = mechanical_rhs if kind == "mechanical" else rlc_rhs
        solution = solve_ivp(
            lambda t, y: rhs(t, y, omega_d),
            (0, end),
            [0.0, 0.0],
            t_eval=times,
            max_step=period / 30,
            rtol=RTOL,
            atol=ATOL,
        )

        if not solution.success:
            raise RuntimeError(solution.message)
        if not np.all(np.isfinite(solution.y)):
            raise RuntimeError("Nonfinite solver output")

        if kind == "mechanical":
            signal = solution.y[0]
            expected = F0 / np.sqrt(
                (OMEGA0**2 - omega_d**2)**2
                + (2 * ZETA * OMEGA0 * omega_d)**2
            )
        else:
            signal = solution.y[1]
            expected = V0 / np.hypot(
                R,
                omega_d * L - 1 / (omega_d * C),
            )

        measured = float(np.ptp(signal) / 2)
        relative_error = float(abs(measured / expected - 1))

        rows.append({
            "frequency_ratio": float(ratio),
            "omega_d_rad_s": omega_d,
            "measured_amplitude": measured,
            "analytic_amplitude": float(expected),
            "relative_error": relative_error,
        })

    return rows


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(rows[0]),
        )
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(rows, unit):
    peak = max(
        rows,
        key=lambda row: row["measured_amplitude"],
    )
    error = max(row["relative_error"] for row in rows)

    return {
        "observable_unit": unit,
        "sampled_peak": peak,
        "maximum_relative_error": error,
        "acceptance_threshold": MAX_RELATIVE_ERROR,
        "comparison_pass": bool(error <= MAX_RELATIVE_ERROR),
    }


def main():
    mechanical = run_sweep("mechanical")
    electrical = run_sweep("rlc")

    summaries = {
        "mechanical_displacement": summarize(
            mechanical,
            "model units",
        ),
        "rlc_current": summarize(electrical, "A"),
    }
    passed = all(
        item["comparison_pass"] for item in summaries.values()
    )

    out = Path(
        tempfile.mkdtemp(
            prefix="timing-models-",
            dir=str(Path.cwd()),
        )
    )
    mechanical_path = out / "mechanical_sweep.csv"
    electrical_path = out / "rlc_current_sweep.csv"

    write_csv(mechanical_path, mechanical)
    write_csv(electrical_path, electrical)

    source = Path(__file__).resolve()
    receipt = {
        "schema": "AQ-TIMING-MODELS/0.1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": (
            "MODEL_COMPARISON_PASS"
            if passed
            else "MODEL_COMPARISON_FAIL"
        ),
        "source_sha256": digest(source),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "omega0_rad_s": float(OMEGA0),
            "zeta": ZETA,
            "mechanical_force_amplitude": F0,
            "L_H": L,
            "C_F": float(C),
            "R_ohm": float(R),
            "voltage_peak_V": V0,
            "rtol": RTOL,
            "atol": ATOL,
            "total_cycles": TOTAL_CYCLES,
            "measurement_cycles": MEASURE_CYCLES,
            "measurement_samples": MEASURE_SAMPLES,
            "frequency_ratios": RATIOS.tolist(),
        },
        "results": summaries,
        "output_sha256": {
            mechanical_path.name: digest(mechanical_path),
            electrical_path.name: digest(electrical_path),
        },
        "limitations": [
            "Known illustrative linear models; no hardware measurements.",
            "RLC charge equation deliberately maps to mechanical displacement.",
            "Amplitude uses sampled extrema; no continuous-peak guarantee.",
            "Fixed force or voltage amplitude is not fixed delivered energy.",
            "No vortex-ring data, two-pulse test, or new-physics claim.",
        ],
    }

    newline = chr(10)
    receipt_path = out / "run-receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + newline,
        encoding="utf-8",
    )

    entries = [
        (mechanical_path, mechanical_path.name),
        (electrical_path, electrical_path.name),
        (receipt_path, receipt_path.name),
        (source, "SOURCE:timing_models.py"),
    ]
    checksum_lines = [
        f"{digest(path)}  {name}"
        for path, name in entries
    ]
    (out / "SHA256SUMS").write_text(
        newline.join(checksum_lines) + newline,
        encoding="utf-8",
    )

    print(json.dumps(summaries, indent=2))
    print("Output directory:", out)
    print("Status:", receipt["status"])

    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
