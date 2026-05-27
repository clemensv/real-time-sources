# Tokyo Docomo Bikeshare feeder Events

Tokyo Docomo Bikeshare publishes station status and availability updates from Docomo Bike Share open feeds for Tokyo bike-share stations. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 2 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{system_id}`, `{system_id}/{station_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `tokyo-docomo-bikeshare`. The record key is `{system_id}`, `{system_id}/{station_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['tokyo-docomo-bikeshare'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `transit/jp/docomo/tokyo-docomo-bikeshare/+/+/+/info`, `transit/jp/docomo/tokyo-docomo-bikeshare/+/+/+/status`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('transit/jp/docomo/tokyo-docomo-bikeshare/+/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `broker-configured address`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/events')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Bikeshare System

CloudEvents type: `JP.ODPT.DocomoBikeshare.BikeshareSystem`

#### What it tells you

A transport update from Docomo Bike Share open feeds. It carries station status and availability updates for Tokyo bike-share stations.

#### Identity

Each event identifies the real-world resource with `{system_id}`. `{system_id}` is unique identifier for this bikeshare system. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tokyo-docomo-bikeshare`, key `{system_id}` |
| `MQTT/5.0` | topic `transit/jp/docomo/tokyo-docomo-bikeshare/{system_id}/{ward}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{system_id}` |

#### Payload

`Bikeshare System` payloads are JSON object. Required fields: `system_id`, `language`, `name`, `timezone`.

- **`system_id`** (string, required): Unique identifier for this bikeshare system. A short, URL-friendly identifier that does not contain spaces, for example 'docomo-cycle-tokyo'. This value is stable and matches the GBFS feed directory name on the ODPT platform.
- **`language`** (string, required): A single IETF BCP 47 language identifier representing the primary language used in this feed, for example 'ja' for Japanese or 'en' for English.
- **`name`** (string, required): Full name of the bikeshare system as displayed to customers, for example 'ドコモ・バイクシェア' or 'Docomo Bikeshare'.
- **`short_name`** (string or null, optional): Optional abbreviation or short form of the system name, for example 'DocomoBike'.
- **`operator`** (string or null, optional): Name of the company or organization that operates the bikeshare system, for example 'NTT Docomo, Inc.'.
- **`url`** (string or null, optional): URL of the bikeshare system or operator website for end users, for example 'https://docomo-cycle.jp/'.
- **`purchase_url`** (string or null, optional): URL where a customer can purchase a membership or learn about purchasing memberships for this bikeshare system.
- **`start_date`** (string or null, optional): Date that the bikeshare system began operations, formatted as YYYY-MM-DD in accordance with ISO 8601.
- **`phone_number`** (string or null, optional): A single voice telephone number for the customer service department of this bikeshare system, including country and area code.
- **`email`** (string or null, optional): A single contact email address actively monitored by the operator's customer service department.
- **`feed_contact_email`** (string or null, optional): A single contact email address for the purpose of reporting issues with the GBFS feed for this system.
- **`timezone`** (string, required): The IANA time zone database name for the time zone where the system is located, for example 'Asia/Tokyo'.
- **`license_url`** (string or null, optional): A fully qualified URL of a page that defines the license terms for the GBFS data published by this system.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "system_id": "string",
  "language": "string",
  "name": "string",
  "short_name": "string",
  "operator": "string",
  "url": "string",
  "purchase_url": "string",
  "start_date": "string",
  "phone_number": "string",
  "email": "string",
  "feed_contact_email": "string",
  "timezone": "string",
  "license_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Bikeshare Station

CloudEvents type: `JP.ODPT.DocomoBikeshare.BikeshareStation`

#### What it tells you

A reference record from Docomo Bike Share open feeds for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{system_id}/{station_id}`. `{system_id}` is identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'; `{station_id}` is unique identifier of the station within the GBFS feed, for example '00010137'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tokyo-docomo-bikeshare`, key `{system_id}/{station_id}` |
| `MQTT/5.0` | topic `transit/jp/docomo/tokyo-docomo-bikeshare/{system_id}/{ward}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{system_id}/{station_id}` |

#### Payload

`Bikeshare Station` payloads are JSON object. Required fields: `system_id`, `station_id`, `name`, `lat`, `lon`.

- **`system_id`** (string, required): Identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'. Included in the payload so that the composite Kafka key {system_id}/{station_id} can be resolved from the event data.
- **`station_id`** (string, required): Unique identifier of the station within the GBFS feed, for example '00010137'. Stable across feed updates; used as the second component of the Kafka key.
- **`name`** (string, required): Public name of the station as displayed to customers. Tokyo Docomo Bikeshare publishes bilingual names in the format 'Japanese / English', for example 'A4-01.東京駅八重洲口 / Tokyo Station Yaesu'.
- **`short_name`** (string or null, optional): Short name or other operator-assigned identifier for the station, if provided.
- **`lat`** (double, required, deg (°)): WGS 84 latitude of the station in decimal degrees. Positive values indicate north of the equator.
- **`lon`** (double, required, deg (°)): WGS 84 longitude of the station in decimal degrees. Positive values indicate east of the prime meridian.
- **`address`** (string or null, optional): Street address of the station, if provided by the operator.
- **`cross_street`** (string or null, optional): Cross street or nearby landmark of the station location, if provided.
- **`region_id`** (string or null, optional): Identifier of the district or region where the station is located, as defined in the GBFS system_regions.json feed.
- **`post_code`** (string or null, optional): Postal code of the station location, if provided.
- **`capacity`** (int32 or null, optional): Total number of docking points installed at the station, including those that are temporarily disabled. Reflects the physical capacity of the station.
- **`is_virtual_station`** (boolean or null, optional): If true, the station is a virtual station (i.e., a parking zone without physical docks) rather than a docked station. If absent or false, the station has physical docking points.
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
  "address": "string",
  "cross_street": "string",
  "region_id": "string",
  "post_code": "string",
  "capacity": 0,
  "is_virtual_station": false
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Bikeshare Station Status

CloudEvents type: `JP.ODPT.DocomoBikeshare.BikeshareStationStatus`

#### What it tells you

A reference record from Docomo Bike Share open feeds for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{system_id}/{station_id}`. `{system_id}` is identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'; `{station_id}` is unique identifier of the station within the GBFS feed, for example '00010137'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tokyo-docomo-bikeshare`, key `{system_id}/{station_id}` |
| `MQTT/5.0` | topic `transit/jp/docomo/tokyo-docomo-bikeshare/{system_id}/{ward}/{station_id}/status`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{system_id}/{station_id}` |

#### Payload

`Bikeshare Station Status` payloads are JSON object. Required fields: `system_id`, `station_id`, `num_bikes_available`, `is_installed`, `is_renting`, `is_returning`.

- **`system_id`** (string, required): Identifier of the bikeshare system this station belongs to, for example 'docomo-cycle-tokyo'. Included in the payload so that the composite Kafka key {system_id}/{station_id} can be resolved from the event data.
- **`station_id`** (string, required): Unique identifier of the station within the GBFS feed, for example '00010137'. Matches the station_id in the corresponding BikeshareStation event.
- **`num_bikes_available`** (int32, required): Number of functional vehicles (bicycles) physically available for rental at this station at the time of the last update.
- **`num_bikes_disabled`** (int32 or null, optional): Number of disabled or broken vehicles at the station that are not available for rental. Absent if the operator does not publish this value.
- **`num_docks_available`** (int32 or null, optional): Number of empty and functional docking points at the station where a customer can return a vehicle. Absent if the operator does not publish this value.
- **`num_docks_disabled`** (int32 or null, optional): Number of broken or disabled docking points at the station that cannot accept vehicle returns. Absent if the operator does not publish this value.
- **`is_installed`** (boolean, required): Indicates whether the station infrastructure is installed on-street and operational. A value of false means the station is temporarily or permanently removed from service.
- **`is_renting`** (boolean, required): Indicates whether the station is currently allowing vehicle rentals. May be false even when bikes are present, for example during a system outage.
- **`is_returning`** (boolean, required): Indicates whether the station is currently accepting vehicle returns. May be false even when docks are empty, for example during a system outage.
- **`last_reported`** (int32 or null, optional): Unix timestamp in seconds (UTC) indicating the last time this station's status was updated by the operator's system. Absent if the operator does not publish this value.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "system_id": "string",
  "station_id": "string",
  "num_bikes_available": 0,
  "num_bikes_disabled": 0,
  "num_docks_available": 0,
  "num_docks_disabled": 0,
  "is_installed": false,
  "is_renting": false,
  "is_returning": false,
  "last_reported": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

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

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/tokyo-docomo-bikeshare.xreg.json`](xreg/tokyo-docomo-bikeshare.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
