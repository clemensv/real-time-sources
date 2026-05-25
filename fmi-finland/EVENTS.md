# FMI Finland Air Quality Bridge Events

This bridge polls the Finnish Meteorological Institute (FMI) open OGC WFS service for hourly air quality observations and republishes them as structured CloudEvents to Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

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

### Endpoint `fi.fmi.opendata.airquality.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.fmi.opendata.airquality`](#messagegroup-fifmiopendataairquality) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `fmi-finland-airquality` |
| Kafka key | `{fmisid}` |
| Deployed | False |

## Messagegroups

### Messagegroup `fi.fmi.opendata.airquality`
<a id="messagegroup-fifmiopendataairquality"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.fmi.opendata.airquality.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `fi.fmi.opendata.airquality.Station`
<a id="message-fifmiopendataairqualitystation"></a>

Reference data for a Finnish Meteorological Institute air quality monitoring station.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.fmi.opendata.airquality.jstruct/schemas/fi.fmi.opendata.airquality.Station`](#schema-fifmiopendataairqualitystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.fmi.opendata.airquality.Station` |
| `source` |  | `uritemplate` | `False` | `https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::ef::stations` |
| `subject` |  | `uritemplate` | `False` | `{fmisid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.fmi.opendata.airquality.Kafka` | `KAFKA` | topic `fmi-finland-airquality`; key `{fmisid}` |

#### Message `fi.fmi.opendata.airquality.Observation`
<a id="message-fifmiopendataairqualityobservation"></a>

Hourly air quality observation aggregated per station and timestamp from FMI OGC WFS simple query results.

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.fmi.opendata.airquality.jstruct/schemas/fi.fmi.opendata.airquality.Observation`](#schema-fifmiopendataairqualityobservation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.fmi.opendata.airquality.Observation` |
| `source` |  | `uritemplate` | `False` | `https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=urban::observations::airquality::hourly::simple` |
| `subject` |  | `uritemplate` | `False` | `{fmisid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.fmi.opendata.airquality.Kafka` | `KAFKA` | topic `fmi-finland-airquality`; key `{fmisid}` |

## Schemagroups

### Schemagroup `fi.fmi.opendata.airquality.jstruct`
<a id="schemagroup-fifmiopendataairqualityjstruct"></a>

#### Schema `fi.fmi.opendata.airquality.Station`
<a id="schema-fifmiopendataairqualitystation"></a>

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
| $id | `https://opendata.fmi.fi/schemas/fi/fmi/opendata/airquality/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/fi/fmi/opendata/airquality/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for an FMI air quality monitoring station. The station identifier is the FMI station identifier (fmisid). Municipality is taken from the WFS station metadata region name, and coordinates are the representative point published by FMI.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fmisid` | `string` | `True` | Stable FMI station identifier (fmisid) used as the Kafka key and CloudEvents subject. | - | pattern=`^[0-9]+$` | - |
| `station_name` | `string` | `True` | Air quality station name from the FMI station metadata, for example 'Helsinki Kallio 2'. | - | - | - |
| `latitude` | `double` | `True` | WGS84 latitude of the station representative point in decimal degrees. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | WGS84 longitude of the station representative point in decimal degrees. | unit=`degree` symbol=`°` | - | - |
| `municipality` | `union` | `True` | Municipality or region name from the station metadata if FMI publishes it. Null when it is not available in the station record. | - | - | - |

