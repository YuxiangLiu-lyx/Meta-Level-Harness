permit (principal is User, action == Action::"obligateFunds", resource is Award)
when { !(resource has approvedBy && resource.approvedBy == principal) };