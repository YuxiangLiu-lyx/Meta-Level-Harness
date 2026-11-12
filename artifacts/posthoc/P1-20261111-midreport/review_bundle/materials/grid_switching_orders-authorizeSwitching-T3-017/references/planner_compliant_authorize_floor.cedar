permit (principal is User, action == Action::"authorizeSwitchingOrder", resource is SwitchingOrder) when {
    (principal.roles.contains(Role::"Planner") && resource.status == "planned" && context.lockoutTagoutVerified && context.fromControlSystemNetwork && !context.voltageAboveShiftSupervisorThreshold)
    && !(!context.fromControlSystemNetwork)
    && !(!context.lockoutTagoutVerified)
};