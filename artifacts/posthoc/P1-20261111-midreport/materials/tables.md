# Mid-report tables

POST-HOC organization of unchanged E0-E5 results.

## Methods

| method | design_stages | construction | construction_attempts | harness_repeats | validation_outputs |
| --- | --- | --- | --- | --- | --- |
| Manual (fixed baseline) | 0 | Static baseline prepared in AI-assisted research workflow | 0 | 1 | 20 |
| Direct | 1 | Frozen packet -> harness | 1 | 1 | 20 |
| Meta | 2 | Frozen packet -> guidance; fresh session -> harness | 3 | 1 | 20 |
| Refine | 2 | Frozen packet -> draft; fresh session -> revision | 2 | 1 | 20 |

Fixed conditions: official Codex CLI 0.162.0-alpha.17.2; requested gpt-6.1-sol, medium effort; static harness at most 500 words; fresh sessions; same schema/requirements/public instructions; no task tools, verifier feedback, or policy repair. Actual serving model unknown. Meta and Refine each have two logical stages, not necessarily equal compute.

## Data

| split | scenarios | families | structural_signatures | published_origins | purpose | content_opened |
| --- | --- | --- | --- | --- | --- | --- |
| design20 | 20 | 20 | 20 | {"rl": 3, "sft": 17} | shared development evidence | yes |
| validation20 | 20 | 20 | 20 | {"sft": 19, "rl": 1} | four-method paired validation | yes |
| published held-out | 375 | not inspected | not inspected | heldout | future final evaluation | no |

Upstream revision `206962d130d2c69d5e15f8103fa0953345cc7690`. Published SFT/RL counts: 4386/1039. Grouping uses the transitive union of scenario family and normalized schema+gold structural signature, then one sampled member from each of 40 shuffled groups (seed 20261110); 139 non-held-out groups were eligible. No new selection occurred in this analysis.

## Performance and mutually exclusive primary error classes

| method | scenarios | pass | success_rate | syntax_failure | schema_type_failure | semantic_failure | output_invalid | unresolved_or_protocol_failure | confirmed_overgrant | confirmed_overdeny |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Manual | 20 | 12 | 0.6 | 0 | 0 | 8 | 0 | 0 | 8 | 4 |
| Direct | 20 | 10 | 0.5 | 0 | 2 | 8 | 0 | 0 | 7 | 6 |
| Meta | 20 | 9 | 0.45 | 0 | 4 | 7 | 0 | 0 | 6 | 6 |
| Refine | 20 | 11 | 0.55 | 0 | 1 | 8 | 0 | 0 | 7 | 7 |

All type failures remain in the denominator. Overgrant/overdeny are overlapping diagnostics among semantically evaluated outputs, not additional mutually exclusive categories. No conditional type-valid subset rate replaces these results.

## Paired Meta-Refine outcomes

| category | scenarios |
| --- | --- |
| both_pass | 8 |
| meta_only | 1 |
| refine_only | 3 |
| both_fail | 8 |

Difference: -10 percentage points. Post-hoc paired percentile bootstrap: 95% interval [-30, +10] percentage points; 100,000 resamples of 20 scenario pairs, seed 20261111. Conditional on these harnesses and saved outputs; no construction randomness included. Zero in the interval does not imply equivalence.

## Infrastructure attempts (separate from final policy error classes)

| attempt_id | stage | configured_seconds | observed_wall_seconds | response_present | usage | recovery |
| --- | --- | --- | --- | --- | --- | --- |
| E3-20261110-meta-harness | construction | 180 | 180.02249789237976 | False | UNKNOWN | one same-input fresh-session retry |
| E4-20261110-validation-refine-17 | validation_policy | 180 | 1165.7377498149872 | False | UNKNOWN | one same-input fresh-session retry |

The 80 E4 final outputs required 81 attempts; the extra missing-response timeout belongs to Refine. Meta construction required one extra attempt before validation. Total: 110 attempts, 108 completed; five logical construction stages, 100 final policies, three smoke diagnostics. No new calls in P1.
