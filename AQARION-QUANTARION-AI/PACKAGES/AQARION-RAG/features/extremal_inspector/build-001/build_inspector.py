import hashlib
import itertools
import json
import platform
from pathlib import Path
import runpy
import subprocess
import sys
from collections import Counter

repo = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()

SOURCE_COMMIT = "d4aa19bba59385fce3be7856ff2384820f2f036e"
PACKAGE = (
    "AQARION-QUANTARION-AI/research/"
    "separating-register-verification"
)

BASELINE = (0, 2, 4, 6, 0, 2, 4, 6)
OBSERVATION = (0, 0, 0, 0, 1, 1, 1, 1)

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(
        ["git", "--no-optional-locks", "-C", str(repo), *args]
    )

before_head = git("rev-parse", "HEAD")
before_status = git("status", "--porcelain")

manifest_relative = PACKAGE + "/PACKAGE-SHA256SUMS"

manifest_bytes = git(
    "show", SOURCE_COMMIT + ":" + manifest_relative
)

require(
    (repo / manifest_relative).read_bytes() == manifest_bytes,
    "Published package manifest differs from the working copy",
)

manifest = {}

for line in manifest_bytes.decode().splitlines():
    expected, relative = line.split("  ", 1)
    manifest[relative] = expected

checker_relative = "cubic-exact-001/exact_cubic_check.py"
checker_path = repo / PACKAGE / checker_relative

require(
    sha(checker_path.read_bytes()) == manifest[checker_relative],
    "Existing exact checker checksum mismatch",
)

# Reuse the preserved standard-library rational checker.
reference = runpy.run_path(str(checker_path))
rank = reference["exact_rank"]
feature_matrix = reference["feature_matrix"]
itinerary_words = reference["itinerary_words"]

recognizer_namespace = runpy.run_path(
    str(output / "recognizer.py")
)
recognize = recognizer_namespace["recognize_extremal"]

invalid_inputs = [
    ([], []),
    ([0, 1, 2], [0, 0, 1]),
    ([0, 2], [0, 1]),
    ([0, 1], [0]),
    ([0, 1], [False, 1]),
    ([0, 1], [0, 2]),
    (None, [0, 1]),
]

for T, h in invalid_inputs:
    try:
        recognize(T, h)
    except ValueError:
        pass
    else:
        raise AssertionError("Malformed input was not rejected")

cache = {}
cases = {}
histogram = Counter()

def analyze(T):
    words = itinerary_words(T, OBSERVATION)

    profiles = []
    for degree in range(4):
        matrix, _ = feature_matrix(words, 8, degree)
        profiles.append(rank(matrix))

    rows = []

    for initial in range(8):
        x = initial
        row = []

        for _ in range(8):
            row.append(OBSERVATION[x])
            x = T[x]

        rows.append(row)

    recognition = recognize(T, OBSERVATION)

    computed_extremal = (
        len(words) == 8 and profiles[2] < 8
    )

    require(
        (recognition["classification"] == "EXTREMAL_REGISTER")
        == computed_extremal,
        "Recognizer disagrees with exact-rank comparison",
    )

    if recognition["classification"] == "EXTREMAL_REGISTER":
        require(
            recognition["rank_profile_theorem_derived"] == profiles,
            "Theorem profile differs from computed profile",
        )

        weights = recognition["certificate"]["state_weights"]

        for degree in range(3):
            for coordinates in itertools.combinations(range(8), degree):
                moment = 0

                for weight, row in zip(weights, rows):
                    value = 1
                    for t in coordinates:
                        value *= row[t]
                    moment += weight * value

                require(
                    moment == 0,
                    "Constructed parity certificate failed",
                )

    # Examine the original baseline weights on the changed system.
    baseline_weights = [
        (-1) ** bin(x).count("1")
        for x in range(8)
    ]

    broken = None

    for degree in range(3):
        for coordinates in itertools.combinations(range(8), degree):
            moment = 0

            for weight, row in zip(baseline_weights, rows):
                value = 1
                for t in coordinates:
                    value *= row[t]
                moment += weight * value

            if moment:
                broken = {
                    "temporal_coordinates": list(coordinates),
                    "weighted_sum": moment,
                }
                break

        if broken is not None:
            break

    return {
        "T": list(T),
        "distinct_itineraries_computed": len(words),
        "rank_profile_computed_exactly": profiles,
        "recognition": recognition,
        "state_itineraries": rows,
        "first_broken_baseline_feature": broken,
    }

