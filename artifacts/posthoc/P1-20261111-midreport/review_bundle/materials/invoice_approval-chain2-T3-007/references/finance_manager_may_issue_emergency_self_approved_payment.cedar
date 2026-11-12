permit (principal, action, resource) when {
    (principal is User && resource is Payment && action == Action::"issuePayment" && principal.roles.contains(Role::"financeManager") && resource.invoice.status == InvoiceStatus::"approved" && resource.invoice has approver && resource.invoice.approver == principal && context.emergencyDeclared)
    && !(resource.invoice has approver && resource.invoice.approver == principal && !context.emergencyDeclared)
};