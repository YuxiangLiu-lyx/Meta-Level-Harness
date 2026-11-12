permit (principal is OrderingProvider, action == Action::"releaseLabResult", resource is LabResult) when {
    (resource.isVerified == true && principal == resource.orderingProvider && resource.sensitivityLevel == "restricted" && resource.criticalValueFlag == true && (!(resource has verifiedBy) || (resource has verifiedBy && resource.verifiedBy.user != principal.user)))
    && !(resource has verifiedBy && resource.verifiedBy.user == principal.user)
    && !(resource.sensitivityLevel == "restricted" && resource.criticalValueFlag == false)
};