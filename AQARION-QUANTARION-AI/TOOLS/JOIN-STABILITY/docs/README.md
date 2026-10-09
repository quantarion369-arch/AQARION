# JOIN-STABILITY Documentation

## Documents

- finite-pullback-rigidity.md contains the mathematical definitions,
  finite rigidity proof, incidence-graph join proof, and infinite
  counterexample.

## Evidence separation

The proof document is mathematical reasoning.
The Python audit is finite computation.
The Lean source is a formalization target and remains OPEN.
The reproduction receipt records what actually ran.

These evidence types are not interchangeable.

## Change control

When a theorem statement, proof, algorithm, expected count, or formal
definition changes:

1. update the relevant complete document;
2. identify dependent claims;
3. rerun the finite audit when computational behavior is affected;
4. compile Lean separately when Lean source changes;
5. record the tested Git revision and artifact hashes;
6. leave release promotion blocked until review is complete.
