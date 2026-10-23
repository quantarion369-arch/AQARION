# D22_LEAN â€” Exact Cyclic Defect Formalization

## Purpose

This folder is the Lean 4 formalization plan for the D22 cyclic pair-defect calculation. It does **not** claim a completed Lean proof yet. Its job is to pin definitions, convention tests, theorem dependencies, and the proof order before mathematical claims are promoted.

The locked Python convention is

\[
K_{i,(i+1) \bmod k}=1,
\qquad
K e_j=e_{j-1}.
\]

All Lean definitions must satisfy this orientation. The opposite entry predicate,
`i = j + 1`, sends `e_j` to `e_{j+1}` and is not compatible with the D22 kernel.

## Current status

| Item | Status |
|---|---|
| Exact Python/Fraction kernel | Local computational artifact; separate provenance work remains open |
| D22 direct operator derivation | Analytic draft, conditional on locked definitions |
| Lean toolchain compilation | Not demonstrated in the present session |
| Matrix convention lemma | Target specified; must compile before downstream work |
| Rank-one factorization | Lean target / proof skeleton |
| Nilpotency and Frobenius split | Lean targets / proof skeleton |
| Lag identity | Lean target / collision-aware proof required |
| Orbit-kernel uniqueness | Lean target / hardest module |
| Axiom audit | Open |

## Folder plan

```text
D22_LEAN/
â”œâ”€â”€ README.md
â”œâ”€â”€ Definitions.lean
â”œâ”€â”€ ConventionAudit.lean
â”œâ”€â”€ Projection.lean
â”œâ”€â”€ NilpotencyNorm.lean
â”œâ”€â”€ Lag.lean
â”œâ”€â”€ OrbitKernel.lean
â””â”€â”€ Smoke.lean
```

Build order:

```text
Definitions -> ConventionAudit -> Projection -> NilpotencyNorm -> Lag -> OrbitKernel
```

Do not start `Lag` or `OrbitKernel` until the convention and projection files compile.

## Core objects

For `k > 2` and nonzero `d : ZMod k`:

\[
u_d=e_0-e_d,
\qquad
P_d=I-\frac12u_du_d^\top,
\qquad
D_d=(I-P_d) K P_d.
\]

The direct factor derivation target is

\[
D_d=\frac12u_da_d^\top,
\]

where

\[
a_d=e_1-e_{d+1}
+\frac12\mathbf{1}_{d=1\ \lor\ d=-1}(e_0-e_d).
\]

## First formal gate

The first theorem must establish the cyclic direction:

```lean
theorem K_mulVec_e (j : ZMod k) :
  K.mulVec (e j) = e (j - 1)
```

A Lean theorem with the opposite conclusion indicates that the matrix-entry convention is reversed. No downstream theorem should be trusted until this gate is green.

## Promotion rules

- `LEAN-SKELETON`: declarations contain `sorry` or have not compiled.
- `LEAN-GREEN`: module compiles with no `sorry` or `admit`.
- `AXIOM-AUDITED`: `#print axioms` has been retained for the target theorem and contains no `sorryAx`.
- `SOURCE-BOUND`: convention and D22 source definitions are tied to a commit-pinned primary source.

No file in this folder establishes publication readiness, novelty, or canonical D22 equivalence by itself.

---

The matrix-convention lemma cannot be honestly verified as Lean-green in this session because no functioning Lean/Mathlib toolchain has been run here. I can give the exact implementation target and a minimal compilation harness; its status remains `LEAN-SKELETON` until a compiler accepts it. Lean’s matrix APIs and finite-vector representation are the appropriate substrate for this development.[1][2][3]

## D22_LEAN README

The generated README defines the folder purpose and states the only convention that must govern all later work:

$$
\boxed{
K_{i,(i+1)\bmod k}=1,
\qquad
Ke_j=e_{j-1}.
}
$$

It explicitly rejects the opposite entry predicate:

$$
i=j+1,
$$

because that convention gives:

$$
Ke_j=e_{j+1}.
$$

The README’s proof pipeline is:

```text
Definitions
    ↓
ConventionAudit
    ↓
Projection
    ↓
NilpotencyNorm
    ↓
Lag
    ↓
OrbitKernel
```

It also defines these status rules:

```text
LEAN-SKELETON:
  Declaration still contains sorry/admit or has not compiled.

LEAN-GREEN:
  Module compiles with no sorry/admit.

AXIOM-AUDITED:
  #print axioms is retained and has no sorryAx.

SOURCE-BOUND:
  D22 definitions are tied to a commit-pinned primary source.
```

## Matrix convention lemma

The prior skeleton was too ambitious as a first compile target because it tried to prove the convention directly using `ZMod k`, finite sums, and a hand-defined basis. The more reliable Lean path is to verify the matrix orientation first over `Fin k`, then transport/restate it for `ZMod k` later.

