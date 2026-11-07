# Six-bit ten-point circuit containment

Feature row:
v(x) = (1, x_i, x_i*x_j for i<j), for x in {0,1}^6.

Let S be a ten-point rational circuit. Clear denominators in its
dependence and divide by the coefficient gcd. This gives a primitive
integer dependence c, with every coefficient on S nonzero.

Reduce c modulo two. The resulting binary vector b is nonzero by
primitivity and is orthogonal to every degree-at-most-two feature.

The finite checks in this run establish:
1. Every nonzero such binary vector supported on at most ten points
   has weight eight.
2. Every weight-eight such vector is an affine 3-flat incidence vector.

Thus the odd coefficients of c identify an eight-point affine 3-flat
F contained in S. Since S is a rational circuit, every proper subset
is independent, so the eight feature rows indexed by F have rank eight.

Uniqueness: two distinct affine 3-flats have intersection size at most
four, hence union size at least twelve. A ten-point support cannot
contain two of them.

Scope:
This proves containment from the checked finite parity lemmas and
elementary rational circuit properties. This run does not enumerate
rational ten-point circuits, rerun VERIFY-002, or independently certify
the global count 22400. That count requires the separate exhaustive
construction-family certificate and its verification.

Reference for the MacWilliams identity and Reed-Muller background:
https://people.math.harvard.edu/~elkies/M256.13/index.html
