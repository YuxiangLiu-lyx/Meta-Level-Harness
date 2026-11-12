permit (principal is Person, action == Action::"viewMedicalRecord", resource is MedicalRecord) when {
    (principal.roles.contains(Role::"pharmacist") && (principal.roles.contains(Role::"attendingPhysician") || principal.roles.contains(Role::"resident")) && principal.clearedLevel >= resource.sensitivity)
    && !((principal.roles.contains(Role::"attendingPhysician") || principal.roles.contains(Role::"resident") || principal.roles.contains(Role::"nurse")) && resource.isSealed && resource.sensitivity > principal.clearedLevel)
};