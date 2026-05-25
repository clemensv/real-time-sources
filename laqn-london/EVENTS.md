# LAQN London Air Quality Network Events

The LAQN London Air Quality Network bridge polls the public LAQN API operated by King's College London and emits structured JSON CloudEvents to Kafka. It keeps the upstream split intact: site metadata, species metadata, hourly site measurements, and Daily Air Quality Index bulletin records.

## At a glance

- **Event types:** 4 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 4 telemetry event types.
- **Identity:** `{site_code}`, `{species_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `laqn-london`. The record key is `{site_code}`, `{species_code}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['laqn-london'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Site

CloudEvents type: `uk.kcl.laqn.Site`

#### What it tells you

LAQN monitoring site reference data, including stable site identity, operator information, and WGS84 coordinates. Reference description of a London Air Quality Network monitoring site, including its stable code, operator metadata, and WGS84 coordinates.

#### Identity

Each event identifies the real-world resource with `{site_code}`. `{site_code}` is stable LAQN site code that identifies the monitoring site, such as BX1. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `laqn-london`, key `{site_code}` |

#### Payload

`Site` payloads are JSON object. Required fields: `site_code`, `site_name`, `site_type`, `local_authority_code`, `local_authority_name`, `latitude`, `longitude`, `date_opened`, `date_closed`, `data_owner`, `data_manager`.

- **`site_code`** (string, required): Stable LAQN site code that identifies the monitoring site, such as BX1.
- **`site_name`** (string, required): Human-readable LAQN site name published for the monitoring site.
- **`site_type`** (enum, required): Site classification published by LAQN, such as Suburban, Kerbside, Roadside, Urban Background, Industrial, Rural, or other.
- **`local_authority_code`** (string, required): Stable local authority code associated with the site in the LAQN reference data.
- **`local_authority_name`** (string, required): Human-readable local authority name associated with the site in the LAQN reference data.
- **`latitude`** (double or null, required): WGS84 latitude of the monitoring site in decimal degrees. This bridge uses the decimal latitude field, not the projected WGS84 metre coordinate, or null when the upstream site record leaves the coordinate blank.
- **`longitude`** (double or null, required): WGS84 longitude of the monitoring site in decimal degrees. This bridge uses the decimal longitude field, not the projected WGS84 metre coordinate, or null when the upstream site record leaves the coordinate blank.
- **`date_opened`** (string, required): Date and time when the site opened, as published by LAQN in YYYY-MM-DD HH:MM:SS format.
- **`date_closed`** (string or null, required): Date and time when the site closed in YYYY-MM-DD HH:MM:SS format, or null when the site is still active and no closure date is published.
- **`data_owner`** (string, required): Organisation listed by LAQN as the owner of the site's data.
- **`data_manager`** (string, required): Organisation listed by LAQN as the manager of the monitoring site data.
##### `site_type` values

- `Suburban`
- `Kerbside`
- `Roadside`
- `Urban Background`
- `Industrial`
- `Rural`
- `other`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_code": "string",
  "site_name": "string",
  "site_type": "Suburban",
  "local_authority_code": "string",
  "local_authority_name": "string",
  "latitude": 0,
  "longitude": 0,
  "date_opened": "string",
  "date_closed": "string",
  "data_owner": "string",
  "data_manager": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Measurement

CloudEvents type: `uk.kcl.laqn.Measurement`

#### What it tells you

LAQN hourly pollutant measurement for a site and species at a GMT timestamp. Hourly air quality measurement for a LAQN site and pollutant species at a GMT timestamp.

#### Identity

Each event identifies the real-world resource with `{site_code}`. `{site_code}` is stable LAQN site code for the monitoring site that produced the measurement. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `laqn-london`, key `{site_code}` |

#### Payload

`Measurement` payloads are JSON object. Required fields: `site_code`, `species_code`, `measurement_date_gmt`, `value`.

- **`site_code`** (string, required): Stable LAQN site code for the monitoring site that produced the measurement.
- **`species_code`** (string, required): Stable LAQN pollutant code for the measured species.
- **`measurement_date_gmt`** (string, required): Measurement timestamp in GMT, encoded by LAQN as YYYY-MM-DD HH:MM:SS.
- **`value`** (double, required): Measured pollutant concentration as a decimal number. The bridge omits records for timestamps where the upstream API reports an empty value.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_code": "string",
  "species_code": "string",
  "measurement_date_gmt": "string",
  "value": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Daily Index

CloudEvents type: `uk.kcl.laqn.DailyIndex`

#### What it tells you

LAQN Daily Air Quality Index (DAQI) for a site and pollutant, published as the latest London-wide bulletin. Daily Air Quality Index bulletin record for a LAQN site and pollutant species within the latest London-wide index publication.

#### Identity

Each event identifies the real-world resource with `{site_code}`. `{site_code}` is stable LAQN site code for the monitoring site to which the daily index applies. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `laqn-london`, key `{site_code}` |

#### Payload

`Daily Index` payloads are JSON object. Required fields: `site_code`, `bulletin_date`, `species_code`, `air_quality_index`, `air_quality_band`, `index_source`.

- **`site_code`** (string, required): Stable LAQN site code for the monitoring site to which the daily index applies.
- **`bulletin_date`** (string, required): Bulletin date and time published by LAQN for the daily index, encoded as YYYY-MM-DD HH:MM:SS.
- **`species_code`** (string, required): Stable LAQN pollutant code for the species to which the daily index applies.
- **`air_quality_index`** (integer, required): LAQN Daily Air Quality Index value from 1 to 10, where 1 to 3 is Low, 4 to 6 is Moderate, 7 to 9 is High, and 10 is Very High. Constraints: minimum `1`, maximum `10`.
- **`air_quality_band`** (enum, required): Textual Daily Air Quality Index band published by LAQN: Low, Moderate, High, or Very High.
- **`index_source`** (enum, required): Origin of the daily index published by LAQN, typically Measurement or Forecast.
##### `air_quality_band` values

- `Low`
- `Moderate`
- `High`
- `Very High`
##### `index_source` values

- `Measurement`
- `Forecast`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_code": "string",
  "bulletin_date": "string",
  "species_code": "string",
  "air_quality_index": 0,
  "air_quality_band": "Low",
  "index_source": "Measurement"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Species

CloudEvents type: `uk.kcl.laqn.Species`

#### What it tells you

LAQN pollutant reference data, including descriptive text and health guidance for a pollutant code. Reference description of a LAQN pollutant species, including explanatory text and health impact guidance.

#### Identity

Each event identifies the real-world resource with `{species_code}`. `{species_code}` is stable LAQN pollutant code, such as NO2, PM10, PM25, O3, SO2, or CO. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `laqn-london`, key `{species_code}` |

#### Payload

`Species` payloads are JSON object. Required fields: `species_code`, `species_name`, `description`, `health_effect`, `link`.

- **`species_code`** (string, required): Stable LAQN pollutant code, such as NO2, PM10, PM25, O3, SO2, or CO.
- **`species_name`** (string, required): Human-readable pollutant name published by LAQN for the pollutant code.
- **`description`** (string, required): LAQN explanatory description of the pollutant and how it is formed or encountered.
- **`health_effect`** (string, required): LAQN health effect guidance describing the health impacts associated with exposure to the pollutant.
- **`link`** (string, required): HTTP URL to the LAQN or LondonAir guidance page with more detailed information about the pollutant.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "species_code": "string",
  "species_name": "string",
  "description": "string",
  "health_effect": "string",
  "link": "string"
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/laqn_london.xreg.json`](xreg/laqn_london.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
