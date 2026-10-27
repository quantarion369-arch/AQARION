# AQARION extremal recognizer and one-edge inspector

## Purpose

A reusable binary extremal-register recognizer and a browser case inspector.

The page contains exact precomputed results for all 64 source/target
selections, corresponding to 57 distinct maps obtained by replacing
one edge of the eight-state baseline.

It is not an arbitrary live computation API.

## Baseline and mutation

Observation:
    (0,0,0,0,1,1,1,1)

Baseline:
    (0,2,4,6,0,2,4,6)
    exact profile [1,4,7,8]

One-edge change:
    (0,2,4,6,0,2,4,7)
    exact profile [1,5,8,8]

## Recognizer outcomes

PREFIX_COLLISION:
A pair of states shares the first d observations. This excludes the
specified separating extremal class, but does not alone decide
longer-time separation.

NONLITERAL_TERMINAL:
The prefix is bijective, but its terminal table is not constant or
a signed coordinate literal. Completeness of the negative extremal
classification uses the spectral-to-register theorem.

EXTREMAL_REGISTER:
The prefix is bijective and the terminal has the required form.
The recognizer supplies the encoding, terminal rule, parity weights,
and theorem-derived rank profile.

## Evidence distinctions

The recognizer does not compute ranks.

The builder separately computes exact ranks with the previously
preserved standard-library rational checker and compares the outcomes.

It explicitly verifies the positive parity certificate against all
degree-at-most-two temporal features for this eight-state experiment.

This is not a formal Lean proof, independent literature review,
comprehensive security audit, or promotion decision.

## Integration boundary

The production RAG server, retrieval routes, corpus, and relationship
registry are unchanged.

After the page is used successfully, it can be installed as an additional
case view in the existing workbench. A separate server is not required.

## Files

recognizer.py       reusable classification function
build_inspector.py  exact case generator and focused checks
cases.json          computed data
verification.json   execution scope and outcomes
inspector.html      self-contained browser page
page-template.html  maintained page template
stdout.txt          execution output
stderr.txt          execution errors, if any
python_exit.txt     process exit status
SHA256SUMS          file fingerprints
