# Switching Authorization — Planned State, Lockout Verification, and Voltage Threshold

## Natural-Language Scenario

The system manages the authorization and field execution of grid switching orders.

The people involved are planners, shift supervisors, operators, control-room operators, and auditors.

One person may hold both the planner and shift-supervisor roles, and one person may hold both the operator and control-room-operator roles.

The resources are switching orders and lockout tags.

Every switching order records the planner who prepared it, the operator designated to execute it, its feeder, its voltage level, its circuit count, its status, and its scheduled start and end times.

Every lockout tag records the order it belongs to, who applied it, and its feeder.

Each request carries the current time, whether it comes from the control-system network, whether lockout-tagout has been verified, and whether an outage emergency has been declared.

A planner or shift supervisor may authorize a switching order only while it is still in the planned state, and an order that has left the planned state may not be authorized.

An order may be authorized only when lockout-tagout has been verified in the control room beforehand, and may not be authorized while that verification is still outstanding.

When the order's voltage level is above the threshold that calls for shift-supervisor authorization, only a shift supervisor may authorize it, while at or below that voltage a planner may authorize it.

A request by a planner to authorize a switching order that breaks none of the rules above must be able to succeed.
