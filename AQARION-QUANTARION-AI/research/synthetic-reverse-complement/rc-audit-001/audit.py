import itertools
import json
import sys

TABLE = str.maketrans("ACGT", "TGCA")

def reverse_complement(sequence):
    return sequence.translate(TABLE)[::-1]

def base_counts(sequence):
    return tuple(sequence.count(base) for base in "ACGT")

checked = 0
failures = 0
examples = []
negative_control = None

for length in range(1, 7):
    for letters in itertools.product("ACGT", repeat=length):
        sequence = "".join(letters)
        transformed = reverse_complement(sequence)
        original = base_counts(sequence)
        changed = base_counts(transformed)

        checks = {
            "involution":
                reverse_complement(transformed) == sequence,
            "GC_count_invariance":
                original[1] + original[2] == changed[1] + changed[2],
            "base_count_equivariance":
                changed == original[::-1],
        }

        for name, passed in checks.items():
            if not passed:
                failures += 1
                if len(examples) < 10:
                    examples.append({
                        "check": name,
                        "sequence": sequence,
                    })

        if negative_control is None and original[0] != changed[0]:
            negative_control = {
                "sequence": sequence,
                "reverse_complement": transformed,
                "original_A_count": original[0],
                "transformed_A_count": changed[0],
            }

        checked += 1

passed = failures == 0 and negative_control is not None

report = {
    "experiment": "RC synthetic audit 001 - saved rerun",
    "domain": "all ACGT sequences of lengths 1 through 6",
    "sequences_checked": checked,
    "property_checks": checked * 3,
    "property_failures": failures,
    "failure_examples": examples,
    "negative_control": negative_control,
    "status": "PASS" if passed else "FAIL",
    "scope": "bounded synthetic software check; no biological inference",
}

print(json.dumps(report, indent=2))
sys.exit(0 if passed else 1)
