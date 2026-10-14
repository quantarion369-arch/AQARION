# AQARION — Closure-Cost Equality Extension

Date: October 14, 2026

## Status

| Lane | Status | Evidence label |
|---|---|---|
| Closure-cost upper bound | Paper-level proof reviewed | Not machine-checked |
| General upper-equality criterion | Paper-level proof reviewed | Maximal splitting at every stage |
| Binary all-ones-profile characterization | Paper-level proof reviewed | Full binary itinerary cube plus feedback condition |
| General nested-alphabet and feedback characterization | Paper-level proof present; precision review pending | Structural consequences of upper equality |
| Replay | Local semantic replay passed on seeds 0 and 1 | Reconstructed dependency; not hash-verified |
| Lean formalization | Deferred | Separate gate |
| Publication / C4 | Blocked | By policy |

## General bound

Let \(T:X\to X\) be a finite map and \(\pi\) a partition into \(k\) nonempty blocks. Let \(Kf=f\circ T\), let \(V_\pi\) be the space of block-constant functions, and define

\[
W_j=V_\pi+KV_\pi+\cdots+K^jV_\pi,
\qquad
\delta_j=\dim W_j-\dim W_{j-1}.
\]

Let \(s\) be the number of stabilized itinerary classes and let \(C=\sum_{j\ge1}\delta_j\). Then

\[
C\le s-k\le
k\left(\prod_{j\ge1}(1+\delta_j)-1\right).
\]

The upper bound is attained exactly when every block at each refinement stage splits into the maximum permitted number, \(1+\delta_j\), of children.

Equivalently, the itinerary-prefix set has the full Cartesian-product size dictated by its coordinate alphabets.
## Structural theorem

The nested-alphabet and common-coordinate feedback characterization is proved
for the general all-\(k\), all-profile case in
`research/closure-cost/GENERAL-FEEDBACK.md`.

The binary all-ones-profile special case remains in
`research/closure-cost/THEOREM.md`.

## Replay evidence

The corrected checker passed locally on seeds 0 and 1. The reported runs agree on the exhaustive (nle5) counts and construction checks.

The dependency `prof.py` is a compatible reconstruction, not the originally reported artifact with SHA-256 prefix `829be3fc…`.

Therefore this is a **local semantic replay**, not a hash-verified byte-for-byte replay.

See:

- `research/closure-cost/THEOREM.md`
- `research/closure-cost/AUDIT.md`
- `extensions/closure-cost-equality/replay/REPLAY.md`
- `extensions/closure-cost-equality/replay/equality_check.py`
- `extensions/closure-cost-equality/replay/local_eq0_reconstructed.txt`
- `extensions/closure-cost-equality/replay/local_eq1_reconstructed.txt`

## Explicit non-claims

- No Lean formalization.
- No novelty claim.
- No publication readiness.
- No claim that sampled cases are exhaustive.
- No claim that the reconstructed dependency is the original artifact.
- No claim of hash-verified replay.

## Position

The extension has a reviewed paper-level argument and a pushed, locally reproduced semantic replay with its dependency limitation stated explicitly. Formalization, novelty, and publication certification remain separate gates.
