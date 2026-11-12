permit (principal is User, action == Action::"authorizeSwitchingOrder", resource is SwitchingOrder)
when { !(!context.fromControlSystemNetwork) };