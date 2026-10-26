# Exact explanation engine 005

Standard-library component for 1–16 states. This is an implementation
limit, not a theorem restriction.

Entry point: `explain(T, labels)` in `explain.py`.
Integer partition labels are normalized in first-occurrence order.
Boolean labels and transitions are rejected.

Reuses the maintained quotient audit for compatibility, the ordered
witness, quotient information, and the exact defect matrix. Reuses the
existing closure-certificate arithmetic without altering its checker.

Reports independent partition and linear stabilization checks,
stable-class annihilators, a generated linear-closure certificate,
and the first rank-increasing product in deterministic basis order.

A product witness is not a minimum-degree or minimum-count repair.
For the bit-swap fixture, the first product may select state 00,
rather than state 11; either supplies the missing direction.

The certificate records C*A=B, K*C=C*M, a nonzero basis minor,
and named time-shift generators for each basis column.
Annihilators are expressed on stable classes, not raw states.

No census, interactive page, formal proof, novelty claim, or automatic
claim promotion is included. The five-state classification is separate.

## Reproduce the focused tests

The recorded local environment uses Python 3.13 and pytest 9.1.1.
The engine uses the standard library; pytest is a test dependency.

From the repository root, run:

    cd AQARION-QUANTARION-AI/research/exact-quotient-agreement/explanation-engine-005
    PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -B -m pytest -o addopts= -p no:cacheprovider -q --tb=short test_explain.py

Keep the repository layout: the engine reuses the sibling
quotient-audit-001 and closure-certificate-004 modules.

The first rank-increasing product supplies one additional direction;
it is not necessarily a complete repair of the linear-closure deficit.

The scoped GitHub Actions workflow uses Python 3.13 and pytest 9.1.1.
It requires exactly eight collected test functions without skips and
preserves a separate JUnit report. Changes to the test count must be
accompanied by a review of the workflow's collection gate.

The local execution receipt records the source revision and test run.
It is not evidence that GitHub-hosted CI has completed successfully.

## Immediate product repair contract

complete_repair reports whether adjoining the returned product vector
to the existing eventual linear span immediately reaches the stable-class
dimension. It does not automatically include subsequent time shifts,
further products, or a minimum-generator calculation.

For T = (1,0,3,1,0,4) and labels = (0,1,0,1,0,0):

    Strict partition sizes:                 2, 4, 6
    Linear dimensions, including check:     2, 3, 4, 4
    Existing eventual span dimension:       4
    First product v = (0,0,0,0,1,1):        rank 5
    complete_repair:                        False
    Kv = (0,0,0,0,0,1), also adjoined:      rank 6
    All pairwise products simultaneously:   rank 6

Thus one product vector is insufficient here, while one nonlinear
generator together with its temporal closure is sufficient.
Product-vector count, nonlinear-generator count, and simultaneous
product-closure rounds are different quantities.

## Historical and current test evidence

The top-level execution.json, test-results.json, and test-output.txt
are historical evidence for the seven-test publication checkpoint
393140e6b19635aaec38a8ed3df2c2e10a6d2dd3. Their recorded source hashes
describe that earlier run, not the subsequently extended test suite.

The extended suite has eight test methods. It independently replays
certificate equations, named generators, the basis minor, and complete
stable-class annihilator relations, with in-memory negative controls.
Fresh evidence must be identified separately from the historical receipts.
