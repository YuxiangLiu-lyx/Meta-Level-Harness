# Research engineering rules

- Read this file and `docs/STATE.md` before resuming work.
- Communicate with the user in Chinese. Author repository files, code, comments, prompts, logs, reports, and commit messages in English.
- Preserve raw evidence unchanged. Store non-English third-party evidence outside this repository and record its path and SHA-256.
- Work in small steps: implement, test relevant invariants, execute, analyze, update state.
- Use the existing Codex subscription through an official local interface. Never extract credentials, switch billing paths, or train a model.
- Keep development context separate from fresh experimental sessions. No tools, references, verifier feedback, history reuse, repair, or best-of-N in policy generation.
- Keep held-out data closed. Split by template/near-duplicate groups before observing model performance.
- Freeze prompts, model settings, data, and implementation before each formal batch. Version changes; never pool incompatible protocols.
- Preserve every attempt and protocol violation. Never invent results, overwrite old experiments, select only favorable runs, or retry semantic failures.
- Every experiment, including failed experiments, needs real counts, analysis, limitations, reproduction instructions, and a next action.
- Distinguish IMPLEMENTED, TESTED, EXECUTED, and ANALYZED. Update README, protocol, experiment log, and state as work progresses.
- Execute serially. Maximum 120 logical model tasks for the first round. Stop model calls on authentication or usage-limit failure; complete independent work.
