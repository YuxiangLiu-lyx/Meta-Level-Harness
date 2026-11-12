# Portable review package (post-hoc, 2026-11-11)

This package preserves original evidence bytes and historical failures. It contains
all 110 model-attempt event records, final responses when present, diagnostic
stderr/schema files, and the 80 E4 verifier runs with their referenced materials.
It excludes credentials, login stores, unrelated personal files, host prompt/debug
captures, model binaries, corpus archives, and all final held-out content.

Run with Python 3.10 or later, from any working directory:

```bash
python3 /path/to/package/review.py analyze /path/to/package --output /new/metrics
python3 /path/to/package/review.py audit /path/to/package --output /new/audit
```

`analyze` recomputes saved-result metrics, paired bootstrap, and attempt accounting.
It does not claim to audit tool activity. `audit` separately verifies file hashes,
raw event coverage, usage/final-response identity, and saved solver outcomes.
Missing evidence yields INCOMPLETE, UNKNOWN tool-audit status, null aggregate tool
events, and exit code 2. Contradictory or tampered evidence yields FAILED.
Neither command runs a model, executes verification plans, or launches a solver.
The package does not establish independently re-executed theorem proofs or an
authenticated transcript from the server.

The export identifies 61 historical solver-log checksum mismatches affecting nine
earlier scenario-method scores in seven shared verifier directories. The scoring
code reused a directory for identical scenario/policy/verifier/material keys and
wrote new logs when another method received the same policy. Available later logs
are preserved, but they cannot replace the missing byte-identical earlier logs.
The full historical audit is therefore INCOMPLETE even with every exported file
present. All four Meta-Refine discordant cases are unaffected. Saved scores remain
unchanged; no missing historical evidence is repaired by re-execution.

Manifest hashes distinguish checksums recorded during the experiment from hashes
first captured at export (notably validate.json, which had no prior raw checksum).
No evidence was redacted, translated, or rewritten. Raw files and copied original
records can contain historical user paths, temporary paths, and session IDs;
these are inert provenance and do not make execution depend on that host.
This package is portable but is NOT an anonymous submission supplement.
Produce separately labeled derived redacted copies if an anonymous supplement is
later required; preserve these originals and their hashes.
