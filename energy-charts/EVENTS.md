# Energy-Charts (Fraunhofer ISE) — European Electricity Data Bridge Events

This bridge polls the [Energy-Charts API](https://api.energy-charts.info/) operated by Fraunhofer ISE and forwards European electricity generation, price, and grid carbon signal data to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

## At a glance

- **Event types:** 3 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{country}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `energy-charts`. The record key is `{country}`. In plain language, `{country}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['energy-charts'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Public Power

CloudEvents type: `info.energy_charts.PublicPower`

#### What it tells you

Net electricity generation by fuel type for a given country at a specific 15-minute interval. Sourced from the Energy-Charts /public_power endpoint (Fraunhofer ISE) which aggregates ENTSO-E transparency platform data. Each record represents one timestamp in the parallel-array response, with individual production types flattened into named fields in megawatts (MW).

#### Identity

Each event identifies the real-world resource with `{country}`. `{country}` is ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany, 'fr' for France). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `energy-charts`, key `{country}` |

#### Payload

`Public Power` payloads are JSON object. Required fields: `country`, `timestamp`, `unix_seconds`.

- **`country`** (string, required): ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany, 'fr' for France). Used as the query parameter in the Energy-Charts API.
- **`timestamp`** (datetime, required): UTC timestamp derived from the unix_seconds value. Marks the start of the 15-minute measurement interval.
- **`unix_seconds`** (int64, required): Unix epoch timestamp in seconds as returned by the Energy-Charts API. Each value corresponds to one row in the parallel arrays of production_types.
- **`hydro_pumped_storage_consumption_mw`** (double or null, optional, MW): Net power consumed by pumped-storage hydroelectric plants (MW). Values are typically negative, indicating the plant is pumping water uphill (consuming electricity). Corresponds to the 'Hydro pumped storage consumption' production type.
- **`cross_border_electricity_trading_mw`** (double or null, optional, MW): Net cross-border electricity exchange (MW). Positive values indicate net imports; negative values indicate net exports. Corresponds to the 'Cross border electricity trading' production type.
- **`hydro_run_of_river_mw`** (double or null, optional, MW): Net generation from run-of-river hydroelectric plants (MW). These plants generate electricity from the natural flow of rivers without significant storage. Corresponds to the 'Hydro Run-of-River' production type.
- **`biomass_mw`** (double or null, optional, MW): Net generation from biomass power plants (MW). Includes solid biomass, biogas, and bioliquids. Corresponds to the 'Biomass' production type.
- **`fossil_brown_coal_lignite_mw`** (double or null, optional, MW): Net generation from brown coal (lignite) power plants (MW). Lignite is a low-grade coal with high moisture content used primarily in Germany. Corresponds to the 'Fossil brown coal / lignite' production type.
- **`fossil_hard_coal_mw`** (double or null, optional, MW): Net generation from hard coal power plants (MW). Hard coal (anthracite/bituminous) has higher energy density than lignite. Corresponds to the 'Fossil hard coal' production type.
- **`fossil_oil_mw`** (double or null, optional, MW): Net generation from oil-fired power plants (MW). Includes heavy fuel oil and light oil combustion turbines. Corresponds to the 'Fossil oil' production type.
- **`fossil_coal_derived_gas_mw`** (double or null, optional, MW): Net generation from coal-derived gas power plants (MW). Includes blast furnace gas, coke oven gas, and coal mine methane. Corresponds to the 'Fossil coal-derived gas' production type.
- **`fossil_gas_mw`** (double or null, optional, MW): Net generation from natural gas power plants (MW). Includes combined-cycle gas turbines (CCGT) and open-cycle gas turbines (OCGT). Corresponds to the 'Fossil gas' production type.
- **`geothermal_mw`** (double or null, optional, MW): Net generation from geothermal power plants (MW). Uses heat from the earth's interior to generate electricity. Corresponds to the 'Geothermal' production type.
- **`hydro_water_reservoir_mw`** (double or null, optional, MW): Net generation from reservoir hydroelectric plants (MW). These plants store water behind a dam and release it to generate electricity on demand. Corresponds to the 'Hydro water reservoir' production type.
- **`hydro_pumped_storage_mw`** (double or null, optional, MW): Net generation from pumped-storage hydroelectric plants when generating (MW). Positive values indicate the plant is releasing stored water to generate electricity. Corresponds to the 'Hydro pumped storage' (generation) production type.
- **`others_mw`** (double or null, optional, MW): Net generation from other power sources not classified into specific categories (MW). May include mixed-fuel plants or uncategorized sources. Corresponds to the 'Others' production type.
- **`waste_mw`** (double or null, optional, MW): Net generation from waste incineration power plants (MW). Includes municipal solid waste and industrial waste combustion. Corresponds to the 'Waste' production type.
- **`wind_offshore_mw`** (double or null, optional, MW): Net generation from offshore wind turbines (MW). Offshore wind farms are located in bodies of water, typically on the continental shelf. Corresponds to the 'Wind offshore' production type.
- **`wind_onshore_mw`** (double or null, optional, MW): Net generation from onshore wind turbines (MW). Onshore wind farms are located on land. Corresponds to the 'Wind onshore' production type.
- **`solar_mw`** (double or null, optional, MW): Net generation from solar photovoltaic (PV) and concentrated solar power (CSP) plants (MW). Corresponds to the 'Solar' production type.
- **`nuclear_mw`** (double or null, optional, MW): Net generation from nuclear power plants (MW). Not present for all countries (e.g. absent for Germany after nuclear phase-out). Corresponds to the 'Nuclear' production type when available.
- **`load_mw`** (double or null, optional, MW): Total electricity grid load (demand) for the country (MW). Represents the sum of all electricity consumption at the given timestamp. Corresponds to the 'Load' production type.
- **`residual_load_mw`** (double or null, optional, MW): Residual load (MW). Calculated as total load minus generation from variable renewable sources (wind and solar). A high residual load indicates that conventional or dispatchable power plants must cover most of the demand. Corresponds to the 'Residual load' production type.
- **`renewable_share_of_generation_pct`** (double or null, optional): Percentage of total electricity generation that comes from renewable sources (0–100). Calculated by dividing renewable generation by total generation. Corresponds to the 'Renewable share of generation' production type.
- **`renewable_share_of_load_pct`** (double or null, optional): Percentage of the total grid load that is covered by renewable generation (0–100). Calculated by dividing renewable generation by total load. Corresponds to the 'Renewable share of load' production type.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "country": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "unix_seconds": 0,
  "hydro_pumped_storage_consumption_mw": 0,
  "cross_border_electricity_trading_mw": 0,
  "hydro_run_of_river_mw": 0,
  "biomass_mw": 0,
  "fossil_brown_coal_lignite_mw": 0,
  "fossil_hard_coal_mw": 0,
  "fossil_oil_mw": 0,
  "fossil_coal_derived_gas_mw": 0,
  "fossil_gas_mw": 0,
  "geothermal_mw": 0,
  "hydro_water_reservoir_mw": 0,
  "hydro_pumped_storage_mw": 0,
  "others_mw": 0,
  "waste_mw": 0,
  "wind_offshore_mw": 0,
  "wind_onshore_mw": 0,
  "solar_mw": 0,
  "nuclear_mw": 0,
  "load_mw": 0,
  "residual_load_mw": 0,
  "renewable_share_of_generation_pct": 0,
  "renewable_share_of_load_pct": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Spot Price

CloudEvents type: `info.energy_charts.SpotPrice`

#### What it tells you

Day-ahead electricity spot price for a given bidding zone at a specific timestamp. Sourced from the Energy-Charts /price endpoint (Fraunhofer ISE) which provides wholesale electricity market prices from ENTSO-E and national exchanges. Prices are the day-ahead auction clearing price in EUR per MWh.

#### Identity

Each event identifies the real-world resource with `{country}`. `{country}` is ISO 3166-1 alpha-2 country code derived from the bidding zone (e.g. 'de' from 'DE-LU'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `energy-charts`, key `{country}` |

#### Payload

`Spot Price` payloads are JSON object. Required fields: `country`, `bidding_zone`, `timestamp`, `unix_seconds`.

- **`country`** (string, required): ISO 3166-1 alpha-2 country code derived from the bidding zone (e.g. 'de' from 'DE-LU'). Used for Kafka key partitioning.
- **`bidding_zone`** (string, required): European electricity bidding zone identifier as used by ENTSO-E (e.g. 'DE-LU' for Germany-Luxembourg, 'FR' for France, 'NO1' for Norway zone 1). The bzn parameter in the Energy-Charts /price API.
- **`timestamp`** (datetime, required): UTC timestamp derived from the unix_seconds value. Marks the start of the price interval (typically 15-minute or hourly depending on the market).
- **`unix_seconds`** (int64, required): Unix epoch timestamp in seconds as returned by the Energy-Charts API.
- **`price_eur_per_mwh`** (double or null, optional, EUR/MWh): Day-ahead electricity spot price in EUR per megawatt-hour (EUR/MWh). This is the clearing price from the day-ahead auction on the relevant power exchange. Can be negative during periods of excess generation.
- **`unit`** (string or null, optional): Unit label as returned by the Energy-Charts API (e.g. 'EUR / MWh'). Included for traceability with the upstream response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "country": "string",
  "bidding_zone": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "unix_seconds": 0,
  "price_eur_per_mwh": 0,
  "unit": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Grid Signal

CloudEvents type: `info.energy_charts.GridSignal`

#### What it tells you

Grid carbon signal for a given country at a specific timestamp. Sourced from the Energy-Charts /signal endpoint (Fraunhofer ISE). Provides a traffic-light signal (0=green, 1=yellow, 2=red) indicating how carbon-intensive the current electricity mix is.

#### Identity

Each event identifies the real-world resource with `{country}`. `{country}` is ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `energy-charts`, key `{country}` |

#### Payload

`Grid Signal` payloads are JSON object. Required fields: `country`, `timestamp`, `unix_seconds`.

- **`country`** (string, required): ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany). Used as the query parameter in the Energy-Charts API.
- **`timestamp`** (datetime, required): UTC timestamp derived from the unix_seconds value. Marks the start of the 15-minute measurement interval.
- **`unix_seconds`** (int64, required): Unix epoch timestamp in seconds as returned by the Energy-Charts API.
- **`signal`** (int32 or null, optional): Traffic-light carbon signal: 0 = green (high renewable share, low carbon — good time to consume), 1 = yellow (moderate renewable share), 2 = red (low renewable share, high carbon — avoid consumption if possible). The thresholds are defined by Fraunhofer ISE based on the renewable share of generation.
- **`renewable_share_pct`** (double or null, optional): Renewable share of generation as a percentage (0–100) at this timestamp. This is the precise numerical value underlying the traffic-light signal.
- **`substitute`** (boolean or null, optional): Whether this signal value is a substitute (forecast or estimate) rather than based on actual metered data. True indicates the value is projected; false indicates it is based on real measurements.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "country": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "unix_seconds": 0,
  "signal": 0,
  "renewable_share_pct": 0,
  "substitute": false
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

- xRegistry manifest: [`xreg/energy_charts.xreg.json`](xreg/energy_charts.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Energy-Charts API: <https://api.energy-charts.info/>
