# KiWIS Events

Transport-neutral KiWIS station catalog events keyed by `{kiwis_id}/{station_id}`. Stations are emitted at startup and periodically refreshed before value telemetry so consumers can interpret timeseries in temporal context.

## At a glance

- **Event types:** 3 documented event types (12 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{kiwis_id}/{station_id}`, `{kiwis_id}/{ts_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `kiwis`. The record key is `{kiwis_id}/{station_id}`, `{kiwis_id}/{ts_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['kiwis'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/kiwis/+/stations/+/info`, `hydro/kiwis/+/timeseries/+/metadata`, `hydro/kiwis/+/timeseries/+/value`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/kiwis/+/stations/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `kiwis`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/kiwis')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `org.kiwis.Station`

#### What it tells you

Reference metadata for one observation station returned by KiWIS getStationList, including stable identifiers, public names, WGS 84 coordinates, river, and catchment context. Reference station payload from KiWIS getStationList with stable identifiers, optional location, river, and catchment context.

#### Identity

Each event identifies the real-world resource with `{kiwis_id}/{station_id}`. `{kiwis_id}` is configuration-assigned identifier for the KiWIS endpoint/datasource; `{station_id}` is stable KiWIS station_id returned by getStationList. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `kiwis`, key `{kiwis_id}/{station_id}` |
| `MQTT/5.0` | topic `hydro/kiwis/{kiwis_id}/stations/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/kiwis`, message subject `{kiwis_id}/{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `kiwis_id`, `base_url`, `station_id`.

- **`kiwis_id`** (string, required): Configuration-assigned identifier for the KiWIS endpoint/datasource. It qualifies upstream identifiers because station_id and ts_id are unique only within a KiWIS datasource.
- **`base_url`** (uri, required): Base KiWIS queryServices URL used as the CloudEvents source and as provenance for records from this instance.
- **`station_id`** (string, required): Stable KiWIS station_id returned by getStationList. This is the station identity within one KiWIS datasource and forms the station event subject with kiwis_id.
- **`station_no`** (string or null, optional): Agency station number returned by getStationList. It is useful for user-facing cross-reference but is not used as the primary event key because KiWIS documents station_id as the stable query identifier.
- **`station_name`** (string or null, optional): Human-readable station name returned by getStationList for display, search, and map labels; not stable enough for keys.
- **`latitude`** (double or null, optional): Station latitude in WGS 84 decimal degrees from station_latitude; null when the upstream catalog omits coordinates.
- **`longitude`** (double or null, optional): Station longitude in WGS 84 decimal degrees from station_longitude; null when the upstream catalog omits coordinates.
- **`river_name`** (string or null, optional): River or water body name returned by KiWIS getStationList, used by consumers for hydrological grouping and map filtering.
- **`catchment_name`** (string or null, optional): Catchment or basin label returned by KiWIS getStationList, used for watershed-level filtering and analytics.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "kiwis_id": "string",
  "base_url": "string",
  "station_id": "string",
  "station_no": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0,
  "river_name": "string",
  "catchment_name": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Timeseries

CloudEvents type: `org.kiwis.Timeseries`

#### What it tells you

Reference metadata for one KiWIS timeseries returned by getTimeseriesList, including station linkage, parameter labels, units, and coverage range. Reference timeseries payload from KiWIS getTimeseriesList with station linkage, parameter labels, units, and coverage.

#### Identity

Each event identifies the real-world resource with `{kiwis_id}/{ts_id}`. `{kiwis_id}` is configuration-assigned identifier for the KiWIS endpoint/datasource; `{ts_id}` is stable KiWIS timeseries identifier returned by getTimeseriesList. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `kiwis`, key `{kiwis_id}/{ts_id}` |
| `MQTT/5.0` | topic `hydro/kiwis/{kiwis_id}/timeseries/{ts_id}/metadata`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/kiwis`, message subject `{kiwis_id}/{ts_id}` |

#### Payload

`Timeseries` payloads are JSON object. Required fields: `kiwis_id`, `base_url`, `ts_id`, `station_id`.

- **`kiwis_id`** (string, required): Configuration-assigned identifier for the KiWIS endpoint/datasource. It qualifies upstream identifiers because station_id and ts_id are unique only within a KiWIS datasource.
- **`base_url`** (uri, required): Base KiWIS queryServices URL used as the CloudEvents source and as provenance for records from this instance.
- **`ts_id`** (string, required): Stable KiWIS timeseries identifier returned by getTimeseriesList. It is globally unique within a KiWIS datasource and forms the key for metadata and value events.
- **`ts_name`** (string or null, optional): Full KiWIS timeseries name such as `15minute.Total` or `Day.Mean`, describing aggregation interval and statistic.
- **`ts_shortname`** (string or null, optional): Short KiWIS timeseries label returned by getTimeseriesList for compact displays and diagnostics.
- **`station_id`** (string, required): Stable station_id of the station owning this timeseries, enabling joins from timeseries metadata to station reference events.
- **`station_name`** (string or null, optional): Human-readable station name repeated by getTimeseriesList for operator convenience; consumers should use station_id for joins.
- **`parametertype_name`** (string or null, optional): KiWIS parameter type name such as level, discharge, precipitation, or temperature; identifies the physical quantity measured.
- **`stationparameter_name`** (string or null, optional): Station-specific parameter name returned by KiWIS, often the locally meaningful label such as Level or Rain.
- **`unit_name`** (string or null, optional): Per-timeseries unit name returned as ts_unitname, such as meter or millimeter. Units vary by timeseries and therefore travel as data fields rather than fixed schema units.
- **`unit_symbol`** (string or null, optional): Per-timeseries unit symbol returned as ts_unitsymbol, such as m, mm, m3/s, or deg C. Consumers use it to label numeric values correctly.
- **`coverage_from`** (datetime or null, optional): Start timestamp of the available coverage range reported by KiWIS getTimeseriesList. It is null when the server omits coverage.
- **`coverage_to`** (datetime or null, optional): End timestamp of the available coverage range reported by KiWIS getTimeseriesList. It is null when the server omits coverage.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "kiwis_id": "string",
  "base_url": "string",
  "ts_id": "string",
  "ts_name": "string",
  "ts_shortname": "string",
  "station_id": "string",
  "station_name": "string",
  "parametertype_name": "string",
  "stationparameter_name": "string",
  "unit_name": "string",
  "unit_symbol": "string",
  "coverage_from": "2024-01-01T00:00:00Z",
  "coverage_to": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Timeseries Value

CloudEvents type: `org.kiwis.TimeseriesValue`

#### What it tells you

One observation row returned by KiWIS getTimeseriesValues for a configured timeseries, carrying timestamp, numeric value, optional quality code, and the per-timeseries unit metadata needed by consumers. Telemetry payload for one KiWIS getTimeseriesValues row with value, quality code, and unit metadata copied from the timeseries catalog.

#### Identity

Each event identifies the real-world resource with `{kiwis_id}/{ts_id}`. `{kiwis_id}` is configuration-assigned identifier for the KiWIS endpoint/datasource; `{ts_id}` is stable KiWIS timeseries identifier returned by getTimeseriesList. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `kiwis`, key `{kiwis_id}/{ts_id}` |
| `MQTT/5.0` | topic `hydro/kiwis/{kiwis_id}/timeseries/{ts_id}/value`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/kiwis`, message subject `{kiwis_id}/{ts_id}` |

#### Payload

`Timeseries Value` payloads are JSON object. Required fields: `kiwis_id`, `base_url`, `ts_id`, `station_id`, `timestamp`.

- **`kiwis_id`** (string, required): Configuration-assigned identifier for the KiWIS endpoint/datasource. It qualifies upstream identifiers because station_id and ts_id are unique only within a KiWIS datasource.
- **`base_url`** (uri, required): Base KiWIS queryServices URL used as the CloudEvents source and as provenance for records from this instance.
- **`ts_id`** (string, required): Stable KiWIS timeseries identifier returned by getTimeseriesList. It is globally unique within a KiWIS datasource and forms the key for metadata and value events.
- **`station_id`** (string, required): Stable station_id of the station owning this timeseries, enabling joins from timeseries metadata to station reference events.
- **`timestamp`** (datetime, required): Observation timestamp from the Timestamp column returned by getTimeseriesValues, parsed as an instant in UTC when the upstream string ends in Z.
- **`value`** (double or null, optional): Numeric observation value from the Value column. It can be null for missing or censored measurements; use unit_name and unit_symbol to interpret magnitude.
- **`quality_code`** (int32 or null, optional): Optional KiWIS Quality Code column value. KiWIS instances use this integer to convey quality, approval, or processing flags; null means the response omitted the column or row value.
- **`unit_name`** (string or null, optional): Per-timeseries unit name returned as ts_unitname, such as meter or millimeter. Units vary by timeseries and therefore travel as data fields rather than fixed schema units.
- **`unit_symbol`** (string or null, optional): Per-timeseries unit symbol returned as ts_unitsymbol, such as m, mm, m3/s, or deg C. Consumers use it to label numeric values correctly.
- **`parametertype_name`** (string or null, optional): KiWIS parameter type name such as level, discharge, precipitation, or temperature; identifies the physical quantity measured.
- **`stationparameter_name`** (string or null, optional): Station-specific parameter name returned by KiWIS, often the locally meaningful label such as Level or Rain.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "kiwis_id": "string",
  "base_url": "string",
  "ts_id": "string",
  "station_id": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "value": 0,
  "quality_code": 0,
  "unit_name": "string",
  "unit_symbol": "string",
  "parametertype_name": "string",
  "stationparameter_name": "string"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/kiwis.xreg.json`](xreg/kiwis.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
