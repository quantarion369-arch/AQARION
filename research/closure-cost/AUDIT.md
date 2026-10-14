# Audit and evidence record — 2026-10-14

## Locally executed by repository owner

- Independent bound sweep through n=4: 3,984 cases, zero violations.
- Regression suite: four passed, one optional n=5 test skipped.
- Reconstructed implementation cross-check: 3,984 cases,
  zero profile/linear-cost mismatches and zero self-check failures.
- Actual production-source cross-check: same counts and zero failures.
- Production source SHA-256:
  e97325fedd0ee6a5d9223003b857358ce5ba303c483603b36215eb233f115db1
- Witness T=(0,1,0), labels=(0,0,1):
  D=(I-P)KP is zero, rank zero.
- Checks share components; not all are independent implementations.

## Assistant execution reported in the work session

Perplexity ran a separate exact-rational implementation:
- 3,984 map-partition cases through n=4.
- 1,908 upper equalities: 1,836 trivial and 72 nontrivial.
- No failures of the bound or maximal-splitting criterion.
- Boolean truth tables:
  d=2: 16 tables, 6 rational-affine.
  d=3: 256 tables, 8 rational-affine.
  d=4: 65,536 tables, 10 rational-affine.

GPT supplied execution reports and code with matching totals.
These assistant runs were not executions in the owner's checkout.
Their full execution artifacts have not been archived here.

## Explicit witnesses independently checked in the assistant session

Non-bijection:
  T=(0,0,1,2,2,1,5,5)
  labels=(0,1,0,0,1,1,0,1)

Permutation with duplicate itineraries:
  T=(1,2,0,4,5,3,7,6,8)
  labels=(0,0,1,0,1,1,0,0,1)

Both have dimensions 2,3,4,4, positive profile (1,1),
s=8, C=2, and upper equality s-k=6.
Thus bijectivity and s=|X| are not necessary for attainment.

## Claude-reported extended computations

Not locally replayed or fully archived:
- n=5 exhaustive: 162,500 cases, zero violations.
- n=6: 1,500 random maps, all partitions; 304,500 cases.
- n=7,8: 800 random maps, k<=3; 510,700 cases.
- Reconstructed-code cross-check through n=5:
  166,484 cases, zero mismatches/self-check failures.
- Further equality sweeps and shift-register constructions reported.

Complete graph enumerator, search scripts, and raw outputs remain
pending export. Truncated command logs are not complete artifacts.
No claim of independent replay of those extended results is made.

## Review disposition

Paper arguments for the bound, stabilization, upper equality, and
binary characterization were reviewed favorably in the session.
Computation corroborates finite cases; it is not the general proof.
No theorem-prover verification or novelty claim is established.
