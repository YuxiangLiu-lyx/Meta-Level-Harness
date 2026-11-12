permit (principal is User, action == Action::"approveInvoice", resource is Invoice)
when { !(resource.status != InvoiceStatus::"submitted") };