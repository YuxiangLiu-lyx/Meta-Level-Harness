# grant_awards-chain2-T3-005

POST-HOC case audit. All four discordant cases are included; no case was resampled or repaired.

Pair category: **meta_only**.

## Required input excerpts

Line numbers refer to the original requirements/schema strings, not a rewritten specification.

```text
L1: This document sets out who may approve grant awards and obligate their funds in the federal grant award management system.
L2: The people involved are reviewers, program officers, grants officers, and applicants; one person may act as both a reviewer and a program officer, and one person may act as both a program officer and a grants officer.
L3: The resources are applications, which record their applicant, assigned reviewers, funding tier, requested amount, program code, and status; and awards, which record their application, who approved them, who obligated their funds, their amount, whether they are flagged high risk, and their status.
L5: In this workflow an award is first approved and then its funds are obligated, and the obligation step can see the award's status, who approved it, and who obligated it.
L6: A program officer or grants officer may approve an award only when their approval authority is at or above the application's funding tier, and when their authority falls below that tier the approval must not proceed.
L7: The grants officer who approved an award must not obligate its funds, so the obligation must fall to a different grants officer.
L8: Funds may be obligated only when the requester holds the designated role, and when the requester lacks that role the obligation must not proceed.
L9: A run through the workflow by a program officer that trips none of the prohibitions above must be able to succeed.
```

```text
L1: entity Role enum ["Reviewer", "ProgramOfficer", "GrantsOfficer", "Applicant"];
L4:     roles: Set<Role>,
L19:     approvedBy?: User,
L20:     obligatedBy?: User,
L36: action obligateFunds appliesTo {
```

Complete inputs: [frozen validation JSONL](../../review_bundle/source/data/validation20.jsonl).

## Meta: PASS

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-meta-13/final.txt); SHA-256 `40f9b05d7c485717ba0b1c46c24ad08a206272d3caa38a4f4af5341f70a0c59a`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L23: permit (
L24:     principal is User,
L25:     action == Action::"obligateFunds",
L26:     resource is Award
L27: )
L28: when {
L29:     principal.roles.contains(Role::"GrantsOfficer") &&
L30:     resource has approvedBy &&
L31:     resource.approvedBy != principal
```

Original validator return code: `0`. [Complete original log](../../review_bundle/raw/verifier/3f7594a4a4161f76647862a625170dc6fcc0f35fbdadaf7b1dd44ac9a97d8c19/validate.json).

```text
  ☞ policy set validation passed
  ╰─▶ no errors or warnings
```

- `approve_award_authorized_role_and_tier_floor` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/3f7594a4a4161f76647862a625170dc6fcc0f35fbdadaf7b1dd44ac9a97d8c19/check-00.json).
- `approve_award_only_authorized_role_and_tier_ceiling` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/3f7594a4a4161f76647862a625170dc6fcc0f35fbdadaf7b1dd44ac9a97d8c19/check-01.json).
- `obligate_funds_grants_officer_different_from_approver_floor` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/3f7594a4a4161f76647862a625170dc6fcc0f35fbdadaf7b1dd44ac9a97d8c19/check-02.json).
- `obligate_funds_only_grants_officer_after_approval_and_not_approver_ceiling` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/3f7594a4a4161f76647862a625170dc6fcc0f35fbdadaf7b1dd44ac9a97d8c19/check-03.json).
- `obligate_funds_disjoint_from_same_approver` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/3f7594a4a4161f76647862a625170dc6fcc0f35fbdadaf7b1dd44ac9a97d8c19/check-04.json).

## Refine: SEMANTIC_FAIL

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-refine-13/final.txt); SHA-256 `e24434175f871e83ea5df57306630dc24ab3824ae74c91ecdd2b2ceeded560fc`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L23: permit (
L24:     principal is User,
L25:     action == Action::"obligateFunds",
L26:     resource is Award
L27: )
L28: when {
L29:     principal.roles.contains(Role::"ProgramOfficer")
L30: };
L31: 
L32: forbid (
L33:     principal is User,
L34:     action == Action::"obligateFunds",
L35:     resource is Award
L36: )
L37: when {
L38:     !principal.roles.contains(Role::"GrantsOfficer")
L39: };
L46: when {
L47:     principal.roles.contains(Role::"GrantsOfficer") &&
L48:     resource has approvedBy &&
L49:     resource.approvedBy == principal
L50: };
```

Original validator return code: `0`. [Complete original log](../../review_bundle/raw/verifier/421f31b9ff4dfab22a8f26c4299fccf8f527eca23efe06cc1ba3b0d33c78c8a2/validate.json).

```text
  ☞ policy set validation passed
  ╰─▶ no errors or warnings
```

- `approve_award_authorized_role_and_tier_floor` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/421f31b9ff4dfab22a8f26c4299fccf8f527eca23efe06cc1ba3b0d33c78c8a2/check-00.json).
- `approve_award_only_authorized_role_and_tier_ceiling` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/421f31b9ff4dfab22a8f26c4299fccf8f527eca23efe06cc1ba3b0d33c78c8a2/check-01.json).
- `obligate_funds_grants_officer_different_from_approver_floor` (floor): **FAIL**. [Raw solver output](../../review_bundle/raw/verifier/421f31b9ff4dfab22a8f26c4299fccf8f527eca23efe06cc1ba3b0d33c78c8a2/check-02.json).

