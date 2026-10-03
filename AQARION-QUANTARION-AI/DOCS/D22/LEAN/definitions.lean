import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Basis
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Algebra.BigOperators.Group.Finset
import Mathlib.Tactic

namespace Aqarion
namespace D22

open scoped BigOperators Matrix
open Matrix Finset

noncomputable section

variable {k : ℕ}

/-
  Index type:
    I k = ZMod k.

  Every theorem carrying a nonzero displacement d will assume:
    hk : 2 < k
    hd0 : d ≠ 0

  This prevents the degenerate d = 0 case and ensures:
    e_0 - e_d has two distinct support coordinates.
-/

abbrev Idx (k : ℕ) := ZMod k
abbrev Vec (k : ℕ) := Idx k → ℝ
abbrev Mat (k : ℕ) := Matrix (Idx k) (Idx k) ℝ

/-- Standard coordinate vector e_i. -/
def e (i : Idx k) : Vec k :=
  fun j => if j = i then 1 else 0

/-- Dot product of finite real vectors. -/
def dot (x y : Vec k) : ℝ :=
  ∑ i, x i * y i

/-- Outer product x yᵀ. -/
def outer (x y : Vec k) : Mat k :=
  fun i j => x i * y j

/-- Identity matrix. -/
def I : Mat k := 1

/-
  Locked Python convention:

      K_{i,(i+1)} = 1

  Equivalently:

      K i j = 1 iff j = i + 1.

  Then:

      K *ᵥ e_j = e_{j-1}.

  Warning:
  Do NOT replace `j = i + 1` by `i = j + 1`.
  That defines the opposite cyclic direction.
-/
def K : Mat k :=
  fun i j => if j = i + 1 then 1 else 0

/-- Defect vector u_d = e_0 - e_d. -/
def u (d : Idx k) : Vec k :=
  e (0 : Idx k) - e d

/-- Boundary predicate used by the D22 closed form. -/
def boundary (d : Idx k) : Prop :=
  d = 1 ∨ d = -1

/-
  Pair-partition orthogonal projection.

  P_d = I - (1/2) u_d u_dᵀ.

  This is the projection onto:
      {x : Vec k | x 0 = x d}
  when d ≠ 0.
-/
def P (d : Idx k) : Mat k :=
  I - (1 / 2 : ℝ) • outer (u d) (u d)

/-- Complementary rank-one projection I - P_d. -/
def Q (d : Idx k) : Mat k :=
  I - P d

/-- D22 defect operator D_d = (I - P_d) K P_d. -/
def D (d : Idx k) : Mat k :=
  Q d * K * P d

/-
  Derived D22 factor:

      a_d = e_1 - e_{d+1}
            + 1/2 · 1_boundary(d) · (e_0 - e_d).

  The Boolean-like branch is kept as a `if`.
-/
def a (d : Idx k) : Vec k :=
  e (1 : Idx k) - e (d + 1) +
    if boundary d then
      (1 / 2 : ℝ) • (e (0 : Idx k) - e d)
    else
      0

/-- Rank-one D22 factorization candidate: (1/2)u_d a_dᵀ. -/
def Dfactor (d : Idx k) : Mat k :=
  (1 / 2 : ℝ) • outer (u d) (a d)

/-- Scalar autocorrelation c_m = a_dᵀ K^m u_d. -/
def c (d m : Idx k) : ℝ :=
  dot (a d) ((K ^ (m.val : ℕ)).mulVec (u d))

/-
  Transmitted lag coefficients.

  A_r = 2 1_{r=0} - 1_{r=d} - 1_{r=-d}.
-/
def Acoef (d r : Idx k) : ℝ :=
  2 * if r = 0 then 1 else 0
    - if r = d then 1 else 0
    - if r = -d then 1 else 0

/-- F(m) = A_{m+1} - (1/2) A_1 A_m. -/
def Fcoef (d m : Idx k) : ℝ :=
  Acoef d (m + 1) -
    (1 / 2 : ℝ) * Acoef d 1 * Acoef d m

/-- Frobenius-square of a finite real matrix. -/
def frobSq (M : Mat k) : ℝ :=
  ∑ i, ∑ j, (M i j)^2

end
end D22
end Aqarion
