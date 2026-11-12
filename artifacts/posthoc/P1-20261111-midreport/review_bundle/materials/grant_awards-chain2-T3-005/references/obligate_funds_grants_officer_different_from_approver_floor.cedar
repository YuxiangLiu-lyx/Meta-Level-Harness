permit (principal, action == Action::"obligateFunds", resource) when {
    (principal is User && resource is Award && principal.roles.contains(Role::"GrantsOfficer") && resource has approvedBy && resource.approvedBy != principal)
    && !(resource has approvedBy && resource.approvedBy == principal)
};