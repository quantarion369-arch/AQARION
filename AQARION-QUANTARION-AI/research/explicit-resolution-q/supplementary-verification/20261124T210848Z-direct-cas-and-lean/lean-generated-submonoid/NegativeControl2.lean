import Lean.Elab.Tactic.Omega

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

theorem should_fail : Feasible 0 0 0 0 1 := by
  constructor <;> omega
