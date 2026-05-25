# Carbon Intensity UK Events

MQTT/5.0 transport variants for National Grid Carbon Intensity events. Non-retained QoS-1 event topics route by GB national/regional area under energy/gb/national-grid/carbon-intensity/{region}/..., where national records use region=national and DNO region records use stable, version-pinned region slugs keyed by region_id such as north-scotland.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 3 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `uk.org.carbonintensity.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.org.carbonintensity`](#messagegroup-ukorgcarbonintensity) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `carbon-intensity` |
| Kafka key | `{period_from}` |
| Deployed | False |

### Endpoint `uk.org.carbonintensity.Regional.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.org.carbonintensity.Regional`](#messagegroup-ukorgcarbonintensityregional) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `carbon-intensity` |
| Kafka key | `{region_id}` |
| Deployed | False |

### Endpoint `uk.org.carbonintensity.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`uk.org.carbonintensity.mqtt`](#messagegroup-ukorgcarbonintensitymqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `uk.org.carbonintensity`
<a id="messagegroup-ukorgcarbonintensity"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.org.carbonintensity.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `uk.org.carbonintensity.Intensity`
<a id="message-ukorgcarbonintensityintensity"></a>

| Field | Value |
| --- | --- |
| Name | Intensity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.org.carbonintensity.jstruct/schemas/uk.org.carbonintensity.Intensity`](#schema-ukorgcarbonintensityintensity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.org.carbonintensity.Intensity` |
| `source` |  | `string` | `False` | `https://api.carbonintensity.org.uk` |
| `subject` |  | `uritemplate` | `False` | `{period_from}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.org.carbonintensity.Kafka` | `KAFKA` | topic `carbon-intensity`; key `{period_from}` |

#### Message `uk.org.carbonintensity.GenerationMix`
<a id="message-ukorgcarbonintensitygenerationmix"></a>

| Field | Value |
| --- | --- |
| Name | GenerationMix |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.org.carbonintensity.jstruct/schemas/uk.org.carbonintensity.GenerationMix`](#schema-ukorgcarbonintensitygenerationmix) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.org.carbonintensity.GenerationMix` |
| `source` |  | `string` | `False` | `https://api.carbonintensity.org.uk` |
| `subject` |  | `uritemplate` | `False` | `{period_from}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.org.carbonintensity.Kafka` | `KAFKA` | topic `carbon-intensity`; key `{period_from}` |

### Messagegroup `uk.org.carbonintensity.Regional`
<a id="messagegroup-ukorgcarbonintensityregional"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.org.carbonintensity.Regional.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `uk.org.carbonintensity.RegionalIntensity`
<a id="message-ukorgcarbonintensityregionalintensity"></a>

| Field | Value |
| --- | --- |
| Name | RegionalIntensity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.org.carbonintensity.jstruct/schemas/uk.org.carbonintensity.RegionalIntensity`](#schema-ukorgcarbonintensityregionalintensity) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.org.carbonintensity.RegionalIntensity` |
| `source` |  | `string` | `False` | `https://api.carbonintensity.org.uk` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.org.carbonintensity.Regional.Kafka` | `KAFKA` | topic `carbon-intensity`; key `{region_id}` |

### Messagegroup `uk.org.carbonintensity.mqtt`
<a id="messagegroup-ukorgcarbonintensitymqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for National Grid Carbon Intensity events. Non-retained QoS-1 event topics route by GB national/regional area under energy/gb/national-grid/carbon-intensity/{region}/..., where national records use region=national and DNO region records use stable, version-pinned region slugs keyed by region_id such as north-scotland. |
| Transport bindings | `uk.org.carbonintensity.Mqtt` (MQTT/5.0) |
| Messages | 3 |

#### Message `uk.org.carbonintensity.mqtt.Intensity`
<a id="message-ukorgcarbonintensitymqttintensity"></a>

| Field | Value |
| --- | --- |
| Name | Intensity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.org.carbonintensity.jstruct/schemas/uk.org.carbonintensity.Intensity`](#schema-ukorgcarbonintensityintensity) |
| Base message chain | `/messagegroups/uk.org.carbonintensity/messages/uk.org.carbonintensity.Intensity` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.org.carbonintensity.Intensity` |
| `source` |  | `string` | `False` | `https://api.carbonintensity.org.uk` |
| `subject` |  | `uritemplate` | `False` | `{period_from}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.org.carbonintensity.Mqtt` | `MQTT/5.0` | topic `energy/gb/national-grid/carbon-intensity/{region}/intensity` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `energy/gb/national-grid/carbon-intensity/{region}/intensity` |
| QoS | 1 |
| Retain | False |

#### Message `uk.org.carbonintensity.mqtt.GenerationMix`
<a id="message-ukorgcarbonintensitymqttgenerationmix"></a>

| Field | Value |
| --- | --- |
| Name | GenerationMix |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.org.carbonintensity.jstruct/schemas/uk.org.carbonintensity.GenerationMix`](#schema-ukorgcarbonintensitygenerationmix) |
| Base message chain | `/messagegroups/uk.org.carbonintensity/messages/uk.org.carbonintensity.GenerationMix` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.org.carbonintensity.GenerationMix` |
| `source` |  | `string` | `False` | `https://api.carbonintensity.org.uk` |
| `subject` |  | `uritemplate` | `False` | `{period_from}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.org.carbonintensity.Mqtt` | `MQTT/5.0` | topic `energy/gb/national-grid/carbon-intensity/{region}/generation-mix` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `energy/gb/national-grid/carbon-intensity/{region}/generation-mix` |
| QoS | 1 |
| Retain | False |

#### Message `uk.org.carbonintensity.mqtt.RegionalIntensity`
<a id="message-ukorgcarbonintensitymqttregionalintensity"></a>

| Field | Value |
| --- | --- |
| Name | RegionalIntensity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.org.carbonintensity.jstruct/schemas/uk.org.carbonintensity.RegionalIntensity`](#schema-ukorgcarbonintensityregionalintensity) |
| Base message chain | `/messagegroups/uk.org.carbonintensity.Regional/messages/uk.org.carbonintensity.RegionalIntensity` |
| Transport override | `MQTT/5.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.org.carbonintensity.RegionalIntensity` |
| `source` |  | `string` | `False` | `https://api.carbonintensity.org.uk` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.org.carbonintensity.Mqtt` | `MQTT/5.0` | topic `energy/gb/national-grid/carbon-intensity/{region}/regional-intensity` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `energy/gb/national-grid/carbon-intensity/{region}/regional-intensity` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `uk.org.carbonintensity.jstruct`
<a id="schemagroup-ukorgcarbonintensityjstruct"></a>

#### Schema `uk.org.carbonintensity.Intensity`
<a id="schema-ukorgcarbonintensityintensity"></a>

| Field | Value |
| --- | --- |
| Name | Intensity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `uk.org.carbonintensity.Intensity` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Intensity`
<a id="schema-node-intensity"></a>

National half-hourly carbon intensity for the Great Britain electricity grid, published by National Grid ESO. Contains the forecast and actual carbon dioxide emission intensity in grams of CO2 per kilowatt-hour, along with a qualitative index band.

| Field | Value |
| --- | --- |
| $id | `uk.org.carbonintensity.Intensity` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `period_from` | `datetime` | `True` | ISO 8601 UTC timestamp marking the start of the half-hour settlement period (e.g. 2026-04-06T09:30Z). | - | - | - |
| `period_to` | `datetime` | `True` | ISO 8601 UTC timestamp marking the end of the half-hour settlement period (e.g. 2026-04-06T10:00Z). | - | - | - |
| `forecast` | `union` | `False` | Forecast carbon intensity for this settlement period in grams of CO2 per kilowatt-hour (gCO2/kWh), computed ahead of real-time by National Grid ESO. | unit=`gCO2/kWh` | - | - |
| `actual` | `union` | `False` | Actual (metered) carbon intensity for this settlement period in grams of CO2 per kilowatt-hour (gCO2/kWh). May be null when the period has not yet completed. | unit=`gCO2/kWh` | - | - |
| `index` | `union` | `False` | Qualitative index band for the carbon intensity: one of 'very low', 'low', 'moderate', 'high', or 'very high'. | - | - | - |
| `region` | `string` | `True` | Topic-safe MQTT/UNS region segment. National GB-wide records use the literal national. | - | - | - |
| `ce_id` | `string` | `True` | Deterministic CloudEvents id for subscriber deduplication, composed from settlement period, national region, and event leaf. | - | - | - |

#### Schema `uk.org.carbonintensity.GenerationMix`
<a id="schema-ukorgcarbonintensitygenerationmix"></a>

| Field | Value |
| --- | --- |
| Name | GenerationMix |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `uk.org.carbonintensity.GenerationMix` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GenerationMix`
<a id="schema-node-generationmix"></a>

National half-hourly electricity generation fuel mix for Great Britain, published by National Grid ESO. Each field represents the percentage contribution of a specific fuel type to total generation during the settlement period.

| Field | Value |
| --- | --- |
| $id | `uk.org.carbonintensity.GenerationMix` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `period_from` | `datetime` | `True` | ISO 8601 UTC timestamp marking the start of the half-hour settlement period. | - | - | - |
| `period_to` | `datetime` | `True` | ISO 8601 UTC timestamp marking the end of the half-hour settlement period. | - | - | - |
| `biomass_pct` | `union` | `False` | Percentage of electricity generated from biomass (wood pellets, energy crops, and other organic matter) during this settlement period. | unit=`%` | - | - |
| `coal_pct` | `union` | `False` | Percentage of electricity generated from coal-fired power stations during this settlement period. | unit=`%` | - | - |
| `gas_pct` | `union` | `False` | Percentage of electricity generated from natural gas (CCGT and OCGT) during this settlement period. | unit=`%` | - | - |
| `hydro_pct` | `union` | `False` | Percentage of electricity generated from hydroelectric power stations during this settlement period. | unit=`%` | - | - |
| `imports_pct` | `union` | `False` | Percentage of electricity supplied via interconnector imports from continental Europe and Ireland during this settlement period. | unit=`%` | - | - |
| `nuclear_pct` | `union` | `False` | Percentage of electricity generated from nuclear power stations during this settlement period. | unit=`%` | - | - |
| `oil_pct` | `union` | `False` | Percentage of electricity generated from oil-fired power stations during this settlement period. | unit=`%` | - | - |
| `other_pct` | `union` | `False` | Percentage of electricity generated from other or unclassified fuel sources during this settlement period. | unit=`%` | - | - |
| `solar_pct` | `union` | `False` | Percentage of electricity generated from solar photovoltaic installations during this settlement period. | unit=`%` | - | - |
| `wind_pct` | `union` | `False` | Percentage of electricity generated from onshore and offshore wind turbines during this settlement period. | unit=`%` | - | - |
| `region` | `string` | `True` | Topic-safe MQTT/UNS region segment. National GB-wide records use the literal national. | - | - | - |
| `ce_id` | `string` | `True` | Deterministic CloudEvents id for subscriber deduplication, composed from settlement period, national region, and event leaf. | - | - | - |

#### Schema `uk.org.carbonintensity.RegionalIntensity`
<a id="schema-ukorgcarbonintensityregionalintensity"></a>

| Field | Value |
| --- | --- |
| Name | RegionalIntensity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `uk.org.carbonintensity.RegionalIntensity` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RegionalIntensity`
<a id="schema-node-regionalintensity"></a>

Half-hourly carbon intensity and generation mix for one of the 17 GB Distribution Network Operator (DNO) regions, published by National Grid ESO. Each record covers a specific DNO region identified by its numeric region ID.

| Field | Value |
| --- | --- |
| $id | `uk.org.carbonintensity.RegionalIntensity` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region_id` | `int32` | `True` | Numeric identifier for the DNO region as assigned by the Carbon Intensity API (1-17). | - | - | - |
| `dnoregion` | `string` | `True` | Full name of the Distribution Network Operator region (e.g. 'Scottish Hydro Electric Power Distribution'). | - | - | - |
| `shortname` | `string` | `True` | Short display name for the DNO region (e.g. 'North Scotland'). | - | - | - |
| `period_from` | `datetime` | `True` | ISO 8601 UTC timestamp marking the start of the half-hour settlement period. | - | - | - |
| `period_to` | `datetime` | `True` | ISO 8601 UTC timestamp marking the end of the half-hour settlement period. | - | - | - |
| `forecast` | `union` | `False` | Forecast carbon intensity for this region and settlement period in grams of CO2 per kilowatt-hour (gCO2/kWh). | unit=`gCO2/kWh` | - | - |
| `index` | `union` | `False` | Qualitative index band for the regional carbon intensity: one of 'very low', 'low', 'moderate', 'high', or 'very high'. | - | - | - |
| `biomass_pct` | `union` | `False` | Percentage of electricity generated from biomass in this region during this settlement period. | unit=`%` | - | - |
| `coal_pct` | `union` | `False` | Percentage of electricity generated from coal in this region during this settlement period. | unit=`%` | - | - |
| `gas_pct` | `union` | `False` | Percentage of electricity generated from natural gas in this region during this settlement period. | unit=`%` | - | - |
| `hydro_pct` | `union` | `False` | Percentage of electricity generated from hydroelectric power in this region during this settlement period. | unit=`%` | - | - |
| `imports_pct` | `union` | `False` | Percentage of electricity supplied via interconnector imports in this region during this settlement period. | unit=`%` | - | - |
| `nuclear_pct` | `union` | `False` | Percentage of electricity generated from nuclear power in this region during this settlement period. | unit=`%` | - | - |
| `oil_pct` | `union` | `False` | Percentage of electricity generated from oil in this region during this settlement period. | unit=`%` | - | - |
| `other_pct` | `union` | `False` | Percentage of electricity generated from other or unclassified fuel sources in this region during this settlement period. | unit=`%` | - | - |
| `solar_pct` | `union` | `False` | Percentage of electricity generated from solar photovoltaic installations in this region during this settlement period. | unit=`%` | - | - |
| `wind_pct` | `union` | `False` | Percentage of electricity generated from wind turbines in this region during this settlement period. | unit=`%` | - | - |
| `region` | `string` | `True` | Stable topic-safe MQTT/UNS region segment from the version-pinned DNO region_id lookup table, for example north-scotland for region_id 1. Falls back to region-{region_id} if an unknown future id appears. | - | - | - |
| `ce_id` | `string` | `True` | Deterministic CloudEvents id for subscriber deduplication, composed from settlement period, DNO region_id, and regional-intensity leaf. | - | - | - |
