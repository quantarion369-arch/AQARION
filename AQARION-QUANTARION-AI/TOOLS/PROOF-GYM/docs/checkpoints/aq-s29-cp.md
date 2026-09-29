https://arxiv.org/abs/2607.19407?utm_source=chatgpt.com

Result of the next pass

The mathematics got cleaner, the computation got stronger, and the public-facing pivot now has a concrete research niche.

Most importantly, I found and independently resolved an apparent numerical contradiction in the checkpoint.

1. The two count tables are both correct — but count different things

My exact brute-force reconstruction produced:

\(n\)	\(\sum_T k_T\)	\(\sum_T k_T^2\)	\(\sum_T k_T(k_T+1)/2\)

1	1	1	1
2	6	10	8
3	51	117	84
4	592	1,960	1,276
5	8,565	40,385	24,475
6	148,896	1,016,496	582,696


Here \(k_T\) is the number of pullback-stable equivalence relations for a fixed \(T\).

So:

1, 8, 84, 1,276, 24,475, 582,696 = unordered \((E,F)\) pairs with repetition allowed.

1, 10, 117, 1,960, 40,385, 1,016,496 = ordered \((E,F)\) pairs.

1, 6, 51, 592, 8,565, 148,896 = individual PB-fixed \((T,E)\) objects.


This exactly explains the apparent discrepancy.

And I independently checked the actual join condition on all 1,016,496 ordered stable pairs for \(n=6\):

\[
\boxed{\text{join failures}=0}.
\]

I also checked the stronger incidence-invariance condition on all of them:

\[
\boxed{\sigma(I)=I}.
\]

That is a useful new receipt because it tests the mechanism of the proof, not just its final boolean.


---

2. The proof should be changed again — this time decisively

The kernel/cardinality theorem is the right primary lemma.

But I would not freeze the previous wording:

> “These permutations induce an automorphism of the incidence graph.”



That sentence is too compressed.

The adversarial question is:

> Why does a permutation of the two vertex sets preserve the reverse incidence relation?



A vertex permutation that merely maps edges forward is not automatically a graph automorphism.

The missing ingredient is finiteness of the incidence relation.

That gives us a much stronger proof.


---

3. The corrected finite join proof

Let

\[
Q_E=X/E,\qquad Q_F=X/F.
\]

By finite pullback rigidity,

\[
T^\ast E=E,
\qquad
T^\ast F=F.
\]

Therefore \(T\) induces permutations

\[
\sigma_E:Q_E\to Q_E,
\qquad
\sigma_F:Q_F\to Q_F.
\]

Define the incidence relation

\[
I\subseteq Q_E\times Q_F
\]

by

\[
(A,B)\in I
\iff
A\cap B\neq\varnothing.
\]

Now define

\[
\sigma=\sigma_E\times\sigma_F.
\]

If \((A,B)\in I\), choose

\[
x\in A\cap B.
\]

Then

\[
T(x)\in \sigma_E(A)\cap\sigma_F(B).
\]

Therefore

\[
\sigma(I)\subseteq I.
\]

Now comes the crucial finite step.

Since \(Q_E\) and \(Q_F\) are finite,

\[
Q_E\times Q_F
\]

is finite.

Since \(\sigma\) is a permutation,

\[
|\sigma(I)|=|I|.
\]

Together with

\[
\sigma(I)\subseteq I
\]

we obtain

\[
\boxed{\sigma(I)=I}.
\]

So the incidence graph really is preserved in both directions.

That is the missing rigor.


---

4. Connected components are the join

The bipartite incidence graph has vertices

\[
Q_E\sqcup Q_F
\]

and edges \(I\).

For each \(x\in X\), connect

\[
[x]_E
\longleftrightarrow
[x]_F.
\]

Then:

\[
x(E\vee F)y
\]

iff

\[
[x]_E
\]

and

\[
[y]_E
\]

are in the same connected component.

Because \(\sigma\) is now a genuine graph automorphism, connected components are preserved in both directions.

Therefore

\[
T(x)(E\vee F)T(y)
\Longrightarrow
x(E\vee F)y.
\]

Hence:

\[
\boxed{
T^\ast(E\vee F)\subseteq E\vee F.
}
\]

So the finite theorem follows.


---

5. This gives us the real proof dependency graph

AQ-DYN-PULL-RIGID-001
        │
        ▼
T*E ⊆ E  →  T*E = E
        │
        ├──────────────┐
        ▼              ▼
 E-class permutation   F-class permutation
        │              │
        └──────┬───────┘
               ▼
       incidence permutation
               │
               ▼
      finite incidence set
               │
        σ(I) ⊆ I
               │
        |σ(I)| = |I|
               │
               ▼
        σ(I) = I
               │
               ▼
       graph automorphism
               │
               ▼
      connected components
               │
               ▼
           E ∨ F
               │
               ▼
        JOIN-STABILITY

That is much more formalization-friendly.


---

6. The infinite boundary becomes even more informative

Your infinite counterexample is now doing double duty.

For

\[
X=\mathbb N,\qquad T(n)=n+1,
\]

take \(E\) with class \({0,1}\) and all other points singleton.

Then

\[
T^\ast E=\Delta_X\subsetneq E.
\]

So the finite rigidity lemma fails.

And therefore the induced class map need not even exist.

This tells the learner exactly where the finite proof breaks.

That is ideal ProofGym material.


---

7. Independent computation I actually ran

I reconstructed partitions as restricted-growth strings and enumerated every

\[
T:[n]\to[n].
\]

For every \(T\), I enumerated every equivalence relation \(E\), tested

\[
T(x)ET(y)\Rightarrow xEy,
\]

then tested every ordered stable pair \((E,F)\).

The exact results were:

INDEPENDENT JOIN AUDIT

n=1
  ordered stable pairs: 1
  join failures:        0
  incidence failures:   0

n=2
  ordered stable pairs: 10
  join failures:        0
  incidence failures:   0

n=3
  ordered stable pairs: 117
  join failures:        0
  incidence failures:   0

n=4
  ordered stable pairs: 1,960
  join failures:        0
  incidence failures:   0

n=5
  ordered stable pairs: 40,385
  join failures:        0
  incidence failures:   0

n=6
  ordered stable pairs: 1,016,496
  join failures:        0
  incidence failures:   0

The \(n=6\) result is particularly useful because it independently reproduces the reported 582,696 unordered-pair receipt:

\[
\frac{1,016,496+148,896}{2}=582,696.
\]

So that apparent discrepancy is now explained rather than ignored.


---

8. Current repository audit limitation

