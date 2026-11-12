permit (principal is User, action == Action::"reviewPullRequest", resource is PullRequest)
when { !(principal == resource.author) };