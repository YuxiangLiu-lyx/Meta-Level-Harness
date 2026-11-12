permit (principal, action == Action::"launchCampaign", resource) when {
    (principal is User && resource is Campaign && resource.advertiser == principal && principal.roles.contains(Role::"Advertiser") && resource.status == CampaignStatus::"BudgetApproved" && resource.riskLabels.contains(context.requiredRiskLabel))
    && !(principal is User && resource is Campaign && (principal.roles.contains(Role::"AccountManager") || principal.roles.contains(Role::"CampaignDirector")) && resource.advertiser != principal)
    && !(principal is User && resource is Campaign && resource.status != CampaignStatus::"BudgetApproved")
    && !(principal is User && resource is Campaign && !resource.riskLabels.contains(context.requiredRiskLabel))
};