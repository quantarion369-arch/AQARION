#!/usr/bin/env python3
"""Classify exact dependencies from the all-600 census."""
import contextlib
import hashlib
import io
import json
import runpy
from collections import Counter

with contextlib.redirect_stdout(io.StringIO()):
    ns = runpy.run_path("all_600_trade_audit.py")

records = ns["records"]

def hist(values):
    return {
        str(k): v
        for k, v in sorted(Counter(values).items())
    }

rows = []
for r in records:
    c = r["dependency"]
    nonzero = [x for x in c if x]
    positive = [x for x in c if x > 0]
    negative = [-x for x in c if x < 0]

    cubic = r["cubic"]
    cubic_vector = list(cubic.values())

    rows.append({
        "support": r["support"],
        "dependency": c,
        "dependency_support_size": len(nonzero),
        "positive_block_count": len(positive),
        "negative_block_count": len(negative),
        "positive_volume": sum(positive),
        "negative_volume": sum(negative),
        "max_abs_coefficient": max(abs(x) for x in c),
        "simple_trade": all(abs(x) == 1 for x in nonzero),
        "cubic_signature": cubic_vector,
        "cubic_nonzero_count": sum(x != 0 for x in cubic_vector),
        "cyclic_realizable": r["cyclic_realizable"],
    })

assert len(rows) == 600
assert all(r["positive_volume"] == r["negative_volume"] for r in rows)
assert all(r["dependency_support_size"] >= 8 for r in rows)

result = {
    "scope": "four-bit Boolean cube; ten-element candidate supports",
    "records": len(rows),
    "dependency_support_size_distribution":
        hist(r["dependency_support_size"] for r in rows),
    "trade_volume_distribution":
        hist(r["positive_volume"] for r in rows),
    "positive_block_count_distribution":
        hist(r["positive_block_count"] for r in rows),
    "negative_block_count_distribution":
        hist(r["negative_block_count"] for r in rows),
    "max_abs_coefficient_distribution":
        hist(r["max_abs_coefficient"] for r in rows),
    "simple_trade_count": sum(r["simple_trade"] for r in rows),
    "weighted_trade_count": sum(not r["simple_trade"] for r in rows),
    "cubic_nonzero_count_distribution":
        hist(r["cubic_nonzero_count"] for r in rows),
    "unique_cubic_signatures": len({
        tuple(r["cubic_signature"]) for r in rows
    }),
    "cyclic_realizable_count": sum(r["cyclic_realizable"] for r in rows),
    "rows": rows,
}

payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
path = "trade_structure_summary.json"
with open(path, "wb") as f:
    f.write(payload + b"\n")

print("AQARION TRADE STRUCTURE SUMMARY")
print("DEPENDENCIES:", len(rows))
for key in (
    "dependency_support_size_distribution",
    "trade_volume_distribution",
    "positive_block_count_distribution",
    "negative_block_count_distribution",
    "max_abs_coefficient_distribution",
    "cubic_nonzero_count_distribution",
):
    print(key.upper() + ":", result[key])
print("SIMPLE TRADES:", result["simple_trade_count"])
print("WEIGHTED TRADES:", result["weighted_trade_count"])
print("UNIQUE CUBIC SIGNATURES:", result["unique_cubic_signatures"])
print("CYCLIC-REALIZABLE:", result["cyclic_realizable_count"])
print("JSON FILE:", path)
print("JSON SHA256:", hashlib.sha256(payload + b"\n").hexdigest())
print("PASS: exact census records classified")
