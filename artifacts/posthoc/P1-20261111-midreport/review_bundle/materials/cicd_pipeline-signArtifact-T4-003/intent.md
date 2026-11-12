# Artifact Signing — Provenance Binding and Network Restriction

## Natural-Language Scenario

The system manages a continuous integration and deployment pipeline for a software company.

The people involved are committers, approvers, release managers, and site reliability engineers.

One person may hold both the committer and approver roles at the same time, and one person may hold both the approver and release manager roles at the same time.

The resources are deployments and artifacts.

Every deployment records its committer, its approver, its target environment, its change risk level, its artifact, and its status.

Every artifact records who built it, whether it has been signed, its build tags, and its status.

Each request to sign an artifact carries the current time, the source network address it was sent from, and whether it is an emergency change.

The committer who built an artifact must be the one who signs it.

A committer who did not build the artifact must not sign it, even if they are a committer, an approver, or a release manager on the same team.

An artifact may be signed only after its build has succeeded and its status shows as built.

An artifact may be signed only when it carries the "production-release" build tag.

An artifact may be signed only when the signing request comes from the corporate VPN network range.

A request by the committer who built a "production-release" artifact, whose build has succeeded, sent from the corporate VPN, to sign that artifact must be able to succeed.
