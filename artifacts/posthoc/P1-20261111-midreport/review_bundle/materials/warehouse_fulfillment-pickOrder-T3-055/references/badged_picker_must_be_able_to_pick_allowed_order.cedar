permit (principal, action == Action::"pickOrder", resource) when {
    (resource is Order && principal is Picker && context.hasBadgedInOnSiteForShift && (resource.requestedBy != principal.user || resource.crossesBulkPickThreshold))
    && !(!context.hasBadgedInOnSiteForShift)
};