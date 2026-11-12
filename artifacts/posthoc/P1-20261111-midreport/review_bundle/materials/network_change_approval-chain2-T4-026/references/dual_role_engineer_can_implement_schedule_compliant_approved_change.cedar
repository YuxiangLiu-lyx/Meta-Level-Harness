permit (principal is User, action == Action::"implementChange", resource is ChangeRequest) when {
    (principal.isNetworkEngineer && principal.isSeniorEngineer && resource.currentStatus == ChangeStatus::"Approved" && (resource.isEmergency || context.currentTime >= resource.maintenanceWindowStart))
    && !((principal.isNetworkEngineer || principal.isSeniorEngineer) && resource.currentStatus == ChangeStatus::"NotApproved")
    && !(!resource.isEmergency && context.currentTime < resource.maintenanceWindowStart)
    && !(resource.currentStatus == ChangeStatus::"NotApproved")
};