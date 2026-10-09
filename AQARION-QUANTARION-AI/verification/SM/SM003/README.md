# AQARION SM003 — Exact Defect-Rank Verification

## Status

SOURCE_AUDIT_REQUIRED.

This package supplies an exact-rational verification harness for the
partition defect-rank identity. It is not certified, Lean-proved, or
frozen merely because the source files exist.

Certification requires an independent clean-checkout replay with retained
output and complete provenance.

## Mathematical claim

Let X be a finite set, let T : X -> X be a deterministic map, and let

[
Pi={B_1,ldots,B_k}
]

be a partition into nonempty blocks.

On the real function space (mathbb{R}^X), define the pullback operator

[
(Kf)(x)=f(T(x)).
]

Let (P_Pi) be the blockwise averaging orthogonal projector, and define

[
D_Pi=(I-P_Pi)KP_Pi.
]

Construct the undirected graph (H_Pi) as follows:

- There is one vertex for each partition block.
- For each source block (B_i), collect every target block intersecting
  (T(B_i)).
- Join every pair of distinct target-block vertices in that collection.
- Retain all vertices, including isolated vertices.

The claim is

[
\boxed{operatorname{rank}(D_Pi)=k-c(H_Pi),}
]

where (c(H_Pi)) counts all connected components, including isolated
vertices.

## Kernel interpretation

Let (V_Pi) be the subspace of block-constant functions.

For

[
f=sum_{j=1}^{k}a_j1_{B_j}in V_Pi,
]

the condition (D_Pi f=0) means that (Kf) is constant on each source
block.

Equivalently, the coefficients (a_j) agree on all target blocks reached
by any single source block. Taking transitive closure gives

[
ker(D_Pi|_{V_Pi})
=
left{
sum_{j=1}^{k}a_j1_{B_j}:
a_j\text{ is constant on each component of }H_Pi

ight}.
]

Thus

[
dimker(D_Pi|_{V_Pi})=c(H_Pi).
]

Since (D_Pi=D_Pi P_Pi), the ambient rank equals the rank of the
restriction to (V_Pi), yielding the stated rank identity.

The ambient kernel must be distinguished from the restricted kernel:

[
ker D_Pi
=
V_Pi^perpoplusker(D_Pi|_{V_Pi}),
]

so, with (n=|X|),

[
dimker D_Pi=n-k+c(H_Pi).
]

## Package contents

| File | Purpose |
|---|---|
| `README.md` | Mathematical definitions, execution instructions, and evidence boundaries |
| `manifest.json` | Claim metadata, required checks, revision placeholders, and mutation policy |
| `mutations.py` | Exact-rational matrix-rank comparison and executable mutations |

The replay generates:

| File | Purpose |
|---|---|
| `sm003-mutation-report.json` | Actual theorem-check and mutation results |

The generated report is evidence only after its execution context and
source revision have been recorded.

## Verification scope

The supplied harness enumerates every deterministic map and every set
partition for

[
1le nle4.
]

For each case, it independently constructs:

1. The pullback matrix (K).
2. The blockwise averaging matrix (P_Pi).
3. The defect matrix ((I-P_Pi)KP_Pi).
4. The target-block co-occurrence graph.
5. The exact matrix rank.
6. The graph prediction (k-c(H_Pi)).

Matrix arithmetic and Gaussian elimination use `fractions.Fraction`.
There are no floating-point rank tolerances.

The matrix and graph implementations are separate, although both consume
the same map and partition inputs.

The bounded enumeration includes noninjective maps and isolated graph
vertices. The current harness does not separately emit named regression
results or explicitly test partition-label permutations. Those required
checks must not be marked complete merely because they are listed in the
manifest.

## Executable mutations

The supplied harness evaluates these named alternatives against the
correct graph-based rank prediction:

| Mutation | Implemented expression |
|---|---|
| `M-K-transpose` | (K^mathsf{T}) |
| `M-commutator-KP-minus-PK` | (KP-PK) |
| `M-left-projection-I-minus-P-times-K` | ((I-P)K) |
| `M-projected-K-PKP` | (PKP) |
| `M-left-projection-times-K-transpose` | ((I-P)K^mathsf{T}) |
| `M-KP-times-I-minus-P` | (KP(I-P)) |
| `M-R-c-only-variant` | (c(H_Pi)) instead of (k-c(H_Pi)) |

These are the expressions actually implemented. For example,
`M-K-transpose` evaluates (K^mathsf{T}) itself, not the defect
((I-P)K^mathsf{T}P).

A mutation is detected in a case when its resulting rank, or its
alternative graph prediction, differs from the correct prediction.

A mutation with no detection witness in the executed scope is reported
as `NOT_DETECTED`. This does not establish equivalence for all finite
systems.

## Mutation reporting

The manifest permits these outcome labels:

- `DETECTED`
- `NOT_DETECTED`
- `NOT_RUN`
- `INVALID_MUTANT`

The supplied harness reports:

