# AQARION certificate-frontier team handoff

Date: 2026-10-26
Owner: James Aaron
Repository: quantarion369-arch/AQARION
Package: AQARION-QUANTARION-AI/research/neutrino-moment-benchmarks/certificate-frontier

## 1. Immediate status and next action

The eight-file benchmark was committed locally as:
a14bc4c85875eacb24bcaf813449f17d207be496

That commit preserves the source, inputs, user-transcribed earlier
receipt, and subsequently captured file-bound replay.

This handoff is added in a separate follow-up commit. The package
then contains nine files. SHA256SUMS is updated rather than duplicated.

Publication remains a separate operation. At handoff creation:
- The base commit is confirmed by the supplied local terminal receipt.
- A push of this package has not been established.
- Do not assume GitHub main already contains these commits.
- Next: inspect destination and outgoing commits, obtain push approval,
  push without force, then verify the remote commit.
- Do not begin another research sweep before closing this checkpoint.

## 2. Purpose

This package compares explicit nonnegative polynomial weights for
detecting a sign change from uncertain angular moments.

It separates:
1. Exact observation ambiguity.
2. Assumptions about the admissible function family.
3. Certificate robustness under specified moment errors.
4. Numerical implementation and evidence provenance.

It does not introduce a new neutrino instability theory.

## 3. Mathematical fixture

Angular coordinate:
  mu in [-1,1]

Third Legendre polynomial:
  P3(mu) = (5*mu^3 - 3*mu)/2

Family:
  G_a(mu) = 1/10 + a*P3(mu)

The frontier calculation fixes a=1/5:
  G(mu) = 1/10 - 3*mu/10 + mu^3/2

Toy occupations:
  f_antinue(mu) = 1/2
  f_nue(mu) = 3/5 + a*P3(mu)

The tested a=0 and a=1/5 occupations lie between zero and one.
This is a controlled occupation-function example, not a
self-consistent supernova transport calculation.

Define:
  s_j = integral[-1,1] mu^j dmu
      = 2/(j+1) for even j, and zero for odd j.

Fixture moments:
  m_j = s_j/10 + (5*s_(j+3) - 3*s_(j+1))/10.

Within the family:
  M0 = 1/5
  M1 = 0
  M2 = 1/15
  M3 = 4*a/35.

Thus low moments through degree two do not determine a or crossing
status. M3 identifies a only under the stated family restriction.

Crossing means taking both strictly positive and strictly negative
values. An endpoint zero alone is not counted as a crossing.

## 4. Why the nonnegative weight matters

For a normalized weight:
  W(mu) >= 0
  integral W = 1

A strictly negative integral of W*G establishes negative values of G.
A strictly positive integral of G establishes positive values of G.
For continuous compatible functions, these establish a crossing.

A signed reconstruction kernel does not have this implication.
In a separate Backus-Gilbert investigation, the degree-seven kernel
was found to take negative values. Its negative estimate therefore
was not accepted as a general crossing certificate.

This package uses structurally nonnegative constructions instead.

## 5. Candidate catalog

Thirty-eight weights are compared.

Three square-based weights have unnormalized form:
  (1-mu)*p(mu)^2

Polynomial coefficients are listed constant term first.

old11:
  [-8, 24, 20, -51, 84, -100]

new11:
  [21, -33, -60, -127, -514, 1000]

simple13:
  [0, -1, -1, -3, -6, -25, 50]

The other thirty-five weights have unnormalized form:
  (1-mu)^r, for integer r=3,...,37.

Each weight is normalized by its exact positive integral.
Nonnegativity follows from the factors on [-1,1], not grid sampling.

## 6. Error model and threshold

Assume:
  |Delta M_j| <= delta*a_j.

Three declared profiles:
  equal:      a_j = 1
  linear:     a_j = 1+j/10
  geometric:  a_j = (11/10)^j

These are illustrative scenarios, not measured sensor uncertainties.

For coefficients w_j of normalized W:
  I = sum_j w_j*m_j
  L = sum_j |w_j|*a_j
  worst-case upper bound = I + delta*L.

