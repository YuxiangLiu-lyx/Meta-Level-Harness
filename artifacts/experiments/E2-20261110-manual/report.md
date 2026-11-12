# E2: Manual development baseline

## Research Question
How well does the fixed manually authored task harness perform on the frozen design20 subset, and what errors can inform all automatic methods equally?

## Hypothesis
The baseline will produce valid Cedar syntax but fail some authorization boundaries and exception compositions. No particular success rate is preregistered.

## Setup and Controlled Variables
Protocol v1, frozen snapshot.zip and freeze.json. Manual static harness, gpt-6.1-sol requested, medium reasoning, 180-second wall timeout, no wrapper retries, no tool assistance. Same public Cedar instructions and strict evaluator as planned for validation. The first five tasks were reused from cache when extending to 20; no duplicate policy generation.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. Pilot 5/5, total 20/20 unique policy generations. Pilot passed 2/5. Full baseline passed 10/20. No retry or candidate repair.

## Results
| Method | Pass / planned | Syntax | Schema | Overgrant | Overdeny | Input tokens | Cached input | Output tokens | Reasoning output | Seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Manual | 10/20 | 20/20 | 20/20 | 7 | 6 | 193921 | 0 | 7408 | 3462 | 248.1 |

All 20/20 outputs passed syntax and schema validation. Ten scenarios failed semantic checks. Confirmed overgrant occurred in 7/20 and overdeny in 6/20; categories overlap. Tool events: 0. Unresolved evaluations: 0. Infrastructure failures: 0. Usage counts include any runtime-visible internal processing; underlying request count remains unknown. Input tokens already include cached input tokens.

## Error Analysis
- Document management: all eight checks passed; the generated rule retained draft, share-list, and version-lock conditions.
- Wire workflow: an extra verifier/treasury role condition blocked approvals that the requirement grants to any sufficiently authorized person. The person-authority floor failed.
- IAM modification: a broad organization exception permitted non-owner cases excluded by the published permission union.
- Patent examination: the policy omitted assigned-examiner equality, causing a ceiling failure. The source requirement does not explicitly state assignment; this is partly a benchmark specification-alignment issue.

All ten failed scenarios and check names are retained in error_analysis.json; no favorable filtering is applied.

## Interpretation
Manual achieves 50% development compliance with the published nonempty verification plans. Syntax is not the limiting factor in this subset. The errors justify studying how construction instructions address permission scope, unnecessary restrictions, and local exceptions.

## Limitations
Development performance is not validation performance. Requirements can underspecify verifier expectations; the baseline's failures do not all prove incorrect translation of the literal text. Only one generation per scenario was sampled. The underlying Codex runtime remains part of the condition.

## Next Action
Freeze the shared design packet with three preselected development inputs, the unchanged Manual harness, aggregate error counts, and three sanitized explanations. Construct Direct, Meta, and Refine without intermediate evaluation. Do not revise Manual.

## Reproduction
`PYTHONPATH=src python3 scripts/run_policies.py --experiment E2-20261110-manual --split design20 --limit 5`, then the same command with `--limit 20`. The cache verifies task/input/model/harness/protocol identity. `PYTHONPATH=src python3 scripts/analyze.py E2-20261110-manual` regenerates deterministic tables without model calls. Independent repeats require new experiment/task identities and separate evidence.
