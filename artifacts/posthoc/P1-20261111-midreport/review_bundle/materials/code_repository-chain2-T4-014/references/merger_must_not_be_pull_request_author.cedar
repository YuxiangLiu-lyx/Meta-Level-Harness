permit (principal is User, action == Action::"mergePullRequest", resource is PullRequest)
when { !(principal == resource.author) };