# PegelOnline → Apache Kafka, MQTT/UNS & AMQP 1.0 Events

Kafka-transport variants of the PegelOnline CloudEvents, adding per-message Kafka key for partitioning.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The checked-in guide documents a default polling interval of 60 seconds.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `pegelonline`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['pegelonline'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/de/wsv/pegelonline/+/+/info`, `hydro/de/wsv/pegelonline/+/+/water-level`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/de/wsv/pegelonline/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `pegelonline`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/pegelonline')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `de.wsv.pegelonline.Station`

#### What it tells you

Reference catalog entry for one WSV PegelOnline gauge installation. Emitted at bridge startup and periodically refreshed so downstream consumers can interpret CurrentMeasurement events without an out-of-band lookup. Sourced from `GET /stations.json` on the PegelOnline REST API v2.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable UUID assigned by WSV to identify the gauge installation; persists across station renaming, relocation within the same Pegelmessstelle, and timeseries reconfiguration. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `pegelonline`, key `{station_id}` |
| `MQTT/5.0` | topic `hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/pegelonline`, message subject `{station_id}`; application properties water_shortname `{water_shortname}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `number`, `shortname`, `longname`, `agency`, `longitude`, `latitude`, `water`.

- **`station_id`** (string, required): Stable UUID assigned by WSV to identify the gauge installation; persists across station renaming, relocation within the same Pegelmessstelle, and timeseries reconfiguration. Sourced from the upstream `uuid` field. Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic `{station_id}` segment, and the AMQP message subject for every event emitted by this source.
- **`number`** (string, required): Official PegelOnline station number. Carries multiple agency-scoped numbering schemes within the same field: WSV Pegelmessstellennummer (6–8 digits) for German federal gauges; partner-agency identifiers such as Austrian via-donau station numbers (4–5 digits), small Regierungspräsidium-IDs for Bodensee gauges (3-digit numbers e.g. '906' KONSTANZ), and German state-agency IDs (e.g. Ruhrverband 13-digit Messstellennummer). Numeric-only across all observed providers; length is provider-specific. National / agency-scoped identifier — not globally unique across data providers; prefer `station_id` (UUID) for cross-system joins. Constraints: pattern `^[0-9]+$`.
- **`shortname`** (string, required): Operator-assigned display label for the gauge (≤40 characters). May differ from the town name when multiple gauges share a town. Mutable — do not use as a routing key or stable identifier.
- **`longname`** (string, required): Canonical gauge name as used in WSV publications (≤255 characters). Mutable — do not use as a routing key.
- **`km`** (null or double, optional, km): Position along the federal waterway expressed as river-kilometre downstream from the waterway's official origin (e.g. Rhine-km 0 at the Old Rhine Bridge in Konstanz). The decimal fraction is the hectometre offset within the kilometre. Negative values occur on tributaries where the kilometre count is measured upstream from a confluence (e.g. Ohře gauge LOUNY at km -61.4 of the Elbe/Ohře system). **Optional**: absent or null for tidal / coastal gauges (Küstenpegel on the North Sea and Baltic) and for waterways without a kilometre reference. Sourced from the upstream `km` field. Unit: km.
- **`agency`** (string, required): Free-form name of the Wasserstraßen- und Schifffahrtsamt (WSA) operating the gauge — e.g. 'WSA RHEIN', 'WSA ELBE'. Sourced from the upstream `agency` field. Provided so downstream consumers can attribute observations to the operating authority; not a stable identifier and not suitable as a routing key.
- **`longitude`** (double, required, deg (°)): WGS84 decimal-degree longitude of the gauge installation; positive east of the prime meridian. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `longitude` field. Constraints: minimum `-180`, maximum `180`.
- **`latitude`** (double, required, deg (°)): WGS84 decimal-degree latitude of the gauge installation; positive north of the equator. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `latitude` field. Constraints: minimum `-90`, maximum `90`.
- **`water`** (object, required): Federal waterway the gauge measures. See the nested Water schema for routing semantics. See [Water](#payload-de-wsv-pegelonline-station-water).
##### Water
<a id="payload-de-wsv-pegelonline-station-water"></a>

Federal waterway / water body the gauge measures, as returned in the nested `water` object of `GET /stations.json` on the PegelOnline REST API v2. Acts as the routing hierarchy for the MQTT Unified Namespace topology.

- **`shortname`** (string, required): Lowercase routing token for the waterway as published by WSV — e.g. 'rhein', 'elbe', 'donau', 'mosel'. Used (after ASCII-normalization for non-ASCII characters such as 'ß' → 'ss' or umlauts) as the `{water_shortname}` template variable on the MQTT topic and the AMQP application property. Sourced from the upstream `water.shortname` key. Maximum 40 characters.
- **`longname`** (string, required): Canonical uppercase WSV name of the waterway (e.g. 'RHEIN', 'ELBE') as published in official German hydrology bulletins. Sourced from the upstream `water.longname` key. Maximum 255 characters.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "number": "string",
  "shortname": "string",
  "longname": "string",
  "km": 0,
  "agency": "string",
  "longitude": 0,
  "latitude": 0,
  "water": {
    "shortname": "string",
    "longname": "string"
  }
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Current Measurement

CloudEvents type: `de.wsv.pegelonline.CurrentMeasurement`

#### What it tells you

Latest 15-minute water-level reading (W timeseries) for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Telemetry counterpart to the Station reference event; both share the `station_id` keying.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable UUID of the gauge this reading was taken at. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `pegelonline`, key `{station_id}` |
| `MQTT/5.0` | topic `hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/water-level`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/pegelonline`, message subject `{station_id}`; application properties water_shortname `{water_shortname}` |

#### Payload

`Current Measurement` payloads are JSON object. Required fields: `station_id`, `timestamp`, `value`.

- **`station_id`** (string, required): Stable UUID of the gauge this reading was taken at. References the `station_id` of the corresponding Station reference event. Used as the CloudEvents `subject` and the Kafka partition key so all readings for a given gauge land on the same partition / topic key.
- **`timestamp`** (datetime, required): Wall-clock time the upstream reading was taken, in ISO 8601 / RFC 3339 with an explicit UTC offset. PegelOnline publishes the value in Europe/Berlin local time, so the offset shifts between `+01:00` (CET) and `+02:00` (CEST) across the DST boundary — preserve the offset when storing. Sourced from the upstream `timestamp` field.
- **`value`** (double, required, cm): Water-level reading on the W (water-level) timeseries, in centimetres above the gauge's Pegelnullpunkt (PNP — a geodetically fixed datum specific to each gauge, see https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Typical operational range is 0–1500 cm; flood events at major Rhine gauges can exceed 1000 cm. Negative readings are valid at gauges whose normal pool is below PNP (e.g. tidal Elbe at low water). Unit: cm. Constraints: minimum `-1000`, maximum `2500`.
- **`stateMnwMhw`** (enum, optional): Categorical classification of the current water level against the gauge's long-term mean low water (MNW) and mean high water (MHW) reference values, as computed by the upstream feed. Omitted by upstream when the gauge has no MNW/MHW reference series configured (treat absence as 'unknown').
- **`stateNswHsw`** (enum, optional): Categorical classification of the current water level against the highest navigable water level (HSW) reference for the reach, as computed by the upstream feed. Drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Note: upstream never emits 'low' on this series — HSW is an upper bound only. Omitted by upstream when the gauge has no HSW reference (treat absence as 'unknown').
- **`trend`** (int8 or null, optional): Short-term trend of the water level relative to the previous reading, as classified by the upstream feed. First-class signal for flood-monitoring dashboards. Sourced from the upstream `trend` field; omitted when upstream cannot compute a trend (e.g. first reading after a gap).
##### `stateMnwMhw` values

- `low` — Below the gauge's mean low water (MNW) reference
- `normal` — Between MNW and the gauge's mean high water (MHW) reference
- `high` — Above MHW
- `unknown` — MNW/MHW reference values are not configured for this station
- `commented` — Value carries an operator comment overriding the automatic classification
- `out-dated` — Reading is stale relative to the gauge's configured freshness window (typically 90 minutes) — do not treat as authoritative
##### `stateNswHsw` values

- `normal` — Below the highest navigable water level (HSW / Höchster Schifffahrtswasserstand)
- `high` — At or above HSW — navigation typically suspended on the affected reach
- `unknown` — HSW reference value is not configured for this station
- `commented` — Value carries an operator comment overriding the automatic classification
- `out-dated` — Reading is stale relative to the gauge's configured freshness window
##### `trend` values

- `-1` — Falling — current value is below the previous reading
- `0` — Steady — within the upstream classification's noise band of the previous reading
- `1` — Rising — current value is above the previous reading
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "value": 0,
  "stateMnwMhw": "low",
  "stateNswHsw": "normal",
  "trend": -1
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
- The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/pegelonline.xreg.json`](xreg/pegelonline.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- PegelOnline: <https://www.pegelonline.wsv.de/>
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
