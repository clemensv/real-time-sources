# iRail Events

iRail publishes train departure, arrival, and connection updates from the Belgian iRail train data API for Belgian railway stations, vehicles, and connections. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 2 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `irail`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['irail'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `transit/be/irail/irail/+/info`, `transit/be/irail/irail/+/station-board`, `transit/be/irail/irail/+/arrival-board`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('transit/be/irail/irail/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `irail`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/irail')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `be.irail.Station`

#### What it tells you

Metadata for a Belgian railway station in the NMBS/SNCB network as provided by the iRail API. The Belgian rail network comprises approximately 600 passenger stations. Each station has a unique UIC-derived numeric identifier assigned by the NMBS, geographic coordinates, and multilingual names.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is nine-digit UIC-derived numeric station identifier assigned by NMBS. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `irail`, key `{station_id}` |
| `MQTT/5.0` | topic `transit/be/irail/irail/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/irail`, message subject `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `name`, `standard_name`, `longitude`, `latitude`, `uri`.

- **`station_id`** (string, required): Nine-digit UIC-derived numeric station identifier assigned by NMBS. Extracted from the iRail id field by stripping the 'BE.NMBS.' prefix. Example: '008814001' for Brussels-South (Bruxelles-Midi / Brussel-Zuid).
- **`name`** (string, required): Default display name of the station in the requested language. Example: 'Brussels-South'.
- **`standard_name`** (string, required): Consistent official station name that does not vary by language, typically using the primary local name. Example: 'Bruxelles-Midi / Brussel-Zuid'.
- **`longitude`** (double, required, deg (°)): Longitude of the station in WGS84 decimal degrees. Sourced from the iRail locationX field.
- **`latitude`** (double, required, deg (°)): Latitude of the station in WGS84 decimal degrees. Sourced from the iRail locationY field.
- **`uri`** (string, required): Stable linked-data URI identifying this station in the iRail namespace. Example: 'http://irail.be/stations/NMBS/008814001'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "standard_name": "string",
  "longitude": 0,
  "latitude": 0,
  "uri": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Station Board

CloudEvents type: `be.irail.StationBoard`

#### What it tells you

A real-time departure board snapshot for a Belgian railway station from the iRail liveboard API. Contains all currently scheduled departures from the station with real-time delay information, platform assignments, cancellation status, and crowd-sourced occupancy levels. The board is polled periodically and each event replaces the previous board state for the same station.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is nine-digit UIC-derived numeric identifier of the station this board belongs to. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `irail`, key `{station_id}` |
| `MQTT/5.0` | topic `transit/be/irail/irail/{station_id}/station-board`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/irail`, message subject `{station_id}` |

#### Payload

`Station Board` payloads are JSON object. Required fields: `station_id`, `station_name`, `retrieved_at`, `departure_count`, `departures`.

- **`station_id`** (string, required): Nine-digit UIC-derived numeric identifier of the station this board belongs to. Matches the station_id in the Station schema.
- **`station_name`** (string, required): Display name of the station this board belongs to.
- **`retrieved_at`** (string, required): ISO 8601 UTC timestamp when this board was retrieved from the iRail API. Converted from the iRail response timestamp field.
- **`departure_count`** (int32, required): Number of departures in this board snapshot. Matches the length of the departures array.
- **`departures`** (array of object, required): Array of departure entries currently shown on the station's departure board. Each entry represents a train service scheduled to depart from this station, enriched with real-time delay and cancellation information.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "retrieved_at": "string",
  "departure_count": 0,
  "departures": [
    {
      "destination_station_id": "string",
      "destination_name": "string",
      "scheduled_time": "string",
      "delay_seconds": 0,
      "is_canceled": false,
      "has_left": false,
      "is_extra_stop": false,
      "vehicle_id": "string",
      "vehicle_short_name": "string",
      "vehicle_type": "string",
      "vehicle_number": "string",
      "platform": "string",
      "is_normal_platform": false,
      "occupancy": "low",
      "departure_connection_uri": "string"
    }
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Arrival Board

CloudEvents type: `be.irail.ArrivalBoard`

#### What it tells you

A real-time arrival board snapshot for a Belgian railway station from the iRail liveboard API. Contains all currently scheduled arrivals at the station with real-time delay information, platform assignments, cancellation status, and crowd-sourced occupancy levels. The board is polled periodically and each event replaces the previous arrival-board state for the same station.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is nine-digit UIC-derived numeric identifier of the station this board belongs to. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `irail`, key `{station_id}` |
| `MQTT/5.0` | topic `transit/be/irail/irail/{station_id}/arrival-board`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/irail`, message subject `{station_id}` |

#### Payload

`Arrival Board` payloads are JSON object. Required fields: `station_id`, `station_name`, `retrieved_at`, `arrival_count`, `arrivals`.

- **`station_id`** (string, required): Nine-digit UIC-derived numeric identifier of the station this board belongs to. Matches the station_id in the Station schema.
- **`station_name`** (string, required): Display name of the station this board belongs to.
- **`retrieved_at`** (string, required): ISO 8601 UTC timestamp when this board was retrieved from the iRail API. Converted from the iRail response timestamp field.
- **`arrival_count`** (int32, required): Number of arrivals in this board snapshot. Matches the length of the arrivals array.
- **`arrivals`** (array of object, required): Array of arrival entries currently shown on the station's arrival board. Each entry represents a train service scheduled to arrive at this station, enriched with real-time delay and cancellation information.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "retrieved_at": "string",
  "arrival_count": 0,
  "arrivals": [
    {
      "origin_station_id": "string",
      "origin_name": "string",
      "scheduled_time": "string",
      "delay_seconds": 0,
      "is_canceled": false,
      "has_arrived": false,
      "is_extra_stop": false,
      "vehicle_id": "string",
      "vehicle_short_name": "string",
      "vehicle_type": "string",
      "vehicle_number": "string",
      "platform": "string",
      "is_normal_platform": false,
      "occupancy": "low",
      "connection_uri": "string"
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

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

## References

- xRegistry manifest: [`xreg/irail.xreg.json`](xreg/irail.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- iRail API: <https://docs.irail.be/>
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
