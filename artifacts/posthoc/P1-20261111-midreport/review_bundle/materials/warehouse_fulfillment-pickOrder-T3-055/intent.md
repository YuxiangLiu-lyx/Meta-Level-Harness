# Warehouse Zone Access and Order Picking

## Natural-Language Scenario

The system manages warehouse zone access and order picking.

The people involved are pickers, forklift operators, zone supervisors, warehouse managers, and security officers. One person may hold both the picker and the forklift operator role at the same time.

The resources are orders, which record who requested them, the picker, items, item count, pick list code, status, destination zone, and release time, and zones, which record zone code, sensitivity, zone group, whether the zone is locked, and operational status.

Each request carries the current time, whether the requester has badged in on-site for the shift, and whether an emergency has been declared.

A picker or forklift operator may pick an order only after they have badged in on-site for the shift.

A picker or forklift operator who has not badged in on-site for the shift may not pick an order.

Neither a picker nor a forklift operator may pick an order they requested themselves when the order's line-item count does not cross the bulk-pick threshold.

When the order's line-item count crosses the bulk-pick threshold, the picker or forklift operator who requested the order may pick it themselves.

A request by a picker to pick an order that does not trip any prohibition above must be able to succeed.