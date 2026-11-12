permit (principal, action == Action::"clearSecurityCheck", resource) when {
    (principal is Person && resource is SecurityCheck && (Role::"BackgroundInvestigator" in principal.roles || Role::"SupervisoryOfficer" in principal.roles) && context.currentTime >= resource.permittedWindowStart && context.currentTime <= resource.permittedWindowEnd)
    && !(context.currentTime < resource.permittedWindowStart || context.currentTime > resource.permittedWindowEnd)
    && !(Role::"BackgroundInvestigator" in principal.roles && resource.status != "pending")
};