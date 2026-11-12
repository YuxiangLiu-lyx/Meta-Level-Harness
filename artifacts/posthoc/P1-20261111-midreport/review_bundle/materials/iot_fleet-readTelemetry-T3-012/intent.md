# IoT Device Fleet Telemetry Access

## Natural-Language Scenario

The system manages telemetry access for an IoT and operational technology device fleet.

The people involved are operators, technicians, fleet admins, and service accounts. One person may hold both the operator and the technician role at the same time.

The resources are devices, telemetry, and commands. Every device records its owner, site group, firmware tags, maintenance mode, and status, and every telemetry record records its device and sensitivity.

Each requester carries their clearance and the groups they belong to.

An operator or fleet admin may read telemetry only when they belong under the device's site group.

An operator or fleet admin outside the device's site group must not read telemetry for that device.

An operator or fleet admin who does not own the device may read its telemetry only when their clearance is at least as high as the telemetry sensitivity.

An operator or fleet admin who owns the device may read its telemetry without meeting the telemetry sensitivity level, as long as they belong under the device's site group.

Neither an operator nor a fleet admin may read telemetry for a device outside their site group.

A request by an operator to read telemetry that does not trip any prohibition above must be able to succeed.