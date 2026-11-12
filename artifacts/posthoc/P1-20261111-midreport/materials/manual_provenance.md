# Fixed-baseline provenance

POST-HOC provenance correction. The historical method label is Manual; report it as **Manual (fixed baseline)**.

The baseline was prepared within this AI-assisted Codex research-engineering workflow. The saved experiment artifacts do not establish independent human-only authorship. The original Git commit's author identity records who committed the repository, not who composed every instruction. Consequently “human-authored” and “manually authored” in the initial protocol/E2 narrative should not be repeated as a verified provenance claim. Those historical artifacts remain unchanged; this note corrects the current description.

Verified facts:

- `configs/manual.json` contains a static instruction/checklist baseline with zero dedicated experimental construction-stage calls.
- Its SHA-256 is `5c5f32c9fad523a5563f5d69f0da1d150ec814713f6456d5736a47999bb8a92f`.
- Its bytes are identical to `configs/manual.json` inside both E2 and E4 `snapshot.zip` archives.
- The 110-task ledger includes no separate Manual harness-construction task. This accounting excludes the research assistant's setup work and is not proof of human-only authorship.

Suggested method-table wording: “Fixed static baseline prepared during an AI-assisted research-engineering setup; no experimental harness-construction stages.” A precise division of human and assistant editorial contributions is not available from the exported experimental task records.
