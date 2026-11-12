permit (principal is Pathologist, action == Action::"releaseLabResult", resource is LabResult)
when { !(resource has verifiedBy && resource.verifiedBy.user == principal.user) };