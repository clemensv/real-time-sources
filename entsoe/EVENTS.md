# ENTSO-E Transparency Platform Bridge Events

The **ENTSO-E Transparency Platform Bridge** polls the [ENTSO-E Transparency Platform REST API](https://transparency.entsoe.eu/) for European electricity market data and emits it as [CloudEvents](https://cloudevents.io/) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

## At a glance

- **Event types:** 11 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 11 telemetry event types.
- **Identity:** `{inDomain}`, `{inDomain}/{psrType}`, `{inDomain}/{outDomain}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `entsoe-transparency`. The record key is `{inDomain}`, `{inDomain}/{psrType}`, `{inDomain}/{outDomain}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['entsoe-transparency'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Day Ahead Prices

CloudEvents type: `eu.entsoe.transparency.DayAheadPrices`

#### What it tells you

This event carries day ahead prices data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}`. `{inDomain}` is EIC code of the bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}` |

#### Payload

`Day Ahead Prices` payloads are JSON object. Required fields: `inDomain`, `price`, `currency`, `unitName`, `resolution`, `documentType`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`price`** (double, required): Day-ahead price
- **`currency`** (string, required): Currency code (EUR)
- **`unitName`** (string, required): Price unit (MWH)
- **`resolution`** (string, required): ISO 8601 duration
- **`documentType`** (string, required): ENTSO-E document type code (A44)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "price": 0,
  "currency": "string",
  "unitName": "string",
  "resolution": "string",
  "documentType": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Actual Total Load

CloudEvents type: `eu.entsoe.transparency.ActualTotalLoad`

#### What it tells you

This event carries actual total load data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}`. `{inDomain}` is EIC code of the bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}` |

#### Payload

`Actual Total Load` payloads are JSON object. Required fields: `inDomain`, `quantity`, `resolution`, `documentType`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`quantity`** (double, required): Total load in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`outDomain`** (string, optional): EIC code of the out domain, if applicable
- **`documentType`** (string, required): ENTSO-E document type code (A65)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "quantity": 0,
  "resolution": "string",
  "outDomain": "string",
  "documentType": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Load Forecast Margin

CloudEvents type: `eu.entsoe.transparency.LoadForecastMargin`

#### What it tells you

This event carries load forecast margin data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}`. `{inDomain}` is EIC code of the bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}` |

#### Payload

`Load Forecast Margin` payloads are JSON object. Required fields: `inDomain`, `quantity`, `resolution`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`quantity`** (double, required): Forecast margin in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`documentType`** (string, required): ENTSO-E document type code (A70)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "quantity": 0,
  "resolution": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Generation Forecast

CloudEvents type: `eu.entsoe.transparency.GenerationForecast`

#### What it tells you

This event carries generation forecast data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}`. `{inDomain}` is EIC code of the bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}` |

#### Payload

`Generation Forecast` payloads are JSON object. Required fields: `inDomain`, `quantity`, `resolution`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`quantity`** (double, required): Forecast total generation in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`documentType`** (string, required): ENTSO-E document type code (A71)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "quantity": 0,
  "resolution": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Reservoir Filling Information

CloudEvents type: `eu.entsoe.transparency.ReservoirFillingInformation`

#### What it tells you

This event carries reservoir filling information data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}`. `{inDomain}` is EIC code of the bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}` |

#### Payload

`Reservoir Filling Information` payloads are JSON object. Required fields: `inDomain`, `quantity`, `resolution`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`quantity`** (double, required): Stored energy in MWh
- **`resolution`** (string, required): ISO 8601 duration
- **`documentType`** (string, required): ENTSO-E document type code (A72)
- **`unitName`** (string, required): Unit of measurement
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "quantity": 0,
  "resolution": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Actual Generation

CloudEvents type: `eu.entsoe.transparency.ActualGeneration`

#### What it tells you

This event carries actual generation data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}`. `{inDomain}` is EIC code of the bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}` |

#### Payload

`Actual Generation` payloads are JSON object. Required fields: `inDomain`, `quantity`, `resolution`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`quantity`** (double, required): Total actual generation in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`documentType`** (string, required): ENTSO-E document type code (A73)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "quantity": 0,
  "resolution": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Actual Generation Per Type

CloudEvents type: `eu.entsoe.transparency.ActualGenerationPerType`

#### What it tells you

This event carries actual generation per type data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}/{psrType}`. `{inDomain}` is EIC code of the bidding zone; `{psrType}` is production type code (B01=Biomass, B02=Lignite, ...). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}/{psrType}` |

