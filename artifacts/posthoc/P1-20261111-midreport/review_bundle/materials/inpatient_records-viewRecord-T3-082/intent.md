# Inpatient Records and Prescriptions

## Natural-Language Scenario

The system manages inpatient medical records and prescriptions.

The people involved are attending physicians, residents, nurses, and pharmacists.

One person may hold both the attending physician and pharmacist roles, or both the resident and pharmacist roles, at the same time.

The resources are medical records, prescriptions, and lab orders.

Every medical record records its patient, care team, ward, sensitivity, and status.

Every prescription records its patient, prescriber, and status.

Every lab order records its patient.

Each requester carries a cleared level and ward, and each request carries the current shift, whether an emergency has been declared, and whether multifactor authentication was used.

An attending physician, resident, or nurse may view a medical record only when the requester's cleared level is high enough for the record's sensitivity.

An attending physician, resident, or nurse whose cleared level is not high enough for the record's sensitivity must not view the medical record.

This clearance requirement applies to attending physicians, residents, and nurses when they request to view medical records.

The clearance requirement does not govern pharmacists because pharmacists are not one of the roles performing this view-record action.

The clearance requirement applies when the medical record is sealed.

When the medical record is not sealed, this sealed-record clearance requirement relaxes.

An attending physician, resident, or nurse must not view a sealed medical record whose sensitivity is above their cleared level.

A request by an attending physician to view a medical record that does not trip any prohibition above must be able to succeed.