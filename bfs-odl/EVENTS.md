# BfS ODL — Ambient Gamma Dose Rate Monitoring Events

MQTT/5.0 transport variants of the BfS ODL CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under radiation/de/bfs/bfs-odl/{state}/{station_id}/... The {state} placeholder is derived from the station's AGS-based Kennziffer (first two digits map to a German Bundesland) and normalized to lowercase kebab-case before publishing.

## At a glance

- **Event types:** 2 documented event types (4 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `bfs-odl`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['bfs-odl'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `radiation/de/bfs/bfs-odl/+/+/info`, `radiation/de/bfs/bfs-odl/+/+/dose-rate`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('radiation/de/bfs/bfs-odl/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Station

CloudEvents type: `de.bfs.odl.Station`

#### What it tells you

Metadata for an ODL (Ortsdosisleistung) measuring station in the BfS gamma dose rate monitoring network. The BfS operates approximately 1,700 stationary probes across Germany that continuously measure ambient gamma dose rate. Station metadata includes the geographic position, elevation above sea level, postal code, and operational status of each probe.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is nine-digit station identifier (Kennziffer) assigned by BfS in the IMIS network. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `radiation/de/bfs/bfs-odl/{state}/{station_id}/info`, retain `true`, QoS `1` |
| `KAFKA` | topic `bfs-odl`, key `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `state`, `station_code`, `name`, `postal_code`, `site_status`, `site_status_text`, `kid`, `height_above_sea`, `longitude`, `latitude`.

- **`station_id`** (string, required): Nine-digit station identifier (Kennziffer) assigned by BfS in the IMIS network. Composed of the official municipality key (AGS) prefix and a station sequence number. Example: '033510091'. This is the stable key used for timeseries retrieval.
- **`state`** (string, required): German federal state (Bundesland) derived from the first two digits of the station Kennziffer (AGS prefix). Normalized to lowercase kebab-case for use as the {state} segment in the MQTT/UNS topic. Example: 'niedersachsen', 'bayern', 'nordrhein-westfalen'.
- **`station_code`** (string, required): Short alphanumeric station code assigned by BfS, consisting of a 'DEZ' prefix followed by a four-digit number. Example: 'DEZ0305'. Used in the BfS web interface and download area.
- **`name`** (string, required): Human-readable name of the station location, typically a German municipality or locality name. Example: 'Flensburg'.
- **`postal_code`** (string, required): German postal code (Postleitzahl / PLZ) of the station location. Five digits as a string.
- **`site_status`** (int32, required): Numeric operational status code. 1 = in operation (in Betrieb), 0 or other values indicate the station is decommissioned or under maintenance.
- **`site_status_text`** (string, required): Human-readable German text describing the operational status. Example: 'in Betrieb' (in operation).
- **`kid`** (int32, required): Numeric region identifier (Kreis-ID) used internally by BfS to group stations into geographic regions.
- **`height_above_sea`** (double or null, required, m): Elevation of the station above mean sea level in meters (Normalhöhennull / NHN). Determines the cosmic radiation component. Null if unknown.
- **`longitude`** (double, required, deg (°)): Longitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates.
- **`latitude`** (double, required, deg (°)): Latitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "state": "string",
  "station_code": "string",
  "name": "string",
  "postal_code": "string",
  "site_status": 0,
  "site_status_text": "string",
  "kid": 0,
  "height_above_sea": 0,
  "longitude": 0,
  "latitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Dose Rate Measurement

CloudEvents type: `de.bfs.odl.DoseRateMeasurement`

#### What it tells you

A one-hour averaged ambient gamma dose rate measurement from the BfS ODL monitoring network. Each measurement reports the gross gamma dose rate in microsieverts per hour (µSv/h), optionally split into cosmic and terrestrial components. The cosmic component originates from secondary cosmic radiation and depends primarily on altitude; the terrestrial component originates from naturally occurring radionuclides in the ground and varies with local geology.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is nine-digit station identifier (Kennziffer) of the measuring probe. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `radiation/de/bfs/bfs-odl/{state}/{station_id}/dose-rate`, retain `true`, QoS `1` |
| `KAFKA` | topic `bfs-odl`, key `{station_id}` |

#### Payload

`Dose Rate Measurement` payloads are JSON object. Required fields: `station_id`, `state`, `start_measure`, `end_measure`, `value`, `value_cosmic`, `value_terrestrial`, `validated`, `nuclide`.

- **`station_id`** (string, required): Nine-digit station identifier (Kennziffer) of the measuring probe. Matches the station_id in the Station schema.
- **`state`** (string, required): German federal state (Bundesland) derived from the station Kennziffer. Propagated from station catalog so subscribers can route by state without a catalog join. Used as the {state} segment of the MQTT/UNS topic.
- **`start_measure`** (string, required): Start of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T12:00:00Z'.
- **`end_measure`** (string, required): End of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T13:00:00Z'.
- **`value`** (double or null, required, uSv/h (µSv/h)): Gross ambient gamma dose rate averaged over the measurement period in microsieverts per hour (µSv/h). This is the total dose rate including both cosmic and terrestrial components. Null if the station did not report a valid measurement for this interval.
- **`value_cosmic`** (double or null, required, uSv/h (µSv/h)): Cosmic radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Estimated from the station's altitude using a standard model. Null when the BfS system has not yet computed the decomposition for this measurement.
- **`value_terrestrial`** (double or null, required, uSv/h (µSv/h)): Terrestrial radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Computed as gross value minus cosmic component. Varies with local geology (granite, basalt, sediment). Null when the cosmic component is not available.
- **`validated`** (int32, required): Data validation flag. 1 = the measurement has been validated by BfS quality control. 0 = the measurement is preliminary or unvalidated.
- **`nuclide`** (string, required): Nuclide identifier describing the type of radiation measured. For standard ODL probes this is always 'Gamma-ODL-Brutto' (gross gamma ambient dose rate).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "state": "string",
  "start_measure": "string",
  "end_measure": "string",
  "value": 0,
  "value_cosmic": 0,
  "value_terrestrial": 0,
  "validated": 0,
  "nuclide": "string"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/bfs_odl.xreg.json`](xreg/bfs_odl.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