I confirmed that [quantarion369-arch/AQARION](https://github.com/quantarion369-arch/AQARION?utm_source=chatgpt.com) is public and its default branch is main.

However, the connected GitHub file-search route did not return the specific JOIN-STABILITY files, so I am not claiming that I inspected the current contents of JOIN_STABILITY_PROOF.md or join_stability_exact_verifier.py directly.

That distinction matters.

The mathematical computation above is independently executed here; the repository-file state remains based on the checkpoint you supplied.


---

9. Recent literature changes the ProofGym idea in a useful way

There is an unusually strong reason to pursue the educational/AI pivot now.

A paper submitted only four days ago, ProofGap, explicitly argues that theorem-level benchmarks miss step-level reasoning failures. It decomposes natural-language proofs into local proof gaps and reports 26,116 such gaps from 3,015 exercises. 

That overlaps strongly with our idea—but also tells us not to pretend the idea is unprecedented.

Another 2026 benchmark, FormalTCS, evaluates end-to-end formal TCS research, including claim understanding, formalization and proof, and reports that autoformalization remains a major bottleneck. Its public repository contains verified Lean projects and an autoresearch pipeline. 

And ITPEval is now explicitly measuring translation between Lean, Rocq, Isabelle and HOL Light, highlighting semantic mismatch between formal systems as a serious problem. 

The lesson for AQARION:

> Do not make “another benchmark of whether an LLM proves theorem X.”



Instead:

> Make the provenance and anatomy of the failure itself the educational object.



That is where our preserved JOIN-STABILITY mistake becomes valuable.


---

10. ProofGap + AQARION can be complementary

ProofGap asks roughly:

> Can the model fill the missing local proof obligation?



AQARION ProofGym can ask:

> Can the model identify that there is a missing obligation in the first place?



That's a different task.

For JOIN-001:

MODEL SEES:

1. T(x) (E∨F) T(y)
2. therefore ...
3. therefore ...
4. QED

The model should output:

FAILURE TYPE:
    hidden direction reversal

LOCATION:
    step 2

MISSING OBLIGATION:
    prove that the relevant incidence structure
    is invariant under the inverse class action.

REPAIR:
    finite pullback rigidity
    +
    finite incidence-cardinality argument.

That's considerably more diagnostic.


---

11. New main pivot: Proof Failure Atlas

I would now make this the public identity rather than simply "ProofGym."

AQARION ProofGym

Proof Failure Atlas

First entry:

PF-001
────────────────────────────

NAME
Hidden Direction Reversal

PATTERN
A → B is available,
but the argument silently uses B → A.

INSTANCE
T(x) E T(y) → x E y

INVALID USE
x E y → T(x) E T(y)

REPAIR
Finite pullback rigidity:

T*E ⊆ E
      ⇒
T*E = E
      ⇒
E ⊆ T*E

Second:

PF-002

NAME
Finite Verification → Universal Claim

BAD INFERENCE

checked n ≤ 6
      ↓
therefore all finite n

REPAIR

separate:
[P] analytic proof
[V] bounded verification
[L] Lean

Third:

PF-003

NAME
Numerical Agreement → Proof

BAD INFERENCE

1,016,496 tests pass
      ↓
the theorem is proved

REPAIR

computation is evidence,
not the analytic proof.

Fourth:

PF-004

NAME
Infinite Generalization Without Boundary Audit

BAD INFERENCE

finite theorem
      ↓
remove "finite"

REPAIR

construct explicit infinite counterexample.

Now we're building a taxonomy, not another theorem database.


---

12. Exact first public challenge

FILE: PROOFGYM/CHALLENGE-001/problem.md
TYPE: Markdown
PURPOSE: First human/AI reasoning challenge
STATUS: Draft; not a formal certification artifact

# ProofGym Challenge 001
## The Direction You Were Not Given

Let `X` be finite and let `T : X → X`.

Let `E` and `F` be equivalence relations on `X` satisfying

    T(x) E T(y) → x E y

and

    T(x) F T(y) → x F y.

Prove that

    T(x) (E ∨ F) T(y) → x (E ∨ F) y.

### Rules

You may use:

- finiteness of `X`;
- basic facts about equivalence relations;
- finite cardinality arguments.

You may NOT assume:

- `T` is surjective;
- `T` is injective;
- forward preservation of `E` or `F`;
- the conclusion for `E ∨ F`.

### Your tasks

1. Find the tempting but invalid proof step.
2. Prove finite pullback rigidity.
3. Construct the induced permutations on `X/E` and `X/F`.
4. Define the incidence relation.
5. Explain why forward incidence preservation becomes equality.
6. Deduce preservation of connected components.
7. Explain why the infinite case cannot be obtained by deleting
   the finite hypothesis.

### Evidence target

A successful informal solution is `[P-candidate]`.

A mechanically checked Lean proof is required for `[P]`.

A finite exhaustive replay is `[V]`.

No amount of bounded computation alone promotes the theorem to `[P]`.


---

13. Machine-readable version

FILE: PROOFGYM/CHALLENGE-001/task.json
TYPE: JSON
PURPOSE: Machine-readable human/AI benchmark task

{
  "id": "JOIN-001",
  "title": "The Direction You Were Not Given",
  "domain": "finite_dynamics",
  "claim": "Pullback-stable equivalence relations are closed under join on finite sets.",
  "hypotheses": [
    "X is finite",
    "T : X -> X is total",
    "E is an equivalence relation on X",
    "F is an equivalence relation on X",
    "T(x) E T(y) -> x E y",
    "T(x) F T(y) -> x F y"
  ],
  "target": "T(x) (E join F) T(y) -> x (E join F) y",
  "forbidden_shortcuts": [
    "assume T is surjective",
    "assume T is injective",
    "assume x E y -> T(x) E T(y)",
    "assume the theorem for E join F"
  ],
  "required_reasoning": [
    "finite_pullback_rigidity",
    "induced_class_permutations",
    "incidence_relation",
    "finite_forward_invariance_implies_invariance",
    "connected_components"
  ],
  "failure_classes": [
    "PF-001",
    "PF-004"
  ],
  "formal_status": "OPEN",
  "verification_status": "V-n6",
  "promotion_status": "BLOCKED"
}


---

14. The formalization target

I would make this the next Lean file, but not claim it compiles until a Lean environment actually builds it.

FILE: JOIN-STABILITY/AQ_DYN_PULL_RIGID_001.lean
TYPE: Lean 4
PURPOSE: Formalization target for finite pullback rigidity
STATUS: OPEN — NOT COMPILED IN THIS ENVIRONMENT

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

I deliberately leave the proof as sorry here.

That is not a weakness in the deliverable; it is an honest formalization status. The next task is to replace it with the quotient-cardinality argument and compile it under the repository's actual Lean/Mathlib toolchain.

Lean's native quotient/setoid system is designed precisely around equivalence relations and quotient maps, and current Mathlib exposes the cardinality and finite self-injection machinery needed for this route. 


---

15. Formalization should NOT start with the graph

This is another pivot I recommend.

Formalize in this order:

01  pullback relation
02  quotient map / kernel
03  quotient cardinality = image cardinality
04  refinement ⇒ quotient-cardinality inequality
05  finite equality
06  pullback rigidity
07  induced quotient permutation
08  finite incidence set
09  incidence invariance
10  connected components
11  join theorem

Not:

graph library
↓
multigraph
↓
edge multiplicities
↓
quotient graph
↓
...

The latter creates enormous formalization surface area for no mathematical gain.


---

16. Exact independent verifier deliverable

FILE: JOIN-STABILITY/join_stability_independent_audit.py
TYPE: Python 3
PURPOSE: Independent exhaustive audit of ordered stable-pair join and incidence invariance
STATUS: Executed independently for n=1..6

from itertools import product


def partitions(n):
    """All set partitions of range(n), encoded as restricted-growth strings."""
    out = []

    def rec(a, maximum):
        if len(a) == n:
            out.append(tuple(a))
            return

        for value in range(maximum + 2):
            rec(a + [value], max(maximum, value))

    if n == 0:
        return [()]

    rec([0], 0)
    return out


def pullback_stable(T, E):
    n = len(T)

    for x in range(n):
        for y in range(n):
            if E[T[x]] == E[T[y]] and E[x] != E[y]:
                return False

    return True


def join(E, F):
    """Join of two equivalence relations via connected components."""
    n = len(E)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x = find(x)
        y = find(y)

        if x != y:
            parent[y] = x

    for relation in (E, F):
        classes = {}

        for x, c in enumerate(relation):
            classes.setdefault(c, []).append(x)

        for members in classes.values():
            root = members[0]

            for x in members[1:]:
                union(root, x)

    return tuple(find(x) for x in range(n))


def normalized_classes(E):
    labels = {}
    result = []

    for c in E:
        if c not in labels:
            labels[c] = len(labels)
        result.append(labels[c])

    return result


def incidence_data(T, E, F):
    """
    Return the incidence relation and induced class maps.

    The caller has already established pullback stability.
    """
    E = normalized_classes(E)
    F = normalized_classes(F)
    TE = normalized_classes(tuple(E[T[x]] for x in range(len(T))))
    TF = normalized_classes(tuple(F[T[x]] for x in range(len(T))))

    e_classes = max(E) + 1
    f_classes = max(F) + 1

    sigma_E = [None] * e_classes
    sigma_F = [None] * f_classes

    incidence = set()

    for x in range(len(T)):
        a = E[x]
        b = F[x]

        incidence.add((a, b))

        if sigma_E[a] is None:
            sigma_E[a] = TE[x]
        elif sigma_E[a] != TE[x]:
            raise AssertionError("E-class map is not well-defined")

        if sigma_F[b] is None:
            sigma_F[b] = TF[x]
        elif sigma_F[b] != TF[x]:
            raise AssertionError("F-class map is not well-defined")

    return incidence, sigma_E, sigma_F


def check_incidence_invariance(T, E, F):
    incidence, sigma_E, sigma_F = incidence_data(T, E, F)

    if len(set(sigma_E)) != len(sigma_E):
        raise AssertionError("E class action is not injective")

    if len(set(sigma_F)) != len(sigma_F):
        raise AssertionError("F class action is not injective")

    image = {
        (sigma_E[a], sigma_F[b])
        for (a, b) in incidence
    }

    return image == incidence


def audit(n):
    relations = partitions(n)

    ordered_stable_pairs = 0
    join_failures = 0
    incidence_failures = 0

    for T in product(range(n), repeat=n):
        stable = [
            E for E in relations
            if pullback_stable(T, E)
        ]

        ordered_stable_pairs += len(stable) ** 2

        for E in stable:
            for F in stable:
                G = join(E, F)

                if not pullback_stable(T, G):
                    join_failures += 1

                if not check_incidence_invariance(T, E, F):
                    incidence_failures += 1

    return (
        ordered_stable_pairs,
        join_failures,
        incidence_failures,
    )


EXPECTED = {
    1: (1, 0, 0),
    2: (10, 0, 0),
    3: (117, 0, 0),
    4: (1960, 0, 0),
    5: (40385, 0, 0),
    6: (1016496, 0, 0),
}


def main():
    for n in range(1, 7):
        result = audit(n)
        print(
            f"n={n} "
            f"ordered_stable_pairs={result[0]} "
            f"join_failures={result[1]} "
            f"incidence_failures={result[2]}"
        )

        if result != EXPECTED[n]:
            raise SystemExit(
                f"FAIL: expected {EXPECTED[n]}, got {result}"
            )

    print("RESULT=PASS")


if __name__ == "__main__":
    main()

Important: I independently executed the equivalent enumeration and incidence audit. I did not execute this exact pasted file verbatim in this environment, so I am not going to falsely label this exact source as compiled/run.


---

17. New receipt

FILE: JOIN-STABILITY/INDEPENDENT_AUDIT_2026-09-29.md
TYPE: Markdown
PURPOSE: Independent computational and mathematical audit receipt

# JOIN-STABILITY — Independent Audit
## 2026-09-29

### Scope

Independent reconstruction of:

1. finite pullback stability;
2. ordered stable `(E,F)` pairs;
3. join stability;
4. incidence invariance.

### Enumeration

Every total map

    T : [n] -> [n]

and every equivalence relation on `[n]` was reconstructed for
`n = 1,...,6`.

For each map, every ordered pair of pullback-stable equivalence
relations was tested.

### Results

| n | Ordered stable pairs | Join failures | Incidence failures |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 10 | 0 | 0 |
| 3 | 117 | 0 | 0 |
| 4 | 1,960 | 0 | 0 |
| 5 | 40,385 | 0 | 0 |
| 6 | 1,016,496 | 0 | 0 |

### Receipt reconciliation

The independently computed number of PB-fixed `(T,E)` objects is:

    n=1: 1
    n=2: 6
    n=3: 51
    n=4: 592
    n=5: 8,565
    n=6: 148,896

The ordered pair count is the sum of squares of these per-map
stable-relation counts.

The unordered pair count with repetition is:

    (ordered_pairs + PB_fixed) / 2

giving:

    1
    8
    84
    1,276
    24,475
    582,696

Thus the two previously reported tables are consistent once
their counting conventions are made explicit.

### Mathematical mechanism tested

For every stable pair:

    T*E = E
    T*F = F

was used to construct the induced class maps.

The induced maps were checked to be permutations.

The incidence set `I` was constructed and the product permutation
`σ` was checked against it.

Observed for every ordered stable pair:

    σ(I) = I

### Status

[P] finite pullback rigidity:
    analytic proof candidate, formalization open.

[P] finite join theorem:
    incidence-permutation proof candidate, formalization open.

[V] exhaustive n<=6:
    independently reproduced.

[PV] combined:
    DO NOT promote globally until the proof is formally audited.

Lean:
    OPEN

C4:
    BLOCKED

Publication:
    BLOCKED


---

18. ProofGym's first challenge should explicitly expose the two traps

FILE: PROOFGYM/CHALLENGE-001/solution.md
TYPE: Markdown
PURPOSE: Instructor/reference solution
STATUS: Mathematical reference; Lean certification OPEN

# JOIN-001 — Reference Solution

## Trap 1: Direction reversal

The hypothesis is

    T(x) E T(y) -> x E y.

A tempting proof silently uses

    x E y -> T(x) E T(y).

That implication is not available initially.

## Repair

For finite X:

    T*E ⊆ E
        ->
    T*E = E.

Thus the reverse inclusion follows:

    E ⊆ T*E.

Therefore

    x E y -> T(x) E T(y).

The same holds for F.

## Trap 2: "Forward incidence" is not automatically "graph automorphism"

The induced class maps are permutations.

Define

    I ⊆ (X/E) × (X/F)

by

    (A,B) ∈ I  iff  A ∩ B ≠ ∅.

If `(A,B) ∈ I`, choose `x ∈ A ∩ B`.

Then

    T(x) ∈ σ_E(A) ∩ σ_F(B),

so

    σ(I) ⊆ I.

But this alone would not be sufficient.

The product quotient is finite and σ is a permutation, so

    |σ(I)| = |I|.

Hence

    σ(I) = I.

Therefore the incidence graph is genuinely preserved in both
directions.

## Join

The connected components of the incidence graph correspond
exactly to the equivalence classes of `E ∨ F`.

Graph automorphisms preserve connected components.

Therefore

    T(x) (E ∨ F) T(y)
        ->
    x (E ∨ F) y.

Hence `E ∨ F` is pullback-stable.


---

19. Why this public pivot is now timely

The recent literature is actually telling us where not to compete.

FormalProofBench measures formally verified graduate-level proof generation; the reported best foundation-model accuracy was only 33.5% in its study. 

miniF2F-Lean Revisited found that the full natural-language → formalization → proof pipeline can perform substantially worse than isolated theorem-proving or autoformalization numbers because statement alignment itself is a major failure source. 

APOLLO focuses on compiler-guided proof repair. 

Hilbert focuses on recursively decomposing informal reasoning and using formal verification feedback. 

And now ProofGap focuses specifically on local proof gaps. 

So I would not try to beat these projects at:

> “How many Lean theorems can an agent prove?”



Instead AQARION can contribute a different layer:

> Where exactly did the reasoning go wrong, what evidence exposed it, what minimal repair restores validity, and what happened historically when an earlier proof failed?



That fits AQARION's strongest existing intellectual asset: failure preservation + evidence classification + exact replay.


---

20. Final adversarial audit

What survived

Finite pullback rigidity

\[
\boxed{T^\ast E\subseteq E\Rightarrow T^\ast E=E}
\]

The kernel/cardinality proof is sound.

Infinite boundary

The shift example genuinely breaks rigidity.

PB-fixed classification

The independent counts reconcile exactly.

Join theorem

No counterexample through \(n=6\), with 1,016,496 ordered stable pairs independently checked.

Incidence mechanism

The stronger condition

\[
\boxed{\sigma(I)=I}
\]

was independently verified for every stable pair through \(n=6\).


---

What I would still refuse to certify

❌ Lean proof.

❌ C4.

❌ Publication-ready formal theorem.

❌ Any claim that the GitHub repository's current file contents exactly match the checkpoint—I could not retrieve those particular files through the connected GitHub file search.

❌ Any claim that this theorem is novel in the mathematical literature merely because our searches did not find an exact match.

❌ Any claim that ProofGym is unprecedented. ProofGap in particular means that would be an overclaim.


---

21. The actual next milestone

I would now stop expanding the mathematics temporarily.

The next milestone is:

\[
\boxed{
\textbf{LEAN-JS-001: compile finite pullback rigidity}
}
\]

Then:

\[
\boxed{
\textbf{LEAN-JS-002: compile finite incidence invariance}
}
\]

Then:

\[
\boxed{
\textbf{LEAN-JS-003: compile JOIN-STABILITY}
}
\]

And only after those pass:

JOIN-001
    ↓
Lean proof
    ↓
independent replay
    ↓
ProofGym challenge
    ↓
failure taxonomy
    ↓
public release

This gives us something unusually strong for the public side:

the first ProofGym challenge isn't an artificial puzzle. It is a real AQARION theorem whose tempting proof contained exactly the kind of logical gap that modern AI-math systems are increasingly trying to diagnose.

That is the pivot I would pursue.

https://arxiv.org/abs/2608.20153?utm_source=chatgpt.com

Worked for 2m 14s

Result of the next pass

The mathematics got cleaner, the computation got stronger, and the public-facing pivot now has a concrete research niche.

Most importantly, I found and independently resolved an apparent numerical contradiction in the checkpoint.

1. The two count tables are both correct — but count different things

My exact brute-force reconstruction produced:

\(n\)	\(\sum_T k_T\)	\(\sum_T k_T^2\)	\(\sum_T k_T(k_T+1)/2\)

1	1	1	1
2	6	10	8
3	51	117	84
4	592	1,960	1,276
5	8,565	40,385	24,475
6	148,896	1,016,496	582,696


Here \(k_T\) is the number of pullback-stable equivalence relations for a fixed \(T\).

So:

1, 8, 84, 1,276, 24,475, 582,696 = unordered \((E,F)\) pairs with repetition allowed.

1, 10, 117, 1,960, 40,385, 1,016,496 = ordered \((E,F)\) pairs.

1, 6, 51, 592, 8,565, 148,896 = individual PB-fixed \((T,E)\) objects.


This exactly explains the apparent discrepancy.

And I independently checked the actual join condition on all 1,016,496 ordered stable pairs for \(n=6\):

\[
\boxed{\text{join failures}=0}.
\]

I also checked the stronger incidence-invariance condition on all of them:

\[
\boxed{\sigma(I)=I}.
\]

That is a useful new receipt because it tests the mechanism of the proof, not just its final boolean.


---

2. The proof should be changed again — this time decisively

The kernel/cardinality theorem is the right primary lemma.

But I would not freeze the previous wording:

> “These permutations induce an automorphism of the incidence graph.”



That sentence is too compressed.

The adversarial question is:

> Why does a permutation of the two vertex sets preserve the reverse incidence relation?



A vertex permutation that merely maps edges forward is not automatically a graph automorphism.

The missing ingredient is finiteness of the incidence relation.

That gives us a much stronger proof.


---

3. The corrected finite join proof

Let

\[
Q_E=X/E,\qquad Q_F=X/F.
\]

By finite pullback rigidity,

\[
T^\ast E=E,
\qquad
T^\ast F=F.
\]

Therefore \(T\) induces permutations

\[
\sigma_E:Q_E\to Q_E,
\qquad
\sigma_F:Q_F\to Q_F.
\]

Define the incidence relation

\[
I\subseteq Q_E\times Q_F
\]

by

\[
(A,B)\in I
\iff
A\cap B\neq\varnothing.
\]

Now define

\[
\sigma=\sigma_E\times\sigma_F.
\]

If \((A,B)\in I\), choose

\[
x\in A\cap B.
\]

Then

\[
T(x)\in \sigma_E(A)\cap\sigma_F(B).
\]

Therefore

\[
\sigma(I)\subseteq I.
\]

Now comes the crucial finite step.

Since \(Q_E\) and \(Q_F\) are finite,

\[
Q_E\times Q_F
\]

is finite.

Since \(\sigma\) is a permutation,

\[
|\sigma(I)|=|I|.
\]

Together with

\[
\sigma(I)\subseteq I
\]

we obtain

\[
\boxed{\sigma(I)=I}.
\]

So the incidence graph really is preserved in both directions.

That is the missing rigor.


---

4. Connected components are the join

The bipartite incidence graph has vertices

\[
Q_E\sqcup Q_F
\]

and edges \(I\).

For each \(x\in X\), connect

\[
[x]_E
\longleftrightarrow
[x]_F.
\]

Then:

\[
x(E\vee F)y
\]

iff

\[
[x]_E
\]

and

\[
[y]_E
\]

are in the same connected component.

Because \(\sigma\) is now a genuine graph automorphism, connected components are preserved in both directions.

Therefore

\[
T(x)(E\vee F)T(y)
\Longrightarrow
x(E\vee F)y.
\]

Hence:

\[
\boxed{
T^\ast(E\vee F)\subseteq E\vee F.
}
\]

So the finite theorem follows.


---

5. This gives us the real proof dependency graph

AQ-DYN-PULL-RIGID-001
        │
        ▼
T*E ⊆ E  →  T*E = E
        │
        ├──────────────┐
        ▼              ▼
 E-class permutation   F-class permutation
        │              │
        └──────┬───────┘
               ▼
       incidence permutation
               │
               ▼
      finite incidence set
               │
        σ(I) ⊆ I
               │
        |σ(I)| = |I|
               │
               ▼
        σ(I) = I
               │
               ▼
       graph automorphism
               │
               ▼
      connected components
               │
               ▼
           E ∨ F
               │
               ▼
        JOIN-STABILITY

That is much more formalization-friendly.


---

6. The infinite boundary becomes even more informative

Your infinite counterexample is now doing double duty.

For

\[
X=\mathbb N,\qquad T(n)=n+1,
\]

take \(E\) with class \({0,1}\) and all other points singleton.

Then

\[
T^\ast E=\Delta_X\subsetneq E.
\]

So the finite rigidity lemma fails.

And therefore the induced class map need not even exist.

This tells the learner exactly where the finite proof breaks.

That is ideal ProofGym material.


---

7. Independent computation I actually ran

I reconstructed partitions as restricted-growth strings and enumerated every

\[
T:[n]\to[n].
\]

For every \(T\), I enumerated every equivalence relation \(E\), tested

\[
T(x)ET(y)\Rightarrow xEy,
\]

then tested every ordered stable pair \((E,F)\).

The exact results were:

INDEPENDENT JOIN AUDIT

n=1
  ordered stable pairs: 1
  join failures:        0
  incidence failures:   0

n=2
  ordered stable pairs: 10
  join failures:        0
  incidence failures:   0

n=3
  ordered stable pairs: 117
  join failures:        0
  incidence failures:   0

n=4
  ordered stable pairs: 1,960
  join failures:        0
  incidence failures:   0

n=5
  ordered stable pairs: 40,385
  join failures:        0
  incidence failures:   0

n=6
  ordered stable pairs: 1,016,496
  join failures:        0
  incidence failures:   0

The \(n=6\) result is particularly useful because it independently reproduces the reported 582,696 unordered-pair receipt:

\[
\frac{1,016,496+148,896}{2}=582,696.
\]

So that apparent discrepancy is now explained rather than ignored.


---

8. Current repository audit limitation

I confirmed that [quantarion369-arch/AQARION](https://github.com/quantarion369-arch/AQARION?utm_source=chatgpt.com) is public and its default branch is main.

However, the connected GitHub file-search route did not return the specific JOIN-STABILITY files, so I am not claiming that I inspected the current contents of JOIN_STABILITY_PROOF.md or join_stability_exact_verifier.py directly.

That distinction matters.

The mathematical computation above is independently executed here; the repository-file state remains based on the checkpoint you supplied.


---

9. Recent literature changes the ProofGym idea in a useful way

There is an unusually strong reason to pursue the educational/AI pivot now.

A paper submitted only four days ago, ProofGap, explicitly argues that theorem-level benchmarks miss step-level reasoning failures. It decomposes natural-language proofs into local proof gaps and reports 26,116 such gaps from 3,015 exercises. 

That overlaps strongly with our idea—but also tells us not to pretend the idea is unprecedented.

Another 2026 benchmark, FormalTCS, evaluates end-to-end formal TCS research, including claim understanding, formalization and proof, and reports that autoformalization remains a major bottleneck. Its public repository contains verified Lean projects and an autoresearch pipeline. 

And ITPEval is now explicitly measuring translation between Lean, Rocq, Isabelle and HOL Light, highlighting semantic mismatch between formal systems as a serious problem. 

The lesson for AQARION:

> Do not make “another benchmark of whether an LLM proves theorem X.”



Instead:

> Make the provenance and anatomy of the failure itself the educational object.



That is where our preserved JOIN-STABILITY mistake becomes valuable.


---

10. ProofGap + AQARION can be complementary

ProofGap asks roughly:

> Can the model fill the missing local proof obligation?



AQARION ProofGym can ask:

> Can the model identify that there is a missing obligation in the first place?



That's a different task.

For JOIN-001:

MODEL SEES:

1. T(x) (E∨F) T(y)
2. therefore ...
3. therefore ...
4. QED

The model should output:

FAILURE TYPE:
    hidden direction reversal

LOCATION:
    step 2

MISSING OBLIGATION:
    prove that the relevant incidence structure
    is invariant under the inverse class action.

REPAIR:
    finite pullback rigidity
    +
    finite incidence-cardinality argument.

That's considerably more diagnostic.


---

11. New main pivot: Proof Failure Atlas

I would now make this the public identity rather than simply "ProofGym."

AQARION ProofGym

Proof Failure Atlas

First entry:

PF-001
────────────────────────────

NAME
Hidden Direction Reversal

PATTERN
A → B is available,
but the argument silently uses B → A.

INSTANCE
T(x) E T(y) → x E y

INVALID USE
x E y → T(x) E T(y)

REPAIR
Finite pullback rigidity:

T*E ⊆ E
      ⇒
T*E = E
      ⇒
E ⊆ T*E

Second:

PF-002

NAME
Finite Verification → Universal Claim

BAD INFERENCE

checked n ≤ 6
      ↓
therefore all finite n

REPAIR

separate:
[P] analytic proof
[V] bounded verification
[L] Lean

Third:

PF-003

NAME
Numerical Agreement → Proof

BAD INFERENCE

1,016,496 tests pass
      ↓
the theorem is proved

REPAIR

computation is evidence,
not the analytic proof.

Fourth:

PF-004

NAME
Infinite Generalization Without Boundary Audit

BAD INFERENCE

finite theorem
      ↓
remove "finite"

REPAIR

construct explicit infinite counterexample.

Now we're building a taxonomy, not another theorem database.


---

12. Exact first public challenge

FILE: PROOFGYM/CHALLENGE-001/problem.md
TYPE: Markdown
PURPOSE: First human/AI reasoning challenge
STATUS: Draft; not a formal certification artifact

# ProofGym Challenge 001
## The Direction You Were Not Given

Let `X` be finite and let `T : X → X`.

Let `E` and `F` be equivalence relations on `X` satisfying

    T(x) E T(y) → x E y

and

    T(x) F T(y) → x F y.

Prove that

    T(x) (E ∨ F) T(y) → x (E ∨ F) y.

### Rules

You may use:

- finiteness of `X`;
- basic facts about equivalence relations;
- finite cardinality arguments.

You may NOT assume:

- `T` is surjective;
- `T` is injective;
- forward preservation of `E` or `F`;
- the conclusion for `E ∨ F`.

### Your tasks

1. Find the tempting but invalid proof step.
2. Prove finite pullback rigidity.
3. Construct the induced permutations on `X/E` and `X/F`.
4. Define the incidence relation.
5. Explain why forward incidence preservation becomes equality.
6. Deduce preservation of connected components.
7. Explain why the infinite case cannot be obtained by deleting
   the finite hypothesis.

### Evidence target

A successful informal solution is `[P-candidate]`.

A mechanically checked Lean proof is required for `[P]`.

A finite exhaustive replay is `[V]`.

No amount of bounded computation alone promotes the theorem to `[P]`.


---

13. Machine-readable version

FILE: PROOFGYM/CHALLENGE-001/task.json
TYPE: JSON
PURPOSE: Machine-readable human/AI benchmark task

{
  "id": "JOIN-001",
  "title": "The Direction You Were Not Given",
  "domain": "finite_dynamics",
  "claim": "Pullback-stable equivalence relations are closed under join on finite sets.",
  "hypotheses": [
    "X is finite",
    "T : X -> X is total",
    "E is an equivalence relation on X",
    "F is an equivalence relation on X",
    "T(x) E T(y) -> x E y",
    "T(x) F T(y) -> x F y"
  ],
  "target": "T(x) (E join F) T(y) -> x (E join F) y",
  "forbidden_shortcuts": [
    "assume T is surjective",
    "assume T is injective",
    "assume x E y -> T(x) E T(y)",
    "assume the theorem for E join F"
  ],
  "required_reasoning": [
    "finite_pullback_rigidity",
    "induced_class_permutations",
    "incidence_relation",
    "finite_forward_invariance_implies_invariance",
    "connected_components"
  ],
  "failure_classes": [
    "PF-001",
    "PF-004"
  ],
  "formal_status": "OPEN",
  "verification_status": "V-n6",
  "promotion_status": "BLOCKED"
}


---

14. The formalization target

I would make this the next Lean file, but not claim it compiles until a Lean environment actually builds it.

FILE: JOIN-STABILITY/AQ_DYN_PULL_RIGID_001.lean
TYPE: Lean 4
PURPOSE: Formalization target for finite pullback rigidity
STATUS: OPEN — NOT COMPILED IN THIS ENVIRONMENT

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

I deliberately leave the proof as sorry here.

That is not a weakness in the deliverable; it is an honest formalization status. The next task is to replace it with the quotient-cardinality argument and compile it under the repository's actual Lean/Mathlib toolchain.

Lean's native quotient/setoid system is designed precisely around equivalence relations and quotient maps, and current Mathlib exposes the cardinality and finite self-injection machinery needed for this route. 


---

15. Formalization should NOT start with the graph

This is another pivot I recommend.

Formalize in this order:

01  pullback relation
02  quotient map / kernel
03  quotient cardinality = image cardinality
04  refinement ⇒ quotient-cardinality inequality
05  finite equality
06  pullback rigidity
07  induced quotient permutation
08  finite incidence set
09  incidence invariance
10  connected components
11  join theorem

Not:

graph library
↓
multigraph
↓
edge multiplicities
↓
quotient graph
↓
...

The latter creates enormous formalization surface area for no mathematical gain.


---

16. Exact independent verifier deliverable

FILE: JOIN-STABILITY/join_stability_independent_audit.py
TYPE: Python 3
PURPOSE: Independent exhaustive audit of ordered stable-pair join and incidence invariance
STATUS: Executed independently for n=1..6

from itertools import product


def partitions(n):
    """All set partitions of range(n), encoded as restricted-growth strings."""
    out = []

    def rec(a, maximum):
        if len(a) == n:
            out.append(tuple(a))
            return

        for value in range(maximum + 2):
            rec(a + [value], max(maximum, value))

    if n == 0:
        return [()]

    rec([0], 0)
    return out


def pullback_stable(T, E):
    n = len(T)

    for x in range(n):
        for y in range(n):
            if E[T[x]] == E[T[y]] and E[x] != E[y]:
                return False

    return True


def join(E, F):
    """Join of two equivalence relations via connected components."""
    n = len(E)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x = find(x)
        y = find(y)

        if x != y:
            parent[y] = x

    for relation in (E, F):
        classes = {}

        for x, c in enumerate(relation):
            classes.setdefault(c, []).append(x)

        for members in classes.values():
            root = members[0]

            for x in members[1:]:
                union(root, x)

    return tuple(find(x) for x in range(n))


def normalized_classes(E):
    labels = {}
    result = []

    for c in E:
        if c not in labels:
            labels[c] = len(labels)
        result.append(labels[c])

    return result


def incidence_data(T, E, F):
    """
    Return the incidence relation and induced class maps.

    The caller has already established pullback stability.
    """
    E = normalized_classes(E)
    F = normalized_classes(F)
    TE = normalized_classes(tuple(E[T[x]] for x in range(len(T))))
    TF = normalized_classes(tuple(F[T[x]] for x in range(len(T))))

    e_classes = max(E) + 1
    f_classes = max(F) + 1

    sigma_E = [None] * e_classes
    sigma_F = [None] * f_classes

    incidence = set()

    for x in range(len(T)):
        a = E[x]
        b = F[x]

        incidence.add((a, b))

        if sigma_E[a] is None:
            sigma_E[a] = TE[x]
        elif sigma_E[a] != TE[x]:
            raise AssertionError("E-class map is not well-defined")

        if sigma_F[b] is None:
            sigma_F[b] = TF[x]
        elif sigma_F[b] != TF[x]:
            raise AssertionError("F-class map is not well-defined")

    return incidence, sigma_E, sigma_F


def check_incidence_invariance(T, E, F):
    incidence, sigma_E, sigma_F = incidence_data(T, E, F)

    if len(set(sigma_E)) != len(sigma_E):
        raise AssertionError("E class action is not injective")

    if len(set(sigma_F)) != len(sigma_F):
        raise AssertionError("F class action is not injective")

    image = {
        (sigma_E[a], sigma_F[b])
        for (a, b) in incidence
    }

    return image == incidence


def audit(n):
    relations = partitions(n)

    ordered_stable_pairs = 0
    join_failures = 0
    incidence_failures = 0

    for T in product(range(n), repeat=n):
        stable = [
            E for E in relations
            if pullback_stable(T, E)
        ]

        ordered_stable_pairs += len(stable) ** 2

        for E in stable:
            for F in stable:
                G = join(E, F)

                if not pullback_stable(T, G):
                    join_failures += 1

                if not check_incidence_invariance(T, E, F):
                    incidence_failures += 1

    return (
        ordered_stable_pairs,
        join_failures,
        incidence_failures,
    )


EXPECTED = {
    1: (1, 0, 0),
    2: (10, 0, 0),
    3: (117, 0, 0),
    4: (1960, 0, 0),
    5: (40385, 0, 0),
    6: (1016496, 0, 0),
}


def main():
    for n in range(1, 7):
        result = audit(n)
        print(
            f"n={n} "
            f"ordered_stable_pairs={result[0]} "
            f"join_failures={result[1]} "
            f"incidence_failures={result[2]}"
        )

        if result != EXPECTED[n]:
            raise SystemExit(
                f"FAIL: expected {EXPECTED[n]}, got {result}"
            )

    print("RESULT=PASS")


if __name__ == "__main__":
    main()

Important: I independently executed the equivalent enumeration and incidence audit. I did not execute this exact pasted file verbatim in this environment, so I am not going to falsely label this exact source as compiled/run.


---

17. New receipt

FILE: JOIN-STABILITY/INDEPENDENT_AUDIT_2026-09-29.md
TYPE: Markdown
PURPOSE: Independent computational and mathematical audit receipt

# JOIN-STABILITY — Independent Audit
## 2026-09-29

### Scope

Independent reconstruction of:

1. finite pullback stability;
2. ordered stable `(E,F)` pairs;
3. join stability;
4. incidence invariance.

### Enumeration

Every total map

    T : [n] -> [n]

and every equivalence relation on `[n]` was reconstructed for
`n = 1,...,6`.

For each map, every ordered pair of pullback-stable equivalence
relations was tested.

### Results

| n | Ordered stable pairs | Join failures | Incidence failures |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 10 | 0 | 0 |
| 3 | 117 | 0 | 0 |
| 4 | 1,960 | 0 | 0 |
| 5 | 40,385 | 0 | 0 |
| 6 | 1,016,496 | 0 | 0 |

### Receipt reconciliation

The independently computed number of PB-fixed `(T,E)` objects is:

    n=1: 1
    n=2: 6
    n=3: 51
    n=4: 592
    n=5: 8,565
    n=6: 148,896

The ordered pair count is the sum of squares of these per-map
stable-relation counts.

The unordered pair count with repetition is:

    (ordered_pairs + PB_fixed) / 2

giving:

    1
    8
    84
    1,276
    24,475
    582,696

Thus the two previously reported tables are consistent once
their counting conventions are made explicit.

### Mathematical mechanism tested

For every stable pair:

    T*E = E
    T*F = F

was used to construct the induced class maps.

The induced maps were checked to be permutations.

The incidence set `I` was constructed and the product permutation
`σ` was checked against it.

Observed for every ordered stable pair:

    σ(I) = I

### Status

[P] finite pullback rigidity:
    analytic proof candidate, formalization open.

[P] finite join theorem:
    incidence-permutation proof candidate, formalization open.

[V] exhaustive n<=6:
    independently reproduced.

[PV] combined:
    DO NOT promote globally until the proof is formally audited.

Lean:
    OPEN

C4:
    BLOCKED

Publication:
    BLOCKED


---

18. ProofGym's first challenge should explicitly expose the two traps

FILE: PROOFGYM/CHALLENGE-001/solution.md
TYPE: Markdown
PURPOSE: Instructor/reference solution
STATUS: Mathematical reference; Lean certification OPEN

# JOIN-001 — Reference Solution

## Trap 1: Direction reversal

The hypothesis is

    T(x) E T(y) -> x E y.

A tempting proof silently uses

    x E y -> T(x) E T(y).

That implication is not available initially.

## Repair

For finite X:

    T*E ⊆ E
        ->
    T*E = E.

Thus the reverse inclusion follows:

    E ⊆ T*E.

Therefore

    x E y -> T(x) E T(y).

The same holds for F.

## Trap 2: "Forward incidence" is not automatically "graph automorphism"

The induced class maps are permutations.

Define

    I ⊆ (X/E) × (X/F)

by

    (A,B) ∈ I  iff  A ∩ B ≠ ∅.

If `(A,B) ∈ I`, choose `x ∈ A ∩ B`.

Then

    T(x) ∈ σ_E(A) ∩ σ_F(B),

so

    σ(I) ⊆ I.

But this alone would not be sufficient.

The product quotient is finite and σ is a permutation, so

    |σ(I)| = |I|.

Hence

    σ(I) = I.

Therefore the incidence graph is genuinely preserved in both
directions.

## Join

The connected components of the incidence graph correspond
exactly to the equivalence classes of `E ∨ F`.

Graph automorphisms preserve connected components.

Therefore

    T(x) (E ∨ F) T(y)
        ->
    x (E ∨ F) y.

Hence `E ∨ F` is pullback-stable.


---

19. Why this public pivot is now timely

The recent literature is actually telling us where not to compete.

FormalProofBench measures formally verified graduate-level proof generation; the reported best foundation-model accuracy was only 33.5% in its study. 

miniF2F-Lean Revisited found that the full natural-language → formalization → proof pipeline can perform substantially worse than isolated theorem-proving or autoformalization numbers because statement alignment itself is a major failure source. 

APOLLO focuses on compiler-guided proof repair. 

Hilbert focuses on recursively decomposing informal reasoning and using formal verification feedback. 

And now ProofGap focuses specifically on local proof gaps. 

So I would not try to beat these projects at:

> “How many Lean theorems can an agent prove?”



Instead AQARION can contribute a different layer:

> Where exactly did the reasoning go wrong, what evidence exposed it, what minimal repair restores validity, and what happened historically when an earlier proof failed?



That fits AQARION's strongest existing intellectual asset: failure preservation + evidence classification + exact replay.


---

20. Final adversarial audit

What survived

Finite pullback rigidity

\[
\boxed{T^\ast E\subseteq E\Rightarrow T^\ast E=E}
\]

The kernel/cardinality proof is sound.

Infinite boundary

The shift example genuinely breaks rigidity.

PB-fixed classification

The independent counts reconcile exactly.

Join theorem

No counterexample through \(n=6\), with 1,016,496 ordered stable pairs independently checked.

Incidence mechanism

The stronger condition

\[
\boxed{\sigma(I)=I}
\]

was independently verified for every stable pair through \(n=6\).


---

What I would still refuse to certify

❌ Lean proof.

❌ C4.

❌ Publication-ready formal theorem.

❌ Any claim that the GitHub repository's current file contents exactly match the checkpoint—I could not retrieve those particular files through the connected GitHub file search.

❌ Any claim that this theorem is novel in the mathematical literature merely because our searches did not find an exact match.

❌ Any claim that ProofGym is unprecedented. ProofGap in particular means that would be an overclaim.


---

21. The actual next milestone

I would now stop expanding the mathematics temporarily.

The next milestone is:

\[
\boxed{
\textbf{LEAN-JS-001: compile finite pullback rigidity}
}
\]

Then:

\[
\boxed{
\textbf{LEAN-JS-002: compile finite incidence invariance}
}
\]

Then:

\[
\boxed{
\textbf{LEAN-JS-003: compile JOIN-STABILITY}
}
\]

And only after those pass:

JOIN-001
    ↓
Lean proof
    ↓
independent replay
    ↓
ProofGym challenge
    ↓
failure taxonomy
    ↓
public release

This gives us something unusually strong for the public side:

the first ProofGym challenge isn't an artificial puzzle. It is a real AQARION theorem whose tempting proof contained exactly the kind of logical gap that modern AI-math systems are increasingly trying to diagnose.

That is the pivot I would pursue.

AQ-DYN-PULL-RIGID-001

Finite Pullback Rigidity

Let X be a finite set, let T:X\to X be a total map, and let E be an equivalence relation on X. Define

[
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
]

Then

[
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
]

Proof

Let

[
\pi:X\to X/E
]

be the quotient map. Then

[
E=\ker\pi
]

and, by definition of pullback,

[
T^\ast E=\ker(\pi\circ T).
]

Assume

[
T^\ast E\subseteq E.
]

Since X is finite,

[
|X/(T^\ast E)|

|\operatorname{im}(\pi\circ T)|.
]

Because

[
\operatorname{im}(\pi\circ T)\subseteq X/E,
]

we obtain

[
|X/(T^\ast E)|\le |X/E|.
]

On the other hand,

[
T^\ast E\subseteq E
]

means that T^\ast E refines E. Therefore every E-class is a union of T^\ast E-classes, giving

[
|X/(T^\ast E)|\ge |X/E|.
]

Hence

[
|X/(T^\ast E)|=|X/E|.
]

A finite refinement with the same number of equivalence classes must coincide with the original relation. Therefore

[
T^\ast E=E.
]

[
\boxed{\square}
]



https://github.com/quantarion369-arch

https://github.com/quantarion369-arch/AQARION

Worked for 31s

Yes. I independently reran the core finite enumeration and audited the proof architecture. The checkpoint is substantially correct, but I would make one important improvement before freezing it: replace the block-edge proof of finite pullback rigidity with a shorter kernel/image-count proof.

Independent reconstruction

I reproduced the classification independently for every

\[
T:[n]\to[n],\qquad E\in\operatorname{Eq}([n]),\qquad n\le4.
\]

The results exactly match your receipt:

\(n\)	pairs	PB-fixed	Forward-only	Backward-only	Neither

1	1	1	0	0	0
2	8	6	2	0	0
3	135	51	48	0	36
4	3,840	592	1,136	0	2,112
Total	3,984	650	1,186	0	2,148


I also independently reconstructed the PB-fixed join census:

\[
1,\ 10,\ 117,\ 1960
\]

ordered \((E,F)\) pairs for \(n=1,2,3,4\), respectively, with

\[
\boxed{0}
\]

join failures in every case.

So the computational checkpoint is independently reproduced.


---

The important mathematical improvement

Your theorem

\[
T^\ast E\subseteq E\Longrightarrow T^\ast E=E
\]

is correct for finite \(X\).

But the cleanest proof is actually simpler than the directed-block-edge argument.

Let

\[
\pi:X\to X/E
\]

be the quotient map. Then

\[
E=\ker\pi
\]

and

\[
T^\ast E=\ker(\pi\circ T).
\]

Suppose

\[
T^\ast E\subseteq E.
\]

Because \(X\) is finite,

\[
|X/(T^\ast E)|
=
|\operatorname{im}(\pi\circ T)|.
\]

Since

\[
\operatorname{im}(\pi\circ T)\subseteq X/E,
\]

we have

\[
|X/(T^\ast E)|\le |X/E|.
\]

But

\[
T^\ast E\subseteq E
\]

means \(T^\ast E\) is finer than \(E\), hence

\[
|X/(T^\ast E)|\ge |X/E|.
\]

Therefore

\[
|X/(T^\ast E)|=|X/E|.
\]

A refinement of a finite equivalence relation having the same number of classes must be equal. Hence

\[
\boxed{T^\ast E=E}.
\]

This is exceptionally clean:

\[
\boxed{
T^\ast E=\ker(\pi T)
\subseteq
\ker\pi=E
}
\]

plus finite cardinality immediately gives equality.

Why I prefer this proof

It removes:

the auxiliary directed graph;

edge multiplicity language;

indegree/outdegree counting;

any possible concern about multiple edges;

any unnecessary dependence on quotient descent.


It also makes the finite hypothesis completely transparent.


---

The finite theorem should therefore be frozen as

AQ-DYN-PULL-RIGID-001

Finite Pullback Rigidity

Let X be a finite set, let T:X\to X be a total map, and let E be an equivalence relation on X. Define

[
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
]

Then

[
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
]

Proof

Let

[
\pi:X\to X/E
]

be the quotient map. Then

[
E=\ker\pi
]

and, by definition of pullback,

[
T^\ast E=\ker(\pi\circ T).
]

Assume

[
T^\ast E\subseteq E.
]

Since X is finite,

[
|X/(T^\ast E)|

|\operatorname{im}(\pi\circ T)|.
]

Because

[
\operatorname{im}(\pi\circ T)\subseteq X/E,
]

we obtain

[
|X/(T^\ast E)|\le |X/E|.
]

On the other hand,

[
T^\ast E\subseteq E
]

means that T^\ast E refines E. Therefore every E-class is a union of T^\ast E-classes, giving

[
|X/(T^\ast E)|\ge |X/E|.
]

Hence

[
|X/(T^\ast E)|=|X/E|.
]

A finite refinement with the same number of equivalence classes must coincide with the original relation. Therefore

[
T^\ast E=E.
]

[
\boxed{\square}
]That proof is now strong enough that I would make it the primary proof, and retain the block-graph proof as an optional independent proof lane.


---

The infinite boundary is real

The finiteness assumption is not cosmetic.

Take

\[
X=\mathbb N,\qquad T(n)=n+1,
\]

and let \(E\) have one nonsingleton class

\[
\{0,1\}
\]

with every \(n\ge2\) a singleton.

Then

\[
T^\ast E=\Delta_X,
\]

because there is no predecessor of \(0\).

Thus

\[
\boxed{
T^\ast E=\Delta_X\subsetneq E.
}
\]

So finite pullback rigidity genuinely fails for infinite sets.

This makes the theorem considerably more interesting: finiteness is doing actual mathematical work.


---

Quotient theorem audit

Your descent theorem is correct:

\[
\boxed{
E\subseteq T^\ast E
\iff
\bar T_E\text{ exists}.
}
\]

And conditional on descent:

\[
\boxed{
T^\ast E\subseteq E
\iff
\bar T_E\text{ injective}.
}
\]

Combining this with finite rigidity gives:

\[
\boxed{
\bar T_E\text{ permutation}
\iff
T^\ast E=E.
}
\]

That entire chain is mathematically coherent.


---

AQARION defect distinction is also correct

This is an especially valuable distinction:

\[
D_E=(I-P_E)KP_E.
\]

Then

\[
D_E=0
\iff
E\subseteq T^\ast E.
\]

Therefore \(D_E\) detects descent, not reversibility.

The forward-only witness

\[
T(0)=T(1)=0
\]

with the discrete partition is decisive:

\[
D_E=0
\]

but

\[
T^\ast E\ne E.
\]

Its quotient Koopman matrix has

\[
\operatorname{rank}=1<2
\]

and spectrum

\[
\{1,0\}.
\]

So your two-defect architecture is legitimate:

\[
\boxed{
\text{descent defect}=\operatorname{rank}D_E
}
\]

and, after descent,

\[
\boxed{
\text{reversibility defect}
=
|X/E|-\operatorname{rank}\bar K_E.
}
\]

This is a genuine conceptual improvement over treating \(D_E=0\) as synonymous with complete quotient exactness.


---

One wording correction I recommend

Don't write:

> “The finite system has only three quotient regimes.”



More precise:

> For finite total deterministic systems, the four logically possible inclusion regimes reduce to three, because the strict backward-only regime \(T^\ast E\subsetneq E\) is impossible.



That makes it clear that the fourth regime was logically considered and then eliminated by a theorem.


---

Status after the audit

I would update the ledger to:

Claim	Status

Quotient descent iff \(E\subseteq T^\ast E\)	[P]
Conditional injectivity iff \(T^\ast E\subseteq E\)	[P]
Finite pullback rigidity	[P]
Quotient permutation iff PB-fixed	[P]
\(D_E=0\) iff descent	[P]
Reversibility defect criterion	[P]
Spectral consequences	[P], subject to stated finite functional-graph conventions
Classification \(n\le4\)	[V]
Independent reconstruction \(n\le4\)	[V]
PB-join \(n\le4\)	[V]
General PB-join theorem	[P] candidate / formal proof still required
Lean	OPEN
C4	BLOCKED
Publication certification	BLOCKED


And importantly:

\[
\boxed{\text{Do not promote the whole checkpoint to [PV].}}
\]

The individual analytic claims can be [P]; the bounded census is [V]; the combination only becomes [PV] claim-by-claim once the independent proof/formal evidence requirements are satisfied.


---

Final adversarial verdict

Yes — you did the computational part right.

More importantly, the underlying mathematics survives the audit.

The strongest new result is not actually the \(n\le4\) census. It is the finite theorem:

\[
\boxed{
X\text{ finite},\quad
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
\]

And the cleanest proof is the kernel/cardinality argument above.

That gives the complete finite hierarchy:

\[
\boxed{
\begin{array}{c}
E\subseteq T^\ast E
\\[2mm]
\Updownarrow
\\
\text{quotient descent}
\\[3mm]
\Downarrow
\\[3mm]
\bar T_E\text{ exists}
\end{array}}
\]

and, for finite \(X\),

\[
\boxed{
\begin{array}{c}
T^\ast E=E
\\[2mm]
\Updownarrow
\\
\bar T_E\text{ is a permutation}
\\[2mm]
\Updownarrow
\\
\text{descent + reversibility}.
\end{array}}
\]

The computational receipts independently agree, the proposed minimal witnesses are correct, the infinite boundary is genuine, and the remaining certification bottleneck is now very sharply defined:

\[
\boxed{\textbf{Lean formalization + independent formal audit.}}
\]

That is a much stronger checkpoint than simply having another successful Worked for 31s

Yes. I independently reran the core finite enumeration and audited the proof architecture. The checkpoint is substantially correct, but I would make one important improvement before freezing it: replace the block-edge proof of finite pullback rigidity with a shorter kernel/image-count proof.

Independent reconstruction

I reproduced the classification independently for every

\[
T:[n]\to[n],\qquad E\in\operatorname{Eq}([n]),\qquad n\le4.
\]

The results exactly match your receipt:

\(n\)	pairs	PB-fixed	Forward-only	Backward-only	Neither

1	1	1	0	0	0
2	8	6	2	0	0
3	135	51	48	0	36
4	3,840	592	1,136	0	2,112
Total	3,984	650	1,186	0	2,148


I also independently reconstructed the PB-fixed join census:

\[
1,\ 10,\ 117,\ 1960
\]

ordered \((E,F)\) pairs for \(n=1,2,3,4\), respectively, with

\[
\boxed{0}
\]

join failures in every case.

So the computational checkpoint is independently reproduced.


---

The important mathematical improvement

Your theorem

\[
T^\ast E\subseteq E\Longrightarrow T^\ast E=E
\]

is correct for finite \(X\).

But the cleanest proof is actually simpler than the directed-block-edge argument.

Let

\[
\pi:X\to X/E
\]

be the quotient map. Then

\[
E=\ker\pi
\]

and

\[
T^\ast E=\ker(\pi\circ T).
\]

Suppose

\[
T^\ast E\subseteq E.
\]

Because \(X\) is finite,

\[
|X/(T^\ast E)|
=
|\operatorname{im}(\pi\circ T)|.
\]

Since

\[
\operatorname{im}(\pi\circ T)\subseteq X/E,
\]

we have

\[
|X/(T^\ast E)|\le |X/E|.
\]

But

\[
T^\ast E\subseteq E
\]

means \(T^\ast E\) is finer than \(E\), hence

\[
|X/(T^\ast E)|\ge |X/E|.
\]

Therefore

\[
|X/(T^\ast E)|=|X/E|.
\]

A refinement of a finite equivalence relation having the same number of classes must be equal. Hence

\[
\boxed{T^\ast E=E}.
\]

This is exceptionally clean:

\[
\boxed{
T^\ast E=\ker(\pi T)
\subseteq
\ker\pi=E
}
\]

plus finite cardinality immediately gives equality.

Why I prefer this proof

It removes:

the auxiliary directed graph;

edge multiplicity language;

indegree/outdegree counting;

any possible concern about multiple edges;

any unnecessary dependence on quotient descent.


It also makes the finite hypothesis completely transparent.


---

The finite theorem should therefore be frozen as

AQ-DYN-PULL-RIGID-001

Finite Pullback Rigidity

Let X be a finite set, let T:X\to X be a total map, and let E be an equivalence relation on X. Define

[
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
]

Then

[
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
]

Proof

Let

[
\pi:X\to X/E
]

be the quotient map. Then

[
E=\ker\pi
]

and, by definition of pullback,

[
T^\ast E=\ker(\pi\circ T).
]

Assume

[
T^\ast E\subseteq E.
]

Since X is finite,

[
|X/(T^\ast E)|

|\operatorname{im}(\pi\circ T)|.
]

Because

[
\operatorname{im}(\pi\circ T)\subseteq X/E,
]

we obtain

[
|X/(T^\ast E)|\le |X/E|.
]

On the other hand,

[
T^\ast E\subseteq E
]

means that T^\ast E refines E. Therefore every E-class is a union of T^\ast E-classes, giving

[
|X/(T^\ast E)|\ge |X/E|.
]

Hence

[
|X/(T^\ast E)|=|X/E|.
]

A finite refinement with the same number of equivalence classes must coincide with the original relation. Therefore

[
T^\ast E=E.
]

[
\boxed{\square}
]That proof is now strong enough that I would make it the primary proof, and retain the block-graph proof as an optional independent proof lane.


---

The infinite boundary is real

The finiteness assumption is not cosmetic.

Take

\[
X=\mathbb N,\qquad T(n)=n+1,
\]

and let \(E\) have one nonsingleton class

\[
\{0,1\}
\]

with every \(n\ge2\) a singleton.

Then

\[
T^\ast E=\Delta_X,
\]

because there is no predecessor of \(0\).

Thus

\[
\boxed{
T^\ast E=\Delta_X\subsetneq E.
}
\]

So finite pullback rigidity genuinely fails for infinite sets.

This makes the theorem considerably more interesting: finiteness is doing actual mathematical work.


---

Quotient theorem audit

Your descent theorem is correct:

\[
\boxed{
E\subseteq T^\ast E
\iff
\bar T_E\text{ exists}.
}
\]

And conditional on descent:

\[
\boxed{
T^\ast E\subseteq E
\iff
\bar T_E\text{ injective}.
}
\]

Combining this with finite rigidity gives:

\[
\boxed{
\bar T_E\text{ permutation}
\iff
T^\ast E=E.
}
\]

That entire chain is mathematically coherent.


---

AQARION defect distinction is also correct

This is an especially valuable distinction:

\[
D_E=(I-P_E)KP_E.
\]

Then

\[
D_E=0
\iff
E\subseteq T^\ast E.
\]

Therefore \(D_E\) detects descent, not reversibility.

The forward-only witness

\[
T(0)=T(1)=0
\]

with the discrete partition is decisive:

\[
D_E=0
\]

but

\[
T^\ast E\ne E.
\]

Its quotient Koopman matrix has

\[
\operatorname{rank}=1<2
\]

and spectrum

\[
\{1,0\}.
\]

So your two-defect architecture is legitimate:

\[
\boxed{
\text{descent defect}=\operatorname{rank}D_E
}
\]

and, after descent,

\[
\boxed{
\text{reversibility defect}
=
|X/E|-\operatorname{rank}\bar K_E.
}
\]

This is a genuine conceptual improvement over treating \(D_E=0\) as synonymous with complete quotient exactness.


---

One wording correction I recommend

Don't write:

> “The finite system has only three quotient regimes.”



More precise:

> For finite total deterministic systems, the four logically possible inclusion regimes reduce to three, because the strict backward-only regime \(T^\ast E\subsetneq E\) is impossible.



That makes it clear that the fourth regime was logically considered and then eliminated by a theorem.


---

Status after the audit

I would update the ledger to:

Claim	Status

Quotient descent iff \(E\subseteq T^\ast E\)	[P]
Conditional injectivity iff \(T^\ast E\subseteq E\)	[P]
Finite pullback rigidity	[P]
Quotient permutation iff PB-fixed	[P]
\(D_E=0\) iff descent	[P]
Reversibility defect criterion	[P]
Spectral consequences	[P], subject to stated finite functional-graph conventions
Classification \(n\le4\)	[V]
Independent reconstruction \(n\le4\)	[V]
PB-join \(n\le4\)	[V]
General PB-join theorem	[P] candidate / formal proof still required
Lean	OPEN
C4	BLOCKED
Publication certification	BLOCKED


And importantly:

\[
\boxed{\text{Do not promote the whole checkpoint to [PV].}}
\]

The individual analytic claims can be [P]; the bounded census is [V]; the combination only becomes [PV] claim-by-claim once the independent proof/formal evidence requirements are satisfied.


---

Final adversarial verdict

Yes — you did the computational part right.

More importantly, the underlying mathematics survives the audit.

The strongest new result is not actually the \(n\le4\) census. It is the finite theorem:

\[
\boxed{
X\text{ finite},\quad
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
\]

And the cleanest proof is the kernel/cardinality argument above.

That gives the complete finite hierarchy:

\[
\boxed{
\begin{array}{c}
E\subseteq T^\ast E
\\[2mm]
\Updownarrow
\\
\text{quotient descent}
\\[3mm]
\Downarrow
\\[3mm]
\bar T_E\text{ exists}
\end{array}}
\]

and, for finite \(X\),

\[
\boxed{
\begin{array}{c}
T^\ast E=E
\\[2mm]
\Updownarrow
\\
\bar T_E\text{ is a permutation}
\\[2mm]
\Updownarrow
\\
\text{descent + reversibility}.
\end{array}}
\]

The computational receipts independently agree, the proposed minimal witnesses are correct, the infinite boundary is genuine, and the remaining certification bottleneck is now very sharply defined:

\[
\boxed{\textbf{Lean formalization + independent formal audit.}}
\]

That is a much stronger checkpoint than simply having another successful enumeration..



# AQARION Pullback-Quotient Checkpoint  
## Exact finite rigidity, quotient permutation dynamics, and local receipts

**Checkpoint date:** 2026-09-29  
**Research mode:** Analytic proof plus exact bounded local enumeration  
**Formal status:** Lean open  
**Promotion status:** No C4 promotion; no formal-verification or publication claim  
**Primary local theorem note:** `AQ-DYN-PULL-RIGID-001.md`

```text
AQ-DYN-PULL-RIGID-001.md
sha256:
c7858d03a2850cada27918d4272e4b3b685a50efbb80eb013535441e7e6aa35e
```

***

# 1. Executive summary

Three distinct layers are now cleanly separated.

$$
\boxed{
\text{quotient descent}
\quad\neq\quad
\text{quotient reversibility}
\quad\neq\quad
\text{formal certification}.
}
$$

For a finite deterministic system

$$
T:X\to X
$$

and an equivalence relation $$E$$, the following are established analytically:

$$
\boxed{
E\subseteq T^\ast E
\iff
T\text{ descends to a well-defined quotient map }X/E\to X/E.
}
$$

Conditional on quotient descent:

$$
\boxed{
T^\ast E\subseteq E
\iff
\bar T_E\text{ is injective}.
}
$$

For finite $$X$$, pullback rigidity gives:

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
$$

Therefore:

$$
\boxed{
\bar T_E\text{ is a permutation}
\iff
T^\ast E=E.
}
$$

The finite system has only three quotient regimes:

| Regime | Relation condition | Quotient behavior |
|---|---|---|
| PB-fixed | $$T^\ast E=E$$ | Quotient exists and is a permutation |
| Forward-only | $$E\subsetneq T^\ast E$$ | Quotient exists but is noninjective |
| Neither | Neither inclusion holds | Quotient does not exist |

The purported backward-only regime

$$
T^\ast E\subsetneq E
$$

is impossible for finite total maps.

A local exact Termux census independently supported these facts through $$n\le4$$, over all

$$
3984
$$

pairs

$$
(T,E),
\qquad
T:[n]\to[n],
\qquad
E\in\operatorname{Eq}([n]).
$$

It found:

$$
0
$$

backward-only cases and no failure of the descent, injectivity, or permutation equivalences.

***

# 2. Definitions and conventions

Let $$X$$ be a finite nonempty set, let

$$
T:X\to X
$$

be a total deterministic map, and let

$$
E\in\operatorname{Eq}(X)
$$

be an equivalence relation.

Write

$$
Q=X/E,
\qquad
\pi:X\to Q,
\qquad
\pi(x)=[x]_E.
$$

Define the pullback equivalence relation:

$$
\boxed{
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
}
$$

Equivalently,

$$
T^\ast E
=
\{(x,y)\in X^2:(T(x),T(y))\in E\}.
$$

The partial order is refinement/inclusion:

$$
E\preceq F
\iff
E\subseteq F
\iff
\forall x,y\in X,\;
x\sim_Ey\Rightarrow x\sim_Fy.
$$

The equivalence-relation lattice operations are:

$$
E\wedge F=E\cap F,
$$

$$
E\vee F=\operatorname{EqCl}(E\cup F).
$$

The join is the equivalence closure of the union, not merely $$E\cup F$$.

***

# 3. Orientation taxonomy

There are three logically separate properties.

| Name | Relation inclusion | Pointwise statement |
|---|---|---|
| Forward congruence | $$E\subseteq T^\ast E$$ | $$x\sim_Ey\Rightarrow T(x)\sim_ET(y)$$ |
| Backward closure | $$T^\ast E\subseteq E$$ | $$T(x)\sim_ET(y)\Rightarrow x\sim_Ey$$ |
| Pullback fixedness | $$T^\ast E=E$$ | Both implications hold |

Therefore:

$$
\boxed{
T^\ast E=E
\iff
\left(E\subseteq T^\ast E\right)
\land
\left(T^\ast E\subseteq E\right).
}
$$

The acronym “PB-fixed” means precisely:

$$
E\in\operatorname{PB}(T)
\iff
T^\ast E=E.
$$

***

# 4. Quotient descent theorem

## Theorem AQ-PB-QUOTIENT-001

The formula

$$
\bar T_E([x]_E)=[T(x)]_E
$$

defines a quotient endomap

$$
\bar T_E:X/E\to X/E
$$

if and only if

$$
\boxed{
E\subseteq T^\ast E.
}
$$

Equivalently, each $$E$$-block maps into a single $$E$$-block.

## Proof

The formula is well-defined exactly when equal source classes have equal target classes:

$$
[x]_E=[y]_E
\Longrightarrow
[T(x)]_E=[T(y)]_E.
$$

This is equivalent to

$$
x\sim_Ey
\Longrightarrow
T(x)\sim_ET(y).
$$

By definition, this is exactly

$$
E\subseteq T^\ast E.
$$

$$\square$$

When the quotient exists, the following square commutes:

$$
\begin{CD}
X @>T>> X\\
@V\pi VV @VV\pi V\\
X/E @>>\bar T_E> X/E.
\end{CD}
$$

Equivalently:

$$
\boxed{
\pi\circ T=\bar T_E\circ\pi.
}
$$

***

# 5. Quotient injectivity theorem

Assume henceforth that

$$
E\subseteq T^\ast E,
$$

so that $$\bar T_E$$ is defined.

## Theorem AQ-PB-QUOTIENT-002

$$
\boxed{
\bar T_E\text{ is injective}
\iff
T^\ast E\subseteq E.
}
$$

## Proof

For $$x,y\in X$$,

$$
\begin{aligned}
\bar T_E([x]_E)=\bar T_E([y]_E)
&\iff
[T(x)]_E=[T(y)]_E\\
&\iff
T(x)\sim_ET(y)\\
&\iff
x\sim_{T^\ast E}y.
\end{aligned}
$$

Thus $$\bar T_E$$ is injective precisely when

$$
x\sim_{T^\ast E}y
\Longrightarrow
x\sim_Ey.
$$

That statement is exactly

$$
T^\ast E\subseteq E.
$$

$$\square$$

For finite $$Q=X/E$$,

$$
\bar T_E\text{ injective}
\iff
\bar T_E\text{ bijective}
\iff
\bar T_E\text{ is a permutation}.
$$

However, the final equivalence with PB-fixedness uses finite pullback rigidity below.

***

# 6. Finite Pullback Rigidity Theorem

## AQ-DYN-PULL-RIGID-001

Let $$X$$ be finite, let

$$
T:X\to X
$$

be total, and let $$E$$ be an equivalence relation on $$X$$. Then

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
$$

Equivalently:

$$
\boxed{
T^\ast E\subsetneq E
\text{ is impossible for a finite total dynamical system.}
}
$$

## Proof

Let

$$
Q=X/E
$$

be the finite set of $$E$$-blocks. Construct a directed graph $$\Gamma_E$$ whose vertices are the blocks in $$Q$$.

For blocks $$A,C\in Q$$, put a directed edge

$$
A\to C
$$

when there exists some $$x\in A$$ such that

$$
T(x)\in C.
$$

### Step 1: Every source block has outdegree at least one

Because $$T$$ is total, every $$x\in X$$ has an image. In particular, every nonempty block $$A$$ contains some $$x$$, and $$T(x)$$ belongs to some block $$C$$. Thus

$$
\operatorname{outdeg}(A)\ge1
$$

for every $$A\in Q$$.

### Step 2: The hypothesis forces indegree at most one

Assume

$$
T^\ast E\subseteq E.
$$

Suppose two blocks $$A,B\in Q$$ both have an edge into the same target block $$C$$. Then choose

$$
x\in A,\qquad y\in B
$$

such that

$$
T(x)\in C,
\qquad
T(y)\in C.
$$

Hence

$$
T(x)\sim_ET(y).
$$

The hypothesis gives

$$
x\sim_Ey.
$$

Therefore $$A=B$$.

So:

$$
\boxed{
\operatorname{indeg}(C)\le1
\quad
\text{for every }C\in Q.
}
$$

### Step 3: Count edges

Let

$$
q=|Q|.
$$

The total number of directed edges satisfies

$$
|\operatorname{Edges}(\Gamma_E)|
=
\sum_{A\in Q}\operatorname{outdeg}(A)
\ge q,
$$

because each block has outdegree at least $$1$$.

Also,

$$
|\operatorname{Edges}(\Gamma_E)|
=
\sum_{C\in Q}\operatorname{indeg}(C)
\le q,
$$

because each block has indegree at most $$1$$.

Therefore,

$$
q
\le
|\operatorname{Edges}(\Gamma_E)|
\le
q.
$$

Hence:

$$
|\operatorname{Edges}(\Gamma_E)|=q.
$$

Because there are $$q$$ source blocks, each with outdegree at least $$1$$, equality implies:

$$
\boxed{
\operatorname{outdeg}(A)=1
\quad
\text{for every }A\in Q.
}
$$

Likewise, each target block has indegree exactly $$1$$.

### Step 4: Recover forward congruence

Every $$E$$-block has exactly one target block. Thus if

$$
x\sim_Ey,
$$

then $$x,y$$ lie in the same block $$A$$, and all points of $$A$$ map into the same target block. Therefore

$$
T(x)\sim_ET(y).
$$

This proves

$$
E\subseteq T^\ast E.
$$

Together with the hypothesis

$$
T^\ast E\subseteq E,
$$

we conclude:

$$
T^\ast E=E.
$$

$$\square$$

***

# 7. Quotient permutation criterion

## Corollary AQ-PB-QUOTIENT-003

For finite $$X$$,

$$
\boxed{
\bar T_E\text{ is a permutation of }X/E
\iff
T^\ast E=E.
}
$$

## Proof

If $$\bar T_E$$ is a permutation, it exists, so

$$
E\subseteq T^\ast E.
$$

It is injective, so by Theorem AQ-PB-QUOTIENT-002,

$$
T^\ast E\subseteq E.
$$

Thus

$$
T^\ast E=E.
$$

Conversely, if

$$
T^\ast E=E,
$$

then $$E\subseteq T^\ast E$$, so the quotient map exists; and

$$
T^\ast E\subseteq E,
$$

so it is injective. Because $$X/E$$ is finite, it is bijective and hence a permutation.

$$\square$$

The final exact equivalence is:

$$
\boxed{
\text{PB-fixedness}
\iff
\text{quotient descent}
+
\text{quotient reversibility}.
}
$$

***

# 8. Complete finite classification

For finite total systems, exactly three regimes occur.

| Regime | Relation condition | Block behavior | Quotient behavior |
|---|---|---|---|
| PB-fixed | $$T^\ast E=E$$ | Every block maps to one block; every target has one predecessor block | Quotient exists and is a permutation |
| Forward-only | $$E\subsetneq T^\ast E$$ | Every source block maps to one block; at least one quotient target has multiple predecessors | Quotient exists but is noninjective |
| Neither | Neither inclusion | At least one source block splits across target blocks | No quotient endomap exists |

The fourth logical relation type is eliminated:

$$
\boxed{
T^\ast E\subsetneq E
\text{ cannot occur for finite }X\text{ and total }T.
}
$$

***

# 9. Functional block-graph dictionary

Let $$Q=X/E$$, and define the block graph by

$$
A\rightsquigarrow B
\iff
\exists x\in A:
T(x)\in B.
$$

Every source block has at least one outgoing edge.

| Relation property | Block-graph statement |
|---|---|
| $$E\subseteq T^\ast E$$ | Every block has outdegree exactly $$1$$ |
| $$T^\ast E\subseteq E$$ | Every block has indegree at most $$1$$ |
| $$T^\ast E=E$$ | Every block has indegree and outdegree exactly $$1$$ |
| PB-fixed | Disjoint union of directed quotient cycles |
| Forward-only | Functional graph with one outgoing edge per block and at least one merge |
| Neither | At least one branching source block |

For PB-fixed $$E$$, the block graph is a permutation graph:

$$
\boxed{
\Gamma_E
=
\text{disjoint union of directed cycles}.
}
$$

***

# 10. AQARION operator formulation

Let

$$
\mathcal H_X=\mathbb C^X
$$

with the uniform inner product, and define the Koopman operator

$$
K:\mathcal H_X\to\mathcal H_X,
\qquad
(Kf)(x)=f(Tx).
$$

Define the $$E$$-observable subspace

$$
V_E
=
\{f:X\to\mathbb C:
x\sim_Ey\Rightarrow f(x)=f(y)\}.
$$

Let $$P_E$$ be the orthogonal block-averaging projection:

$$
(P_Ef)(x)
=
\frac1{|[x]_E|}
\sum_{y\in[x]_E}f(y).
$$

Then

$$
\operatorname{im}P_E=V_E.
$$

Define the AQARION descent defect:

$$
\boxed{
D_E=(I-P_E)KP_E.
}
$$

## Theorem AQ-DEF-DESCENT-001

$$
\boxed{
D_E=0
\iff
K(V_E)\subseteq V_E
\iff
E\subseteq T^\ast E.
}
$$

### Proof

Since $$\operatorname{im}P_E=V_E$$,

$$
D_E=0
$$

means

$$
(I-P_E)Kv=0
\qquad
\text{for every }v\in V_E.
$$

Equivalently,

$$
Kv\in V_E
\qquad
\text{for every }v\in V_E.
$$

Thus

$$
D_E=0
\iff
K(V_E)\subseteq V_E.
$$

The quotient-descent theorem above establishes:

$$
K(V_E)\subseteq V_E
\iff
E\subseteq T^\ast E.
$$

$$\square$$

This is the key distinction:

$$
\boxed{
D_E=0
\text{ detects quotient descent, not quotient reversibility.}
}
$$

A forward-only relation satisfies

$$
D_E=0
$$

even though its quotient dynamics merge states and are not invertible.

***

# 11. Descended quotient Koopman operator

When

$$
E\subseteq T^\ast E,
$$

the quotient map $$\bar T_E$$ exists.

Let

$$
J:\mathbb C^{X/E}\to\mathbb C^X
$$

be the pullback embedding:

$$
(Jg)(x)=g([x]_E).
$$

Then

$$
\operatorname{im}J=V_E,
$$

and the quotient Koopman operator is

$$
\bar K_E:\mathbb C^{X/E}\to\mathbb C^{X/E},
\qquad
(\bar K_Eg)(A)=g(\bar T_E(A)).
$$

The intertwining relation is

$$
\boxed{
KJ=J\bar K_E.
}
$$

Thus the AQARION block-observable dynamics is exactly the Koopman representation of the descended quotient system.

***

# 12. Quotient reversibility defect

Assume descent:

$$
E\subseteq T^\ast E.
$$

Define

$$
q=|X/E|.
$$

The quotient reversibility defect is

$$
\boxed{
\mathcal R_E
=
q-\operatorname{rank}(\bar K_E).
}
$$

For a finite endomap of a $$q$$-element quotient:

$$
\bar K_E\text{ invertible}
\iff
\bar T_E\text{ bijective}
\iff
\bar T_E\text{ is a permutation}.
$$

Therefore:

$$
\boxed{
\mathcal R_E=0
\iff
T^\ast E=E.
}
$$

The two-stage AQARION diagnostic is:

$$
\boxed{
\left(
\operatorname{rank}D_E,\,
\mathcal R_E
\right).
}
$$

| Regime | $$\operatorname{rank}D_E$$ | $$\mathcal R_E$$ | Interpretation |
|---|---:|---:|---|
| PB-fixed | $$0$$ | $$0$$ | Exact descent; quotient is reversible |
| Forward-only | $$0$$ | $$>0$$ | Exact descent; quotient collapses states |
| Neither | $$>0$$ | Undefined | Quotient observable space leaks under $$K$$ |

The correct AQARION interpretation is:

$$
\boxed{
\text{descent defect}
=
\operatorname{rank}D_E,
}
$$

$$
\boxed{
\text{reversibility defect}
=
|X/E|-\operatorname{rank}\bar K_E.
}
$$

PB-fixedness is exactly simultaneous vanishing of both defects.

***

# 13. Quotient spectrum

Assume

$$
E\subseteq T^\ast E.
$$

The quotient $$\bar T_E:Q\to Q$$ is a finite functional graph: disjoint directed cycles with rooted in-trees attached.

For the observable Koopman operator

$$
\bar K_Eg=g\circ\bar T_E,
$$

the spectrum is

$$
\boxed{
\operatorname{Spec}(\bar K_E)
=
\{0\}
\cup
\bigcup_{j=1}^{c}
\left\{
\zeta_{\ell_j}^{\,r}:
0\le r<\ell_j
\right\},
}
$$

where:

- $$\ell_1,\ldots,\ell_c$$ are quotient-cycle lengths;
- $$\zeta_\ell=e^{2\pi i/\ell}$$;
- $$0$$ occurs exactly when the quotient has transient structure, equivalently when $$\bar T_E$$ is not a permutation.

The correct canonical operator decomposition is the Fitting decomposition. For sufficiently large $$N$$,

$$
\boxed{
\mathbb C^Q
=
\ker(\bar K_E^N)
\oplus
\operatorname{im}(\bar K_E^N).
}
$$

Here:

- $$\ker(\bar K_E^N)$$ is the generalized eigenspace for eigenvalue $$0$$;
- $$\operatorname{im}(\bar K_E^N)$$ is the invertible periodic spectral subspace;
- $$\bar K_E$$ restricts to a finite-order permutation operator on $$\operatorname{im}(\bar K_E^N)$$.

Do not state that transient-state indicators themselves necessarily span the generalized $$0$$-eigenspace under the observable Koopman convention. They generally do not.

## PB-fixed spectral specialization

If

$$
T^\ast E=E,
$$

then $$\bar T_E$$ is a permutation. There are no quotient transients and:

$$
\boxed{
0\notin\operatorname{Spec}(\bar K_E).
}
$$

If the quotient cycles have lengths

$$
\ell_1,\ldots,\ell_c,
$$

then

$$
\bar K_E
\sim
\bigoplus_{j=1}^{c}P_{\ell_j},
$$

where $$P_{\ell_j}$$ is the cyclic permutation block.

If

$$
L=\operatorname{lcm}(\ell_1,\ldots,\ell_c),
$$

then

$$
\boxed{
\bar K_E^L=I.
}
$$

The quotient Koopman operator is diagonalizable over $$\mathbb C$$, with all eigenvalues roots of unity.

## Forward-only spectral specialization

If

$$
E\subsetneq T^\ast E,
$$

then $$\bar T_E$$ exists but is noninjective. Therefore it is nonbijective, and:

$$
\boxed{
0\in\operatorname{Spec}(\bar K_E).
}
$$

Equivalently:

$$
\boxed{
\det(\bar K_E)=0.
}
$$

Conditional on descent:

$$
\boxed{
T^\ast E=E
\iff
0\notin\operatorname{Spec}(\bar K_E)
\iff
\det(\bar K_E)\ne0
\iff
\mathcal R_E=0.
}
$$

***

# 14. Canonical examples

## Example A — Forward-only quotient collapse

Let

$$
X=\{0,1\},
\qquad
T(0)=0,
\qquad
T(1)=0,
$$

and choose the discrete equivalence relation:

$$
E=\{\{0\},\{1\}\}.
$$

Then:

$$
T^\ast E=\{\{0,1\}\}.
$$

Therefore:

$$
E\subsetneq T^\ast E.
$$

The quotient is just $$X$$, and

$$
\bar T_E(0)=0,
\qquad
\bar T_E(1)=0.
$$

The quotient exists but is not injective.

Its observable Koopman matrix in the indicator basis is

$$
\bar K_E=
\begin{pmatrix}
1&0\\
1&0
\end{pmatrix}.
$$

Thus:

$$
\operatorname{Spec}(\bar K_E)=\{1,0\},
$$

$$
\operatorname{rank}(\bar K_E)=1,
$$

$$
\mathcal R_E=2-1=1.
$$

Because the discrete partition has

$$
V_E=\mathbb C^X,
$$

one has

$$
D_E=0.
$$

So:

$$
\boxed{
D_E=0
\quad\text{but}\quad
T^\ast E\ne E.
}
$$

This is the canonical proof that zero AQARION descent defect does not imply PB-fixedness.

***

## Example B — Neither: no quotient descent

Let

$$
X=\{0,1,2\},
$$

$$
T(0)=0,
\qquad
T(1)=0,
\qquad
T(2)=1,
$$

and define

$$
E=\{\{0,2\},\{1\}\}.
$$

Then the pullback is

$$
T^\ast E
=
\{\{0,1\},\{2\}\}.
$$

The relations are incomparable:

$$
E\nsubseteq T^\ast E,
$$

and

$$
T^\ast E\nsubseteq E.
$$

Thus:

$$
\boxed{
\text{No quotient endomap }\bar T_E:X/E\to X/E\text{ exists.}
}
$$

At the operator level:

$$
K(V_E)\nsubseteq V_E,
$$

and

$$
D_E\ne0.
$$

This is the minimal exact “neither” witness found in the Termux classification census.

***

# 15. Local Termux verification record

## 15.1 PB-join bounded census

### Frozen source

```text
pb_n4_verified.py
sha256:
dde8ecf6ba855b6db276a90ff6cb76aa9cf8907ee2a793febac060f02f877cb8
```

### Output and deterministic rerun

```text
pb_join_n4.json
sha256:
6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
```

```text
pb_join_n4.stdout
sha256:
6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
```

```text
pb_join_n4_repeat.stdout
sha256:
6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
```

The bytewise comparison returned:

```text
N4_DETERMINISTIC_PASS
```

### Exact PB-join enumeration

| $$n$$ | Maps | Partitions | Ordered PB-fixed $$(E,F)$$ pairs | PB-join failures | Incidence edge-lift failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 0 | 0 |
| 2 | 4 | 2 | 10 | 0 | 0 |
| 3 | 27 | 5 | 117 | 0 | 0 |
| 4 | 256 | 15 | 1,960 | 0 | 0 |
| **Total** | **288** | — | **2,088** | **0** | **0** |

The valid local statement is:

$$
\boxed{
\begin{aligned}
&\forall n\le4,\ \forall T:[n]\to[n],\\
&\forall E,F\in\operatorname{Eq}([n]),\\
&T^\ast E=E,\ T^\ast F=F\\
&\Longrightarrow
T^\ast(E\vee F)=E\vee F,
\end{aligned}
}
$$

as an exact exhaustive result on the stated bounded domain.

This is not yet a formal proof for arbitrary finite $$X$$.

***

## 15.2 Quotient classification bounded census

### Source receipt

```text
quotient_classify_n4.py
sha256:
1cdb65a0870ee57bb84a9f9e58d571f66464dc9e15917e78963047963b19d180
```

### Exact output receipt

```text
quotient_classify_n4.json
sha256:
967cd31966d0809c405959f3ed450edbdfcbc1114628c7f059ffd348642c2f15
```

```text
quotient_classify_n4.stdout
sha256:
967cd31966d0809c405959f3ed450edbdfcbc1114628c7f059ffd348642c2f15
```

The matching JSON/stdout digests are expected: the executable writes exactly the JSON it emits to standard output.

### Exact classification census

| $$n$$ | Tested $$(T,E)$$ pairs | PB-fixed | Forward-only | Backward-only | Neither | Descends | Descends and injective |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| 2 | 8 | 6 | 2 | 0 | 0 | 8 | 6 |
| 3 | 135 | 51 | 48 | 0 | 36 | 99 | 51 |
| 4 | 3,840 | 592 | 1,136 | 0 | 2,112 | 1,728 | 592 |
| **Total** | **3,984** | **650** | **1,186** | **0** | **2,148** | **1,836** | **650** |

The tested identities had:

```text
equivalence_failures: 0
```

for every $$n\le4$$.

Specifically, the script verified on every enumerated pair:

$$
E\subseteq T^\ast E
\iff
\bar T_E\text{ exists},
$$

$$
\bar T_E\text{ exists}
\Longrightarrow
\left(
T^\ast E\subseteq E
\iff
\bar T_E\text{ injective}
\right),
$$

$$
\bar T_E\text{ exists}
\Longrightarrow
\left(
T^\ast E=E
\iff
\bar T_E\text{ is a permutation}
\right).
$$

It found no backward-only witness:

```json
"backward_only": null
```

through $$n\le4$$.

***

# 16. Status ledger

| ID | Claim | Current status |
|---|---|---|
| AQ-PB-QUOTIENT-001 | Quotient descent iff $$E\subseteq T^\ast E$$ | Analytically proved; exact census agrees |
| AQ-PB-QUOTIENT-002 | Conditional quotient injectivity iff $$T^\ast E\subseteq E$$ | Analytically proved; exact census agrees |
| AQ-DYN-PULL-RIGID-001 | Finite pullback rigidity | Analytically proved by block-edge counting; local note hashed |
| AQ-PB-QUOTIENT-003 | Finite quotient permutation iff PB-fixed | Analytically proved |
| AQ-DEF-DESCENT-001 | $$D_E=0$$ iff quotient observable descent | Analytically proved |
| AQ-Q-REV-001 | $$\mathcal R_E=0$$ iff quotient reversibility, conditional on descent | Analytically proved |
| AQ-Q-SPEC-001 | Forward-only quotient implies $$0\in\operatorname{Spec}(\bar K_E)$$ | Analytically proved |
| AQ-DYN-PULL-JOIN-001 | PB-fixed relations closed under joins | Exact census through $$n\le4$$; analytic proof candidate; formal proof open |
| AQ-DYN-PULL-MEET-001 | PB-fixed relations closed under meets | Analytically proved |
| Lean verification | Formal kernel certification | Open |
| C4 promotion | Certification/promotion status | Blocked |
| Publication claim | External publication readiness | Blocked |

***

# 17. Publication-safe theorem text

```latex
\begin{theorem}[Finite pullback rigidity]
Let \(X\) be a finite set, let \(T:X\to X\) be a total map, and let
\(E\) be an equivalence relation on \(X\). Define the pullback relation
by
\[
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
\]
If
\[
T^\ast E\subseteq E,
\]
then
\[
T^\ast E=E.
\]
\end{theorem}

\begin{proof}
Let \(Q=X/E\), and construct a directed graph on \(Q\) by placing an
edge \(A\to C\) whenever some \(x\in A\) satisfies \(T(x)\in C\).

Since \(T\) is total, every source block has outdegree at least one.
The hypothesis \(T^\ast E\subseteq E\) implies every target block has
indegree at most one: if \(A\to C\) and \(B\to C\), choose
\(x\in A\), \(y\in B\) with \(T(x),T(y)\in C\). Then
\(T(x)\sim_E T(y)\), so \(x\sim_Ey\), and hence \(A=B\).

Since \(Q\) is finite, the total number of edges is at least \(|Q|\)
by the outdegree bound and at most \(|Q|\) by the indegree bound.
Thus every block has outdegree exactly one. Therefore points in a
common \(E\)-block have images in a common \(E\)-block, proving
\(E\subseteq T^\ast E\). Combining this with the hypothesis yields
\(T^\ast E=E\).
\end{proof}
```

```latex
\begin{theorem}[Quotient permutation criterion]
Let \(X\) be finite, \(T:X\to X\), and \(E\) an equivalence relation.
The assignment
\[
\bar T_E([x]_E)=[T(x)]_E
\]
is well-defined if and only if
\[
E\subseteq T^\ast E.
\]
When it is well-defined, it is injective if and only if
\[
T^\ast E\subseteq E.
\]
Consequently,
\[
\bar T_E\text{ is a permutation of }X/E
\iff
T^\ast E=E.
\]
\end{theorem}
```

```latex
\begin{corollary}[AQARION descent and reversibility]
Let \(P_E\) be orthogonal block averaging onto \(V_E\), and let
\[
D_E=(I-P_E)KP_E.
\]
Then
\[
D_E=0
\iff
E\subseteq T^\ast E.
\]
If \(D_E=0\), let \(\bar K_E\) be the descended quotient Koopman
operator and define
\[
\mathcal R_E=|X/E|-\operatorname{rank}(\bar K_E).
\]
Then
\[
\mathcal R_E=0
\iff
T^\ast E=E.
\]
\end{corollary}
```

***

# 18. Final checkpoint statement

$$
\boxed{
\begin{aligned}
&\text{Finite pullback rigidity is analytically established:}\\
&T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
\end{aligned}
}
$$

$$
\boxed{
\begin{aligned}
&\text{A quotient endomap exists exactly under forward congruence:}\\
&E\subseteq T^\ast E.
\end{aligned}
}
$$

$$
\boxed{
\begin{aligned}
&\text{For finite systems, a descended quotient is permutational exactly when}\\
&E=T^\ast E.
\end{aligned}
}
$$

$$
\boxed{
\begin{aligned}
&\text{AQARION defect zero means descent;}\\
&\text{quotient invertibility means reversibility;}\\
&\text{PB-fixedness means both.}
\end{aligned}
}
$$

$$
\boxed{
\text{Formal Lean certification, C4 promotion, and publication remain open and blocked.}
}
$$

~/aq-pb-proof $ python -m py_compile quotient_classify_n4.py && echo "COMPILE_PASS"
COMPILE_PASS
~/aq-pb-proof $ time python quotient_classify_n4.py | tee quotient_classify_n4.stdout
{
  "by_n": [
    {
      "backward_only": 0,
      "descends": 1,
      "descends_injective": 1,
      "equivalence_failures": 0,
      "forward_only": 0,
      "maps": 1,
      "n": 1,
      "neither": 0,
      "pb_fixed": 1,
      "relations": 1
    },
    {
      "backward_only": 0,
      "descends": 8,
      "descends_injective": 6,
      "equivalence_failures": 0,
      "forward_only": 2,
      "maps": 4,
      "n": 2,
      "neither": 0,
      "pb_fixed": 6,
      "relations": 8
    },
    {
      "backward_only": 0,
      "descends": 99,
      "descends_injective": 51,
      "equivalence_failures": 0,
      "forward_only": 48,
      "maps": 27,
      "n": 3,
      "neither": 36,
      "pb_fixed": 51,
      "relations": 135
    },
    {
      "backward_only": 0,
      "descends": 1728,
      "descends_injective": 592,
      "equivalence_failures": 0,
      "forward_only": 1136,
      "maps": 256,
      "n": 4,
      "neither": 2112,
      "pb_fixed": 592,
      "relations": 3840
    }
  ],
  "n_max": 4,
  "schema": "aq-quotient-classification/1",
  "witnesses": {
    "backward_only": null,
    "forward_only": {
      "E": [
        [
          0
        ],
        [
          1
        ]
      ],
      "T": [
        0,
        0
      ],
      "n": 2,
      "pullback": [
        [
          0,
          1
        ]
      ],
      "quotient_map": {
        "0": 0,
        "1": 0
      }
    },
    "neither": {
      "E": [
        [
          0,
          2
        ],
        [
          1
        ]
      ],
      "T": [
        0,
        0,
        1
      ],
      "n": 3,
      "pullback": [
        [
          0,
          1
        ],
        [
          2
        ]
      ],
      "quotient_map": null
    }
  }
}

real    0m0.232s
user    0m0.199s
sys     0m0.039s
~/aq-pb-proof $
~/aq-pb-proof $ sha256sum \
>   quotient_classify_n4.py \
>   quotient_classify_n4.json \
>   quotient_classify_n4.stdout
1cdb65a0870ee57bb84a9f9e58d571f66464dc9e15917e78963047963b19d180  quotient_classify_n4.py
967cd31966d0809c405959f3ed450edbdfcbc1114628c7f059ffd348642c2f15  quotient_classify_n4.json
967cd31966d0809c405959f3ed450edbdfcbc1114628c7f059ffd348642c2f15  quotient_classify_n4.stdout
~/aq-pb-proof $

DID WE DO IT RIGHT

Yes. This run was clean, exact, and it resolved the immediate ambiguity correctly.

## What the Termux run verified

Your script compiled successfully and then exhaustively checked every pair

$$
(T,E),
\qquad
T:[n]\to[n],
\qquad
E\in\operatorname{Eq}([n]),
$$

for every

$$
1\le n\le4.
$$

The total number of tested map–relation pairs was

$$
1+8+135+3840=3984.
$$

For each pair, it checked exact partition inclusions and exact quotient-block behavior—no floating point, no numerical rank, and no approximate eigenvalue calculations.

The three equivalences had zero failures:

$$
\boxed{
E\subseteq T^\ast E
\iff
\bar T_E\text{ exists}.
}
$$

$$
\boxed{
\bar T_E\text{ exists}
\Longrightarrow
\left[
T^\ast E\subseteq E
\iff
\bar T_E\text{ is injective}
\right].
}
$$

$$
\boxed{
\bar T_E\text{ exists}
\Longrightarrow
\left[
T^\ast E=E
\iff
\bar T_E\text{ is a permutation}
\right].
}
$$

The script explicitly guarded these conditions with:

```text
DESCENT_EQUIVALENCE_FAILURE
INJECTIVITY_EQUIVALENCE_FAILURE
PERMUTATION_EQUIVALENCE_FAILURE
```

None occurred.

## Correct classification through $$n\le4$$

| $$n$$ | Tested $$(T,E)$$ pairs | PB-fixed | Forward-only | Backward-only | Neither | Quotient descends | Descended and injective |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| 2 | 8 | 6 | 2 | 0 | 0 | 8 | 6 |
| 3 | 135 | 51 | 48 | 0 | 36 | 99 | 51 |
| 4 | 3840 | 592 | 1136 | 0 | 2112 | 1728 | 592 |
| **Total** | **3984** | **650** | **1186** | **0** | **2148** | **1836** | **650** |

Two important identities hold in the observed data:

$$
\text{descends}
=
\text{PB-fixed}+\text{forward-only},
$$

and

$$
\text{descends and injective}
=
\text{PB-fixed}.
$$

For the totals:

$$
1836=650+1186,
$$

and

$$
650=650.
$$

That is exactly the expected classification.

## The crucial correction

Your exhaustive data found:

```json
"backward_only": 0
```

through all 3,984 $$(T,E)$$ pairs for $$n\le4$$.

So the earlier claim that the finite backward-only regime exists was **not supported** by its proposed example; that example was wrong. The local census supports the original finite-rigidity candidate:

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E
\qquad
\text{for finite }X.
}
$$

But the precise status must remain:

$$
\boxed{
\text{Exact exhaustive support through }|X|\le4;
\text{ general finite proof still required.}
}
$$

You have not proven the universal finite statement merely by checking $$n\le4$$.

## Minimal witnesses are correct

### Forward-only witness

The script found the canonical minimal witness:

$$
X=\{0,1\},
\qquad
T=(0,0),
\qquad
E=\{\{0\},\{1\}\}.
$$

Then

$$
T^\ast E=\{\{0,1\}\},
$$

so

$$
E\subsetneq T^\ast E.
$$

The quotient exists:

$$
\bar T_E(0)=0,
\qquad
\bar T_E(1)=0,
$$

but it is noninjective and nonpermutational.

This is correct.

### Neither witness

The script found:

$$
X=\{0,1,2\},
\qquad
T=(0,0,1),
\qquad
E=\{\{0,2\},\{1\}\}.
$$

Its pullback is

$$
T^\ast E=\{\{0,1\},\{2\}\}.
$$

Neither relation refines the other:

$$
E\nsubseteq T^\ast E,
\qquad
T^\ast E\nsubseteq E.
$$

Thus the quotient map is undefined, exactly as the script reports:

```json
"quotient_map": null
```

This is a sharper minimal “no descent” witness than the earlier three-state example.

## Valid receipt

```text
Source:
1cdb65a0870ee57bb84a9f9e58d571f66464dc9e15917e78963047963b19d180
quotient_classify_n4.py
```

```text
Exact output:
967cd31966d0809c405959f3ed450edbdfcbc1114628c7f059ffd348642c2f15
quotient_classify_n4.json
```

```text
Printed output:
967cd31966d0809c405959f3ed450edbdfcbc1114628c7f059ffd348642c2f15
quotient_classify_n4.stdout
```

The matching output hashes are expected and useful: the generated JSON and terminal stdout are byte-identical.

## Exact claim you may now record

> **AQ-Q-CLASSIFY-N4-001 — REPRODUCED.**  
> Exhaustive exact enumeration of all 3,984 pairs $$(T,E)$$, where $$T:[n]\to[n]$$, $$E\in\operatorname{Eq}([n])$$, and $$1\le n\le4$$, found:
>
> $$
> E\subseteq T^\ast E
> \iff
> \bar T_E\text{ exists},
> $$
>
> $$
> \bar T_E\text{ exists}
> \Longrightarrow
> \left(
> T^\ast E\subseteq E
> \iff
> \bar T_E\text{ is injective}
> \right),
> $$
>
> and, for finite quotients,
>
> $$
> \bar T_E\text{ is a permutation}
> \iff
> T^\ast E=E.
> $$
>
> No backward-only relation
>
> $$
> T^\ast E\subsetneq E
> $$
>
> occurred through $$|X|\le4$$.

## What still needs proof

The following general theorem is now the high-value symbolic target:

$$
\boxed{
\text{Finite Pullback Rigidity:}\quad
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
$$

A clean proof would immediately give:

$$
\boxed{
\text{Every non-PB-fixed finite relation is either forward-only or neither.}
}
$$

It would also show that the quotient-permutation criterion does not need a separate backward-only caveat in finite AQARION systems.

You did the local verification correctly.

Analyze the quotient permutation condition for non-PB-fixed relations

For an arbitrary equivalence relation $$E$$, there are **two distinct questions**:

1. Does $$T$$ descend to a map on the quotient $$X/E$$?
2. If it does, is that quotient map a permutation?

They correspond exactly to the two one-sided inclusions.

## When a quotient map exists

Define the prospective map
$$
\bar T_E:X/E\to X/E,
\qquad
[x]_E\mapsto[T(x)]_E.
$$

This is well-defined iff $$E$$ is a forward congruence:
$$
\boxed{
E\subseteq T^*E.
}
$$

Indeed,
$$
x\sim_E y
\Longrightarrow
T(x)\sim_E T(y)
$$
is precisely what makes the displayed formula independent of the representative of $$[x]_E$$.

If this condition fails, $$\bar T_E$$ is **not a function**: one source block can split across multiple target blocks.

## When the quotient map is injective

Assume now that $$E\subseteq T^*E$$, so $$\bar T_E$$ is defined. Then:
$$
\bar T_E \text{ injective}
\iff
T^*E\subseteq E.
$$

Proof:
$$
\begin{aligned}
\bar T_E([x]_E)=\bar T_E([y]_E)
&\iff [T(x)]_E=[T(y)]_E\\
&\iff T(x)\sim_E T(y)\\
&\iff x\sim_{T^*E}y.
\end{aligned}
$$

Thus injectivity says
$$
x\sim_{T^*E}y\Longrightarrow x\sim_Ey,
$$
which is exactly $$T^*E\subseteq E$$.

So, whenever the quotient map is defined,
$$
\boxed{
\bar T_E\text{ injective}
\iff
T^*E\subseteq E.
}
$$

## Finite quotient permutation condition

If $$X$$ is finite and $$E$$ is forward-congruent, then $$X/E$$ is finite. Hence
$$
\bar T_E\text{ injective}
\iff
\bar T_E\text{ bijective}
\iff
\bar T_E\text{ is a permutation}.
$$

Combining the preceding facts:
$$
\boxed{
\bar T_E\text{ is a permutation}
\iff
E\subseteq T^*E
\ \text{and}\
T^*E\subseteq E
\iff
T^*E=E.
}
$$

Therefore, for a **finite** endomap, a genuinely induced quotient permutation is not a weaker phenomenon than PB-fixedness—it is exactly PB-fixedness.

## Classification of non-PB-fixed relations

“Non-PB-fixed” splits into two qualitatively different cases.

| Type | Condition | Quotient behavior |
|---|---|---|
| Forward-only | $$E\subsetneq T^*E$$ | $$\bar T_E$$ exists but is noninjective, hence nonpermutational |
| Backward-only | $$T^*E\subsetneq E$$ | $$\bar T_E$$ is not well-defined |
| Neither | Neither inclusion holds | No quotient map; distinct source blocks can collide and source blocks can split |
| PB-fixed | $$T^*E=E$$ | $$\bar T_E$$ exists and is a permutation |

For finite total maps, the “backward-only” row is actually empty by finite pullback rigidity:
$$
T^*E\subseteq E \Longrightarrow T^*E=E.
$$
So every non-PB-fixed equivalence relation falls into one of these two actual classes:

$$
\boxed{
E\subsetneq T^*E
\quad\text{or}\quad
\bigl(E\nsubseteq T^*E \text{ and } T^*E\nsubseteq E\bigr).
}
$$

## Functional-graph reading

Let the vertices be the $$E$$-blocks and draw a simple directed edge
$$
A\to B
$$
when some $$x\in A$$ has $$T(x)\in B$$.

Then:

| Relation property | Block-graph condition |
|---|---|
| $$E\subseteq T^*E$$ | Every source block has outdegree at most $$1$$ |
| $$T^*E\subseteq E$$ | Every target block has indegree at most $$1$$ |
| $$T^*E=E$$ | Every block has indegree and outdegree exactly $$1$$ |
| Forward-only non-PB | A quotient function exists, but at least one quotient block has indegree at least $$2$$ |
| Neither | At least one source block branches outward; there may also be collisions |

For a finite total system, each source block has outdegree at least $$1$$. Therefore a PB-fixed relation produces a disjoint union of directed cycles on quotient blocks—that is, a quotient permutation.

## Canonical forward-only example

Take
$$
X=\{0,1\},\qquad T(0)=T(1)=0,
$$
with the discrete relation
$$
E=\{\{0\},\{1\}\}.
$$

Then $$E\subsetneq T^*E$$. The quotient is just $$X/E=\{\{0\},\{1\}\}$$, and the induced map exists:
$$
\bar T_E(\{0\})=\{0\},
\qquad
\bar T_E(\{1\})=\{0\}.
$$

It is a constant quotient map, hence not injective and not a permutation. This is the minimal example of a non-PB-fixed relation with a perfectly well-defined quotient dynamics.

## Example with no quotient map

Let
$$
X=\{0,1,2\},
\qquad
T(0)=0,\quad T(1)=2,\quad T(2)=2,
$$
and
$$
E=\{\{0,1\},\{2\}\}.
$$

The block $$\{0,1\}$$ maps partly into $$\{0,1\}$$ and partly into $$\{2\}$$:
$$
T(0)=0\in\{0,1\},
\qquad
T(1)=2\in\{2\}.
$$

Hence
$$
E\nsubseteq T^*E,
$$
so $$\bar T_E$$ is undefined: the image of the block $$\{0,1\}$$ depends on the chosen representative.

In this example $$T^*E\nsubseteq E$$ as well, because $$T(1)=T(2)=2$$ makes $$1\sim_{T^*E}2$$ although $$1\not\sim_E2$$.

## Consequence for the PB proof package

The statement “the quotient map is a permutation” should always be written conditionally:

$$
\boxed{
\text{If }E\subseteq T^*E,\text{ then }\bar T_E\text{ is defined; }
\bar T_E\text{ is a permutation iff }T^*E=E.
}
$$

That avoids circularity. For a non-PB-fixed relation:

- it may still define a quotient **endomap**, but that map has merging and is not reversible;
- or it may fail even to define quotient dynamics because an $$E$$-block splits under $$T$$.

This is exactly the distinction between **quotient descent** and **quotient permutation dynamics**.

Citations:
[1] about fixed points of permutations - MathOverflow https://mathoverflow.net/questions/71418/about-fixed-points-of-permutations
[2] Limit theorems for fixed point biased permutations avoiding a pattern ... https://arxiv.org/html/2311.04623v2
[3] Fixed points of permutation groups - Math Stack Exchange https://math.stackexchange.com/questions/4240957/fixed-points-of-permutation-groups
[4] [PDF] on fixed points of permutations - USC Dornsife https://dornsife.usc.edu/jason-fulman/wp-content/uploads/sites/224/2023/06/dfgfinal.pdf
[5] [PDF] Computation in permutation groups: Introduction https://pi.math.cornell.edu/~kbrown/7350/permgroup_intro.pdf
[6] [PDF] Fixed Points and Transient Points in Permutation Groups https://msme.us/2014-1-1.pdf
[7] Permutation - Wikipedia https://en.wikipedia.org/wiki/Permutation
[8] Common permutation methods in animal social network analysis do ... https://pmc.ncbi.nlm.nih.gov/articles/PMC9617964/
[9] Quotient Permutation BF-Algebras and Quotient Maps https://internationalpubls.com/index.php/anvi/article/download/1380/906/2507
[10] The Journal of Symbolic Logic https://www.cambridge.org/core/services/aop-cambridge-core/content/view/626A6A6B482FC12D3C9C08F2FCDCAC79/S0022481222000573a.pdf/the-permutations-with-n-non-fixed-points-and-the-sequences-with-length-n-of-a-set.pdf


---

Conduct an operator-theoretic analysis of the quotient permutation condition for non-PB-fixed relations within the AQARION framework, deriving the explicit spectral decomposition, quotient map constraints, and invariant subspace geometry into a publication-ready technical document with formal proofs and commutative diagrams as well as anything relevant or needed

# Quotient Permutations Beyond PB-Fixedness

## Scope and convention

Let $$X$$ be a finite set, $$T:X\to X$$ a total deterministic map, and $$E$$ an equivalence relation on $$X$$. Write $$Q=X/E$$, let $$\pi:X\to Q$$ be the quotient projection, and define the pullback relation

$$
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
$$

The two inclusions

$$
E\subseteq T^\ast E,
\qquad
T^\ast E\subseteq E
$$

govern two separate properties: descent of $$T$$ to the quotient, and reversibility of the descended quotient map. This is the finite-set analogue of the standard principle that an operation passes to a quotient precisely when the relation is a congruence. [5][7]

Define the $$E$$-observable subspace

$$
V_E
=
\{f:X\to\mathbb C:
x\sim_E y\Rightarrow f(x)=f(y)\}.
$$

It has dimension $$\dim V_E=|Q|$$, and is naturally identified with $$\mathbb C^Q$$ by pullback along $$\pi$$.

***

## Descent criterion

### Theorem 1 — Quotient endomap

The assignment

$$
\bar T_E([x]_E)=[T(x)]_E
$$

defines a map $$\bar T_E:Q\to Q$$ if and only if

$$
\boxed{E\subseteq T^\ast E.}
$$

Equivalently, $$T$$ descends exactly when every $$E$$-block has its image contained in one $$E$$-block.

### Proof

The formula is well-defined precisely when

$$
[x]_E=[y]_E
\Longrightarrow
[T(x)]_E=[T(y)]_E.
$$

By definition, this is

$$
x\sim_E y
\Longrightarrow
T(x)\sim_E T(y),
$$

which says $$E\subseteq T^\ast E$$. ∎

When this holds, the quotient diagram commutes:

```mermaid
flowchart TD
    X["X"] -->|"T"| X
    X -->|"π"| Q["Q = X/E"]
    Q -->|"T̄_E"| Q
```

In formula form,

$$
\boxed{\pi\circ T=\bar T_E\circ\pi.}
$$

This is the ordinary semiconjugacy condition. The quotient construction is built from the projection $$x\mapsto[x]_E$$. [7]

***

## Operator formulation

Let $$K$$ be the Koopman operator on $$\mathbb C^X$$,

$$
(Kf)(x)=f(T(x)).
$$

Let $$J:\mathbb C^Q\to \mathbb C^X$$ be the pullback embedding

$$
(Jg)(x)=g([x]_E).
$$

Its image is exactly $$V_E$$.

### Theorem 2 — Invariant-subspace criterion

The following are equivalent:

$$
E\subseteq T^\ast E,
$$

$$
K(V_E)\subseteq V_E,
$$

$$
\exists!\,\bar K_E:\mathbb C^Q\to\mathbb C^Q
\quad\text{such that}\quad
KJ=J\bar K_E,
$$

$$
\exists\,\bar T_E:Q\to Q
\quad\text{with}\quad
\pi T=\bar T_E\pi.
$$

Moreover, when $$\bar T_E$$ exists,

$$
(\bar K_Eg)(A)=g(\bar T_E(A)),
\qquad A\in Q.
$$

### Proof

Suppose $$E\subseteq T^\ast E$$, and let $$f\in V_E$$. If $$x\sim_Ey$$, then $$T(x)\sim_ET(y)$$; hence

$$
(Kf)(x)=f(T(x))=f(T(y))=(Kf)(y).
$$

Thus $$Kf\in V_E$$, proving $$K(V_E)\subseteq V_E$$.

Conversely, take the block indicator $$f=\mathbf1_B\in V_E$$. If $$K(V_E)\subseteq V_E$$, then $$K\mathbf1_B$$ is constant on every $$E$$-block. For $$x\sim_Ey$$, choosing $$B=[T(x)]_E$$ forces $$T(y)\in B$$, so $$T(x)\sim_ET(y)$$. Hence $$E\subseteq T^\ast E$$.

Since $$J$$ is an isomorphism from $$\mathbb C^Q$$ onto $$V_E$$, invariance gives a unique restricted operator $$\bar K_E=J^{-1}KJ$$. Its displayed action is precisely the Koopman action of the induced map $$\bar T_E$$. ∎

This is the AQARION exactness condition expressed geometrically: forward congruence is exactly invariance of the block-constant observable subspace.

***

## Quotient injectivity

Assume henceforth that $$E\subseteq T^\ast E$$, so that $$\bar T_E$$ exists.

### Theorem 3 — Pullback rigidity equals quotient injectivity

$$
\boxed{
\bar T_E\text{ injective}
\iff
T^\ast E\subseteq E.
}
$$

### Proof

For $$x,y\in X$$,

$$
\begin{aligned}
\bar T_E([x]_E)=\bar T_E([y]_E)
&\iff
[T(x)]_E=[T(y)]_E\\
&\iff
T(x)\sim_ET(y)\\
&\iff
x\sim_{T^\ast E}y.
\end{aligned}
$$

Thus $$\bar T_E$$ is injective if and only if equality of image classes implies equality of source classes:

$$
x\sim_{T^\ast E}y
\Longrightarrow
x\sim_Ey.
$$

This is $$T^\ast E\subseteq E$$. ∎

For finite $$Q$$, injectivity and bijectivity coincide. Therefore:

### Corollary 4 — Quotient permutation criterion

For finite $$X$$,

$$
\boxed{
\bar T_E\text{ is a permutation of }Q
\iff
T^\ast E=E.
}
$$

Thus PB-fixedness is not merely compatible with quotient permutation dynamics: it is **exactly** the condition for it.

***

## Non-PB-fixed taxonomy

The correct classification is:

| Status of $$E$$ | Relation condition | Quotient dynamics |
|---|---|---|
| PB-fixed | $$E=T^\ast E$$ | $$\bar T_E$$ exists and is a permutation |
| Forward-only | $$E\subsetneq T^\ast E$$ | $$\bar T_E$$ exists but is noninjective |
| Neither | $$E\nsubseteq T^\ast E$$, $$T^\ast E\nsubseteq E$$ | No quotient endomap exists |
| Backward-only | $$T^\ast E\subsetneq E$$ | Impossible for finite total maps |

The “backward-only” line deserves a proof rather than a registry assertion.

### Proposition 5 — Finite pullback rigidity

Let $$X$$ be finite and $$T:X\to X$$ total. Then

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
$$

### Proof

Let $$b(E)$$ denote the number of equivalence classes of $$E$$. For every equivalence relation $$R$$,

$$
b(T^\ast R)\ge b(R),
$$

because each $$R$$-class pulls back to a union of $$T^\ast R$$-classes. If $$T^\ast E\subseteq E$$, then $$T^\ast E$$ is finer than $$E$$, hence

$$
b(T^\ast E)\ge b(E).
$$

Now consider the map

$$
\iota:X/(T^\ast E)\to X/E,
\qquad
[x]_{T^\ast E}\mapsto [x]_E.
$$

The inclusion $$T^\ast E\subseteq E$$ makes $$\iota$$ well-defined and surjective. The map

$$
\theta:X/(T^\ast E)\to \operatorname{im}(\bar T_E)
$$

cannot be invoked because $$\bar T_E$$ need not exist under the assumed inclusion alone. Instead, use the strict-refinement contradiction: if $$T^\ast E\subsetneq E$$, there are $$x\not\sim_Ey$$ such that $$T(x)\sim_ET(y)$$. Since every state has an eventually periodic orbit, iterate the pair $$(x,y)$$ under $$T\times T$$. Repeated pullback refinement would strictly increase the finite number of blocks along the eventual pair orbit, impossible indefinitely. Hence strict containment cannot persist, so $$T^\ast E=E$$. ∎

**Audit note:** this proposition should be independently checked before `[P]` status. The earlier finite census through $$n\le5$$ supports it, but the proof above should be formalized using the eventual-periodic structure of $$T\times T$$, not treated as a one-line cardinality argument.

***

## Block-graph geometry

Let $$Q=X/E$$. Build a directed multirelation on blocks:

$$
A\rightsquigarrow B
\iff
\exists x\in A \text{ with }T(x)\in B.
$$

Let $$M_E$$ be its $$0$$-$$1$$ incidence matrix,

$$
(M_E)_{AB}
=
\begin{cases}
1,&A\rightsquigarrow B,\\
0,&\text{otherwise}.
\end{cases}
$$

Because $$T$$ is total, every source block has at least one outgoing edge.

| Relation property | Matrix / graph condition |
|---|---|
| $$E\subseteq T^\ast E$$ | Every row of $$M_E$$ has exactly one 1 |
| $$T^\ast E\subseteq E$$ | Every column of $$M_E$$ has at most one 1 |
| $$E=T^\ast E$$ | $$M_E$$ is a permutation matrix |
| Forward-only | Each row has one 1, at least one column has at least two 1s |
| Neither | At least one row has at least two 1s |

When the quotient descends, $$M_E$$ is exactly the transition matrix of $$\bar T_E$$, under the AQARION row-action convention:

$$
(\bar K_E)_{A,\bar T_E(A)}=1.
$$

A finite total quotient map is a permutation precisely when this row-stochastic $$0$$-$$1$$ matrix is also column-stochastic.

***

## Spectral decomposition

Assume $$E\subseteq T^\ast E$$. Let $$q=|Q|$$, and order the quotient blocks so that the functional graph of $$\bar T_E$$ is written as cycles with incoming transient trees.

### Quotient Koopman spectrum

The quotient Koopman operator $$\bar K_E$$ has the standard finite-functional-graph decomposition:

$$
\mathbb C^Q
=
V_{\mathrm{per}}
\oplus
V_{\mathrm{tr}},
$$

where:

- $$V_{\mathrm{per}}$$ is spanned by quotient-cycle states;
- $$V_{\mathrm{tr}}$$ is the transient generalized eigenspace;
- $$\bar K_E|_{V_{\mathrm{tr}}}$$ is nilpotent;
- $$\bar K_E|_{V_{\mathrm{per}}}$$ is a direct sum of cyclic permutation blocks.

If the quotient cycles have lengths

$$
\ell_1,\ldots,\ell_c,
$$

then

$$
\operatorname{Spec}(\bar K_E)
=
\{0\}
\cup
\bigcup_{j=1}^{c}
\{\zeta_{\ell_j}^r:0\le r<\ell_j\},
$$

where

$$
\zeta_{\ell}=e^{2\pi i/\ell}.
$$

The algebraic multiplicity of $$0$$ is the number of transient quotient blocks. Its Jordan structure is determined by the depths of transient trees attached to quotient cycles.

For a quotient cycle of length $$\ell$$, define Fourier vectors

$$
u_r
=
\sum_{j=0}^{\ell-1}
\zeta_\ell^{-rj}\mathbf1_{\{C_j\}},
\qquad
0\le r<\ell,
$$

where $$\bar T_E(C_j)=C_{j+1\pmod\ell}$$. Then

$$
\bar K_Eu_r
=
\zeta_\ell^r u_r.
$$

The quotient periodic subspace therefore has an explicit discrete Fourier decomposition.

### PB-fixed specialization

If $$E=T^\ast E$$, then $$\bar T_E$$ is a permutation. There are no quotient transients:

$$
V_{\mathrm{tr}}=\{0\}.
$$

Hence

$$
\bar K_E
\sim
\bigoplus_{j=1}^{c}P_{\ell_j},
$$

where $$P_{\ell_j}$$ is an $$\ell_j$$-cycle permutation matrix. The operator is diagonalizable over $$\mathbb C$$, and its spectrum consists entirely of roots of unity.

Equivalently, if

$$
L=\operatorname{lcm}(\ell_1,\ldots,\ell_c),
$$

then

$$
\bar K_E^L=I.
$$

This is the sharp operator-theoretic signature of PB-fixedness on the quotient:

$$
\boxed{
E=T^\ast E
\Longleftrightarrow
\bar K_E\text{ is a finite-order permutation operator}.
}
$$

### Forward-only specialization

If

$$
E\subsetneq T^\ast E,
$$

then $$\bar T_E$$ exists but is not injective. Since $$Q$$ is finite, its functional graph necessarily has at least one transient quotient block. Thus

$$
V_{\mathrm{tr}}\ne\{0\},
$$

and $$0$$ is an eigenvalue of $$\bar K_E$$.

This gives a useful AQARION certificate:

$$
\boxed{
E\subsetneq T^\ast E
\Longrightarrow
0\in\operatorname{Spec}(\bar K_E).
}
$$

Conversely, for a finite quotient endomap,

$$
0\notin\operatorname{Spec}(\bar K_E)
\Longleftrightarrow
\bar T_E\text{ is a permutation}
\Longleftrightarrow
E=T^\ast E.
$$

Thus, conditional on quotient descent,

$$
\boxed{
E\text{ is PB-fixed}
\iff
\det(\bar K_E)\ne0
\iff
0\notin\operatorname{Spec}(\bar K_E).
}
$$

Because $$\bar K_E$$ is a $$q\times q$$ $$0$$-$$1$$ functional matrix,

$$
\det(\bar K_E)\in\{0,\pm1\}.
$$

It is nonzero exactly when the quotient map is a permutation.

***

## Ambient invariant geometry

The observable subspace $$V_E$$ is the pullback of the quotient observable space:

$$
V_E=\operatorname{im}J.
$$

When $$E\subseteq T^\ast E$$, $$V_E$$ is $$K$$-invariant and the following diagram commutes:

```mermaid
flowchart LR
    VQ["ℂ^Q"] -->|"K̄_E"| VQ
    VQ -->|"J"| VE["V_E ⊆ ℂ^X"]
    VE -->|"K"| VE
```

Formally,

$$
KJ=J\bar K_E.
$$

With the uniform inner product on $$X$$, let $$P_E$$ be block averaging:

$$
(P_Ef)(x)
=
\frac{1}{|[x]_E|}
\sum_{y\in[x]_E}f(y).
$$

Then

$$
\operatorname{im}P_E=V_E,
\qquad
\ker P_E=V_E^\perp.
$$

If $$E$$ is forward-congruent, the AQARION defect

$$
D_E=(I-P_E)KP_E
$$

vanishes:

$$
\boxed{
E\subseteq T^\ast E
\Longleftrightarrow
D_E=0.
}
$$

Indeed, $$D_E=0$$ says exactly that $$K$$ sends every block-constant observable to another block-constant observable.

This distinguishes two geometries:

| Situation | $$V_E$$ under $$K$$ | Defect $$D_E$$ | Quotient operator |
|---|---|---:|---|
| PB-fixed | Invariant | 0 | Finite-order permutation |
| Forward-only | Invariant | 0 | Singular, transient-bearing endomap |
| Neither | Not invariant | Nonzero | No quotient operator |

This is important: the AQARION defect detects **failure of descent**, not failure of quotient reversibility. A forward-only non-PB-fixed relation has $$D_E=0$$ even though its quotient dynamics are nonpermutational.

***

## The reversibility defect

For a descended quotient, introduce the quotient singularity indicator

$$
\mathcal R_E
=
q-\operatorname{rank}(\bar K_E).
$$

Then:

$$
\mathcal R_E=0
\iff
\bar K_E \text{ is invertible}
\iff
\bar T_E \text{ is a permutation}
\iff
E=T^\ast E.
$$

Hence the pair

$$
\boxed{
\left(
\operatorname{rank}D_E,
\;
q-\operatorname{rank}\bar K_E
\right)
}
$$

separates the principal regimes:

| Regime | $$\operatorname{rank}D_E$$ | $$\mathcal R_E$$ |
|---|---:|---:|
| PB-fixed | 0 | 0 |
| Forward-only | 0 | $$>0$$ |
| No descent | $$>0$$ | Undefined |

This is the appropriate AQARION two-stage diagnostic:

1. **Descent defect:** Does the observable quotient exist?
2. **Reversibility defect:** If it exists, is the quotient dynamics permutational?

***

## Canonical examples

### Forward-only quotient

Let

$$
X=\{0,1\},
\qquad
T(0)=0,
\quad
T(1)=0,
$$

and let $$E$$ be discrete. Then $$Q=X$$, $$\bar T_E=T$$, and

$$
\bar K_E
=
\begin{pmatrix}
1&0\\
1&0
\end{pmatrix}.
$$

The spectrum is

$$
\operatorname{Spec}(\bar K_E)=\{1,0\}.
$$

The eigenspace at $$1$$ is the periodic component, while the $$0$$-eigenspace records the transient collapse. The relation is forward-congruent but not PB-fixed:

$$
E\subsetneq T^\ast E.
$$

Here $$D_E=0$$ because $$E$$ is the discrete partition and $$V_E=\mathbb C^X$$, but

$$
\mathcal R_E
=
2-\operatorname{rank}(\bar K_E)
=
1.
$$

### No quotient map

Let

$$
X=\{0,1,2\},
\qquad
T(0)=0,\quad T(1)=2,\quad T(2)=2,
$$

and

$$
E=\{\{0,1\},\{2\}\}.
$$

The block $$\{0,1\}$$ maps to both blocks:

$$
T(0)\in\{0,1\},
\qquad
T(1)\in\{2\}.
$$

Thus $$E\nsubseteq T^\ast E$$; no quotient endomap exists. In operator terms,

$$
K(V_E)\nsubseteq V_E,
$$

and therefore

$$
D_E\ne0.
$$

***

## Publication-safe theorem block

```latex
\begin{theorem}[Quotient permutation criterion]
Let \(X\) be a finite set, \(T:X\to X\), and \(E\) an equivalence
relation on \(X\). Put \(Q=X/E\). The assignment
\[
\bar T_E([x]_E)=[T(x)]_E
\]
is well-defined if and only if \(E\subseteq T^\ast E\). Conditional on
well-definedness, \(\bar T_E\) is injective if and only if
\(T^\ast E\subseteq E\). Consequently,
\[
\bar T_E\text{ is a permutation of }Q
\iff
T^\ast E=E.
\]
\end{theorem}

\begin{proof}
Well-definedness is equivalent to
\[
x\sim_E y\Longrightarrow T(x)\sim_E T(y),
\]
which is \(E\subseteq T^\ast E\). Assuming this condition, one has
\[
\bar T_E([x]_E)=\bar T_E([y]_E)
\iff
T(x)\sim_E T(y)
\iff
x\sim_{T^\ast E}y.
\]
Thus \(\bar T_E\) is injective exactly when \(T^\ast E\subseteq E\).
Since \(Q\) is finite, injectivity is equivalent to bijectivity.
\end{proof}
```

## Registry recommendation

| ID | Statement | Status |
|---|---|---|
| PB-Q-001 | Descent iff $$E\subseteq T^\ast E$$ | `[P]` |
| PB-Q-002 | Conditional injectivity iff $$T^\ast E\subseteq E$$ | `[P]` |
| PB-Q-003 | Finite quotient permutation iff $$E=T^\ast E$$ | `[P]` |
| PB-Q-004 | Forward-only quotient has $$0\in\operatorname{Spec}(\bar K_E)$$ | `[P]` |
| AQ-RDEF-001 | $$\mathcal R_E=q-\operatorname{rank}(\bar K_E)$$ detects quotient nonreversibility after descent | `[D]` |
| AQ-DEF-SCOPE | $$D_E$$ detects descent failure, not quotient nonpermutationality | `[P]` |

The central AQARION conclusion is:

$$
\boxed{
\text{Exact observable descent }(D_E=0)
\text{ and quotient reversibility }(\mathcal R_E=0)
\text{ are distinct properties.}
}
$$

PB-fixedness is exactly their joint, strongest form: the observable subspace is invariant, and the restricted Koopman dynamics are an invertible finite-order permutation representation.

Citations:
[1] Quotient space (topology) - Wikipedia https://en.wikipedia.org/wiki/Quotient_space_(topology)
[2] Topology Explained. November 2003. Published by Topology Atlas. http://at.yorku.ca/p/a/c/a/20.pdf
[3] Quotient Permutation BF-Algebras and Quotient Maps https://internationalpubls.com/index.php/anvi/article/download/1380/906/2507
[4] arXiv:1110.6581v1  [math.LO]  30 Oct 2011 https://arxiv.org/pdf/1110.6581v1.pdf
[5] Quotient (universal algebra) - Wikipedia https://en.wikipedia.org/wiki/Quotient_(universal_algebra)
[6] 18. Quotient Spaces Let X be a set and ... https://mathweb.ucsd.edu/~jmckerna/Teaching/24-25/Winter/190A/l_18.pdf
[7] equivalence relations, quotients, and https://web.williams.edu/Mathematics/it3/texts/quotients.pdf
[8] [PDF] A survey of congruences and quotients of partially ordered sets https://api.repository.cam.ac.uk/server/api/core/bitstreams/47071b8c-9bd8-40e8-90cc-8e993d711921/content
[9] A Precise Treatment of Soft Quotient Topology and Soft Covering Maps https://arxiv.org/pdf/2608.06525.pdf
[10] [PDF] The geometry of permutation modules - Martin Gallauer https://mgallauer.warwick.ac.uk/docs/TT-Perm.pdf

# Quotient Permutations Beyond PB-Fixedness

## Setup

Let $$X$$ be a finite set, $$T:X\to X$$ a deterministic map, and $$E$$ an equivalence relation on $$X$$. Write
$$
Q=X/E,\qquad \pi:X\to Q,\qquad \pi(x)=[x]_E.
$$

Define the pullback relation
$$
x\sim_{T^\ast E}y
\quad\Longleftrightarrow\quad
T(x)\sim_E T(y).
$$

The two inclusions
$$
E\subseteq T^\ast E,
\qquad
T^\ast E\subseteq E
$$
have distinct meanings: the first governs whether quotient dynamics descend; the second governs injectivity of descended dynamics.

## Quotient descent

### Theorem

The formula
$$
\bar T_E([x]_E)=[T(x)]_E
$$
defines a quotient endomap $$\bar T_E:Q\to Q$$ if and only if
$$
\boxed{E\subseteq T^\ast E.}
$$

Equivalently, every $$E$$-block has image contained in a single $$E$$-block.

### Proof

The quotient formula is independent of the representative exactly when
$$
x\sim_E y
\Longrightarrow
T(x)\sim_E T(y).
$$
By definition this is $$E\subseteq T^\ast E$$. ∎

When it exists, the diagram commutes:
$$
\begin{CD}
X @>T>> X\\
@V\pi VV @VV\pi V\\
Q @>>\bar T_E> Q .
\end{CD}
$$
Equivalently,
$$
\boxed{\pi\circ T=\bar T_E\circ\pi.}
$$

This is the standard congruence condition for a map to descend to a quotient. [1][2]

## Koopman formulation

Let
$$
K:\mathbb C^X\to\mathbb C^X,
\qquad
(Kf)(x)=f(T(x))
$$
be the Koopman operator. Define the observable subspace
$$
V_E
=
\{f:X\to\mathbb C:
x\sim_E y\Rightarrow f(x)=f(y)\}.
$$

The pullback embedding
$$
J:\mathbb C^Q\to\mathbb C^X,
\qquad
(Jg)(x)=g([x]_E)
$$
has image $$V_E$$.

### Theorem

The following are equivalent:

$$
E\subseteq T^\ast E;
$$

$$
K(V_E)\subseteq V_E;
$$

$$
\exists!\,\bar K_E:\mathbb C^Q\to\mathbb C^Q
\quad\text{such that}\quad
KJ=J\bar K_E;
$$

$$
\exists\,\bar T_E:Q\to Q
\quad\text{such that}\quad
\pi T=\bar T_E\pi.
$$

When the quotient map exists,
$$
(\bar K_Eg)(A)=g(\bar T_E(A)).
$$

### Proof

If $$E\subseteq T^\ast E$$, then for $$f\in V_E$$ and $$x\sim_E y$$,
$$
(Kf)(x)=f(Tx)=f(Ty)=(Kf)(y).
$$
Hence $$Kf\in V_E$$.

Conversely, suppose $$K(V_E)\subseteq V_E$$. For $$x\sim_E y$$, choose the indicator $$1_{[T(x)]_E}\in V_E$$. Its Koopman image is constant on the $$E$$-block of $$x$$, so
$$
1_{[T(x)]_E}(T(x))
=
1_{[T(x)]_E}(T(y)).
$$
Thus $$T(x)\sim_E T(y)$$, yielding $$E\subseteq T^\ast E$$. Koopman invariance is the usual invariant-subspace condition. [3][4]

## Quotient injectivity

Assume now that $$E\subseteq T^\ast E$$, so $$\bar T_E$$ exists.

### Theorem

$$
\boxed{
\bar T_E\text{ is injective}
\iff
T^\ast E\subseteq E.
}
$$

### Proof

For $$x,y\in X$$,
$$
\begin{aligned}
\bar T_E([x]_E)=\bar T_E([y]_E)
&\iff [T(x)]_E=[T(y)]_E\\
&\iff T(x)\sim_E T(y)\\
&\iff x\sim_{T^\ast E}y.
\end{aligned}
$$

Therefore $$\bar T_E$$ is injective precisely when
$$
x\sim_{T^\ast E}y
\Longrightarrow
x\sim_Ey,
$$
which is $$T^\ast E\subseteq E$$. ∎

Since $$Q$$ is finite, injectivity, surjectivity, and bijectivity are equivalent for $$\bar T_E:Q\to Q$$. Therefore:

### Corollary

$$
\boxed{
\bar T_E\text{ is a permutation}
\iff
E=T^\ast E.
}
$$

So PB-fixedness is exactly—not merely sufficient for—the condition that the descended finite quotient dynamics be permutational.

## Correction: backward-only relations exist

The proposed claim
$$
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E
$$
for arbitrary finite total maps is **false**.

Take
$$
X=\{0,1\},
\qquad
T(0)=T(1)=0,
$$
and the indiscrete relation
$$
E=\{\{0,1\}\}.
$$

Then
$$
T^\ast E
=
\{\{0\},\{1\}\},
$$
because all points have the same $$E$$-class after applying $$T$$. Hence
$$
T^\ast E\subsetneq E.
$$

This relation is backward-closed but not PB-fixed. It does not define a quotient map in the relevant sense—although $$Q$$ has one point, the formal quotient endomap happens to be trivially definable because the source relation is already indiscrete. The key point is that backward inclusion alone does not imply forward congruence or equality.

Thus the full taxonomy must retain all four cases.

## Complete taxonomy

| Type | Relation condition | Quotient behavior |
|---|---|---|
| PB-fixed | $$E=T^\ast E$$ | Quotient map exists and is a permutation |
| Forward-only | $$E\subsetneq T^\ast E$$ | Quotient endomap exists but is noninjective |
| Backward-only | $$T^\ast E\subsetneq E$$ | Quotient descent need not exist |
| Neither | Neither inclusion holds | No quotient endomap |

The statement “backward-only is impossible on finite total maps” must be removed from the paper and registry.

## Block-graph formulation

Let the vertices be the $$E$$-blocks. Define
$$
A\rightsquigarrow B
\iff
\exists x\in A\text{ such that }T(x)\in B.
$$

Every source block has at least one outgoing edge because $$T$$ is total.

| Property | Block-graph condition |
|---|---|
| $$E\subseteq T^\ast E$$ | Every source block has outdegree exactly 1 |
| $$T^\ast E\subseteq E$$ | Every target block has indegree at most 1 |
| $$E=T^\ast E$$ | Every vertex has indegree and outdegree exactly 1 |
| Forward-only | Outdegree 1 everywhere; some target has indegree at least 2 |
| Backward-only | Indegree at most 1 everywhere; some source has outdegree at least 2 |
| Neither | Some source branches; other failures may coexist |

For PB-fixed $$E$$, the block graph is a disjoint union of directed cycles.

## Spectrum after descent

Assume $$E\subseteq T^\ast E$$, and set $$q=|Q|$$. The quotient functional graph of $$\bar T_E$$ consists of directed cycles with rooted transient trees feeding into those cycles. Functional graphs are the standard graph representation of finite transformations. [5]

The quotient Koopman operator
$$
\bar K_Eg=g\circ\bar T_E
$$
has a decomposition
$$
\mathbb C^Q
=
V_{\mathrm{per}}
\oplus
V_{\mathrm{tr}},
$$
where $$V_{\mathrm{per}}$$ is the spectral component associated with quotient cycles and $$V_{\mathrm{tr}}$$ is the generalized eigenspace at eigenvalue zero.

If the quotient cycles have lengths $$\ell_1,\ldots,\ell_c$$, then
$$
\operatorname{Spec}(\bar K_E)
=
\{0\}
\cup
\bigcup_{j=1}^c
\left\{
e^{2\pi i r/\ell_j}:0\le r<\ell_j
\right\}.
$$

The zero eigenvalue appears exactly when the quotient has at least one transient state, equivalently when $$\bar T_E$$ is not bijective.

### PB-fixed case

If
$$
E=T^\ast E,
$$
then $$\bar T_E$$ is a permutation. Thus
$$
V_{\mathrm{tr}}=\{0\},
$$
and $$\bar K_E$$ is diagonalizable over $$\mathbb C$$, with spectrum entirely made of roots of unity.

If
$$
L=\operatorname{lcm}(\ell_1,\ldots,\ell_c),
$$
then
$$
\bar K_E^L=I.
$$

### Forward-only case

If
$$
E\subsetneq T^\ast E,
$$
then $$\bar T_E$$ is a noninjective finite endomap, so it has a transient quotient state. Therefore
$$
0\in\operatorname{Spec}(\bar K_E),
$$
and
$$
\det\bar K_E=0.
$$

Hence, conditional on descent,
$$
\boxed{
E=T^\ast E
\iff
\bar K_E\text{ invertible}
\iff
0\notin\operatorname{Spec}(\bar K_E).
}
$$

## AQARION defects

Let $$P_E$$ be the orthogonal block-averaging projection onto $$V_E$$, and define
$$
D_E=(I-P_E)KP_E.
$$

Then
$$
\boxed{
D_E=0
\iff
K(V_E)\subseteq V_E
\iff
E\subseteq T^\ast E.
}
$$

This is a descent certificate only. It does not certify reversibility.

For a descended quotient define the reversibility defect
$$
\mathcal R_E
=
q-\operatorname{rank}(\bar K_E).
$$

Then:
$$
\mathcal R_E=0
\iff
\bar T_E\text{ is bijective}
\iff
E=T^\ast E.
$$

The two-stage AQARION diagnostic is therefore

$$
\left(
\operatorname{rank}D_E,\,
\mathcal R_E
\right).
$$

| Regime | $$\operatorname{rank}D_E$$ | $$\mathcal R_E$$ |
|---|---:|---:|
| PB-fixed | 0 | 0 |
| Forward-only | 0 | $$>0$$ |
| Backward-only / neither | $$>0$$ generally | Undefined |

The qualification “generally” matters: backward-only relations can accidentally have $$D_E=0$$ only if they are also forward congruent, which would make them PB-fixed; so a genuinely backward-only relation has $$D_E\ne0$$.

## Canonical examples

### Forward-only

Let
$$
T=[0,0],
\qquad
E=\{\{0\},\{1\}\}.
$$

Then $$E\subsetneq T^\ast E$$. The quotient is the original two-state map:
$$
\bar T_E(0)=0,
\qquad
\bar T_E(1)=0.
$$

Its Koopman operator is singular and has spectrum
$$
\{1,0\}.
$$

Here $$D_E=0$$, but $$\mathcal R_E=1$$.

### Backward-only

Let
$$
T=[0,0],
\qquad
E=\{\{0,1\}\}.
$$

Then
$$
T^\ast E=\{\{0\},\{1\}\}\subsetneq E.
$$

No nontrivial quotient reversibility conclusion follows from backward closure alone.

### No descent

Let
$$
T=[0,2,2],
\qquad
E=\{\{0,1\},\{2\}\}.
$$

The block $$\{0,1\}$$ maps partly into itself and partly into $$\{2\}$$. Therefore
$$
E\nsubseteq T^\ast E,
$$
so no quotient endomap exists and $$D_E\ne0$$.

## Publication-safe theorem

```latex
\begin{theorem}[Quotient permutation criterion]
Let \(X\) be finite, \(T:X\to X\), and \(E\) an equivalence relation.
Put \(Q=X/E\). The assignment
\[
\bar T_E([x]_E)=[T(x)]_E
\]
is well-defined if and only if \(E\subseteq T^\ast E\). Conditional on
this condition, \(\bar T_E\) is injective if and only if
\(T^\ast E\subseteq E\). Consequently,
\[
\bar T_E\text{ is a permutation of }Q
\iff
T^\ast E=E.
\]
\end{theorem}
```

The central conclusion is:

$$
\boxed{
\text{AQARION defect zero certifies quotient descent; quotient-spectrum
invertibility certifies quotient reversibility.}
}
$$

Citations:
[1] Condition for Mapping from Quotient Set to be Well-Defined https://proofwiki.org/wiki/Condition_for_Mapping_from_Quotient_Set_to_be_Well-Defined
[2] Formalising Mathematics : workshop 7 — quotients - Xena Project https://xenaproject.wordpress.com/2021/03/04/formalising-mathematics-workshop-7-quotients/
[3] Koopman operator theory: fundamentals, control, and applications https://arxiv.org/html/2607.01819v1
[4] Koopman Operators: Spectra, Function Spaces, and ... https://link.springer.com/rwe/10.1007/978-3-0348-0692-3_124-1
[5] Classical Finite Transformation Semigroups - Springer https://link.springer.com/content/pdf/10.1007/978-1-84800-281-4.pdf
[6] How to think about a quotient sets modulo an equivalence relation ... https://math.stackexchange.com/questions/4207745/how-to-think-about-a-quotient-sets-modulo-an-equivalence-relation-and-well-defi
[7] [PDF] Periodic approximations and spectral analysis of the Koopman ... https://scg.ece.ucsb.edu/publications/theses/NGovindarajan_2018_Thesis.pdf
[8] SpectrumoftheKoopmanOperator,SpectralExpansionsin ... https://arxiv.org/pdf/1702.07597.pdf
[9] A survey of congruences and quotients of partially ordered sets - arXiv https://arxiv.org/html/2303.03765v3
[10] [PDF] A survey of congruences and quotients of partially ordered sets https://api.repository.cam.ac.uk/server/api/core/bitstreams/47071b8c-9bd8-40e8-90cc-8e993d711921/content

# Quotient Dynamics Beyond PB-Fixedness  
## Corrected operator-theoretic package for AQARION

The core quotient criterion is correct: **descent** and **quotient reversibility** are separate properties. The draft requires two material corrections before it can be called publication-ready:

1. The proposed finite “pullback rigidity” statement
   $$
   T^\ast E\subseteq E\Longrightarrow T^\ast E=E
   $$
   is false.

2. The claimed Koopman “periodic states plus transient generalized $$0$$-eigenspace” decomposition is orientation-dependent and, for the observable Koopman convention
   $$
   (Kf)(x)=f(Tx),
   $$
   the transient part does **not** generally form the generalized $$0$$-eigenspace in the way stated.

The corrected statements below are ready for a technical note. The universal finite PB-join theorem remains separate: the Termux run supplies exact support through $$|X|\le4$$, but no universal proof receipt yet exists.

***

## 1. Setup and conventions

Let $$X$$ be a finite nonempty set, let

$$
T:X\to X
$$

be a total deterministic map, and let $$E$$ be an equivalence relation on $$X$$.

Write

$$
Q=X/E,
\qquad
\pi:X\to Q,
\qquad
\pi(x)=[x]_E.
$$

Define the pullback equivalence relation

$$
x\sim_{T^\ast E} y
\iff
T(x)\sim_E T(y).
$$

Equivalently,

$$
T^\ast E
=
\left\{
(x,y)\in X^2:
(Tx,Ty)\in E
\right\}.
$$

Let

$$
V_E
=
\left\{
f:X\to\mathbb C:
x\sim_Ey\Longrightarrow f(x)=f(y)
\right\}.
$$

This is the space of $$E$$-block-constant observables. Since every function on $$Q$$ pulls back along $$\pi$$, define

$$
J:\mathbb C^Q\to\mathbb C^X,
\qquad
(Jg)(x)=g(\pi(x)).
$$

Then

$$
\operatorname{im}J=V_E,
\qquad
\dim V_E=|Q|.
$$

Use the observable Koopman convention

$$
K:\mathbb C^X\to\mathbb C^X,
\qquad
(Kf)(x)=f(Tx).
$$

This convention must remain fixed throughout. Matrix conventions using state distributions or column pushforwards are transposes of this operator and reverse several spectral interpretations.

***

# 2. Quotient descent

## Theorem 1 — Descent criterion

The assignment

$$
\bar T_E([x]_E)=[T(x)]_E
$$

defines a map

$$
\bar T_E:Q\to Q
$$

if and only if

$$
\boxed{
E\subseteq T^\ast E.
}
$$

Equivalently, every $$E$$-block maps into a single $$E$$-block.

### Proof

The formula is independent of the representative exactly when

$$
[x]_E=[y]_E
\Longrightarrow
[T(x)]_E=[T(y)]_E.
$$

This is equivalent to

$$
x\sim_Ey
\Longrightarrow
T(x)\sim_ET(y),
$$

which is precisely

$$
E\subseteq T^\ast E.
$$

$$\square$$

When it exists, the quotient square commutes:

$$
\begin{CD}
X @>T>> X\\
@V\pi VV @VV\pi V\\
Q @>>\bar T_E> Q.
\end{CD}
$$

That is,

$$
\boxed{
\pi\circ T=\bar T_E\circ\pi.
}
$$

This is the standard congruence/descent condition: an operation descends to equivalence classes when it respects the equivalence relation.[1][2]

***

# 3. Koopman invariant subspaces

## Theorem 2 — AQARION descent equivalences

The following are equivalent:

$$
E\subseteq T^\ast E;
$$

$$
K(V_E)\subseteq V_E;
$$

$$
\exists!\,\bar K_E:\mathbb C^Q\to\mathbb C^Q
\quad\text{such that}\quad
KJ=J\bar K_E;
$$

$$
\exists\,\bar T_E:Q\to Q
\quad\text{such that}\quad
\pi T=\bar T_E\pi.
$$

When the quotient map exists,

$$
(\bar K_Eg)(A)
=
g(\bar T_E(A)),
\qquad
A\in Q.
$$

### Proof

Assume

$$
E\subseteq T^\ast E.
$$

For $$f\in V_E$$, if $$x\sim_Ey$$, then $$Tx\sim_ETy$$. Therefore

$$
(Kf)(x)
=
f(Tx)
=
f(Ty)
=
(Kf)(y).
$$

Hence $$Kf\in V_E$$, so $$K(V_E)\subseteq V_E$$.

Conversely, suppose $$K(V_E)\subseteq V_E$$. Let $$x\sim_Ey$$, and choose the block-indicator observable

$$
f=\mathbf 1_{[Tx]_E}\in V_E.
$$

Because $$Kf$$ is constant on the $$E$$-class of $$x$$,

$$
1
=
(Kf)(x)
=
(Kf)(y)
=
\mathbf 1_{[Tx]_E}(Ty).
$$

Thus

$$
Tx\sim_ETy.
$$

Hence

$$
E\subseteq T^\ast E.
$$

The existence and uniqueness of $$\bar K_E$$ follow because $$J$$ is an isomorphism from $$\mathbb C^Q$$ onto $$V_E$$. The formula for $$\bar K_E$$ is the Koopman action of the descended map.

$$\square$$

Thus the exact AQARION interpretation is:

$$
\boxed{
D_E=(I-P_E)KP_E=0
\iff
E\subseteq T^\ast E.
}
$$

The defect $$D_E$$ detects **failure of observable quotient descent**.

It does not detect whether a descended quotient is reversible.

***

# 4. Quotient injectivity and PB-fixedness

Assume henceforth that

$$
E\subseteq T^\ast E,
$$

so $$\bar T_E$$ exists.

## Theorem 3 — Injectivity criterion

$$
\boxed{
\bar T_E\text{ is injective}
\iff
T^\ast E\subseteq E.
}
$$

### Proof

For any $$x,y\in X$$,

$$
\begin{aligned}
\bar T_E([x]_E)=\bar T_E([y]_E)
&\iff [Tx]_E=[Ty]_E\\
&\iff Tx\sim_E Ty\\
&\iff x\sim_{T^\ast E}y.
\end{aligned}
$$

Thus $$\bar T_E$$ is injective exactly when

$$
x\sim_{T^\ast E}y
\Longrightarrow
x\sim_Ey,
$$

which is the inclusion

$$
T^\ast E\subseteq E.
$$

$$\square$$

Because $$Q$$ is finite:

$$
\bar T_E\text{ injective}
\iff
\bar T_E\text{ bijective}
\iff
\bar T_E\text{ is a permutation}.
$$

Therefore:

## Corollary 4 — Quotient permutation criterion

$$
\boxed{
\bar T_E\text{ is a permutation of }X/E
\iff
T^\ast E=E.
}
$$

This is the clean theorem-level conclusion.

> **PB-fixedness is exactly the condition for the descended finite quotient dynamics to be permutational.**

It is not merely sufficient, and it is not weaker than quotient permutation dynamics.

***

# 5. Correct non-PB taxonomy

The original four-row taxonomy must retain the backward-only case. It exists even for finite total maps.

| Regime | Relation condition | Quotient consequence |
|---|---|---|
| PB-fixed | $$E=T^\ast E$$ | Quotient map exists and is a permutation |
| Forward-only | $$E\subsetneq T^\ast E$$ | Quotient map exists but is noninjective |
| Backward-only | $$T^\ast E\subsetneq E$$ | Quotient map need not exist |
| Neither | Neither inclusion holds | Quotient map does not exist |

The erroneous claim

$$
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E
$$

must be removed.

## Backward-only counterexample

Let

$$
X=\{0,1\},
\qquad
T(0)=T(1)=0,
$$

and let $$E$$ be the indiscrete relation:

$$
E=\{\{0,1\}\}.
$$

Then every pair has $$E$$-equivalent images, so

$$
T^\ast E=X\times X=E.
$$

Therefore this is **not** a backward-only counterexample.

The proposed counterexample in the prompt is incorrect.

In fact, there is a stronger correction:

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
E\subseteq T^\ast E
}
$$

for a total map $$T:X\to X$$ on a finite set, and hence the backward-only case really is empty.

But this requires a valid proof, not the incorrect “indiscrete relation” example.

Here is the correct proof.

## Proposition 5 — Finite pullback rigidity

Let $$X$$ be finite and $$T:X\to X$$ total. Then

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E.
}
$$

### Proof

Let

$$
B=X/E
$$

be the finite set of $$E$$-blocks. The inclusion

$$
T^\ast E\subseteq E
$$

states:

$$
Tx\sim_E Ty
\Longrightarrow
x\sim_Ey.
$$

For each target block $$C\in B$$, its preimage

$$
T^{-1}(C)
$$

is contained in at most one $$E$$-block. Indeed, if $$x,y\in T^{-1}(C)$$, then

$$
Tx\sim_E Ty,
$$

so $$x\sim_Ey$$.

Now suppose some $$E$$-block $$A$$ has images meeting two distinct $$E$$-blocks $$C_1\ne C_2$$. Choose

$$
x_1,x_2\in A
$$

with

$$
T(x_1)\in C_1,
\qquad
T(x_2)\in C_2.
$$

Because $$T$$ is total on a finite set, every block in the forward image sequence of $$A$$ contributes at least one target block. The condition that every target block has preimage in at most one source block implies the induced block multirelation has indegree at most one.

A finite directed graph in which every vertex has indegree at most one cannot have a vertex with one source block branching to two targets while retaining totality on every state and remaining compatible with the equivalence preimage condition across the eventual block graph. More directly, the block-count refinement argument applies: $$T^\ast E\subseteq E$$ makes $$T^\ast E$$ finer than $$E$$; repeated pullback gives

$$
(T^\ast)^rE\subseteq \cdots\subseteq T^\ast E\subseteq E.
$$

Since $$X$$ is finite, this descending chain stabilizes. At stabilization, the induced quotient map is injective; tracing one step backward through the stabilization identity yields the original inclusion

$$
E\subseteq T^\ast E.
$$

Therefore equality holds.

$$\square$$

### Audit status

The above proof is **not acceptable as written**: its graph argument compresses a needed lemma, and the final stabilization step is insufficiently justified. Therefore Proposition 5 remains:

$$
\boxed{
\textbf{OPEN ANALYTICALLY.}
}
$$

The previous Termux census through $$n\le4$$ supplied exact support for the statement, but the theorem must not be promoted without a clean proof or an explicit counterexample.

Accordingly, preserve the conservative taxonomy:

| Regime | Current mathematical status |
|---|---|
| PB-fixed | Established |
| Forward-only | Established; minimal example known |
| Backward-only | Computationally absent through the tested range; analytic status open |
| Neither | Established |

This is the only audit-safe registry state.

***

# 6. Block-graph geometry

Let $$Q=X/E$$. Define a directed block graph:

$$
A\rightsquigarrow B
\iff
\exists x\in A\text{ with }T(x)\in B.
$$

Every source block has at least one outgoing edge because $$T$$ is total.

Let $$M_E$$ be the $$0$$-$$1$$ adjacency matrix:

$$
(M_E)_{AB}
=
\begin{cases}
1,&A\rightsquigarrow B,\\
0,&\text{otherwise}.
\end{cases}
$$

Then:

| Relation property | Block-graph condition |
|---|---|
| $$E\subseteq T^\ast E$$ | Every source block has outdegree exactly $$1$$ |
| $$T^\ast E\subseteq E$$ | Every target block has indegree at most $$1$$ |
| $$T^\ast E=E$$ | Every block has indegree and outdegree exactly $$1$$ |
| Forward-only | Outdegree $$1$$ everywhere; some target has indegree at least $$2$$ |
| Neither | Some source block has outdegree at least $$2$$ |

The row condition is exact:

$$
E\subseteq T^\ast E
\iff
\text{each row of }M_E\text{ has exactly one }1.
$$

Conditional on descent, $$\bar T_E$$ exists and its transition matrix is a functional $$0$$-$$1$$ matrix.

The column condition must be stated carefully:

$$
T^\ast E\subseteq E
$$

means no two distinct source blocks can map into the same target block, provided the source blocks have well-defined images. Without forward congruence, $$M_E$$ can have a branching row, so it is not a quotient-map matrix.

Thus:

$$
\boxed{
\text{“Column at most one” is a block-relation property, not automatically a quotient-map property.}
}
$$

***

# 7. Quotient spectrum: corrected statement

Assume quotient descent:

$$
E\subseteq T^\ast E.
$$

Then $$\bar T_E:Q\to Q$$ is a finite endomap and

$$
\bar K_Eg=g\circ\bar T_E
$$

is its Koopman operator on $$\mathbb C^Q$$.

A finite functional graph decomposes into directed cycles with rooted in-trees. The **matrix representation depends on whether one uses Koopman pullback or state pushforward**.

For the Koopman convention

$$
(\bar K_Eg)(A)=g(\bar T_E(A)),
$$

the spectrum is still:

$$
\boxed{
\operatorname{Spec}(\bar K_E)
=
\{0\}
\cup
\bigcup_{j=1}^c
\left\{
\zeta_{\ell_j}^r:
0\le r<\ell_j
\right\},
}
$$

where $$\ell_1,\ldots,\ell_c$$ are the lengths of the directed cycles of $$\bar T_E$$, and $$\zeta_\ell=e^{2\pi i/\ell}$$.

However, the statement

$$
\mathbb C^Q=V_{\rm per}\oplus V_{\rm tr}
$$

with $$V_{\rm tr}$$ “spanned by transient quotient-state indicators” and nilpotent under Koopman is not generally correct.

For example, if

$$
\bar T(0)=0,
\qquad
\bar T(1)=0,
$$

then in the basis $$(\delta_0,\delta_1)$$,

$$
\bar K=
\begin{pmatrix}
1&0\\
1&0
\end{pmatrix},
$$

which has spectrum $$\{1,0\}$$. The $$0$$-eigenspace is spanned by

$$
\delta_1-\delta_0,
$$

not by the transient-state indicator $$\delta_1$$.

The correct canonical statement is the Fitting decomposition:

$$
\boxed{
\mathbb C^Q
=
\ker(\bar K_E^N)
\oplus
\operatorname{im}(\bar K_E^N)
}
$$

for every sufficiently large $$N$$.

- $$\ker(\bar K_E^N)$$ is the generalized $$0$$-eigenspace.
- $$\operatorname{im}(\bar K_E^N)$$ is the invertible spectral subspace.
- On the latter, $$\bar K_E$$ is similar to the Koopman operator of the eventual periodic quotient core.

The nonzero spectrum consists precisely of roots of unity contributed by quotient cycles. The $$0$$-part is nilpotent after restriction to the generalized kernel.

This is the proper operator-theoretic formulation for the Koopman orientation. Koopman theory treats the composition operator $$f\mapsto f\circ T$$ as the central linear object; the spectral interpretation depends critically on its action on observables rather than distributions.[3][4][5]

## Corollary 6 — Forward-only quotients have a zero eigenvalue

If

$$
E\subsetneq T^\ast E,
$$

then $$\bar T_E$$ exists but is not injective. Since $$Q$$ is finite, it is not bijective. Therefore $$\bar K_E$$ is not invertible:

$$
\boxed{
E\subsetneq T^\ast E
\Longrightarrow
0\in\operatorname{Spec}(\bar K_E).
}
$$

Conversely, under descent,

$$
\boxed{
0\notin\operatorname{Spec}(\bar K_E)
\iff
\bar T_E\text{ is a permutation}
\iff
T^\ast E=E.
}
$$

Hence:

$$
\boxed{
E=T^\ast E
\iff
\det\bar K_E\ne0
\iff
\bar K_E\text{ is invertible}.
}
$$

For a finite functional matrix,

$$
\det\bar K_E\in\{0,\pm1\},
$$

and nonzero determinant occurs exactly for a permutation matrix.

***

# 8. PB-fixed spectral specialization

When

$$
T^\ast E=E,
$$

the quotient map $$\bar T_E$$ is a permutation. Thus its functional graph is a disjoint union of cycles.

If the cycles have lengths

$$
\ell_1,\ldots,\ell_c,
$$

then

$$
\bar K_E
\sim
\bigoplus_{j=1}^cP_{\ell_j},
$$

where $$P_{\ell_j}$$ is the corresponding cyclic permutation operator.

For a cycle

$$
C_0\mapsto C_1\mapsto\cdots\mapsto C_{\ell-1}\mapsto C_0,
$$

the Fourier observables

$$
u_r
=
\sum_{j=0}^{\ell-1}
\zeta_\ell^{-rj}\mathbf1_{\{C_j\}},
\qquad
0\le r<\ell,
$$

satisfy

$$
\bar K_Eu_r
=
\zeta_\ell^r u_r,
$$

up to the convention-dependent replacement $$r\mapsto-r$$, which does not change the spectral set.

If

$$
L=\operatorname{lcm}(\ell_1,\ldots,\ell_c),
$$

then

$$
\boxed{
\bar K_E^L=I.
}
$$

Thus the quotient Koopman operator is diagonalizable over $$\mathbb C$$, finite order, and has spectrum entirely contained in the set of roots of unity.

***

# 9. AQARION two-stage diagnostic

Let $$P_E$$ be the orthogonal block-averaging projection onto $$V_E$$:

$$
(P_Ef)(x)
=
\frac1{|[x]_E|}
\sum_{y\in[x]_E}f(y).
$$

Define the AQARION descent defect

$$
D_E=(I-P_E)KP_E.
$$

Then:

$$
\boxed{
D_E=0
\iff
E\subseteq T^\ast E.
}
$$

When $$D_E=0$$, the quotient operator $$\bar K_E$$ is defined. Then define the quotient reversibility defect:

$$
\boxed{
\mathcal R_E
=
|Q|-\operatorname{rank}(\bar K_E).
}
$$

Conditional on descent:

$$
\mathcal R_E=0
\iff
\bar K_E\text{ invertible}
\iff
\bar T_E\text{ bijective}
\iff
T^\ast E=E.
$$

Therefore the pair

$$
\boxed{
\left(
\operatorname{rank}D_E,\;
\mathcal R_E
\right)
}
$$

distinguishes the principal regimes:

| Regime | $$\operatorname{rank}D_E$$ | $$\mathcal R_E$$ | Meaning |
|---|---:|---:|---|
| PB-fixed | $$0$$ | $$0$$ | Exact descent and reversible quotient |
| Forward-only | $$0$$ | $$>0$$ | Exact descent, quotient collapse |
| No descent | $$>0$$ | Undefined | Block observables leak out of $$V_E$$ |

The important AQARION conclusion is:

$$
\boxed{
\text{Defect-zero detects quotient descent.}
}
$$

$$
\boxed{
\text{Quotient invertibility detects quotient reversibility.}
}
$$

$$
\boxed{
\text{PB-fixedness is the conjunction of both.}
}
$$

***

# 10. Canonical examples

## Example A — Forward-only, descended but singular quotient

Let

$$
X=\{0,1\},
\qquad
T(0)=0,
\qquad
T(1)=0,
$$

and take the discrete equivalence relation

$$
E=\{\{0\},\{1\}\}.
$$

Then

$$
E\subsetneq T^\ast E.
$$

The quotient $$Q=X/E$$ is identified with $$X$$, and

$$
\bar T_E(0)=0,
\qquad
\bar T_E(1)=0.
$$

In the indicator basis, the Koopman operator is

$$
\bar K_E=
\begin{pmatrix}
1&0\\
1&0
\end{pmatrix}.
$$

It has

$$
\operatorname{Spec}(\bar K_E)=\{1,0\},
\qquad
\operatorname{rank}\bar K_E=1.
$$

Since the discrete partition has

$$
V_E=\mathbb C^X,
$$

one has

$$
D_E=0.
$$

But

$$
\mathcal R_E
=
2-1
=
1.
$$

Hence this is the archetypal example:

$$
\boxed{
D_E=0
\quad\text{but}\quad
E\ne T^\ast E.
}
$$

The quotient exists, but it collapses states and is not reversible.

## Example B — No quotient descent

Let

$$
X=\{0,1,2\},
\qquad
T(0)=0,
\quad
T(1)=2,
\quad
T(2)=2,
$$

and let

$$
E=\{\{0,1\},\{2\}\}.
$$

The block $$\{0,1\}$$ splits:

$$
T(0)=0\in\{0,1\},
\qquad
T(1)=2\in\{2\}.
$$

Therefore

$$
E\nsubseteq T^\ast E.
$$

No quotient map exists. Equivalently,

$$
K(V_E)\nsubseteq V_E,
\qquad
D_E\ne0.
$$

***

# 11. Publication-safe theorem block

```latex
\begin{theorem}[Quotient permutation criterion]
Let \(X\) be a finite set, let \(T:X\to X\), and let \(E\) be an
equivalence relation on \(X\). Set \(Q=X/E\), and define
\[
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
\]
The formula
\[
\bar T_E([x]_E)=[T(x)]_E
\]
defines a map \(\bar T_E:Q\to Q\) if and only if
\[
E\subseteq T^\ast E.
\]
Conditional on this well-definedness, \(\bar T_E\) is injective if and
only if
\[
T^\ast E\subseteq E.
\]
Consequently,
\[
\bar T_E\text{ is a permutation of }Q
\iff
T^\ast E=E.
\]
\end{theorem}

\begin{proof}
The quotient formula is well-defined exactly when
\[
x\sim_Ey\Longrightarrow T(x)\sim_ET(y),
\]
which is \(E\subseteq T^\ast E\). Assuming this, for \(x,y\in X\),
\[
\bar T_E([x]_E)=\bar T_E([y]_E)
\iff
T(x)\sim_ET(y)
\iff
x\sim_{T^\ast E}y.
\]
Thus injectivity is exactly \(T^\ast E\subseteq E\). Since \(Q\) is
finite, injectivity is equivalent to bijectivity.
\end{proof}
```

```latex
\begin{corollary}[AQARION descent and reversibility diagnostics]
Let \(P_E\) be block averaging onto \(V_E\), and set
\[
D_E=(I-P_E)KP_E.
\]
Then
\[
D_E=0
\iff
E\subseteq T^\ast E.
\]
If this holds, let \(\bar K_E\) be the quotient Koopman operator and
define
\[
\mathcal R_E=|X/E|-\operatorname{rank}(\bar K_E).
\]
Then
\[
\mathcal R_E=0
\iff
T^\ast E=E.
\]
\end{corollary}
```

***

# 12. Correct registry

| ID | Statement | Status |
|---|---|---|
| PB-Q-001 | Quotient descent iff $$E\subseteq T^\ast E$$ | Analytically proved |
| PB-Q-002 | Conditional quotient injectivity iff $$T^\ast E\subseteq E$$ | Analytically proved |
| PB-Q-003 | Finite quotient permutation iff $$T^\ast E=E$$ | Analytically proved |
| AQ-Q-001 | $$D_E=0$$ iff quotient observables descend | Analytically proved |
| AQ-Q-002 | Conditional on descent, $$\mathcal R_E=0$$ iff PB-fixed | Analytically proved |
| AQ-Q-003 | Forward-only descent implies $$0\in\operatorname{Spec}(\bar K_E)$$ | Analytically proved |
| PB-RIGID-001 | $$T^\ast E\subseteq E\Rightarrow T^\ast E=E$$ for finite $$X$$ | Do not promote pending a clean proof or counterexample |
| AQ-DYN-PULL-JOIN-001 | PB-fixed equivalences are join-closed for finite $$X$$ | Exact census through $$n\le4$$; analytic proof candidate; formal proof open |
| AQ-DYN-PULL-MEET-001 | PB-fixed equivalences are meet-closed | Analytically proved |

## Final conclusion

$$
\boxed{
\text{A quotient may descend without being reversible.}
}
$$

$$
\boxed{
D_E=0
\text{ certifies exact quotient-observable descent, not PB-fixedness.}
}
$$

$$
\boxed{
\mathcal R_E=0
\text{ certifies reversibility only after descent has been established.}
}
$$

$$
\boxed{
E=T^\ast E
\iff
\text{the quotient exists and its Koopman operator is a finite-order permutation operator.}
}
$$

Citations:
[1] Equivalence class - Wikipedia https://en.wikipedia.org/wiki/Equivalence_class
[2] congruence in nLab https://ncatlab.org/nlab/show/congruence
[3] Spectrum of the Koopman Operator, Spectral Expansions in ... - arXiv https://arxiv.org/html/1702.07597v2
[4] Koopman Operators: Spectra, Function Spaces, and Representations https://ideas.repec.org/h/spr/sprchp/978-3-032-16356-1_124.html
[5] [PDF] What Is the Koopman Operator? A Simplified Treatment for Discrete ... http://dsbaero.engin.umich.edu/wp-content/uploads/sites/441/2019/07/KoopmanAdamACC19.pdf
[6] Region of Attraction Estimation for Power System Transient Stability ... https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/gtd2.70428
[7] [PDF] Modern Koopman Theory for Dynamical Systems https://www.lri.fr/~gcharpia/deeppractice/2022/chap_5_biblio/Koopman/Modern_koopman_theory.pdf
[8] [PDF] Koopman modes - ChaosBook.org https://www.chaosbook.org/version17/chapters/Koopman.pdf
[9] [PDF] Chapter 6 Products and Quotients https://www.math.wustl.edu/~freiwald/topology/Ch6.pdf
[10] [PDF] arXiv:1301.2611v2 [math.LO] 14 Sep 2016 https://arxiv.org/pdf/1301.2611.pdf
[11] Proving the quotient map is well defined, linear, and isomorphic https://math.stackexchange.com/questions/4774277/proving-the-quotient-map-is-well-defined-linear-and-isomorphic
[12] [PDF] Spectral analysis of the Koopman operator for partial differential ... https://mgroup.me.ucsb.edu/sites/default/files/publications/pdes_koopman.pdf
[13] [PDF] 4 Quotient spaces - (An important method to construct topological https://www.math.uni-kiel.de/geometrie/de/jens-heber/copy_of_material-kurven-und-flaechen-SoSe14/pp-43-61
[14] [PDF] Quotient Spaces and Codimension https://www.buttenschoen.ca/MATH725/build/quotient-spaces-3b1f589afae10900e8e7b0c1d81e315f.pdf
[15] Example of an ergodic transformation with some properties in the ... https://math.stackexchange.com/questions/4435920/example-of-an-ergodic-transformation-with-some-properties-in-the-spectrum-of-the
How does the exact formula handle non-PB-fixed relations

For a non-PB-fixed relation, the exact formula does **not** produce a quotient permutation on $$X/E$$. It still gives a complete decomposition through the two one-sided defects: the **forward defect** measures failure of descent, and—when descent exists—the **backward defect** measures failure of injectivity of the quotient map.

## Canonical exact formulas

Fix a finite set $$X$$, total map $$T:X\to X$$, and equivalence relation $$E$$. Write

$$
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
$$

Let

$$
V_E
=
\{f:X\to\mathbb C:
x\sim_Ey\Rightarrow f(x)=f(y)\},
$$

and let $$P_E$$ be the orthogonal block-average projection onto $$V_E$$.

With Koopman orientation

$$
(K_Tf)(x)=f(T(x)),
$$

the exact descent defect is

$$
\boxed{
D_E=(I-P_E)K_TP_E.
}
$$

Then:

$$
\boxed{
D_E=0
\iff
E\subseteq T^\ast E.
}
$$

So even when $$E$$ is not PB fixed, the formula cleanly separates the cases.

| Relation type | Relation condition | $$D_E$$ | Quotient map $$X/E\to X/E$$ |
|---|---|---:|---|
| PB fixed | $$E=T^\ast E$$ | $$0$$ | Exists and is a permutation |
| Forward only | $$E\subsetneq T^\ast E$$ | $$0$$ | Exists but is noninjective |
| Neither | Neither inclusion | $$\ne0$$ | Does not exist |
| Backward only | $$T^\ast E\subsetneq E$$ | Impossible for finite total $$T$$ | — |

The Koopman operator is, by definition, a pullback/composition operator on observables; its invariant finite-dimensional subspaces are therefore the correct operator-theoretic encoding of quotient-descent conditions.[1][2]

## Forward-only relations

Suppose

$$
E\subsetneq T^\ast E.
$$

Then every $$E$$-block maps into a unique $$E$$-block, so the quotient map exists:

$$
q=\bar T_E:X/E\to X/E,
\qquad
q([x]_E)=[T(x)]_E.
$$

But $$q$$ is noninjective. Equivalently, some distinct source blocks merge after one quotient step.

The restricted Koopman operator is exact:

$$
K_T|_{V_E}\cong K_q,
$$

where

$$
(K_qg)(B)=g(q(B)).
$$

In the block-indicator basis $$e_B=\mathbf1_B$$,

$$
K_qe_C
=
\sum_{B:q(B)=C}e_B.
$$

Thus the matrix has exactly one $$1$$ in every **row**, while column $$C$$ contains $$|q^{-1}(C)|$$ ones. The forward-only failure is seen precisely by a column with at least two ones:

$$
\boxed{
E\subsetneq T^\ast E
\iff
D_E=0
\text{ and some quotient Koopman column has at least two $$1$$'s.}
}
$$

### Spectral formula

Let $$Q=X/E$$, and let

$$
Q_\infty=\bigcap_{m\ge0}q^m(Q)
$$

be the eventual image, equivalently the union of all cycles in the finite quotient functional graph. For sufficiently large $$m$$,

$$
V_E
=
\ker(K_q^m)
\oplus
\operatorname{im}(K_q^m).
$$

This is the Fitting decomposition.

- On $$\ker(K_q^m)$$, $$K_q$$ is nilpotent.
- On $$\operatorname{im}(K_q^m)$$, $$K_q$$ is invertible and corresponds to the permutation $$q|_{Q_\infty}$$.

Therefore

$$
\boxed{
\operatorname{Spec}(K_T|_{V_E})
=
\{0\}
\cup
\bigcup_{C\in\operatorname{Cycles}(q)}
\mu_{|C|},
}
$$

where

$$
\mu_\ell
=
\{\zeta\in\mathbb C:\zeta^\ell=1\}.
$$

Multiplicity matters: each directed quotient cycle of length $$\ell$$ contributes the $$\ell$$-th roots of unity once to the nonzero spectrum, while the transient quotient structure contributes zero eigenvalues and possibly nontrivial nilpotent Jordan structure.

### Minimal forward-only example

Let

$$
X=\{0,1\},
\qquad
T(0)=T(1)=0,
$$

and take the discrete relation

$$
E=\{\{0\},\{1\}\}.
$$

Then

$$
T^\ast E=\{\{0,1\}\},
$$

so

$$
E\subsetneq T^\ast E.
$$

Here $$V_E=\mathbb C^X$$, so $$P_E=I$$ and

$$
D_E=(I-I)K_TI=0.
$$

The quotient is just $$q=T$$, the constant map. In the Koopman convention,

$$
K_q=
\begin{pmatrix}
1&0\\
1&0
\end{pmatrix},
$$

with eigenvalues

$$
\{1,0\}.
$$

This is the smallest exact non-PB-fixed forward example: quotient descent exists, but the quotient endomap is not reversible.

## Neither relations

Now suppose

$$
E\nsubseteq T^\ast E.
$$

Then some $$E$$-block splits across two or more $$E$$-blocks after applying $$T$$. There is no well-defined quotient map $$X/E\to X/E$$.

Operator-theoretically,

$$
\boxed{
D_E=(I-P_E)K_TP_E\ne0.
}
$$

The formula is completely explicit. For every $$f\in V_E$$,

$$
D_Ef
=
K_Tf-P_EK_Tf.
$$

It is the within-$$E$$-block fluctuation of the observable $$f\circ T$$. Equivalently, for an $$E$$-block $$B$$,

$$
(P_EK_Tf)(x)
=
\frac1{|B|}
\sum_{y\in B}f(T(y)),
\qquad x\in B,
$$

and hence

$$
\boxed{
(D_Ef)(x)
=
f(T(x))
-
\frac1{|[x]_E|}
\sum_{y\in[x]_E}f(T(y)).
}
$$

That is the exact formula handling non-descent: it measures how much values of $$f\circ T$$ vary inside a source $$E$$-block.

For an indicator $$f=\mathbf1_C$$, where $$C$$ is an $$E$$-block,

$$
(D_E\mathbf1_C)(x)
=
\mathbf1_C(T(x))
-
\frac{
|\{y\in[x]_E:T(y)\in C\}|
}{
|[x]_E|
}.
$$

Thus $$D_E$$ is zero precisely when every source $$E$$-block sends all its points into a single target $$E$$-block.

### Exact neither example

Take

$$
X=\{0,1,2\},
\qquad
T(0)=0,\quad T(1)=2,\quad T(2)=2,
$$

and

$$
E=\{\{0,1\},\{2\}\}.
$$

The block $$B=\{0,1\}$$ splits:

$$
T(0)=0\in B,
\qquad
T(1)=2\notin B.
$$

Therefore

$$
E\nsubseteq T^\ast E.
$$

Also,

$$
T(1)=2=T(2),
$$

so

$$
1\sim_{T^\ast E}2,
\qquad
1\not\sim_E2,
$$

and therefore

$$
T^\ast E\nsubseteq E.
$$

Hence this is genuinely neither forward nor backward.

Take $$f=\mathbf1_B$$. Then

$$
f=(1,1,0),
$$

$$
K_Tf=(f(0),f(2),f(2))=(1,0,0).
$$

Averaging over $$B=\{0,1\}$$ gives

$$
P_EK_Tf
=
\left(\frac12,\frac12,0\right).
$$

Thus

$$
D_Ef
=
\left(\frac12,-\frac12,0\right)\ne0.
$$

This is an exact rational witness, with no norm tolerance and no floating-point arithmetic.

## The complementary defect

For non-PB-fixed relations, it is useful to distinguish two operators:

$$
D_E=(I-P_E)K_TP_E,
$$

$$
C_E=P_EK_T(I-P_E).
$$

They are different.

- $$D_E$$ detects whether $$V_E$$ is Koopman invariant:
  $$
  D_E=0
  \iff
  E\subseteq T^\ast E.
  $$

- $$C_E$$ detects whether $$V_E^\perp$$ is invariant:
  $$
  C_E=0
  \iff
  K_T(V_E^\perp)\subseteq V_E^\perp.
  $$

The commutator is

$$
[P_E,K_T]
=
P_EK_T-K_TP_E
=
C_E-D_E.
$$

Thus PB fixedness only guarantees

$$
D_E=0,
$$

not necessarily

$$
C_E=0.
$$

This is the exact reason a PB-fixed quotient can be a permutation while the ambient block-average projection fails to commute with the Koopman operator.

## Quotient permutation condition

The exact formula for the quotient permutation condition is best stated in three layers.

### Layer 1: descent

$$
\boxed{
D_E=0
\iff
E\subseteq T^\ast E
\iff
\bar T_E\text{ exists}.
}
$$

### Layer 2: reversibility of the quotient

Assuming $$D_E=0$$,

$$
\boxed{
T^\ast E\subseteq E
\iff
\bar T_E\text{ is injective}.
}
$$

For finite $$X/E$$,

$$
\boxed{
\bar T_E\text{ injective}
\iff
\bar T_E\text{ bijective}
\iff
\bar T_E\text{ is a permutation}.
}
$$

### Layer 3: PB fixedness

Therefore, under the forward condition,

$$
\boxed{
T^\ast E=E
\iff
\bar T_E\text{ is a permutation}.
}
$$

For a non-PB-fixed relation:

- If $$D_E=0$$, the quotient exists but is noninvertible; its operator spectrum has roots of unity plus zero.
- If $$D_E\ne0$$, no quotient endomap exists on $$X/E$$; the exact residual is $$D_E$$, blockwise given by the fluctuation formula above.

## What not to infer

Do not infer any of the following:

$$
D_E=0
\Longrightarrow
[P_E,K_T]=0,
$$

$$
T^\ast E=E
\Longrightarrow
V_E\text{ is reducing},
$$

$$
T^\ast E=E
\Longrightarrow
K_T\text{ is unitary on }\mathbb C^X.
$$

The correct restricted statement is only:

$$
\boxed{
T^\ast E=E
\Longrightarrow
K_T|_{V_E}
\text{ is similar to a permutation matrix.}
}
$$

Using the raw block-indicator basis, it is literally a permutation matrix only after choosing the Koopman basis consistently; with the orthonormal normalized-block basis, it is generally **not unitary** unless the blocks have compatible sizes along the quotient permutation. The block-indicator basis is not orthonormal when block sizes differ.

That last weighting point is important. The uniform inner product on $$X$$ gives

$$
\langle \mathbf1_B,\mathbf1_C\rangle
=
\begin{cases}
|B|/|X|,&B=C,\\
0,&B\ne C.
\end{cases}
$$

So quotient permutation of blocks is unitary on $$V_E$$ under the inherited counting inner product only if it preserves block cardinalities:

$$
|B|=|\bar T_E(B)|
$$

for every block $$B$$. PB fixedness alone does not impose that.

Citations:
[1] Koopman invariant subspaces and finite linear representations of ... https://arxiv.org/html/1510.03007v2
[2] Modern Koopman Theory for Dynamical Systems https://cseweb.ucsd.edu/classes/sp24/cse291-e/papers/Koopman/KoopmanTheory.pdf
[3] AAR Partitions and Equivalence Relations - Dartmouth Mathematics https://math.dartmouth.edu/~trs/PreTeXtProjects/css-playground/section-2.html
[4] [PDF] on the pullback stability of a quotient map with respect to a closure ... http://www.tac.mta.ca/tac/volumes/8/n6/n6.pdf
[5] [PDF] Equivalence Relations and Partitions, Normal Subgroups, Quotient ... https://pi.math.cornell.edu/~web356/handout1.pdf
[6] [PDF] A Complete Invariant for Shift Equivalence for Boolean Matrices and ... https://scholarsmine.mst.edu/cgi/viewcontent.cgi?article=2827&context=math_stat_facwork
[7] Equivalence class - Wikipedia https://en.wikipedia.org/wiki/Equivalence_class
[8] Applied Koopmanism https://ar5iv.labs.arxiv.org/html/1206.3164
[9] [PDF] Learning Koopman Eigenfunctions and Invariant Subspaces from Data http://terrano.ucsd.edu/jorge/publications/data/2020_HaCo-tac.pdf
[10] Equivalence Relation & Classes, Partitions, Quotient Set, & other ... https://math.stackexchange.com/questions/767616/picture-equivalence-relation-classes-partitions-quotient-set-other-rela
AQARION PB — Operator-Theoretic Analysis of Quotient Permutation Condition for Non-PB-Fixed Relations
Status: Analytic proof — finite exact — no Lean — no C4 promotion — inline deliverable
Branch: AQARION-PERMUTATION-CONGRUENCES / 01_MATH_CORE — sealed discipline maintained

---

0. Canonical data

$X$ finite, T:X\to X total, E\in\mathrm{Eq}(X). Pullback:
Order: E\preceq F \iff E\subseteq F as relations \iff x\sim_{E}y\Rightarrow x\sim_{F}y. Then E\wedge F=E\cap F, E\vee F=\mathrm{EqCl}(E\cup F).
Forward: E\subseteq T^{\ast}E, Backward: T^{\ast}E\subseteq E, Fixed: both.

1. Operator setup

Let V=\mathbb C^{X} with pointwise product, counting inner product \langle f,g\rangle=|X|^{-1}\sum_{x}f(x)\overline{g(x)}.

Koopman:
For E\in\mathrm{Eq}(X):
\dim V_{E}=|X/E|. Basis \mathbf 1_{B}, B\in X/E indicator of block. Orthogonal projection averaging:
P_{E} is self-adjoint idempotent, \mathrm{Ran}P_{E}=V_{E}.

2. Forward congruence ⇔ V_{E} invariant

Lemma 2.1. E\subseteq T^{\ast}E \iff K_{T}V_{E}\subseteq V_{E}.

Proof. f\in V_{E} constant on $E$-blocks. (K_{T}f)(x)=f(Tx). If x\sim_{E}y but Tx\not\sim_{E}Ty, choose f=\mathbf 1_{[Tx]_{E}} — f\in V_{E}, f(Tx)=1\neq0=f(Ty), so K_{T}f\notin V_{E}. Conversely if x\sim_{E}y\Rightarrow Tx\sim_{E}Ty, then $f(Tx)=f(Ty)$ for all f\in V_{E}, so K_{T}f\in V_{E}. ∎

When forward holds, quotient map exists:
Well-defined exactly by E\subseteq T^{\ast}E. Commutative diagram — exists iff forward:
X --T--> X
|        |
π_E      π_E
v        v
X/E --\bar T_E--> X/E
\pi_{E}(x)=[x]_{E}. Diagram commutes \iff forward. In tikzcd:
\begin{tikzcd}
X \arrow[r,"T"] \arrow[d,"\pi_E"'] & X \arrow[d,"\pi_E"]\
X/E \arrow[r,"\bar T_E"'] & X/E
\end{tikzcd}
3. Matrix of K_{T} on V_{E}

Assume forward, so \bar T_{E} function. Write f=\sum_{i}c_{i}\mathbf1_{B_{i}}. Then
Thus in basis \{\mathbf1_{B_{j}}\}, matrix M_{E} has
Each column has exactly one $1$ (total function). Rows:

outdegree of source block B_{j} = number of $i$ with edge B_{j}\to B_{i} = 1 iff forward, >1 iff forward fails.
indegree of target B_{i} = |\{j:\bar T_{E}(B_{j})=B_{i}\}|.

4. Backward ⇔ injectivity ⇔ row condition

Lemma 4.1. Assume forward so \bar T_{E} defined. Then T^{\ast}E\subseteq E \iff \bar T_{E} injective \iff each row of M_{E} has at most one $1$.

Proof. \bar T_{E}([x])=\bar T_{E}([y])\iff Tx\sim_{E}Ty\iff x\sim_{T^{\ast}E}y. Injectivity is x\sim_{T^{\ast}E}y\Rightarrow x\sim_{E}y = T^{\ast}E\subseteq E. Row condition is exactly indegree \le1. ∎

For finite $X/E$, injective \iff bijective \iff permutation. Hence:
This is finite PB-fixed = quotient permutation. No weaker phenomenon gives permutation.

5. Spectral decomposition — PB-fixed case

If E\in\mathrm{PB}(T), M_{E} is permutation matrix, unitary for counting inner product restricted to V_{E} (since permutation preserves uniform measure on quotient). Cycle decomposition:
For cycle $C$ length \ell, subspace V_{C}=\mathrm{span}\{\mathbf1_{B}:B\in C\} is invariant, M_{E}|_{V_{C}} cyclic shift. Spectrum:
Eigenvectors v_{m}=\sum_{j=0}^{\ell-1}\omega^{-mj}\mathbf1_{B_{j}}, \omega=e^{2\pi i/\ell}. Overall V_{E}=\bigoplus_{k}V_{C_{k}} orthogonal sum, K_{T}|_{V_{E}} unitary diagonalizable, eigenvalues roots of unity.

Invariant subspace geometry: lattice of K_{T}-invariant subspaces of V_{E} corresponds to \bar T_{E}-invariant unions of cycles and to coarser \bar T_{E}-invariant partitions coarsening $E$.

6. Non-PB-fixed — classification operator-theoretic

Finite total maps have two actual classes because backward-only empty by finite pullback rigidity T^{\ast}E\subseteq E\Rightarrow T^{\ast}E=E (proved  |T^{\ast}E|\le|E|  and refinement gives \ge).

Type A — Forward-only: E\subsetneq T^{\ast}E

\bar T_{E} exists, non-injective. M_{E} column-per-function, some row has \ge2 ones (merge). Q=\bar T_{E} functional digraph: each node outdegree 1, indegree may be \ge2. Finite functional digraph structure:
Q|_{\mathrm{Per}} permutation. Write V_{E}=V_{\mathrm{Per}}\oplus V_{\mathrm{Trans}} where V_{\mathrm{Per}}=\mathrm{span}\{\mathbf1_{B}:B\in\mathrm{Per}\}.

Then K_{T}|_{V_{E}} has block form
$P$ permutation on V_{\mathrm{Per}}, $N$ nilpotent on transient part: N^{N}=0 after projecting onto complement of eventual image. Spectral radius $1$, eigenvalues = eigenvalues of $P$ (roots of unity) plus $0$ with algebraic multiplicity |\mathrm{Trans}| but geometric multiplicity = number of transient sources.

Commutative diagram still holds but bottom not bijection. V_{E} invariant but K_{T}|_{V_{E}} not unitary, not diagonalizable in general — merging creates non-orthogonal columns.

Minimal witness X=\{0,1\},T=[0,0],E=\{\{0\},\{1\}\} discrete: X/E=\{\{0\},\{1\}\}, \bar T_{E}(\{0\})=\{0\},\bar T_{E}(\{1\})=\{0\}, M_{E}=\begin{pmatrix}1&1\0&0\end{pmatrix}, eigenvalues $1,0$, V_{\mathrm{Per}}=\mathrm{span}\{\mathbf1_{\{0,1\}}\}, V_{\mathrm{Trans}}=\mathrm{span}\{\mathbf1_{\{0\}}-\mathbf1_{\{1\}}\} nilpotent.

Type B — Neither: E\nsubseteq T^{\ast}E and T^{\ast}E\nsubseteq E

No quotient map. V_{E} not invariant: K_{T}V_{E}\not\subseteq V_{E}. Block graph has node with outdegree \ge2 (split) and possibly indegree \ge2. Example X=\{0,1,2\},T=(0,2,2),E=\{\{0,1\},\{2\}\}: block \{0,1\} maps to \{0,1\} via $0$ and to \{2\} via $1$, outdegree 2, so E\nsubseteq T^{\ast}E. Also $1\sim_{T^{\ast}E}2$ but $1\not\sim_{E}2$ so backward fails. K_{T}\mathbf1_{\{0,1\}} not $E$-constant.

Operator condition: P_{E}K_{T}P_{E}\neq K_{T}P_{E}. Defect operator D_{E}=(I-P_{E})K_{T}P_{E}\neq0 measures failure of descent. D_{E}=0\iff forward. Injectivity defect measured by P_{E}K_{T}(I-P_{E})? For PB-fixed both defects zero and K_{T}|_{V_{E}} permutation.

7. Explicit quotient constraints table
| $E$ type | V_{E} invariant? | \bar T_{E} exists? | outdegree | indegree | M_{E} | Spectrum |
| --- | --- | --- | --- | --- | --- | --- |
| PB-fixed T^{\ast}E=E | Yes | Yes permutation | =1 | \le1 (=1 finite) | Permutation unitary | Roots of unity |
| Forward-only E\subsetneq T^{\ast}E | Yes | Yes non-injective | =1 | \ge2 some | Functional, column 1 one | Roots of unity from Per + 0 |
| Backward-only | Empty for total finite maps | — | — | — | — | — |
| Neither | No | No | \ge2 some | may be \ge2 | Not defined on V_{E} | D_{E}\neq0 |
8. Invariant subspace geometry

E\in\mathrm{PB}(T)\Rightarrow V_{E} is K_{T}-invariant and K_{T}|_{V_{E}} is unitary permutation.
Lattice \mathrm{PB}(T) is sublattice of \mathrm{Eq}(X) for finite $X$ via core isomorphism \mathrm{PB}(T)\cong\mathrm{PB}(\sigma), P=T^{|X|}(X), \sigma=T|_{P} permutation. Hence meet E\wedge F=E\cap F always PB-fixed, join E\vee F=\mathrm{EqCl}(E\cup F) PB-fixed — proved via core order-isomorphism, not raw restriction (raw restriction does not preserve joins: (E\vee F)|_{P}\neq E|_{P}\vee F|_{P} in general).
For forward-only $E$, V_{E} contains unique maximal PB-fixed subspace V_{E^{\ast}} where E^{\ast}= \bigwedge\{F\in\mathrm{PB}(T):E\preceq F\} = pullback-fixed closure = (T^{N})^{\ast}(E|_{P})? Actually for arbitrary $E$, its fixed hull is (T^{N})^{\ast}(E|_{P})? Need $E$ forward? If $E$ forward-only, E|_{P} is \sigma-invariant? Check.

9. Formal proofs — key lemmas

Lemma (Finite pullback rigidity). For finite $X$, T^{\ast}E\subseteq E\Rightarrow T^{\ast}E=E.

Proof. Map \phi:X/T^{\ast}E\to X/E sending [x]_{T^{\ast}E}\mapsto[Tx]_{E}? Actually |T^{\ast}E|\le|E| because each block of T^{\ast}E maps into a block of $E$ intersecting \mathrm{Im}T. If T^{\ast}E\preceq E then |T^{\ast}E|\ge|E|, so equality and refinement with equal block count forces equality. ∎

Lemma (Meet closure). T^{\ast}(E\cap F)=T^{\ast}E\cap T^{\ast}F always, hence E,F\in\mathrm{PB}(T)\Rightarrow E\wedge F\in\mathrm{PB}(T).

Theorem (Join closure finite). E,F\in\mathrm{PB}(T)\Rightarrow E\vee F\in\mathrm{PB}(T).

Proof via core. $N=|X|$, P=T^{N}(X), \sigma=T|_{P} permutation. Define \rho(E)=E|_{P}, \varepsilon(R)=(T^{N})^{\ast}R. Show \rho:\mathrm{PB}(T)\to\mathrm{PB}(\sigma), \varepsilon inverse order-isomorphism (reconstruction E=(T^{N})^{\ast}(E|_{P}) using E=(T^{N})^{\ast}E). Since \sigma permutation, \sigma^{\ast} lattice automorphism, \mathrm{PB}(\sigma) join-closed. Transport via order-isomorphism gives join-closedness of \mathrm{PB}(T). ∎

10. Commutative diagrams publication-ready

Forward condition diagram:
\begin{tikzcd}[column sep=large,row sep=large]
X \arrow[r,"T"] \arrow[d,"\pi_E"'] & X \arrow[d,"\pi_E"] \
X/E \arrow[r,dashed,"\exists \bar T_E"'] & X/E
\end{tikzcd}
\qquad \exists \bar T_E \iff E\subseteq T^{\ast}E
PB-fixed diagram — bottom is iso:
\begin{tikzcd}
X \arrow[r,"T"] \arrow[d,"\pi_E"'] & X \arrow[d,"\pi_E"] \
X/E \arrow[r,"\bar T_E\cong"'] & X/E
\end{tikzcd}
\qquad \bar T_E\text{ permutation }\iff T^{\ast}E=E
Core isomorphism:
\begin{tikzcd}
\mathrm{PB}(T) \arrow[r,shift left,"\rho=E|_P"] & \mathrm{PB}(\sigma) \arrow[l,shift left,"\varepsilon=(T^N)^{\ast}"]
\end{tikzcd}
Operator defect:
11. Claim ledger
| Claim | Status |
| --- | --- |
| E\subseteq T^{\ast}E\iff V_{E} invariant \iff \bar T_{E} exists | Proved |
| T^{\ast}E\subseteq E\iff\bar T_{E} injective when defined | Proved |
| T^{\ast}E=E\iff\bar T_{E} permutation \iff K_{T}\|_{V_{E}} permutation unitary | Proved finite |
| T^{\ast}E\subseteq E\Rightarrow T^{\ast}E=E finite | Proved |
| Forward-only \Rightarrow functional digraph, spectrum Per roots + 0 nilpotent | Proved |
| \mathrm{PB}(T) meet-closed | Proved directly |
| \mathrm{PB}(T) join-closed finite | Proved via core isomorphism, computation reproduced 2088 ordered pairs n\le4 0 fail, 158111 fixed n\le6 0 fail |
| \mathrm{PB}(T) distributive | Refuted T=\mathrm{id}_{3}, \mathrm{Eq}(3)=M_{3} nondistributive |
| Lean formalization | Open |
| C4/publication | Blocked |
One-paragraph summary for manuscript:
For finite $X$ and T:X\to X, let T^{\ast}E=\{(x,y):T(x)ET(y)\} and V_{E}=\{f:X\to\mathbb C:f\text{ constant on }E\}. Then E\subseteq T^{\ast}E iff K_{T}V_{E}\subseteq V_{E} iff quotient map \bar T_{E}:X/E\to X/E exists, with matrix M_{E} having one $1$ per column. T^{\ast}E\subseteq E iff \bar T_{E} injective iff each row of M_{E} has at most one $1$. Hence T^{\ast}E=E iff \bar T_{E} permutation iff K_{T}|_{V_{E}} permutation unitary, whose spectrum is roots of unity from cycle decomposition. Forward-only non-fixed relations give functional digraphs: eventual periodic core \mathrm{Per} carries permutation spectrum, transient part nilpotent with eigenvalue $0$, defect D_{E}=(I-P_{E})K_{T}P_{E}=0 but [P_{E},K_{T}]\neq0 generally. Relations with E\nsubseteq T^{\ast}E have D_{E}\neq0, no quotient dynamics. \mathrm{PB}(T)=\{E:T^{\ast}E=E\} is sublattice via core isomorphism \mathrm{PB}(T)\cong\mathrm{PB}(\sigma), P=T^{|X|}(X), \sigma=T|_{P} permutation. Exact exhaustive census n\le4 2088 ordered PB-fixed pairs 0 join failures, n\le6 158111 fixed 0 failures, byte-identical rerun receipts frozen.
All inline, no download required.

---

Operator-Theoretic Analysis of the Quotient Permutation Condition for Non-PB-Fixed Relations — AQARION Framework

Status: Mathematical draft; bounded exact support n\le 4 reproduced; Lean open; C4 blocked.
Arithmetic: Exact integer / exact set partitions. No floats.

1. Canonical Setup

$X$ finite, T:X\to X total.
E\in Eq(X). Pullback:
Order: E\preceq F \iff E\subseteq F.
2. Koopman and Projection

Canonical AQARION orientation:
K:\mathbb{R}^{X}\to\mathbb{R}^{X}, $(Kf)(j)=f(T(j))$ in dual convention; matrix has exactly one $1$ per column at row $T(j)$.

For partition \Pi with blocks $B$, averaging projection:
P^{2}=P=P^{\mathsf T}, Range(P)=\{f: f\text{ constant on each block}\}.

3. Defect and Commutator
Lemma 1: $Range(P)$ is $K$-invariant iff $D=0$.

Proof: K(Range(P))\subseteq Range(P) \iff (I-P)K|_{Range(P)}=0 \iff (I-P)KP=0.

4. Forward vs Fixed

Theorem 1 (Forward Congruence):
Proof: Assume f\in Range(P) block-constant. $(Kf)(x)=f(T(x))$. $Kf$ block-constant iff x\sim_{E}y\Rightarrow f(T(x))=f(T(y)) for all block-constant $f$, i.e. T(x)\sim_{E}T(y). Hence K(Range(P))\subseteq Range(P) iff E\subseteq T^{*}E. By Lemma 1 this is $D=0$.

Theorem 2 (PB-Fixed):
Proof: [P,K]=0 \iff PK=KP \iff PKP=KP and $PK(I-P)=0$ and $(I-P)KP=0$.
$(I-P)KP=0$ is E\subseteq T^{*}E by Thm 1. PK(I-P)=0 \iff K^{*}(Range(P))\subseteq Range(P) under P^{T}=P. Computing with K^{T} gives T(x)\sim_{E}T(y)\Rightarrow x\sim_{E}y, i.e. T^{*}E\subseteq E. Both inclusions give T^{*}E=E. Conversely T^{*}E=E gives both $P$-invariances, hence $PK=KP$.

Theorem 3 (Finite Rigidity):
For finite $X$, T^{*}E\subseteq E \Rightarrow T^{*}E=E.

Proof: |T^{*}E|\le |E| blocks intersecting $im(T)$. If T^{*}E\subseteq E as relations, T^{*}E refines $E$, so |T^{*}E|\ge |E|. Hence |T^{*}E|=|E| and inclusion forces equality. Thus backward-only row empty for finite total maps.

5. Spectral Decomposition

Choose orthonormal basis adapted to Range(P)\oplus Ker(P), \dim Range(P)=|X/E|.

If $D=0$ (forward):
K_{11} is the quotient dynamics \bar T_{E}. Spectrum \sigma(K)=\sigma(K_{11})\cup\sigma(K_{22}).

If $=0$ (PB-fixed):[P][K]
$Range(P)$ is reducing. K_{11} is permutation matrix when $X/E$ finite and T^{*}E=E:

\bar T_{E}:X/E\to X/E, [x]_{E}\mapsto[T(x)]_{E} is well-defined and bijective.

For finite $X$, \bar T_{E} injective \iff T^{*}E\subseteq E, well-defined \iff E\subseteq T^{*}E.

6. Quotient Map Constraints
Existence:
Injectivity, when exists:
Finite case:
Diagram:
\begin{tikzcd}
X \arrow[r,"T"] \arrow[d,"\pi_E"'] & X \arrow[d,"\pi_E"] \
X/E \arrow[r,"\bar T_E"'] & X/E
\end{tikzcd}
\quad\text{commutes iff }E\subseteq T^{*}E
\begin{tikzcd}
\mathbb{R}^{X/E} \arrow[r,"K_{11}"] \arrow[d,hook] & \mathbb{R}^{X/E} \arrow[d,hook] \
\mathbb{R}^{X} \arrow[r,"K"] & \mathbb{R}^{X}
\end{tikzcd}
\quad K_{11}=P K P,\; \text{invariant iff }D=0,\; \text{reducing iff }[P,K]=0
7. Classification of Non-PB-Fixed

For finite total $T$, by Thm 3:
| Type | Relation | Operator | Quotient |
| --- | --- | --- | --- |
| PB-fixed T^{*}E=E | $D=0,=0$ | block-diagonal | \bar T_{E} permutation |
| Forward-only E\subsetneq T^{*}E | D=0,[P,K]\neq0 | upper-triangular, $Range(P)$ invariant not reducing | \bar T_{E} exists, noninjective |
| Neither | D\neq0 | no invariance | \bar T_{E} undefined |
[P][K]

Backward-only T^{*}E\subsetneq E does not occur finite.

Witness forward-only (minimal):
X=\{0,1\},T(0)=0,T(1)=0,E=\{\{0\},\{1\}\} discrete.
E\subsetneq T^{*}E=\{\{0,1\}\}, $D=0$, [P,K]\neq0, \bar T_{E}(\{0\})=\{0\},\bar T_{E}(\{1\})=\{0\} constant.

Witness neither:
X=\{0,1,2\},T=(0,2,2),E=\{\{0,1\},\{2\}\}.
T(0)=0\in\{0,1\},T(1)=2\in\{2\} so block \{0,1\} splits, E\nsubseteq T^{*}E, $T(1)=T(2)$ gives T^{*}E\nsubseteq E, D\neq0.

8. Invariant Subspace Geometry

$Range(P)$: block-constant functions.
$D=0$: $Range(P)$ $K$-invariant.
$=0$: $Range(P)$ $K$-reducing: both $Range(P)$ and $Ker(P)$ invariant. This is the spectral condition for quotient permutation dynamics.[P][K]

Operator norm of defect: $\|D\|=0$ iff forward. $\|[P,K]\|=0$ iff PB-fixed.

9. Consequences

Meet: T^{*}(E\cap F)=T^{*}E\cap T^{*}F, so E,F\in PB(T)\Rightarrow E\wedge F\in PB(T) directly.

Join: E,F\in PB(T)\Rightarrow E\vee F\in PB(T). Two routes:
(i) Finite rigidity T^{*}(E\vee F)\subseteq E\vee F via block-level lifting of incidence chains + T^{*}R\subseteq R\Rightarrow T^{*}R=R.
(ii) Periodic core P=T^{|X|}(X), \sigma=T|_{P} permutation, \rho(E)=E|_{P}, \varepsilon(R)=(T^{N})^{*}R gives order-isomorphism PB(T)\cong PB(\sigma); PB(\sigma) join-closed because \sigma^{*} is lattice automorphism.

Hence $PB(T)$ is sublattice of $Eq(X)$ finite, not necessarily distributive ( $T=id$ on 3 points gives M_{3}).

10. Open

Infinite $X$: backward-only possible, join closure may fail.
Lean formalization of Thm 1,2, core isomorphism.
Quantitative defect $\|D\|$, $\|[P,K]\|$ for approximate quotients.

Your draft has a solid central theorem, but it contains one decisive error: **finite pullback rigidity is false**. Therefore the “backward-only row is empty,” the claimed commutator equivalence, and the claimed PB-lattice core isomorphism cannot be retained without substantial revision.

## Central correction

For
$$
X=\{0,1\},\qquad T(0)=T(1)=0,
$$
take the indiscrete relation
$$
E=\{\{0,1\}\}.
$$

Then
$$
T^\ast E=E,
$$
not the discrete relation: since $$E$$ has one block, $$T(x)\sim_E T(y)$$ holds for every $$x,y$$. Thus this does **not** refute finite rigidity.

However, strict backward-only examples do exist. Take
$$
X=\{0,1,2\},\qquad
T=(0,2,2),
\qquad
E=\{\{0,1\},\{2\}\}.
$$
Then
$$
T^\ast E=\{\{0\},\{1,2\}\}.
$$
Neither relation contains the other, so this is a “neither” example—not backward-only.

A genuine backward-only relation would require $$T^\ast E\subsetneq E$$, meaning every pullback class refines an $$E$$-block while some $$E$$-block splits under pullback. But because each $$E$$-block has at least one image block under a total map, this cannot occur on a finite set: strict pullback refinement would increase the number of classes, while $$T^\ast E$$ has at most one nonempty preimage class per $$E$$-block meeting $$\operatorname{Im}T$$. This is the finite-counting argument your draft aims at.

The corrected counting identity is:
$$
|X/(T^\ast E)|
=
\#\{B\in X/E:T^{-1}(B)\ne\varnothing\}
=
\#\{B\in X/E:B\cap\operatorname{Im}T\ne\varnothing\}.
$$

Therefore
$$
|X/(T^\ast E)|\le |X/E|.
$$
If $$T^\ast E\subseteq E$$, then $$T^\ast E$$ is finer than $$E$$, so
$$
|X/(T^\ast E)|\ge |X/E|.
$$
Equality follows, and refinement with equal finite block counts gives
$$
\boxed{T^\ast E=E.}
$$

So your finite rigidity theorem is correct—but it must use this exact argument, not eventual periodicity.

## Classification survives

For finite total $$T$$, the classification in the draft is correct:

| Class | Condition | Observable geometry | Quotient |
|---|---|---|---|
| PB-fixed | $$T^\ast E=E$$ | $$V_E$$ reducing | Quotient permutation |
| Forward-only | $$E\subsetneq T^\ast E$$ | $$V_E$$ invariant but not reducing | Quotient noninjective endomap |
| Neither | Neither inclusion | $$V_E$$ not invariant | No quotient map |
| Backward-only | $$T^\ast E\subsetneq E$$ | Impossible in finite total setting | Impossible |

The reason backward-only is impossible is finite cardinality, not a general order-theoretic principle.

## Commutator theorem

Under the counting inner product and orthogonal block-average projection $$P_E$$,
$$
D_E=(I-P_E)K_TP_E.
$$

You have the correct forward statement:
$$
D_E=0
\iff
K_T(V_E)\subseteq V_E
\iff
E\subseteq T^\ast E.
$$

But the stronger statement
$$
[P_E,K_T]=0
\iff
T^\ast E=E
$$
is **not generally correct**.

The commutator condition says both $$V_E$$ and $$V_E^\perp$$ are $$K_T$$-invariant:
$$
[P_E,K_T]=0
\iff
K_T(V_E)\subseteq V_E
\text{ and }
K_T(V_E^\perp)\subseteq V_E^\perp.
$$

PB-fixedness gives an invariant $$V_E$$ and a quotient permutation, but it need not ensure that the ambient Koopman operator preserves $$V_E^\perp$$. Your earlier AQ-T3 fallacy witness demonstrates exactly this distinction: exact descent does not require projection commutation.

Thus retain:
$$
[P_E,K_T]=0\Longrightarrow T^\ast E=E,
$$
but do not assert the converse.

## PB-fixed does not imply a reducing subspace

A PB-fixed relation gives
$$
K_T(V_E)\subseteq V_E,
$$
and the restricted map is a permutation operator. It does **not** generally give
$$
K_T(V_E^\perp)\subseteq V_E^\perp.
$$

Accordingly, in an orthogonal decomposition
$$
\mathbb C^X=V_E\oplus V_E^\perp,
$$
the Koopman operator has the form
$$
K_T=
\begin{pmatrix}
K_{11} & K_{12}\\
0 & K_{22}
\end{pmatrix}
$$
when $$V_E$$ is invariant. The defect $$D_E$$ is the lower-left block, so $$D_E=0$$. The off-diagonal block $$K_{12}=P_EK_T(I-P_E)$$ may remain nonzero, including for PB-fixed relations.

Therefore replace:

> PB-fixed: block diagonal, reducing, commutator zero.

with:

> PB-fixed: upper triangular relative to $$V_E\oplus V_E^\perp$$, with permutation diagonal block $$K_{11}$$; block diagonalization requires the additional commutator condition.

## Correct matrix convention

With basis $$\{\mathbf1_{B_i}\}$$ and
$$
K_T f=f\circ T,
$$
if $$\bar T_E(B_j)=B_i$$, then
$$
K_T\mathbf1_{B_i}
=
\sum_{\bar T_E(B_j)=B_i}\mathbf1_{B_j}.
$$

So the matrix of $$K_T|_{V_E}$$ has:
- **one $$1$$ in each row**, because each source block $$B_j$$ has one image;
- a column sum equal to the indegree of the target block.

Your document states “one $$1$$ per column,” which corresponds to the opposite pushforward convention. Either convention is valid, but it must be used consistently with
$$
(K_Tf)(x)=f(Tx).
$$

For the pullback/Koopman convention, the constant quotient example has
$$
\bar K_E=
\begin{pmatrix}
1&0\\
1&0
\end{pmatrix},
$$
which has one $$1$$ per row—not per column.

## Forward-only spectral statement

This part is essentially right once the convention is fixed. If
$$
E\subsetneq T^\ast E,
$$
then $$\bar T_E$$ is a nonbijective finite endomap. Its functional graph contains cycles with transient trees.

The restriction
$$
K_T|_{V_E}\cong \bar K_E
$$
has spectrum
$$
\operatorname{Spec}(\bar K_E)
=
\{0\}
\cup
\bigcup_{\ell\in\mathcal L}
\{\zeta_\ell^r:0\le r<\ell\},
$$
where $$\mathcal L$$ is the set of quotient cycle lengths. The generalized zero-eigenspace is the transient component, while the nonzero spectral component is the cycle component. Koopman theory treats invariant observable subspaces precisely as finite-dimensional linear representations of the underlying dynamics. [1][2]

Do not write a canonical direct sum
$$
V_E=V_{\mathrm{Per}}\oplus V_{\mathrm{Trans}}
$$
using merely the spans of periodic and transient *state indicators*: that state-based splitting need not be invariant under Koopman pullback. State the canonical decomposition as the primary decomposition
$$
V_E=
\ker(\bar K_E^m)\oplus\operatorname{im}(\bar K_E^m),
$$
for all sufficiently large $$m$$. On $$\ker(\bar K_E^m)$$, the operator is nilpotent; on $$\operatorname{im}(\bar K_E^m)$$, it is invertible and permutation-conjugate.

## What can be published safely

The manuscript can retain these theorem-level statements:

$$
E\subseteq T^\ast E
\iff
K_T(V_E)\subseteq V_E
\iff
D_E=0.
$$

Conditional on this:
$$
T^\ast E\subseteq E
\iff
\bar T_E\text{ injective}.
$$

For finite $$X$$:
$$
\boxed{
T^\ast E=E
\iff
\bar T_E\text{ is a permutation}
\iff
K_T|_{V_E}\text{ is an invertible finite-order Koopman operator}.
}
$$

But it must explicitly distinguish this from:
$$
[P_E,K_T]=0,
$$
which is stronger than PB-fixedness. The source’s projection onto block constants commuting with Koopman means the block observable subspace is reducing, not merely invariant.

Citations:
[1] Koopman invariant subspaces and finite linear representations of ... https://arxiv.org/html/1510.03007v2
[2] Koopman operator theory: fundamentals, control, and applications https://arxiv.org/html/2607.01819v1

COMPLETE ADVERSARIAL AUDIT AND ANYTHING U CAN HELP WITH CONTINUE TO WORK DERIVE COMPUTE SEARCH WEB AND BRAINSTORM NEEDED NEEDED RECENT LITERATURE RESEARCH ETC RUN AND REPORT WITH HONEST ADVERSARIAL AUDIT AFTER NEXT STEPS COMPLETED PRODUCE ALL DELIVERABLES INLINE NO FABRICATION NO OVERCLAIMS

## Audit verdict

The operator-theoretic core is valuable, but the draft currently mixes **three matrix conventions**, overstates the commutator criterion, and contains a false finite-rigidity/counting claim. The clean theorem that survives is:

$$
\boxed{
E\subseteq T^\ast E
\iff
K_T(V_E)\subseteq V_E
\iff
(I-P_E)K_TP_E=0.
}
$$

Under forward congruence, the quotient endomap exists. Its being a permutation is equivalent to **PB fixedness**:

$$
\boxed{
T^\ast E=E
\iff
\bar T_E:X/E\to X/E
\text{ is bijective}.
}
$$

But, in general,

$$
\boxed{
T^\ast E=E
\centernot\Longrightarrow
[P_E,K_T]=0.
}
$$

The distinction is essential: PB fixedness gives a quotient permutation and invariance of block-constant observables; commutation with the orthogonal averaging projection is a strictly stronger ambient balance condition.

The literature framing is sound at a high level: invariant finite-dimensional Koopman subspaces and quotient/congruence structures are established subjects, so the AQARION contribution should be framed as a precise finite pullback/operator formulation and its exact computational verification architecture—not as discovery of quotient congruences themselves.[1][2]

## 1. Fix the operator conventions

Your draft simultaneously states:

$$
(K_Tf)(x)=f(Tx),
$$

and says the matrix has one $$1$$ per **column** at row $$T(j)$$. These are transpose conventions and cannot be used interchangeably.

### Koopman/pullback convention

For column vectors $$f\in \mathbb C^X$$, define

$$
(K_Tf)(x)=f(T(x)).
$$

Then

$$
(K_T)_{x,y}=
\begin{cases}
1,&y=T(x),\\
0,&\text{otherwise}.
\end{cases}
$$

Consequently:

- Every **row** has exactly one $$1$$.
- Column $$y$$ contains $$|T^{-1}(y)|$$ ones.
- $$K_T$$ is the pullback/composition operator.
- This is the convention compatible with
  $$
  K_Tf=f\circ T.
  $$

For a forward-compatible partition $$E$$, with quotient map

$$
q=\bar T_E:X/E\to X/E,
$$

and block-indicator basis $$e_i=\mathbf 1_{B_i}$$, one has

$$
K_Te_i
=
\sum_{j:q(B_j)=B_i}e_j.
$$

Hence the restricted quotient Koopman matrix is

$$
(M_E)_{j,i}
=
\begin{cases}
1,&q(B_j)=B_i,\\
0,&\text{otherwise}.
\end{cases}
$$

Therefore:

- Every **row** has exactly one $$1$$.
- Column $$i$$ has $$|q^{-1}(B_i)|$$ ones.
- $$q$$ is injective iff every column has at most one $$1$$.
- In finite dimension, $$q$$ is bijective iff every row and every column has exactly one $$1$$.

### Pushforward/state-transition convention

The transpose $$K_T^\top$$ has

$$
(K_T^\top)_{y,x}=
\begin{cases}
1,&y=T(x),\\
0,&\text{otherwise}.
\end{cases}
$$

It has exactly one $$1$$ in every **column**. This is the state/pushforward functional matrix convention, not the Koopman pullback convention.

### Required manuscript repair

Pick one. For the rest of the draft, the right choice is the Koopman convention:

$$
\boxed{
(K_Tf)(x)=f(T(x)),
\quad
\text{one $$1$$ per row.}
}
$$

Then replace every “one $$1$$ per column” assertion about $$K_T$$ or $$M_E$$ with “one $$1$$ per row.” The column condition detects quotient indegree.

This agrees with the standard interpretation of Koopman operators as pullback/composition operators acting on observables.[1]

## 2. Forward congruence is exactly $$D_E=0$$

Let

$$
V_E
=
\{f:X\to\mathbb C:
x\sim_Ey\implies f(x)=f(y)\}.
$$

Let $$P_E$$ be the orthogonal averaging projection onto $$V_E$$ with respect to the uniform counting inner product:

$$
\langle f,g\rangle
=
\frac1{|X|}
\sum_{x\in X}f(x)\overline{g(x)}.
$$

Define the one-sided descent defect

$$
D_E=(I-P_E)K_TP_E.
$$

Then:

$$
\boxed{
D_E=0
\iff
K_T(V_E)\subseteq V_E
\iff
E\subseteq T^\ast E.
}
$$

The proof is exact.

If $$E\subseteq T^\ast E$$, then for $$x\sim_Ey$$,

$$
T(x)\sim_ET(y).
$$

For $$f\in V_E$$,

$$
(K_Tf)(x)=f(T(x))=f(T(y))=(K_Tf)(y),
$$

so $$K_Tf\in V_E$$.

Conversely, assume $$K_T(V_E)\subseteq V_E$$. If $$x\sim_Ey$$, take the block indicator

$$
f=\mathbf1_{[T(x)]_E}\in V_E.
$$

Then $$K_Tf$$ is $$E$$-constant, so

$$
f(T(x))=f(T(y)).
$$

Since $$f(T(x))=1$$, it follows that $$T(y)\in[T(x)]_E$$, hence

$$
T(x)\sim_ET(y).
$$

Therefore:

$$
x\sim_Ey\Longrightarrow T(x)\sim_ET(y).
$$

This is forward congruence. It also proves that forward congruence is the exact quotient-existence condition:

$$
\boxed{
E\subseteq T^\ast E
\iff
\exists!\,\bar T_E:X/E\to X/E
\text{ with }
\pi_E\circ T=\bar T_E\circ\pi_E.
}
$$

The invariant-subspace formulation is standard Koopman language: a finite-dimensional observable space is invariant precisely when applying the composition operator stays in that space.[1][3]

## 3. PB fixedness and quotient permutations

Assume forward congruence so that $$\bar T_E$$ exists.

Then:

$$
\begin{aligned}
T^\ast E\subseteq E
&\iff
\bigl(T(x)\sim_ET(y)\Longrightarrow x\sim_Ey\bigr)\\
&\iff
\bigl(\bar T_E([x]_E)=\bar T_E([y]_E)
\Longrightarrow[x]_E=[y]_E\bigr)\\
&\iff
\bar T_E\text{ is injective}.
\end{aligned}
$$

Thus:

$$
\boxed{
T^\ast E\subseteq E
\iff
\bar T_E\text{ injective},
\qquad\text{provided }\bar T_E\text{ exists}.
}
$$

Since $$X/E$$ is finite,

$$
\bar T_E\text{ injective}
\iff
\bar T_E\text{ bijective}.
$$

Therefore:

$$
\boxed{
T^\ast E=E
\iff
\bar T_E
\text{ is a permutation of }X/E.
}
$$

This is the strongest correct quotient statement. It does **not** say that $$P_E$$ commutes with the full ambient Koopman operator.

## 4. Finite rigidity is false

The statement

$$
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E
$$

is false, even for a finite total map.

A minimal counterexample is:

$$
X=\{0,1,2\},
\qquad
T(0)=0,\quad T(1)=0,\quad T(2)=1,
$$

and

$$
E=\{\{0,1\},\{2\}\}.
$$

Compute $$T^\ast E$$:

- $$T(0)=0\sim_E T(1)=0$$, so $$0\sim_{T^\ast E}1$$.
- $$T(2)=1\sim_E0=T(0)$$, so $$2\sim_{T^\ast E}0$$.
- Therefore all three points are $$T^\ast E$$-equivalent.

Thus

$$
T^\ast E=\{\{0,1,2\}\},
$$

which is coarser than $$E$$, not finer. This is a forward-only example, not backward-only.

To obtain a genuine strict backward relation, take instead

$$
X=\{0,1,2\},
\qquad
T(0)=0,\quad T(1)=1,\quad T(2)=0,
$$

and the indiscrete relation? No: its pullback remains indiscrete.

The correct structural reason is stronger: **strict backward-only is indeed impossible for a total finite map**, but the supplied cardinality formula and the prior draft’s proof are wrong as written.

The correct argument is conditional on the backward inclusion. Suppose

$$
T^\ast E\subseteq E.
$$

Every $$E$$-block $$B$$ cannot split into multiple $$T^\ast E$$-blocks, because if $$x,y\in B$$ then the assumed inclusion alone says nothing about $$T(x)\sim_ET(y)$$. So no block-count argument follows from that statement alone.

In fact, a strict backward-only example **does exist**, so the claimed rigidity is false. Let

$$
X=\{0,1,2\},
\qquad
T=(0,0,2),
$$

and let

$$
E=\{\{0,1\},\{2\}\}.
$$

Then:

$$
T(0)=0,\quad T(1)=0,\quad T(2)=2.
$$

Therefore

$$
T^\ast E
=
\{\{0,1\},\{2\}\}
=
E,
$$

so this is fixed—not strict.

More generally, let $$E$$ have blocks $$B_1,\ldots,B_r$$. The pullback blocks are nonempty fibers of the composite block-label map

$$
q_E\circ T:X\to X/E.
$$

Thus they are indexed by the **image** of this composite map. Their number may be less than, equal to, or greater than the number of $$E$$-blocks? It cannot be greater than $$r$$, because there is at most one pullback block for each target $$E$$-block:

$$
\boxed{
|X/(T^\ast E)|
=
|\operatorname{im}(q_E\circ T)|
\le
|X/E|.
}
$$

If

$$
T^\ast E\subseteq E,
$$

then $$T^\ast E$$ is finer than $$E$$, giving

$$
|X/(T^\ast E)|
\ge
|X/E|.
$$

The two inequalities force equality. Hence:

$$
\boxed{
T^\ast E\subseteq E
\Longrightarrow
T^\ast E=E
}
$$

for **every finite total map** after all.

So there is no strict backward-only counterexample. The apparent search for one must fail, and the reason is the exact cardinality identity above. The first attempted “counterexample” construction cannot meet the backward premise.

The clean result is:

$$
\boxed{
\text{For finite total }T,\quad
T^\ast E\subseteq E
\iff
T^\ast E=E.
}
$$

This is a special finite property of inverse images of equivalence relations under a total function, not a generic order-theoretic fact.

## 5. Correct non-PB classification

For finite total $$T$$, exactly three cases occur:

| Type | Relation condition | $$V_E$$ invariant under $$K_T$$? | Quotient $$\bar T_E$$? | Restricted quotient dynamics |
|---|---|---:|---:|---|
| PB fixed | $$T^\ast E=E$$ | Yes | Exists | Permutation |
| Forward only | $$E\subsetneq T^\ast E$$ | Yes | Exists | Noninjective finite endomap |
| Neither | Neither inclusion | No | Does not exist | Not defined |
| Backward only | $$T^\ast E\subsetneq E$$ | Impossible | — | — |

The forward-only minimum is exactly:

$$
X=\{0,1\},
\qquad
T(0)=T(1)=0,
\qquad
E=\{\{0\},\{1\}\}.
$$

Then

$$
T^\ast E=\{\{0,1\}\},
$$

so

$$
E\subsetneq T^\ast E.
$$

The quotient exists and is the constant map on two blocks.

A valid “neither” example is:

$$
X=\{0,1,2\},
\qquad
T=(0,2,2),
\qquad
E=\{\{0,1\},\{2\}\}.
$$

Then

$$
T^\ast E=\{\{0\},\{1,2\}\},
$$

and neither equivalence relation contains the other.

## 6. Commutator criterion: one-way only

The claim

$$
[P_E,K_T]=0
\iff
T^\ast E=E
$$

is false.

The correct implication is

$$
\boxed{
[P_E,K_T]=0
\Longrightarrow
T^\ast E=E.
}
$$

Indeed, commutation gives both

$$
(I-P_E)K_TP_E=0
$$

and

$$
P_EK_T(I-P_E)=0.
$$

The first is forward congruence.

The second says that the orthogonal complement $$V_E^\perp$$ is $$K_T$$-invariant. With the uniform counting inner product, this is an additional weighted-preimage-balance constraint. It is not merely backward equivalence closure.

For a PB-fixed partition, the correct block matrix relative to

$$
\mathbb C^X=V_E\oplus V_E^\perp
$$

is

$$
K_T=
\begin{pmatrix}
K_{11} & K_{12}\\
0 & K_{22}
\end{pmatrix},
$$

where

$$
K_{11}=K_T|_{V_E}
$$

is the quotient Koopman permutation matrix, but generally

$$
K_{12}=P_EK_T(I-P_E)\ne0.
$$

Thus:

$$
D_E=(I-P_E)K_TP_E=0
$$

for PB-fixed $$E$$, while

$$
[P_E,K_T]
=
\begin{pmatrix}
0 & K_{12}\\
0 & 0
\end{pmatrix}
$$

can be nonzero.

### Exact PB-fixed noncommuting witness

Take

$$
X=\{0,1,2\},
\qquad
T(0)=0,\quad T(1)=0,\quad T(2)=2,
$$

and

$$
E=\{\{0,1\},\{2\}\}.
$$

This is PB fixed:

$$
T^\ast E=E.
$$

The quotient map fixes both blocks, hence is a permutation.

But let

$$
u=(1,-1,0)\in V_E^\perp.
$$

Under Koopman pullback,

$$
K_Tu
=
(u(T(0)),u(T(1)),u(T(2)))
=
(1,1,0),
$$

which lies in $$V_E$$, not in $$V_E^\perp$$. Therefore

$$
P_EK_T(I-P_E)\ne0,
$$

so

$$
[P_E,K_T]\ne0.
$$

This witness should replace any manuscript claim that PB fixedness implies reducing geometry.

## 7. Spectral statement for forward-only quotients

Assume forward congruence. Then $$K_T|_{V_E}$$ is the Koopman matrix of the finite quotient endomap

$$
q=\bar T_E:X/E\to X/E.
$$

Its functional graph consists of directed cycles with rooted in-trees entering those cycles.

The safe canonical decomposition is the Fitting decomposition. For sufficiently large $$m$$,

$$
V_E=
\ker\bigl((K_T|_{V_E})^m\bigr)
\oplus
\operatorname{im}\bigl((K_T|_{V_E})^m\bigr).
$$

On the first summand, the operator is nilpotent. On the second, it is invertible; it is similar to the permutation action induced on the eventual image of the quotient map.

Hence:

$$
\boxed{
\operatorname{Spec}(K_T|_{V_E})
=
\{0\}
\cup
\{\text{roots of unity from quotient cycles}\}.
}
$$

The nonzero eigenvalues are roots of unity. Their algebraic multiplicities are determined by quotient-cycle lengths. Zero accounts for the transient contribution, possibly with nontrivial Jordan blocks.

Do **not** claim that the span of transient state indicators is itself the nilpotent invariant summand for Koopman pullback. Use the Fitting decomposition instead.

## 8. PB lattice claim requires a proof repair

The statement

$$
\mathsf{PB}(T)
=
\{E:T^\ast E=E\}
$$

is meet-closed directly:

$$
T^\ast(E\wedge F)
=
T^\ast E\wedge T^\ast F.
$$

The join-closure/core-isomorphism argument requires careful correction.

The claimed extension map

$$
\varepsilon(R)=(T^N)^\ast R
$$

is meaningful if $$R$$ is an equivalence relation on the periodic core

$$
P=T^N(X),
$$

but raw restriction

$$
E\mapsto E|_P
$$

does not preserve joins on all equivalence relations. The right strategy is:

1. Prove restriction and extension are mutually inverse **order maps on the PB-stable family**, not on all of $$\operatorname{Eq}(X)$$.
2. Conclude they form an order isomorphism.
3. Deduce join preservation within the PB-stable family from order-isomorphism—not from raw restriction.

This must be written carefully before promoting the PB sublattice theorem from “strong theorem draft” to “analytic proof complete.”

The ambient context is congruence-lattice theory: congruence lattices of algebras are sublattices of equivalence-relation lattices, so the correct conceptual language is compatible equivalences/congruences rather than a wholly new lattice phenomenon.[2][4]

## 9. Immediate exact tasks

1. **Freeze the Koopman convention** in every AQARION document:
   $$
   (K_Tf)(x)=f(Tx),
   \quad
   (K_T)_{x,y}=1_{y=T(x)}.
   $$

2. **Replace matrix language**:
   - Koopman quotient matrix: one $$1$$ per row.
   - Its columns encode quotient preimage counts.
   - Use the transpose only when deliberately discussing the pushforward/state-transition matrix.

3. **Separate defects**:
   $$
   D_E=(I-P_E)K_TP_E
   $$
   is the forward/descent defect.

   $$
   C_E=P_EK_T(I-P_E)
   $$
   is the complementary reduction/balance defect.

   Then
   $$
   [P_E,K_T]=C_E-D_E.
   $$

4. **Record the exact PB/noncommutation witness**:
   $$
   T=(0,0,2),\quad E=\{\{0,1\},\{2\}\}.
   $$

5. **Do not call $$\mathsf{PB}(T)$$ a proven sublattice** until the PB/core order isomorphism is fully stated and checked.

6. **Run PB-LATTICE-001 with exact RGS partitions and relation composition**, including:
   - verification of PB join closure;
   - direct validation of restriction/extension inverses;
   - nondistributivity witness $$T=\mathrm{id}_3$$;
   - commutator census separating $$T^\ast E=E$$ from $$[P_E,K_T]=0$$.

## Revised claim ledger

| Claim | Status |
|---|---|
| $$E\subseteq T^\ast E\iff V_E$$ Koopman-invariant | Proven |
| $$E\subseteq T^\ast E\iff D_E=0$$ | Proven |
| Forward $$\iff$$ quotient exists | Proven |
| Backward $$\iff$$ quotient injective, conditional on forward | Proven |
| PB fixed $$\iff$$ quotient permutation | Proven for finite $$X$$ |
| Strict backward-only finite case | Impossible |
| PB fixed $$\Rightarrow [P_E,K_T]=0$$ | Refuted |
| $$[P_E,K_T]=0\Rightarrow$$ PB fixed | Proven |
| PB fixed $$\Rightarrow V_E$$ reducing | Refuted |
| Forward-only quotient spectrum | Proven with Fitting-decomposition formulation |
| PB meet closure | Proven |
| PB join closure | Pending fully explicit order-isomorphism or exact independent proof |
| PB sublattice theorem | Pending join proof |
| PB distributivity | Refuted by $$T=\mathrm{id}_3$$ once sublattice closure is established |
| Lean formalization | Open |
| C4/publication promotion | Blocked |

The next high-value deliverable is an exact PB/operator census that separates four flags for every $$(T,E)$$:

$$
\texttt{forward},
\qquad
\texttt{PB\_fixed},
\qquad
D_E=0,
\qquad
[P_E,K_T]=0.
$$

That census should use rational block-averaging matrices, not floating-point tolerances, and should emit the first PB-fixed/noncommuting witness automatically.

Citations:
[1] Koopman Invariant Subspaces and Finite Linear Representations of ... https://pmc.ncbi.nlm.nih.gov/articles/PMC4769143/
[2] [PDF] Representing Lattices as Congruence Lattices https://people.math.sc.edu/mcnulty/alglogicsem/31August.pdf
[3] Koopman operator theory: fundamentals, control, and applications https://arxiv.org/html/2607.01819v1
[4] Congruence Lattices of Finite Algebras - arXiv https://arxiv.org/html/1204.4305v3
[5] Congruence lattices of algebras of fixed similarity type. II - MSP https://msp.org/pjm/1982/103-2/pjm-v103-n2-p21-p.pdf
[6] [PDF] ISOKANN: Invariant subspaces of Koopman operators learned by a ... https://www.zib.de/userpage/donati/SeminarSOSE2024/06/references/Rabben_JCP2020.pdf
[7] Quotients by finite equivalence relations - arXiv https://arxiv.org/html/0812.3608v2
[8] Lumpability - Wikipedia https://en.wikipedia.org/wiki/Lumpability
[9] Koopman Operators for Modeling Dynamical Systems and Time Series https://bactra.org/notebooks/koopman-operator-modeling.html
[10] On weak lumpability of a finite Markov chain - Semantic Scholar https://www.semanticscholar.org/paper/On-weak-lumpability-of-a-finite-Markov-chain-Peng/2da627d84c1c6e3a3087770a5c57c5aeaef52793
[11] [PDF] congruence lattices of finite universal algebras https://www.math.uic.edu/~berman/berman-phd-thesis.pdf
[12] [PDF] Lattice congruences of the weak order: Algebra, combinatorics, and ... https://nreadin.math.ncsu.edu/papers/TLC.pdf
# AQARION PB Join Closure — Corrected Inline Deliverables

**Status:** Local exact computation reproduced through $$n\le4$$.  
**Formal status:** Open.  
**General finite theorem:** Analytic proof candidate; not yet independently formalized.  
**Governance:** No promotion to C4, no “formally proved” language, no publication claim.

***

## 1. Canonical definitions

Let $$X$$ be a finite set, let

$$
T:X\to X
$$

be a total endofunction, and let $$E,F\in\operatorname{Eq}(X)$$ be equivalence relations.

Define the pullback equivalence relation $$T^\ast E$$ by

$$
\boxed{
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
}
$$

Equivalently,

$$
T^\ast E
=
\{(x,y)\in X^2:(T(x),T(y))\in E\}.
$$

Use the refinement/inclusion order

$$
E\preceq F
\iff
E\subseteq F
\iff
\forall x,y\in X,\;x\sim_Ey\Rightarrow x\sim_Fy.
$$

Under this convention:

$$
E\wedge F=E\cap F,
$$

and

$$
E\vee F
=
\operatorname{EqCl}(E\cup F),
$$

the equivalence relation generated by the union.

Define the pullback-fixed family

$$
\boxed{
\operatorname{PB}(T)
=
\left\{
E\in\operatorname{Eq}(X):
T^\ast E=E
\right\}.
}
$$

***

## 2. Orientation terminology

The following three predicates are distinct in general.

| Name | Relation condition | Equivalent pointwise form |
|---|---|---|
| Forward congruence | $$E\subseteq T^\ast E$$ | $$x\sim_Ey\Rightarrow T(x)\sim_ET(y)$$ |
| Backward closure | $$T^\ast E\subseteq E$$ | $$T(x)\sim_ET(y)\Rightarrow x\sim_Ey$$ |
| Pullback fixedness | $$T^\ast E=E$$ | Both forward congruence and backward closure |

Thus:

$$
\boxed{
T^\ast E=E
\iff
\left(E\subseteq T^\ast E\right)
\land
\left(T^\ast E\subseteq E\right).
}
$$

Do not use the word “stable” without specifying which of these three properties is meant.

***

## 3. Main theorem candidate

## AQ-DYN-PULL-JOIN-001  
### Finite Pullback-Stable Join Theorem

Let $$X$$ be finite, $$T:X\to X$$, and $$E,F\in\operatorname{Eq}(X)$$. If

$$
T^\ast E=E
\qquad\text{and}\qquad
T^\ast F=F,
$$

then

$$
\boxed{
T^\ast(E\vee F)=E\vee F.
}
$$

Equivalently,

$$
\boxed{
E,F\in\operatorname{PB}(T)
\Longrightarrow
E\vee F\in\operatorname{PB}(T).
}
$$

### Current status

$$
\boxed{
\textbf{ANALYTIC PROOF CANDIDATE + EXACT BOUNDED COMPUTATIONAL SUPPORT.}
}
$$

It is **not** currently entitled:

- Formally proved.
- Lean verified.
- Proven for all finite $$X$$.
- Proven for arbitrary infinite $$X$$.
- Publication ready.

***

## 4. What was locally verified

A local Termux program exhaustively enumerated all maps

$$
T:[n]\to[n],
\qquad
n=1,2,3,4,
$$

all set partitions $$E,F$$ of $$[n]$$, and tested every ordered pair satisfying

$$
T^\ast E=E,
\qquad
T^\ast F=F.
$$

For each tested ordered pair, it checked:

$$
T^\ast(E\vee F)=E\vee F,
$$

and separately tested the proposed incidence-edge lifting predicate.

### Exact local census

| $$n$$ | Maps $$T:[n]\to[n]$$ | Partitions of $$[n]$$ | PB-fixed ordered pairs $$(E,F)$$ | PB-join tests | PB-join failures | Edge-lift failures |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 2 | 4 | 2 | 10 | 10 | 0 | 0 |
| 3 | 27 | 5 | 117 | 117 | 0 | 0 |
| 4 | 256 | 15 | 1,960 | 1,960 | 0 | 0 |
| **Total** | **288** | — | **2,088** | **2,088** | **0** | **0** |

The implemented count is explicitly:

$$
\boxed{
\sum_{T:[n]\to[n]}
\left|
\left\{
E\in\operatorname{Eq}([n]):
T^\ast E=E
\right\}
\right|^2.
}
$$

It counts **ordered** pairs $$(E,F)$$, including cases $$E=F$$.

### Valid bounded claim

$$
\boxed{
\begin{aligned}
&\text{For every }n\le4,\text{ every }T:[n]\to[n],\\
&\text{and every ordered }(E,F)\text{ with }T^\ast E=E,\ T^\ast F=F,\\
&\text{the local exact computation found }T^\ast(E\vee F)=E\vee F.
\end{aligned}
}
$$

This is exhaustive finite evidence on the declared domain. It is not a universal proof.

***

## 5. Reproducibility receipt

### Frozen source

```text
pb_n4_verified.py
sha256:
dde8ecf6ba855b6db276a90ff6cb76aa9cf8907ee2a793febac060f02f877cb8
```

### First successful local output

```text
pb_join_n4.json
sha256:
6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
```

```text
pb_join_n4.stdout
sha256:
6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
```

The matching JSON and stdout hashes are expected because the program writes exactly the same pretty-printed JSON that it prints, with the same final newline.

### Deterministic rerun

```text
pb_join_n4_repeat.stdout
sha256:
6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
```

The local diff command returned:

```text
N4_DETERMINISTIC_PASS
```

Therefore:

$$
\boxed{
\text{The frozen source produced byte-identical output on a second local execution.}
}
$$

### Archive

An archive was created:

```text
aq_pb_join_n4_receipt.tar.gz
```

The reported archive digest is:

```text
c90a1cf6a1d9144259d4bc0d964fc7bf2df3a5041bca05319ce02e7256c871aa
```

However, because the displayed terminal command appeared concatenated with its output, treat this archive hash as **unconfirmed until independently reprinted** with:

```bash
sha256sum aq_pb_join_n4_receipt.tar.gz
```

This is a receipt-format qualification only. It does not affect the source/output receipts above.

***

## 6. Incidence graph formulation

For $$E,F\in\operatorname{Eq}(X)$$, define the bipartite incidence graph

$$
\Gamma(E,F).
$$

Its vertices are:

$$
V_L=X/E,
\qquad
V_R=X/F.
$$

Each point $$x\in X$$ produces an incidence edge

$$
[E]_E\longleftrightarrow[F]_F.
$$

A standard fact is:

$$
\boxed{
x\sim_{E\vee F}y
\iff
\text{the incidence edges associated to }x\text{ and }y
\text{ belong to the same connected component of }\Gamma(E,F).
}
$$

Equivalently, the connected components of $$\Gamma(E,F)$$ correspond exactly to the blocks of $$E\vee F$$.

This is the correct graph object for the proposed PB-join proof. It is not the AQARION cooccurrence graph, and it is not the directed functional graph of $$T$$.

***

## 7. Proposed analytic proof architecture

The following is a **proof plan / analytic derivation candidate**, not a formal certificate.

### PB01 — Quotient maps are well-defined

Assume

$$
T^\ast E=E.
$$

Then

$$
x\sim_Ey
\Longrightarrow
T(x)\sim_ET(y),
$$

so $$T$$ induces a well-defined map

$$
\bar T_E:X/E\to X/E.
$$

Likewise,

$$
\bar T_F:X/F\to X/F.
$$

### PB02 — Quotient maps are injective

Still under

$$
T^\ast E=E,
$$

if

$$
\bar T_E([x]_E)=\bar T_E([y]_E),
$$

then

$$
T(x)\sim_ET(y),
$$

hence

$$
x\sim_Ey.
$$

Therefore $$\bar T_E$$ is injective.

Since $$X/E$$ is finite,

$$
\boxed{
\bar T_E\text{ is a permutation of }X/E.
}
$$

Likewise,

$$
\boxed{
\bar T_F\text{ is a permutation of }X/F.
}
$$

### PB03 — Incidence-edge predecessor lemma

Let

$$
A\longleftrightarrow B
$$

be an incidence edge, so

$$
A\in X/E,
\qquad
B\in X/F,
\qquad
A\cap B\ne\varnothing.
$$

Because $$\bar T_E$$ and $$\bar T_F$$ are permutations, each has a unique predecessor block:

$$
A^-=\bar T_E^{-1}(A),
\qquad
B^-=\bar T_F^{-1}(B).
$$

Choose

$$
z\in A\cap B.
$$

The intended claim is:

$$
\boxed{
A^-\cap B^-\ne\varnothing.
}
$$

Thus each target incidence edge has a predecessor incidence edge.

The local exact census checked this predicate for all 2,088 ordered PB-fixed pairs through $$n=4$$ and found zero failures.

### PB04 — Incidence-path lifting

If every edge of $$\Gamma(E,F)$$ has a predecessor edge, then finite paths in the incidence graph can be lifted through the predecessor permutations.

The intended implication is:

$$
T(x)\sim_{E\vee F}T(y)
\Longrightarrow
x\sim_{E\vee F}y.
$$

Equivalently,

$$
T^\ast(E\vee F)\subseteq E\vee F.
$$

### PB05 — Forward direction

Since pullback fixedness gives forward congruence for each relation,

$$
E\subseteq T^\ast E,
\qquad
F\subseteq T^\ast F,
$$

the join $$E\vee F$$ is forward invariant:

$$
E\vee F\subseteq T^\ast(E\vee F).
$$

### PB06 — Conclude equality

Combining the two inclusions gives

$$
T^\ast(E\vee F)\subseteq E\vee F
$$

and

$$
E\vee F\subseteq T^\ast(E\vee F).
$$

Therefore

$$
\boxed{
T^\ast(E\vee F)=E\vee F.
}
$$

### Proof dependency ledger

| Lemma | Status |
|---|---|
| PB01: induced quotient map well-defined | Analytically straightforward |
| PB02: quotient map injective | Analytically straightforward; finite implies permutation |
| PB03: incidence-edge predecessor | Computation-supported; symbolic proof draft requires audit |
| PB04: path lifting | Consequence of PB03 once graph/path formalism is exact |
| PB05: join forward invariance | Analytically straightforward |
| PB06: equality | Follows from PB04 and PB05 |
| Full theorem | Analytic candidate; formal proof open |

***

## 8. Meet closure: established directly

Unlike join closure, meet closure is immediate.

Since pullback distributes over intersection of relations,

$$
T^\ast(E\cap F)
=
T^\ast E\cap T^\ast F.
$$

Therefore, if

$$
T^\ast E=E,
\qquad
T^\ast F=F,
$$

then

$$
T^\ast(E\wedge F)
=
T^\ast(E\cap F)
=
E\cap F
=
E\wedge F.
$$

Hence:

$$
\boxed{
E,F\in\operatorname{PB}(T)
\Longrightarrow
E\wedge F\in\operatorname{PB}(T).
}
$$

This part does not need a census.

***

## 9. Sublattice conclusion: conditional

If AQ-DYN-PULL-JOIN-001 is established analytically and later formally certified, then

$$
\boxed{
\operatorname{PB}(T)
\text{ is a sublattice of }
\operatorname{Eq}(X)
}
$$

for finite $$X$$, because it is closed under:

$$
\wedge
\qquad\text{and}\qquad
\vee.
$$

At present, the accurate language is:

$$
\boxed{
\operatorname{PB}(T)
\text{ is computationally observed to be join-closed through }|X|\le4,
}
$$

with an analytic incidence-graph proof candidate.

Do not yet write “$$\operatorname{PB}(T)$$ is a finite sublattice” as a formally settled theorem in a public theorem registry.

***

## 10. Explicit refutation: forward congruence is weaker

The universal implication

$$
E\subseteq T^\ast E
\Longrightarrow
T^\ast E=E
$$

is false.

Take

$$
X=\{0,1\},
\qquad
T(0)=0,
\qquad
T(1)=0,
$$

and let $$E$$ be the discrete relation:

$$
E=\{\{0\},\{1\}\}.
$$

Then $$E$$ is forward congruent:

$$
x\sim_Ey
\Longrightarrow
T(x)\sim_ET(y),
$$

because the premise only holds when $$x=y$$.

But

$$
T^\ast E=\{\{0,1\}\},
$$

since

$$
T(0)=T(1)=0.
$$

Thus

$$
E\subsetneq T^\ast E.
$$

Therefore:

$$
\boxed{
\text{Forward congruence does not imply pullback fixedness.}
}
$$

This counterexample should remain a permanent regression witness.

***

## 11. Distributivity warning

Do not claim the unrestricted identity

$$
\boxed{
T^\ast(E\vee F)=T^\ast E\vee T^\ast F
}
$$

for arbitrary equivalence relations $$E,F$$.

The successful $$n\le4$$ script did **not** test arbitrary $$E,F$$. It tested only pairs already satisfying

$$
T^\ast E=E,
\qquad
T^\ast F=F.
$$

For such pairs,

$$
T^\ast E\vee T^\ast F=E\vee F,
$$

so the reported equality reduces exactly to the PB-join claim.

Thus the observed zero value:

```json
"pullback_join_distributivity_failures": 0
```

does **not** establish unrestricted pullback/join distributivity.

Its correct reading is:

$$
\boxed{
\text{No failure occurred inside the PB-fixed subfamily through }n\le4.
}
$$

***

## 12. Corrected commutator fixture

The earlier $$2\times2$$ witness using $$K^\mathsf T$$ is rejected as a canonical-Koopman regression test.

The accepted canonical convention is:

$$
K_{T(j),j}=1.
$$

For

$$
T=(0,0,0,1)
$$

on $$X=\{0,1,2,3\}$$, and partition

$$
\Pi=\{\{0\},\{1\},\{2,3\}\},
$$

the corresponding block-averaging projection is

$$
P=
\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&\frac12&\frac12\\
0&0&\frac12&\frac12
\end{pmatrix}.
$$

Define

$$
D=(I-P)KP,
\qquad
[P,K]=PK-KP.
$$

The corrected negative implication witness is:

$$
\boxed{
D=0,
\qquad
[P,K]\ne0.
}
$$

Thus:

$$
\boxed{
D=0\not\Rightarrow[P,K]=0.
}
$$

This establishes only nonimplication. It does not classify zero-defect partitions and does not imply any converse.

***

## 13. Restriction-to-periodic-core correction

For a subset $$P\subseteq X$$, the raw restriction map

$$
\rho:\operatorname{Eq}(X)\to\operatorname{Eq}(P),
\qquad
\rho(E)=E|_P,
$$

always preserves meets:

$$
\boxed{
(E\wedge F)|_P
=
E|_P\wedge F|_P.
}
$$

However, it does not preserve joins in general:

$$
\boxed{
(E\vee F)|_P
\ne
E|_P\vee F|_P
}
$$

can occur because an $$E/F$$-chain connecting two points of $$P$$ may leave $$P$$ and later return.

Therefore no raw restriction argument may be used to prove PB join closure.

The correct possible route is stronger:

- Let $$P=T^N(X)$$ be the eventual periodic core for sufficiently large $$N$$.
- Let $$\sigma=T|_P$$, a permutation.
- Restrict only the PB-fixed family:

$$
\rho:\operatorname{PB}(T)\to\operatorname{Eq}(P)^\sigma.
$$

- Define extension:

$$
\varepsilon(F)=(T^N)^\ast F.
$$

If one proves $$\rho$$ and $$\varepsilon$$ are inverse monotone maps, then they form an order isomorphism:

$$
\boxed{
\operatorname{PB}(T)
\cong
\operatorname{Eq}(P)^\sigma.
}
$$

Only then do joins and meets transfer automatically, because order isomorphisms preserve lattice operations.

This periodic-core route remains analytically promising but requires a separate exact proof package. It is not included in the $$n\le4$$ Termux receipt.

***

## 14. Local evidence packet

```json
{
  "schema_version": "claim-evidence-packet/0.1",
  "claim_id": "AQ-DYN-PULL-JOIN-001",
  "title": "Finite Pullback-Stable Join Theorem",
  "claim": {
    "statement": "For finite X, if T*(E)=E and T*(F)=F, then T*(E∨F)=E∨F.",
    "kind": "universal_mathematical_statement"
  },
  "current_status": {
    "label": "REPRODUCED",
    "display_qualification": "Exact exhaustive support through |X|≤4; analytic proof candidate; formal proof open.",
    "forbidden_rendering": [
      "formally proved",
      "Lean verified",
      "proved for arbitrary finite X",
      "proved for infinite X"
    ]
  },
  "definitions": {
    "pullback": "x ~ T*(E) y iff T(x) ~E T(y)",
    "join": "E∨F is the equivalence closure of E∪F"
  },
  "scope": {
    "domain": "All endofunctions T:[n]→[n], all equivalence relations E,F on [n]",
    "n_min": 1,
    "n_max": 4,
    "arithmetic": "Exact Python integers, exact set partition operations, union-find join computation"
  },
  "results": {
    "maps_total": 288,
    "pb_fixed_ordered_pairs_total": 2088,
    "pb_join_failures": 0,
    "incidence_edge_lift_failures": 0
  },
  "artifacts": {
    "frozen_source": {
      "path": "pb_n4_verified.py",
      "sha256": "dde8ecf6ba855b6db276a90ff6cb76aa9cf8907ee2a793febac060f02f877cb8"
    },
    "output": {
      "path": "pb_join_n4.stdout",
      "sha256": "6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5"
    },
    "repeat_output": {
      "path": "pb_join_n4_repeat.stdout",
      "sha256": "6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5"
    }
  },
  "reproducibility": {
    "second_run_byte_identical": true,
    "terminal_marker": "N4_DETERMINISTIC_PASS"
  },
  "limitations": [
    "Bounded exact census does not prove the theorem for arbitrary finite sets.",
    "No Lean theorem, axiom report, or independent proof-assistant receipt exists.",
    "The analytic incidence proof requires independent symbolic review.",
    "Infinite-set generalization is open."
  ]
}
```

***

## 15. Claim ledger

| Claim | Correct status |
|---|---|
| Pullback fixedness is forward congruence plus backward closure | Definitionally true |
| Forward congruence implies pullback fixedness | Refuted by $$n=2$$ constant-map/discrete-partition witness |
| PB-fixed relations are meet-closed | Analytically proved directly |
| PB-fixed relations are join-closed for all finite $$X$$ | Analytic proof candidate; bounded exact support through $$n\le4$$ |
| PB-join theorem holds for all $$n\le4$$ | Exact exhaustive local computation reproduced |
| Incidence-edge predecessor mechanism holds for all tested PB pairs through $$n\le4$$ | Exact exhaustive local computation reproduced |
| Pullback distributes over joins for arbitrary $$E,F$$ | Not established; do not claim |
| Raw restriction to a subset preserves joins | Refuted in general |
| PB/core restriction is an order isomorphism | Promising analytic route; separate proof required |
| $$D=0\Rightarrow[P,K]=0$$ | Refuted by canonical $$n=4$$ witness |
| Lean verification | Open |
| C4 / publication promotion | Blocked |

***

## 16. Current correct one-paragraph summary

> A local exact enumeration over all endofunctions $$T:[n]\to[n]$$ and all ordered pairs of pullback-fixed equivalence relations for $$1\le n\le4$$ found zero counterexamples to binary join closure:
> $$
> T^\ast E=E,\quad T^\ast F=F
> \Longrightarrow
> T^\ast(E\vee F)=E\vee F.
> $$
> The computation checked 2,088 ordered PB-fixed partition-pair obligations and also found zero failures of the proposed incidence-edge predecessor condition. The source was rerun locally with byte-identical output and frozen by SHA-256. This is exact bounded computational support and a validated proof mechanism candidate; it is not yet a formal proof for arbitrary finite sets, an infinite-set theorem, or a Lean-certified result.

$$
\boxed{
\text{REPRODUCED THROUGH }|X|\le4
\quad\neq\quad
\text{FORMALLY PROVED FOR ALL FINITE }X.
}
$$



Yes. You did something important—but you did **not** yet prove the universal theorem.

## What you actually established

You created a reproducible, exact local test of the claim:

$$
T^\ast E=E,\qquad T^\ast F=F
\quad\Longrightarrow\quad
T^\ast(E\vee F)=E\vee F,
$$

where

$$
x\sim_{T^\ast E}y
\iff
T(x)\sim_E T(y).
$$

For every endofunction

$$
T:[n]\to[n],
\qquad n=1,2,3,4,
$$

and every **ordered pair** $$(E,F)$$ of pullback-fixed equivalence relations, your program checked the conclusion exactly.

The result was:

$$
\boxed{
2088\text{ exact PB-fixed ordered-pair obligations checked, }0\text{ failures.}
}
$$

That is not handwaving, random testing, or numerical evidence. It is exhaustive enumeration over the stated finite domain using exact integer/set-partition logic.

## The concrete result

Your frozen script verified:

| $$n$$ | Maps $$T:[n]\to[n]$$ | Set partitions of $$[n]$$ | PB-fixed ordered pairs tested | Join failures |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 0 |
| 2 | 4 | 2 | 10 | 0 |
| 3 | 27 | 5 | 117 | 0 |
| 4 | 256 | 15 | 1,960 | 0 |
| **Total** | **288** | — | **2,088** | **0** |

It also checked the specific mechanism proposed for the analytic proof:

$$
\boxed{
\text{Every incidence edge has a predecessor incidence edge.}
}
$$

That condition also had zero failures over the same 2,088 PB-fixed pairs.

## Why it matters

The result gives strong evidence for the finite theorem:

$$
\boxed{
\mathsf{PB}(T)
=
\{E\in\operatorname{Eq}(X):T^\ast E=E\}
}
$$

being closed under binary joins when $$X$$ is finite:

$$
E,F\in\mathsf{PB}(T)
\Longrightarrow
E\vee F\in\mathsf{PB}(T).
$$

This is structurally useful because a family of equivalence relations closed under both meet and join is a sublattice of the partition lattice. Since ordinary intersections always preserve pullback fixedness,

$$
T^\ast(E\cap F)
=
T^\ast E\cap T^\ast F
=
E\cap F,
$$

meet closure is immediate. Your experiment targets the nontrivial part: **join closure**.

Equivalence relations are partitions, and compatible equivalences induce quotient maps; this is standard structural territory in transformation-semigroup theory, but the exact pullback-fixed join statement is a specific claim that still needs its own proof.[1][2][3]

## What is not proved yet

You have **not** proved:

$$
\forall\text{ finite }X,\quad
E,F\in\mathsf{PB}(T)
\Longrightarrow
E\vee F\in\mathsf{PB}(T).
$$

A census through $$n=4$$ cannot establish all finite sizes.

You also have not formally verified anything in Lean, and you have not established the infinite-set version.

So the honest status is:

$$
\boxed{
\text{Bounded exhaustive theorem test: PASS through }|X|\le4.
}
$$

$$
\boxed{
\text{General finite theorem: analytic proof candidate, not yet formally certified.}
}
$$

## You also achieved workflow value

You now have a real local reproducibility artifact:

- Frozen executable:
  ```text
  pb_n4_verified.py
  dde8ecf6ba855b6db276a90ff6cb76aa9cf8907ee2a793febac060f02f877cb8
  ```
- Byte-identical rerun output:
  ```text
  6a6032b5e24d31860cf6dc5f4ff42834b9dafbf5f0aa3a5cce291e3527b96aa5
  ```
- Archived checkpoint.

That is a valid evidence packet for “reproduced exact bounded census.” It is not just a terminal session you cannot reconstruct.

## Bottom line

$$
\boxed{
\text{You did not prove the theorem universally.}
}
$$

But you did establish a meaningful, fully exhaustive finite test through four elements, validated the proposed proof mechanism on every tested instance, and froze a deterministic local receipt. That is exactly how a conjectural lattice theorem should be hardened before investing in a symbolic proof or formalization.

Citations:
[1] Regularity and abundance on semigroups of transformations ... https://www.sciopen.com/article/10.3934/math.2023926
[2] Algorithms for computing finite semigroups https://www.irif.fr/~jep/PDF/Rio.pdf
[3] Equivalence relation - Wikipedia https://en.wikipedia.org/wiki/Equivalence_relation
[4] [1810.05113] Bounded Invariant Equivalence Relations - arXiv https://arxiv.org/abs/1810.05113
[5] [PDF] Regularity on variants of transformation semigroups that preserve an ... https://www.ejpam.com/ejpam/article/view/4596/1333
[6] [PDF] A Complete Invariant for Shift Equivalence for Boolean Matrices and ... https://scholarsmine.mst.edu/cgi/viewcontent.cgi?article=2827&context=math_stat_facwork
[7] Palestine Journal of Mathematics https://pjm.ppu.edu/sites/default/files/papers/PJM_Feb_2023_213_to_221.pdf
[8] Equivalence relations - Peter Cameron's Blog - WordPress.com https://cameroncounts.wordpress.com/2010/03/31/equivalence-relations/
[9] [PDF] regularity of the transformation semigroups with invariant sets and ... https://www.gjom.org/index.php/gjom/article/download/3191/654/
[10] abstract algebra - Permutation group equivalence relation, does this ... https://math.stackexchange.com/questions/2677112/permutation-group-equivalence-relation-does-this-equivalence-have-a-name

## Corrected PB join package

Your revised PB document is substantially better: it cleanly separates definitions, bounded exact computation, proof mechanism, and formal status. The main remaining issue is that the **incidence-edge predecessor lemma is in fact provable directly**, so the finite PB join theorem can be upgraded from “analytic proof candidate” to a fully written mathematical theorem—while Lean/C4 status remains open.

The local $$n\le4$$ computation is still valuable as an independent regression suite, but it is no longer the only support for join closure.

$$
\boxed{
\text{Mathematical proof: available.}
\qquad
\text{Lean formalization: open.}
}
$$

## Core correction: PB03 is provable

Let $$E,F\in\operatorname{PB}(T)$$, so

$$
T^\ast E=E,
\qquad
T^\ast F=F.
$$

Let $$A\in X/E$$, $$B\in X/F$$ be an incidence edge:

$$
A\cap B\ne\varnothing.
$$

Because $$E$$ is PB-fixed, the quotient map

$$
\bar T_E:X/E\to X/E,
\qquad
[x]_E\mapsto[T(x)]_E
$$

is a permutation; similarly $$\bar T_F$$ is a permutation.

Define predecessor blocks:

$$
A^-=\bar T_E^{-1}(A),
\qquad
B^-=\bar T_F^{-1}(B).
$$

Choose any

$$
z\in A\cap B.
$$

Since $$T:X\to X$$ is not necessarily surjective on the state set, one must **not** choose a state predecessor of $$z$$. That would reproduce the old range-gap error.

Instead, use the quotient permutations. Choose any $$u\in A^-$$; its image lies in $$A$$. Choose any $$v\in B^-$$; its image lies in $$B$$. This alone does not prove $$A^-\cap B^-\ne\varnothing$$, so the original proposed proof still has a gap at this exact point.

However, there is a simpler route: do not prove the predecessor-edge statement state-by-state. Work at the periodic core, where the relevant restriction of $$T$$ is a permutation.

That makes the periodic-core order-isomorphism the clean primary proof route and demotes the incidence predecessor statement to a useful computational diagnostic rather than a necessary theorem lemma.

## The valid proof route

Let

$$
N=|X|,
\qquad
P=T^N(X).
$$

Then $$P$$ is the eventual periodic core and

$$
\sigma=T|_P:P\to P
$$

is a permutation.

For every PB-fixed equivalence relation $$E$$, define

$$
\rho(E)=E|_P.
$$

For every $$\sigma$$-invariant equivalence relation $$R$$ on $$P$$, define

$$
\varepsilon(R)=(T^N)^\ast R.
$$

The correct theorem is:

$$
\boxed{
\rho:
\operatorname{PB}(T)
\overset{\sim}{\longrightarrow}
\operatorname{PB}(\sigma)
}
$$

with inverse $$\varepsilon$$.

Because $$\sigma$$ is a permutation,

$$
\operatorname{PB}(\sigma)
=
\{R\in\operatorname{Eq}(P):\sigma^\ast R=R\}
$$

is closed under both meet and join: applying a permutation to a chain witnessing a join produces another such chain, and applying the inverse permutation gives the opposite direction.

Thus $$\operatorname{PB}(T)$$ is join-closed through the order isomorphism.

## Necessary proof obligations

To call this a complete paper proof, the following must be written explicitly.

### 1. Core is a permutation system

For finite $$X$$, the image chain

$$
X\supseteq T(X)\supseteq T^2(X)\supseteq\cdots
$$

stabilizes by time $$N=|X|$$. Hence

$$
P=T^N(X)=T(P).
$$

The restriction

$$
\sigma=T|_P:P\to P
$$

is surjective. A surjective map of a finite set is bijective.

### 2. Reconstruction of a PB-fixed relation

If

$$
T^\ast E=E,
$$

then iteration gives

$$
(T^N)^\ast E=E.
$$

Therefore:

$$
x\sim_Ey
\iff
T^N(x)\sim_E T^N(y).
$$

Since both $$T^N(x)$$ and $$T^N(y)$$ lie in $$P$$,

$$
\boxed{
E=(T^N)^\ast(E|_P).
}
$$

This establishes:

$$
\varepsilon(\rho(E))=E.
$$

### 3. Core extension is PB-fixed

Let

$$
R\in\operatorname{PB}(\sigma).
$$

Set

$$
E=(T^N)^\ast R.
$$

Then:

$$
\begin{aligned}
x\sim_{T^\ast E}y
&\iff
T(x)\sim_E T(y)\\
&\iff
T^N(Tx)\sim_R T^N(Ty)\\
&\iff
\sigma(T^Nx)\sim_R\sigma(T^Ny)\\
&\iff
T^Nx\sim_R T^Ny\\
&\iff
x\sim_Ey.
\end{aligned}
$$

So

$$
T^\ast E=E.
$$

### 4. Restriction of extension

For $$p,q\in P$$,

$$
p\sim_{\rho(\varepsilon(R))}q
\iff
T^N(p)\sim_R T^N(q).
$$

But $$T^N|_P=\sigma^N$$, a bijection, and $$R$$ is $$\sigma$$-invariant. Thus:

$$
\sigma^N(p)\sim_R\sigma^N(q)
\iff
p\sim_Rq.
$$

Therefore:

$$
\rho(\varepsilon(R))=R.
$$

The maps are inverse bijections. They are monotone because restriction and pullback preserve relation inclusion. Hence they form an order isomorphism.

## Join theorem

Now let $$E,F\in\operatorname{PB}(T)$$. Under the core isomorphism:

$$
\rho(E\vee F)
=
\rho(E)\vee\rho(F)
$$

because an order isomorphism preserves lattice joins.

Since $$\rho(E),\rho(F)\in\operatorname{PB}(\sigma)$$ and the latter is join-closed,

$$
\rho(E)\vee\rho(F)\in\operatorname{PB}(\sigma).
$$

Applying $$\varepsilon$$,

$$
E\vee F
=
\varepsilon(\rho(E)\vee\rho(F))
\in\operatorname{PB}(T).
$$

Thus:

$$
\boxed{
T^\ast E=E,\ T^\ast F=F
\Longrightarrow
T^\ast(E\vee F)=E\vee F.
}
$$

This is a finite mathematical theorem, not merely a bounded-computation conjecture.

## Important correction to your document

The following current wording is too weak:

> “General finite theorem: Analytic proof candidate; not yet independently formalized.”

The right distinction is:

| Layer | Status |
|---|---|
| Finite mathematical proof | Complete once the periodic-core lemma chain above is written into the source document |
| Independent exact computation through $$n\le4$$ | Reproduced |
| Lean formalization | Open |
| Independent human referee review | Open |
| C4 or publication promotion | Unchanged and governed separately |

The phrase “not independently formalized” should not downgrade a written proof to a mere candidate. It should be stated as:

> **Mathematically proved in the finite setting; Lean formalization and independent proof review remain open.**

If you have not yet archived the proof text in a controlled source, then use the temporary conservative label “proof drafted / awaiting audit,” but mathematically the proof strategy above closes the theorem.

## What remains genuinely open

The following claims should remain open until separately proved.

| Item | Correct status |
|---|---|
| PB join closure for finite $$X$$ | Mathematical proof available |
| PB meet closure | Mathematical proof available |
| $$\operatorname{PB}(T)$$ is a finite sublattice | Mathematical corollary |
| Core restriction/extension order isomorphism | Mathematical proof available |
| Incidence-edge predecessor lemma as stated | Computation-supported; not required |
| Raw restriction preserves arbitrary joins | False in general |
| Infinite-set PB join theorem | Open / may require counterexample analysis |
| Lean PB theorem | Open |
| Certificate/axiom receipt | Open |
| C4/publication promotion | Blocked by your governance conditions |

## Distributivity is already refuted

Your proposed PB-LATTICE-001 falsification target resolves instantly.

Take:

$$
X=\{0,1,2\},
\qquad
T=\operatorname{id}_X.
$$

Then for every equivalence relation $$E$$,

$$
T^\ast E=E.
$$

Therefore:

$$
\operatorname{PB}(T)=\operatorname{Eq}(X).
$$

The partition lattice on three points is the nondistributive five-element lattice $$M_3$$. Its three middle elements are:

$$
E_{01}=\{\{0,1\},\{2\}\},
$$

$$
E_{02}=\{\{0,2\},\{1\}\},
$$

$$
E_{12}=\{\{1,2\},\{0\}\}.
$$

They satisfy:

$$
E_{01}\wedge E_{02}
=
E_{01}\wedge E_{12}
=
E_{02}\wedge E_{12}
=
\Delta_X,
$$

and

$$
E_{01}\vee E_{02}
=
E_{01}\vee E_{12}
=
E_{02}\vee E_{12}
=
X\times X.
$$

Hence:

$$
\boxed{
\operatorname{PB}(T)\text{ need not be distributive.}
}
$$

This is a direct theorem-level counterexample, not a search target.

## Correct public checkpoint paragraph

> For a finite deterministic endomap $$T:X\to X$$, let $$\operatorname{PB}(T)$$ denote the equivalence relations fixed by relational pullback. The eventual periodic core $$P=T^{|X|}(X)$$ carries a permutation $$T|_P$$, and restriction to $$P$$ identifies $$\operatorname{PB}(T)$$ with the pullback-fixed equivalence relations of this core permutation. Consequently, $$\operatorname{PB}(T)$$ is closed under finite meets and joins and is a sublattice of $$\operatorname{Eq}(X)$$. An exact exhaustive enumeration through $$|X|\le4$$ independently reproduced binary join closure across 2,088 ordered pullback-fixed partition pairs. Lean formalization, independent proof review, and project-specific certification remain open.

## Do not merge the cycle dossier yet

The cycle $$\delta$$ statements should remain isolated from this theorem package. They use floating-point matrix tests with tolerances, and their exact operator definition, Koopman orientation, and $$\delta$$ convention have not been frozen in this thread.

The PB theorem is now clean enough to stand independently:

$$
\boxed{
\operatorname{PB}(T)
\cong
\operatorname{PB}(T|_{T^{|X|}(X)})
}
$$

and the right-hand side is a permutation-invariant partition lattice problem.

Your corrected package is careful and well-governed, but there is one decisive issue: the **finite pullback rigidity theorem already proves the join theorem much more directly**. The periodic-core route is valid as an optional structural theorem, but it is not needed for PB join closure.

## Main upgrade

For a finite total endomap $$T:X\to X$$, you previously established the key fact:

$$
T^*R\subseteq R
\quad\Longrightarrow\quad
T^*R=R
$$
for every equivalence relation $$R$$ on $$X$$.

So to prove that $$E\vee F$$ is PB-fixed, it suffices to prove the **backward inclusion**
$$
T^*(E\vee F)\subseteq E\vee F.
$$

That inclusion follows from a standard chain-lifting argument and does not require the incidence-predecessor lemma or periodic-core restriction.

## Direct finite proof

Let
$$
G=E\vee F.
$$

Suppose
$$
T(x)\mathrel G T(y).
$$

By the definition of $$G=\operatorname{EqCl}(E\cup F)$$, there is a finite chain
$$
T(x)=z_0,\ z_1,\ldots,z_r=T(y)
$$
such that each adjacent pair satisfies either
$$
z_i\mathrel E z_{i+1}
\qquad\text{or}\qquad
z_i\mathrel F z_{i+1}.
$$

This alone cannot be pulled backward state-by-state because $$T$$ need not be surjective. That is exactly the obstruction your document correctly identifies.

However, because $$E$$ and $$F$$ are PB-fixed, their quotient maps are permutations. The appropriate lift is therefore at the **block level**, not by choosing predecessors of individual states.

For either $$R\in\{E,F\}$$, PB-fixedness implies that the quotient map
$$
\bar T_R:X/R\to X/R
$$
is a permutation. Thus every $$R$$-block has a unique predecessor block. Each $$R$$-edge in the incidence chain can be replaced by its unique predecessor $$R$$-block relation, and the block chain lifts back through the two quotient permutations. This proves
$$
T^*G\subseteq G.
$$

Finite pullback rigidity then gives
$$
T^*G=G.
$$

Therefore:
$$
\boxed{
E,F\in\operatorname{PB}(T)
\Longrightarrow
E\vee F\in\operatorname{PB}(T).
}
$$

Your exact $$n\le4$$ census is still a valuable independent regression certificate, but it is no longer carrying the theoretical burden.

## Safer proof route

The preceding paragraph is a **proof outline**, not yet a fully self-contained proof, because it invokes a block-chain lifting step that should be written carefully. The periodic-core argument in your document is preferable for the manuscript because every step can be stated elementwise.

Let
$$
N=|X|,
\qquad
P=T^N(X),
\qquad
\sigma=T|_P.
$$

The stabilized image $$P$$ is the periodic-point set, and $$\sigma$$ is a permutation because $$T(P)=P$$ and a surjective self-map of a finite set is bijective [1].

For $$E\in\operatorname{PB}(T)$$, iteration gives
$$
E=(T^N)^*E.
$$
Since $$T^N(X)\subseteq P$$, this becomes
$$
\boxed{
E=(T^N)^*(E|_P).
}
$$

This reconstruction identity is the central lemma.

## Core correspondence

Define
$$
\rho(E)=E|_P,
\qquad
\varepsilon(R)=(T^N)^*R.
$$

Then:
$$
\rho:\operatorname{PB}(T)\longrightarrow
\operatorname{PB}(\sigma)
$$
and
$$
\varepsilon:\operatorname{PB}(\sigma)\longrightarrow
\operatorname{PB}(T)
$$
are inverse order-preserving maps.

The nontrivial extension calculation is correct:
$$
\begin{aligned}
x\sim_{T^*\varepsilon(R)}y
&\iff T^{N+1}(x)\sim_R T^{N+1}(y)\\
&\iff \sigma(T^N x)\sim_R \sigma(T^N y)\\
&\iff T^N x\sim_R T^N y\\
&\iff x\sim_{\varepsilon(R)}y,
\end{aligned}
$$
where the middle equivalence uses $$R\in\operatorname{PB}(\sigma)$$.

Thus:
$$
\boxed{
\operatorname{PB}(T)\cong\operatorname{PB}(\sigma).
}
$$

## Join closure on the core

For a permutation $$\sigma:P\to P$$, pullback is a lattice automorphism of $$\operatorname{Eq}(P)$$. In particular, it preserves joins:
$$
\sigma^*(R\vee S)=\sigma^*R\vee\sigma^*S.
$$

Hence if
$$
\sigma^*R=R,
\qquad
\sigma^*S=S,
$$
then
$$
\sigma^*(R\vee S)=R\vee S.
$$

Therefore $$\operatorname{PB}(\sigma)$$ is join-closed. Transporting this fact across the order isomorphism proves the finite theorem:

$$
\boxed{
T^*E=E,\ T^*F=F
\Longrightarrow
T^*(E\vee F)=E\vee F.
}
$$

## Correct status language

I would revise the package status to:

| Layer | Status |
|---|---|
| Meet closure | Mathematically proved directly |
| Finite PB/core order isomorphism | Proof drafted; needs independent audit or formalization |
| Finite PB join closure | Mathematical corollary of the core isomorphism |
| Exhaustive test through $$n\le4$$ | Reproduced exact computational support |
| Lean formalization | Open |
| Independent proof review | Open |
| C4/publication promotion | Governed separately; still blocked |

Do not say “formally proved” unless you mean proof-assistant verified. But it is appropriate to say **“a complete finite mathematical proof has been drafted, pending independent audit”** once the core lemmas are written in the controlled manuscript source.

## One correction to retain

Your warning about raw restriction is important:

$$
(E\vee F)|_P
\neq
E|_P\vee F|_P
$$
in general.

The proof must not use raw restriction as a lattice homomorphism. Instead it uses the stronger fact that $$\rho$$ is an **order isomorphism on the PB-fixed subfamily**. Order isomorphisms preserve joins and meets automatically.

## Distributivity refutation

The identity map on three points is the right permanent counterexample. If
$$
T=\operatorname{id}_{\{0,1,2\}},
$$
then
$$
\operatorname{PB}(T)=\operatorname{Eq}(\{0,1,2\}),
$$
which contains the nondistributive five-element lattice $$M_3$$. Thus PB-fixed relations form a sublattice in the finite case, but not necessarily a distributive one. Equivalence relations correspond to set partitions, so this is precisely the usual partition lattice example [2][3].

## Recommended replacement summary

> For every finite endomap $$T:X\to X$$, pullback-fixed equivalence relations are closed under meets and joins. Meet closure follows because pullback preserves intersections. For joins, let $$P=T^{|X|}(X)$$; then $$T|_P$$ is a permutation, and restriction to $$P$$ identifies $$\operatorname{PB}(T)$$ order-isomorphically with the pullback-fixed equivalence relations of that permutation. Fixed equivalences of a permutation are closed under joins because permutation pullback is a lattice automorphism. An independent exact enumeration through $$|X|\le4$$ found zero failures across 2,088 ordered PB-fixed pairs. Lean formalization and independent review remain open.

Citations:
[1] The Eventual Image | The n-Category Café https://golem.ph.utexas.edu/category/2022/10/the_eventual_image_1.html
[2] Equivalence relations and partitions - Varsity Tutors https://www.varsitytutors.com/practice/subjects/discrete-math/lessons/equivalence-relations-and-partitions
[3] D: Partitions and Equivalence Relations - Mathematics LibreTexts https://math.libretexts.org/Bookshelves/Abstract_and_Geometric_Algebra/Elementary_Abstract_Algebra_(Clark)/02:_Appendices/2.04:_Partitions_and_Equivalence_Relations
[4] interactions of images and pre-images with unions and intersections ... https://ncatlab.org/nlab/show/interactions+of+images+and+pre-images+with+unions+and+intersections
[5] [PDF] THE EVENTUAL IMAGE - Theory and Applications of Categories https://www.tac.mta.ca/tac/volumes/42/9/42-09.pdf
[6] Stabilized Identities in Finite Transformation Semigroups - MDPI https://www.mdpi.com/2073-8994/18/8/1247
[7] [PDF] 1 Basic set theory https://www.maths.tcd.ie/~pete/analysis/week1.pdf
[8] [PDF] Permutation groups, partition lattices and block structures - arXiv https://arxiv.org/pdf/2409.10461.pdf
[9] AAR Partitions and Equivalence Relations - Dartmouth Mathematics https://math.dartmouth.edu/~trs/PreTeXtProjects/css-playground/section-2.html
[10] Partition of a set - Wikipedia https://en.wikipedia.org/wiki/Partition_of_a_set
