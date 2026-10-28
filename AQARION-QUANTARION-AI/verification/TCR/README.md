# TCR verification evidence

## Location

The temporal-circuit evidence package is preserved at:

    temporal-circuits-001/

It was first published at commit
20a43b7235dd72c5158b40c5312d545907b79229 under:

    AQARION-QUANTARION-AI/research/separating-register-verification/temporal-circuits-001/

The package has subsequently been relocated intact into verification/TCR.
Its original publication manifest records its historical preparation
destination. That historical field has deliberately not been rewritten.

## Scope

The package preserves completed local experiment sources, outputs,
checksums, and written scope/proof notes. Read its README for the exact
finite coverage and limitations.

Relocation and checksum verification do not constitute a fresh experiment
replay, formal proof certificate, novelty clearance, or claim promotion.

## Workflow status

No TCR-specific workflow is introduced by this organization step.
A future integrity workflow must distinguish archive verification from
fresh execution of the archived experiments.

## Current integrity and regression checks

The subsequent TCR Evidence Verification workflow is defined in
`.github/workflows/tcr-evidence.yml`.

From the repository root:

    python3 -I -B AQARION-QUANTARION-AI/verification/TCR/verify_evidence.py
    python3 -I -B AQARION-QUANTARION-AI/verification/TCR/test_integrity.py

The first command checks both package manifests and reruns only the
nine small scalar fixtures and ten count-formula arithmetic checks.
The second tests rejection of damaged disposable evidence packages.

It does not rerun the archived family/classification censuses, prove the
written theorems formally, or establish novelty. GitHub execution must
be checked separately after publication.

`OBSERVATION_POLYNOMIAL.md` supplies the individual-observation addendum.
