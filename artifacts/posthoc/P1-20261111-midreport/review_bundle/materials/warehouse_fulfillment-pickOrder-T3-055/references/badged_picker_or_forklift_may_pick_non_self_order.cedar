permit (principal, action == Action::"pickOrder", resource) when {
    (resource is Order && context.hasBadgedInOnSiteForShift && ((principal is Picker && resource.requestedBy != principal.user) || (principal is ForkliftOperator && resource.requestedBy != principal.user)))
    && !(!context.hasBadgedInOnSiteForShift)
};