A negative upper bound requires:
  delta < -I/L, when I<0.

Thresholds are strict. Equality does not establish strict negativity.

These are bounds for a specified moment box. The box corners
attaining a linear bound need not be physically jointly realizable.
Conservative bounds remain valid for physical distributions inside it.

Crossing additionally requires positive total integral. All positive
reported candidate thresholds are below 1/5 and all profiles have
a_0=1, so a single box centered at the fixture retains M0>0 when
delta is below those thresholds.

Uniform guarantees over displaced measured centers plus their own
uncertainty boxes require accounting for both budgets. Do not
silently promote a single-box threshold to a doubled-budget guarantee.

## 7. Selected exact single-box thresholds

old11:
  equal:
    35723537/29654024400
  linear:
    71447074/108662278725
  geometric:
    11163605312500/20798495299655073

new11:
  equal:
    515138509/319709590200
  linear:
    1030277018/1264800101565
  geometric:
    643923136250000/1021203794368676919

simple13:
  equal:
    40500847/19894574700
  linear:
    40500847/43459461045
  geometric:
    101252117500000/154569839188465701

power37:
  equal:
    122/50635
  linear:
    488/577239
  geometric:
    33535104647168000000000000000000000000000000000000/
    84643714786604304859650997024073002629122615446856907

The two lines of the final fraction denote one numerator/denominator.

Historical correction:
An earlier proposed checker mistyped the old11 equal-error
denominator as 29654063370. The correct value is 29654024400.
The saved passing implementation uses the corrected value.

## 8. Frontier result

Best candidates within this finite catalog:

Available degree 11:
  new11 wins under all three profiles.

Available degree 13:
  simple13 wins under all three profiles.

Available degree 20:
  simple13 wins under all three profiles.

Available degree 37:
  equal errors: power37
  linear errors: simple13
  geometric errors: simple13

Main result:
The preferred certificate depends on the error profile, not just
the highest available moment.

No global optimality or minimum-degree claim is established.
An unchanged winner between budgets does not prove that unsearched
weights at intermediate degrees cannot improve it.

## 9. Separate degree-13 doubled-budget checkpoint

For simple13:
  Z = 7331596/9009
  I = -40500847/1557964150
  equal-error L1 = 23405382/1832899.

At delta=1/1000:
  I + 2*delta*L1 = -1779244/3894910375 < 0
  M0 - 2*delta = 99/500 > 0.

This exact certificate was separately reported as passing on Termux.
Its earlier standalone execution log is not included in this package.
Do not label it as a second independently captured execution here.

## 10. Implementation and execution environment

Working interpreter recorded in the successful environment:
  /root/.venvs/aqarion-flint-090/bin/python

Python-FLINT:
  0.9.0

The path is environment-specific, not a portable installation rule.
Native Termux Python and Ubuntu's system Python did not expose this
venv's FLINT installation during the locator checks.

The replay compares:
- FLINT polynomial expansion against Fraction coefficient expansion.
- FLINT exact integration against Fraction monomial integration.
- Weighted integrals computed by both paths.
- Four selected equal-error thresholds against exact references.

The frontier run completed:
  candidates = 38
  checks = 321
  exit code = 0.

These are exact rational calculations. Decimal values are display only.

## 11. Evidence provenance and file inventory

README.md
  Package overview and reproduction instructions.

frontier_check.py
  Saved replay implementation, assembled from the accepted chat method.
  Its saved bytes were subsequently executed through Ubuntu Python.

inputs.json
  Fixture, candidate definitions, profiles, and degree budgets.
  The script contains equivalent hardcoded definitions; it does not
  dynamically load this JSON. Keep both synchronized if changing inputs.

receipts/user-reported-frontier.json
  Structured transcription of an earlier user-supplied chat receipt.
  Not an original stdout capture.

receipts/file-bound-replay.stdout.txt
  Actual stdout captured during execution of the saved source bytes.

