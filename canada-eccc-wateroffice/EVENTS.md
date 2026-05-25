# Canada ECCC Water Office Hydrometric Bridge Events

ECCC Water Office publishes real-time water level and flow observations from Environment and Climate Change Canada Water Survey of Canada for Canadian hydrometric stations. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `stations/{station_number}` identifies the resource each event is about.
- **Operations:** Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `canada-eccc-wateroffice`. The record key is `stations/{station_number}`. In plain language, `stations/{station_number}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['canada-eccc-wateroffice'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `CA.Gov.ECCC.Hydro.Station`

#### What it tells you

A reference record for one Canadian hydrometric station published by Environment and Climate Change Canada Water Survey of Canada. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events. Reference data for a Water Survey of Canada hydrometric monitoring station from the ECCC OGC API hydrometric-stations collection.

#### Identity

Each event identifies the real-world resource with `stations/{station_number}`. `{station_number}` is unique WSC station identifier following the scheme 2-digit major drainage area + letter + station digits, e.g. '05BJ004'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `canada-eccc-wateroffice`, key `stations/{station_number}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_number`, `station_name`, `prov_terr_state_loc`.

- **`station_number`** (string, required): Unique WSC station identifier following the scheme 2-digit major drainage area + letter + station digits, e.g. '05BJ004'. Upstream field: STATION_NUMBER.
- **`station_name`** (string, required): Official name of the hydrometric station, e.g. 'ELBOW RIVER AT BRAGG CREEK'. Upstream field: STATION_NAME.
- **`prov_terr_state_loc`** (string, required): Two-letter province, territory or state location code where the station is situated, e.g. 'AB' for Alberta. Upstream field: PROV_TERR_STATE_LOC.
- **`status_en`** (string or null, optional): Operational status of the station in English, e.g. 'Active', 'Discontinued'. Upstream field: STATUS_EN.
- **`contributor_en`** (string or null, optional): Name of the contributing agency responsible for operating this station in English, e.g. 'Water Survey of Canada'. Upstream field: CONTRIBUTOR_EN.
- **`drainage_area_gross`** (double or null, optional, square kilometre (km²)): Gross drainage area of the watershed upstream of this station in square kilometres. Upstream field: DRAINAGE_AREA_GROSS.
- **`drainage_area_effect`** (double or null, optional, square kilometre (km²)): Effective (contributing) drainage area of the watershed upstream of this station in square kilometres, excluding non-contributing areas. Upstream field: DRAINAGE_AREA_EFFECT.
- **`rhbn`** (boolean or null, optional): Indicates whether the station is part of the Reference Hydrometric Basin Network (RHBN), a subset of hydrologically stable, minimally disturbed basins used for climate change studies. Upstream field: RHBN.
- **`real_time`** (boolean or null, optional): Indicates whether real-time data are available for this station via the WSC real-time data service. Upstream field: REAL_TIME.
- **`latitude`** (double or null, optional, degree (°)): Geographic latitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.
- **`longitude`** (double or null, optional, degree (°)): Geographic longitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_number": "string",
  "station_name": "string",
  "prov_terr_state_loc": "string",
  "status_en": "string",
  "contributor_en": "string",
  "drainage_area_gross": 0,
  "drainage_area_effect": 0,
  "rhbn": false,
  "real_time": false,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Observation

CloudEvents type: `CA.Gov.ECCC.Hydro.Observation`

#### What it tells you

A current measurement from Environment and Climate Change Canada Water Survey of Canada for one monitoring site. It carries real-time water level and flow observations when the upstream feed reports a new or refreshed value. Real-time hydrometric observation from the ECCC OGC API hydrometric-realtime collection.

#### Identity

Each event identifies the real-world resource with `stations/{station_number}`. `{station_number}` is unique WSC station identifier, e.g. '05BJ004'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `canada-eccc-wateroffice`, key `stations/{station_number}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `station_number`, `identifier`, `station_name`, `prov_terr_state_loc`, `observation_datetime`.

- **`station_number`** (string, required): Unique WSC station identifier, e.g. '05BJ004'. Upstream field: STATION_NUMBER.
- **`identifier`** (string, required): Unique observation identifier composed of station number and ISO 8601 observation datetime, e.g. '05BJ004.2026-03-07T07:00:00Z'. Upstream field: IDENTIFIER.
- **`station_name`** (string, required): Official name of the hydrometric station. Upstream field: STATION_NAME.
- **`prov_terr_state_loc`** (string, required): Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC.
- **`observation_datetime`** (datetime, required): Timestamp of the observation in UTC. Upstream field: DATETIME.
- **`level`** (double or null, optional, metre (m)): Water level at the station gauge in metres above the station datum. Null when not measured or unavailable. Upstream field: LEVEL.
- **`discharge`** (double or null, optional, cubic metre per second (m³/s)): Water discharge (flow rate) at the station in cubic metres per second. Null when not measured or unavailable. Upstream field: DISCHARGE.
- **`latitude`** (double or null, optional, degree (°)): Geographic latitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.
- **`longitude`** (double or null, optional, degree (°)): Geographic longitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_number": "string",
  "identifier": "string",
  "station_name": "string",
  "prov_terr_state_loc": "string",
  "observation_datetime": "2024-01-01T00:00:00Z",
  "level": 0,
  "discharge": 0,
  "latitude": 0,
  "longitude": 0
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

- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/canada-eccc-wateroffice.xreg.json`](xreg/canada-eccc-wateroffice.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
