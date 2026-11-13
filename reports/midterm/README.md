# Midterm progress report

Title: **An Exploratory Comparison of Static Harness Construction for Cedar Policy Synthesis**

The English manuscript is written as a short research progress paper: research question and related work, experimental design, completed work, preliminary validation results, two verified error cases, limitations, and prioritized next steps. The supplied course requirements are recorded in [course_requirements.md](course_requirements.md).

## Deliverables

| File | Purpose |
| --- | --- |
| [main.pdf](main.pdf) | Anonymous ACL review-format PDF. |
| [main.tex](main.tex) | Editable manuscript source. |
| [references.bib](references.bib) | Six cited and verified references. |
| [abstract.txt](abstract.txt) | Plain-text abstract for review or the OpenReview form. |
| [verification.json](verification.json) | Actual page count, abstract length, build/anonymity checks, and evidence limitations. |
| [claim_evidence_map.md](claim_evidence_map.md) | Internal source index; not an anonymous attachment. |
| `checks/` | Supporting offline and PDF check records; not an anonymous attachment. |

The PDF has **3 body pages and 1 reference page**. The abstract is **104 words** by whitespace-delimited counting. The official ACL `review` option hides author names. All four pages were rendered and visually checked; references begin on page 4. No unresolved citations, missing files, or overfull boxes remain. One underfull line and one underfull column warning remain; both were visually inspected and are readable. The final page counts and artifact hashes are recorded in `verification.json`.

## Build

From the repository root:

```bash
sh reports/midterm/build.sh
```

The command uses latexmk, pdfLaTeX and BibTeX, puts intermediate files in the ignored `build/` directory, and writes `main.pdf`. TeX Live 2025 (pdfTeX 1.40.27) and latexmk 4.86a were used. Standard LaTeX packages include Times, latexsym, fontenc, microtype, inconsolata, booktabs, natbib and hyperref. The bundled official `acl.sty` and `acl_natbib.bst` are unchanged; their revision and hashes are in `template_provenance.json`. No network connection, experimental model call, or solver run is needed to build.

Optional macOS rendering and inspection, using a new output path:

```bash
swift reports/midterm/inspect_pdf.swift reports/midterm/main.pdf /tmp/new-midterm-pdf-review
```

After any edits, rebuild and recheck the PDF; the verification hashes apply only to the current files.

## Evidence and check scope

All results come from saved E4 outcomes and P1 post-hoc analysis. Success counts remain 12/20, 10/20, 9/20, and 11/20; all type failures stay in the primary denominator. Meta-Refine counts remain 8/1/3/8, with a -10 percentage-point difference and a conditional paired bootstrap interval of [-30,+10] points.

The same-day offline verification from the preceding preparation turn is retained in `checks/`: 19 tests passed, saved-result recomputation matched P1, and portable bundle relocation passed. No experiment implementation changed afterward, so those tests were not rerun merely for this prose revision. The retained recomputation is checked again against current P1 and original E4 metrics; P1 and original preservation manifests are also checked for unchanged bytes. PDF compilation, rendering, abstract/page counts, and anonymity checks are new for this manuscript.

Three findings remain distinct:

1. Saved outcomes and call accounting can be recomputed offline.
2. Current exported validator/solver decisions support all 80 saved scores.
3. Full historical byte-level audit remains **INCOMPLETE**: 61 of 538 original semantic-check hashes are unavailable across nine results; 477 match. All four discordant cases retain their key evidence. No rerun is used to claim recovery.

The existing `scripts/audit_evidence.py` intentionally exits 2 for this gap. Incomplete raw coverage yields `UNKNOWN`/`null` for aggregate tool-event audit status, not a passing zero-event audit. Validator-gate hashes were first captured at export rather than execution.

## Submission handoff

The supplied deadline is **November 12, 2026**, with no exact time specified. One group member should upload the reviewed anonymous PDF to OpenReview and add the other members in the system. The report has not been uploaded, committed, or pushed by this preparation task.

Review the manuscript before uploading. It was prepared with AI assistance; the supplied requirement table does not specify an AI-writing policy, so any separate course rule still applies. No unsupported personal-authorship declaration is included. The manuscript contains no administrative placeholder paragraphs. Keep the internal evidence map, logs, source paths, and raw bundle out of an anonymous submission unless separately reviewed for that purpose.
