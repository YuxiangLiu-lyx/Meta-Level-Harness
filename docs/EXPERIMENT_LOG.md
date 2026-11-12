# Experiment log

| ID | Question | Status | Key results | Evidence directory | Next action |
| --- | --- | --- | --- | --- | --- |
| E0-20261110-preflight | Can the existing subscription support isolated tasks? | ANALYZED | 3/3 diagnostics; 0 tool events; grouped 20+20 data | artifacts/experiments/E0-20261110-preflight | E1 |
| E1-20261110-sanity | Does the verifier detect known faults? | ANALYZED | 5/5 references pass; 10/10 semantic mutants detected; 3/3 grammar/schema controls | artifacts/experiments/E1-20261110-sanity | E2 |
| E2-20261110-manual | What is Manual development performance? | ANALYZED | 20/20 outputs; 10/20 pass; 20/20 syntax/schema | artifacts/experiments/E2-20261110-manual | Freeze common packet |
| E3-20261110-construction | Can all design stages complete? | ANALYZED_PARTIAL | 5/5 attempted; 4 valid; Meta final stage timeout; no final response | artifacts/experiments/E3-20261110-construction | Disclosed infrastructure amendment |
| E3R-20261110-recovery | Does one same-input retry recover Meta? | ANALYZED | 1/1 recovered; 5 logical stages and 6 attempts total; 3 final harnesses | artifacts/experiments/E3R-20261110-recovery | Freeze E4 under v1.1 |
| E4-20261110-validation | Does Meta outperform Refine on paired validation? | ANALYZED | 80/80 final outputs; Manual 12, Direct 10, Meta 9, Refine 11 passes /20 | artifacts/experiments/E4-20261110-validation | Preserve paired evidence |
| E5-20261110-evidence | What conclusions do saved results support? | ANALYZED a2 | 110/120 attempts; 100 final policies; 20 resolved pairs; Meta-Refine -10 pp | artifacts/experiments/E5-20261110-evidence | New preregistered repeated-design round |

The v1.1 retry amendment was made before any validation output was observed. Original failed attempts and unknown usage are retained. No final test evaluation is performed. Reports distinguish completion, output errors, protocol violations, and unresolved infrastructure/evaluation outcomes.

## Final incidents and analysis corrections

- E3 Meta final-harness attempt: no final response; timeout; one same-input recovery under the disclosed v1.1 amendment. Initial failed E3 report remains separate.
- E4 Refine validation position 18: no final response; one same-input recovery under the same rule. Observed wall elapsed 1165.7377 seconds exceeded the configured 180 seconds; cause unknown. Record real elapsed time and unknown token cost.
- Analysis a1 incorrectly described an empty list of semantic checks after schema failure as passing in case-summary prose. a2 corrects the wording; policy outputs, scores, and paired counts never changed. a1 files are preserved under artifacts/analysis_revisions/a1. The correction required zero additional model calls.
- Final evidence audit: all 110 session IDs distinct; 0 observed tool events; 0 unresolved final evaluations; 375 held-out scenarios not opened or evaluated. Eleven focused tests pass. Frozen snapshots preserve their original file hashes.

## User confirmation received after E0-E5 delivery

The user's asynchronous reply explicitly permits a uniform maximum of one retry for infrastructure failures with no final response, while retaining the original failure and clearly disclosing the protocol amendment. This matches the v1.1 rule already applied to the two missing-response timeouts. Completed answers remain ineligible for retry.

The reply arrived after delivery of the completed E0-E5 results. At amendment time, the optional preference question was unanswered; the amendment was an investigator decision under the original task's bounded-network-retry authorization. This later confirmation does not retroactively make the amendment preregistered or imply that explicit confirmation preceded execution. The original E3 report remains unchanged as a historical record. Recording this reply adds no model calls and changes no runtime configuration, frozen evidence, outputs, scores, or results; total attempts remain 110/120.

## P1-20261111-midreport: post-hoc offline analysis

IMPLEMENTED, TESTED, EXECUTED, ANALYZED. Output: artifacts/posthoc/P1-20261111-midreport. No new experiment was run; calls remain 110/120. All E0-E5 outputs, scores, freezes, and a1/a2 artifacts are retained. Main results 12/20, 10/20, 9/20, 11/20 and pairing 8/1/3/8 are unchanged. All four discordant cases were re-read from raw output/validator/solver evidence. Three Refine-only cases are Meta schema/type failures; the Meta-only case is a Refine semantic failure with floor and ceiling counterexamples.

Post-hoc paired percentile bootstrap: 20 scenario pairs, 100000 replicates, seed 20261111, -10 pp estimate, 95% interval [-30,+10] pp, conditional on these harnesses/outputs. No equivalence claim or type-failure exclusion.

Portable export uses an explicit allowlist, relative index, unchanged raw bytes, and original checksums where available. Relocation tests deny host-user paths, network, and child processes; metrics remain identical after raw evidence is removed from a temporary copy. Nineteen tests pass. Bibliographic metadata was verified separately using primary web sources; analysis itself uses saved local data only.

Expanded audit discovered 61 unavailable original check-log hashes across nine outputs in seven shared verifier directories. The original verifier's log path omitted task identity, allowing later identical-policy evaluations to overwrite earlier logs. All currently available decisions match saved scores; the full historical audit is nevertheless INCOMPLETE. The old auditor checked model logs only and did not detect this. No old report or score was changed. Validator-gate hashes are first captured at export, not retroactively called execution-time hashes. All four discordant cases retain their recorded check-log bytes.

Manual provenance is corrected in current writing material to a fixed baseline prepared in an AI-assisted setup; independent human-only authorship is not established. P1 includes limitations, method/data/performance/pair tables, four case audits, two body-case notes, an evidence index, an anonymous ACL-style outline, and verified BibTeX. Next action: write the mid report with these disclosures; no new model experiments are authorized by this analysis task.
