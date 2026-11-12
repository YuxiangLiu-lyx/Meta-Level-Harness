# Research protocol

Protocol: `v1` (generation/evaluation implementation frozen for E2). User-facing date: 2026-11-10, America/New_York.

## Question and hypothesis

Does generating harness-design guidance before a harness improve scenario-level Cedar correctness relative to directly revising a harness under the same fixed Codex runtime? The directional exploratory hypothesis is Meta > Refine. One harness per automatic method and 20 validation scenarios cannot establish general superiority or statistical significance.

## Methods

- Manual: fixed baseline instructions/checklist prepared in the AI-assisted research setup; zero experimental model design stages. Independent human-only authorship is not established (P1 provenance clarification).
- Direct: one stage produces one harness.
- Meta: one stage produces guidance, then a fresh session produces a harness from that guidance.
- Refine: one stage produces a harness, then a fresh session revises it.

There are five logical automatic design stages. All receive the identical frozen packet containing selected development inputs and Manual development error summaries, without reference policies or verification plans. No evaluation or new feedback occurs between stages.

## Data and isolation

Inspect Aizhouym/raise and record its commit and release structure. Preserve upstream held-out data without evaluation. Select design20 and validation20 from non-held-out data by deterministic template/near-duplicate grouping; record IDs, seed, hashes, and reconstruction limitations. Reference policies and verification plans are accessible only to preparation and evaluation code.

Each generation input contains only complete requirements, complete schema, final harness, and fixed public instructions. Each input occurs once. Fresh independent working directories and sessions must exclude research instructions, memory, skills, MCP, search, answers, and feedback. Read-only mode alone is insufficient. Check actual event logs; retain violations and exclude contaminated results from any claimed tool-free main comparison. Unremovable runtime instructions are a fixed background.

## Runtime and budget

Use one officially supported subprocess backend with existing subscription authentication. Requested/effective model, runtime version, effort, exposed parameters, tools, date, and usage must be recorded. Unexposed temperature, seed, token limits, reasoning tokens, or internal request counts are null, not zero. Execute serially. Plan: 20 Manual development generations + 80 validation generations + 5 design tasks; total at most 120 logical model tasks including smoke tests and diagnostics. No retries for incorrect answers. Initially zero wrapper network retries; runtime retries must be logged. Stop on authentication or subscription limits.

Harness JSON allows static instruction blocks, an input order containing requirements/schema exactly once, and an optional checklist. Editable instruction text and Meta guidance are each at most 500 whitespace-delimited words. No executable code, retrieval, extra calls, or repair loops. Meta and Refine have equal per-stage settings and configurable wall-clock budgets; actual usage is reported separately. Parse JSON exactly or unwrap one entire JSON code fence deterministically; no model repair.

## Evaluation

Primary success requires syntax, schema validity, and all nonempty semantic checks. Report syntax/schema rates, confirmed overgrant/overdeny, usage, latency, truncation, violations, and infrastructure failures separately. Verifier crashes, timeouts, and unknown outcomes are unresolved evaluation states, not semantic failures. Reevaluate saved policies after verifier repairs without generation. Check-level rates are diagnostic only.

Report Meta-Refine both_pass, meta_only, refine_only, both_fail, success counts/denominators, and percentage-point difference. Preserve unsuccessful and unresolved cases. Do not inspect final test data or claim broad/general/significant gains.

## Freezes and evidence

Cache keys include task identity, repeat identity, complete input, harness, runtime settings, and protocol. Scoring keys also include verifier and evaluation-material versions. Freeze code and inputs before formal execution; do not edit code used by a running batch. New result-affecting versions invalidate incompatible prior evidence. Experiments use unique directories and deliver English reports with Research Question, Hypothesis, Setup and Controlled Variables, Execution Status, Results, Error Analysis, Interpretation, Limitations, Next Action, and Reproduction.

## Verified implementation details (before validation)

The runtime is the official extension CLI 0.162.0-alpha.17.2. Requested model gpt-6.1-sol and medium reasoning are fixed for construction and policy execution. Per-task wall-clock budget is 180 seconds, with zero wrapper retries. No supported hard output-token cap, temperature, or seed is claimed. CLI features explicitly disable shell/unified execution, apps/plugins, hooks, memories, multi-agent capabilities, browser/computer/image tools, skill search, goals, sleep, and unbounded connection retries; search is disabled and MCP config is empty. Host skill discovery is skipped using an experimentally supported flag. Credentials remain in the user's existing official login store. Each model task runs in a fresh temporary directory with --no-daemon, --ignore-user-config, --ignore-rules, --ephemeral, and project_doc_max_bytes=0. Full prompt/debug and event evidence is retained externally. Residual fixed runtime developer/system instructions are not described as a bare-model prompt.

