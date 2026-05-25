# EURDEP Radiation Events

Bridge for the **EURDEP (European Radiological Data Exchange Platform)** pan-European ambient gamma dose rate monitoring network.

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

### Endpoint `eu.jrc.eurdep.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`eu.jrc.eurdep`](#messagegroup-eujrceurdep) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `eurdep-radiation` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `eu.jrc.eurdep`
<a id="messagegroup-eujrceurdep"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `eu.jrc.eurdep.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `eu.jrc.eurdep.Station`
<a id="message-eujrceurdepstation"></a>

Reference metadata for an ambient gamma dose rate monitoring station in the EURDEP (European Radiological Data Exchange Platform) network. EURDEP aggregates data from approximately 5,500 stations across 39 European countries. Each station continuously measures ambient gamma dose rate and reports hourly averaged values. Station metadata includes the geographic position, elevation above sea level, country of origin, and operational status.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.jrc.eurdep.jstruct/schemas/eu.jrc.eurdep.Station`](#schema-eujrceurdepstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.jrc.eurdep.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.jrc.eurdep.Kafka` | `KAFKA` | topic `eurdep-radiation`; key `{station_id}` |

#### Message `eu.jrc.eurdep.DoseRateReading`
<a id="message-eujrceurdepdoseratereading"></a>

An ambient gamma dose rate reading from a EURDEP monitoring station. Each reading reports the gross gamma dose rate in microsieverts per hour (µSv/h) averaged over a one-hour measurement window. Readings include validation status, the nuclide type measured, measurement duration, and the analysis time range. Normal European background levels range from approximately 0.04 to 0.20 µSv/h depending on local geology and altitude.

| Field | Value |
| --- | --- |
| Name | DoseRateReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.jrc.eurdep.jstruct/schemas/eu.jrc.eurdep.DoseRateReading`](#schema-eujrceurdepdoseratereading) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.jrc.eurdep.DoseRateReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.jrc.eurdep.Kafka` | `KAFKA` | topic `eurdep-radiation`; key `{station_id}` |

## Schemagroups

### Schemagroup `eu.jrc.eurdep.jstruct`
<a id="schemagroup-eujrceurdepjstruct"></a>

#### Schema `eu.jrc.eurdep.Station`
<a id="schema-eujrceurdepstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/eu/jrc/eurdep/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/jrc/eurdep/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference metadata for an ambient gamma dose rate monitoring station in the EURDEP network. EURDEP (European Radiological Data Exchange Platform) is operated by the European Commission's Joint Research Centre (JRC) and aggregates real-time radiological monitoring data from national networks across 39 European countries. Each station is identified by a country-prefixed alphanumeric code (e.g. 'AT0001' for Austria, 'DE0123' for Germany).

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Alphanumeric station identifier assigned within the EURDEP network. The first two characters are the ISO 3166-1 alpha-2 country code of the operating country, followed by a numeric station sequence. Example: 'AT0001' (Austria), 'DE0123' (Germany), 'FR0456' (France). This is the stable key used for data retrieval and cross-referencing. | - | - | - |
| `name` | `string` | `True` | Human-readable name of the station location, typically a city or locality name. Example: 'Laa/ThayaAMS'. | - | - | - |
| `country_code` | `string` | `True` | ISO 3166-1 alpha-2 country code extracted from the first two characters of the station_id. Identifies the country operating the monitoring station. Example: 'AT' for Austria, 'DE' for Germany, 'CZ' for Czech Republic. | - | - | - |
| `latitude` | `double` | `True` | Latitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates returned by the WFS endpoint. | unit=`deg` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Longitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates returned by the WFS endpoint. | unit=`deg` symbol=`°` | - | - |
| `height_above_sea` | `union` | `True` | Elevation of the station above mean sea level in meters. Determines the cosmic radiation component contribution. Null if the elevation is not reported by the national network. | unit=`m` symbol=`m` | - | - |
| `site_status` | `int32` | `True` | Numeric operational status code of the station. 1 = active and reporting, other values indicate the station is inactive, under maintenance, or decommissioned. | - | - | - |
| `site_status_text` | `string` | `True` | Human-readable text describing the operational status of the station. Language depends on the reporting country. Example: 'in Betrieb' (German for 'in operation'). | - | - | - |

#### Schema `eu.jrc.eurdep.DoseRateReading`
<a id="schema-eujrceurdepdoseratereading"></a>

| Field | Value |
| --- | --- |
| Name | DoseRateReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/eu/jrc/eurdep/DoseRateReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/jrc/eurdep/DoseRateReading` |
| Type | `object` |

###### Object `DoseRateReading`
<a id="schema-node-doseratereading"></a>

An ambient gamma dose rate reading from a EURDEP monitoring station. The gross dose rate value is the total ambient dose equivalent rate at the station location, expressed in microsieverts per hour (µSv/h). Each reading covers a one-hour measurement window and includes validation status and the nuclide type measured. Normal European background levels range from approximately 0.04 to 0.20 µSv/h depending on local geology and altitude.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Alphanumeric station identifier from the EURDEP network. Matches the station_id in the Station schema. Example: 'AT0001'. | - | - | - |
| `name` | `string` | `True` | Human-readable name of the station location. Included for convenience so readings are self-describing without a Station reference join. | - | - | - |
| `value` | `union` | `True` | Gross ambient gamma dose rate averaged over the measurement period in microsieverts per hour (µSv/h). Null if the station did not report a valid measurement for this interval. | unit=`uSv/h` symbol=`µSv/h` | - | - |
| `unit` | `string` | `True` | Unit of the dose rate value as reported by the upstream EURDEP system. Typically 'µSv/h' (microsieverts per hour), though encoding artifacts may appear in the raw API response. | - | - | - |
| `start_measure` | `string` | `True` | Start of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-08T19:00:00Z'. | - | - | - |
| `end_measure` | `string` | `True` | End of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-08T20:00:00Z'. | - | - | - |
| `nuclide` | `string` | `True` | Nuclide identifier describing the type of radiation measured. For standard gamma dose rate probes this is 'Gamma-ODL-Brutto' (gross gamma ambient dose rate). | - | - | - |
| `duration` | `string` | `True` | Measurement integration period as reported by the upstream system. Example: '1h' for one hour. | - | - | - |
| `validated` | `int32` | `True` | Data validation status flag. 0 = not validated, 1 = validated by national authority, 2 = validated by EURDEP system. Higher values indicate stronger quality assurance. | - | - | - |

### Schemagroup `eu.jrc.eurdep.avro`
<a id="schemagroup-eujrceurdepavro"></a>

#### Schema `eu.jrc.eurdep.Station`
<a id="schema-eujrceurdepstation"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | eu.jrc.eurdep |
| Type | `record` |
| Doc | Reference metadata for an ambient gamma dose rate monitoring station in the EURDEP network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Alphanumeric station identifier with country prefix (e.g. 'AT0001'). | `-` |
| `name` | `string` | Human-readable station location name. | `-` |
| `country_code` | `string` | ISO 3166-1 alpha-2 country code extracted from station_id. | `-` |
| `latitude` | `double` | Latitude in WGS84 decimal degrees. | `-` |
| `longitude` | `double` | Longitude in WGS84 decimal degrees. | `-` |
| `height_above_sea` | `null` \| `double` | Elevation above sea level in meters. Null if unknown. | `-` |
| `site_status` | `int` | Numeric operational status code. 1 = active. | `-` |
| `site_status_text` | `string` | Human-readable operational status text. | `-` |

#### Schema `eu.jrc.eurdep.DoseRateReading`
<a id="schema-eujrceurdepdoseratereading"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DoseRateReading |
| Namespace | eu.jrc.eurdep |
| Type | `record` |
| Doc | An ambient gamma dose rate reading from a EURDEP monitoring station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Alphanumeric station identifier from the EURDEP network. | `-` |
| `name` | `string` | Human-readable station location name. | `-` |
| `value` | `null` \| `double` | Gross ambient gamma dose rate in µSv/h. Null if not reported. | `-` |
| `unit` | `string` | Unit of the dose rate value, typically 'µSv/h'. | `-` |
| `start_measure` | `string` | Start of measurement period in ISO 8601 UTC. | `-` |
| `end_measure` | `string` | End of measurement period in ISO 8601 UTC. | `-` |
| `nuclide` | `string` | Nuclide identifier, typically 'Gamma-ODL-Brutto'. | `-` |
| `duration` | `string` | Measurement integration period (e.g. '1h'). | `-` |
| `validated` | `int` | Validation status flag. 0 = not validated, 1 = nationally validated, 2 = EURDEP validated. | `-` |
