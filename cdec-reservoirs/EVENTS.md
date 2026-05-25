# CDEC California Reservoirs Bridge Events

This source bridges real-time reservoir data from the California Data Exchange Center (CDEC) to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

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

### Endpoint `gov.ca.water.cdec.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`gov.ca.water.cdec`](#messagegroup-govcawatercdec) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `cdec-reservoirs` |
| Kafka key | `{station_id}/{sensor_num}` |
| Deployed | False |

## Messagegroups

### Messagegroup `gov.ca.water.cdec`
<a id="messagegroup-govcawatercdec"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `gov.ca.water.cdec.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `gov.ca.water.cdec.ReservoirReading`
<a id="message-govcawatercdecreservoirreading"></a>

A single sensor reading from a CDEC reservoir station, representing an hourly (or sub-hourly) observation of storage, elevation, inflow, outflow, or river stage. Each reading corresponds to one station/sensor/timestamp combination as reported by the California Data Exchange Center JSON Data Servlet.

| Field | Value |
| --- | --- |
| Name | ReservoirReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.ca.water.cdec.jstruct/schemas/gov.ca.water.cdec.ReservoirReading`](#schema-govcawatercdecreservoirreading) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.ca.water.cdec.ReservoirReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{sensor_num}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.ca.water.cdec.Kafka` | `KAFKA` | topic `cdec-reservoirs`; key `{station_id}/{sensor_num}` |

## Schemagroups

### Schemagroup `gov.ca.water.cdec.jstruct`
<a id="schemagroup-govcawatercdecjstruct"></a>

#### Schema `gov.ca.water.cdec.ReservoirReading`
<a id="schema-govcawatercdecreservoirreading"></a>

| Field | Value |
| --- | --- |
| Name | ReservoirReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/gov/ca/water/cdec/ReservoirReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/gov/ca/water/cdec/ReservoirReading` |
| Type | `object` |

###### Object `ReservoirReading`
<a id="schema-node-reservoirreading"></a>

A single sensor reading from a CDEC reservoir station. The California Data Exchange Center (CDEC) publishes hourly and sub-hourly observations for over 2,600 stations across California. Each reading captures one measurement for a specific station, sensor type, and timestamp.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Three-letter CDEC station identifier (e.g. SHA for Shasta Dam, ORO for Oroville Dam, FOL for Folsom Dam). This is the primary key for the monitoring station and is immutable. | - | - | - |
| `sensor_num` | `int32` | `True` | CDEC numeric sensor identifier. Standard sensor numbers: 15=STORAGE (acre-feet), 6=RESERVOIR ELEVATION (feet), 76=INFLOW (cubic feet per second), 23=OUTFLOW (cubic feet per second), 1=RIVER STAGE (feet). | - | - | - |
| `sensor_type` | `string` | `True` | Human-readable sensor type label as returned by the CDEC API (e.g. 'STORAGE', 'RES ELE', 'INFLOW', 'OUTFLOW', 'STAGE'). | - | - | - |
| `value` | `union` | `True` | Observed measurement value in the units specified by the 'units' field. Null when no observation is available or when the upstream reports the sentinel value -9999. | - | - | - |
| `units` | `string` | `True` | Engineering units of the measurement as reported by CDEC (e.g. 'AF' for acre-feet, 'FEET' for feet, 'CFS' for cubic feet per second). | - | - | - |
| `date` | `string` | `True` | Observation timestamp as reported by CDEC in PST (Pacific Standard Time, UTC-8). Format from the API is 'YYYY-M-D H:MM' and is normalized to ISO 8601 format 'YYYY-MM-DDTHH:MM:SS-08:00'. CDEC always reports in PST regardless of daylight saving time. | - | - | - |
| `dur_code` | `string` | `True` | Duration code indicating the measurement interval. 'H' for hourly observations, 'D' for daily observations, 'E' for event-based (15-minute or irregular). | - | - | - |
| `data_flag` | `string` | `True` | Quality flag character applied to the observation by CDEC. A single space ' ' means no flag (normal data). Other values indicate provisional, edited, or suspect data. | - | - | - |

### Schemagroup `gov.ca.water.cdec.avro`
<a id="schemagroup-govcawatercdecavro"></a>

#### Schema `gov.ca.water.cdec.ReservoirReading`
<a id="schema-govcawatercdecreservoirreading"></a>

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
| Name | ReservoirReading |
| Namespace | gov.ca.water.cdec |
| Type | `record` |
| Doc | A single sensor reading from a CDEC reservoir station. The California Data Exchange Center (CDEC) publishes hourly and sub-hourly observations for over 2,600 stations across California. Each reading captures one measurement for a specific station, sensor type, and timestamp. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Three-letter CDEC station identifier (e.g. SHA for Shasta Dam, ORO for Oroville Dam, FOL for Folsom Dam). This is the primary key for the monitoring station and is immutable. | `-` |
| `sensor_num` | `int` | CDEC numeric sensor identifier. Standard sensor numbers: 15=STORAGE (acre-feet), 6=RESERVOIR ELEVATION (feet), 76=INFLOW (cubic feet per second), 23=OUTFLOW (cubic feet per second), 1=RIVER STAGE (feet). | `-` |
| `sensor_type` | `string` | Human-readable sensor type label as returned by the CDEC API (e.g. 'STORAGE', 'RES ELE', 'INFLOW', 'OUTFLOW', 'STAGE'). | `-` |
| `value` | `null` \| `double` | Observed measurement value in the units specified by the 'units' field. Null when no observation is available or when the upstream reports the sentinel value -9999. | `-` |
| `units` | `string` | Engineering units of the measurement as reported by CDEC (e.g. 'AF' for acre-feet, 'FEET' for feet, 'CFS' for cubic feet per second). | `-` |
| `date` | `string` | Observation timestamp as reported by CDEC in PST (Pacific Standard Time, UTC-8). Format from the API is 'YYYY-M-D H:MM' and is normalized to ISO 8601 format 'YYYY-MM-DDTHH:MM:SS-08:00'. CDEC always reports in PST regardless of daylight saving time. | `-` |
| `dur_code` | `string` | Duration code indicating the measurement interval. 'H' for hourly observations, 'D' for daily observations, 'E' for event-based (15-minute or irregular). | `-` |
| `data_flag` | `string` | Quality flag character applied to the observation by CDEC. A single space ' ' means no flag (normal data). Other values indicate provisional, edited, or suspect data. | `-` |
