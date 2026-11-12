permit (principal, action == Action::"releaseLabResult", resource) when {
    (resource is LabResult && resource.isVerified == true && ((principal is Pathologist) || (principal is OrderingProvider && principal == resource.orderingProvider)) && (!(resource has verifiedBy) || (resource has verifiedBy && resource.verifiedBy.user != principal.user)))
    && !(resource has verifiedBy && resource.verifiedBy.user == principal.user)
    && !(resource.sensitivityLevel == "restricted" && resource.criticalValueFlag == false)
};