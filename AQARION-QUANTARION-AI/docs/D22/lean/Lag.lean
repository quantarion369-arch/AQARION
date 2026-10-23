import Aqarion.D22.NilpotencyNorm

namespace Aqarion
namespace D22

open scoped BigOperators Matrix
open Matrix Finset

noncomputable section

variable {k : ℕ}

/-
  Powers of K must first be related to modular index shifts.

  Required orientation theorem:

      K^m e_j = e_{j-m}.

  The exponent is natural in matrix powers. To state the lag coefficient
  for a residue m : ZMod k, either:

  A. work with m : ℕ and reduce each index modulo k;
  B. introduce a natural representative m.val;
  C. formalize a group representation of ZMod k by permutation matrices.

  A is simplest for an initial proof.
-/
theorem K_pow_mulVec_e
    (hk : 0 < k)
    (m : ℕ)
    (j : Idx k) :
    (K ^ m).mulVec (e j) = e (j - m) := by
  induction m with
  | zero =>
      simp
  | succ m ih =>
      rw [pow_succ, Matrix.mulVec_mulVec, ih]
      simpa using K_mulVec_e (k := k) hk (j - m)
  sorry

/-
  Required scalar coordinate formula:

      a_dᵀ K^m u_d = a_{-m} - a_{d-m}.
-/
theorem lag_coordinate
    (hk : 0 < k)
    (d : Idx k)
    (m : ℕ) :
    dot (a d) ((K ^ m).mulVec (u d)) =
      a d (-m : Idx k) - a d (d - m) := by
  rw [show u d = e 0 - e d by rfl]
  simp [Matrix.mulVec_sub, K_pow_mulVec_e hk m 0, K_pow_mulVec_e hk m d]
  simp [dot, e]
  sorry

/-
  Main scalar D22 lag identity.

  To complete this theorem, expand `a` and `Acoef`, then use a
  three-case proof:
    d = 1,
    d = -1,
    d ≠ 1 and d ≠ -1.

  The modular delta bookkeeping should live in a dedicated helper file.
-/
theorem lag_formula
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0)
    (m : ℕ) :
    dot (a d) ((K ^ m).mulVec (u d)) =
      Acoef d ((m : Idx k) + 1) -
        (1 / 2 : ℝ) * Acoef d 1 * Acoef d (m : Idx k) := by
  rw [lag_coordinate (show 0 < k from lt_trans (by decide) hk) d m]
  by_cases h1 : d = 1
  · subst h1
    simp [a, Acoef, boundary]
    sorry
  · by_cases hm1 : d = -1
    · subst hm1
      simp [a, Acoef, boundary]
      sorry
    · simp [a, Acoef, boundary, h1, hm1]
      sorry

/-
  Full matrix lag identity.
-/
theorem defect_Kpow_defect
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0)
    (m : ℕ) :
    D d * K ^ m * D d =
      (1 / 4 : ℝ) *
        Fcoef d (m : Idx k) • outer (u d) (a d) := by
  rw [defect_rankOne hk d hd0]
  rw [outer_mul_outer]
  rw [lag_formula hk d hd0 m]
  ext i j
  simp [outer]
  ring

end
end D22
end Aqarion
