# Time and Modes — Hosted Computational Checkpoint

## Status

**COMPUTATIONAL_CHECKPOINT_PASS**

This record verifies that the repository’s supplied checks and timing-model
sweeps completed successfully in a hosted GitHub Actions environment.

It does **not** establish physical validation, scientific novelty, historical
priority, formal proof, or reproduction of any externally reported experiment.

## Tested revision

- Repository: `quantarion369-arch/AQARION`
- Branch: `main`
- Tested commit: `71b45894ca5f6ba6bbae9b71e848f65bac3446ce`
- Workflow: `.github/workflows/time-and-modes-check.yml`
- Workflow run: Time and Modes Check #4
- Run ID: `38320884906`
- Artifact ID: `11779142554`
- Artifact ZIP SHA-256: `df286741401af8744ba69e526842ae758d898c99959276873a79b88534cb811b`

## Environment

- Runner operating system: Ubuntu 24.04
- Python: 3.12.15
- NumPy: 2.5.4
- SciPy: 1.18.1
- Dependency source: `requirements.txt`

## Commands executed

The workflow executed the repository’s `run.sh` unchanged:

```bash
python -m py_compile causal_estimator.py test_causal_estimator.py timing_models.py
python -m unittest -v test_causal_estimator
python timing_models.py
