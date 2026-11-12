permit (principal is User, action == Action::"cloneRepository", resource is Repository)
when {
    (principal.roles.contains(Role::"developer") &&
  principal.clearanceLevel == ClearanceLevel::"confidential" &&
  resource.lifecycleStatus == RepositoryLifecycleStatus::"active" &&
  resource.topicTags.contains("regulated-data") &&
  resource.sensitivityClassification == ClearanceLevel::"confidential")
    && !((principal.roles.contains(Role::"developer") || principal.roles.contains(Role::"reviewer") || principal.roles.contains(Role::"maintainer") || principal.roles.contains(Role::"securityLead")) && ((principal.clearanceLevel == ClearanceLevel::"public" && (resource.sensitivityClassification == ClearanceLevel::"internal" || resource.sensitivityClassification == ClearanceLevel::"confidential" || resource.sensitivityClassification == ClearanceLevel::"restricted")) || (principal.clearanceLevel == ClearanceLevel::"internal" && (resource.sensitivityClassification == ClearanceLevel::"confidential" || resource.sensitivityClassification == ClearanceLevel::"restricted")) || (principal.clearanceLevel == ClearanceLevel::"confidential" && resource.sensitivityClassification == ClearanceLevel::"restricted")))
    && !(resource.lifecycleStatus == RepositoryLifecycleStatus::"archived")
    && !(resource.topicTags.contains("regulated-data") && ((principal.clearanceLevel == ClearanceLevel::"public" && (resource.sensitivityClassification == ClearanceLevel::"internal" || resource.sensitivityClassification == ClearanceLevel::"confidential" || resource.sensitivityClassification == ClearanceLevel::"restricted")) || (principal.clearanceLevel == ClearanceLevel::"internal" && (resource.sensitivityClassification == ClearanceLevel::"confidential" || resource.sensitivityClassification == ClearanceLevel::"restricted")) || (principal.clearanceLevel == ClearanceLevel::"confidential" && resource.sensitivityClassification == ClearanceLevel::"restricted")))
    && !(!resource.topicTags.contains("regulated-data"))
};