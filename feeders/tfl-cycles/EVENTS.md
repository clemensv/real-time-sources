# TfL Santander Cycles Events

Transport-neutral event family for the Transport for London public cycle-hire scheme (branded Santander Cycles, operated on the TfL BikePoint platform). Both the slowly-changing docking-station reference event and the near-real-time availability event are keyed by the stable BikePoint identifier `{station_id}` so consumers can build temporally consistent views of one docking station.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `tfl-cycles`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['tfl-cycles'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `mobility/tfl-cycles/+/info`, `mobility/tfl-cycles/+/status`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('mobility/tfl-cycles/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `tfl-cycles`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/tfl-cycles')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station Information

CloudEvents type: `UK.Gov.TfL.Cycles.StationInformation`

#### What it tells you

Reference data describing one Transport for London cycle-hire docking station (BikePoint), sourced from the TfL Unified API `GET /BikePoint` response `Place` object. Carries the stable BikePoint identifier, customer-facing name, WGS 84 coordinates, legacy terminal identifier, physical docking capacity, and provisioning lifecycle flags. Emitted at bridge startup and on periodic reference refresh so consumers can join StationStatus availability records against stable station metadata.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable BikePoint identifier from the `id` field of the TfL `Place` object, for example `BikePoints_1`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tfl-cycles`, key `{station_id}` |
| `MQTT/5.0` | topic `mobility/tfl-cycles/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tfl-cycles`, message subject `{station_id}` |

#### Payload

`Station Information` payloads are JSON object. Required fields: `station_id`, `name`, `lat`, `lon`.

- **`station_id`** (string, required): Stable BikePoint identifier from the `id` field of the TfL `Place` object, for example `BikePoints_1`. It is unique within the London cycle-hire scheme, persists across API refreshes, appears in the `/Place/{id}` resource URL, and forms the single component of both the CloudEvents subject and the Kafka key.
- **`name`** (string, required): Customer-facing station name from the `commonName` field of the TfL `Place` object, for example `River Street , Clerkenwell`. Intended for maps, screens, and accessibility tooling.
- **`lat`** (double, required, deg (°)): WGS 84 latitude of the docking station in decimal degrees from the `lat` field of the TfL `Place` object. Positive values are north of the equator. Constraints: minimum `-90`, maximum `90`.
- **`lon`** (double, required, deg (°)): WGS 84 longitude of the docking station in decimal degrees from the `lon` field of the TfL `Place` object. Positive values are east of the prime meridian and negative values are west; all London BikePoints are slightly west or east of Greenwich. Constraints: minimum `-180`, maximum `180`.
- **`terminal_name`** (null or string, optional): Legacy terminal identifier from the `TerminalName` entry in `additionalProperties`, for example `001023`. This is the numbering used by the original cycle-hire terminal hardware and the legacy `livecyclehireupdates.xml` feed; the bridge emits null when the entry is absent.
- **`capacity`** (null or int32, optional): Total number of physical docking points at the station, parsed from the string-valued `NbDocks` entry in `additionalProperties`. Represents the fixed physical size of the docking station; the bridge emits null when `NbDocks` is absent or non-numeric. Constraints: minimum `0`.
- **`temporary`** (null or boolean, optional): Whether the docking station is a temporary installation, parsed from the string-valued `Temporary` entry in `additionalProperties` (`true`/`false`). Temporary stations are deployed for events or roadworks and may be removed; the bridge emits null when the entry is absent.
- **`install_date`** (null or datetime, optional): Timestamp at which the docking station was installed, in ISO 8601 / RFC 3339 UTC. The upstream `InstallDate` entry in `additionalProperties` is a string of Unix epoch milliseconds (for example `1278947280000`); the bridge converts it to an absolute UTC instant and emits null when the entry is empty or absent.
- **`removal_date`** (null or datetime, optional): Timestamp at which the docking station is scheduled to be, or was, removed, in ISO 8601 / RFC 3339 UTC. The upstream `RemovalDate` entry in `additionalProperties` is a string of Unix epoch milliseconds or an empty string; the bridge converts a populated value to an absolute UTC instant and emits null for active stations with no removal scheduled.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "lat": 0,
  "lon": 0,
  "terminal_name": "string",
  "capacity": 0,
  "temporary": false,
  "install_date": "2024-01-01T00:00:00Z",
  "removal_date": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Station Status

CloudEvents type: `UK.Gov.TfL.Cycles.StationStatus`

#### What it tells you

Near-real-time availability telemetry for one Transport for London cycle-hire docking station (BikePoint), derived from the `additionalProperties` key/value entries of the TfL Unified API `GET /BikePoint` response. Reports the current count of rentable standard bikes and e-bikes, empty docks available for returns, total docks, and the operating flags together with the most recent upstream modification timestamp for the station. Near-real-time availability record for one Transport for London cycle-hire docking station (BikePoint), derived from the string-valued `additionalProperties` key/value entries on the TfL `Place` object returned by `GET /BikePoint`.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable BikePoint identifier from the `id` field of the TfL `Place` object, for example `BikePoints_1`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tfl-cycles`, key `{station_id}` |
| `MQTT/5.0` | topic `mobility/tfl-cycles/{station_id}/status`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tfl-cycles`, message subject `{station_id}` |

#### Payload

`Station Status` payloads are JSON object. Required fields: `station_id`, `num_bikes_available`, `num_empty_docks`, `is_installed`, `is_locked`, `modified`.

- **`station_id`** (string, required): Stable BikePoint identifier from the `id` field of the TfL `Place` object, for example `BikePoints_1`. Matches the `station_id` of the corresponding `StationInformation` event and forms the CloudEvents subject and Kafka key.
- **`num_bikes_available`** (int32, required): Total number of rentable cycles currently docked and available at the station (standard pedal bikes plus e-bikes), parsed from the string-valued `NbBikes` entry in `additionalProperties`. Constraints: minimum `0`.
- **`num_standard_bikes_available`** (null or int32, optional): Number of mechanical (non-electric) pedal cycles currently available at the station, parsed from the string-valued `NbStandardBikes` entry in `additionalProperties`. The bridge emits null when the operator does not report the standard/e-bike split for the station. Constraints: minimum `0`.
- **`num_ebikes_available`** (null or int32, optional): Number of electrically assisted cycles (e-bikes) currently available at the station, parsed from the string-valued `NbEBikes` entry in `additionalProperties`. The bridge emits null when the operator does not report the standard/e-bike split for the station. Constraints: minimum `0`.
- **`num_empty_docks`** (int32, required): Number of empty docking points currently available for returning a cycle at the station, parsed from the string-valued `NbEmptyDocks` entry in `additionalProperties`. Constraints: minimum `0`.
- **`num_docks`** (null or int32, optional): Total number of docking points reported live for the station in this poll, parsed from the string-valued `NbDocks` entry in `additionalProperties`. Under normal operation this equals `num_bikes_available` plus `num_empty_docks` plus any broken docks; the bridge emits null when `NbDocks` is absent or non-numeric. Constraints: minimum `0`.
- **`is_installed`** (boolean, required): Whether the station is currently installed and in service, parsed from the string-valued `Installed` entry in `additionalProperties` (`true`/`false`). A value of false indicates the station is not physically present or is decommissioned.
- **`is_locked`** (boolean, required): Whether the station is currently locked and temporarily out of service, parsed from the string-valued `Locked` entry in `additionalProperties` (`true`/`false`). A locked station accepts neither rentals nor returns even when it reports available bikes or docks.
- **`modified`** (datetime, required): Most recent modification timestamp among the station's `additionalProperties` entries, in ISO 8601 / RFC 3339 UTC. Each availability property on the TfL `Place` object carries its own `modified` timestamp; the bridge takes the newest of these as the point in time at which TfL last updated this station's availability counts.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "num_bikes_available": 0,
  "num_standard_bikes_available": 0,
  "num_ebikes_available": 0,
  "num_empty_docks": 0,
  "num_docks": 0,
  "is_installed": false,
  "is_locked": false,
  "modified": "2024-01-01T00:00:00Z"
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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/tfl-cycles.xreg.json`](xreg/tfl-cycles.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Unified API BikePoint: <https://api.tfl.gov.uk/BikePoint>
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
