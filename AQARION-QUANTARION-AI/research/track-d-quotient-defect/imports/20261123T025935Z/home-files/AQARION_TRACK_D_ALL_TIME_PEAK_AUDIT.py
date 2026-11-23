#!/usr/bin/env python3
from fractions import Fraction as F
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import sys

OUT = Path.home() / "AQARION_TRACK_D_ALL_TIME_PEAK_RECEIPT.txt"
SRC = Path(__file__)
checks = 0
cases = 0

def check(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)

def tau(s):
    if s <= 1:
        return F(1)
    return F(1, 2 ** (s - 1))

def direct_B(delta, t):
    alpha = F(1, 2) + delta
    return sum(
        (delta * alpha**r * tau(t - 1 - r)
         for r in range(t)),
        F(0)
    )

def closed_B(delta, t):
    alpha = F(1, 2) + delta
    C = F(1, 2) + delta * (1 + alpha)
    if t == 1:
        return delta
    return C * alpha**(t - 2) - F(1, 2**(t - 1))

def main():
    global cases

    print("AQARION TRACK D ALL-TIME PEAK AUDIT")
    print("ARITHMETIC=EXACT_FRACTION")
    print("DELTA_GRID=1/100,...,25/100")
    print("FORMULA=EXACT_CLOSED_FORM")
    print()

    threshold = (F(2) ** F(1, 2) - 1) / 2
    # The threshold is irrational. Use the equivalent exact
    # rational sign test delta^2 + delta - 1/4.
    peak_counts = {2: 0, 3: 0}
    global_peak = F(-1)
    global_peak_cases = []

    for j in range(1, 26):
        delta = F(j, 100)
        alpha = F(1, 2) + delta
        C = F(1, 2) + delta * (1 + alpha)

        cases += 1

        # Exact direct convolution equals closed form.
        for t in range(1, 101):
            check(
                direct_B(delta, t) == closed_B(delta, t),
                f"closed-form mismatch delta={delta}, t={t}"
            )

        # Exact recurrence:
        # B_(t+1) = alpha*B_t + delta*tau(t).
        for t in range(1, 100):
            lhs = closed_B(delta, t + 1)
            rhs = alpha * closed_B(delta, t) + delta * tau(t)
            check(lhs == rhs, f"recurrence mismatch {delta=} {t=}")

        # Peak classification by exact polynomial sign.
        sign = delta * delta + delta - F(1, 4)
        predicted_peak = 3 if sign > 0 else 2
        peak_counts[predicted_peak] += 1

        # Check the predicted peak against a long exact horizon.
        values = [closed_B(delta, t) for t in range(1, 501)]
        actual_peak = max(range(1, 501), key=lambda t: values[t-1])
        check(actual_peak == predicted_peak,
              f"peak mismatch delta={delta}: "
              f"predicted={predicted_peak}, actual={actual_peak}")

        # Check monotonic tail beginning at t=3.
        for t in range(3, 500):
            check(
                closed_B(delta, t + 1) <= closed_B(delta, t),
                f"tail not decreasing delta={delta}, t={t}"
            )

        # Check the analytic sufficient inequality:
        # C(1-alpha)alpha >= 1/8.
        check(
            C * (1 - alpha) * alpha >= F(1, 8),
            f"analytic tail inequality failed delta={delta}"
        )

        peak_value = values[actual_peak - 1]
        if peak_value > global_peak:
            global_peak = peak_value
            global_peak_cases = [(delta, actual_peak)]
        elif peak_value == global_peak:
            global_peak_cases.append((delta, actual_peak))

        print(
            f"DELTA={delta} ALPHA={alpha} "
            f"PEAK_T={actual_peak} PEAK={peak_value} "
            f"TAIL=PASS"
        )

    # Verify the closed-form difference formula:
    # B_(t+1)-B_t = 2^(-t) - C(1-alpha)alpha^(t-2).
    for j in range(1, 26):
        delta = F(j, 100)
        alpha = F(1, 2) + delta
        C = F(1, 2) + delta * (1 + alpha)
        for t in range(3, 100):
            lhs = closed_B(delta, t + 1) - closed_B(delta, t)
            rhs = F(1, 2**t) - C * (1-alpha) * alpha**(t-2)
            check(lhs == rhs, "difference identity mismatch")

    print()
    print("=== FINAL RECEIPT ===")
    print(f"CASES={cases}")
    print(f"CHECKS_PASSED={checks}")
    print(f"PEAK_AT_T2={peak_counts[2]}")
    print(f"PEAK_AT_T3={peak_counts[3]}")
    print(f"GLOBAL_GRID_MAX={global_peak}")
    print(f"GLOBAL_GRID_MAX_CASES={global_peak_cases}")
    print("CLOSED_FORM=EXACT")
    print("RECURRENCE=EXACT")
    print("TAIL_MONOTONICITY_GRID=PASS")
    print("ANALYTIC_TAIL_INEQUALITY_GRID=PASS")
    print("LEAN_PROOF=NOT_RUN")
    print("NOVELTY=NOT_CLAIMED")
    print("STATUS=COMPLETED_ALL_TIME_PEAK_AUDIT")

if __name__ == "__main__":
    start = datetime.now(timezone.utc).isoformat()
    try:
        main()
        status = 0
    except Exception as exc:
        print(f"AUDIT_FAILURE={type(exc).__name__}: {exc}")
        status = 1

    end = datetime.now(timezone.utc).isoformat()
    with OUT.open("w") as f:
        f.write("AQARION TRACK D ALL-TIME PEAK AUDIT RECEIPT\n")
        f.write(f"UTC_START={start}\n")
        f.write(f"UTC_END={end}\n")
        f.write(f"EXIT={status}\n")
        f.write(f"SOURCE={SRC}\n")
        f.write(f"SOURCE_SHA256={sha256(SRC.read_bytes()).hexdigest()}\n")
        f.write(f"STATUS={'PASS' if status == 0 else 'FAIL'}\n")

    print(f"RUN_EXIT={status}")
    print(f"RECEIPT={OUT}")
    sys.exit(status)
