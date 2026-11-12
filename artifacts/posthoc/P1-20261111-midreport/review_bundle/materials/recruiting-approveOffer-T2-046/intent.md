# Recruiting Applicant Tracking

## Natural-Language Scenario

The system manages job applications, interview feedback, and offers for recruiting.

The people involved are recruiters, hiring managers, interviewers, and coordinators. One person may hold recruiter and interviewer roles together, or recruiter and hiring manager roles together.

The resources are applications, interview feedback, and offers, with each application recording its candidate, referrer, hiring team, req code, PII sensitivity, and status, each interview feedback record recording its application, interviewer, candidate, and status, and each offer recording its application, extender, compensation, signing bonus, and status.

Each person making a request carries their PII clearance.

Each request carries whether it is from the corporate network, the current time, and whether executive approval is present.

A hiring manager may approve an offer only while the offer is drafted, unless the request falls within a permitted window.

When the request falls within a permitted window, the hiring manager may approve an offer that is not drafted.

A hiring manager must not approve an offer that is not drafted when the request is outside the permitted window.

A request by a hiring manager to approve an offer that does not trip any prohibition above must be able to succeed.