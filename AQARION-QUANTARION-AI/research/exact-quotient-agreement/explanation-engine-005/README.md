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
It requires exactly seven collected test functions without skips and
preserves a separate JUnit report. Changes to the test count must be
accompanied by a review of the workflow's collection gate.

The local execution receipt records the source revision and test run.
It is not evidence that GitHub-hosted CI has completed successfully.
