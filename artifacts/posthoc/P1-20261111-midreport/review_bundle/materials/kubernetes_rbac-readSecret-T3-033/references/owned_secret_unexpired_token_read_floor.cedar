permit (principal, action == Action::"readNamespaceSecret", resource is NamespaceSecret) when {
    (context.serviceAccountToken.expiresAt > context.currentTime && (((principal is User) && (resource has ownerUser) && resource.ownerUser == principal && principal.clearance >= resource.sensitivity) || ((principal is ServiceAccount) && (resource has ownerServiceAccount) && resource.ownerServiceAccount == principal && principal.clearance >= resource.sensitivity)))
    && !(((principal is User) && (!(resource has ownerUser) || ((resource has ownerUser) && resource.ownerUser != principal))) || ((principal is ServiceAccount) && (!(resource has ownerServiceAccount) || ((resource has ownerServiceAccount) && resource.ownerServiceAccount != principal))))
    && !(context.serviceAccountToken.expiresAt <= context.currentTime)
    && !(context.serviceAccountToken.expiresAt <= context.currentTime)
};