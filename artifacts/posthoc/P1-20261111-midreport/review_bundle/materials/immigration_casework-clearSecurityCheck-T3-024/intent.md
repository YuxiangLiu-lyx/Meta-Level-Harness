# Immigration Case Adjudication

## Natural-Language Scenario

The system manages immigration case adjudication and security-check clearance.

The people involved are adjudication officers, supervisory officers, background investigators, and records clerks. One person may hold both the adjudication officer and background investigator roles, and one person may hold both the supervisory officer and adjudication officer roles.

The resources are cases, security checks, and applicant records. Every case records its applicant, assigned officer, case team, field office, and status.

Every security check records its case, investigator, and status.

Every applicant record records its applicant, assigned officer, need-to-know team, data sensitivity, and status.

Each requester carries their clearance and recused cases.

Each request carries whether it is on the government network, the current time, and whether supervisor approval is present.

A background investigator may clear a security check only while it is pending.

A supervisory officer may clear a security check even when it is not pending.

A background investigator and a supervisory officer may clear a security check only during the permitted time window.

A background investigator and a supervisory officer must not clear a security check outside the permitted time window.

A request by a background investigator to clear a pending security check during the permitted time window, tripping no prohibition above, must be able to succeed.