# Energy-Charts (Fraunhofer ISE) — European Electricity Data Bridge Events

This bridge polls the [Energy-Charts API](https://api.energy-charts.info/) operated by Fraunhofer ISE and forwards European electricity generation, price, and grid carbon signal data to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `info.energy_charts.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`info.energy_charts`](#messagegroup-infoenergycharts) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `energy-charts` |
| Kafka key | `{country}` |
| Deployed | False |

## Messagegroups

### Messagegroup `info.energy_charts`
<a id="messagegroup-infoenergycharts"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `info.energy_charts.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `info.energy_charts.PublicPower`
<a id="message-infoenergychartspublicpower"></a>

| Field | Value |
| --- | --- |
| Name | PublicPower |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/info.energy_charts.jstruct/schemas/info.energy_charts.PublicPower`](#schema-infoenergychartspublicpower) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `info.energy_charts.PublicPower` |
| `source` |  | `string` | `False` | `https://api.energy-charts.info` |
| `subject` |  | `uritemplate` | `False` | `{country}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `info.energy_charts.Kafka` | `KAFKA` | topic `energy-charts`; key `{country}` |

#### Message `info.energy_charts.SpotPrice`
<a id="message-infoenergychartsspotprice"></a>

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/info.energy_charts.jstruct/schemas/info.energy_charts.SpotPrice`](#schema-infoenergychartsspotprice) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `info.energy_charts.SpotPrice` |
| `source` |  | `string` | `False` | `https://api.energy-charts.info` |
| `subject` |  | `uritemplate` | `False` | `{country}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `info.energy_charts.Kafka` | `KAFKA` | topic `energy-charts`; key `{country}` |

#### Message `info.energy_charts.GridSignal`
<a id="message-infoenergychartsgridsignal"></a>

| Field | Value |
| --- | --- |
| Name | GridSignal |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/info.energy_charts.jstruct/schemas/info.energy_charts.GridSignal`](#schema-infoenergychartsgridsignal) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `info.energy_charts.GridSignal` |
| `source` |  | `string` | `False` | `https://api.energy-charts.info` |
| `subject` |  | `uritemplate` | `False` | `{country}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `info.energy_charts.Kafka` | `KAFKA` | topic `energy-charts`; key `{country}` |

## Schemagroups

### Schemagroup `info.energy_charts.jstruct`
<a id="schemagroup-infoenergychartsjstruct"></a>

#### Schema `info.energy_charts.PublicPower`
<a id="schema-infoenergychartspublicpower"></a>

| Field | Value |
| --- | --- |
| Name | PublicPower |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.energy-charts.info/schemas/info/energy_charts/PublicPower` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PublicPower`
<a id="schema-node-publicpower"></a>

Net electricity generation by fuel type for a given country at a specific 15-minute interval. Sourced from the Energy-Charts /public_power endpoint (Fraunhofer ISE) which aggregates ENTSO-E transparency platform data. Each record represents one timestamp in the parallel-array response, with individual production types flattened into named fields in megawatts (MW). Negative values for hydro pumped storage consumption and cross-border trading indicate consumption or export. The renewable_share_of_generation and renewable_share_of_load fields are percentages (0–100). Load represents total grid demand.

| Field | Value |
| --- | --- |
| $id | `https://api.energy-charts.info/schemas/info/energy_charts/PublicPower` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `country` | `string` | `True` | ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany, 'fr' for France). Used as the query parameter in the Energy-Charts API. | - | - | - |
| `timestamp` | `datetime` | `True` | UTC timestamp derived from the unix_seconds value. Marks the start of the 15-minute measurement interval. | - | - | - |
| `unix_seconds` | `int64` | `True` | Unix epoch timestamp in seconds as returned by the Energy-Charts API. Each value corresponds to one row in the parallel arrays of production_types. | - | - | - |
| `hydro_pumped_storage_consumption_mw` | `union` | `False` | Net power consumed by pumped-storage hydroelectric plants (MW). Values are typically negative, indicating the plant is pumping water uphill (consuming electricity). Corresponds to the 'Hydro pumped storage consumption' production type. | unit=`MW` symbol=`MW` | - | - |
| `cross_border_electricity_trading_mw` | `union` | `False` | Net cross-border electricity exchange (MW). Positive values indicate net imports; negative values indicate net exports. Corresponds to the 'Cross border electricity trading' production type. | unit=`MW` symbol=`MW` | - | - |
| `hydro_run_of_river_mw` | `union` | `False` | Net generation from run-of-river hydroelectric plants (MW). These plants generate electricity from the natural flow of rivers without significant storage. Corresponds to the 'Hydro Run-of-River' production type. | unit=`MW` symbol=`MW` | - | - |
| `biomass_mw` | `union` | `False` | Net generation from biomass power plants (MW). Includes solid biomass, biogas, and bioliquids. Corresponds to the 'Biomass' production type. | unit=`MW` symbol=`MW` | - | - |
| `fossil_brown_coal_lignite_mw` | `union` | `False` | Net generation from brown coal (lignite) power plants (MW). Lignite is a low-grade coal with high moisture content used primarily in Germany. Corresponds to the 'Fossil brown coal / lignite' production type. | unit=`MW` symbol=`MW` | - | - |
| `fossil_hard_coal_mw` | `union` | `False` | Net generation from hard coal power plants (MW). Hard coal (anthracite/bituminous) has higher energy density than lignite. Corresponds to the 'Fossil hard coal' production type. | unit=`MW` symbol=`MW` | - | - |
| `fossil_oil_mw` | `union` | `False` | Net generation from oil-fired power plants (MW). Includes heavy fuel oil and light oil combustion turbines. Corresponds to the 'Fossil oil' production type. | unit=`MW` symbol=`MW` | - | - |
| `fossil_coal_derived_gas_mw` | `union` | `False` | Net generation from coal-derived gas power plants (MW). Includes blast furnace gas, coke oven gas, and coal mine methane. Corresponds to the 'Fossil coal-derived gas' production type. | unit=`MW` symbol=`MW` | - | - |
| `fossil_gas_mw` | `union` | `False` | Net generation from natural gas power plants (MW). Includes combined-cycle gas turbines (CCGT) and open-cycle gas turbines (OCGT). Corresponds to the 'Fossil gas' production type. | unit=`MW` symbol=`MW` | - | - |
| `geothermal_mw` | `union` | `False` | Net generation from geothermal power plants (MW). Uses heat from the earth's interior to generate electricity. Corresponds to the 'Geothermal' production type. | unit=`MW` symbol=`MW` | - | - |
| `hydro_water_reservoir_mw` | `union` | `False` | Net generation from reservoir hydroelectric plants (MW). These plants store water behind a dam and release it to generate electricity on demand. Corresponds to the 'Hydro water reservoir' production type. | unit=`MW` symbol=`MW` | - | - |
| `hydro_pumped_storage_mw` | `union` | `False` | Net generation from pumped-storage hydroelectric plants when generating (MW). Positive values indicate the plant is releasing stored water to generate electricity. Corresponds to the 'Hydro pumped storage' (generation) production type. | unit=`MW` symbol=`MW` | - | - |
| `others_mw` | `union` | `False` | Net generation from other power sources not classified into specific categories (MW). May include mixed-fuel plants or uncategorized sources. Corresponds to the 'Others' production type. | unit=`MW` symbol=`MW` | - | - |
| `waste_mw` | `union` | `False` | Net generation from waste incineration power plants (MW). Includes municipal solid waste and industrial waste combustion. Corresponds to the 'Waste' production type. | unit=`MW` symbol=`MW` | - | - |
| `wind_offshore_mw` | `union` | `False` | Net generation from offshore wind turbines (MW). Offshore wind farms are located in bodies of water, typically on the continental shelf. Corresponds to the 'Wind offshore' production type. | unit=`MW` symbol=`MW` | - | - |
| `wind_onshore_mw` | `union` | `False` | Net generation from onshore wind turbines (MW). Onshore wind farms are located on land. Corresponds to the 'Wind onshore' production type. | unit=`MW` symbol=`MW` | - | - |
| `solar_mw` | `union` | `False` | Net generation from solar photovoltaic (PV) and concentrated solar power (CSP) plants (MW). Corresponds to the 'Solar' production type. | unit=`MW` symbol=`MW` | - | - |
| `nuclear_mw` | `union` | `False` | Net generation from nuclear power plants (MW). Not present for all countries (e.g. absent for Germany after nuclear phase-out). Corresponds to the 'Nuclear' production type when available. | unit=`MW` symbol=`MW` | - | - |
| `load_mw` | `union` | `False` | Total electricity grid load (demand) for the country (MW). Represents the sum of all electricity consumption at the given timestamp. Corresponds to the 'Load' production type. | unit=`MW` symbol=`MW` | - | - |
| `residual_load_mw` | `union` | `False` | Residual load (MW). Calculated as total load minus generation from variable renewable sources (wind and solar). A high residual load indicates that conventional or dispatchable power plants must cover most of the demand. Corresponds to the 'Residual load' production type. | unit=`MW` symbol=`MW` | - | - |
| `renewable_share_of_generation_pct` | `union` | `False` | Percentage of total electricity generation that comes from renewable sources (0–100). Calculated by dividing renewable generation by total generation. Corresponds to the 'Renewable share of generation' production type. | - | - | - |
| `renewable_share_of_load_pct` | `union` | `False` | Percentage of the total grid load that is covered by renewable generation (0–100). Calculated by dividing renewable generation by total load. Corresponds to the 'Renewable share of load' production type. | - | - | - |

#### Schema `info.energy_charts.SpotPrice`
<a id="schema-infoenergychartsspotprice"></a>

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.energy-charts.info/schemas/info/energy_charts/SpotPrice` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SpotPrice`
<a id="schema-node-spotprice"></a>

Day-ahead electricity spot price for a given bidding zone at a specific timestamp. Sourced from the Energy-Charts /price endpoint (Fraunhofer ISE) which provides wholesale electricity market prices from ENTSO-E and national exchanges. Prices are the day-ahead auction clearing price in EUR per MWh. The bidding zone identifies the market area (e.g. 'DE-LU' for the Germany-Luxembourg zone).

| Field | Value |
| --- | --- |
| $id | `https://api.energy-charts.info/schemas/info/energy_charts/SpotPrice` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `country` | `string` | `True` | ISO 3166-1 alpha-2 country code derived from the bidding zone (e.g. 'de' from 'DE-LU'). Used for Kafka key partitioning. | - | - | - |
| `bidding_zone` | `string` | `True` | European electricity bidding zone identifier as used by ENTSO-E (e.g. 'DE-LU' for Germany-Luxembourg, 'FR' for France, 'NO1' for Norway zone 1). The bzn parameter in the Energy-Charts /price API. | - | - | - |
| `timestamp` | `datetime` | `True` | UTC timestamp derived from the unix_seconds value. Marks the start of the price interval (typically 15-minute or hourly depending on the market). | - | - | - |
| `unix_seconds` | `int64` | `True` | Unix epoch timestamp in seconds as returned by the Energy-Charts API. | - | - | - |
| `price_eur_per_mwh` | `union` | `False` | Day-ahead electricity spot price in EUR per megawatt-hour (EUR/MWh). This is the clearing price from the day-ahead auction on the relevant power exchange. Can be negative during periods of excess generation. | unit=`EUR/MWh` symbol=`EUR/MWh` | - | - |
| `unit` | `union` | `False` | Unit label as returned by the Energy-Charts API (e.g. 'EUR / MWh'). Included for traceability with the upstream response. | - | - | - |

#### Schema `info.energy_charts.GridSignal`
<a id="schema-infoenergychartsgridsignal"></a>

| Field | Value |
| --- | --- |
| Name | GridSignal |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.energy-charts.info/schemas/info/energy_charts/GridSignal` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GridSignal`
<a id="schema-node-gridsignal"></a>

Grid carbon signal for a given country at a specific timestamp. Sourced from the Energy-Charts /signal endpoint (Fraunhofer ISE). Provides a traffic-light signal (0=green, 1=yellow, 2=red) indicating how carbon-intensive the current electricity mix is. Green (0) means high renewable share and low carbon intensity — a good time to consume electricity. Red (2) means low renewable share and high carbon intensity. The renewable share percentage is also included for precise analysis.

| Field | Value |
| --- | --- |
| $id | `https://api.energy-charts.info/schemas/info/energy_charts/GridSignal` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `country` | `string` | `True` | ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany). Used as the query parameter in the Energy-Charts API. | - | - | - |
| `timestamp` | `datetime` | `True` | UTC timestamp derived from the unix_seconds value. Marks the start of the 15-minute measurement interval. | - | - | - |
| `unix_seconds` | `int64` | `True` | Unix epoch timestamp in seconds as returned by the Energy-Charts API. | - | - | - |
| `signal` | `union` | `False` | Traffic-light carbon signal: 0 = green (high renewable share, low carbon — good time to consume), 1 = yellow (moderate renewable share), 2 = red (low renewable share, high carbon — avoid consumption if possible). The thresholds are defined by Fraunhofer ISE based on the renewable share of generation. | - | - | - |
| `renewable_share_pct` | `union` | `False` | Renewable share of generation as a percentage (0–100) at this timestamp. This is the precise numerical value underlying the traffic-light signal. | - | - | - |
| `substitute` | `union` | `False` | Whether this signal value is a substitute (forecast or estimate) rather than based on actual metered data. True indicates the value is projected; false indicates it is based on real measurements. | - | - | - |

