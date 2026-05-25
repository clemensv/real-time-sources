# Nepal BIPAD Portal — Real-Time River Monitoring Bridge Events

Nepal BIPAD River Monitoring publishes river water level observations from Nepal's BIPAD Portal for river monitoring stations in Nepal. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nepal-bipad-hydrology`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nepal-bipad-hydrology'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### River Station

CloudEvents type: `np.gov.bipad.hydrology.RiverStation`

#### What it tells you

A reference record for one river monitoring stations in Nepal published by Nepal's BIPAD Portal. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events. Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nepal-bipad-hydrology`, key `{station_id}` |

#### Payload

`River Station` payloads are JSON object. Required fields: `station_id`, `title`, `basin`, `latitude`, `longitude`, `data_source`.

- **`station_id`** (string, required): Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility.
- **`title`** (string, required): Human-readable name of the river station, typically in the format 'River at Location' (e.g. 'Babai at Chepang').
- **`basin`** (string, required): Name of the river basin the station belongs to (e.g. 'Bagmati', 'Narayani', 'Koshi', 'Karnali', 'Mahakali', 'Babai').
- **`latitude`** (double, required): Latitude coordinate of the station in WGS84 decimal degrees, extracted from the GeoJSON point geometry.
- **`longitude`** (double, required): Longitude coordinate of the station in WGS84 decimal degrees, extracted from the GeoJSON point geometry.
- **`elevation`** (integer or null, optional): Elevation of the station in meters above sea level, as reported by the BIPAD portal. Null when not available.
- **`danger_level`** (double or null, optional): Configured danger water level threshold in meters for the station. Water levels above this indicate a danger condition. Null when not configured.
- **`warning_level`** (double or null, optional): Configured warning water level threshold in meters for the station. Water levels above this indicate a warning condition. Null when not configured.
- **`description`** (string or null, optional): Free-text description of the station, may include historical notes, relocation history, or elevation corrections. Null when not provided.
- **`data_source`** (string, required): Origin system providing the station data, typically 'hydrology.gov.np' for Nepal Department of Hydrology and Meteorology stations.
- **`province`** (integer or null, optional): Nepal province administrative code for the station location. Null when not assigned.
- **`district`** (integer or null, optional): Nepal district administrative code for the station location. Null when not assigned.
- **`municipality`** (integer or null, optional): Nepal municipality or rural municipality administrative code for the station location. Null when not assigned.
- **`ward`** (integer or null, optional): Nepal ward-level administrative code for the station location. Null when not assigned.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "title": "string",
  "basin": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0,
  "danger_level": 0,
  "warning_level": 0,
  "description": "string",
  "data_source": "string",
  "province": 0,
  "district": 0,
  "municipality": 0,
  "ward": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Water Level Reading

CloudEvents type: `np.gov.bipad.hydrology.WaterLevelReading`

#### What it tells you

A current measurement from Nepal's BIPAD Portal for one monitoring site. It carries river water level observations when the upstream feed reports a new or refreshed value. Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal, including current water level, alert status, and trend direction.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nepal-bipad-hydrology`, key `{station_id}` |

#### Payload

`Water Level Reading` payloads are JSON object. Required fields: `station_id`, `title`, `basin`, `status`, `trend`, `water_level_on`.

- **`station_id`** (string, required): Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility.
- **`title`** (string, required): Human-readable name of the river station at the time of the reading.
- **`basin`** (string, required): Name of the river basin the station belongs to at the time of the reading.
- **`water_level`** (double or null, optional): Current water level at the station in meters. Null when the station has no current reading available.
- **`danger_level`** (double or null, optional): Configured danger water level threshold in meters. Null when not configured.
- **`warning_level`** (double or null, optional): Configured warning water level threshold in meters. Null when not configured.
- **`status`** (string, required): Current alert status of the station relative to configured thresholds. Known values: 'BELOW WARNING LEVEL', 'WARNING', 'DANGER'.
- **`trend`** (string, required): Direction of water level change. Known values: 'STEADY', 'RISING', 'FALLING'.
- **`water_level_on`** (string, required): ISO 8601 timestamp of when the water level was measured, in Nepal Standard Time (+05:45).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "title": "string",
  "basin": "string",
  "water_level": 0,
  "danger_level": 0,
  "warning_level": 0,
  "status": "string",
  "trend": "string",
  "water_level_on": "string"
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

- xRegistry manifest: [`xreg/nepal_bipad_hydrology.xreg.json`](xreg/nepal_bipad_hydrology.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
