# Work-Order QA Sign-Off

## Natural-Language Scenario

The system manages quality sign-off for manufacturing work orders before production release.

The people involved are operators, inspectors, quality managers, production supervisors, and auditors. One person may hold both the operator and inspector roles, and one person may hold both the inspector and quality manager roles.

The resources are work orders and production releases. Every work order records its operator, inspector, part code, defect count, hold flag, status, station, and creation time.

Each request carries the current time, whether it comes from the plant network, and whether a deviation has been authorized.

An operator may create a work order and start work on it.

An inspector or quality manager may sign off a work order only while it is in progress.

An inspector and a quality manager must not sign off a work order that is not in progress.

An inspector or quality manager may sign off a work order when the part code matches or has a controlled-part prefix.

An inspector and a quality manager must not sign off a work order when the part code neither matches nor has a controlled-part prefix.

An inspector or quality manager may sign off a work order when the recorded defect count is at or below the acceptance threshold.

An inspector and a quality manager must not sign off a work order when the recorded defect count is above the acceptance threshold.

A production supervisor may release a signed-off work order to production.

An auditor may view the quality log.

A request by an inspector to sign off an in-progress work order with an acceptable part code and a defect count at or below the acceptance threshold must be able to succeed.