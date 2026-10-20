
# Preserved retrieval development evidence

These reports retain the original executions and the explicit M02 label review.
The original baseline is not overwritten by its reviewed interpretation.

No experimental ranker was promoted. No semantic-abstention or general
answerability claim follows from these measurements.

The maintained runner and cases.json are outside this historical directory.
Experimental scripts and the original runner here retain historical assumptions.

SHA256SUMS at the benchmarks directory level covers the preserved files.
Checksums provide consistency checks, not independent validation.

## Immediate-neighbor context experiment

At implementation commit 482af5384b280c647f976aa89602c0d99411d56d,
a local 24-case experiment reproduced every baseline top-three result and
added the immediately preceding and following nonempty paragraphs from each
seed's pinned document. Expansion was nonrecursive, deduplicated per query,
and capped at six supplementary passages.

Single-passage support remained 12/16. Complete multi-passage support increased
from 1/4 to 3/4; required evidence-group coverage increased from 4/8 to 6/8.
M01 and M03 became complete. M04 and the four single-passage misses remained
unresolved.

The experiment added 112 supplementary passage occurrences and 15,983
characters to 69 seed occurrences and 21,810 seed characters. These are
per-query totals, not globally unique passage counts. The expanded budget
must not be presented as an equal-budget ranking improvement.

All returned citation slices reconstructed. Supplementary passages remain
context-only, not adjudicated supporting evidence. Unsupported queries also
received additional context. No answer-generation or abstention validation
was performed.

The experiment is preserved under benchmarks/evidence/2026-10-19/adjacency/.
It was executed locally, not by the existing CI benchmark runner.
No production ranker, legacy API, or deployed endpoint was changed.

## Optional context module and passage-budget comparison

context.retrieve_with_context(query) preserves the original top-three cited
results and returns immediate paragraph neighbors separately. Expansion is
nonrecursive, pinned-source-local, deduplicated, and capped at six supplements.
Each supplementary record retains exact offsets and seed links. Context is
not adjudicated support. No HTTP context endpoint has been added.

Tests cover boundaries, repeated text, shared neighbors, seed deduplication,
document/revision isolation, input preservation, invalid spans, the cap, and
exact replay of all 24 saved adjacency cases.

The preserved local passage-budget comparison found:

| Method | Single supported | Complete multi-passage | Evidence groups | Characters |
|---|---:|---:|---:|---:|
| Top three | 12/16 | 1/4 | 4/8 | 21810 |
| Adjacent context | 12/16 | 3/4 | 6/8 | 37793 |
| Deeper ranked retrieval | 14/16 | 2/4 | 5/8 | 50051 |

Deeper retrieval received each query's adjacency passage allowance. L07 had
two fewer positive-scoring results than its allowance. Character budgets
were not matched. Counts aggregate passage occurrences across queries.

Adjacency uniquely recovered M03 in this comparison; deeper retrieval
recovered L06 and Q03. Neither resolved M04. The methods are complementary
on this development set, not independently validated universal improvements.

Comparison receipts are under benchmarks/evidence/2026-10-19/budget-comparison/.
Production ranking and existing HTTP response contracts remain unchanged.

## Whole-passage supplementary character-cap experiment

The local experiment replayed all 24 maintained context outputs.
It compared immediate-neighbor candidates with deeper-ranked candidates
under supplementary caps of 0, 500, 1000, and 2000 decoded characters.
Seeds remained unchanged and were excluded from the supplementary cap.

Passages were considered in existing order: accept a whole passage if
it fits; otherwise skip it and continue. No truncation was performed.
The maximum allowance matched, but actual consumption did not.
This is not an optimal-packing, equal-token-cost, or held-out evaluation.

| Cap | Method | Single support | Complete multi | Evidence groups | Extra characters |
|---:|---|---:|---:|---:|---:|
| 0 | adjacency | 12/16 | 1/4 | 4/8 | 0 |
| 0 | deeper | 12/16 | 1/4 | 4/8 | 0 |
| 500 | adjacency | 12/16 | 2/4 | 5/8 | 8899 |
| 500 | deeper | 13/16 | 1/4 | 4/8 | 11070 |
| 1000 | adjacency | 12/16 | 3/4 | 6/8 | 14733 |
| 1000 | deeper | 14/16 | 2/4 | 5/8 | 22559 |
| 2000 | adjacency | 12/16 | 3/4 | 6/8 | 15983 |
| 2000 | deeper | 15/16 | 2/4 | 5/8 | 44670 |

Adjacency recovered M03 at the 500-character cap; deeper ranking did
not complete M03 at any tested cap. Deeper ranking recovered Q03 at
500, L06 at 1000, and Q01 at 2000. Q05 and M04 remained unresolved.

Both methods added context to unsupported questions. Added text is not
adjudicated support, and no generated-answer evaluation was performed.
No production default was selected and no general superiority is claimed.

The maintained context module is unchanged: it has a six-supplement
passage cap, not a character cap. Character selection occurred only in
this experiment. No HTTP context endpoint or hybrid policy was added.

All cap results and selection decisions are preserved under
benchmarks/evidence/2026-10-19/character-budget/.
