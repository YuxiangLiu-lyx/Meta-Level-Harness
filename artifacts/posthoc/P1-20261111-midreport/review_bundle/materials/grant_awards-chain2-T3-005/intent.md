# Grant Award Approval and Fund Obligation

## Natural-Language Scenario

This document sets out who may approve grant awards and obligate their funds in the federal grant award management system.
The people involved are reviewers, program officers, grants officers, and applicants; one person may act as both a reviewer and a program officer, and one person may act as both a program officer and a grants officer.
The resources are applications, which record their applicant, assigned reviewers, funding tier, requested amount, program code, and status; and awards, which record their application, who approved them, who obligated their funds, their amount, whether they are flagged high risk, and their status.
Each request carries the current time, whether it comes from the government network, and whether an emergency has been declared.
In this workflow an award is first approved and then its funds are obligated, and the obligation step can see the award's status, who approved it, and who obligated it.
A program officer or grants officer may approve an award only when their approval authority is at or above the application's funding tier, and when their authority falls below that tier the approval must not proceed.
The grants officer who approved an award must not obligate its funds, so the obligation must fall to a different grants officer.
Funds may be obligated only when the requester holds the designated role, and when the requester lacks that role the obligation must not proceed.
A run through the workflow by a program officer that trips none of the prohibitions above must be able to succeed.
