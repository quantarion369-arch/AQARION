# Quadratic stability witnesses

Computed evidence for the real quadratic map x -> x^2 + c, starting at x = 0.

Definitions:
- bounded_orbit: the orbit remains with |x| <= 2 for 500 iterations.
- attracting_fixed_point: a real fixed point x* exists with |2x*| < 1.

These are two distinct readings of stability. Neither is assumed to imply the other.

| c | bounded_orbit | attracting_fixed_point |
|---|---|---|
| -2.0 | true | false |
| -1.0 | true | false |
| -0.5 | true | true |
| 0.0 | true | true |
| 0.2 | true | true |
| 0.25 | true | false |
| 0.3 | false | false |
| 0.5 | false | false |
| 1.0 | false | false |
| 1.5 | false | false |

Method: deterministic recomputation, standard library only, fixed iteration count.
Witness rule: a row with bounded_orbit = false is a counterexample witness against any universal bounded-orbit stability claim over the reals.

## Witness statements (bounded_orbit reading)

The quadratic map with c = -2.0 is stable under the bounded_orbit reading.

The quadratic map with c = -1.0 is stable under the bounded_orbit reading.

The quadratic map with c = -0.5 is stable under the bounded_orbit reading.

The quadratic map with c = 0.0 is stable under the bounded_orbit reading.

The quadratic map with c = 0.2 is stable under the bounded_orbit reading.

The quadratic map with c = 0.25 is stable under the bounded_orbit reading.

The quadratic map with c = 0.3 is unstable under the bounded_orbit reading.

The quadratic map with c = 0.5 is unstable under the bounded_orbit reading.

The quadratic map with c = 1.0 is unstable under the bounded_orbit reading.

The quadratic map with c = 1.5 is unstable under the bounded_orbit reading.

