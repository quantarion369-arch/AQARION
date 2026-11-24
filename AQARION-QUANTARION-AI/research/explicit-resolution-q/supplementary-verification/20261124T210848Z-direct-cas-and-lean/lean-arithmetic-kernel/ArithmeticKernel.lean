import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace Aqarion.P2Arithmetic

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

structure StrictFeasible (a0 a1 a2 a3 k : Int) : Prop where
  n0 : 0 < a0
  n1 : 0 < a1
  n2 : 0 < a2
  n3 : 0 < a3
  p01 : k < a0 + a1
  p02 : k < a0 + a2
  p03 : k < a0 + a3
  p12 : k < a1 + a2
  p13 : k < a1 + a3
  p23 : k < a2 + a3

theorem generator_A : Feasible 0 0 0 0 (-1) := by
  constructor <;> omega

theorem generator_E0 : Feasible 1 0 0 0 0 := by
  constructor <;> omega

theorem generator_E1 : Feasible 0 1 0 0 0 := by
  constructor <;> omega

theorem generator_E2 : Feasible 0 0 1 0 0 := by
  constructor <;> omega

theorem generator_E3 : Feasible 0 0 0 1 0 := by
  constructor <;> omega

theorem generator_B0 : Feasible 0 1 1 1 1 := by
  constructor <;> omega

theorem generator_B1 : Feasible 1 0 1 1 1 := by
  constructor <;> omega

theorem generator_B2 : Feasible 1 1 0 1 1 := by
  constructor <;> omega

theorem generator_B3 : Feasible 1 1 1 0 1 := by
  constructor <;> omega

theorem generator_C : Feasible 1 1 1 1 2 := by
  constructor <;> omega

variable {a0 a1 a2 a3 k : Int}

theorem subtract_B0_zero (h : Feasible a0 a1 a2 a3 k) (hk : 1 ≤ k) (hz : a0 = 0) : Feasible a0 (a1 - 1) (a2 - 1) (a3 - 1) (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_B1_zero (h : Feasible a0 a1 a2 a3 k) (hk : 1 ≤ k) (hz : a1 = 0) : Feasible (a0 - 1) a1 (a2 - 1) (a3 - 1) (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_B2_zero (h : Feasible a0 a1 a2 a3 k) (hk : 1 ≤ k) (hz : a2 = 0) : Feasible (a0 - 1) (a1 - 1) a2 (a3 - 1) (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_B3_zero (h : Feasible a0 a1 a2 a3 k) (hk : 1 ≤ k) (hz : a3 = 0) : Feasible (a0 - 1) (a1 - 1) (a2 - 1) a3 (k - 1) := by
  cases h
  constructor <;> omega

theorem subtract_C (h : Feasible a0 a1 a2 a3 k) (h0 : 1 ≤ a0) (h1 : 1 ≤ a1) (h2 : 1 ≤ a2) (h3 : 1 ≤ a3) : Feasible (a0 - 1) (a1 - 1) (a2 - 1) (a3 - 1) (k - 2) := by
  cases h
  constructor <;> omega

theorem subtract_B0_at_one (h : Feasible a0 a1 a2 a3 1) (h1 : 1 ≤ a1) (h2 : 1 ≤ a2) (h3 : 1 ≤ a3) : Feasible a0 (a1 - 1) (a2 - 1) (a3 - 1) 0 := by
  cases h
  constructor <;> omega

theorem strict_iff_shifted : StrictFeasible a0 a1 a2 a3 k ↔ Feasible (a0 - 1) (a1 - 1) (a2 - 1) (a3 - 1) (k - 1) := by
  constructor
  · intro h
    cases h
    constructor <;> omega
  · intro h
    cases h
    constructor <;> omega

theorem bound_after_B (n : Nat) (k : Int) (h : k ≤ ((n + 1 : Nat) : Int)) : k - 1 ≤ (n : Int) := by
  omega

theorem bound_after_C (n : Nat) (k : Int) (h : k ≤ ((n + 1 : Nat) : Int)) : k - 2 ≤ (n : Int) := by
  omega

theorem bound_by_toNat (k : Int) : k ≤ (Int.toNat k : Int) := by
  omega

end Aqarion.P2Arithmetic

#print axioms Aqarion.P2Arithmetic.generator_A
#print axioms Aqarion.P2Arithmetic.generator_E0
#print axioms Aqarion.P2Arithmetic.generator_E1
#print axioms Aqarion.P2Arithmetic.generator_E2
#print axioms Aqarion.P2Arithmetic.generator_E3
#print axioms Aqarion.P2Arithmetic.generator_B0
#print axioms Aqarion.P2Arithmetic.generator_B1
#print axioms Aqarion.P2Arithmetic.generator_B2
#print axioms Aqarion.P2Arithmetic.generator_B3
#print axioms Aqarion.P2Arithmetic.generator_C
#print axioms Aqarion.P2Arithmetic.subtract_B0_zero
#print axioms Aqarion.P2Arithmetic.subtract_B1_zero
#print axioms Aqarion.P2Arithmetic.subtract_B2_zero
#print axioms Aqarion.P2Arithmetic.subtract_B3_zero
#print axioms Aqarion.P2Arithmetic.subtract_C
#print axioms Aqarion.P2Arithmetic.subtract_B0_at_one
#print axioms Aqarion.P2Arithmetic.strict_iff_shifted
#print axioms Aqarion.P2Arithmetic.bound_after_B
#print axioms Aqarion.P2Arithmetic.bound_after_C
#print axioms Aqarion.P2Arithmetic.bound_by_toNat
