import Lean.Elab.Tactic.Omega
set_option autoImplicit false

namespace Aqarion.P2Gen

structure Feasible (a0 a1 a2 a3 k : Int) : Prop where
  n0 : 0 ≤ a0
  n1 : 0 ≤ a1
  n2 : 0 ≤ a2
  n3 : 0 ≤ a3
  p01 : k ≤ a0 + a1
  p02 : k ≤ a0 + a2
  p03 : k ≤ a0 + a3
  p12 : k ≤ a1 + a2
  p13 : k ≤ a1 + a3
  p23 : k ≤ a2 + a3

inductive Gen : Int → Int → Int → Int → Int → Prop where
  | zero : Gen 0 0 0 0 0
  | addA {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen a0 a1 a2 a3 (k - 1)
  | addE0 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen (a0 + 1) a1 a2 a3 k
  | addE1 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen a0 (a1 + 1) a2 a3 k
  | addE2 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen a0 a1 (a2 + 1) a3 k
  | addE3 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen a0 a1 a2 (a3 + 1) k
  | addB0 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen a0 (a1 + 1) (a2 + 1) (a3 + 1) (k + 1)
  | addB1 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen (a0 + 1) a1 (a2 + 1) (a3 + 1) (k + 1)
  | addB2 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen (a0 + 1) (a1 + 1) a2 (a3 + 1) (k + 1)
  | addB3 {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen (a0 + 1) (a1 + 1) (a2 + 1) a3 (k + 1)
  | addC {a0 a1 a2 a3 k : Int} :
      Gen a0 a1 a2 a3 k → Gen (a0 + 1) (a1 + 1) (a2 + 1) (a3 + 1) (k + 2)

theorem gen_cast {a0 a1 a2 a3 k b0 b1 b2 b3 l : Int}
    (h : Gen a0 a1 a2 a3 k)
    (e0 : a0 = b0) (e1 : a1 = b1) (e2 : a2 = b2) (e3 : a3 = b3)
    (e : k = l) : Gen b0 b1 b2 b3 l := by
  subst e0
  subst e1
  subst e2
  subst e3
  subst e
  exact h

theorem gen_feasible {a0 a1 a2 a3 k : Int} (h : Gen a0 a1 a2 a3 k) :
    Feasible a0 a1 a2 a3 k := by
  induction h with
  | zero => constructor <;> omega
  | addA _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addE0 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addE1 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addE2 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addE3 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addB0 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addB1 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addB2 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addB3 _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega
  | addC _ ih =>
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := ih
    constructor <;> omega

theorem gen_A_mul (m : Nat) : Gen 0 0 0 0 (-(m : Int)) := by
  induction m with
  | zero => exact gen_cast Gen.zero rfl rfl rfl rfl (by omega)
  | succ m ih => exact gen_cast (Gen.addA ih) rfl rfl rfl rfl (by omega)

theorem gen_shift0 {a0 a1 a2 a3 k : Int} (h : Gen a0 a1 a2 a3 k) (m : Nat) :
    Gen (a0 + (m : Int)) a1 a2 a3 k := by
  induction m with
  | zero => exact gen_cast h (by omega) rfl rfl rfl rfl
  | succ m ih => exact gen_cast (Gen.addE0 ih) (by omega) rfl rfl rfl rfl

theorem gen_shift1 {a0 a1 a2 a3 k : Int} (h : Gen a0 a1 a2 a3 k) (m : Nat) :
    Gen a0 (a1 + (m : Int)) a2 a3 k := by
  induction m with
  | zero => exact gen_cast h rfl (by omega) rfl rfl rfl
  | succ m ih => exact gen_cast (Gen.addE1 ih) rfl (by omega) rfl rfl rfl

theorem gen_shift2 {a0 a1 a2 a3 k : Int} (h : Gen a0 a1 a2 a3 k) (m : Nat) :
    Gen a0 a1 (a2 + (m : Int)) a3 k := by
  induction m with
  | zero => exact gen_cast h rfl rfl (by omega) rfl rfl
  | succ m ih => exact gen_cast (Gen.addE2 ih) rfl rfl (by omega) rfl rfl

theorem gen_shift3 {a0 a1 a2 a3 k : Int} (h : Gen a0 a1 a2 a3 k) (m : Nat) :
    Gen a0 a1 a2 (a3 + (m : Int)) k := by
  induction m with
  | zero => exact gen_cast h rfl rfl rfl (by omega) rfl
  | succ m ih => exact gen_cast (Gen.addE3 ih) rfl rfl rfl (by omega) rfl

theorem gen_base {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k)
    (hk : k ≤ 0) : Gen a0 a1 a2 a3 k := by
  obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := h
  have h0 := gen_A_mul (Int.toNat (-k))
  have h1 := gen_shift0 h0 (Int.toNat a0)
  have h2 := gen_shift1 h1 (Int.toNat a1)
  have h3 := gen_shift2 h2 (Int.toNat a2)
  have h4 := gen_shift3 h3 (Int.toNat a3)
  exact gen_cast h4 (by omega) (by omega) (by omega) (by omega) (by omega)

theorem subtract_B0_zero {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k)
    (hk : 1 ≤ k) (hz : a0 = 0) :
    Feasible a0 (a1 - 1) (a2 - 1) (a3 - 1) (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_B1_zero {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k)
    (hk : 1 ≤ k) (hz : a1 = 0) :
    Feasible (a0 - 1) a1 (a2 - 1) (a3 - 1) (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_B2_zero {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k)
    (hk : 1 ≤ k) (hz : a2 = 0) :
    Feasible (a0 - 1) (a1 - 1) a2 (a3 - 1) (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_B3_zero {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k)
    (hk : 1 ≤ k) (hz : a3 = 0) :
    Feasible (a0 - 1) (a1 - 1) (a2 - 1) a3 (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_C {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k)
    (h0 : 1 ≤ a0) (h1 : 1 ≤ a1) (h2 : 1 ≤ a2) (h3 : 1 ≤ a3) :
    Feasible (a0 - 1) (a1 - 1) (a2 - 1) (a3 - 1) (k - 2) := by
  cases h
  constructor <;> omega

theorem subtract_B0_at_one {a0 a1 a2 a3 : Int} (h : Feasible a0 a1 a2 a3 1)
    (h1 : 1 ≤ a1) (h2 : 1 ≤ a2) (h3 : 1 ≤ a3) :
    Feasible a0 (a1 - 1) (a2 - 1) (a3 - 1) 0 := by
  cases h
  constructor <;> omega

theorem feasible_gen_aux :
    ∀ (n : Nat) (a0 a1 a2 a3 k : Int),
      Feasible a0 a1 a2 a3 k → k ≤ (n : Int) → Gen a0 a1 a2 a3 k := by
  intro n
  induction n with
  | zero =>
    intro a0 a1 a2 a3 k h hk
    exact gen_base h (by omega)
  | succ n ih =>
    intro a0 a1 a2 a3 k h hk
    have hc := h
    obtain ⟨n0, n1, n2, n3, p01, p02, p03, p12, p13, p23⟩ := hc
    by_cases hkn : k ≤ 0
    · exact gen_base h hkn
    have hk1 : 1 ≤ k := by omega
    by_cases z0 : a0 = 0
    · have g := ih _ _ _ _ _ (subtract_B0_zero h hk1 z0) (by omega)
      exact gen_cast (Gen.addB0 g) rfl (by omega) (by omega) (by omega) (by omega)
    by_cases z1 : a1 = 0
    · have g := ih _ _ _ _ _ (subtract_B1_zero h hk1 z1) (by omega)
      exact gen_cast (Gen.addB1 g) (by omega) rfl (by omega) (by omega) (by omega)
    by_cases z2 : a2 = 0
    · have g := ih _ _ _ _ _ (subtract_B2_zero h hk1 z2) (by omega)
      exact gen_cast (Gen.addB2 g) (by omega) (by omega) rfl (by omega) (by omega)
    by_cases z3 : a3 = 0
    · have g := ih _ _ _ _ _ (subtract_B3_zero h hk1 z3) (by omega)
      exact gen_cast (Gen.addB3 g) (by omega) (by omega) (by omega) rfl (by omega)
    have hz0 : 1 ≤ a0 := by omega
    have hz1 : 1 ≤ a1 := by omega
    have hz2 : 1 ≤ a2 := by omega
    have hz3 : 1 ≤ a3 := by omega
    by_cases k1 : k = 1
    · subst k1
      have g0 := gen_base (subtract_B0_at_one h hz1 hz2 hz3) (by omega)
      exact gen_cast (Gen.addB0 g0) rfl (by omega) (by omega) (by omega) (by omega)
    · have g := ih _ _ _ _ _ (subtract_C h hz0 hz1 hz2 hz3) (by omega)
      exact gen_cast (Gen.addC g) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem feasible_gen {a0 a1 a2 a3 k : Int} (h : Feasible a0 a1 a2 a3 k) :
    Gen a0 a1 a2 a3 k :=
  feasible_gen_aux (Int.toNat k) a0 a1 a2 a3 k h (by omega)

theorem gen_iff {a0 a1 a2 a3 k : Int} :
    Gen a0 a1 a2 a3 k ↔ Feasible a0 a1 a2 a3 k :=
  ⟨gen_feasible, feasible_gen⟩

end Aqarion.P2Gen

#print axioms Aqarion.P2Gen.gen_feasible
#print axioms Aqarion.P2Gen.gen_base
#print axioms Aqarion.P2Gen.feasible_gen
#print axioms Aqarion.P2Gen.gen_iff
