permit (principal is User, action == Action::"authorizeSwitchingOrder", resource is SwitchingOrder) when {
    (principal.roles.contains(Role::"Planner") && principal.roles.contains(Role::"ShiftSupervisor") && resource.status == "planned" && context.lockoutTagoutVerified)
    && !(!context.fromControlSystemNetwork)
    && !(!context.lockoutTagoutVerified)
};