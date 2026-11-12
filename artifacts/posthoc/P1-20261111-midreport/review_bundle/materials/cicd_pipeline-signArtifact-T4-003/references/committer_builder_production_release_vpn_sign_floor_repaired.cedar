permit (principal is User, action == Action::"signArtifact", resource is Artifact) when {
    (principal.roles.contains(Role::"committer") && resource.builtBy == principal && resource.buildTags.contains("production-release") && resource.buildSucceeded == true && resource.status == "built" && context.sourceNetworkIsCorporateVpn == true)
    && !(resource.builtBy != principal)
};