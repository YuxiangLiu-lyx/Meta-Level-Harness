permit (
    principal is Person,
    action == Action::"examinePatentApplication",
    resource is PatentApplication
)
when {
    Role::"examiner" in principal.roles &&
    resource.assignedExaminer == principal &&
    true &&
    context.mfaUsed == true
};