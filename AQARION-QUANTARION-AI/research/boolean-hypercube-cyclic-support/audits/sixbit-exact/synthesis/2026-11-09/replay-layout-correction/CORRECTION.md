# Additive replay-layout correction

Release under correction:
755fdabb5aa067c06f441eea2c32c25fa46bae81

The fresh-output instructions omit copying the execution source into
the output directory before running it.

Odd-twelve Stage 2 requires reconstruct.py in its predecessor directory.
The odd-eight successor requires check.py in the pilot directory and
in the pilot manifest.

The original Termux wrappers supplied those files before execution.
Calling the archived Python programs with unrelated fresh output
directories does not reproduce that layout.

replay.py copies a hash-verified archived source into a fresh directory
before execution. Existing evidence and manifests remain unchanged.

Status: wrapper written; not yet executed or clean-environment validated.
No numerical claim is changed by this correction.

Use --help for invocation syntax. Run predecessor stages first, then pass
the printed fresh output path with --previous to the corresponding
successor stage.

replay.log and WRAPPER-RECEIPT.json are wrapper additions and are not
retroactively inserted into the checker's original manifest.
