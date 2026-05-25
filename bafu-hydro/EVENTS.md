# BAFU Hydrology Bridge Usage Guide Events

BAFU Hydrology publishes water level, discharge, and water temperature observations from the Swiss Federal Office for the Environment (BAFU/FOEN) for Swiss river, lake, and stream gauges. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types (4 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The checked-in guide documents a default polling interval of 600 seconds.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `bafu-hydro`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['bafu-hydro'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/ch/bafu/bafu-hydro/+/+/info`, `hydro/ch/bafu/bafu-hydro/+/+/water-level`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/ch/bafu/bafu-hydro/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Station

CloudEvents type: `CH.BAFU.Hydrology.Station`

#### What it tells you

A reference record for one Swiss river, lake, and stream gauge published by the Swiss Federal Office for the Environment (BAFU/FOEN). It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events. Reference details for one monitoring station or site in the BAFU Hydrology source.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the monitoring station or site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bafu-hydro`, key `{station_id}` |
| `MQTT/5.0` | topic `hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/info`, retain `true`, QoS `1` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `name`, `latitude`, `longitude`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the monitoring station or site.
- **`name`** (string, required): Human-readable name of the station, site, or location.
- **`water_body_name`** (string, optional): Name of the river, lake, canal, reservoir, or other water body observed at the station.
- **`water_body_type`** (string, optional): Provider classification for the observed water body.
- **`latitude`** (double, required): Latitude of the station in WGS 84 coordinates.
- **`longitude`** (double, required): Longitude of the station in WGS 84 coordinates.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "water_body_name": "string",
  "water_body_type": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Water Level Observation

CloudEvents type: `CH.BAFU.Hydrology.WaterLevelObservation`

#### What it tells you

A current measurement from the Swiss Federal Office for the Environment (BAFU/FOEN) for one monitoring site. It carries water level, discharge, and water temperature observations when the upstream feed reports a new or refreshed value. Measurement payload for water level, discharge, and water temperature observations in the BAFU Hydrology source.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the monitoring station or site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bafu-hydro`, key `{station_id}` |
| `MQTT/5.0` | topic `hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/water-level`, retain `true`, QoS `1` |

#### Payload

`Water Level Observation` payloads are JSON object. Required fields: `station_id`, `water_body_name`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the monitoring station or site.
- **`water_body_name`** (string, required): Name of the water body the station observes (BAFU/FOEN 'water-body-name' field, e.g. 'Rhein', 'Aare', 'Bodensee'). Sourced by the bridge from the station catalog (existenz.ch /apiv1/hydro/locations endpoint, details.water-body-name) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river / lake. Used as the {water_body_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing.
- **`water_level`** (double, optional): Current water level reported for the station.
- **`water_level_unit`** (string, optional): Unit used for the water-level value.
- **`water_level_timestamp`** (datetime, optional): Time associated with the water-level measurement.
- **`discharge`** (double, optional): Current streamflow or discharge reported for the station.
- **`discharge_unit`** (string, optional): Unit used for the discharge value.
- **`discharge_timestamp`** (datetime, optional): Time associated with the discharge measurement.
- **`water_temperature`** (double, optional): Current water temperature reported for the station.
- **`water_temperature_unit`** (string, optional): Unit used for the water-temperature value.
- **`water_temperature_timestamp`** (datetime, optional): Time associated with the water-temperature measurement.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "water_body_name": "string",
  "water_level": 0,
  "water_level_unit": "string",
  "water_level_timestamp": "2024-01-01T00:00:00Z",
  "discharge": 0,
  "discharge_unit": "string",
  "discharge_timestamp": "2024-01-01T00:00:00Z",
  "water_temperature": 0,
  "water_temperature_unit": "string",
  "water_temperature_timestamp": "2024-01-01T00:00:00Z"
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

- The checked-in guide documents a default polling interval of 600 seconds.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/bafu_hydro.xreg.json`](xreg/bafu_hydro.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- existenz.ch Hydro API: <https://api.existenz.ch>
