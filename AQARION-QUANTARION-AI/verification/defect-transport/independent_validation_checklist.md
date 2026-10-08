# Independent Validation Checklist — AQARION Defect Transport

## Status

Python reference implementation supplied. Independent validation remains pending. A passing self-test is not an independent audit and does not establish Lean formalization.

## A. Clean Execution

- [ ] Run in a separate, clean sandbox.
- [ ] Record Python version, exact command, exit code and source SHA-256.
- [ ] Run `python defect_auditor.py --self-test --output fresh-output.json`.
- [ ] Confirm exit code `0` and `"all_pass": true`.
- [ ] Inspect every individual fixture result; do not rely only on the summary field.

## B. Independent Mathematical Recomputation

- [ ] Independently construct the block-averaging projection $$P_\Pi$$.
- [ ] Independently construct $$K$$ using the declared pullback convention $$K[x,T(x)]=1$$.
- [ ] Compute $$D_\Pi=(I-P_\Pi)KP_\Pi$$.
- [ ] Recompute the exact rational rank of $$D_\Pi$$.
- [ ] Recompute the transport matrix $$M_{ij}=\#\{x\in B_i:T(x)\in B_j\}$$.
- [ ] Reconstruct the support graph and count its connected components.
- [ ] Check $$\operatorname{rank}D_\Pi=k-c(H_M)$$.
- [ ] Check the component-indicator vectors span the restricted kernel.
- [ ] Compare direct Frobenius energy with the transport formula using exact fractions.

## C. Adversarial Controls

- [ ] Mutate the Koopman matrix construction to use the wrong orientation; ensure a test fails.
- [ ] Mutate the transport matrix convention; ensure a test fails.
- [ ] Mutate an energy denominator or introduce an erroneous factor of two; ensure a test fails.
- [ ] Verify that tests exercise the mutated implementation itself, rather than only comparing two separately chosen examples.
- [ ] Confirm failures return a nonzero exit code or an explicit `FAIL`.

## D. Input Validation

Test and require explicit rejection of:
- [ ] Empty state space.
- [ ] Out-of-range image under $$T$$.
- [ ] Empty partition block.
- [ ] Duplicate state across blocks.
- [ ] Missing state.
- [ ] Invalid or non-integer state label.

## E. Structural Fixtures

- [ ] Identity map with singleton blocks.
- [ ] A constant map.
- [ ] A non-injective map.
- [ ] A bijection.
- [ ] One-block partition.
- [ ] Partition into singletons.
- [ ] Same-support/different-multiplicity pair.

For the last pair, expected values are:

$$M_1=\begin{pmatrix}1&3\\3&1\end{pmatrix},\quad M_2=\begin{pmatrix}2&2\\2&2\end{pmatrix}.$$

Both support graphs are connected, both defect ranks equal $$1$$, and the exact energies are $$3/4$$ and $$1$$, respectively.

## F. Evidence and Governance

Record the validator/tool and version, source hash, command, exit code, tests performed, independent calculations, unresolved defects and reviewer.

Keep mathematical proof, Python verification, independent reproduction and Lean formalization as separate evidence categories. Do not promote AQARION to FORMAL, FROZEN or CLOSED on the basis of this script alone.
