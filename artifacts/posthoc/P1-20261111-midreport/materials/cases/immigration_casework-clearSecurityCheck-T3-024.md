# immigration_casework-clearSecurityCheck-T3-024

POST-HOC case audit. All four discordant cases are included; no case was resampled or repaired.

Pair category: **refine_only**.

## Required input excerpts

Line numbers refer to the original requirements/schema strings, not a rewritten specification.

```text
L3: The people involved are adjudication officers, supervisory officers, background investigators, and records clerks. One person may hold both the adjudication officer and background investigator roles, and one person may hold both the supervisory officer and adjudication officer roles.
L15: A background investigator may clear a security check only while it is pending.
L17: A supervisory officer may clear a security check even when it is not pending.
L19: A background investigator and a supervisory officer may clear a security check only during the permitted time window.
L21: A background investigator and a supervisory officer must not clear a security check outside the permitted time window.
L23: A request by a background investigator to clear a pending security check during the permitted time window, tripping no prohibition above, must be able to succeed.
```

```text
L2:     roles: Set<Role>,
L7: entity Role enum ["AdjudicationOfficer", "SupervisoryOfficer", "BackgroundInvestigator", "RecordsClerk"];
L20:     status: String,
L26:     status: String,
L27:     permittedWindowStart: datetime,
L28:     permittedWindowEnd: datetime,
L36:     status: String,
L44:         currentTime: datetime,
```

Complete inputs: [frozen validation JSONL](../../review_bundle/source/data/validation20.jsonl).

## Meta: SCHEMA_FAIL

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-meta-16/final.txt); SHA-256 `902d190a4bdb710c0a7d0c23115d8b8e1992bbd5525df6c873fb103ff5721272`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L6: when {
L7:     principal.roles.contains(Role::"BackgroundInvestigator") &&
L8:     resource.status == "pending" &&
L9:     context.currentTime.greaterThanOrEqual(resource.permittedWindowStart) &&
L10:     context.currentTime.lessThanOrEqual(resource.permittedWindowEnd)
L11: };
L18: when {
L19:     principal.roles.contains(Role::"SupervisoryOfficer") &&
L20:     context.currentTime.greaterThanOrEqual(resource.permittedWindowStart) &&
L21:     context.currentTime.lessThanOrEqual(resource.permittedWindowEnd)
L22: };
L30:     (principal.roles.contains(Role::"BackgroundInvestigator") ||
L31:      principal.roles.contains(Role::"SupervisoryOfficer")) &&
L32:     !(context.currentTime.greaterThanOrEqual(resource.permittedWindowStart) &&
L33:       context.currentTime.lessThanOrEqual(resource.permittedWindowEnd))
L34: };
```

Original validator return code: `3`. [Complete original log](../../review_bundle/raw/verifier/fb7bba924712f641d5b459f1ac3bafb74101ba8eeb604bb9a4df2b2b9b389637/validate.json).

```text
  × policy set validation failed
  ╰─▶ for policy `policy0`, unexpected type: expected decimal but saw datetime
    ╭─[9:5]
  8 │     resource.status == "pending" &&
  9 │     context.currentTime.greaterThanOrEqual(resource.permittedWindowStart) &&
    ·     ─────────────────────────────────────────────────────────────────────
 10 │     context.currentTime.lessThanOrEqual(resource.permittedWindowEnd)
    ╰────
```

Semantic checks were **not run** after the failed schema/type gate. Their outcome is unknown.

## Refine: PASS

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-refine-16/final.txt); SHA-256 `aeb593fab529972a2c529456ffe05abc29df01ceccb94ddb3683fd4f6393246b`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L6: when {
L7:     principal.roles.contains(Role::"BackgroundInvestigator") &&
L8:     resource.status == "pending" &&
L9:     context.currentTime >= resource.permittedWindowStart &&
L10:     context.currentTime <= resource.permittedWindowEnd
L11: };
L18: when {
L19:     principal.roles.contains(Role::"SupervisoryOfficer") &&
L20:     context.currentTime >= resource.permittedWindowStart &&
L21:     context.currentTime <= resource.permittedWindowEnd
L22: };
L29: when {
L30:     principal.roles.contains(Role::"BackgroundInvestigator") &&
L31:     resource.status != "pending"
L32: };
L39: when {
L40:     (principal.roles.contains(Role::"BackgroundInvestigator") ||
L41:      principal.roles.contains(Role::"SupervisoryOfficer")) &&
L42:     (context.currentTime < resource.permittedWindowStart ||
L43:      context.currentTime > resource.permittedWindowEnd)
```

Original validator return code: `0`. [Complete original log](../../review_bundle/raw/verifier/774e290071dc5afa0b9a635f05b81697aeb9ed886f8352eb95b1211e937af79c/validate.json).

```text
  ☞ policy set validation passed
  ╰─▶ no errors or warnings
```

- `investigator_or_supervisor_clear_security_check_in_window_floor` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/774e290071dc5afa0b9a635f05b81697aeb9ed886f8352eb95b1211e937af79c/check-00.json).
- `clear_security_check_limited_to_authorized_roles_and_window` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/774e290071dc5afa0b9a635f05b81697aeb9ed886f8352eb95b1211e937af79c/check-01.json).
- `clear_security_check_outside_window_disjointness` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/774e290071dc5afa0b9a635f05b81697aeb9ed886f8352eb95b1211e937af79c/check-02.json).
- `background_investigator_non_pending_clear_disjointness` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/774e290071dc5afa0b9a635f05b81697aeb9ed886f8352eb95b1211e937af79c/check-03.json).
- `background_investigator_pending_clear_security_check_liveness` (liveness-overlap): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/774e290071dc5afa0b9a635f05b81697aeb9ed886f8352eb95b1211e937af79c/check-04.json).

## Supported explanation

Meta again invokes decimal comparison methods on datetime window endpoints; validation exits with code 3 before semantic evaluation. Refine uses datetime comparison operators and passes the five saved floor, ceiling, disjointness, and liveness checks. Its non-pending investigator veto is visible in the original output.

## Unsupported conclusions

A passing verification plan does not settle every informal interpretation of overlapping investigator/supervisor roles or exception precedence. These outputs do not isolate a causal effect of guidance versus revision, and the Meta semantic outcome after a hypothetical type repair remains unknown.

Both results retain their original contribution to the primary 20-scenario denominator. This case audit does not define a replacement metric.
