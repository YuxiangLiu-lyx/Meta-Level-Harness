# E3R: Recovered construction and fairness audit

## Research Question
Can Direct, Meta, and Refine produce one valid static harness each under the same frozen development evidence and stage budgets?

## Hypothesis
Guidance before harness construction may improve later validation relative to direct revision. Construction validity alone cannot test that performance hypothesis.

## Setup and Controlled Variables
Five logical design stages: Direct 1, Meta 2, Refine 2. Six actual design task attempts include the preserved Meta timeout. Protocol v1.1 adds one same-input recovery attempt for missing-response infrastructure failures, before any validation outcome is observed. All use identical frozen design packet, requested gpt-6.1-sol, medium effort, 180 seconds per stage, and 500-word editable artifact limit. Every stage is a fresh official Codex task. Second stages receive only the common materials and their permitted first-stage artifact. No candidate evaluation, validator feedback, or new evidence occurs between stages. Full stage inputs, raw output references, parsed artifacts, and snapshot are saved.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. 5/5 logical design stages now have valid artifacts. 3/3 final automatic harnesses constructed; one disclosed infrastructure retry, no output repair, search, or candidate selection. Initial E3 remains reported as 4/5 completed. Manual remains unchanged.

## Results
| Stage | Words | Input | Cached input | Output | Reasoning output | Seconds |
| --- | --- | --- | --- | --- | --- | --- |
| direct | 377 | 11114 | 0 | 702 | 184 | 27.6 |
| meta-guidance | 369 | 11102 | 0 | 519 | 51 | 24.4 |
| meta-harness | 371 | 11586 | 0 | 598 | 79 | 19.4 |
| refine-draft | 381 | 11114 | 0 | 815 | 286 | 28.5 |
| refine-revision | 437 | 11654 | 0 | 737 | 136 | 24.7 |

The fairness audit confirms identical packet and runtime settings, five distinct successful sessions, plus a separate failed Meta attempt, permitted artifact transfer, and zero tool events. All final harnesses contain only static instruction blocks, a legal input order, and a checklist. Input content is not rewritten or duplicated. Actual compute differs across equal-stage methods and is reported above.

## Error Analysis
No completed-output DESIGN_INVALID outcome occurred. The original Meta attempt timed out without a final response; its token usage is unknown. The one recovery used byte-identical prompt text, including the same guidance and packet. No new feedback was added. all_attempts.json retains all six attempts. The table above contains successful-stage usage only; Meta total input/output/reasoning usage is unknown, and reported successful-stage sums are known lower bounds. Elapsed attempt time includes the extra 180.022 seconds when comparing operational cost. Runtime warning events concern the fixed experimental skill-discovery feature and are preserved separately from tool events. Representative construction artifacts are the Meta guidance and the Refine draft/revision; each is stored in its task result. These artifacts are not shown to execution tasks except for the corresponding final harness.

## Interpretation
The construction manipulation is available with a disclosed infrastructure-recovery deviation. Any eventual difference is conditional on these single sampled harnesses and the shared packet. No performance comparison has yet been made at this stage.

## Limitations
One final harness per method. The post-freeze operational amendment weakens preregistration fidelity and adds an unobserved-usage Meta attempt; it must accompany any comparison. Word limits and common stage settings do not equalize input/output/reasoning tokens. Model sampling and unobserved server behavior prevent bit-for-bit regeneration guarantees. Raw reference-alignment ambiguity in the corpus remains.

## Next Action
Freeze all four final harnesses and execute exactly 80 validation policy generations, rotating method order by scenario. Keep the previously stated exploratory Meta > Refine hypothesis unchanged.

## Reproduction
Use the original E3 snapshot for the failed initial batch. `PYTHONPATH=src python3 scripts/recover_construction.py` reuses the single recovery attempt from cache. `PYTHONPATH=src python3 scripts/finalize_construction.py` checks fairness and creates the next freeze. Independent design repeats require new identities and a separate protocol run; do not overwrite these outputs.
