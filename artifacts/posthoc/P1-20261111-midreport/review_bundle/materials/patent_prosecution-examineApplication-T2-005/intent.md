# Patent Prosecution Docket

## Natural-Language Scenario

The system manages patent applications, office actions, filings, and examination work on a prosecution docket.

The people involved are patent attorneys, docket clerks, examiners, and inventors. One person may hold both the patent attorney and docket clerk roles, and one person may hold both the examiner and inventor roles.

The resources are patent applications, office actions, and filings. Every patent application records its inventor, prosecuting attorney, assigned examiner, team, confidentiality, bar date, and status.

Each requester carries their clearance.

Each request carries the current date, whether it is made on the firm network, whether there is a court order, and whether MFA was used.

An examiner may examine a patent application only when MFA was used.

An examiner who has not used MFA must not examine a patent application.

An examiner who is a named inventor on a patent application must recuse and may not examine that application.

An examiner who is not a named inventor on the application and has used MFA may examine it.

A request by an examiner to examine an application that does not trip any prohibition above must be able to succeed.