Original counterexample (verbatim stdout):

```text
✗ Policy set 1 implies policy set 2: DOES NOT HOLD
  Counterexample found:
principal: User::"", action: Action::"obligateFunds", resource: Award::""
context: {currentTime: datetime("1970-01-01").offset(duration("0ms")), emergencyDeclared: false, fromGovernmentNetwork: false}
entities: [
  Role::"ProgramOfficer",
  Role::"Applicant",
  User::"" {
    approvalAuthority: -1,
    roles: [Role::"GrantsOfficer"],
  },
  Action::"obligateFunds",
  Award::"" {
    amount: decimal("-0.0001"),
    application: Application::"",
    approvedBy: User::"A",
    highRisk: true,
    obligatedBy: User::"",
    status: "",
  },
  Action::"approveAward",
  Role::"GrantsOfficer",
  User::"A" {
    approvalAuthority: -1,
    roles: [Role::"GrantsOfficer"],
  },
  Application::"" {
    applicant: User::"",
    assignedReviewers: [],
    fundingTier: 0,
    programCode: "",
    requestedAmount: decimal("0.0000"),
    status: "",
  },
  Role::"Reviewer",
]
```

- `obligate_funds_only_grants_officer_after_approval_and_not_approver_ceiling` (implies): **FAIL**. [Raw solver output](../../review_bundle/raw/verifier/421f31b9ff4dfab22a8f26c4299fccf8f527eca23efe06cc1ba3b0d33c78c8a2/check-03.json).

Original counterexample (verbatim stdout):

```text
✗ Policy set 1 implies policy set 2: DOES NOT HOLD
  Counterexample found:
principal: User::"", action: Action::"obligateFunds", resource: Award::""
context: {currentTime: datetime("1970-01-01").offset(duration("0ms")), emergencyDeclared: false, fromGovernmentNetwork: false}
entities: [
  User::"" {
    approvalAuthority: -1,
    roles: [Role::"GrantsOfficer", Role::"ProgramOfficer"],
  },
  Role::"Reviewer",
  Award::"" {
    amount: decimal("-0.0001"),
    application: Application::"",
    highRisk: true,
    obligatedBy: User::"",
    status: "",
  },
  Application::"" {
    applicant: User::"",
    assignedReviewers: [],
    fundingTier: 0,
    programCode: "",
    requestedAmount: decimal("0.0000"),
    status: "",
  },
  Role::"GrantsOfficer",
  Action::"approveAward",
  Action::"obligateFunds",
  Role::"Applicant",
  Role::"ProgramOfficer",
]
```

- `obligate_funds_disjoint_from_same_approver` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/421f31b9ff4dfab22a8f26c4299fccf8f527eca23efe06cc1ba3b0d33c78c8a2/check-04.json).

## Supported explanation

Both policies pass syntax and schema validation. Refine permits obligateFunds for ProgramOfficer but forbids it for anyone without GrantsOfficer. The resulting grant effectively requires both roles. The saved floor counterexample has only GrantsOfficer and an approvedBy value pointing to another user, so a required request is denied. The saved ceiling counterexample has both roles and no approvedBy attribute, so Refine allows an obligation outside the verification plan. Meta requires GrantsOfficer, approvedBy presence, and a different approver and passes all five recorded checks.

## Unsupported conclusions

This one semantic success does not show that Meta generally reasons better about workflows. The approval-presence requirement is explicitly enforced by the verification plan; its interpretation from the prose is not independently adjudicated. Passing five checks is not proof of correctness against every possible informal reading.

Both results retain their original contribution to the primary 20-scenario denominator. This case audit does not define a replacement metric.
