# GIOŚ Poland Air Quality Poller Events

**GIOŚ Poland Air Quality Poller** polls the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality API for station metadata, sensor reference data, hourly measurements, and air quality index values, and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen measurement timestamps per sensor to avoid sending duplicates.

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

### Endpoint `pl.gov.gios.airquality.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`pl.gov.gios.airquality`](#messagegroup-plgovgiosairquality) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `gios-poland` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `pl.gov.gios.airquality`
<a id="messagegroup-plgovgiosairquality"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `pl.gov.gios.airquality.Kafka` (KAFKA) |
| Messages | 4 |

#### Message `pl.gov.gios.airquality.Station`
<a id="message-plgovgiosairqualitystation"></a>

Reference data for a GIOŚ air quality monitoring station, including its geographic location, city, commune, district, and voivodeship.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/pl.gov.gios.airquality.jstruct/schemas/pl.gov.gios.airquality.Station`](#schema-plgovgiosairqualitystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `pl.gov.gios.airquality.Station` |
| `source` |  | `string` | `False` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `pl.gov.gios.airquality.Kafka` | `KAFKA` | topic `gios-poland`; key `{station_id}` |

#### Message `pl.gov.gios.airquality.Sensor`
<a id="message-plgovgiosairqualitysensor"></a>

Reference data for a sensor (measurement point) installed at a GIOŚ station, identifying the pollutant it measures.

| Field | Value |
| --- | --- |
| Name | Sensor |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/pl.gov.gios.airquality.jstruct/schemas/pl.gov.gios.airquality.Sensor`](#schema-plgovgiosairqualitysensor) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `pl.gov.gios.airquality.Sensor` |
| `source` |  | `string` | `False` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `pl.gov.gios.airquality.Kafka` | `KAFKA` | topic `gios-poland`; key `{station_id}` |

#### Message `pl.gov.gios.airquality.Measurement`
<a id="message-plgovgiosairqualitymeasurement"></a>

Hourly air quality measurement from a single sensor, reporting the concentration of the monitored pollutant in µg/m³.

| Field | Value |
| --- | --- |
| Name | Measurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/pl.gov.gios.airquality.jstruct/schemas/pl.gov.gios.airquality.Measurement`](#schema-plgovgiosairqualitymeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `pl.gov.gios.airquality.Measurement` |
| `source` |  | `string` | `False` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `pl.gov.gios.airquality.Kafka` | `KAFKA` | topic `gios-poland`; key `{station_id}` |

#### Message `pl.gov.gios.airquality.AirQualityIndex`
<a id="message-plgovgiosairqualityairqualityindex"></a>

Current Polish Air Quality Index for a station, including the overall index and sub-indices for individual pollutants (SO₂, NO₂, PM10, PM2.5, O₃).

| Field | Value |
| --- | --- |
| Name | AirQualityIndex |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/pl.gov.gios.airquality.jstruct/schemas/pl.gov.gios.airquality.AirQualityIndex`](#schema-plgovgiosairqualityairqualityindex) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `pl.gov.gios.airquality.AirQualityIndex` |
| `source` |  | `string` | `False` | `https://api.gios.gov.pl/pjp-api/v1/rest/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `pl.gov.gios.airquality.Kafka` | `KAFKA` | topic `gios-poland`; key `{station_id}` |

## Schemagroups

### Schemagroup `pl.gov.gios.airquality.jstruct`
<a id="schemagroup-plgovgiosairqualityjstruct"></a>

#### Schema `pl.gov.gios.airquality.Station`
<a id="schema-plgovgiosairqualitystation"></a>

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
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference record for a GIOŚ air quality monitoring station in Poland. Contains the station identifier, code, name, WGS84 coordinates, and administrative location (city, commune, district, voivodeship, street). Fields are mapped from the Polish-language GIOŚ REST API /station/findAll endpoint.

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `integer` | `True` | Unique numeric identifier of the monitoring station assigned by GIOŚ. Mapped from the Polish field 'Identyfikator stacji'. | - | - | - |
| `station_code` | `string` | `True` | Short alphanumeric code uniquely identifying the station, e.g. 'DsLegAlRzecz'. Mapped from 'Kod stacji'. | - | - | - |
| `name` | `string` | `True` | Human-readable name of the monitoring station, typically including city and street. Mapped from 'Nazwa stacji'. | - | - | - |
| `latitude` | `union` | `False` | Latitude of the station in decimal degrees north (WGS84). Mapped from 'WGS84 φ N'. | unit=`deg` symbol=`°N` | - | - |
| `longitude` | `union` | `False` | Longitude of the station in decimal degrees east (WGS84). Mapped from 'WGS84 λ E'. | unit=`deg` symbol=`°E` | - | - |
| `city_id` | `union` | `False` | Numeric identifier of the city where the station is located. Mapped from 'Identyfikator miasta'. | - | - | - |
| `city_name` | `union` | `False` | Name of the city where the station is located. Mapped from 'Nazwa miasta'. | - | - | - |
| `commune` | `union` | `False` | Name of the commune (gmina) where the station is located. Mapped from 'Gmina'. | - | - | - |
| `district` | `union` | `False` | Name of the district (powiat) where the station is located. Mapped from 'Powiat'. | - | - | - |
| `voivodeship` | `union` | `False` | Name of the voivodeship (province) where the station is located, in uppercase Polish. Mapped from 'Województwo'. | - | - | - |
| `street` | `union` | `False` | Street address of the station, if available. Mapped from 'Ulica'. | - | - | - |

#### Schema `pl.gov.gios.airquality.Sensor`
<a id="schema-plgovgiosairqualitysensor"></a>

| Field | Value |
| --- | --- |
| Name | Sensor |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/Sensor` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Sensor`
<a id="schema-node-sensor"></a>

Reference record for a sensor installed at a GIOŚ air quality station. Identifies the specific pollutant being measured (e.g. PM10, NO₂, O₃) along with the sensor and station identifiers. Fields are mapped from the Polish-language /station/sensors/{stationId} endpoint.

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/Sensor` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor_id` | `integer` | `True` | Unique numeric identifier of the sensor (measurement point) assigned by GIOŚ. Mapped from 'Identyfikator stanowiska'. | - | - | - |
| `station_id` | `integer` | `True` | Numeric identifier of the parent monitoring station. Mapped from 'Identyfikator stacji'. | - | - | - |
| `parameter_name` | `string` | `True` | Polish-language name of the measured pollutant, e.g. 'pył zawieszony PM10', 'dwutlenek azotu'. Mapped from 'Wskaźnik'. | - | - | - |
| `parameter_formula` | `union` | `False` | Chemical formula of the measured pollutant, e.g. 'PM10', 'NO2', 'SO2', 'O3', 'CO', 'C6H6', 'PM2.5'. Mapped from 'Wskaźnik - wzór'. | - | - | - |
| `parameter_code` | `string` | `True` | Short code identifying the pollutant parameter, e.g. 'PM10', 'NO2'. Mapped from 'Wskaźnik - kod'. | - | - | - |
| `parameter_id` | `union` | `False` | Numeric identifier of the pollutant parameter in the GIOŚ system. Mapped from 'Id wskaźnika'. | - | - | - |

#### Schema `pl.gov.gios.airquality.Measurement`
<a id="schema-plgovgiosairqualitymeasurement"></a>

| Field | Value |
| --- | --- |
| Name | Measurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/Measurement` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Measurement`
<a id="schema-node-measurement"></a>

Hourly air quality measurement from a GIOŚ sensor. Reports the pollutant concentration in µg/m³ at a specific timestamp. The measurement may be null when data is missing or under validation. Fields are mapped from the Polish-language /data/getData/{sensorId} endpoint.

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/Measurement` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `integer` | `True` | Numeric identifier of the monitoring station that owns this sensor. | - | - | - |
| `sensor_id` | `integer` | `True` | Numeric identifier of the sensor that produced this measurement. | - | - | - |
| `sensor_code` | `string` | `True` | Code identifying the sensor and its aggregation period, e.g. 'DsLegAlRzecz-NO2-1g'. Mapped from 'Kod stanowiska'. | - | - | - |
| `timestamp` | `datetime` | `True` | Measurement timestamp in local Polish time (ISO 8601 format). Mapped from 'Data'. | - | - | - |
| `value` | `union` | `False` | Measured pollutant concentration. Unit: micrograms per cubic meter (µg/m³). Null when the measurement is missing or invalid. Mapped from 'Wartość'. | unit=`ug/m3` symbol=`µg/m³` | - | - |

#### Schema `pl.gov.gios.airquality.AirQualityIndex`
<a id="schema-plgovgiosairqualityairqualityindex"></a>

| Field | Value |
| --- | --- |
| Name | AirQualityIndex |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/AirQualityIndex` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AirQualityIndex`
<a id="schema-node-airqualityindex"></a>

Current Polish Air Quality Index (Indeks Jakości Powietrza) for a GIOŚ monitoring station. Includes the overall index value and category plus sub-indices for SO₂, NO₂, PM10, PM2.5, and O₃. Each sub-index uses a 0–5 scale: 0=Bardzo dobry (Very good), 1=Dobry (Good), 2=Umiarkowany (Moderate), 3=Dostateczny (Sufficient), 4=Zły (Bad), 5=Bardzo zły (Very bad). Fields are mapped from the Polish-language /aqindex/getIndex/{stationId} endpoint.

| Field | Value |
| --- | --- |
| $id | `https://api.gios.gov.pl/schemas/pl/gov/gios/airquality/AirQualityIndex` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `integer` | `True` | Numeric identifier of the monitoring station. Mapped from 'Identyfikator stacji pomiarowej'. | - | - | - |
| `calculation_timestamp` | `datetime` | `True` | Timestamp when the overall index was calculated (ISO 8601 in local Polish time). Mapped from 'Data wykonania obliczeń indeksu'. | - | - | - |
| `index_value` | `union` | `False` | Overall air quality index value: 0=Bardzo dobry (Very good), 1=Dobry (Good), 2=Umiarkowany (Moderate), 3=Dostateczny (Sufficient), 4=Zły (Bad), 5=Bardzo zły (Very bad). Mapped from 'Wartość indeksu'. | - | - | - |
| `index_category` | `union` | `False` | Polish-language category name of the overall index, e.g. 'Bardzo dobry', 'Dobry', 'Umiarkowany'. Mapped from 'Nazwa kategorii indeksu'. | - | - | - |
| `source_data_timestamp` | `union` | `False` | Timestamp of the source measurement data used for the overall index calculation. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika st'. | - | - | - |
| `so2_calculation_timestamp` | `union` | `False` | Timestamp when the SO₂ sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika SO2'. | - | - | - |
| `so2_index_value` | `union` | `False` | SO₂ sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika SO2'. | - | - | - |
| `so2_index_category` | `union` | `False` | Polish-language category name for the SO₂ sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika SO2'. | - | - | - |
| `so2_source_data_timestamp` | `union` | `False` | Timestamp of the source data used for the SO₂ sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika SO2'. | - | - | - |
| `no2_calculation_timestamp` | `union` | `False` | Timestamp when the NO₂ sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika NO2'. | - | - | - |
| `no2_index_value` | `union` | `False` | NO₂ sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika NO2'. | - | - | - |
| `no2_index_category` | `union` | `False` | Polish-language category name for the NO₂ sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika NO2'. | - | - | - |
| `no2_source_data_timestamp` | `union` | `False` | Timestamp of the source data used for the NO₂ sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika NO2'. | - | - | - |
| `pm10_calculation_timestamp` | `union` | `False` | Timestamp when the PM10 sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika PM10'. | - | - | - |
| `pm10_index_value` | `union` | `False` | PM10 sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika PM10'. | - | - | - |
| `pm10_index_category` | `union` | `False` | Polish-language category name for the PM10 sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika PM10'. | - | - | - |
| `pm10_source_data_timestamp` | `union` | `False` | Timestamp of the source data used for the PM10 sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM10'. | - | - | - |
| `pm25_calculation_timestamp` | `union` | `False` | Timestamp when the PM2.5 sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika PM2.5'. | - | - | - |
| `pm25_index_value` | `union` | `False` | PM2.5 sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika PM2.5'. | - | - | - |
| `pm25_index_category` | `union` | `False` | Polish-language category name for the PM2.5 sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika PM2.5'. | - | - | - |
| `pm25_source_data_timestamp` | `union` | `False` | Timestamp of the source data used for the PM2.5 sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM2.5'. | - | - | - |
| `o3_calculation_timestamp` | `union` | `False` | Timestamp when the O₃ sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika O3'. | - | - | - |
| `o3_index_value` | `union` | `False` | O₃ sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika O3'. | - | - | - |
| `o3_index_category` | `union` | `False` | Polish-language category name for the O₃ sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika O3'. | - | - | - |
| `o3_source_data_timestamp` | `union` | `False` | Timestamp of the source data used for the O₃ sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika O3'. | - | - | - |
| `overall_status` | `union` | `False` | Whether the overall air quality index is currently valid for this station. Mapped from 'Status indeksu ogólnego dla stacji pomiarowej'. | - | - | - |
| `critical_pollutant_code` | `union` | `False` | Code of the pollutant that determined the overall index value, e.g. 'OZON', 'PM10'. Mapped from 'Kod zanieczyszczenia krytycznego'. | - | - | - |