for source in range(8):
    for target in range(8):
        changed = list(BASELINE)
        changed[source] = target
        T = tuple(changed)

        if T not in cache:
            cache[T] = analyze(T)
            histogram[
                cache[T]["recognition"]["classification"]
            ] += 1

        cases[f"{source}:{target}"] = cache[T]

require(len(cache) == 57, "Expected 57 distinct one-edge maps")

require(
    dict(histogram) == {
        "EXTREMAL_REGISTER": 1,
        "NONLITERAL_TERMINAL": 8,
        "PREFIX_COLLISION": 48,
    },
    "Unexpected classification histogram",
)

require(
    cases["7:6"]["rank_profile_computed_exactly"] == [1, 4, 7, 8],
    "Baseline profile mismatch",
)
require(
    cases["7:7"]["rank_profile_computed_exactly"] == [1, 5, 8, 8],
    "One-edge mutation profile mismatch",
)

data = {
    "mode": "PRECOMPUTED_EXACT_ONE_EDGE_CASES",
    "baseline": list(BASELINE),
    "observation": list(OBSERVATION),
    "source_commit_for_reference_checker": SOURCE_COMMIT,
    "reference_checker_sha256": sha(checker_path.read_bytes()),
    "recognizer_sha256": sha(
        (output / "recognizer.py").read_bytes()
    ),
    "unique_maps": len(cache),
    "classification_histogram": dict(histogram),
    "cases": cases,
}

(output / "cases.json").write_text(
    json.dumps(data, indent=2) + "\n",
    encoding="utf-8",
)

template = (output / "page-template.html").read_text(encoding="utf-8")
embedded = json.dumps(data, separators=(",", ":")).replace(
    "<", "\\u003c"
)

(output / "inspector.html").write_text(
    template.replace("__CASE_DATA__", embedded),
    encoding="utf-8",
)

require(
    git("rev-parse", "HEAD") == before_head
    and git("status", "--porcelain") == before_status,
    "Repository state changed",
)

report = {
    "status": "PASS",
    "unique_maps_checked": len(cache),
    "selectable_source_target_pairs": len(cases),
    "classification_histogram": dict(histogram),
    "malformed_input_controls": len(invalid_inputs),
    "exact_rank_comparisons": "PASS",
    "positive_parity_certificate_checks": "PASS",
    "baseline_profile": [1, 4, 7, 8],
    "one_edge_mutation_profile": [1, 5, 8, 8],
    "repository_state_unchanged": True,
    "browser_interaction": "USER_CHECK_PENDING",
    "production_RAG_integration": "NOT_INSTALLED",
    "python": sys.version,
    "platform": platform.platform(),
    "dependencies": "Python standard library only",
}

(output / "verification.json").write_text(
    json.dumps(report, indent=2) + "\n",
    encoding="utf-8",
)

print("MALFORMED_INPUT_CONTROLS=7/7")
print("DISTINCT_ONE_EDGE_MAPS=57")
print("SELECTABLE_EDGE_CHOICES=64")
print("EXTREMAL_REGISTER=1")
print("NONLITERAL_TERMINAL=8")
print("PREFIX_COLLISION=48")
print("EXACT_RANK_COMPARISONS=PASS")
print("POSITIVE_PARITY_CERTIFICATES=PASS")
print("BASELINE_PROFILE=[1,4,7,8]")
print("ONE_EDGE_MUTATION_PROFILE=[1,5,8,8]")
print("REPOSITORY_STATE_UNCHANGED=YES")
print("RAG_ROUTES_CHANGED=NO")
print("BROWSER_INTERACTION=USER_CHECK_PENDING")
print("OVERALL_BUILD_STATUS=PASS")
