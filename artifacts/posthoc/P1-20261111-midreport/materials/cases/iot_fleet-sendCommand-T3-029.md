# iot_fleet-sendCommand-T3-029

POST-HOC case audit. All four discordant cases are included; no case was resampled or repaired.

Pair category: **refine_only**.

## Required input excerpts

Line numbers refer to the original requirements/schema strings, not a rewritten specification.

```text
L5: The resources are devices, telemetry, and commands. Every device records its owner, site group, firmware tags, maintenance mode, and status.
L7: Each request carries its source IP address, current time, and maintenance window.
L9: An operator, technician, or fleet admin may send a command only when the request falls within a permitted maintenance window.
L11: Outside a permitted maintenance window, an operator, technician, or fleet admin must not send a command.
L13: An operator, technician, or fleet admin may send a command to an active device.
L17: An operator, technician, or fleet admin who owns a device may send a command to that device even when the device is provisioned or decommissioned, as long as the request is within a permitted maintenance window.
```

```text
L3: entity DeviceStatus enum ["active", "provisioned", "decommissioned"];
L13: entity MaintenanceWindow {
L14:     startTime: datetime,
L15:     endTime: datetime,
L16:     permitted: Bool,
L24:     status: DeviceStatus,
L38:         currentTime: datetime,
L39:         maintenanceWindow: MaintenanceWindow,
```

Complete inputs: [frozen validation JSONL](../../review_bundle/source/data/validation20.jsonl).

## Meta: SCHEMA_FAIL

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-meta-14/final.txt); SHA-256 `dba3aa7d63be5e2076f6bcc8510e5187151dd7d86bff37b6b202a13ea4911d61`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L19: when {
L20:     (principal.roles.contains(Role::"operator") ||
L21:      principal.roles.contains(Role::"technician") ||
L22:      principal.roles.contains(Role::"fleetAdmin")) &&
L23:     !(context.maintenanceWindow.permitted &&
L24:       context.currentTime.greaterThanOrEqual(context.maintenanceWindow.startTime) &&
L25:       context.currentTime.lessThanOrEqual(context.maintenanceWindow.endTime))
L26: };
```

Original validator return code: `3`. [Complete original log](../../review_bundle/raw/verifier/9721148253c1ccf026f8986e5a739f8bc3ab78d1b21e196ef6e9c202d654b722/validate.json).

```text
  × policy set validation failed
  ╰─▶ for policy `policy1`, unexpected type: expected decimal but saw datetime
    ╭─[25:43]
 24 │       context.currentTime.greaterThanOrEqual(context.maintenanceWindow.startTime) &&
 25 │       context.currentTime.lessThanOrEqual(context.maintenanceWindow.endTime))
    ·                                           ─────────────────────────────────
 26 │ };
    ╰────
```

Semantic checks were **not run** after the failed schema/type gate. Their outcome is unknown.

## Refine: PASS

Original final response: [raw JSON](../../review_bundle/raw/model/E4-20261110-validation-refine-14/final.txt); SHA-256 `e3bf0e78aa39a455d85f60e5289506846090cedd6209a5f9dbf6150c5ada8af8`.

Key policy lines (JSON string decoded for display only; no changes):

```text
L6: when {
L7:     (
L8:         principal.roles.contains(Role::"operator") ||
L9:         principal.roles.contains(Role::"technician") ||
L10:         principal.roles.contains(Role::"fleetAdmin")
L11:     ) &&
L12:     context.maintenanceWindow.permitted &&
L13:     context.currentTime >= context.maintenanceWindow.startTime &&
L14:     context.currentTime <= context.maintenanceWindow.endTime &&
L15:     (
L16:         resource.targetDevice.status == DeviceStatus::"active" ||
L17:         (
L18:             resource.targetDevice.owner == principal &&
L19:             (
L20:                 resource.targetDevice.status == DeviceStatus::"provisioned" ||
L21:                 resource.targetDevice.status == DeviceStatus::"decommissioned"
L22:             )
L23:         )
L24:     )
L25: };
L26: 
L27: forbid (
L33:     (
L34:         principal.roles.contains(Role::"operator") ||
L35:         principal.roles.contains(Role::"technician") ||
L36:         principal.roles.contains(Role::"fleetAdmin")
L37:     ) &&
L38:     !(
L39:         context.maintenanceWindow.permitted &&
L40:         context.currentTime >= context.maintenanceWindow.startTime &&
L41:         context.currentTime <= context.maintenanceWindow.endTime
L42:     )
L43: };
L44: 
```

Original validator return code: `0`. [Complete original log](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/validate.json).

```text
  ☞ policy set validation passed
  ╰─▶ no errors or warnings
```

- `dual_operator_technician_can_send_command_in_window_to_active_device` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-00.json).
- `send_command_roles_window_active_or_owned_in_window_ceiling` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-01.json).
- `device_owner_roles_can_send_command_in_window_to_non_active_device` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-02.json).
- `send_command_status_owner_window_union_ceiling` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-03.json).
- `roles_can_send_command_in_window_to_active_device` (floor): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-04.json).
- `p0009_send_command_active_device_union_ceiling` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-05.json).
- `non_owner_roles_cannot_send_to_provisioned_or_decommissioned_device` (implies): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-06.json).
- `operator_send_command_non_prohibited_request_liveness` (liveness-overlap): **PASS**. [Raw solver output](../../review_bundle/raw/verifier/29d7af378677dc829d271a0face462b124b70f27f366d432da8d36463b555810/check-07.json).

## Supported explanation

Meta uses greaterThanOrEqual and lessThanOrEqual on datetime fields in the maintenance-window veto. The validator reports expected decimal but saw datetime and exits with code 3. Refine uses >= and <= for the window and passes eight recorded checks covering active devices, owned non-active devices, non-owner restrictions, and liveness.

## Unsupported conclusions

The logs do not determine whether a repaired Meta policy would satisfy the device-status exceptions. No repair or counterfactual policy generation was performed. This is another observed type error, not an independent harness construction replicate.

Both results retain their original contribution to the primary 20-scenario denominator. This case audit does not define a replacement metric.
