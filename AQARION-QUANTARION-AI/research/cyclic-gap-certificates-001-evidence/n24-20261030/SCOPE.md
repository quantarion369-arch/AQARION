# Cyclic-gap n=24 evidence — 2026-10-30

## Preserved local artifacts
- witness_audit.py: copied from AQARION_N24_AUDIT.
- witness_audit.log: copied from AQARION_N24_AUDIT.
- SHA256SUMS: portable manifest for the two files above.

## Mathematical claims reported in the research session
- G(24)=14; L(24)=13.
- The reported maximizing cyclotomic signature is {4,12,24}.
- Two displayed binary words have 24 rotations and reported direct gap 14.
- Corrected cofactors reported for those words:
  - first: 1+z+z^2+z^3+z^4+z^5+z^6
  - second: 1+z+z^2+z^4+z^5
- The pasted cert24.py output reports exact integer multiplication/division,
  numerical root evaluations, and direct-rank checks.
- The pasted cg3.py output reports G(n)=L(n) for n=25,26,27,28.

## Evidence limitations
The corrected cert24.py, cg3.py, their complete source files, and full
enumeration receipts were not present in the local AQARION_N24_AUDIT
directory when this package was assembled. The n=25..28 enumeration
results are therefore session-reported results, not independently
replayable from this directory.

Floating-point root evaluations are diagnostic, not exact certificates.
No Lean verification, CLAIMLOCK certification, novelty determination,
or promotion is claimed.

Status: RESEARCH EVIDENCE ONLY — NOT PROMOTED.
