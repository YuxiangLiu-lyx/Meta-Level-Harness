permit (principal is Person, action == Action::"signOffWorkOrder", resource is WorkOrder) when {
    (principal.roles.contains(Role::"inspector") && resource.status == WorkOrderStatus::"inProgress" && resource.partCodeAcceptable && resource.defectCount <= resource.acceptanceThreshold)
    && !((principal.roles.contains(Role::"inspector") || principal.roles.contains(Role::"qualityManager")) && !(resource.status == WorkOrderStatus::"inProgress"))
    && !((principal.roles.contains(Role::"inspector") || principal.roles.contains(Role::"qualityManager")) && !(context.partCodeMatches || context.hasControlledPartPrefix))
    && !((principal.roles.contains(Role::"inspector") || principal.roles.contains(Role::"qualityManager")) && resource.defectCount > resource.acceptanceThreshold)
};