import Aqarion.D22.Projection
import Aqarion.D22.NilpotencyNorm

namespace Aqarion
namespace D22
namespace Smoke

open scoped BigOperators Matrix
open Matrix Finset

noncomputable section

/-
  Concrete checks are not substitutes for theorems. They are convention
  regression tests for the exact signs and index orientation.
-/

example :
    (K : Mat 6).mulVec (e (2 : Idx 6)) = e (1 : Idx 6) := by
  simpa using K_mulVec_e (k := 6) (by decide) (2 : Idx 6)

example :
    a (k := 6) (2 : Idx 6) =
      e (k := 6) 1 - e (k := 6) 3 := by
  simp [a, boundary]

example :
    a (k := 7) (1 : Idx 7) =
      (1 / 2 : ℝ) • e (k := 7) 0 +
      (1 / 2 : ℝ) • e (k := 7) 1 -
      e (k := 7) 2 := by
  simp [a, boundary]
  ring

example :
    a (k := 7) (-1 : Idx 7) =
      e (k := 7) 1 -
      (1 / 2 : ℝ) • e (k := 7) 0 -
      (1 / 2 : ℝ) • e (k := 7) (-1) := by
  simp [a, boundary]
  ring

end
end Smoke
end D22
end Aqarion
