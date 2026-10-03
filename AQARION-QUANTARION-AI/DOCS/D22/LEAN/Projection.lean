import Aqarion.D22.ConventionAudit

namespace Aqarion
namespace D22

open scoped BigOperators Matrix
open Matrix Finset

noncomputable section

variable {k : ℕ}

/-- The coordinates of u_d. -/
@[simp]
theorem u_apply (d i : Idx k) :
    u d i =
      (if i = 0 then 1 else 0) -
      (if i = d then 1 else 0) := by
  simp [u, e]

/-
  For d ≠ 0, u_d has norm square 2.

      u_dᵀ u_d = 2.
-/
theorem dot_u_u
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    dot (u d) (u d) = 2 := by
  simp [dot, u, e]
  /-
    Requires finite delta-sum lemmas and the fact d ≠ 0.
  -/
  sorry

/-
  Outer product multiplication rule:

      outer x y * outer z w
      =
      dot y z • outer x w.

  This is the fundamental rank-one matrix lemma.
-/
theorem outer_mul_outer
    (x y z w : Vec k) :
    outer x y * outer z w = dot y z • outer x w := by
  ext i j
  simp [outer, dot, Matrix.mul_apply]
  /-
    Reduce to:
      ∑ l, (x i * y l) * (z l * w j)
      =
      (∑ l, y l * z l) * (x i * w j)

    Use ring distribution and Finset.sum_mul / mul_sum.
  -/
  sorry

/-
  Q_d is exactly the rank-one complementary projection.

      Q_d = 1/2 u_d u_dᵀ.
-/
theorem Q_eq_rankOne
    (d : Idx k) :
    Q d = (1 / 2 : ℝ) • outer (u d) (u d) := by
  ext i j
  simp [Q, P, I]
  ring

/-
  Projection idempotence.

      P_d² = P_d.

  This depends on u_dᵀu_d = 2.
-/
theorem P_mul_P
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    P d * P d = P d := by
  rw [show P d = I - (1 / 2 : ℝ) • outer (u d) (u d) by rfl]
  rw [outer_mul_outer, dot_u_u hk d hd0]
  ext i j
  simp [I]
  ring

/-
  Exact row factor before evaluating its coordinates:

      D_d = 1/2 u_d [u_dᵀ K P_d].

  We represent the row factor with Matrix.vecMul.
-/
def aFromProjection (d : Idx k) : Vec k :=
  Matrix.vecMul (u d) (K * P d)

/-
  First rank-one projection theorem.

      D_d = 1/2 outer(u_d, aFromProjection_d).
-/
theorem defect_rankOne_from_projection
    (d : Idx k) :
    D d = (1 / 2 : ℝ) • outer (u d) (aFromProjection d) := by
  rw [D, Q_eq_rankOne]
  ext i j
  simp [outer, aFromProjection, Matrix.mul_apply, Matrix.vecMul, dotProduct]
  ring_nf
  /-
    The remaining finite-sum reassociation should identify:
      uᵀ (K P)
    with
      (uᵀ K) P.
  -/
  sorry

/-
  Algebraic row expansion:

      uᵀ K P
      =
      uᵀ K - 1/2 (uᵀ K u) uᵀ.
-/
theorem aFromProjection_expand
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    aFromProjection d =
      Matrix.vecMul (u d) K -
        (1 / 2 : ℝ) *
          dot (Matrix.vecMul (u d) K) (u d) • u d := by
  funext j
  simp [aFromProjection, P, Matrix.vecMul, dotProduct, outer]
  ring_nf
  sorry

/-
  Scalar overlap:

      u_dᵀ K u_d = -1_{d=1} - 1_{d=-1}.

  This is where the boundary correction originates.
-/
theorem u_vecMul_K_dot_u
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    dot (Matrix.vecMul (u d) K) (u d) =
      - (if d = 1 then 1 else 0)
      - (if d = -1 then 1 else 0) := by
  simp [u, e, dot, K, Matrix.vecMul, dotProduct]
  /-
    This requires:
      e_0ᵀ K e_d = 1 iff d = 1
      e_dᵀ K e_0 = 1 iff d = -1
      diagonal terms vanish because k > 2 and d ≠ 0.
  -/
  sorry

/-
  Exact closed form of the projection row factor.

      aFromProjection d = a d.
-/
theorem aFromProjection_eq_a
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    aFromProjection d = a d := by
  rw [aFromProjection_expand hk d hd0]
  rw [u_vecMul_K_dot_u hk d hd0]
  rw [e_vecMul_K hk 0, e_vecMul_K hk d]
  simp [u, a, boundary]
  by_cases h1 : d = 1
  · subst h1
    simp
    ring
  · by_cases hm1 : d = -1
    · subst hm1
      simp
      ring
    · simp [h1, hm1]
      ring

/-
  Final exact D22 operator factorization.

      (I-P_d) K P_d = 1/2 u_d a_dᵀ.
-/
theorem defect_rankOne
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0) :
    D d = Dfactor d := by
  rw [defect_rankOne_from_projection]
  rw [aFromProjection_eq_a hk d hd0]
  rfl

end
end D22
end Aqarion
