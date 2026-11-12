# P1: Offline post-hoc analysis and mid-report evidence preparation

Analysis date: 2026-11-11. **POST-HOC**, separate from the original E0-E5 experiments and a1/a2 analyses. No new model calls, solver executions, policy edits, sample selection, or held-out reads.

## Research Question

What do the completed 20 paired validation scenarios support about Meta versus Refine, and how much of the saved evidence can an external reviewer audit offline?

## Hypothesis

The original exploratory directional hypothesis Meta > Refine is retained. P1 does not invent a new positive-result criterion. Error explanations and bootstrap uncertainty are post-hoc diagnostics.

## Setup and Controlled Variables

The source is E4's 80 final scenario-method results, with all syntax/type failures included. No score or prediction was changed. The four discordant cases were checked against raw final responses, validator output, and solver logs rather than copied report prose. Bootstrap resamples the 20 scenario pairs with replacement, retaining both outcomes together. It uses 100000 replicates, Python MT19937/randrange, seed 20261111, a 95% percentile interval, and type-7 endpoint interpolation. It conditions on these two generated harnesses and the saved outputs.

## Execution Status

IMPLEMENTED, TESTED, EXECUTED, ANALYZED offline. Nineteen focused tests pass. The standalone review package was copied to a new temporary directory and executed under a Python audit hook that rejects `/Users/` reads, networking, and subprocesses. Saved-result metrics remained identical after deleting all raw evidence from the temporary copy. Missing raw evidence correctly returned INCOMPLETE/UNKNOWN, with a null aggregate tool-event count.

## Results

| Method | Pass | Syntax failure | Schema/type failure | Semantic failure | Unresolved final output |
| --- | --- | --- | --- | --- | --- |
| Manual (fixed baseline) | 12/20 | 0 | 0 | 8 | 0 |
| Direct | 10/20 | 0 | 2 | 8 | 0 |
| Meta | 9/20 | 0 | 4 | 7 | 0 |
| Refine | 11/20 | 0 | 1 | 8 | 0 |

Paired outcomes remain both_pass=8, meta_only=1, refine_only=3, both_fail=8. Meta minus Refine is **-10 percentage points**, with a **post-hoc 95% paired bootstrap interval of [-30, +10] points**. This interval does not establish equivalence or a general ranking. Eighty outputs are not eighty independent scenarios.

The experiment ledger remains 110/120 attempts: three diagnostics, 20 development policy calls, six construction attempts for five logical stages, and 81 validation attempts for 80 final policies. Two attempts timed out without final responses and were each retried once under the disclosed uniform amendment. Their missing usage remains unknown. P1 adds zero experimental calls.

## Error Analysis

All three Refine-only cases are Meta schema/type failures: Kubernetes secret access, IoT command sending, and immigration security-check clearance. Their raw validator output identifies decimal comparison methods applied to datetime values, with return code 3 and no subsequent Meta semantic checks. Refine passes 7, 8, and 5 checks respectively.

The sole Meta-only case is grant obligation. Refine passes the type gate but fails a floor and a ceiling check: its permit/veto combination denies a GrantsOfficer-only requester with a different approver, and allows a dual-role requester without approval state. Both counterexamples are preserved verbatim. Meta passes all five checks. No hypothetical policy repair was evaluated.

See [all four detailed cases](materials/case_evidence.json), [two body examples](materials/main_text_cases.md), and [tables](materials/tables.md). No type-valid conditional subset replaces the primary result.

## Evidence Portability and Newly Identified Gaps

**Layer 1: COMPLETE.** The package alone can recompute all primary rates, error counts, paired outcomes, bootstrap results, and 110-attempt accounting from saved records. It does not need local source paths, Codex, Cedar, cvc5, credentials, or a network.

**Layer 2: INCOMPLETE.** All 110 model-event files and their recorded hashes are available. The exported current solver outputs reproduce all 80 saved decisions and 538 check statuses. However, **61 historical per-check hashes across nine earlier outputs do not match available files**. Seven verifier cache directories were shared by identical scenario/policy/verifier/material keys; the original evaluator wrote fresh logs for later methods into those directories. No matching older byte versions were found in the existing selected-scenario verifier store. There are 477 matching historical check hashes; 71 of 80 scores retain all their recorded per-check bytes. Validator-gate files had no execution-time hashes, so their hashes are explicitly first-captured-at-export.

These later available logs are not silently substituted for older originals. The discrepancy is retained in the manifest/index, [audit JSON](analysis/evidence_audit.json), and [gap table](materials/historical_solver_hash_gaps.csv). All four discordant cases are unaffected. The old audit checked model-event hashes and did not audit solver-log hashes; P1 expands that scope and corrects the completeness claim without rewriting the old reports.

The standalone auditor returns exit code 2, INCOMPLETE, UNKNOWN aggregate tool-audit status, and null aggregate tool events for the full bundle's known historical gap. Tampered exported bytes or inconsistent decisions return FAILED. A missing raw directory still permits layer-1 recomputation but cannot pass layer 2. No solver is re-run and no cryptographic server attestation is claimed.

## Interpretation

The observed difference has a useful error decomposition: three Meta losses stop at the type gate, while its one exclusive success reflects a different semantic outcome. This motivates a future controlled target-language diagnostic; it does not show that repairing Meta would reverse the result. One construction repeat cannot estimate general method effects. The material supports an honest exploratory mid report, including a negative observation and transparent evidence limitations.

## Limitations

See the concise [limitations and deviations](materials/limitations_and_deviations.md). Manual is accurately described as a fixed baseline prepared in an AI-assisted workflow; human-only authorship is not established. The actual serving model, failed-attempt usage, timing-discrepancy cause, and missing earlier solver bytes remain unknown. The portable raw package contains historical paths/session IDs and is not an anonymous supplement.

## Next Action

Use the [2-4 page ACL-style outline](materials/acl_midreport_outline.md), [verified references](materials/references.md), [BibTeX](materials/references.bib), and [claim-to-evidence index](materials/evidence_index.md) to write the report. A full submission manuscript was not drafted. Prioritize independent repeated harness construction, expanded validation, uniform target-language guidance diagnostics, and final held-out evaluation only after the final freeze. Future runs also need distinct per-attempt solver logs and verified timing behavior.

## Reproduction

From a new clone, with Python 3.10+ and no model/solver installation:

```bash
python3 scripts/review_offline.py analyze artifacts/posthoc/P1-20261111-midreport/review_bundle --output /tmp/new-review-metrics
python3 scripts/audit_evidence.py
python3 scripts/validate_review_bundle.py artifacts/posthoc/P1-20261111-midreport/review_bundle --output /tmp/new-portability-check.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The audit intentionally returns 2 for the documented historical gaps. Use fresh output paths; existing outputs are rejected. The self-contained package also includes `review.py`, so it works without the repository. See [package instructions](review_bundle/README.md) and [relocation validation](portable_validation.json).

For transfer, use [review_bundle.zip](review_bundle.zip) with its [SHA-256 file](review_bundle.zip.sha256). [The preservation record](provenance/original_evidence_preservation.json) confirms that all 575 checked original evidence/config/data files remain byte-identical to the pre-P1 Git commit.

Exporting again from the original evidence store uses `python3 scripts/export_review_bundle.py --output /new/package/path`. Missing files and unmatched original hashes are disclosed, never repaired. The manifest records original checksums where available, export-time hashes otherwise, and no redactions. Only the allowlisted evidence and selected materials are copied; final held-out content and credential stores are excluded.
