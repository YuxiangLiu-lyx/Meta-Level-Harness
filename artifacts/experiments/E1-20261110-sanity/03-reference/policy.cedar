permit (
    principal is Person,
    action == Action::"approveWire",
    resource is WireTransfer
)
when {
    principal.authorityTier >= resource.amountTier &&
    resource.amountPlusFeeExceedsApprovalThreshold
};

permit (
    principal is Person,
    action == Action::"releaseWire",
    resource is WireTransfer
)
when {
    principal.isTreasuryOfficer &&
    resource.status == "Approved" &&
    resource has verifiedBy &&
    resource.account.allowedBeneficiaries.contains(resource.beneficiary) &&
    resource.amountExceedsMoneyThreshold
};