# Paired case review

Selection rule: the first scenario in frozen validation order from each of meta_only, refine_only, both_pass, and both_fail. Later outcomes cannot replace these cases. These examples explain observed outputs; they are not independent statistical samples or proof that a particular instruction caused an error.

## Meta passes, Refine fails

Scenario: `grant_awards-chain2-T3-005` (validation position 14).

Meta's obligateFunds permit requires the GrantsOfficer role, presence of approvedBy, and an approver different from the requester. It passes the published plan. Refine instead gives the permit to ProgramOfficer while separately forbidding non-GrantsOfficer requesters. The combined policy therefore excludes grants officers who are not also program officers. It also lacks an approvedBy guard on this permit, permitting some dual-role requests before approval is recorded. The saved floor and ceiling counterexamples confirm both missing permission and excess permission. This is an action-specific grant-composition error, even though both outputs correctly implement the approval authority condition.

## Refine passes, Meta fails

Scenario: `kubernetes_rbac-readSecret-T3-033` (validation position 6).

Meta calls currentTime.lessThan(expiresAt) and currentTime.greaterThanOrEqual(expiresAt). Cedar rejects these calls because the methods expect decimal while the schema supplies datetime. Refine uses the direct >= comparison for expiry and passes the plan. Meta's failure is a schema/type failure, not a solver crash or demonstrated semantic counterexample. Both outputs attempt to encode ownership, clearance, and token expiry; this pair illustrates how a small API/operator error can determine a scenario's result under one sample.

## Both pass

Scenario: `warehouse_fulfillment-pickOrder-T3-055` (validation position 1).

Both Meta and Refine pass syntax, schema, and every nonempty published semantic check. This is a shared success; it does not favor Meta. Full policy text and per-check results remain in the E4 task and score directories.

## Both fail

Scenario: `network_change_approval-chain2-T4-026` (validation position 4).

Both Meta and Refine use decimal-style comparison methods for datetime maintenance-window values, so both fail schema validation. Direct has the same type problem. Manual passes the type gate but fails semantic checks. No method is assigned a semantic-check pass merely because a type error prevented checks from running. This shared failure shows a residual weakness that extra design stages did not eliminate in this round.

## Scope of interpretation

The grant workflow text contains potentially ambiguous descriptions of a program officer's successful workflow; the reported classification follows the published reference checks. The Kubernetes and network-change failures are directly evidenced type errors. Repeating harness construction and generation is necessary to distinguish stable method effects from variation in individual outputs. The original hypothesis remains unchanged, and none of these observations was fed back into the frozen harnesses.
