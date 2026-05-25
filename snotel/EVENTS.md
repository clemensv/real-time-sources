# USDA NRCS SNOTEL Snow and Weather Bridge Events

A real-time data bridge that fetches hourly snow and weather observations from the USDA Natural Resources Conservation Service (NRCS) SNOTEL (SNOwpack TELemetry) network and produces them as CloudEvents to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_triplet}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `snotel`. The record key is `{station_triplet}`. In plain language, `{station_triplet}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['snotel'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `gov.usda.nrcs.snotel.Station`

#### What it tells you

Reference metadata for a USDA NRCS SNOTEL (SNOwpack TELemetry) station. SNOTEL is an automated system of over 900 snowpack monitoring sites in the western United States and Alaska operated by the Natural Resources Conservation Service. Each station reports snowpack, precipitation, and temperature data via satellite telemetry.

#### Identity

Each event identifies the real-world resource with `{station_triplet}`. `{station_triplet}` is SNOTEL station triplet identifier in the format '{stationId}:{stateCode}:SNTL'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `snotel`, key `{station_triplet}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_triplet`, `name`, `state`, `elevation`, `latitude`, `longitude`.

- **`station_triplet`** (string, required): SNOTEL station triplet identifier in the format '{stationId}:{stateCode}:SNTL'. This is the canonical identifier used by the USDA NRCS Water and Climate Center to uniquely reference each SNOTEL site (e.g. '838:CO:SNTL' for University Camp, Colorado).
- **`name`** (string, required): Human-readable station name assigned by the USDA NRCS (e.g. 'University Camp', 'Berthoud Summit'). Station names are generally geographic references to the site location.
- **`state`** (string, required): Two-letter US state or territory code where the station is located (e.g. 'CO', 'AK', 'MT'). Stations are distributed across the western United States and Alaska.
- **`elevation`** (double, required, [ft_i] (ft)): Station elevation above sea level. Reported by the NRCS in feet. SNOTEL stations are typically located at high elevations in mountainous terrain to monitor snowpack.
- **`latitude`** (double, required): Latitude of the SNOTEL station in decimal degrees north. All SNOTEL stations are in the northern hemisphere (positive values).
- **`longitude`** (double, required): Longitude of the SNOTEL station in decimal degrees east. Western US stations have negative values indicating west of the Prime Meridian.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_triplet": "string",
  "name": "string",
  "state": "string",
  "elevation": 0,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Snow Observation

CloudEvents type: `gov.usda.nrcs.snotel.SnowObservation`

#### What it tells you

Hourly snow and weather observation from a USDA NRCS SNOTEL station. Each record represents one hourly reading transmitted via satellite telemetry from an automated high-elevation monitoring site. The observation includes Snow Water Equivalent (the primary hydrologic measurement), snow depth, accumulated precipitation, and air temperature.

#### Identity

Each event identifies the real-world resource with `{station_triplet}`. `{station_triplet}` is SNOTEL station triplet identifier in the format '{stationId}:{stateCode}:SNTL'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `snotel`, key `{station_triplet}` |

#### Payload

`Snow Observation` payloads are JSON object. Required fields: `station_triplet`, `date_time`.

- **`station_triplet`** (string, required): SNOTEL station triplet identifier in the format '{stationId}:{stateCode}:SNTL'. Links this observation to the station that reported it.
- **`date_time`** (datetime, required): Observation timestamp reported by the SNOTEL station. Hourly readings are transmitted via satellite telemetry, typically at the top of each hour. The time is in the station's local standard time as reported by the NRCS Report Generator.
- **`snow_water_equivalent`** (double or null, optional, [in_i] (in)): Snow Water Equivalent (SWE) — the depth of water that would theoretically result if the entire snowpack were melted instantaneously. Measured by a snow pillow sensor at the station. This is the primary measurement for water supply forecasting. Reported in inches.
- **`snow_depth`** (double or null, optional, [in_i] (in)): Total snow depth measured by an ultrasonic depth sensor mounted above the snow surface. Reported in inches. Can fluctuate due to settling, wind redistribution, and measurement noise.
- **`precipitation`** (double or null, optional, [in_i] (in)): Water-year accumulated precipitation measured by a storage-type precipitation gauge. The accumulation resets on October 1 (start of the water year). Reported in inches. Values are cumulative and should be monotonically increasing within a water year.
- **`air_temperature`** (double or null, optional, [degF] (°F)): Instantaneously observed air temperature at the station. SNOTEL air temperature data contains a known bias rooted in the sensor conversion equation that varies through the output range; see the NRCS Air Temperature Bias Correction documentation. Reported in degrees Fahrenheit.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_triplet": "string",
  "date_time": "2024-01-01T00:00:00Z",
  "snow_water_equivalent": 0,
  "snow_depth": 0,
  "precipitation": 0,
  "air_temperature": 0
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

- xRegistry manifest: [`xreg/snotel.xreg.json`](xreg/snotel.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
