permit (principal is User, action == Action::"cloneRepository", resource is Repository)
when {
  principal.roles.contains(Role::"developer") &&
  principal.clearanceLevel == ClearanceLevel::"confidential" &&
  resource.lifecycleStatus == RepositoryLifecycleStatus::"active" &&
  resource.topicTags.contains("regulated-data") &&
  resource.sensitivityClassification == ClearanceLevel::"confidential"
};