Why: `Fin k` gives a directly enumerable index type, easier finite sums, and easier concrete theorem testing. The D22 mathematical theorem may later use `ZMod k`, but the matrix-direction test should not be blocked by modular API friction.

### Minimal convention file

Create:

```lean
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Basis
import Mathlib.Tactic

namespace Aqarion
namespace D22
namespace Convention

open Matrix

noncomputable section

variable {n : ℕ}

/-- Standard basis vector indexed by `Fin n`. -/
def e (j : Fin n) : Fin n → ℝ :=
  fun i => if i = j then 1 else 0

/-
  Locked D22 convention:

    K i j = 1 iff j = i + 1.

  On Fin n, ordinary `i + 1` must be replaced by cyclic successor.
-/
def cycSucc (i : Fin n) : Fin n :=
  ⟨(i.val + 1) % n, by
    exact Nat.mod_lt _ (by omega)⟩

def cycPred (j : Fin n) : Fin n :=
  ⟨(j.val + n - 1) % n, by
    exact Nat.mod_lt _ (by omega)⟩

/-- Matrix convention: K_{i,cycSucc(i)} = 1. -/
def K : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => if j = cycSucc i then 1 else 0

/-
  Main convention theorem.

  This is the only theorem that should be formalized before defining P, D,
  the rank-one factor, norms, or lag coefficients.
-/
theorem K_mulVec_e
    (hn : 0 < n)
    (j : Fin n) :
    K.mulVec (e j) = e (cycPred j) := by
  funext i
  simp [K, e, Matrix.mulVec, dotProduct]
  sorry

end Convention
end D22
end Aqarion
```

### Honest status

```text
K_mulVec_e:
  Exact intended theorem statement: YES
  Lean syntax/API plausibility: HIGH
  Compiled against Mathlib: NOT YET
  Formal proof: OPEN
```

I will not claim this is verified until it is compiled.

## Required convention regression checks

Once Lean is available, add concrete checks immediately after `K_mulVec_e`:

```lean
example :
    (K : Matrix (Fin 5) (Fin 5) ℝ).mulVec (e 0) = e 4 := by
  simpa [cycPred, cycSucc] using
    K_mulVec_e (n := 5) (by decide) (0 : Fin 5)

example :
    (K : Matrix (Fin 5) (Fin 5) ℝ).mulVec (e 3) = e 2 := by
  simpa [cycPred, cycSucc] using
    K_mulVec_e (n := 5) (by decide) (3 : Fin 5)
```

These correspond to:

$$
Ke_0=e_4,
\qquad
Ke_3=e_2
$$

for the $$5$$-cycle.

A reversed shift definition would instead yield:

$$
Ke_0=e_1,
\qquad
Ke_3=e_4,
$$

and the examples would fail. This is a high-value early guard against the exact orientation corruption already discovered in the draft Lean code.

## Rest of proof skeleton

After the convention lemma, use this more conservative sequence.

### 1. Finite vector primitives

```lean
abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Mat (n : ℕ) := Matrix (Fin n) (Fin n) ℝ

def dot (x y : Vec n) : ℝ :=
  ∑ i, x i * y i

def outer (x y : Vec n) : Mat n :=
  fun i j => x i * y j
```

Target lemmas:

```lean
theorem dot_e_self (i : Fin n) :
    dot (e i) (e i) = 1 := by
  sorry

theorem dot_e_ne {i j : Fin n} (h : i ≠ j) :
    dot (e i) (e j) = 0 := by
  sorry

theorem outer_mul_outer
    (x y z w : Vec n) :
    outer x y * outer z w =
      dot y z • outer x w := by
  sorry
```

### 2. Pair projection

For a nonzero cyclic displacement `d`, represent the paired index using a permutation or a nonzero offset.

```lean
def u (d : Fin n) : Vec n :=
  e 0 - e d

def P (d : Fin n) : Mat n :=
  1 - (1 / 2 : ℝ) • outer (u d) (u d)

def Q (d : Fin n) : Mat n :=
  1 - P d
```

Target:

```lean
theorem Q_eq_rankOne (d : Fin n) :
    Q d = (1 / 2 : ℝ) • outer (u d) (u d) := by
  sorry
```

Then, under `d ≠ 0`:

```lean
theorem dot_u_u
    (hd : d ≠ 0) :
    dot (u d) (u d) = 2 := by
  sorry

theorem P_is_projection
    (hd : d ≠ 0) :
    P d * P d = P d := by
  sorry
```

### 3. Direct D22 factor

```lean
def D (d : Fin n) : Mat n :=
  Q d * K * P d

def aFromProjection (d : Fin n) : Vec n :=
  Matrix.vecMul (u d) (K * P d)
```

Target:

