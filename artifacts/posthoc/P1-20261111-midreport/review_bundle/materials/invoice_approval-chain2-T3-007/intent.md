# Invoice Approval and Payment, With an Emergency Override of the Approver-Payer Split

## Natural-Language Scenario

This is the access-control document for the invoice approval and payment system.
The people involved are clerks, approvers, finance managers, and auditors, and one person may be both a clerk and an approver at the same time.
The resources are invoices, each recording their creator, approver, amount, surcharge, line-item count, status, cost center, and when they were submitted, and payments, each recording their invoice, issuer, and amount.
Each request carries the current time, whether the request is on the corporate network, and whether an emergency has been declared.
In this workflow the same invoice is first approved and then a payment is issued against it, and the payment step can see the invoice's status and who approved it as recorded by the approval step.
When an approver or a finance manager approves an invoice, it may be approved only after it has been submitted.
When a finance manager issues a payment, the person who approved the invoice may not be the one who issues its payment.
This approver-payer split is overridden when an emergency has been declared, in which case a finance manager may issue payment even on an invoice they themselves approved.
When no emergency has been declared, the person who approved an invoice may not issue its payment.
If the two rules on payment disagree, the declared emergency wins and the finance manager may issue the payment.
An approver or a finance manager must not approve an invoice that has not been submitted.
A finance manager must not issue payment on an invoice they themselves approved unless an emergency has been declared.
A run through the workflow by an approver that trips none of the prohibitions above must be able to succeed.
