import Aqarion.D22.Projection

namespace Aqarion
namespace D22

open scoped BigOperators Matrix
open Matrix Finset

noncomputable section

variable {k : ℕ}

/-
  The closed factor has equal coordinates at 0 and d.

  This is exactly a_dᵀu_d = 0.
-/
theorem dot_a_u_zero
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    dot (a d) (u d) = 0 := by
  simp [a, u, e, dot, boundary]
  by_cases h1 : d = 1
  · subst h1
    simp
  · by_cases hm1 : d = -1
    · subst hm1
      simp
    · simp [h1, hm1, hd0]
  sorry

/-
  Rank-one square identity:

      (c outer u a)² = c² dot a u outer u a.
-/
theorem Dfactor_sq
    (d : Idx k) :
    Dfactor d * Dfactor d =
      (1 / 4 : ℝ) * dot (a d) (u d) • outer (u d) (a d) := by
  simp [Dfactor]
  rw [outer_mul_outer]
  ext i j
  simp [outer]
  ring

/-- Nilpotency of the exact D22 defect operator. -/
theorem defect_sq_zero
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    D d * D d = 0 := by
  rw [defect_rankOne hk d hd0]
  rw [Dfactor_sq]
  rw [dot_a_u_zero hk d hd0]
  simp

/-
  Frobenius-square of an outer product:

      frobSq(outer x y) = dot x x * dot y y.
-/
theorem frobSq_outer
    (x y : Vec k) :
    frobSq (outer x y) = dot x x * dot y y := by
  simp [frobSq, outer, dot]
  ring_nf
  /-
    Reorder double sums:
      Σ_i Σ_j (x_i*y_j)^2
      =
      (Σ_i x_i^2) * (Σ_j y_j^2).
  -/
  sorry

/-
  Frobenius-square of Dfactor:

      ||D||_F² = 1/2 ||a||².
-/
theorem frobSq_Dfactor
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    frobSq (Dfactor d) = (1 / 2 : ℝ) * dot (a d) (a d) := by
  simp [Dfactor, frobSq_outer]
  rw [dot_u_u hk d hd0]
  ring

/-
  Interior factor norm.

  Requires d ≠ 1 and d ≠ -1.
-/
theorem dot_a_a_interior
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0)
    (h1 : d ≠ 1)
    (hm1 : d ≠ -1) :
    dot (a d) (a d) = 2 := by
  simp [a, boundary, h1, hm1, dot, e]
  sorry

/-
  Boundary norm: d = 1.
-/
theorem dot_a_a_boundary_one
    (hk : 2 < k) :
    dot (a (1 : Idx k)) (a (1 : Idx k)) = 3 / 2 := by
  simp [a, boundary, dot, e]
  norm_num
  sorry

/-
  Boundary norm: d = -1.
-/
theorem dot_a_a_boundary_neg_one
    (hk : 2 < k) :
    dot (a (-1 : Idx k)) (a (-1 : Idx k)) = 3 / 2 := by
  simp [a, boundary, dot, e]
  norm_num
  sorry

/-
  Exact Frobenius split.
-/
theorem frobSq_defect
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    frobSq (D d) =
      if boundary d then (3 / 4 : ℝ) else 1 := by
  rw [defect_rankOne hk d hd0]
  rw [frobSq_Dfactor hk d hd0]
  by_cases h : boundary d
  · rcases h with h1 | hm1
    · subst h1
      simp [dot_a_a_boundary_one hk]
    · subst hm1
      simp [dot_a_a_boundary_neg_one hk]
  · simp [h]
    have h1 : d ≠ 1 := by
      intro hd; exact h (Or.inl hd)
    have hm1 : d ≠ -1 := by
      intro hd; exact h (Or.inr hd)
    rw [dot_a_a_interior hk d hd0 h1 hm1]
    ring

end
end D22
end Aqarion