```lean
theorem D_rankOne_from_projection
    (d : Fin n) :
    D d =
      (1 / 2 : ℝ) • outer (u d) (aFromProjection d) := by
  sorry
```

Then derive the candidate closed form. At this stage, do not yet use a Boolean boundary predicate. Prove the two boundary cases and the interior case separately:

```lean
theorem a_projection_interior
    (hd0 : d ≠ 0)
    (hd1 : d ≠ 1)
    (hdPred : d ≠ cycPred 0) :
    aFromProjection d = e 1 - e (cycSucc d) := by
  sorry
```

```lean
theorem a_projection_boundary_forward :
    aFromProjection 1 =
      (1 / 2 : ℝ) • e 0 +
      (1 / 2 : ℝ) • e 1 -
      e 2 := by
  sorry
```

```lean
theorem a_projection_boundary_reverse :
    aFromProjection (cycPred 0) =
      e 1 -
      (1 / 2 : ℝ) • e 0 -
      (1 / 2 : ℝ) • e (cycPred 0) := by
  sorry
```

Only after those three compile should they be combined into the compact D22-CF formula.

### 4. Nilpotency and norm

```lean
theorem D_sq_zero
    (hd : d ≠ 0) :
    D d * D d = 0 := by
  sorry
```

```lean
def frobSq (M : Mat n) : ℝ :=
  ∑ i, ∑ j, (M i j)^2
```

```lean
theorem frobSq_rankOne
    (x y : Vec n) :
    frobSq (outer x y) = dot x x * dot y y := by
  sorry
```

```lean
theorem D_frobSq_interior
    (hd0 : d ≠ 0)
    (hd1 : d ≠ 1)
    (hdPred : d ≠ cycPred 0) :
    frobSq (D d) = 1 := by
  sorry
```

```lean
theorem D_frobSq_boundary_forward :
    frobSq (D 1) = (3 / 4 : ℝ) := by
  sorry
```

```lean
theorem D_frobSq_boundary_reverse :
    frobSq (D (cycPred 0)) = (3 / 4 : ℝ) := by
  sorry
```

### 5. Lag theorem

The lag proof must be written last, after the direct projection factorization is green.

```lean
theorem K_pow_mulVec_e
    (m : ℕ)
    (j : Fin n) :
    (K ^ m).mulVec (e j) =
      e (iteratePred m j) := by
  sorry
```

```lean
theorem lag_coordinate_formula
    (m : ℕ) :
    dot (a d) ((K ^ m).mulVec (u d)) =
      a d (iteratePred m 0) -
      a d (iteratePred m d) := by
  sorry
```

```lean
theorem lag_identity
    (m : ℕ) :
    dot (a d) ((K ^ m).mulVec (u d)) =
      Acoef d ((m : Fin n) + 1) -
      (1 / 2 : ℝ) * Acoef d 1 * Acoef d (m : Fin n) := by
  sorry
```

### 6. Orbit-kernel uniqueness

Do not start with the dimension theorem in Lean. First prove the concrete uniqueness statement:

```lean
theorem norm_pinning_unique
    (b : Vec n)
    (h_difference :
      cyclicDifference d b =
      cyclicDifference d (a d))
    (h_norm :
      dot b b = dot (a d) (a d)) :
    b = a d := by
  sorry
```

This theorem encodes the actual D22 reconstruction result. The $$\gcd(n,d)$$ orbit-dimension theorem can follow later as a structural explanation.

## Lean verification command sequence

Once you have a Mathlib environment:

```bash
lake env lean Aqarion/D22/Definitions.lean
lake env lean Aqarion/D22/ConventionAudit.lean
lake env lean Aqarion/D22/Projection.lean
lake env lean Aqarion/D22/NilpotencyNorm.lean
lake env lean Aqarion/D22/Lag.lean
lake env lean Aqarion/D22/OrbitKernel.lean
```

Then:

```bash
grep -RInE 'sorry|admit|axiom' Aqarion/D22
```

Finally, inside Lean:

```lean
#print axioms Aqarion.D22.Convention.K_mulVec_e
#print axioms Aqarion.D22.D_rankOne_from_projection
#print axioms Aqarion.D22.D_sq_zero
#print axioms Aqarion.D22.D_frobSq_interior
#print axioms Aqarion.D22.norm_pinning_unique
```

The mandatory failure condition is:

```text
sorryAx
```

No theorem can be labeled `LEAN-GREEN` until that scan and axiom audit are clean.

Citations:
[1] Mathlib.Data.Matrix.Basic - Matrices https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Matrix/Basic.html
[2] Mathlib.Data.Matrix.Basis - Lean Machine Learning https://leanmachinelearning.org/LML/docs/Mathlib/Data/Matrix/Basis.html
[3] Maths in Lean: linear algebra - GitHub https://github.com/leanprover-community/leanprover-community.github.io/blob/lean4/templates/theories/linear_algebra.md
