permit (principal, action, resource) when {
    (principal is User && resource is Invoice && action == Action::"approveInvoice" && (principal.roles.contains(Role::"approver") || principal.roles.contains(Role::"financeManager")) && resource.status == InvoiceStatus::"submitted")
    && !(resource.status != InvoiceStatus::"submitted")
};