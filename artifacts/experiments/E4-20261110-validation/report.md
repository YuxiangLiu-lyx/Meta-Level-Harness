# E4: Validation comparison

## Research Question
Does guidance-first Meta outperform direct-revision Refine on the same 20 validation scenarios under the fixed runtime?

## Hypothesis
The previously recorded directional exploratory hypothesis is Meta > Refine. It was not changed after validation.

## Setup and Controlled Variables
Protocol v1.1 for all validation conditions. One frozen harness per method; 20 shared scenarios; 80 logical policy generations. Requested gpt-6.1-sol, medium effort, fixed public instructions, no tools or verifier feedback, fresh sessions. Order rotates Manual/Direct/Meta/Refine by scenario. Maximum one same-input retry is allowed only for a missing-response infrastructure failure; completed answers are never repaired or retried. Original E3 construction had one Meta timeout and one disclosed recovery before validation; this deviation is retained and affects cost observability.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. 80/80 validation scenario-method pairs have saved outcomes. All results are included. Additional validation infrastructure attempts: 1. Final held-out evaluation: 0 scenarios.

## Results
| Method | Pass / planned | Syntax | Schema | Overgrant | Overdeny | Input tokens | Cached input | Output tokens | Reasoning output | Seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Direct | 10/20 | 20/20 | 18/20 | 7 | 6 | 200670 | 83072 | 9381 | 4826 | 317.8 |
| Manual | 12/20 | 20/20 | 20/20 | 8 | 4 | 194120 | 90624 | 8049 | 3510 | 259.6 |
| Meta | 9/20 | 20/20 | 16/20 | 6 | 6 | 200696 | 90624 | 10273 | 4701 | 308.8 |
| Refine | 11/20 | 20/20 | 19/20 | 7 | 7 | None | None | None | None | 1456.5 |

Refine: 1 additional infrastructure attempt(s). Total tokens are unknown if a failed attempt omitted usage. Known input subtotal: 202314; known output subtotal: 9701. Elapsed seconds include failed and successful attempts.

Meta-Refine pairing: both_pass=8, meta_only=1, refine_only=3, both_fail=8; resolved pairs=20/20; unresolved/protocol-violating pairs=0/20. Meta succeeds on 9/20; Refine on 11/20. Difference: -10 percentage points. Input tokens include cached input; do not add them. Blank/null totals indicate missing usage, not zero. Tables report scenario-level success; check counts are diagnostic only.

## Error Analysis
Examples are selected by first occurrence in frozen validation order for each pair category:
- meta_only: `grant_awards-chain2-T3-005`. Meta: PASS; all semantic checks pass; Refine: SEMANTIC_FAIL; obligate_funds_grants_officer_different_from_approver_floor, obligate_funds_only_grants_officer_after_approval_and_not_approver_ceiling.
- refine_only: `kubernetes_rbac-readSecret-T3-033`. Meta: SCHEMA_FAIL; semantic checks not run; Refine: PASS; all semantic checks pass.
- both_pass: `warehouse_fulfillment-pickOrder-T3-055`. Meta: PASS; all semantic checks pass; Refine: PASS; all semantic checks pass.
- both_fail: `network_change_approval-chain2-T4-026`. Meta: SCHEMA_FAIL; semantic checks not run; Refine: SCHEMA_FAIL; semantic checks not run.

All scenario-method outcomes and paired rows are in results.csv and paired_results.csv. Confirmed overgrant and overdeny counts can overlap. Runtime/tool violations and unresolved evaluations are reported separately from semantic failures.

## Interpretation
Meta trailed Refine by 10 percentage points in this single exploratory sample. This describes the observed harnesses and subset only. It cannot isolate a general causal advantage of meta-level guidance from single-design variability. A pass means satisfying the published nonempty checks, not equivalence to every plausible natural-language interpretation.

## Limitations
The configured subprocess timeout was 180 seconds, but the Refine validation timeout recorded 1165.7377 seconds of wall elapsed time. The cause is unknown; do not interpret this as model-compute time or claim the wall deadline was strictly enforced. The raw value is preserved in all cost totals. Analysis revision a2 corrects an earlier case-summary bug that described empty checks after schema failure as passing; original reports are archived under artifacts/analysis_revisions/a1. Scores and model outputs are unchanged.

Only 20 scenarios and one sampled design per automatic method. No statistical significance or general superiority is claimed. Equal stage counts do not imply equal compute. The Meta timeout has unknown token cost, and a post-freeze retry-rule amendment was necessary. Some requirements underspecify relationships required by the plans. Unexposed server model identity, internal requests, and sampling parameters remain unknown. No final test was opened.

## Next Action
Preserve this round. In a new preregistered round, fix recovery policy in advance, repeat designs across independent runs, audit ambiguous specification/check pairs, and expand validation without using the held-out test for development.

## Reproduction
The exact execution snapshot and hashes are in snapshot.zip and freeze.json. `PYTHONPATH=src python3 scripts/run_policies.py --experiment E4-20261110-validation --split validation20 --methods Manual Direct Meta Refine` reuses cached task identities. `PYTHONPATH=src python3 scripts/evidence_package.py` regenerates tables without model calls. Independent resampling requires new experiment identities and separate reporting.
