# Source Repository Cloning — Clearance and Repository Eligibility

## Natural-Language Scenario

The system manages access to source-code repositories, their pull requests, and their branches for a software engineering organization.

The people involved are developers, reviewers, maintainers, and security leads.

One person may hold both the developer and reviewer role at the same time.

The resources are repositories, pull requests, and branches.

Every repository records its owner, team, sensitivity classification, whether its default branch is protected, its topic tags, and its lifecycle status.

Every pull request records its repository, author, approvers, target branch, approval count, lines changed, whether it requires security review, and its status.

Every branch records its name and whether it is protected.

Each requester carries a clearance level of public, internal, confidential, or restricted, in ascending order of access.

To clone a repository, the requester's clearance level must be at least as high as the repository's sensitivity classification.

A developer, reviewer, maintainer, or security lead must not clone a repository whose sensitivity classification is higher than their own clearance level.

Cloning is only permitted when the repository carries the "regulated-data" topic tag.

A repository that does not carry the "regulated-data" tag may be cloned without this clearance check applying.

Cloning is only permitted when the repository's lifecycle status is active.

A repository that has been archived may not be cloned, even by a requester whose clearance is otherwise sufficient.

A request by a developer with confidential clearance to clone an active repository tagged "regulated-data" and classified as confidential must be able to succeed.
