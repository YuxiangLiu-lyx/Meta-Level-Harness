# kubernetes_rbac-readSecret-T3-033

POST-HOC case audit. All four discordant cases are included; no case was resampled or repaired.

Pair category: **refine_only**.

## Required input excerpts

Line numbers refer to the original requirements/schema strings, not a rewritten specification.

```text
L5: The resources are namespaces, workloads, namespace secrets, and service account tokens. Every namespace secret records its namespace, owner, sensitivity, and status.
L7: Each requester carries clearance, granted scope, and group membership.
L11: A deployer, maintainer, cluster operator, or service account may read a namespace secret only when their clearance is at least as high as the secret's sensitivity.
L13: A deployer, maintainer, cluster operator, or service account with lower clearance than the secret's sensitivity must not read that secret.
L15: A deployer, maintainer, cluster operator, or service account may read a namespace secret they own when no other rule blocks the request.
L17: A deployer, maintainer, cluster operator, or service account must not read a namespace secret they do not own.
L19: A deployer, maintainer, cluster operator, or service account may read a namespace secret only when the service account token presented for the request has not expired.
L21: A deployer, maintainer, cluster operator, or service account must not read a namespace secret using an expired service account token.
```

```text
L12:     clearance: Long,
L18:     clearance: Long,
L29:     ownerUser?: User,
L30:     ownerServiceAccount?: ServiceAccount,
L31:     sensitivity: Long,
L35: entity ServiceAccountToken {
L36:     expiresAt: datetime,
L44:         currentTime: datetime,
L47:         serviceAccountToken: ServiceAccountToken,
```

Complete inputs: [frozen validation JSONL](../../review_bundle/source/data/validation20.jsonl).

## Meta: SCHEMA_FAIL

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-meta-05/final.txt); SHA-256 `7eb6052c9d57466272445b6d281973ab70c59ba7080864d83a78c468e446b083`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L7:     (principal is User || principal is ServiceAccount) &&
L8:     principal.clearance >= resource.sensitivity &&
L9:     (
L10:         (principal is User && resource has ownerUser && resource.ownerUser == principal) ||
L11:         (principal is ServiceAccount && resource has ownerServiceAccount && resource.ownerServiceAccount == principal)
L12:     ) &&
L13:     context.currentTime.lessThan(context.serviceAccountToken.expiresAt)
L14: };
L45:     (principal is User || principal is ServiceAccount) &&
L46:     context.currentTime.greaterThanOrEqual(context.serviceAccountToken.expiresAt)
L47: };
```

Original validator return code: `3`. [Complete original log](../../review_bundle/raw/verifier/adbf462a9db777577286c8300ea420096a9c4eeaf0f229d09147c5c6fe2e381c/validate.json).

```text
  × policy set validation failed
  ╰─▶ for policy `policy0`, unexpected type: expected decimal but saw datetime
    ╭─[13:34]
 12 │     ) &&
 13 │     context.currentTime.lessThan(context.serviceAccountToken.expiresAt)
    ·                                  ─────────────────────────────────────
 14 │ };
    ╰────
```

Semantic checks were **not run** after the failed schema/type gate. Their outcome is unknown.

## Refine: PASS

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-refine-05/final.txt); SHA-256 `4146410382ecfb2d0734721eec7154affe373b2b0db76ab78b7efdcd017ac17c`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L6: when {
L7:     (principal is User && resource has ownerUser && resource.ownerUser == principal) ||
L8:     (principal is ServiceAccount && resource has ownerServiceAccount && resource.ownerServiceAccount == principal)
L9: };
L15: )
L16: when {
L17:     principal.clearance < resource.sensitivity
L33:     resource is NamespaceSecret
L34: )
L35: when {
L36:     context.currentTime >= context.serviceAccountToken.expiresAt
L37: };
```

Original validator return code: `0`. [Complete original log](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/validate.json).

```text
  ☞ policy set validation passed
  ╰─▶ no errors or warnings
```

- `owned_secret_clearance_read_floor` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-00.json).
- `read_secret_requires_sufficient_clearance` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-01.json).
- `read_secret_excludes_non_owners` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-02.json).
- `read_secret_excludes_expired_token` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-03.json).
- `owned_secret_unexpired_token_read_floor` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-04.json).
- `service_account_read_secret_excludes_expired_token` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-05.json).
- `deployer_read_namespace_secret_liveness` (liveness-overlap): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/b0fb9a00b1e45bde716b6fe72325a02c86f3b2b9ac97be29cb813e13eb7b56f3/check-06.json).

## Supported explanation

Meta calls decimal comparison methods on datetime-valued currentTime and expiresAt. The recorded validator exits with code 3 before any semantic checks. Refine uses the datetime >= operator for the expired-token veto and passes all seven recorded checks. This identifies a target-language type/API error in this particular Meta output.

## Unsupported conclusions

It does not establish that the Meta authorization logic would pass after a syntax/type edit: no edited policy was evaluated. It does not show a general semantic-reasoning advantage for Refine or identify which harness sentence caused the error.

Both results retain their original contribution to the primary 20-scenario denominator. This case audit does not define a replacement metric.
