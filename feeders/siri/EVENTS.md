# SIRI event reference

[📘 **Overview**](README.md) · [🐳 **Container images**](CONTAINER.md)

This document defines the CloudEvents contract emitted by the generic `siri` feeder.

## At a glance

- **Event types:** `org.siri.Operator`, `org.siri.VehiclePosition`
- **Identity:** operators use `{operator_ref}`; telemetry uses `{operator_ref}/{vehicle_ref}`
- **Kafka topic:** `siri`
- **MQTT topics:** `transit/siri/{operator_ref}/info`, `transit/siri/{operator_ref}/{vehicle_ref}/position`
- **AMQP node:** `siri`
- **CloudEvents source:** the sanitized upstream request URL used for the current provider request

## Operator

- **CloudEvents type:** `org.siri.Operator`
- **Role:** reference data
- **Identity:** `{operator_ref}`

Payload:

- `operator_ref` — operator identifier from `MonitoredVehicleJourney/OperatorRef`

Example:

```json
{
  "operator_ref": "A2BR"
}
```

## VehiclePosition

- **CloudEvents type:** `org.siri.VehiclePosition`
- **Role:** telemetry
- **Identity:** `{operator_ref}/{vehicle_ref}`

Payload:

- `operator_ref` — stable operator identifier from `OperatorRef`
- `vehicle_ref` — provider-scoped vehicle identifier from `VehicleRef`
- `line_ref` — route or service identifier
- `direction_ref` — direction label such as `inbound` or `outbound`
- `published_line_name` — public-facing line label
- `origin_ref`, `origin_name` — origin stop reference and display name
- `destination_ref`, `destination_name` — destination stop reference and display name
- `longitude`, `latitude` — WGS84 coordinates
- `bearing` — heading in degrees clockwise from north
- `recorded_at_time` — activity timestamp from `RecordedAtTime`
- `valid_until_time` — stale-after timestamp from `ValidUntilTime`
- `block_ref` — operational block identifier
- `vehicle_journey_ref` — vehicle journey identifier
- `origin_aimed_departure_time` — scheduled origin departure time
- `data_frame_ref` — framed service-day identifier
- `dated_vehicle_journey_ref` — framed dated journey identifier
- `item_identifier` — upstream `ItemIdentifier` used for dedupe

Example:

```json
{
  "operator_ref": "A2BR",
  "vehicle_ref": "3312",
  "line_ref": "T12",
  "direction_ref": "outbound",
  "published_line_name": "T12",
  "origin_ref": "0500SLONN009",
  "origin_name": "Longstanton Park-and-Ride",
  "destination_ref": "0500ESUTT002",
  "destination_name": "Windmill Lane",
  "longitude": 0.054376,
  "latitude": 52.29166,
  "bearing": 73,
  "recorded_at_time": "2026-06-04T05:56:35+00:00",
  "valid_until_time": "2026-06-04T06:02:14.931+00:00",
  "block_ref": "T12",
  "vehicle_journey_ref": "0700",
  "origin_aimed_departure_time": "2026-06-04T06:00:00+00:00",
  "data_frame_ref": "2026-06-04",
  "dated_vehicle_journey_ref": "VJ_1",
  "item_identifier": "9e8f75df-84fb-460d-9aa0-6245bd881a15"
}
```

## Transport notes

- **Kafka** uses structured JSON CloudEvents on topic `siri`.
- **MQTT** uses binary-mode CloudEvents on `transit/siri/...`; operator records are retained QoS 1 and telemetry is non-retained QoS 0.
- **AMQP** uses binary-mode CloudEvents on node `siri`; the AMQP `subject` mirrors the CloudEvents `subject`.
