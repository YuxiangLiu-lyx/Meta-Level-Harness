# E5: Evidence package

## Research Question
What conclusions are supported by this completed exploratory research loop, including failures and procedural deviations?

## Hypothesis
Meta may outperform Refine under a fixed runtime. This remains a limited exploratory hypothesis rather than a general claim.

## Setup and Controlled Variables
Upstream RAISE commit 206962d130d2c69d5e15f8103fa0953345cc7690. Published 375-scenario held-out preserved. Fixed grouped design20/validation20, seed 20261110; no shared families/signatures between subsets. Tables: dataset.csv, environment.csv, verifier_sanity.csv, construction_usage.csv, performance.csv, meta_refine_pairs.csv, task_accounting.csv. All authored reports and prompts are English; original raw evidence stays external with paths/hashes. Runtime is Codex, not a bare model.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. E0: 3/3 diagnostics. E1: 18/18 controls. E2: 20/20 generations, 10/20 passes. E3 initial: 4/5 completed; E3R: 1/1 recovery. E4: 80/80 logical generations. Task attempts: 110/120; completed attempts: 108; distinct sessions: 110. Incomplete infrastructure attempts: 2. Tool events: 0. Final test: 0 evaluations.

## Results
| Method | Pass / planned | Syntax | Schema | Overgrant | Overdeny | Input tokens | Cached input | Output tokens | Reasoning output | Seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Direct | 10/20 | 20/20 | 18/20 | 7 | 6 | 200670 | 83072 | 9381 | 4826 | 317.8 |
| Manual | 12/20 | 20/20 | 20/20 | 8 | 4 | 194120 | 90624 | 8049 | 3510 | 259.6 |
| Meta | 9/20 | 20/20 | 16/20 | 6 | 6 | 200696 | 90624 | 10273 | 4701 | 308.8 |
| Refine | 11/20 | 20/20 | 19/20 | 7 | 7 | None | None | None | None | 1456.5 |

Refine: 1 additional infrastructure attempt(s). Total tokens are unknown if a failed attempt omitted usage. Known input subtotal: 202314; known output subtotal: 9701. Elapsed seconds include failed and successful attempts.

Primary paired result: Meta 9/20 versus Refine 11/20, -10 percentage points; both_pass=8, meta_only=1, refine_only=3, both_fail=8. These 20 pairs are the unit of analysis.

## Error Analysis
Manual development failures included both broadened grants and added prerequisites; 7/20 confirmed overgrant and 6/20 overdeny, with overlap. Sanity controls detected 10/10 known semantic mutants and 3/3 syntax/schema errors; 5/5 references passed. The original Meta design timeout has no final answer or usage event and remains an infrastructure failure. Its cost is not zero: Meta total design tokens and whole-run totals are unknown; known subtotals are provided. Positive and negative paired cases are indexed in cases.json using a deterministic selection rule.

## Interpretation
Meta trailed Refine by 10 percentage points in this single exploratory sample. The pipeline can conduct and audit this comparison using an existing Codex subscription and actual Cedar/CVC5 checks. The outcome supports a descriptive observation about these frozen artifacts, not statistical significance, general superiority, a bare-model result, or a final-test claim.

## Limitations
The Refine validation timeout recorded 1165.7377 wall seconds despite a configured 180-second timeout. Its cause is unknown, and wall latency is not compute. The initial analysis report incorrectly called empty check lists after schema failure passing; a2 corrects the wording without changing scores, while preserving a1 under artifacts/analysis_revisions/a1.

Small sample, one design repeat, benchmark specification ambiguity, unequal actual design compute, hidden runtime context, and a disclosed post-freeze infrastructure amendment. Code/cache/split reproducibility is supported; stochastic model output is not guaranteed bit-for-bit reproducible. The original v1 zero-retry construction batch and v1.1 validation batch remain separately labeled; no failed evidence is discarded.

## Next Action
Preregister a complete timeout/retry plan before the next round. Repeat the Meta/Refine design construction with paired independent design seeds or repeats if supported; increase validation sample size across template groups; manually adjudicate requirement/plan mismatches without changing this round's scores. Keep the final held-out closed until hypotheses and methods are stable. No training or large prompt search is needed for this next diagnostic step.

## Reproduction
Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`, `PYTHONPATH=src python3 scripts/audit_evidence.py`, and `PYTHONPATH=src python3 scripts/evidence_package.py`. These commands do not invoke a model. See README.md for installation, pinned external evidence, frozen snapshots, and new-run identity requirements. Every initial failed attempt, successful response, evaluation, and report is retained.
