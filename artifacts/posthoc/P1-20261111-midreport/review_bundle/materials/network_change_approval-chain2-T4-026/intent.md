# Network Change Approval then Implementation — Cost-Triggered CAB Sign-Off and Emergency Scheduling

## Natural-Language Scenario

The system manages network change control approval and maintenance-window implementation at a telecommunications carrier.

The people involved are network engineers, senior engineers, change managers, CAB approvers, and auditors. One person may hold both the network engineer and the senior engineer role at the same time.

The resources are change requests and implementation records. Every change request records the engineer who requested it, the engineer who implemented it, the person who approved it, its assessed change risk, its affected-node count, its rollback-step count, its estimated cost, its change code, whether it is an emergency change, its change category, its current status, and its maintenance-window start. Every implementation record records the change it belongs to, who carried it out, and when it was carried out.

Each request carries the current time, whether it comes from the management network, whether a change-freeze waiver has been granted, and whether a major incident has been declared.

In this workflow a change is first approved and then implemented, and the implementation step can see the change's status, who approved it, and who implemented it as recorded by the approval step.

A change manager or CAB approver may approve a change only when their granted change-authority level is at least as high as the change's assessed risk, and a change whose risk exceeds the approver's authority may not be approved by that person.

This authority requirement is set aside when the change's estimated cost crosses the money threshold that requires CAB sign-off, in which case a CAB approver must sign off instead, and when the cost stays below that threshold the standard authority requirement applies.

A change may be implemented only after it has been approved, and a change that has not yet been approved may not be implemented.

The standard scheduling requirement is relaxed when the change is flagged as an emergency, allowing implementation ahead of the normal window, and when it is not flagged as an emergency the standard schedule applies.

Neither a network engineer nor a senior engineer may implement a change before it has been approved.

A run through the workflow by a change manager who approves a low-cost change within their authority and then has a network engineer implement it must be able to succeed.
