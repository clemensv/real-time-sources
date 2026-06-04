# UK BODS SIRI event reference

This document defines the CloudEvents contract emitted by the UK BODS SIRI feeder. For the project overview see [README.md](README.md); for the published container images and their environment-variable matrix see [CONTAINER.md](CONTAINER.md).

## At a glance

- **Event types:** `uk.gov.dft.bods.Operator`, `uk.gov.dft.bods.VehiclePosition`.
- **Transports:** Kafka, MQTT 5.0, AMQP 1.0.
- **Reference vs telemetry:** `Operator` is reference data; `VehiclePosition` is telemetry.
- **Identity:** operators use `{operator_ref}`; vehicle telemetry uses `{operator_ref}/{vehicle_ref}`.
- **CloudEvents source:** the BODS bulk AVL archive endpoint `https://data.bus-data.dft.gov.uk/avl/download/bulk_archive`.

## Quick start — how to consume

### Kafka

Subscribe to topic `uk-bods-siri`. Vehicle telemetry records use key `{operator_ref}/{vehicle_ref}`; operator references use `{operator_ref}`.

### MQTT 5.0

Subscribe to `transit/uk/dft/bods/+/info` for operator references and `transit/uk/dft/bods/+/+/position` for live vehicle telemetry.

### AMQP 1.0

Attach a receiver to node `uk-bods-siri`. CloudEvents are sent in binary mode; AMQP `subject` mirrors the CloudEvents `subject`.

## Event catalog

### Operator

CloudEvents type: `uk.gov.dft.bods.Operator`

#### What it tells you

A distinct bus operator code observed in the BODS SIRI-VM AVL bulk archive. The feeder extracts these records from the same archive that supplies telemetry so consumers can keep operator context in-stream.

#### Identity

`{operator_ref}` — the operator code from `MonitoredVehicleJourney/OperatorRef`, typically the National Operator Code (NOC).

#### Where to find it

| Transport | Location |
| --- | --- |
| Kafka | topic `uk-bods-siri`, key `{operator_ref}` |
| MQTT 5.0 | topic `transit/uk/dft/bods/{operator_ref}/info`, retain `true`, QoS `1` |
| AMQP 1.0 | node `uk-bods-siri`, message `subject` `{operator_ref}` |

#### Payload

- **`operator_ref`** (string, required): Operator code from `MonitoredVehicleJourney/OperatorRef`, typically the National Operator Code (NOC) of the bus operator publishing the AVL feed to BODS.

#### Example payload

```json
{
  "operator_ref": "A2BR"
}
```

### VehiclePosition

CloudEvents type: `uk.gov.dft.bods.VehiclePosition`

#### What it tells you

One current BODS SIRI 2.0 `VehicleActivity` record from the AVL bulk archive. Each event represents the latest monitored vehicle journey state for one physical bus at one poll cycle.

#### Identity

`{operator_ref}/{vehicle_ref}` — operator code plus operator-scoped vehicle identifier.

#### Where to find it

| Transport | Location |
| --- | --- |
| Kafka | topic `uk-bods-siri`, key `{operator_ref}/{vehicle_ref}` |
| MQTT 5.0 | topic `transit/uk/dft/bods/{operator_ref}/{vehicle_ref}/position`, retain `false`, QoS `0` |
| AMQP 1.0 | node `uk-bods-siri`, message `subject` `{operator_ref}/{vehicle_ref}` |

#### Payload

- **`operator_ref`** (string, required): Bus operator code from `MonitoredVehicleJourney/OperatorRef`.
- **`vehicle_ref`** (string, required): Operator-scoped vehicle identifier from `MonitoredVehicleJourney/VehicleRef`.
- **`line_ref`** (string or null): Route or service identifier from `MonitoredVehicleJourney/LineRef`.
- **`direction_ref`** (string or null): Direction label such as `inbound` or `outbound` from `MonitoredVehicleJourney/DirectionRef`.
- **`published_line_name`** (string or null): Public-facing line name from `MonitoredVehicleJourney/PublishedLineName`.
- **`origin_ref`** / **`origin_name`** (string or null): Origin stop code and display name from `OriginRef` / `OriginName`.
- **`destination_ref`** / **`destination_name`** (string or null): Destination stop code and display name from `DestinationRef` / `DestinationName`.
- **`longitude`** / **`latitude`** (double or null): WGS84 vehicle coordinates from `VehicleLocation`.
- **`bearing`** (integer or null): Heading in degrees clockwise from north from `Bearing`.
- **`recorded_at_time`** (string, required): Snapshot timestamp from `RecordedAtTime`.
- **`valid_until_time`** (string or null): Expiry timestamp from `ValidUntilTime`.
- **`block_ref`** (string or null): Operational block identifier from `BlockRef`.
- **`vehicle_journey_ref`** (string or null): Journey instance identifier from `VehicleJourneyRef`.
- **`origin_aimed_departure_time`** (string or null): Scheduled origin departure time from `OriginAimedDepartureTime`.
- **`data_frame_ref`** (string or null): Service-day identifier from `FramedVehicleJourneyRef/DataFrameRef`.
- **`dated_vehicle_journey_ref`** (string or null): Dated journey identifier from `FramedVehicleJourneyRef/DatedVehicleJourneyRef`.
- **`item_identifier`** (string, required): Unique `VehicleActivity/ItemIdentifier` used by the feeder for deduplication.

#### Example payload

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

- **Kafka:** uses the shared topic `uk-bods-siri`.
- **MQTT:** operator references are retained QoS-1 state; vehicle telemetry is non-retained QoS-0 stream data.
- **AMQP:** application properties expose `operator_ref` and, for telemetry, `vehicle_ref`; the `x-opt-partition-key` annotation mirrors the CloudEvents subject.
