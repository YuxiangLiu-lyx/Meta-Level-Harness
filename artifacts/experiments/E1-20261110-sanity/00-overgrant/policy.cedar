forbid (principal, action == Action::"modifyCloudResource", resource)
when {
    principal is User &&
    resource is CloudResource &&
    false &&
    (
        Role::"owner" in principal.roles ||
        Role::"developer" in principal.roles ||
        Role::"operator" in principal.roles
    )
};

forbid (principal, action == Action::"modifyCloudResource", resource)
when {
    principal is User &&
    resource is CloudResource &&
    (
        Role::"owner" in principal.roles ||
        Role::"developer" in principal.roles ||
        Role::"operator" in principal.roles
    ) &&
    resource.environment == Environment::"production" &&
    resource.promoted == false
}
unless {
    principal.orgMembership in resource.orgUnit
};

permit (principal, action == Action::"modifyCloudResource", resource)
when {
    principal is User &&
    resource is CloudResource &&
    Role::"owner" in principal.roles &&
    principal == resource.owner
};

permit (principal, action == Action::"modifyCloudResource", resource)
when {
    principal is User &&
    resource is CloudResource &&
    (
        Role::"owner" in principal.roles ||
        Role::"developer" in principal.roles ||
        Role::"operator" in principal.roles
    ) &&
    (
        resource.environment == Environment::"nonProduction" ||
        (
            resource.environment == Environment::"production" &&
            resource.promoted == true
        )
    )
};