# Verified additive replay correction

Active wrapper: ../replay-v2.py

The original replay.py is superseded and retained as history. The earlier CORRECTION.md statement that the wrapper had not been executed describes the earlier checkpoint, not this one.

Both fresh replay chains passed in the existing Termux environment using a detached frozen checkout. All four processes exited zero and all checker manifests passed verification after process completion.

The V2 wrapper places logs and wrapper receipts outside checker output directories. It copies unchanged archived sources into fresh run directories before execution.

This is not a clean dependency-installation test. It does not retroactively validate the original published recipe verbatim. No formal proof, peer review, or novelty certification is supplied.

Use PORTABLE-INDEX.json for repository-relative copies. Original report paths and hashes are preserved unchanged.
