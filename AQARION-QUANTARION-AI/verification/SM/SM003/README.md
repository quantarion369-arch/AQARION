# SM003 — Exact Defect-Rank Verification

**Package:** AQARION / verification / SM / SM003
**Repository:** `quantarion369-arch/AQARION`
**Path:** `AQARION-QUANTARION-AI/verification/SM/SM003/README.md`
**Status:** `SOURCE_AUDIT_REQUIRED` until a clean-checkout run and a
revision-bound receipt are recorded.

## Mathematical claim

For a finite set `X`, total map `T : X -> X`, and partition `Pi` with
`k = |Pi|` nonempty blocks, define the Koopman matrix

```
K[x][T(x)] = 1
```

and the block-average orthogonal projector

```
P[i][j] = 1/|B|  if i, j in same block B of Pi, else 0.
```

The partition defect is

```
D = (I - P) K P.
```

Build the target-block co-occurrence graph `H_Pi`:

- one vertex per block of `Pi`;
- for each source block `B`, join every pair of distinct target blocks
  hit by `T(B)`;
- retain all vertices, including isolated vertices.

The claim is

```
rank(D) = k - c(H_Pi)
```

where `c(H_Pi)` counts every connected component, including isolated
vertices.

## Paper-level argument

`P` projects onto the space `V_Pi` of functions that are constant on every
block of `Pi`. Since `D = D P`, the operator is determined by its action on
`V_Pi`.

For a block-constant `h`, `D h = 0` iff `K h` is again block-constant. If
`x, y` lie in the same source block `B`, then `h(T x) = h(T y)` for every
block-constant `h`. This is exactly the condition that the block-values of
`h` agree across every edge of `H_Pi`.

The kernel of `D` restricted to `V_Pi` is therefore the space of functions
that are constant on each connected component of `H_Pi`. Hence

```
dim ker(D | V_Pi) = c(H_Pi)
```

and, by rank-nullity on the `k`-dimensional domain,

```
rank(D) = k - c(H_Pi).
```

This is a paper-level proof. The computational census is a separate
evidence category.

## Executable audit

`mutations.py` uses `fractions.Fraction` throughout. It implements the six
declared D-level matrix alternatives plus the graph-level alternatives in
`manifest.json`. It records one of:

```
DETECTED
NOT_DETECTED
NOT_RUN
INVALID_MUTANT
```

`R:c-only-variant` is explicitly marked `INVALID_MUTANT` because its
implemented expression is identical to `R:c`. It is not counted as
distinct coverage.

Default scope is exhaustive over all maps and partitions for `n = 1..4`,
totalling `3,984` map-partition pairs:

| `n` | map-partition pairs |
|---:|---:|
| 1 | 1 |
| 2 | 8 |
| 3 | 135 |
| 4 | 3,840 |
| total | 3,984 |

Historical totals:

| scope | cases | coverage type |
|---|---:|---|
| `n = 3,4` | 3,975 | graph alternatives only |
| `n = 3,4,5` | 166,475 | graph alternatives only |
| `n = 1..4` (new default) | 3,984 | D-level + graph alternatives |

The old `mutations.py` evaluated graph alternatives only, so those
historical totals do not substantiate D-level mutation coverage.

## Replay commands

From the repository root:

```bash
python3 AQARION-QUANTARION-AI/verification/SM/SM003/mutations.py \
  --max-n 4 \
  --report AQARION-QUANTARION-AI/verification/SM/SM003/sm003-mutation-report.json

python3 -m unittest discover \
  -s AQARION-QUANTARION-AI/verification/SM/SM003 \
  -p 'test_sm003.py' -v
```

Retain stdout, stderr, exit status, runtime, environment, and source
digests in the receipt. Do not replace observed output with expected
output.

## Provenance

The previous manifest contained a literal commit placeholder. This
package does not self-assert a future commit. Record the tested source
revision, source digests, command lines, stdout, stderr, exit codes,
runtime, and environment in the generated audit report after running
against the committed tree.

The previously documented `.github/workflows/sm003-verify.yml` was not
present at the audited commit. Do not report that workflow as current
unless it is restored and verified. The current BRT workflow is separate
and does not establish SM003 execution.

## Evidence boundary

`PASS` means only that the baseline rank identity matched the graph
prediction over the declared finite scope. It does not establish:

- a universal theorem;
- Lean formalisation;
- certification;
- publication readiness;
- promotion.

## Non-goals

This package does not:

- verify the repository's old `mutations.py` correctness;
- run GitHub Actions;
- close the SM003 claim;
- touch PB, D22, or the partition-koopman experiment;
- certify the BRT workflow.

## Package file list

| File | Purpose |
|---|---|
| `README.md` | This file |
| `manifest.json` | Claim metadata, scope, mutant IDs, mutation policy |
| `mutations.py` | Exact-rational defect-rank audit and alternative execution |
| `test_sm003.py` | Regression tests for `mutations.py` |
| `sm003-mutation-report.json` | Generated output (created on replay, not pre-committed) |
| `SM003-BRT-DELTA.md` | Delta summary of the SM003 / BRT refactor |
