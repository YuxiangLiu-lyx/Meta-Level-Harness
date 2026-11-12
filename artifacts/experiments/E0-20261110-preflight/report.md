# E0: Environment, backend, and data readiness

## Research Question
Can the existing subscription support fresh, isolated Codex CLI tasks with auditable evidence?

## Hypothesis
Official local CLI invocation can provide structured answers without experimental tool use.

## Setup and Controlled Variables
Codex CLI 0.162.0-alpha.17.2 from the official VS Code extension; ChatGPT subscription login; requested gpt-6.1-sol, medium effort. Every task uses a new temporary directory and session, no daemon, ephemeral mode, ignored user config/rules, zero project-document bytes, disabled skills discovery/instruction catalog, memory, plugins, MCP, search, shell, browser, and agent tools. Built-in runtime instructions remain. Credentials are neither read nor copied. Details are in config.json and environment.json.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. Completed 3/3 diagnostics. These tasks are outside performance denominators. Logical task ledger contains 3 tasks. Seven core invariant tests pass.

## Results
3/3 final responses received; 2/2 structured outputs parsed. 0 observed tool events. The file-access challenge returned UNAVAILABLE and did not expose the secret or project-instruction canary. The debug prompt audit had no research documents or skill catalog. Published upstream assignments contain 375 held-out, 1,039 RL, and 4,386 SFT scenarios. Selected 20 design and 20 validation scenarios from 139 family/signature groups with seed 20261110. No cross-subset family/signature overlap. Held-out content was not extracted or evaluated.

## Error Analysis
The PATH npm launcher fails because its ARM executable is missing. The official extension binary works. Initial event classification counted a CLI unstable-feature warning as a tool event; corrected analysis is saved separately in smoke-01/analysis.json, preserving the original result and raw events. No generation was repeated. skip_host_skill_discovery is an experimental runtime feature.

## Interpretation
The local official CLI and subscription work. Configuration inspection and actual diagnostics support proceeding with monitored tool-free tasks. This does not establish control over hidden server-side system context.

## Limitations
Effective server model and exact underlying request counts are not exposed in exec JSONL and remain null. Temperature, seed, and hard generation-token limits are not set. Usage is subscription-limited, not unlimited/free. Fresh sessions can still benefit from server prompt caching. The diagnostic with two agent messages used one visible turn; underlying request count remains unknown. The model catalog is supporting metadata, not proof of effective serving model. Published held-out assignments are preserved; our 20/20 subsets are newly sampled, not a paper split reconstruction.

## Next Action
Run E1 semantic controls and then the frozen Manual baseline.

## Reproduction
Run `python3 scripts/install_verifier.py`, then `PYTHONPATH=src python3 scripts/prepare_data.py` in a fresh checkout after cloning the pinned upstream commit externally. Run `PYTHONPATH=src python3 scripts/smoke.py` using the saved preflight config and a new diagnostic identity for an independent repeat. Never overwrite existing attempts. See data/manifest.json for exact IDs and hashes. Original CLI evidence is external under the paths in task results.
