# Claim-to-evidence index

POST-HOC, 2026-11-11. Paths are relative. The package [manifest](../review_bundle/manifest.json) indexes exact file hashes; [index.json](../review_bundle/index.json) maps each task to its source and raw evidence. Original absolute paths inside copied payloads are never used for offline reads.

| Claim or diagnostic | Direct evidence | Scope or limitation |
| --- | --- | --- |
| Validation successes 12/20, 10/20, 9/20, 11/20 | [Recomputed metrics](../analysis/results.json), [80 source score mappings](../review_bundle/index.json), [performance table](performance_error_types.csv) | Saved scores, unchanged |
| Syntax failures 0/0/0/0; type failures 0/2/4/1; semantic failures 8/8/7/8 | [Error table](performance_error_types.csv); original score.json and validate.json via index | Type failures are included in primary denominators |
| Both pass 8, Meta only 1, Refine only 3, both fail 8 | [All 20 paired rows](../analysis/pairs.csv), [pair counts](paired_counts.csv) | Pairing by scenario ID |
| Difference -10 pp, bootstrap 95% interval [-30,+10] pp | [Method/settings/results](../analysis/bootstrap.json), [replicate histogram](../analysis/bootstrap_histogram.csv), [standalone implementation](../review_bundle/review.py) | Post-hoc, seed 20261111, 100000 resamples, fixed harnesses/outputs |
| All three Refine-only cases are Meta type failures | [Kubernetes](cases/kubernetes_rbac-readSecret-T3-033.md), [IoT](cases/iot_fleet-sendCommand-T3-029.md), [immigration](cases/immigration_casework-clearSecurityCheck-T3-024.md) | Original policy strings, return code 3, decimal/datetime errors; Meta semantic checks not run |
| Meta-only case has a Refine semantic failure | [Grant awards](cases/grant_awards-chain2-T3-005.md) | Original floor and ceiling counterexamples, both type gates passed |
| No type-valid subset substitutes for the primary comparison | [Tables](tables.md), [analysis implementation](../review_bundle/review.py) | All 20 scenarios used for each method and bootstrap |
| 110 attempts, 108 completed, two missing-response timeouts | [Attempt table](../analysis/attempts.csv), [saved ledger](../review_bundle/source/artifacts/task_ledger.jsonl), model events through index | Underlying service requests and failed-attempt token usage unknown |
| 180-second configuration versus anomalous wall elapsed | [Infrastructure table](infrastructure_failures.csv), original result.json through index | Cause unknown; no compute-time interpretation |
| 20 development + 20 validation, disjoint groups; held-out unopened | [Original data manifest](../review_bundle/source/data/manifest.json), [split table](data_splits.csv) | Held-out IDs/metadata only; no held-out content exported |
| Fixed baseline cannot be called independently human-authored | [Manual provenance](manual_provenance.md), original configs/manual.json in package and E2/E4 snapshot.zip in repository | No human-only authorship record; AI-assisted setup |
| Requirement/plan mismatch is a real limitation | [Patent intent](../review_bundle/materials/patent_prosecution-examineApplication-T2-005/intent.md), [plan](../review_bundle/materials/patent_prosecution-examineApplication-T2-005/verification_plan.py), [ceiling](../review_bundle/materials/patent_prosecution-examineApplication-T2-005/references/examine_limited_to_assigned_examiner_mfa_noninventor.cedar) | Assignment appears as resource metadata but is imposed as an authorization condition by the plan |
| a1-to-a2 fixed prose only | [Original correction record](../review_bundle/source/artifacts/experiments/E5-20261110-evidence/analysis_corrections.json) and preserved repository a1/a2 | Predictions/scores unchanged |
| Expanded historical audit is INCOMPLETE | [Audit JSON](../analysis/evidence_audit.json), [61 hash gaps](historical_solver_hash_gaps.csv), [nine affected outputs](historical_gap_by_task.csv) | All available decisions agree; older byte-identical solver logs unavailable |
| Shared solver-log paths explain the overwrite mechanism | [Original verifier code](../review_bundle/source/src/harness_lab/verifier.py), raw paths/cache keys and hashes in original score records | Log naming omits task/attempt identity; does not justify reconstructing lost bytes |
| Portable recomputation works without host paths/network | [Relocation validation](../portable_validation.json), repository scripts/validate_review_bundle.py | Layer 1 complete; layer 2 faithfully reports historical gaps |
| References have verified metadata | [Reference notes](references.md), [BibTeX](references.bib) | Primary sources checked 2026-11-11; venue status distinguished from preprint |

No new model call, solver run, policy edit, sample selection, or held-out read was used for these conclusions.
