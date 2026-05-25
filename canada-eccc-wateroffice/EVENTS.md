# Canada ECCC Water Office Hydrometric Bridge Events

Real-time hydrometric data from [Environment and Climate Change Canada (ECCC) Water Survey of Canada](https://wateroffice.ec.gc.ca/) bridged to Apache Kafka as CloudEvents.

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

### Endpoint `CA.Gov.ECCC.Hydro.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`CA.Gov.ECCC.Hydro`](#messagegroup-cagoveccchydro) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `canada-eccc-wateroffice` |
| Kafka key | `stations/{station_number}` |
| Deployed | False |

## Messagegroups

### Messagegroup `CA.Gov.ECCC.Hydro`
<a id="messagegroup-cagoveccchydro"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `CA.Gov.ECCC.Hydro.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `CA.Gov.ECCC.Hydro.Station`
<a id="message-cagoveccchydrostation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CA.Gov.ECCC.Hydro.jstruct/schemas/CA.Gov.ECCC.Hydro.Station`](#schema-cagoveccchydrostation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CA.Gov.ECCC.Hydro.Station` |
| `source` |  | `string` | `False` | `https://api.weather.gc.ca/collections/hydrometric-stations` |
| `subject` |  | `uritemplate` | `False` | `stations/{station_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CA.Gov.ECCC.Hydro.Kafka` | `KAFKA` | topic `canada-eccc-wateroffice`; key `stations/{station_number}` |

#### Message `CA.Gov.ECCC.Hydro.Observation`
<a id="message-cagoveccchydroobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CA.Gov.ECCC.Hydro.jstruct/schemas/CA.Gov.ECCC.Hydro.Observation`](#schema-cagoveccchydroobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CA.Gov.ECCC.Hydro.Observation` |
| `source` |  | `string` | `False` | `https://api.weather.gc.ca/collections/hydrometric-realtime` |
| `subject` |  | `uritemplate` | `False` | `stations/{station_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CA.Gov.ECCC.Hydro.Kafka` | `KAFKA` | topic `canada-eccc-wateroffice`; key `stations/{station_number}` |

## Schemagroups

### Schemagroup `CA.Gov.ECCC.Hydro.jstruct`
<a id="schemagroup-cagoveccchydrojstruct"></a>

#### Schema `CA.Gov.ECCC.Hydro.Station`
<a id="schema-cagoveccchydrostation"></a>

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
| $id | `https://example.com/schemas/CA/Gov/ECCC/Hydro/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for a Water Survey of Canada hydrometric monitoring station from the ECCC OGC API hydrometric-stations collection.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CA/Gov/ECCC/Hydro/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_number` | `string` | `True` | Unique WSC station identifier following the scheme 2-digit major drainage area + letter + station digits, e.g. '05BJ004'. Upstream field: STATION_NUMBER. | altnames=`["STATION_NUMBER"]` | - | - |
| `station_name` | `string` | `True` | Official name of the hydrometric station, e.g. 'ELBOW RIVER AT BRAGG CREEK'. Upstream field: STATION_NAME. | altnames=`["STATION_NAME"]` | - | - |
| `prov_terr_state_loc` | `string` | `True` | Two-letter province, territory or state location code where the station is situated, e.g. 'AB' for Alberta. Upstream field: PROV_TERR_STATE_LOC. | altnames=`["PROV_TERR_STATE_LOC"]` | - | - |
| `status_en` | `union` | `False` | Operational status of the station in English, e.g. 'Active', 'Discontinued'. Upstream field: STATUS_EN. | altnames=`["STATUS_EN"]` | - | - |
| `contributor_en` | `union` | `False` | Name of the contributing agency responsible for operating this station in English, e.g. 'Water Survey of Canada'. Upstream field: CONTRIBUTOR_EN. | altnames=`["CONTRIBUTOR_EN"]` | - | - |
| `drainage_area_gross` | `union` | `False` | Gross drainage area of the watershed upstream of this station in square kilometres. Upstream field: DRAINAGE_AREA_GROSS. | unit=`square kilometre` symbol=`km²`<br>altnames=`["DRAINAGE_AREA_GROSS"]` | - | - |
| `drainage_area_effect` | `union` | `False` | Effective (contributing) drainage area of the watershed upstream of this station in square kilometres, excluding non-contributing areas. Upstream field: DRAINAGE_AREA_EFFECT. | unit=`square kilometre` symbol=`km²`<br>altnames=`["DRAINAGE_AREA_EFFECT"]` | - | - |
| `rhbn` | `union` | `False` | Indicates whether the station is part of the Reference Hydrometric Basin Network (RHBN), a subset of hydrologically stable, minimally disturbed basins used for climate change studies. Upstream field: RHBN. | altnames=`["RHBN"]` | - | - |
| `real_time` | `union` | `False` | Indicates whether real-time data are available for this station via the WSC real-time data service. Upstream field: REAL_TIME. | altnames=`["REAL_TIME"]` | - | - |
| `latitude` | `union` | `False` | Geographic latitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `union` | `False` | Geographic longitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates. | unit=`degree` symbol=`°` | - | - |

#### Schema `CA.Gov.ECCC.Hydro.Observation`
<a id="schema-cagoveccchydroobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CA/Gov/ECCC/Hydro/Observation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Real-time hydrometric observation from the ECCC OGC API hydrometric-realtime collection. Data are provisional and updated approximately every 5 minutes.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CA/Gov/ECCC/Hydro/Observation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_number` | `string` | `True` | Unique WSC station identifier, e.g. '05BJ004'. Upstream field: STATION_NUMBER. | altnames=`["STATION_NUMBER"]` | - | - |
| `identifier` | `string` | `True` | Unique observation identifier composed of station number and ISO 8601 observation datetime, e.g. '05BJ004.2026-03-07T07:00:00Z'. Upstream field: IDENTIFIER. | altnames=`["IDENTIFIER"]` | - | - |
| `station_name` | `string` | `True` | Official name of the hydrometric station. Upstream field: STATION_NAME. | altnames=`["STATION_NAME"]` | - | - |
| `prov_terr_state_loc` | `string` | `True` | Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC. | altnames=`["PROV_TERR_STATE_LOC"]` | - | - |
| `observation_datetime` | `datetime` | `True` | Timestamp of the observation in UTC. Upstream field: DATETIME. | altnames=`["DATETIME"]` | - | - |
| `level` | `union` | `False` | Water level at the station gauge in metres above the station datum. Null when not measured or unavailable. Upstream field: LEVEL. | unit=`metre` symbol=`m`<br>altnames=`["LEVEL"]` | - | - |
| `discharge` | `union` | `False` | Water discharge (flow rate) at the station in cubic metres per second. Null when not measured or unavailable. Upstream field: DISCHARGE. | unit=`cubic metre per second` symbol=`m³/s`<br>altnames=`["DISCHARGE"]` | - | - |
| `latitude` | `union` | `False` | Geographic latitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `union` | `False` | Geographic longitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates. | unit=`degree` symbol=`°` | - | - |

### Schemagroup `CA.Gov.ECCC.Hydro.avro`
<a id="schemagroup-cagoveccchydroavro"></a>

#### Schema `CA.Gov.ECCC.Hydro.Station`
<a id="schema-cagoveccchydrostation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | CA.Gov.ECCC.Hydro |
| Type | `record` |
| Doc | Reference data for a Water Survey of Canada hydrometric monitoring station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_number` | `string` | Unique WSC station identifier, e.g. '05BJ004'. Upstream field: STATION_NUMBER. | `-` |
| `station_name` | `string` | Official name of the hydrometric station. Upstream field: STATION_NAME. | `-` |
| `prov_terr_state_loc` | `string` | Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC. | `-` |
| `status_en` | `null` \| `string` | Operational status of the station in English. Upstream field: STATUS_EN. | `-` |
| `contributor_en` | `null` \| `string` | Name of the contributing agency in English. Upstream field: CONTRIBUTOR_EN. | `-` |
| `drainage_area_gross` | `null` \| `double` | Gross drainage area in km². Upstream field: DRAINAGE_AREA_GROSS. | `-` |
| `drainage_area_effect` | `null` \| `double` | Effective drainage area in km². Upstream field: DRAINAGE_AREA_EFFECT. | `-` |
| `rhbn` | `null` \| `boolean` | Part of the Reference Hydrometric Basin Network. Upstream field: RHBN. | `-` |
| `real_time` | `null` \| `boolean` | Real-time data availability flag. Upstream field: REAL_TIME. | `-` |
| `latitude` | `null` \| `double` | Station latitude in decimal degrees (WGS84). | `-` |
| `longitude` | `null` \| `double` | Station longitude in decimal degrees (WGS84). | `-` |

#### Schema `CA.Gov.ECCC.Hydro.Observation`
<a id="schema-cagoveccchydroobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Observation |
| Namespace | CA.Gov.ECCC.Hydro |
| Type | `record` |
| Doc | Real-time hydrometric observation from ECCC Water Survey of Canada. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_number` | `string` | Unique WSC station identifier. Upstream field: STATION_NUMBER. | `-` |
| `identifier` | `string` | Unique observation identifier. Upstream field: IDENTIFIER. | `-` |
| `station_name` | `string` | Official name of the hydrometric station. Upstream field: STATION_NAME. | `-` |
| `prov_terr_state_loc` | `string` | Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC. | `-` |
| `observation_datetime` | `string` | Timestamp of the observation in UTC. Upstream field: DATETIME. | `-` |
| `level` | `null` \| `double` | Water level in metres. Upstream field: LEVEL. | `-` |
| `discharge` | `null` \| `double` | Discharge in m³/s. Upstream field: DISCHARGE. | `-` |
| `latitude` | `null` \| `double` | Station latitude in decimal degrees (WGS84). | `-` |
| `longitude` | `null` \| `double` | Station longitude in decimal degrees (WGS84). | `-` |
