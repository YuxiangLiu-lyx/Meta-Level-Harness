permit (principal is User, action == Action::"cloneRepository", resource is Repository)
when { !(resource.lifecycleStatus == RepositoryLifecycleStatus::"archived") };