Use the upstream commit 206962d130d2c69d5e15f8103fa0953345cc7690 and its published split assignments. Do not read the heldout.jsonl content. A preparation-only pass reads split metadata, unions non-held-out scenarios sharing a family or normalized schema+gold signature, shuffles the 139 components using seed 20261110, and chooses one scenario per first 40 groups. First 20 form design20 and next 20 validation20. Only those scenario directories are extracted. This is an experimental grouped subset of a published split, not the paper's original evaluation subset.

Cedar 4.14.1 experimental and CVC5 1.4.2 are pinned with archive/binary hashes. The strict evaluation adapter reuses original plans without changing their semantics; only explicit proofs/counterexamples resolve a query. Empty/unknown checks and solver failures are unresolved. Compliance with published plans may differ from a reasonable reading of underspecified requirements. This limitation was identified in E1, before model validation results.

The E2 pilot uses the first five frozen design scenarios. Its outputs are reused with the same task identities for the 20-scenario baseline. Automatic methods use an identical packet with three fixed representative inputs (the first three design scenarios), the Manual harness, aggregate Manual errors, and at most three concise manually reviewed explanations. The packet contains no reference policies, raw counterexamples, or verification plans. Direct and Refine draft stages use identical construction instructions but independent fresh sessions. All five design stages use the same model, effort, and wall-clock limit. No intermediate candidate is evaluated. E4 rotates the method order by scenario while remaining fully serial.

## v1.1 infrastructure amendment, after E3 and before any validation

The v1 Meta final-harness attempt timed out after 180 seconds with no final response. Initial E3 is reported separately as 4/5 completed, not relabeled successful. The original user request permits uniform bounded network retries; the investigator initially chose zero. v1.1 changes only recovery handling: at most one additional fresh-session attempt for a timeout or recognized transport failure with no final response. No retry for authentication, quota, completed invalid output, syntax/schema/semantic failure, or protocol violation. Each attempt retains its own ID and consumes the 120-task ledger budget. Each attempt keeps the same 180-second wall limit, model, effort, tools, and complete input. Missing usage remains unknown. No claim of equal actual compute is made.

This is a disclosed post-freeze procedural amendment, not preregistered behavior. No validation outcomes were observed before it. Valid v1 development/construction artifacts remain usable as frozen inputs because their contents and generation settings are unchanged; their original protocol provenance is retained. E2 v1 development performance and E4 v1.1 validation performance are separate tables, not pooled. All 80 E4 generation tasks use v1.1, and no completed policy is regenerated. Existing v1 freezes remain archived and must be checked against their own snapshots, not modified working files. The v1.1 retry rule cannot retroactively make the original E3 attempt complete.

## Observed timing limitation and analysis revision

During E4, the first Refine attempt for validation position 18 timed out without a response. The subprocess timeout setting was 180 seconds, but time.time-based elapsed recording was 1165.7377 seconds. The cause is not established by the logs; host suspension, scheduling delay, and clock behavior are possibilities, not findings. Do not claim a strict observed wall-clock cap or interpret wall latency as inference compute. Preserve the actual number and null token usage. Its only retry used exactly the same input and completed successfully.

Analysis a2 fixes a prose-only vacuous-pass bug: a schema failure with zero semantic checks must say that semantic checks were not run. All original a1 reports and the generating script are archived; model outputs, actual score statuses, denominators, and paired results are unchanged. No extra model calls or policy resampling occurred for this correction.

## P1 post-hoc analysis and evidence export (2026-11-11)

P1 uses the completed 80 E4 results and preserves all main scores, policies, frozen snapshots, and a1/a2. All four Meta-Refine disagreements are audited from raw responses and verifier logs. A 95% paired percentile bootstrap resamples 20 scenario pairs, with 100000 repetitions, Python random.Random/randrange, seed 20261111, and linear-interpolated quantiles. This is post-hoc and conditional on the saved harnesses/outputs; it omits construction randomness and does not establish equivalence. All type failures remain in the primary denominator.

The portable review interface distinguishes saved-result recomputation from raw-evidence audit. Only allowlisted original events, final responses, relevant diagnostics, verifier outputs/materials, and source records are exported. Relative paths drive all reads; absolute strings inside preserved payloads are inert provenance. No raw text is translated or rewritten. Missing evidence returns INCOMPLETE/UNKNOWN, not a successful zero-tool audit. The expanded audit reveals 61 historical solver-log hash mismatches from reused verifier directories; available later logs are not substitutes for earlier byte-identical records. This is disclosed as a provenance gap without modifying the old experiments. Future verifier fixes must use a new version and separate runs; no rerun is performed in P1.
