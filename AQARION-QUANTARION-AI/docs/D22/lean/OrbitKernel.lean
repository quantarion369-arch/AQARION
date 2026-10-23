import Aqarion.D22.Lag

namespace Aqarion
namespace D22

open scoped BigOperators Matrix
open Matrix Finset

noncomputable section

variable {k : ℕ}

/-
  Translation of indices by d.

  This is a permutation of ZMod k.
-/
def tau (d : Idx k) : Equiv.Perm (Idx k) where
  toFun i := i + d
  invFun i := i - d
  left_inv i := by simp
  right_inv i := by simp

/-
  Orbit relation:
    i ~ j iff ∃ n : ℤ, tau(d)^n i = j.

  Initial formalization recommendation:
  avoid defining an arbitrary set of orbit sets immediately.
  Instead define the kernel condition:
      v (i+d) = v i
  and prove constancy along integer iterates.
-/

/-- A vector is tau_d-invariant exactly when it is constant under d-shift. -/
def tauInvariant (d : Idx k) (v : Vec k) : Prop :=
  ∀ i, v (i + d) = v i

/-
  Difference operator:

      Δ_d(v)(i) = v(i) - v(i+d).

  Its kernel is exactly tau-invariant vectors.
-/
def cyclicDifference (d : Idx k) : Vec k → Vec k :=
  fun v i => v i - v (i + d)

theorem cyclicDifference_eq_zero_iff
    (d : Idx k)
    (v : Vec k) :
    cyclicDifference d v = 0 ↔ tauInvariant d v := by
  constructor
  · intro h i
    have hi := congrFun h i
    simp [cyclicDifference] at hi
    linarith
  · intro h
    funext i
    simp [cyclicDifference, h i]

/-
  The full gcd-dimension statement is best approached with an explicit
  equivalence between orbit classes of addition by d on ZMod k and ZMod gcd(k,d).

  This is deliberately left as a theorem target because it requires a
  nontrivial library/API choice for gcd arithmetic in ZMod.
-/
theorem tau_orbit_count
    (hk : 0 < k)
    (d : ℕ) :
    Fintype.card (Quotient (show Setoid (Idx k) from by
      sorry)) = Nat.gcd k d := by
  sorry

/-
  Strong orbit orthogonality should be stated only after an orbit
  representative/indexing system is implemented. For the immediate
  D22 uniqueness proof, an equivalent direct formulation is cleaner:

  Every kernel vector h of cyclicDifference d is constant on each
  translation orbit. If a is orthogonal to all such h, then norm pinning
  eliminates h.

  A practical interim theorem:
-/
theorem a_orthogonal_to_kernel
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0)
    (h : cyclicDifference d h = 0) :
    dot (a d) h = 0 := by
  /-
    This theorem needs:
    1. h is constant on each d-orbit;
    2. D22-CF has zero orbit sum.

    It avoids introducing orbit indicator objects into the first formal
    iteration.
  -/
  sorry

/-
  Uniqueness target:

  If b solves the same cyclic difference equation as a, then b-a belongs
  to ker cyclicDifference. If b has the same norm as a, orthogonality
  forces b=a.
-/
theorem norm_pinning_unique
    (hk : 2 < k)
    (d : Idx k)
    (hd0 : d ≠ 0)
    (b : Vec k)
    (h_same_difference :
      cyclicDifference d b = cyclicDifference d (a d))
    (h_same_norm :
      dot b b = dot (a d) (a d)) :
    b = a d := by
  let h := b - a d
  have hker : cyclicDifference d h = 0 := by
    simp [h, cyclicDifference, h_same_difference]
  have hortho : dot (a d) h = 0 :=
    a_orthogonal_to_kernel hk d hd0 h hker
  have hnorm :
      dot h h = 0 := by
    /-
      Expand:
        ||b-a||² = ||b||² - 2<a,b-a> - ||a||²
      and use:
        ||b||² = ||a||²
        <a,h> = 0.
    -/
    simp [h, dot] at *
    ring_nf at *
    linarith
  /-
    Conclude h=0 from a finite sum of nonnegative squares.
    This requires a separate lemma:
      dot h h = 0 -> h = 0
    over real finite vectors.
  -/
  have hz : h = 0 := by
    sorry
  simpa [h] using sub_eq_zero.mp hz

end
end D22
end Aqarion