### Schemagroup `info.energy_charts.avro`
<a id="schemagroup-infoenergychartsavro"></a>

#### Schema `info.energy_charts.PublicPower`
<a id="schema-infoenergychartspublicpower"></a>

| Field | Value |
| --- | --- |
| Name | PublicPower |
| Format | Avro/1.11.1 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.1 |

###### Avro

| Field | Value |
| --- | --- |
| Name | PublicPower |
| Namespace | info.energy_charts |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `country` | `string` |  | `-` |
| `timestamp` | `long` |  | `-` |
| `unix_seconds` | `long` |  | `-` |
| `hydro_pumped_storage_consumption_mw` | `null` \| `double` |  | `-` |
| `cross_border_electricity_trading_mw` | `null` \| `double` |  | `-` |
| `hydro_run_of_river_mw` | `null` \| `double` |  | `-` |
| `biomass_mw` | `null` \| `double` |  | `-` |
| `fossil_brown_coal_lignite_mw` | `null` \| `double` |  | `-` |
| `fossil_hard_coal_mw` | `null` \| `double` |  | `-` |
| `fossil_oil_mw` | `null` \| `double` |  | `-` |
| `fossil_coal_derived_gas_mw` | `null` \| `double` |  | `-` |
| `fossil_gas_mw` | `null` \| `double` |  | `-` |
| `geothermal_mw` | `null` \| `double` |  | `-` |
| `hydro_water_reservoir_mw` | `null` \| `double` |  | `-` |
| `hydro_pumped_storage_mw` | `null` \| `double` |  | `-` |
| `others_mw` | `null` \| `double` |  | `-` |
| `waste_mw` | `null` \| `double` |  | `-` |
| `wind_offshore_mw` | `null` \| `double` |  | `-` |
| `wind_onshore_mw` | `null` \| `double` |  | `-` |
| `solar_mw` | `null` \| `double` |  | `-` |
| `nuclear_mw` | `null` \| `double` |  | `-` |
| `load_mw` | `null` \| `double` |  | `-` |
| `residual_load_mw` | `null` \| `double` |  | `-` |
| `renewable_share_of_generation_pct` | `null` \| `double` |  | `-` |
| `renewable_share_of_load_pct` | `null` \| `double` |  | `-` |

#### Schema `info.energy_charts.SpotPrice`
<a id="schema-infoenergychartsspotprice"></a>

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Format | Avro/1.11.1 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.1 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SpotPrice |
| Namespace | info.energy_charts |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `country` | `string` |  | `-` |
| `bidding_zone` | `string` |  | `-` |
| `timestamp` | `long` |  | `-` |
| `unix_seconds` | `long` |  | `-` |
| `price_eur_per_mwh` | `null` \| `double` |  | `-` |
| `unit` | `null` \| `string` |  | `-` |

#### Schema `info.energy_charts.GridSignal`
<a id="schema-infoenergychartsgridsignal"></a>

| Field | Value |
| --- | --- |
| Name | GridSignal |
| Format | Avro/1.11.1 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.1 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GridSignal |
| Namespace | info.energy_charts |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `country` | `string` |  | `-` |
| `timestamp` | `long` |  | `-` |
| `unix_seconds` | `long` |  | `-` |
| `signal` | `null` \| `int` |  | `-` |
| `renewable_share_pct` | `null` \| `double` |  | `-` |
| `substitute` | `null` \| `boolean` |  | `-` |
