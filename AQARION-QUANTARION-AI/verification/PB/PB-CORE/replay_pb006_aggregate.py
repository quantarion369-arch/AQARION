import json, hashlib, subprocess, sys, math
from functools import lru_cache

@lru_cache(maxsize=None)
def p(n):  # partition number
    if n == 0: return 1
    return sum((-1)**k * p(n - k*(3*k-1)//2) for k in range(1, n+1) if n - k*(3*k-1)//2 >= 0) * -1 if False else _part(n)

def _part(n):
    if n == 0: return 1
    total = 0
    for k in range(1, n+1):
        for s in (1, -1):
            m = k*(3*k-s)//2
            if m > n: break
            total += (-1)**(k+1) * _part(n-m)
    return total

def A(n):
    return sum(math.comb(n,k)*math.factorial(k)*p(k)*k*n**(n-k-1) for k in range(1,n)) + math.factorial(n)*p(n)

REFERENCE = {1:1,2:6,3:51,4:592,5:8565,6:148896,7:3018127,8:69844608,9:1816084233,10:52399129600,11:1660832066091,12:57351480413184}

results = [{"n":n,"value":A(n),"matches_reference":A(n)==REFERENCE[n]} for n in range(1,13)]
commit = subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
script_bytes = open(__file__,"rb").read()
receipt_path = "AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-006-AGGREGATE-REPLAY.json"

receipt = {
  "schema": "AQ-PB006-AGGREGATE-REPLAY/2",
  "formula": "A_n = sum_{k=1}^{n-1} C(n,k)*k!*p(k)*k*n^(n-k-1) + n!*p(n)",
  "scope": {"n_min":1,"n_max":12},
  "results": results,
  "all_match": all(r["matches_reference"] for r in results),
  "status": "PASS" if all(r["matches_reference"] for r in results) else "FAIL",
  "provenance": {
    "source_commit": commit,
    "verifier_hash": hashlib.sha256(script_bytes).hexdigest(),
    "command": f"python3 {__file__}",
    "python_version": sys.version,
    "receipt_path": receipt_path
  }
}
json.dump(receipt, open(receipt_path,"w"), indent=2)
print(receipt["status"], "| commit:", commit[:12], "| all_match:", receipt["all_match"])
