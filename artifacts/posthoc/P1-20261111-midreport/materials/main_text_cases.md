# Two cases for the report body

POST-HOC selection: one representative type failure and the sole Meta-only semantic failure. The appendix materials audit all four discordant scenarios. These are writing notes, not a complete report draft.

## Case A: Kubernetes token expiry (Refine only)

Use `kubernetes_rbac-readSecret-T3-033`. The requirement disallows reading with an expired service-account token; both `currentTime` and `expiresAt` have type `datetime`. Meta line 13 calls `context.currentTime.lessThan(context.serviceAccountToken.expiresAt)`; line 46 calls `greaterThanOrEqual`. The actual validator returns code 3 and reports `expected decimal but saw datetime`. Refine line 36 uses `context.currentTime >= context.serviceAccountToken.expiresAt` in a forbid and passes all seven recorded semantic checks.

This illustrates a schema/type failure that prevents semantic evaluation. Retain it as a main-metric failure; do not describe it as “almost correct” or assume a repair would pass. The same error class occurs in the other two Refine-only cases. No causal attribution to a particular harness sentence is established.

Evidence: [full case](cases/kubernetes_rbac-readSecret-T3-033.md), including original final-response hashes, validator output, and all seven solver logs.

## Case B: Grant obligation roles and approval state (Meta only)

Use `grant_awards-chain2-T3-005`. Refine permits `obligateFunds` for `ProgramOfficer` (line 29), forbids it without `GrantsOfficer` (line 38), and checks same-approver prohibition only if `approvedBy` exists (lines 47-49). The saved floor counterexample has a GrantsOfficer-only requester and a different approver: Refine wrongly denies it. The ceiling counterexample has both roles and no `approvedBy`: Refine grants it outside the plan's permitted slice. Meta lines 29-31 require GrantsOfficer, `approvedBy` presence, and a different approver; its five checks pass.

This is a confirmed semantic failure after both policies pass the type gate, with overdeny and overgrant evidence. It illustrates local grant/veto composition and workflow-state handling, not a general superiority claim for Meta. The requirement-to-plan interpretation remains part of the evaluation limitation.

Evidence: [full case](cases/grant_awards-chain2-T3-005.md), containing both original counterexamples verbatim and the exact policy excerpts.
