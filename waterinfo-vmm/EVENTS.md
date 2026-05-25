# Waterinfo VMM (Belgium/Flanders) Water Level Bridge Events

Waterinfo VMM publishes water level observations from Waterinfo.be and the Flemish Environment Agency (VMM) for Flemish water monitoring locations. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_no}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `waterinfo-vmm`. The record key is `{station_no}`. In plain language, `{station_no}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['waterinfo-vmm'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `BE.Vlaanderen.Waterinfo.VMM.Station`

#### What it tells you

A reference record for one Flemish water monitoring location published by Waterinfo.be and the Flemish Environment Agency (VMM). It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events. Reference details for one monitoring station or site in the Waterinfo VMM source.

#### Identity

Each event identifies the real-world resource with `{station_no}`. `{station_no}` is provider-supplied station no value for this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `waterinfo-vmm`, key `{station_no}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_no`, `station_name`, `station_latitude`, `station_longitude`.

- **`station_no`** (string, required): Provider-supplied station no value for this record.
- **`station_name`** (string, required): Human-readable name of the monitoring station.
- **`station_id`** (string, optional): Stable identifier assigned by the upstream provider for the monitoring station or site.
- **`station_latitude`** (double, required): Provider-supplied station latitude value for this record.
- **`station_longitude`** (double, required): Provider-supplied station longitude value for this record.
- **`river_name`** (string or null, optional): Name of the river or watercourse observed at the station.
- **`stationparameter_name`** (string or null, optional): Human-readable name of the stationparameter.
- **`ts_id`** (string or null, optional): Stable identifier assigned by the upstream provider for the ts.
- **`ts_unitname`** (string or null, optional): Provider-supplied ts unitname value for this record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_no": "string",
  "station_name": "string",
  "station_id": "string",
  "station_latitude": 0,
  "station_longitude": 0,
  "river_name": "string",
  "stationparameter_name": "string",
  "ts_id": "string",
  "ts_unitname": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Water Level Reading

CloudEvents type: `BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading`

#### What it tells you

A current measurement from Waterinfo.be and the Flemish Environment Agency (VMM) for one monitoring site. It carries water level observations when the upstream feed reports a new or refreshed value. WaterLevelReading

#### Identity

Each event identifies the real-world resource with `{station_no}`. `{station_no}` is provider-supplied station no value for this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `waterinfo-vmm`, key `{station_no}` |

#### Payload

`Water Level Reading` payloads are JSON object. Required fields: `ts_id`, `station_no`, `timestamp`, `value`.

- **`ts_id`** (string, required): Stable identifier assigned by the upstream provider for the ts.
- **`station_no`** (string, required): Provider-supplied station no value for this record.
- **`station_name`** (string, optional): Human-readable name of the monitoring station.
- **`timestamp`** (datetime, required): Time when the provider recorded or published the observation.
- **`value`** (double, required): Measured value reported by the upstream provider.
- **`unit_name`** (string, optional): Human-readable name of the unit.
- **`parameter_name`** (string, optional): Plain-language name of the measured parameter.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "ts_id": "string",
  "station_no": "string",
  "station_name": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "value": 0,
  "unit_name": "string",
  "parameter_name": "string"
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

- xRegistry manifest: [`xreg/waterinfo_vmm.xreg.json`](xreg/waterinfo_vmm.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- KIWIS API docs: <https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&request=getrequestinfo>