receipts/file-bound-replay.stderr.txt
  Actual stderr, including retained PRoot binding warnings.

receipts/file-bound-replay.json
  Execution command, source/output hashes, exit status, and comparisons
  of twelve exact thresholds and twelve winner entries against the
  earlier user transcription.

SHA256SUMS
  Hashes of all package files except SHA256SUMS itself.
  Updated to include this handoff.

TEAM_HANDOFF.md
  This document. It is explanatory documentation, not another run.

Verified replay source SHA256:
  53bcf2f4c0378ec45688844e5c53c08a376c85c2af43cd74ee2a874789b5482a

The captured stdout reports zero files created by the mathematical
program. Its outer capture wrapper did write the receipt artifacts.
Do not confuse those two scopes.

The original execution lacked an execution-time source hash.
The later file-bound replay closes that gap for the saved replay,
not retrospectively for the earlier run.

## 12. Reproduction

Inside a compatible Python environment with python-flint:
  python -B -I frontier_check.py

On the recorded phone, a Termux caller can use PRoot-Distro and
the explicit Ubuntu venv interpreter.

If importing flint fails:
- Inspect the interpreter path first.
- Do not assume the mathematics failed.
- Do not reinstall or modify unrelated environments automatically.

SHA256SUMS should be checked before changing or executing source.
A new independent execution should produce a separately labeled receipt.
Do not overwrite the existing successful capture.

## 13. Related work and boundaries

Positive-polynomial detection of angular crossings is prior art.
Relevant starting source:
Johns and Nagakura, Fast flavor instabilities and the search for
neutrino angular crossings, arXiv:2104.04106.
https://arxiv.org/abs/2104.04106

FLINT rational-polynomial documentation:
https://python-flint.readthedocs.io/en/latest/fmpq_poly.html

This package is a reproducible finite-catalog comparison and exact
robustness calculation. Novelty of a broader algorithm is undetermined.

It does not establish:
- A new crossing or instability theorem.
- Globally optimal certificates.
- Minimum required moment degree.
- Measured astrophysical error distributions.
- Nonlinear neutrino conversion.
- Physical-unit growth rates.
- Interval-certified roots of the dispersion determinant.
- A global count of unstable roots.
- Lean formalization or formal-status promotion.

Related completed work discussed in the research session includes
dispersion-root reproduction, angular-resolution comparisons,
external diagnostic reconstruction, and Hilbert conditioning tests.
Their complete source/receipt packages are not contained here.

## 14. Integration boundaries

Keep this research package under research/.

RAG integration, if requested later:
- Reference a committed revision and exact source paths.
- Do not equate retrieval with independent verification.
- Preserve limitations alongside positive results.

Lean integration, if requested later:
- Formalize a precisely stated implication separately.
- Do not relabel a numerical receipt as a Lean proof.

No application, registry, training, or production-service changes are
part of this package.

## 15. Team operating rules

- Finish the publication checkpoint before another research sweep.
- Do not rerun completed work merely to collect another PASS.
- Preserve failed outputs as failures.
- Do not weaken tolerances to force success.
- Distinguish proof, exact computation, numerical evidence, and proposal.
- Keep user-transcribed receipts separate from captured output.
- Search numerically if useful; verify accepted candidates exactly.
- Use the same uncertainty model when comparing candidates.
- Keep global optimality separate from best candidate found.
- Do not install, fork, record sensors, or publish without approval.
- Never stage unrelated files with a broad git add.

## 16. Next work after publication

First close the current publication:
1. Verify the two local package commits.
2. Inspect origin's push destination and outgoing commit range.
3. Obtain authorization for the exact push.
4. Push without force and verify the remote commit.
5. Record the publication result without inventing CI success.

Only then select a bounded next task:
- Extend certificate discovery for one declared uncertainty profile.
- Seek exact upper bounds or dual certificates for optimality.
- Improve a single user-facing AQARION entry point.
- Pursue local dispersion-root enclosure as a separate deliverable.

Do not launch all of these in parallel by default.
