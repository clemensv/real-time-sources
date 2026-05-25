# Carbon Intensity UK Events

MQTT/5.0 transport variants for National Grid Carbon Intensity events. Non-retained QoS-1 event topics route by GB national/regional area under energy/gb/national-grid/carbon-intensity/{region}/..., where national records use region=national and DNO region records use stable, version-pinned region slugs keyed by region_id such as north-scotland.

## At a glance

- **Event types:** 3 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{period_from}`, `{region_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `carbon-intensity`. The record key is `{period_from}`, `{region_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['carbon-intensity'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `energy/gb/national-grid/carbon-intensity/+/intensity`, `energy/gb/national-grid/carbon-intensity/+/generation-mix`, `energy/gb/national-grid/carbon-intensity/+/regional-intensity`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('energy/gb/national-grid/carbon-intensity/+/intensity', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Intensity

CloudEvents type: `uk.org.carbonintensity.Intensity`

#### What it tells you

National half-hourly carbon intensity for the Great Britain electricity grid, published by National Grid ESO. Contains the forecast and actual carbon dioxide emission intensity in grams of CO2 per kilowatt-hour, along with a qualitative index band.

#### Identity

Each event identifies the real-world resource with `{period_from}`. `{period_from}` is ISO 8601 UTC timestamp marking the start of the half-hour settlement period (e.g. 2026-04-06T09:30Z). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `carbon-intensity`, key `{period_from}` |
| `MQTT/5.0` | topic `energy/gb/national-grid/carbon-intensity/{region}/intensity`, retain `false`, QoS `1` |

#### Payload

`Intensity` payloads are JSON object. Required fields: `period_from`, `period_to`, `region`, `ce_id`.

- **`period_from`** (datetime, required): ISO 8601 UTC timestamp marking the start of the half-hour settlement period (e.g. 2026-04-06T09:30Z).
- **`period_to`** (datetime, required): ISO 8601 UTC timestamp marking the end of the half-hour settlement period (e.g. 2026-04-06T10:00Z).
- **`forecast`** (int32 or null, optional, gCO2/kWh): Forecast carbon intensity for this settlement period in grams of CO2 per kilowatt-hour (gCO2/kWh), computed ahead of real-time by National Grid ESO.
- **`actual`** (int32 or null, optional, gCO2/kWh): Actual (metered) carbon intensity for this settlement period in grams of CO2 per kilowatt-hour (gCO2/kWh). May be null when the period has not yet completed.
- **`index`** (string or null, optional): Qualitative index band for the carbon intensity: one of 'very low', 'low', 'moderate', 'high', or 'very high'.
- **`region`** (string, required): Topic-safe MQTT/UNS region segment. National GB-wide records use the literal national.
- **`ce_id`** (string, required): Deterministic CloudEvents id for subscriber deduplication, composed from settlement period, national region, and event leaf.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "period_from": "2024-01-01T00:00:00Z",
  "period_to": "2024-01-01T00:00:00Z",
  "forecast": 0,
  "actual": 0,
  "index": "string",
  "region": "string",
  "ce_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Generation Mix

CloudEvents type: `uk.org.carbonintensity.GenerationMix`

#### What it tells you

National half-hourly electricity generation fuel mix for Great Britain, published by National Grid ESO. Each field represents the percentage contribution of a specific fuel type to total generation during the settlement period.

#### Identity

Each event identifies the real-world resource with `{period_from}`. `{period_from}` is ISO 8601 UTC timestamp marking the start of the half-hour settlement period. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `carbon-intensity`, key `{period_from}` |
| `MQTT/5.0` | topic `energy/gb/national-grid/carbon-intensity/{region}/generation-mix`, retain `false`, QoS `1` |

#### Payload

`Generation Mix` payloads are JSON object. Required fields: `period_from`, `period_to`, `region`, `ce_id`.

- **`period_from`** (datetime, required): ISO 8601 UTC timestamp marking the start of the half-hour settlement period.
- **`period_to`** (datetime, required): ISO 8601 UTC timestamp marking the end of the half-hour settlement period.
- **`biomass_pct`** (double or null, optional, %): Percentage of electricity generated from biomass (wood pellets, energy crops, and other organic matter) during this settlement period.
- **`coal_pct`** (double or null, optional, %): Percentage of electricity generated from coal-fired power stations during this settlement period.
- **`gas_pct`** (double or null, optional, %): Percentage of electricity generated from natural gas (CCGT and OCGT) during this settlement period.
- **`hydro_pct`** (double or null, optional, %): Percentage of electricity generated from hydroelectric power stations during this settlement period.
- **`imports_pct`** (double or null, optional, %): Percentage of electricity supplied via interconnector imports from continental Europe and Ireland during this settlement period.
- **`nuclear_pct`** (double or null, optional, %): Percentage of electricity generated from nuclear power stations during this settlement period.
- **`oil_pct`** (double or null, optional, %): Percentage of electricity generated from oil-fired power stations during this settlement period.
- **`other_pct`** (double or null, optional, %): Percentage of electricity generated from other or unclassified fuel sources during this settlement period.
- **`solar_pct`** (double or null, optional, %): Percentage of electricity generated from solar photovoltaic installations during this settlement period.
- **`wind_pct`** (double or null, optional, %): Percentage of electricity generated from onshore and offshore wind turbines during this settlement period.
- **`region`** (string, required): Topic-safe MQTT/UNS region segment. National GB-wide records use the literal national.
- **`ce_id`** (string, required): Deterministic CloudEvents id for subscriber deduplication, composed from settlement period, national region, and event leaf.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "period_from": "2024-01-01T00:00:00Z",
  "period_to": "2024-01-01T00:00:00Z",
  "biomass_pct": 0,
  "coal_pct": 0,
  "gas_pct": 0,
  "hydro_pct": 0,
  "imports_pct": 0,
  "nuclear_pct": 0,
  "oil_pct": 0,
  "other_pct": 0,
  "solar_pct": 0,
  "wind_pct": 0,
  "region": "string",
  "ce_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Regional Intensity

CloudEvents type: `uk.org.carbonintensity.RegionalIntensity`

#### What it tells you

Half-hourly carbon intensity and generation mix for one of the 17 GB Distribution Network Operator (DNO) regions, published by National Grid ESO. Each record covers a specific DNO region identified by its numeric region ID.

#### Identity

Each event identifies the real-world resource with `{region_id}`. `{region_id}` is numeric identifier for the DNO region as assigned by the Carbon Intensity API (1-17). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `carbon-intensity`, key `{region_id}` |
| `MQTT/5.0` | topic `energy/gb/national-grid/carbon-intensity/{region}/regional-intensity`, retain `false`, QoS `1` |

#### Payload

`Regional Intensity` payloads are JSON object. Required fields: `region_id`, `dnoregion`, `shortname`, `period_from`, `period_to`, `region`, `ce_id`.

- **`region_id`** (int32, required): Numeric identifier for the DNO region as assigned by the Carbon Intensity API (1-17).
- **`dnoregion`** (string, required): Full name of the Distribution Network Operator region (e.g. 'Scottish Hydro Electric Power Distribution').
- **`shortname`** (string, required): Short display name for the DNO region (e.g. 'North Scotland').
- **`period_from`** (datetime, required): ISO 8601 UTC timestamp marking the start of the half-hour settlement period.
- **`period_to`** (datetime, required): ISO 8601 UTC timestamp marking the end of the half-hour settlement period.
- **`forecast`** (int32 or null, optional, gCO2/kWh): Forecast carbon intensity for this region and settlement period in grams of CO2 per kilowatt-hour (gCO2/kWh).
- **`index`** (string or null, optional): Qualitative index band for the regional carbon intensity: one of 'very low', 'low', 'moderate', 'high', or 'very high'.
- **`biomass_pct`** (double or null, optional, %): Percentage of electricity generated from biomass in this region during this settlement period.
- **`coal_pct`** (double or null, optional, %): Percentage of electricity generated from coal in this region during this settlement period.
- **`gas_pct`** (double or null, optional, %): Percentage of electricity generated from natural gas in this region during this settlement period.
- **`hydro_pct`** (double or null, optional, %): Percentage of electricity generated from hydroelectric power in this region during this settlement period.
- **`imports_pct`** (double or null, optional, %): Percentage of electricity supplied via interconnector imports in this region during this settlement period.
- **`nuclear_pct`** (double or null, optional, %): Percentage of electricity generated from nuclear power in this region during this settlement period.
- **`oil_pct`** (double or null, optional, %): Percentage of electricity generated from oil in this region during this settlement period.
- **`other_pct`** (double or null, optional, %): Percentage of electricity generated from other or unclassified fuel sources in this region during this settlement period.
- **`solar_pct`** (double or null, optional, %): Percentage of electricity generated from solar photovoltaic installations in this region during this settlement period.
- **`wind_pct`** (double or null, optional, %): Percentage of electricity generated from wind turbines in this region during this settlement period.
- **`region`** (string, required): Stable topic-safe MQTT/UNS region segment from the version-pinned DNO region_id lookup table, for example north-scotland for region_id 1. Falls back to region-{region_id} if an unknown future id appears.
- **`ce_id`** (string, required): Deterministic CloudEvents id for subscriber deduplication, composed from settlement period, DNO region_id, and regional-intensity leaf.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region_id": 0,
  "dnoregion": "string",
  "shortname": "string",
  "period_from": "2024-01-01T00:00:00Z",
  "period_to": "2024-01-01T00:00:00Z",
  "forecast": 0,
  "index": "string",
  "biomass_pct": 0,
  "coal_pct": 0,
  "gas_pct": 0,
  "hydro_pct": 0,
  "imports_pct": 0,
  "nuclear_pct": 0,
  "oil_pct": 0,
  "other_pct": 0,
  "solar_pct": 0,
  "wind_pct": 0,
  "region": "string",
  "ce_id": "string"
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

## References

- xRegistry manifest: [`xreg/carbon_intensity.xreg.json`](xreg/carbon_intensity.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- National Grid ESO Carbon Intensity API: <https://api.carbonintensity.org.uk/>
