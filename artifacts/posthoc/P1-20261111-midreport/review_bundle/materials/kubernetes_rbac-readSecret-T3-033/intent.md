# Kubernetes Namespace RBAC

## Natural-Language Scenario

The system manages reading namespace secrets in Kubernetes namespaces.

The people involved are deployers, maintainers, cluster operators, and service accounts. One person may hold both the deployer and maintainer role at the same time.

The resources are namespaces, workloads, namespace secrets, and service account tokens. Every namespace secret records its namespace, owner, sensitivity, and status.

Each requester carries clearance, granted scope, and group membership.

Each request carries source IP, current time, emergency change, and whether MFA was used.

A deployer, maintainer, cluster operator, or service account may read a namespace secret only when their clearance is at least as high as the secret's sensitivity.

A deployer, maintainer, cluster operator, or service account with lower clearance than the secret's sensitivity must not read that secret.

A deployer, maintainer, cluster operator, or service account may read a namespace secret they own when no other rule blocks the request.

A deployer, maintainer, cluster operator, or service account must not read a namespace secret they do not own.

A deployer, maintainer, cluster operator, or service account may read a namespace secret only when the service account token presented for the request has not expired.

A deployer, maintainer, cluster operator, or service account must not read a namespace secret using an expired service account token.

A request by a deployer to read a namespace secret that does not trip any prohibition above must be able to succeed.