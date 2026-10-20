
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
