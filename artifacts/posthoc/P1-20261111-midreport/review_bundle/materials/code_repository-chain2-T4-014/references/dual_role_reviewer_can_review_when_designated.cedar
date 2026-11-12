permit (principal is User, action == Action::"reviewPullRequest", resource is PullRequest)
when {
    (Role::"Developer" in principal.roles &&
    Role::"Reviewer" in principal.roles &&
    resource.designatedRole == Role::"Reviewer" &&
    resource.designatedRole in principal.roles &&
    principal != resource.author)
    && !(principal == resource.author)
};