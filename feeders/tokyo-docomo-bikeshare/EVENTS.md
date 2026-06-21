# Tokyo Docomo Bikeshare event reference

This document defines the CloudEvents contract emitted by this Tokyo Docomo thin wrapper over the generalized GBFS bikeshare feeder. For the project overview see README.md; for the published container images and runtime configuration see CONTAINER.md.

## At a glance

- **Event types:** 4 documented event types (16 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 4 telemetry event types.
- **Identity:** `{system_id}`, `{system_id}/{station_id}`, `{system_id}/{bike_id}` identifies the resource each event is about.
- **Operations:** The checked-in guide documents a default polling interval of 60 seconds.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `tokyo-docomo-bikeshare`. The record key is `{system_id}`, `{system_id}/{station_id}`, `{system_id}/{bike_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['gbfs-bikeshare'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `mobility/gbfs/+/system`, `mobility/gbfs/+/+/info`, `mobility/gbfs/+/+/status`, `mobility/gbfs/+/+/position`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('mobility/gbfs/+/system', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `gbfs-bikeshare`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/tokyo-docomo-bikeshare')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### System Information

CloudEvents type: `org.gbfs.SystemInformation`

#### What it tells you

Reference data describing one GBFS system as published in `system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against stable system metadata. Reference data from the GBFS `system_information.json` feed.

#### Identity

Each event identifies the real-world resource with `{system_id}`. `{system_id}` is stable identifier for the GBFS system from the `system_id` field in `system_information.json`, or a configured override when the user supplies `GBFS_SYSTEM_IDS` to relabel systems consistently across deployments. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gbfs-bikeshare`, key `{system_id}` |
| `MQTT/5.0` | topic `mobility/gbfs/{system_id}/system`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tokyo-docomo-bikeshare`, message subject `{system_id}` |

#### Payload

`System Information` payloads are JSON object. Required fields: `system_id`, `name`, `timezone`.

- **`system_id`** (string, required): Stable identifier for the GBFS system from the `system_id` field in `system_information.json`, or a configured override when the user supplies `GBFS_SYSTEM_IDS` to relabel systems consistently across deployments.
- **`name`** (string, required): Public system display name from the `name` field in `system_information.json`, such as the brand name shown in the operator app and on the website.
- **`operator`** (string or null, optional): Optional operator company or agency name from the `operator` field in `system_information.json`.
- **`url`** (string or null, optional): Optional public website URL from the `url` field in `system_information.json`.
- **`timezone`** (string, required): IANA timezone identifier from the `timezone` field in `system_information.json`, such as `America/New_York` or `Europe/London`.
- **`language`** (string or null, optional): Optional BCP-47 language tag from the `language` field in `system_information.json`, representing the primary language used in this dataset.
- **`phone_number`** (string or null, optional): Optional customer-service phone number from the `phone_number` field in `system_information.json`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "system_id": "string",
  "name": "string",
  "operator": "string",
  "url": "string",
  "timezone": "string",
  "language": "string",
  "phone_number": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Station Information

CloudEvents type: `org.gbfs.StationInformation`

#### What it tells you

Reference data for one dock-based GBFS station from `station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking capacity, and optional address / regional context so consumers can interpret real-time availability telemetry. Dock-based station reference data from the GBFS `station_information.json` feed.

#### Identity

Each event identifies the real-world resource with `{system_id}/{station_id}`. `{system_id}` is stable identifier for the GBFS system that publishes this station; `{station_id}` is unique station identifier within the GBFS system, sourced from the `station_id` field in `station_information.json`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gbfs-bikeshare`, key `{system_id}/{station_id}` |
| `MQTT/5.0` | topic `mobility/gbfs/{system_id}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tokyo-docomo-bikeshare`, message subject `{system_id}/{station_id}` |

#### Payload

`Station Information` payloads are JSON object. Required fields: `system_id`, `station_id`, `name`, `lat`, `lon`.

- **`system_id`** (string, required): Stable identifier for the GBFS system that publishes this station. The bridge resolves it from `system_information.system_id`, or from operator configuration when a custom label is supplied. It is the first component of the CloudEvents subject and Kafka key.
- **`station_id`** (string, required): Unique station identifier within the GBFS system, sourced from the `station_id` field in `station_information.json`. This identifier is stable across feed refreshes and forms the second component of the CloudEvents subject and Kafka key.
- **`name`** (string, required): Public-facing station name from `station_information.json`. GBFS recommends mixed-case, human-readable names suitable for maps, screens, and accessibility tooling.
- **`short_name`** (string or null, optional): Optional short station name or numbering code from the `short_name` field in `station_information.json`, such as a kiosk number or abbreviated label used on maps or in the operator app.
- **`lat`** (number, required, degree): WGS 84 latitude of the station in decimal degrees from `station_information.json`. GBFS recommends six decimal places of precision for latitude / longitude coordinates. Constraints: minimum `-90`, maximum `90`.
- **`lon`** (number, required, degree): WGS 84 longitude of the station in decimal degrees from `station_information.json`. Positive values are east of the prime meridian and negative values are west. Constraints: minimum `-180`, maximum `180`.
- **`capacity`** (integer or null, optional): Total number of docking points or parking capacity published for the station in `station_information.json`. When omitted upstream, the bridge emits null rather than inventing a capacity.
- **`region_id`** (string or null, optional): Optional region identifier from the `region_id` field in `station_information.json`. When present, it links the station to a region published in `system_regions.json`.
- **`address`** (string or null, optional): Optional street address from the `address` field in `station_information.json`, as supplied by the operator for customer navigation.
- **`post_code`** (string or null, optional): Optional postal or ZIP code from the `post_code` field in `station_information.json`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "system_id": "string",
  "station_id": "string",
  "name": "string",
  "short_name": "string",
  "lat": 0,
  "lon": 0,
  "capacity": 0,
  "region_id": "string",
  "address": "string",
  "post_code": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Station Status

CloudEvents type: `org.gbfs.StationStatus`

#### What it tells you

Real-time station availability telemetry from `station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the upstream `last_reported` timestamp for one GBFS station. Near-real-time station availability data from the GBFS `station_status.json` feed.

#### Identity

Each event identifies the real-world resource with `{system_id}/{station_id}`. `{system_id}` is stable identifier for the GBFS system that publishes this station status record; `{station_id}` is stable station identifier from the `station_id` field in `station_status.json`, matching the corresponding `StationInformation` event. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gbfs-bikeshare`, key `{system_id}/{station_id}` |
| `MQTT/5.0` | topic `mobility/gbfs/{system_id}/{station_id}/status`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tokyo-docomo-bikeshare`, message subject `{system_id}/{station_id}` |

#### Payload

`Station Status` payloads are JSON object. Required fields: `system_id`, `station_id`, `num_bikes_available`, `is_installed`, `is_renting`, `is_returning`, `last_reported`.

- **`system_id`** (string, required): Stable identifier for the GBFS system that publishes this station status record.
- **`station_id`** (string, required): Stable station identifier from the `station_id` field in `station_status.json`, matching the corresponding `StationInformation` event.
- **`num_bikes_available`** (integer, required): Current number of rentable bikes or vehicles available at the station from the `num_bikes_available` field in `station_status.json`.
- **`num_docks_available`** (integer or null, optional): Current number of empty docks or parking spaces available for return at the station from `num_docks_available`. Some operators omit this field, in which case the bridge emits null.
- **`num_ebikes_available`** (integer or null, optional): Current number of electric bikes available at the station from `num_ebikes_available` when the operator distinguishes e-bikes from the aggregate bike count.
- **`is_installed`** (boolean, required): Boolean flag indicating whether the station is physically installed, normalized from the GBFS `is_installed` value.
- **`is_renting`** (boolean, required): Boolean flag indicating whether the station is currently accepting rentals, normalized from the GBFS `is_renting` value.
- **`is_returning`** (boolean, required): Boolean flag indicating whether the station is currently accepting vehicle returns, normalized from the GBFS `is_returning` value.
- **`last_reported`** (integer, required): POSIX timestamp from the GBFS `last_reported` field representing when the operator backend last received a status update for this station.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "system_id": "string",
  "station_id": "string",
  "num_bikes_available": 0,
  "num_docks_available": 0,
  "num_ebikes_available": 0,
  "is_installed": false,
  "is_renting": false,
  "is_returning": false,
  "last_reported": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Free Bike Status

CloudEvents type: `org.gbfs.FreeBikeStatus`

#### What it tells you

Real-time dockless vehicle telemetry from `free_bike_status.json` (renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location, reservation and disablement state, optional vehicle type reference, and optional remaining range for a single rentable vehicle that is not currently in an active trip. Dockless vehicle telemetry from the GBFS `free_bike_status.json` feed, which is renamed `vehicle_status.json` in GBFS v3.

#### Identity

Each event identifies the real-world resource with `{system_id}/{bike_id}`. `{system_id}` is stable identifier for the GBFS system that publishes this dockless-vehicle status record; `{bike_id}` is unique vehicle identifier from the `bike_id` field in `free_bike_status.json`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gbfs-bikeshare`, key `{system_id}/{bike_id}` |
| `MQTT/5.0` | topic `mobility/gbfs/{system_id}/{bike_id}/position`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tokyo-docomo-bikeshare`, message subject `{system_id}/{bike_id}` |

#### Payload

`Free Bike Status` payloads are JSON object. Required fields: `system_id`, `bike_id`, `is_reserved`, `is_disabled`.

- **`system_id`** (string, required): Stable identifier for the GBFS system that publishes this dockless-vehicle status record.
- **`bike_id`** (string, required): Unique vehicle identifier from the `bike_id` field in `free_bike_status.json`. This value is stable for the vehicle within the system and forms the second component of the CloudEvents subject and Kafka key.
- **`lat`** (number or null, optional, degree): Optional WGS 84 latitude in decimal degrees for the vehicle's current position. GBFS allows free-bike records without coordinates when precise location is not published. Constraints: minimum `-90`, maximum `90`.
- **`lon`** (number or null, optional, degree): Optional WGS 84 longitude in decimal degrees for the vehicle's current position. Constraints: minimum `-180`, maximum `180`.
- **`is_reserved`** (boolean, required): Boolean flag from `is_reserved` indicating whether the vehicle is currently reserved for a customer and therefore not immediately rentable by others.
- **`is_disabled`** (boolean, required): Boolean flag from `is_disabled` indicating whether the vehicle is disabled or otherwise unavailable for rental.
- **`vehicle_type_id`** (string or null, optional): Optional vehicle-type identifier from `vehicle_type_id`, used by operators that publish multiple vehicle classes such as e-bikes or scooters.
- **`current_range_meters`** (number or null, optional, meter): Optional remaining electric range in meters from `current_range_meters`, typically published for electric vehicles.
- **`last_reported`** (integer or null, optional): Optional POSIX timestamp from the `last_reported` field representing the last time the operator backend received a telemetry update for this vehicle.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "system_id": "string",
  "bike_id": "string",
  "lat": 0,
  "lon": 0,
  "is_reserved": false,
  "is_disabled": false,
  "vehicle_type_id": "string",
  "current_range_meters": 0,
  "last_reported": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

- The checked-in guide documents a default polling interval of 60 seconds.
- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`../gbfs-bikeshare/xreg/gbfs-bikeshare.xreg.json`](../gbfs-bikeshare/xreg/gbfs-bikeshare.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