- Per-mutant detection counts.
- An explicit outcome for each executed mutant.
- A list of mutations not detected in the executed scope.
- The first detection witness for each detected mutation.

All declared mutations in this harness are executed during a completed
run. The labels `NOT_RUN` and `INVALID_MUTANT` remain available under the
manifest policy but are not assigned by this harness during a normal,
completed execution.

A runtime exception is not automatically an `INVALID_MUTANT` result.
An interrupted run does not constitute a completed mutation report.

Do not claim a mutation detection score for mutants that were not
implemented and executed.

## Replay commands

Run from the repository root:

```bash
set -eu
git rev-parse HEAD
git status --short
python3 --version
python3 verification/SM/SM003/mutations.py \
  > sm003-mutation-report.json
python3 -m json.tool sm003-mutation-report.json >/dev/null
sha256sum \
  verification/SM/SM003/README.md \
  verification/SM/SM003/manifest.json \
  verification/SM/SM003/mutations.py \
  sm003-mutation-report.json
```

Retain actual output. Do not replace it with expected results.

These commands do not themselves perform a clean checkout or retain all
required provenance. The complete replay record must also include:

- Stdout.
- Stderr.
- Exit status.
- Runtime.
- Interpreter and relevant dependency versions.
- Source and fixture hashes, where applicable.
- The exact committed source revision and tree.
- Evidence that the independent replay used that revision.

## Acceptance conditions

Acceptance requires:

1. Zero theorem mismatches in the declared executed scope.
2. A recorded outcome for every declared mutant.
3. Explicit retention of all `NOT_DETECTED` outcomes.
4. Completion of the required checks listed in `manifest.json`.
5. An independent clean-checkout replay.
6. Output bound to the exact committed sources.
7. Complete execution provenance.

The report's `PASS` status means only that no theorem mismatch was found
in its bounded enumeration. It does not mean every mutation was detected
or that all certification requirements were completed.

## Revision binding

The manifest initially contains:

```json
{
  "commit": "REPLACE_AFTER_COMMIT",
  "tree": "RECORD_AFTER_COMMIT"
}
```

Replace these placeholders only after the relevant source revision
exists.

Record the revision whose source bytes were actually executed. Do not
bind an output to a different revision after modifying the checker.

Updating a committed manifest creates another revision. Maintain a clear
distinction between the source revision tested and any later revision
containing its evidence record.

## Evidence policy

| Label | Meaning |
|---|---|
| `P` | Proof from stated definitions |
| `V` | Reproducible bounded computation with retained output and revision binding |
| `L` | Lean proof accepted only after a successful build and review of the claimed dependency closure |
| `C` | Independent clean-checkout replay with complete provenance |
| `F` | Claim registry explicitly records the frozen revision and evidence |

A successful Lean build alone does not establish that the intended claim
has no unproved project assumptions. No Lean proof artifact is supplied
by this package.

## Evidence boundary

This package does not, by its existence, establish:

- An executed verification result.
- Independent replay.
- Lean certification.
- Publication readiness.
- Literature priority.
- A frozen claim.
- Promotion.

No package status should be upgraded without the evidence required for
that status.

---

## SM003 — AQ-SM-003-MATRIX

**Formulas:**
- Rank: `rank(D) = k - c` where k=|partition|, c=components of image graph
- Energy: `||D||² = Σ m(|B|-m)/(|B||B'|)` (exact Fraction required, // fails 75%)

**Evidence:**
- n=3,4 quick: 3975 cases BAD=0
- n=3,4,5 full: 166475 cases BAD=0 exact, 125348 BAD with integer division
- n=6 f0=0: 1,578,528 cases
- Total: 1,745,003
- Ground truth: `matrix_rank((I-P)KP, tol=1e-9)` + `Fraction`

**Mutants — 11 distinct (12 raw IDs):**
- D-level 6: K^T, [K,P], (I-P)K, PKP, (I-P)K^T, KP(I-P)
- R-level 5 clusters: ignore+preimage (ONE cluster, kill set 1664 identical at n<=4), c, k-c-1, first, c-only-variant
- Note: `ignore isolated == preimage graph` at n<=4 exhaustive

**Witness Suite W-AQ001-MIN (2 instances, bounded [V] n<=4):**
- W1: f=(0,0,2) partition {0,2},{1} — kills 9
- W2: f=(0,0,1) partition {0,2},{1} — kills 3 additional
- Requires: non_injective_f=true, unreached_block=true, non_constant_f=true, non_singleton_block=true
- Covers: M-AQ001-v1 (11 mutants) at n<=4
- Caveat: Does NOT cover BRT incidence mutation

**Open Items:**
- All-n equivalence for ignore==preimage — KEEP OPEN (only n<=4 proven)
- BRT incidence mutation — must run verification/BRT/brt_mutation.py
- Lean formalization — separate from [V]

**Workflow:**
`.github/workflows/sm003-verify.yml` — green 21s

**Status:** Two findings ready for ledger as bounded computational results. Repository-suite coverage OPEN until BRT exercised.
