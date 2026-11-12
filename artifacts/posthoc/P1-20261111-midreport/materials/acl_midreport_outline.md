# Outline for a 2-4 page anonymous ACL-style mid report

Writing material only; no complete submission manuscript is generated. Confirm the course's exact page/reference rules before typesetting; this outline does not assume a particular ACL venue's current submission policy.

Working title: **An Exploratory Comparison of Static Harness Construction for Cedar Policy Synthesis**.

## Four-page allocation

| Space | Content | Supporting material |
| --- | --- | --- |
| 0.25 page | Short abstract: question, four methods, 20 paired validation scenarios, observed negative difference, exploratory scope | P1 report; performance/pair tables |
| 0.5 page | Motivation and related work: formal plan compliance, instruction optimization, one revision versus guidance-first construction | Verified RAISE, Cedar, OPRO, Self-Refine references |
| 0.75 page | Methods and setup: static harness schema; construction stages; shared frozen packet; fixed baseline provenance; grouped split; fixed runtime; semantic evaluator | methods.csv; data_splits.csv; limitations |
| 0.75 page | Results: all four primary success rates and mutually exclusive error classes; 20-pair table; difference and post-hoc bootstrap interval | performance_error_types.csv; paired_counts.csv; bootstrap.json |
| 0.75 page | Error analysis: all four disagreements summarized, Kubernetes and grant-awards as two brief body cases | main_text_cases.md; four detailed case files |
| 0.5 page | Limitations and deviations: single construction repeat, compute/usage/timing limits, requirement-plan ambiguity, audit gap, a1/a2 correction | limitations_and_deviations.md; evidence index |
| 0.5 page | Work completed, evidence portability, and ordered next experiments | portable_validation.json; future-work paragraph |

References occupy the space allowed by the actual course instructions; do not assume they are excluded from the limit.

## Two-page compression

- Use a 60-80 word abstract and one short motivation paragraph.
- Merge methods and data into one compact table plus the fixed-runtime sentence.
- Keep all primary rates, error categories, four pair counts, and the conditional bootstrap interval.
- Give each body case two or three sentences and retain the source pointers in an accompanying evidence index if permitted.
- Reserve a paragraph for limitations and the historical log gap, and a paragraph for the ordered future work. Move detailed logs/case excerpts to review material, not into tiny unreadable type.

## Claims to make and avoid

- State that Meta trails Refine by 10 percentage points for these observed harnesses on this subset. The 95% post-hoc paired percentile interval is [-30, +10] points.
- State that all three Refine-only cases are Meta type failures and the sole Meta-only case is a Refine semantic failure. Include all type failures in the primary outcome.
- Do not claim a general ranking, significant superiority, equivalence, equal actual compute, or pure human authorship of Manual.
- Do not present a type-valid conditional subset as the main comparison. Do not claim that syntax fixes would recover Meta successes.
- Distinguish completed experiments from diagnostics and planned work. P1 added zero model/solver runs and did not open held-out data.
- State that metrics can be fully recomputed offline while full historical solver-log audit remains incomplete; the existence of a portable archive is not proof of complete historical evidence.

## Anonymity preparation

Use anonymous author fields in the chosen ACL review template. Do not include the named public repository URL, personal directory paths, account names, or session IDs in the manuscript. Cite public upstream research normally. The raw review bundle preserves such provenance and is not anonymous; if a supplement is required, prepare a separately marked redacted derivative with an explicit mapping/hash manifest while preserving the originals. Do not silently alter raw evidence to anonymize it.

## Prioritized next experiments

1. Independently repeat harness construction for each method under a newly frozen plan, allowing uncertainty across designs to be estimated.
2. Expand validation with new grouped scenarios and a prespecified analysis, keeping this first subset/results intact.
3. Run a controlled target-language diagnostic with identical Cedar operator/type guidance across all methods, rather than repairing only Meta outputs.
4. Evaluate the untouched final held-out only after methods and reporting decisions are frozen.

Prerequisites for any future execution: isolate verifier logs by attempt identity, test timeout-clock behavior, and adjudicate requirement/plan ambiguities. These are future changes, not alterations to E0-E5.
