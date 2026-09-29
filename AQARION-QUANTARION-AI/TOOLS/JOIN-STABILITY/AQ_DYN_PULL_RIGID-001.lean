import Mathlib.Data.Setoid.Basic
import Mathlib.Data.Fintype.Card

namespace AQARION

variable {X : Type*} [Fintype X]
variable (T : X → X)
variable (E : Setoid X)

/-- Pullback of an equivalence relation along a map. -/
def pullback (E : Setoid X) (T : X → X) : Setoid X :=
  E.comap T

/-- Finite pullback rigidity target. -/
theorem finite_pullback_rigidity
    (h : pullback E T ≤ E) :
    pullback E T = E := by
  sorry

end AQARION
