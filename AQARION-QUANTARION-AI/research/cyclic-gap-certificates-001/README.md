# Cyclic gap certificates 001

Standalone research verifier. No production imports or registry changes.
Dependency: SymPy 1.14.0. Written arguments are in PROOF.md.

Run verify_cyclic_gap.py --exhaustive --output-dir NEW_DIRECTORY.
The directory must not exist. Keep receipts outside the source package.
To recheck a saved certificate add --certificate PATH_TO_CERTIFICATE.

Tests: all 1022 binary words of lengths 1-9, each as list and tuple;
direct and gcd ranks; constant boundaries; three certificate corruptions;
five invalid inputs; prime-power attaining constructions through length 32;
length-18 low-rank support masks.

This is a compact revised implementation, not byte-identical to the earlier
downloadable packet. It does not run production CLAIMLOCK, prove novelty,
or mechanically verify the written mathematical arguments.
