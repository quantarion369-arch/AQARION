from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from math import comb, factorial
import csv
import hashlib
import json
import platform
import sys

ROOT = Path(__file__).resolve().parent
BASE = Path.home() / "AQARION_AUDIT/cycle_ratio/prime-power-step.Q8Gyo6"
BASE_SOURCE = "be36141ea1f15dcbf7bf04c7842df6de2c55b01ec1ead826acac2f552cfbe988"
BASE_RECEIPT = "83fa9e2ff4ec3061d33141063ca883ec2d4c3e2cadca1d61444debc37041073b"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def vp(x, p):
    need(x != 0, "Zero valuation needs separate handling")
    x = abs(x)
    result = 0
    while x % p == 0:
        result += 1
        x //= p
    return result

def save(name, rows):
    path = ROOT / name
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return sha(path.read_bytes())

source = Path(__file__).read_bytes()
raw = (BASE / "receipt.json").read_bytes()
need(sha(raw) == BASE_RECEIPT, "Prior receipt changed")
prior = json.loads(raw)
need(prior["status"] == "PASS", "Prior run not PASS")
need(sha((BASE / "audit.py").read_bytes()) == BASE_SOURCE, "Prior source changed")
need(prior["source_sha256"] == BASE_SOURCE, "Prior source binding differs")
for name, expected in prior["table_sha256"].items():
    need(sha((BASE / name).read_bytes()) == expected, "Prior CSV changed")

primes = [2, 3, 5, 7, 11]
polynomials = {
    "x": lambda x: x,
    "x2": lambda x: x*x,
    "x2_plus_1": lambda x: x*x+1,
    "x_times_xplus1": lambda x: x*(x+1),
    "2x_plus_1": lambda x: 2*x+1,
    "x2_minus_x_plus_1": lambda x: x*x-x+1
}
poly_rows = []
second_rows = []
failures = []
modes = {"strict": 0, "tied_nonzero": 0, "tied_zero": 0}
print("RUNNING=reciprocal polynomial certificates", flush=True)
for name, f in polynomials.items():
    values = []
    elementary = [Fraction(1)]
    for n in range(1, 21):
        values.append(f(n))
        elementary.append(Fraction(0))
        for k in range(n, 0, -1):
            elementary[k] += elementary[k-1]/f(n)
        for p in primes:
            weights = [vp(z, p) for z in values]
            ordered = sorted(weights, reverse=True)
            for k in range(1, n+1):
                L = sum(ordered[:k])
                threshold = ordered[k-1]
                high = [i for i, w in enumerate(weights) if w > threshold]
                tied = [i for i, w in enumerate(weights) if w == threshold]
                h = k-len(high)
                dp = [0]*(h+1)
                dp[0] = 1
                for i in tied:
                    unit = values[i] // p**weights[i]
                    inverse = pow(unit, -1, p)
                    for j in range(h, 0, -1):
                        dp[j] = (dp[j]+inverse*dp[j-1]) % p
                residue = dp[h]
                for i in high:
                    unit = values[i] // p**weights[i]
                    residue = residue*pow(unit, -1, p) % p
                exact = elementary[k]
                actual = vp(exact.numerator, p)-vp(exact.denominator, p)
                strict = k == n or ordered[k-1] > ordered[k]
                mode = "strict" if strict else ("tied_nonzero" if residue else "tied_zero")
                modes[mode] += 1
                valid = actual >= -L
                valid = valid and (actual == -L if residue else actual >= -L+1)
                if not valid:
                    failures.append(["polynomial", name, n, k, p])
                poly_rows.append({
                    "polynomial": name, "n": n, "k": k, "p": p,
                    "top_weight_sum": L, "normalized_residue": residue,
                    "actual_valuation": actual, "mode": mode,
                    "nonintegrality_certified": bool(residue and L > 0),
                    "status": "PASS" if valid else "FAIL"
                })

print("RUNNING=second-kind modular certificates", flush=True)
S = [[0]*41 for _ in range(41)]
S[0][0] = 1
for n in range(1, 41):
    for k in range(1, n+1):
        S[n][k] = k*S[n-1][k]+S[n-1][k-1]
period_checks = 0
for n in range(1, 41):
    for k in range(1, min(n, 12)+1):
        for p in primes:
            modulus = p**3
            residue = sum((-1)**(k-j)*comb(k,j)*pow(j,n,modulus) for j in range(k+1)) % modulus
            exact = factorial(k)*S[n][k]
            actual = vp(exact, p)
            valid = residue == exact % modulus
            valid = valid and (vp(residue,p) == actual if residue else actual >= 3)
            periods = True
            for t in range(1, min(3,n)+1):
                mod = p**t
                period = (p-1)*p**(t-1)
                left = sum((-1)**(k-j)*comb(k,j)*pow(j,n,mod) for j in range(k+1)) % mod
                right = sum((-1)**(k-j)*comb(k,j)*pow(j,n+period,mod) for j in range(k+1)) % mod
                periods = periods and left == right
                period_checks += 1
            valid = valid and periods
            if not valid:
                failures.append(["second_kind", n, k, p])
            second_rows.append({
                "n": n, "k": k, "p": p, "modulus": modulus,
                "factorial_times_S_residue": residue,
                "factorial_times_S_valuation": actual,
                "period_checks_pass": periods,
                "status": "PASS" if valid else "FAIL"
            })

control = Fraction(1,2)+Fraction(1,3)+Fraction(1,6)
need(control == 1, "Tie-cancellation control failed")
if (len(poly_rows),len(second_rows),period_checks) != (6300,2070,6190):
    failures.append(["domain_count_mismatch"])
if Path(__file__).read_bytes() != source:
    failures.append(["source_changed"])
tables = {
    "polynomial_certificates.csv": save("polynomial_certificates.csv",poly_rows),
    "second_kind_certificates.csv": save("second_kind_certificates.csv",second_rows)
}
report = {
    "status": "PASS" if not failures else "FAIL",
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(), "source_sha256": sha(source),
    "table_sha256": tables, "prior_receipt_sha256": BASE_RECEIPT,
    "polynomial_checks": len(poly_rows), "polynomial_modes": modes,
    "second_kind_checks": len(second_rows),
    "modular_periodicity_checks": period_checks,
    "tie_cancellation_control": "E_2(1,1/2,1/3)=1",
    "failures": failures, "general_step_conjecture": "UNPROVED",
    "novelty_clearance": "OPEN", "formal_certification": "OPEN",
    "promotion": False, "git_operations": 0
}
receipt = ROOT / "receipt.json"
with receipt.open("x", encoding="utf-8") as stream:
    json.dump(report,stream,indent=2,sort_keys=True)
print("STATUS="+report["status"])
print("PRIOR_EVIDENCE_BINDINGS=PASS")
print("POLYNOMIAL_CHECKS="+str(len(poly_rows)))
print("SECOND_KIND_CHECKS="+str(len(second_rows)))
print("MODULAR_PERIODICITY_CHECKS="+str(period_checks))
print("FAILURES="+str(len(failures)))
print("SOURCE_SHA256="+sha(source))
print("RECEIPT_SHA256="+sha(receipt.read_bytes()))
print("EVIDENCE_DIRECTORY="+str(ROOT))
print("CSV_DUMP=NO")
print("GIT_OPERATIONS=0")
print("PROMOTION=FALSE")
if failures:
    raise SystemExit(1)
