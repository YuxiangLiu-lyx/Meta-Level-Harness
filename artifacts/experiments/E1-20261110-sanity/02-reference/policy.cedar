permit (
    principal is User,
    action == Action::"preparePayrollRun",
    resource is PayrollRun
)
when {
    principal.roles.contains("payroll_admin")
};

permit (
    principal is User,
    action == Action::"approveLeaveRequest",
    resource is LeaveRequest
)
when {
    principal.roles.contains("manager")
};

permit (
    principal is User,
    action == Action::"viewEmployeeRecord",
    resource is EmployeeRecord
)
when {
    (principal.roles.contains("manager") || principal.roles.contains("hr_specialist")) &&
    (context.onCorporateVpn || principal.clearance >= resource.piiLevel)
};