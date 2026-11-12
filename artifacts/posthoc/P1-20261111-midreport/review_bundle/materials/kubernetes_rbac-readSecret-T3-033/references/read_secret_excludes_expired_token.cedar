permit (principal is User, action == Action::"readNamespaceSecret", resource is NamespaceSecret)
when { !(context.serviceAccountToken.expiresAt <= context.currentTime) };