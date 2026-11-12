# Number Port Authorization — Separation of Duty with a High-Value Exception

## Natural-Language Scenario

This system manages number portability authorization and cutover for a telephone carrier.

The people involved are porting specialists, porting supervisors, fraud reviewers, line technicians, and auditors. One person may hold both the porting specialist and fraud reviewer roles at the same time, and one person may hold both the line technician and porting specialist roles at the same time.

The resources are port requests and port completions. Every port request records who initiated it, who authorized it, the technician assigned to it, the account numbers being ported, the size of the number block, the gaining carrier code, the port type, the subscriber's region, its status, and the time it was requested. Every port completion records the request it belongs to, who completed the cutover, and the time the numbers were ported.

Each request carries the current time, whether it comes from the carrier's own operations network, whether a port-freeze override has been declared, and whether a regulator escalation is in effect.

The porting specialist who submitted a port request may not authorize that same request, to guard against a person slamming a port through on their own.

This bar does not apply when the account numbers being ported include a flagged or high-value line, in which case the specialist who submitted the request may authorize it.

When the account numbers include no flagged or high-value line, neither a porting specialist nor a porting supervisor may authorize a port request that they themselves submitted.

A request by a porting specialist who did not submit the port request to authorize it, tripping no prohibition above, must be able to succeed.
