permit (principal is Picker, action == Action::"pickOrder", resource is Order)
when { !(!context.hasBadgedInOnSiteForShift) };