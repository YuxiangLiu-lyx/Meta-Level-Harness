# Meta-Level Harness Design for Natural-Language Rule Translation

This repository implements a small exploratory comparison of editable static task harness construction under a fixed Codex runtime. Natural-language access requirements plus a Cedar schema are translated into one Cedar policy per scenario. The primary comparison is Meta (guidance then harness) versus Refine (harness then direct revision); Manual and Direct are controls. This is a Codex-runtime experiment, not a bare-model experiment.

## Current status

E0-E5 are IMPLEMENTED, TESTED, EXECUTED, and ANALYZED, including the failed initial E3 attempt, disclosed v1.1 recovery, and corrected analysis a2. Completed 100/100 final policy outputs, five logical design stages, and three smoke diagnostics. Actual task attempts: 110/120, including two preserved missing-response timeouts and their single retries. No observed tool execution; no unresolved final evaluation; all 375 held-out scenarios remain unopened and unevaluated.

| Method | Validation success | Rate |
| --- | --- | --- |
| Manual | 12/20 | 60% |
| Direct | 10/20 | 50% |
| Meta | 9/20 | 45% |
| Refine | 11/20 | 55% |

Meta-Refine: both pass 8, Meta only 1, Refine only 3, both fail 8; difference -10 percentage points. This sample does not support Meta superiority and cannot establish a general ranking. E2 Manual development performance was 10/20 and is reported separately.

Start with [E5 evidence report](artifacts/experiments/E5-20261110-evidence/report.md), [E4 full comparison](artifacts/experiments/E4-20261110-validation/report.md), and [paired case analysis](artifacts/experiments/E5-20261110-evidence/case_analysis.md). Detailed tables include performance, design usage, paired outcomes, all task attempts, and verifier controls. Read docs/STATE.md and docs/EXPERIMENT_LOG.md before resuming.

Important limitations: Meta construction and Refine validation each had one timeout with unknown token usage. A retry-policy amendment was disclosed before validation. The Refine timeout recorded 1165.7 wall seconds despite a configured 180-second subprocess timeout; its cause is unknown. Use known token subtotals and do not interpret wall latency as compute. Analysis a1 contained an empty-check-list display bug; a2 corrects the report without changing predictions or scores, preserving a1 under artifacts/analysis_revisions/a1.

## Minimal architecture

- src/harness_lab/backend.py: subprocess-only official Codex CLI, isolated fresh tasks, identity-aware cache, bounded infrastructure recovery, external raw evidence.
- src/harness_lab/protocol.py: static JSON harness validation, exact input allowlist, deterministic parsing, freeze checks, pairing.
- src/harness_lab/verifier.py: actual Cedar validate and SymCC/CVC5 checks using original RAISE plans; unknown/timeouts remain unresolved.
- scripts/: small preparation, execution, analysis, and evidence-audit entry points.
- data/: answer-free selected inputs and hashes/IDs; references stay in the external evidence directory.
- artifacts/experiments/: immutable attempts, configs, snapshots, scores, tables, and reports.

## Audited environment

Python 3.13.7 on Apple Silicon macOS. The PATH npm Codex launcher is broken; configs/runtime.json points to the working executable bundled with the official VS Code extension (0.162.0-alpha.17.2). Existing ChatGPT login is verified using codex login status. Requested model is gpt-6.1-sol, medium effort. Effective serving model, temperature, random seed, hard output-token cap, and internal request count are not exposed and are not invented. No API key, API-credit purchase, local language model, or training dependencies are used.

Cedar CLI 4.14.1 experimental build and CVC5 1.4.2 are official pinned ARM downloads with recorded hashes. scripts/install_verifier.py installs only these evaluation binaries outside this repository. The Python implementation uses the standard library.

## Data provenance and held-out boundary

Upstream: https://github.com/Aizhouym/raise at commit 206962d130d2c69d5e15f8103fa0953345cc7690. Published split metadata contains 375 held-out, 1,039 RL, and 4,386 SFT scenarios. Held-out content is not extracted, read, or evaluated. Preparation unions non-held-out family and structural-signature groups, shuffles 139 groups with seed 20261110, and samples one scenario from each of 40 groups. First 20 are design20; next 20 are validation20. These are new experimental subsets of published assignments, not a claim to reproduce a paper's exact evaluation set. data/manifest.json records complete IDs and hashes.

## Reproduce analysis without model calls

Run from the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/audit_evidence.py
PYTHONPATH=src python3 scripts/analyze.py E2-20261110-manual
PYTHONPATH=src python3 scripts/evidence_package.py
```

The last command uses the completed E4 evidence. It reads saved generations and scores, never invokes Codex. Original JSONL events and Cedar solver outputs are outside the repository, currently at /Users/liuyuxiang/Documents/USA/599/harness_experiment_raw, with paths and SHA-256 values in repository artifacts. Preserve that directory when moving the project; do not translate or rewrite raw evidence. Missing raw evidence is reported by the audit.

## Reproduce execution

Every formal experiment contains freeze.json and snapshot.zip. Use that experiment's snapshot in a separate checkout to reproduce its original code/config, especially v1 E2/E3 versus v1.1 E3R/E4. Current files intentionally fail old freeze checks; do not erase old freezes or silently pool old and new protocol outputs.

On a fresh installation, clone the exact upstream revision into the configured external directory, set the official CLI path and raw_root in a new runtime config, run python3 scripts/install_verifier.py, and run PYTHONPATH=src python3 scripts/prepare_data.py. Preparation refuses to overwrite existing splits. Verify ChatGPT subscription login with the official CLI. Credentials are never read or copied by this project. The supplied installer is specific to the audited Apple Silicon environment.

The frozen E4 invocation is:

```bash
PYTHONPATH=src python3 scripts/run_policies.py --experiment E4-20261110-validation --split validation20 --methods Manual Direct Meta Refine
```

With existing evidence and matching freeze, this reuses cached task identities. An independent stochastic repeat requires a new experiment ID, new freeze/snapshot, and a separate ledger/budget; do not reuse an old identity as a new sample. Generation is not guaranteed bit-for-bit reproducible. Model tasks run serially with at most 120 actual attempts in this round. v1.1 permits one additional fresh attempt only for a recognized transport failure or timeout with no final response, not for authentication/quota failures or wrong answers. Per-attempt wall limit is 180 seconds. No final-test command is provided.

## Evidence and interpretation

The experiment reports distinguish IMPLEMENTED, TESTED, EXECUTED, and ANALYZED. All failures, deviations, and unknown usage are retained. A scenario pass requires parse, schema validity, and every nonempty semantic check. Published plans can impose relationships omitted from the natural-language text, so plan compliance is not a complete measure of semantic fidelity. Twenty pairs and one design repeat cannot establish statistical significance or general superiority. Meta's timed-out design attempt adds unknown token cost, which is not recorded as zero.
