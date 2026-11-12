permit (principal is User, action == Action::"mergePullRequest", resource is PullRequest)
when {
    (Role::"Maintainer" in principal.roles &&
    principal != resource.author &&
    resource.approvalCount > 0)
    && !(principal == resource.author)
};