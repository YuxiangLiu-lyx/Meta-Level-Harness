# Pull Request Review and Merge — Self-Approval Ban, Scrutiny Exception, and Author Separation

## Natural-Language Scenario

This document describes how a source-code repository access system controls who may review a pull request and who may merge it.
The people involved are developers, reviewers, maintainers, and security leads, and one person may hold developer together with reviewer at the same time.
The resources are repositories, which record their owner, team, sensitivity, whether the default branch is protected, topics, and status; pull requests, which record their repository, author, who approved them, target branch, approval count, lines changed, whether a security review is required, and status; and branches, which record their name and whether they are protected.
In this workflow a pull request is first reviewed and then merged on the same pull request, and the merge step can see the pull request's status and who authored and approved it.
When a pull request is reviewed, a reviewer may not approve their own pull request.
That self-approval ban is set aside when the number of changed lines crosses the threshold requiring extra scrutiny, and it holds when the changed lines stay below that threshold.
The review step takes effect only when the person reviewing holds the designated role, and it does not take effect when they do not hold that role.
When a pull request is merged, the author of the pull request may not be the one who merges it.
A maintainer must not merge a pull request that they themselves authored.
A run through the workflow by a reviewer that trips none of these prohibitions must be able to succeed.
