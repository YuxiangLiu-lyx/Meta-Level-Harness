# CI/CD Deployment Approval

## Natural-Language Scenario

The system manages deployment approvals in a CI/CD pipeline.

The people involved are committers, approvers, release managers, and SREs. One person may hold both the committer and approver roles, or both the approver and release manager roles, at the same time.

The resources are deployments and artifacts. Every deployment records its committer, approver, target environment, change risk, artifact, and status.

Every artifact records who built it, whether it is signed, its build tags, and its status.

Each requester carries a deploy tier.

Each request carries the current time, source IP, and whether the change is an emergency change.

An approver or release manager may approve a deployment.

An approver who committed a deployment must not approve it.

A release manager who committed a deployment must not approve it.

When a deployment's change-risk score crosses the extra-scrutiny threshold, an approver or release manager may approve it only after it has been submitted for review.

When a deployment's change-risk score does not cross the extra-scrutiny threshold, the submitted-for-review requirement does not block approval.

A request by an approver to approve a deployment that does not trip any prohibition above must be able to succeed.