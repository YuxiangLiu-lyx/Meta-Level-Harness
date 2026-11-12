permit (principal, action == Action::"authorizePortRequest", resource) when {
    (principal is User && resource is PortRequest && principal.isPortingSpecialist && resource.initiatedBy != principal)
    && !((principal.isPortingSpecialist || principal.isPortingSupervisor) && resource.initiatedBy == principal && !resource.includesFlaggedOrHighValueLine)
};