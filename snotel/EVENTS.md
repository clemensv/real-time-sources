# USDA NRCS SNOTEL Snow and Weather Bridge Events

A real-time data bridge that fetches hourly snow and weather observations from the USDA Natural Resources Conservation Service (NRCS) SNOTEL (SNOwpack TELemetry) network and produces them as CloudEvents to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

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

### Endpoint `gov.usda.nrcs.snotel.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`gov.usda.nrcs.snotel`](#messagegroup-govusdanrcssnotel) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `snotel` |
| Kafka key | `{station_triplet}` |
| Deployed | False |

## Messagegroups

### Messagegroup `gov.usda.nrcs.snotel`
<a id="messagegroup-govusdanrcssnotel"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `gov.usda.nrcs.snotel.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `gov.usda.nrcs.snotel.Station`
<a id="message-govusdanrcssnotelstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.usda.nrcs.snotel.jstruct/schemas/gov.usda.nrcs.snotel.Station`](#schema-govusdanrcssnotelstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.usda.nrcs.snotel.Station` |
| `source` |  | `string` | `False` | `https://wcc.sc.egov.usda.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_triplet}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.usda.nrcs.snotel.Kafka` | `KAFKA` | topic `snotel`; key `{station_triplet}` |

#### Message `gov.usda.nrcs.snotel.SnowObservation`
<a id="message-govusdanrcssnotelsnowobservation"></a>

| Field | Value |
| --- | --- |
| Name | SnowObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.usda.nrcs.snotel.jstruct/schemas/gov.usda.nrcs.snotel.SnowObservation`](#schema-govusdanrcssnotelsnowobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.usda.nrcs.snotel.SnowObservation` |
| `source` |  | `string` | `False` | `https://wcc.sc.egov.usda.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_triplet}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.usda.nrcs.snotel.Kafka` | `KAFKA` | topic `snotel`; key `{station_triplet}` |

## Schemagroups

### Schemagroup `gov.usda.nrcs.snotel.jstruct`
<a id="schemagroup-govusdanrcssnoteljstruct"></a>

#### Schema `gov.usda.nrcs.snotel.Station`
<a id="schema-govusdanrcssnotelstation"></a>

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
| $id | `https://wcc.sc.egov.usda.gov/schemas/gov/usda/nrcs/snotel/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference metadata for a USDA NRCS SNOTEL (SNOwpack TELemetry) station. SNOTEL is an automated system of over 900 snowpack monitoring sites in the western United States and Alaska operated by the Natural Resources Conservation Service. Each station reports snowpack, precipitation, and temperature data via satellite telemetry. This reference record provides the station identity and geographic context for the hourly telemetry observations.

| Field | Value |
| --- | --- |
| $id | `https://wcc.sc.egov.usda.gov/schemas/gov/usda/nrcs/snotel/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_triplet` | `string` | `True` | SNOTEL station triplet identifier in the format '{stationId}:{stateCode}:SNTL'. This is the canonical identifier used by the USDA NRCS Water and Climate Center to uniquely reference each SNOTEL site (e.g. '838:CO:SNTL' for University Camp, Colorado). | - | - | - |
| `name` | `string` | `True` | Human-readable station name assigned by the USDA NRCS (e.g. 'University Camp', 'Berthoud Summit'). Station names are generally geographic references to the site location. | - | - | - |
| `state` | `string` | `True` | Two-letter US state or territory code where the station is located (e.g. 'CO', 'AK', 'MT'). Stations are distributed across the western United States and Alaska. | - | - | - |
| `elevation` | `double` | `True` | Station elevation above sea level. Reported by the NRCS in feet. SNOTEL stations are typically located at high elevations in mountainous terrain to monitor snowpack. | unit=`[ft_i]` symbol=`ft` | - | - |
| `latitude` | `double` | `True` | Latitude of the SNOTEL station in decimal degrees north. All SNOTEL stations are in the northern hemisphere (positive values). | - | - | - |
| `longitude` | `double` | `True` | Longitude of the SNOTEL station in decimal degrees east. Western US stations have negative values indicating west of the Prime Meridian. | - | - | - |

#### Schema `gov.usda.nrcs.snotel.SnowObservation`
<a id="schema-govusdanrcssnotelsnowobservation"></a>

| Field | Value |
| --- | --- |
| Name | SnowObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://wcc.sc.egov.usda.gov/schemas/gov/usda/nrcs/snotel/SnowObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SnowObservation`
<a id="schema-node-snowobservation"></a>

Hourly snow and weather observation from a USDA NRCS SNOTEL station. Each record represents one hourly reading transmitted via satellite telemetry from an automated high-elevation monitoring site. The observation includes Snow Water Equivalent (the primary hydrologic measurement), snow depth, accumulated precipitation, and air temperature. Missing values are common when sensors are offline, under maintenance, or producing suspect readings — the NRCS quality-control process may flag or remove values. Data is sourced from the NRCS Report Generator at https://wcc.sc.egov.usda.gov/reportGenerator/.

| Field | Value |
| --- | --- |
| $id | `https://wcc.sc.egov.usda.gov/schemas/gov/usda/nrcs/snotel/SnowObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_triplet` | `string` | `True` | SNOTEL station triplet identifier in the format '{stationId}:{stateCode}:SNTL'. Links this observation to the station that reported it. | - | - | - |
| `date_time` | `datetime` | `True` | Observation timestamp reported by the SNOTEL station. Hourly readings are transmitted via satellite telemetry, typically at the top of each hour. The time is in the station's local standard time as reported by the NRCS Report Generator. | - | - | - |
| `snow_water_equivalent` | `union` | `False` | Snow Water Equivalent (SWE) — the depth of water that would theoretically result if the entire snowpack were melted instantaneously. Measured by a snow pillow sensor at the station. This is the primary measurement for water supply forecasting. Reported in inches. | unit=`[in_i]` symbol=`in` | - | - |
| `snow_depth` | `union` | `False` | Total snow depth measured by an ultrasonic depth sensor mounted above the snow surface. Reported in inches. Can fluctuate due to settling, wind redistribution, and measurement noise. | unit=`[in_i]` symbol=`in` | - | - |
| `precipitation` | `union` | `False` | Water-year accumulated precipitation measured by a storage-type precipitation gauge. The accumulation resets on October 1 (start of the water year). Reported in inches. Values are cumulative and should be monotonically increasing within a water year. | unit=`[in_i]` symbol=`in` | - | - |
| `air_temperature` | `union` | `False` | Instantaneously observed air temperature at the station. SNOTEL air temperature data contains a known bias rooted in the sensor conversion equation that varies through the output range; see the NRCS Air Temperature Bias Correction documentation. Reported in degrees Fahrenheit. | unit=`[degF]` symbol=`°F` | - | - |
