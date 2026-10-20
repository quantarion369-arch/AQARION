# Degree-four cyclic classifier: Termux execution receipt

Execution date: 2026-10-20.

This directory preserves the original classifier and a successful Termux
execution of its `all` and `validate` modes. It does not replace earlier
receipts or claim a GitHub Actions execution.

Source SHA-256:
a7075338a20cd4b3734de877b22bc74b8d0ef00b159864eed810e47c18a80363

## Classification scope

Nonzero binary words with absent primitive-order Fourier component,
Fourier support generating the full cyclic group, and sumset degree
at least four.

## Recorded results

- Lengths 2 through 71: 25 surviving abstract support patterns;
  zero realizing qualifying binary words.
- Length 24, threshold three: 48 qualifying words.
- Length 72, threshold four: 432 qualifying words.
- All 432 length-72 words have active orders (1,2,8,9,18) and degree four.
- Both process exits are zero; wrapper acceptance is PASS.

Counts refer to words, not symmetry classes.

## Evidence and limitations

SHA256SUMS preserves the original receipt-file identities.
The classifier requires NumPy. The receipt does not include a complete
environment capture or a source-repository commit identifier.

The classifier prints classifications; the replay wrapper separately checked
the expected output and recorded acceptance. The wrapper itself is not
included in this directory.

This is bounded computational evidence. It does not establish the infinite
family theorem, novelty, Lean verification, or remote CI execution.

## Optional future replay

python3 -I min_length_classify_standalone.py all
python3 -I min_length_classify_standalone.py validate

No replay was performed while preparing this publication commit.
