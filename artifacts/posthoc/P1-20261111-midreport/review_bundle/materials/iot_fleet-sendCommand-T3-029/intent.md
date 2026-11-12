# IoT Device Commanding

## Natural-Language Scenario

The system manages command delivery for an IoT and operational-technology device fleet.

The people involved are operators, technicians, fleet admins, and service accounts. One person may hold both the operator and technician role at the same time.

The resources are devices, telemetry, and commands. Every device records its owner, site group, firmware tags, maintenance mode, and status.

Each request carries its source IP address, current time, and maintenance window.

An operator, technician, or fleet admin may send a command only when the request falls within a permitted maintenance window.

Outside a permitted maintenance window, an operator, technician, or fleet admin must not send a command.

An operator, technician, or fleet admin may send a command to an active device.

An operator, technician, or fleet admin who does not own a device must not send a command to it when the device is provisioned or decommissioned.

An operator, technician, or fleet admin who owns a device may send a command to that device even when the device is provisioned or decommissioned, as long as the request is within a permitted maintenance window.

A request by an operator to send a command that does not trip any prohibition above must be able to succeed.