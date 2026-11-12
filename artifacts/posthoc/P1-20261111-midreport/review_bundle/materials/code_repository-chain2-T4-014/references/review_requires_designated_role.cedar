permit (principal is User, action == Action::"reviewPullRequest", resource is PullRequest)
when {
    resource.designatedRole in principal.roles
};