#### Schema `fi.fmi.opendata.airquality.Observation`
<a id="schema-fifmiopendataairqualityobservation"></a>

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
| $id | `https://opendata.fmi.fi/schemas/fi/fmi/opendata/airquality/Observation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/fi/fmi/opendata/airquality/Observation` |
| Type | `object` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Hourly FMI air quality observation aggregated per station and observation timestamp from the urban::observations::airquality::hourly::simple stored query. Each event combines all supported pollutant and index parameters published for the station and hour.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fmisid` | `string` | `True` | Stable FMI station identifier (fmisid) for the observing station. | - | pattern=`^[0-9]+$` | - |
| `station_name` | `string` | `True` | Station name resolved from station metadata or, if metadata lookup fails, the station identifier string. | - | - | - |
| `observation_time` | `string` | `True` | Observation timestamp in UTC, formatted as an ISO-8601 instant such as 2024-01-15T13:00:00Z. | - | pattern=`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$` | - |
| `aqindex` | `union` | `True` | Finnish Air Quality Index 1-hour average from the AQINDEX_PT1H_avg parameter. Null when FMI reports the parameter as missing or not available. | altnames=`{"json": "AQINDEX_PT1H_avg"}` | - | - |
| `pm10_ug_m3` | `union` | `True` | PM10 particulate matter concentration 1-hour average in micrograms per cubic meter from the PM10_PT1H_avg parameter. Null when the value is missing. | unit=`µg/m³`<br>altnames=`{"json": "PM10_PT1H_avg"}` | - | - |
| `pm2_5_ug_m3` | `union` | `True` | PM2.5 particulate matter concentration 1-hour average in micrograms per cubic meter from the PM25_PT1H_avg parameter. Null when the value is missing. | unit=`µg/m³`<br>altnames=`{"json": "PM25_PT1H_avg"}` | - | - |
| `no2_ug_m3` | `union` | `True` | Nitrogen dioxide concentration 1-hour average in micrograms per cubic meter from the NO2_PT1H_avg parameter. Null when the value is missing. | unit=`µg/m³`<br>altnames=`{"json": "NO2_PT1H_avg"}` | - | - |
| `o3_ug_m3` | `union` | `True` | Ozone concentration 1-hour average in micrograms per cubic meter from the O3_PT1H_avg parameter. Null when the value is missing. | unit=`µg/m³`<br>altnames=`{"json": "O3_PT1H_avg"}` | - | - |
| `so2_ug_m3` | `union` | `True` | Sulfur dioxide concentration 1-hour average in micrograms per cubic meter from the SO2_PT1H_avg parameter. Null when the value is missing. | unit=`µg/m³`<br>altnames=`{"json": "SO2_PT1H_avg"}` | - | - |
| `co_mg_m3` | `union` | `True` | Carbon monoxide concentration 1-hour average in milligrams per cubic meter from the CO_PT1H_avg parameter. Null when the value is missing. | unit=`mg/m³`<br>altnames=`{"json": "CO_PT1H_avg"}` | - | - |

### Schemagroup `fi.fmi.opendata.airquality.avro`
<a id="schemagroup-fifmiopendataairqualityavro"></a>

#### Schema `fi.fmi.opendata.airquality.Station`
<a id="schema-fifmiopendataairqualitystation"></a>

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
| Namespace | fi.fmi.opendata.airquality |
| Type | `record` |
| Doc | Reference data for an FMI air quality monitoring station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fmisid` | `string` | Stable FMI station identifier (fmisid) used as the Kafka key and CloudEvents subject. | `-` |
| `station_name` | `string` | Air quality station name from the FMI station metadata. | `-` |
| `latitude` | `double` | WGS84 latitude of the station representative point in decimal degrees. | `-` |
| `longitude` | `double` | WGS84 longitude of the station representative point in decimal degrees. | `-` |
| `municipality` | `null` \| `string` | Municipality or region name from the station metadata if available. | `-` |

#### Schema `fi.fmi.opendata.airquality.Observation`
<a id="schema-fifmiopendataairqualityobservation"></a>

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
| Namespace | fi.fmi.opendata.airquality |
| Type | `record` |
| Doc | Hourly FMI air quality observation aggregated per station and timestamp. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fmisid` | `string` | Stable FMI station identifier (fmisid) for the observing station. | `-` |
| `station_name` | `string` | Station name resolved from station metadata or, if metadata lookup fails, the station identifier string. | `-` |
| `observation_time` | `string` | Observation timestamp in UTC, formatted as an ISO-8601 instant such as 2024-01-15T13:00:00Z. | `-` |
| `aqindex` | `null` \| `double` | Finnish Air Quality Index 1-hour average. | `-` |
| `pm10_ug_m3` | `null` \| `double` | PM10 particulate matter concentration 1-hour average in micrograms per cubic meter. | `-` |
| `pm2_5_ug_m3` | `null` \| `double` | PM2.5 particulate matter concentration 1-hour average in micrograms per cubic meter. | `-` |
| `no2_ug_m3` | `null` \| `double` | Nitrogen dioxide concentration 1-hour average in micrograms per cubic meter. | `-` |
| `o3_ug_m3` | `null` \| `double` | Ozone concentration 1-hour average in micrograms per cubic meter. | `-` |
| `so2_ug_m3` | `null` \| `double` | Sulfur dioxide concentration 1-hour average in micrograms per cubic meter. | `-` |
| `co_mg_m3` | `null` \| `double` | Carbon monoxide concentration 1-hour average in milligrams per cubic meter. | `-` |
