# Clinical Lab Result Release — Verification Independence and Restricted-Sensitivity Gate

## Natural-Language Scenario

The system manages the release of laboratory test results to patient charts in a hospital clinical lab.

The people involved are medical technologists, pathologists, ordering providers, and the lab director. One person may hold both the pathologist and ordering provider roles at the same time, and one person may hold both the medical technologist and pathologist roles at the same time.

The resources are lab results and lab orders. Every lab result records its patient, its ordering provider, the technologist who verified it, its sensitivity level, whether it carries a critical-value flag, the time it was released to the patient portal, and its status. Every lab order records its patient, its ordering provider, its test code, and its status.

Each request carries the current time, whether multi-factor authentication was used, whether the requester is on the hospital network, whether this is an emergency release, and whether coverage has been authorized.

A pathologist or an ordering provider may release a lab result.

The technologist who verified a lab result must not be the same person who releases it, even when that person also holds the pathologist role.

A pathologist or an ordering provider must not release a lab result that has not yet been verified.

When a lab result's sensitivity is at a restricted level, an ordering provider must not release it, and only a pathologist may do so.

For a restricted-sensitivity result that also carries a critical-value flag, an ordering provider may release it despite the restriction.

A request by a pathologist to release a verified result that does not trip any of the restrictions above must be able to succeed.