#### Payload

`Actual Generation Per Type` payloads are JSON object. Required fields: `inDomain`, `psrType`, `quantity`, `resolution`, `businessType`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`psrType`** (string, required): Production type code (B01=Biomass, B02=Lignite, ...)
- **`quantity`** (double, required): Generated power in MW
- **`resolution`** (string, required): ISO 8601 duration (PT15M, PT60M)
- **`businessType`** (string, required): Business type code
- **`documentType`** (string, required): ENTSO-E document type code (A75)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "psrType": "string",
  "quantity": 0,
  "resolution": "string",
  "businessType": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wind Solar Forecast

CloudEvents type: `eu.entsoe.transparency.WindSolarForecast`

#### What it tells you

This event carries wind solar forecast data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}/{psrType}`. `{inDomain}` is EIC code of the bidding zone; `{psrType}` is production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}/{psrType}` |

#### Payload

`Wind Solar Forecast` payloads are JSON object. Required fields: `inDomain`, `psrType`, `quantity`, `resolution`, `businessType`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`psrType`** (string, required): Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore)
- **`quantity`** (double, required): Forecast power in MW
- **`resolution`** (string, required): ISO 8601 duration (PT15M, PT60M)
- **`businessType`** (string, required): Business type code
- **`documentType`** (string, required): ENTSO-E document type code (A69)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "psrType": "string",
  "quantity": 0,
  "resolution": "string",
  "businessType": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wind Solar Generation

CloudEvents type: `eu.entsoe.transparency.WindSolarGeneration`

#### What it tells you

This event carries wind solar generation data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}/{psrType}`. `{inDomain}` is EIC code of the bidding zone; `{psrType}` is production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}/{psrType}` |

#### Payload

`Wind Solar Generation` payloads are JSON object. Required fields: `inDomain`, `psrType`, `quantity`, `resolution`, `businessType`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`psrType`** (string, required): Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore)
- **`quantity`** (double, required): Actual wind/solar generation in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`businessType`** (string, required): Business type code
- **`documentType`** (string, required): ENTSO-E document type code (A74)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "psrType": "string",
  "quantity": 0,
  "resolution": "string",
  "businessType": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Installed Generation Capacity Per Type

CloudEvents type: `eu.entsoe.transparency.InstalledGenerationCapacityPerType`

#### What it tells you

This event carries installed generation capacity per type data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}/{psrType}`. `{inDomain}` is EIC code of the bidding zone; `{psrType}` is production type code (B01=Biomass, B02=Lignite, ...). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}/{psrType}` |

#### Payload

`Installed Generation Capacity Per Type` payloads are JSON object. Required fields: `inDomain`, `psrType`, `quantity`, `resolution`, `businessType`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the bidding zone
- **`psrType`** (string, required): Production type code (B01=Biomass, B02=Lignite, ...)
- **`quantity`** (double, required): Installed capacity in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`businessType`** (string, required): Business type code
- **`documentType`** (string, required): ENTSO-E document type code (A68)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "psrType": "string",
  "quantity": 0,
  "resolution": "string",
  "businessType": "string",
  "documentType": "string",
  "unitName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Cross Border Physical Flows

CloudEvents type: `eu.entsoe.transparency.CrossBorderPhysicalFlows`

#### What it tells you

This event carries cross border physical flows data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{inDomain}/{outDomain}`. `{inDomain}` is EIC code of the importing bidding zone; `{outDomain}` is EIC code of the exporting bidding zone. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `entsoe-transparency`, key `{inDomain}/{outDomain}` |

#### Payload

`Cross Border Physical Flows` payloads are JSON object. Required fields: `inDomain`, `outDomain`, `quantity`, `resolution`, `documentType`, `unitName`.

- **`inDomain`** (string, required): EIC code of the importing bidding zone
- **`outDomain`** (string, required): EIC code of the exporting bidding zone
- **`quantity`** (double, required): Physical flow in MW
- **`resolution`** (string, required): ISO 8601 duration
- **`documentType`** (string, required): ENTSO-E document type code (A11)
- **`unitName`** (string, required): Unit of measurement (MAW)
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "inDomain": "string",
  "outDomain": "string",
  "quantity": 0,
  "resolution": "string",
  "documentType": "string",
  "unitName": "string"
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

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/entsoe.xreg.json`](xreg/entsoe.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- ENTSO-E Transparency Platform REST API: <https://transparency.entsoe.eu/>
- Transparency Platform RESTful API Guide: <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>
