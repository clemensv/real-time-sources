# EURDEP Radiation Events

Bridge for the **EURDEP (European Radiological Data Exchange Platform)** pan-European ambient gamma dose rate monitoring network.

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

Subscribe to `eurdep-radiation`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['eurdep-radiation'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `eu.jrc.eurdep.Station`

#### What it tells you

Reference metadata for an ambient gamma dose rate monitoring station in the EURDEP (European Radiological Data Exchange Platform) network. EURDEP aggregates data from approximately 5,500 stations across 39 European countries. Each station continuously measures ambient gamma dose rate and reports hourly averaged values.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is alphanumeric station identifier assigned within the EURDEP network. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `eurdep-radiation`, key `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `name`, `country_code`, `latitude`, `longitude`, `height_above_sea`, `site_status`, `site_status_text`.

- **`station_id`** (string, required): Alphanumeric station identifier assigned within the EURDEP network. The first two characters are the ISO 3166-1 alpha-2 country code of the operating country, followed by a numeric station sequence. Example: 'AT0001' (Austria), 'DE0123' (Germany), 'FR0456' (France). This is the stable key used for data retrieval and cross-referencing.
- **`name`** (string, required): Human-readable name of the station location, typically a city or locality name. Example: 'Laa/ThayaAMS'.
- **`country_code`** (string, required): ISO 3166-1 alpha-2 country code extracted from the first two characters of the station_id. Identifies the country operating the monitoring station. Example: 'AT' for Austria, 'DE' for Germany, 'CZ' for Czech Republic.
- **`latitude`** (double, required, deg (°)): Latitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates returned by the WFS endpoint.
- **`longitude`** (double, required, deg (°)): Longitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates returned by the WFS endpoint.
- **`height_above_sea`** (double or null, required, m): Elevation of the station above mean sea level in meters. Determines the cosmic radiation component contribution. Null if the elevation is not reported by the national network.
- **`site_status`** (int32, required): Numeric operational status code of the station. 1 = active and reporting, other values indicate the station is inactive, under maintenance, or decommissioned.
- **`site_status_text`** (string, required): Human-readable text describing the operational status of the station. Language depends on the reporting country. Example: 'in Betrieb' (German for 'in operation').
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "country_code": "string",
  "latitude": 0,
  "longitude": 0,
  "height_above_sea": 0,
  "site_status": 0,
  "site_status_text": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Dose Rate Reading

CloudEvents type: `eu.jrc.eurdep.DoseRateReading`

#### What it tells you

An ambient gamma dose rate reading from a EURDEP monitoring station. Each reading reports the gross gamma dose rate in microsieverts per hour (µSv/h) averaged over a one-hour measurement window. Readings include validation status, the nuclide type measured, measurement duration, and the analysis time range.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is alphanumeric station identifier from the EURDEP network. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `eurdep-radiation`, key `{station_id}` |

#### Payload

`Dose Rate Reading` payloads are JSON object. Required fields: `station_id`, `name`, `value`, `unit`, `start_measure`, `end_measure`, `nuclide`, `duration`, `validated`.

- **`station_id`** (string, required): Alphanumeric station identifier from the EURDEP network. Matches the station_id in the Station schema. Example: 'AT0001'.
- **`name`** (string, required): Human-readable name of the station location. Included for convenience so readings are self-describing without a Station reference join.
- **`value`** (double or null, required, uSv/h (µSv/h)): Gross ambient gamma dose rate averaged over the measurement period in microsieverts per hour (µSv/h). Null if the station did not report a valid measurement for this interval.
- **`unit`** (string, required): Unit of the dose rate value as reported by the upstream EURDEP system. Typically 'µSv/h' (microsieverts per hour), though encoding artifacts may appear in the raw API response.
- **`start_measure`** (string, required): Start of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-08T19:00:00Z'.
- **`end_measure`** (string, required): End of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-08T20:00:00Z'.
- **`nuclide`** (string, required): Nuclide identifier describing the type of radiation measured. For standard gamma dose rate probes this is 'Gamma-ODL-Brutto' (gross gamma ambient dose rate).
- **`duration`** (string, required): Measurement integration period as reported by the upstream system. Example: '1h' for one hour.
- **`validated`** (int32, required): Data validation status flag. 0 = not validated, 1 = validated by national authority, 2 = validated by EURDEP system. Higher values indicate stronger quality assurance.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "value": 0,
  "unit": "string",
  "start_measure": "string",
  "end_measure": "string",
  "nuclide": "string",
  "duration": "string",
  "validated": 0
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

- xRegistry manifest: [`xreg/eurdep_radiation.xreg.json`](xreg/eurdep_radiation.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
