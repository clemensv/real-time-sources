# AviationWeather.gov Bridge Events

**AviationWeather.gov Bridge** polls the NOAA Aviation Weather Center API for METAR observations, SIGMET advisories, and station reference data, then sends them to a Kafka topic as CloudEvents. The tool tracks previously seen observations to avoid sending duplicates.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `gov.noaa.aviationweather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`gov.noaa.aviationweather`](#messagegroup-govnoaaaviationweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `aviationweather` |
| Kafka key | `{icao_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `gov.noaa.aviationweather`
<a id="messagegroup-govnoaaaviationweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `gov.noaa.aviationweather.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `gov.noaa.aviationweather.Station`
<a id="message-govnoaaaviationweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.noaa.aviationweather.jstruct/schemas/gov.noaa.aviationweather.Station`](#schema-govnoaaaviationweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.noaa.aviationweather.Station` |
| `source` |  | `string` | `False` | `https://aviationweather.gov` |
| `subject` |  | `uritemplate` | `False` | `{icao_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.noaa.aviationweather.Kafka` | `KAFKA` | topic `aviationweather`; key `{icao_id}` |

#### Message `gov.noaa.aviationweather.Metar`
<a id="message-govnoaaaviationweathermetar"></a>

| Field | Value |
| --- | --- |
| Name | Metar |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.noaa.aviationweather.jstruct/schemas/gov.noaa.aviationweather.Metar`](#schema-govnoaaaviationweathermetar) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.noaa.aviationweather.Metar` |
| `source` |  | `string` | `False` | `https://aviationweather.gov` |
| `subject` |  | `uritemplate` | `False` | `{icao_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.noaa.aviationweather.Kafka` | `KAFKA` | topic `aviationweather`; key `{icao_id}` |

#### Message `gov.noaa.aviationweather.Sigmet`
<a id="message-govnoaaaviationweathersigmet"></a>

| Field | Value |
| --- | --- |
| Name | Sigmet |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.noaa.aviationweather.jstruct/schemas/gov.noaa.aviationweather.Sigmet`](#schema-govnoaaaviationweathersigmet) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.noaa.aviationweather.Sigmet` |
| `source` |  | `string` | `False` | `https://aviationweather.gov` |
| `subject` |  | `uritemplate` | `False` | `{icao_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.noaa.aviationweather.Kafka` | `KAFKA` | topic `aviationweather`; key `{icao_id}` |

## Schemagroups

### Schemagroup `gov.noaa.aviationweather.jstruct`
<a id="schemagroup-govnoaaaviationweatherjstruct"></a>

#### Schema `gov.noaa.aviationweather.Station`
<a id="schema-govnoaaaviationweatherstation"></a>

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
| $id | `https://aviationweather.gov/schemas/gov/noaa/aviationweather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference record for an aviation weather reporting station. Sourced from the AviationWeather.gov station information endpoint. Fields cover ICAO, IATA, FAA, and WMO identifiers, location, elevation, and available data products.

| Field | Value |
| --- | --- |
| $id | `https://aviationweather.gov/schemas/gov/noaa/aviationweather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `icao_id` | `string` | `True` | ICAO station identifier. Four-character alphanumeric code assigned by ICAO (e.g. 'KJFK' for John F. Kennedy International Airport). | - | - | - |
| `iata_id` | `union` | `False` | IATA airport code, a three-character code used by the airline industry (e.g. 'JFK'). May be null for non-airport stations. | - | - | - |
| `faa_id` | `union` | `False` | FAA location identifier. Three or four character code assigned by the FAA. May be null for non-US stations. | - | - | - |
| `wmo_id` | `union` | `False` | WMO station identifier. Five-digit numeric code assigned by the World Meteorological Organization. May be null. | - | - | - |
| `name` | `string` | `True` | Human-readable site name from the AviationWeather station database, e.g. 'New York/JF Kennedy Intl'. | - | - | - |
| `latitude` | `double` | `True` | Station latitude in decimal degrees north. Negative values indicate southern hemisphere. | unit=`deg` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Station longitude in decimal degrees east. Negative values indicate western hemisphere. | unit=`deg` symbol=`°` | - | - |
| `elevation` | `union` | `False` | Station field elevation in meters above mean sea level. | unit=`m` symbol=`m` | - | - |
| `state` | `union` | `False` | State or province code where the station is located (e.g. 'NY'). May be null for non-US stations. | - | - | - |
| `country` | `union` | `False` | Two-character ISO 3166-1 alpha-2 country code (e.g. 'US', 'GB'). | - | - | - |
| `site_type` | `union` | `False` | Comma-separated list of data products available at this station from the siteType array (e.g. 'METAR,TAF'). | - | - | - |

#### Schema `gov.noaa.aviationweather.Metar`
<a id="schema-govnoaaaviationweathermetar"></a>

| Field | Value |
| --- | --- |
| Name | Metar |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://aviationweather.gov/schemas/gov/noaa/aviationweather/Metar` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Metar`
<a id="schema-node-metar"></a>

METAR aviation weather observation from the AviationWeather.gov API. Reports surface conditions including temperature, dewpoint, wind, visibility, pressure, clouds, and flight category for an ICAO reporting station.

| Field | Value |
| --- | --- |
| $id | `https://aviationweather.gov/schemas/gov/noaa/aviationweather/Metar` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `icao_id` | `string` | `True` | ICAO station identifier for the reporting station (e.g. 'KJFK'). | - | - | - |
| `obs_time` | `datetime` | `True` | Observation time as a Unix epoch timestamp (seconds since 1970-01-01T00:00:00Z) from the obsTime field in the API response. | - | - | - |
| `report_time` | `union` | `False` | Report time as an ISO 8601 UTC string from the reportTime field. This is the time the observation was officially reported. | - | - | - |
| `temp` | `union` | `False` | Air temperature at the station. Unit: degrees Celsius. | unit=`CEL` symbol=`°C` | - | - |
| `dewp` | `union` | `False` | Dewpoint temperature at the station. Unit: degrees Celsius. | unit=`CEL` symbol=`°C` | - | - |
| `wdir` | `union` | `False` | Wind direction in degrees true (the direction from which the wind is blowing), averaged over the observation period. Value of 0 indicates variable or calm. | unit=`deg` symbol=`°` | - | - |
| `wspd` | `union` | `False` | Sustained wind speed in knots. | unit=`[kn_i]` symbol=`kt` | - | - |
| `wgst` | `union` | `False` | Wind gust speed in knots. Null if no gusts reported. | unit=`[kn_i]` symbol=`kt` | - | - |
| `visib` | `union` | `False` | Prevailing visibility as reported. Value is a string because it can contain qualifiers like '10+' (greater than 10 statute miles) or fractional values. Unit: statute miles. | - | - | - |
| `altim` | `union` | `False` | Altimeter setting (QNH) in hectopascals. | unit=`hPa` symbol=`hPa` | - | - |
| `slp` | `union` | `False` | Sea level pressure in hectopascals. May be null if not reported. | unit=`hPa` symbol=`hPa` | - | - |
| `qc_field` | `union` | `False` | Quality control flag bitmask from the qcField in the API response. | - | - | - |
| `wx_string` | `union` | `False` | Present weather string using standard METAR codes (e.g. '-RA' for light rain, 'BR' for mist). | - | - | - |
| `metar_type` | `union` | `False` | METAR report type: 'METAR' for routine, 'SPECI' for special observation. | - | - | - |
| `raw_ob` | `string` | `True` | The full raw METAR observation text as received, e.g. 'METAR KJFK 061051Z 32013KT 10SM SCT050 05/M05 A3001'. | - | - | - |
| `latitude` | `union` | `False` | Station latitude in decimal degrees north from the METAR response. | unit=`deg` symbol=`°` | - | - |
| `longitude` | `union` | `False` | Station longitude in decimal degrees east from the METAR response. | unit=`deg` symbol=`°` | - | - |
| `elevation` | `union` | `False` | Station elevation in meters above mean sea level from the METAR response. | unit=`m` symbol=`m` | - | - |
| `flt_cat` | `union` | `False` | Flight category derived from ceiling and visibility: VFR, MVFR, IFR, or LIFR. | - | - | - |
| `clouds` | `union` | `False` | JSON-encoded array of cloud layer objects. Each object has 'cover' (string: SKC, CLR, FEW, SCT, BKN, OVC) and 'base' (integer or null: cloud base in feet AGL). Example: '[{"cover":"SCT","base":5000}]'. | - | - | - |
| `name` | `union` | `False` | Human-readable station name included in the METAR response (e.g. 'New York/JF Kennedy Intl, NY, US'). | - | - | - |

#### Schema `gov.noaa.aviationweather.Sigmet`
<a id="schema-govnoaaaviationweathersigmet"></a>

| Field | Value |
| --- | --- |
| Name | Sigmet |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://aviationweather.gov/schemas/gov/noaa/aviationweather/Sigmet` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Sigmet`
<a id="schema-node-sigmet"></a>

SIGMET (Significant Meteorological Information) advisory from the AviationWeather.gov API. Covers both US domestic convective/non-convective SIGMETs and international SIGMETs. Reports hazardous weather conditions for aviation including thunderstorms, turbulence, icing, and volcanic ash.

| Field | Value |
| --- | --- |
| $id | `https://aviationweather.gov/schemas/gov/noaa/aviationweather/Sigmet` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `icao_id` | `string` | `True` | ICAO identifier for the issuing office (e.g. 'KKCI' for the Kansas City Aviation Weather Center) or FIR identifier for international SIGMETs. | - | - | - |
| `series_id` | `string` | `True` | SIGMET series identifier combining alphanumeric sequence (e.g. '6W' for domestic, '8' for international). | - | - | - |
| `valid_time_from` | `datetime` | `True` | Start of the SIGMET validity period as a Unix epoch timestamp (seconds since 1970-01-01T00:00:00Z). | - | - | - |
| `valid_time_to` | `datetime` | `True` | End of the SIGMET validity period as a Unix epoch timestamp (seconds since 1970-01-01T00:00:00Z). | - | - | - |
| `hazard` | `union` | `False` | Weather hazard type: 'CONVECTIVE' for US convective SIGMETs, 'TS' (thunderstorm), 'TURB' (turbulence), 'ICE' (icing), 'VA' (volcanic ash), 'MTW' (mountain wave), etc. | - | - | - |
| `qualifier` | `union` | `False` | Hazard qualifier for international SIGMETs (e.g. 'EMBD' for embedded, 'SEV' for severe, 'OBSC' for obscured). Null for US domestic SIGMETs. | - | - | - |
| `sigmet_type` | `union` | `False` | SIGMET classification: 'SIGMET' for US domestic, 'ISIGMET' for international SIGMETs. | - | - | - |
| `altitude_hi` | `union` | `False` | Upper altitude limit of the hazard area in feet. From altitudeHi1 for US SIGMETs or top for international SIGMETs. | unit=`[ft_i]` symbol=`ft` | - | - |
| `altitude_low` | `union` | `False` | Lower altitude limit of the hazard area in feet. From altitudeLow1 for US SIGMETs or base for international SIGMETs. | unit=`[ft_i]` symbol=`ft` | - | - |
| `movement_dir` | `union` | `False` | Direction of movement of the weather phenomenon. Numeric degrees for US SIGMETs, cardinal direction string (e.g. 'NE') for international. | - | - | - |
| `movement_spd` | `union` | `False` | Speed of movement of the weather phenomenon. Numeric knots for US SIGMETs, knots string for international. | - | - | - |
| `severity` | `union` | `False` | Severity level indicator from the severity field in the US SIGMET response. Higher values indicate greater severity. | - | - | - |
| `raw_sigmet` | `union` | `False` | Full raw SIGMET text as received from the upstream source. | - | - | - |
| `coords` | `union` | `False` | JSON-encoded array of coordinate objects defining the hazard area polygon. Each object has 'lat' (number) and 'lon' (number). Example: '[{"lat":41.88,"lon":-123.70},{"lat":40.00,"lon":-124.23}]'. | - | - | - |
