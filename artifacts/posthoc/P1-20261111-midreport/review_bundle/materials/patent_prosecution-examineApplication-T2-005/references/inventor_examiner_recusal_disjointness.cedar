permit (principal is Person, action == Action::"examinePatentApplication", resource is PatentApplication)
when { !(resource.inventor == principal) };