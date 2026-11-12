permit (principal is Requester, action == Action::"readTelemetry", resource is TelemetryRecord) when {
    ((principal.roles.contains(Role::"Operator") || principal.roles.contains(Role::"FleetAdmin")) && principal.groups.contains(resource.device.siteGroup) && resource.device.owner == principal)
    && !((principal.roles.contains(Role::"Operator") || principal.roles.contains(Role::"FleetAdmin")) && !principal.groups.contains(resource.device.siteGroup))
    && !((principal.roles.contains(Role::"Operator") || principal.roles.contains(Role::"FleetAdmin")) && resource.device.owner != principal && principal.clearance < resource.sensitivity)
};