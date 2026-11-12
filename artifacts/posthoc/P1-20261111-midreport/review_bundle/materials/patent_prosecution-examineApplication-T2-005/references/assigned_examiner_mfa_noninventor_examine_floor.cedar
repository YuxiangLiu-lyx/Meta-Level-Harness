permit (principal, action == Action::"examinePatentApplication", resource) when {
    (principal is Person && resource is PatentApplication && Role::"examiner" in principal.roles && resource.assignedExaminer == principal && resource.inventor != principal && context.mfaUsed)
    && !(resource.inventor == principal)
};