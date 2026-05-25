# Ireland OPW waterlevel.ie Bridge Events

This project provides a bridge that reads real-time water level, temperature, and voltage data from Ireland's OPW (Office of Public Works) hydrometric stations via the [waterlevel.ie](https://waterlevel.ie) GeoJSON API and emits the data as CloudEvents to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

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

### Endpoint `ie.gov.opw.waterlevel.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`ie.gov.opw.waterlevel`](#messagegroup-iegovopwwaterlevel) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ireland-opw-waterlevel` |
| Kafka key | `{station_ref}` |
| Deployed | False |

## Messagegroups

### Messagegroup `ie.gov.opw.waterlevel`
<a id="messagegroup-iegovopwwaterlevel"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `ie.gov.opw.waterlevel.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `ie.gov.opw.waterlevel.Station`
<a id="message-iegovopwwaterlevelstation"></a>

Reference data for an OPW hydrometric station in Ireland, including location and region.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/ie.gov.opw.waterlevel.jstruct/schemas/ie.gov.opw.waterlevel.Station`](#schema-iegovopwwaterlevelstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `ie.gov.opw.waterlevel.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_ref}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `ie.gov.opw.waterlevel.Kafka` | `KAFKA` | topic `ireland-opw-waterlevel`; key `{station_ref}` |

#### Message `ie.gov.opw.waterlevel.WaterLevelReading`
<a id="message-iegovopwwaterlevelwaterlevelreading"></a>

A sensor reading from an OPW hydrometric station, covering water level, temperature, voltage, or Ordnance Datum.

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/ie.gov.opw.waterlevel.jstruct/schemas/ie.gov.opw.waterlevel.WaterLevelReading`](#schema-iegovopwwaterlevelwaterlevelreading) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `ie.gov.opw.waterlevel.WaterLevelReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_ref}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `ie.gov.opw.waterlevel.Kafka` | `KAFKA` | topic `ireland-opw-waterlevel`; key `{station_ref}` |

## Schemagroups

### Schemagroup `ie.gov.opw.waterlevel.jstruct`
<a id="schemagroup-iegovopwwaterleveljstruct"></a>

#### Schema `ie.gov.opw.waterlevel.Station`
<a id="schema-iegovopwwaterlevelstation"></a>

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
| $id | `https://example.com/schemas/ie/gov/opw/waterlevel/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/ie/gov/opw/waterlevel/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for an OPW hydrometric station in Ireland, including location and region.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_ref` | `string` | `True` | Zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041'). | - | - | - |
| `station_name` | `string` | `True` | Human-readable name of the hydrometric station (e.g. 'Sandy Mills'). | - | - | - |
| `region_id` | `int32` | `True` | Integer identifier of the OPW hydrometric region the station belongs to. | - | - | - |
| `longitude` | `double` | `True` | Longitude of the station location in WGS84 decimal degrees. | - | - | - |
| `latitude` | `double` | `True` | Latitude of the station location in WGS84 decimal degrees. | - | - | - |

#### Schema `ie.gov.opw.waterlevel.WaterLevelReading`
<a id="schema-iegovopwwaterlevelwaterlevelreading"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/ie/gov/opw/waterlevel/WaterLevelReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/ie/gov/opw/waterlevel/WaterLevelReading` |
| Type | `object` |

###### Object `WaterLevelReading`
<a id="schema-node-waterlevelreading"></a>

A sensor reading from an OPW hydrometric station, covering water level, temperature, voltage, or Ordnance Datum.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_ref` | `string` | `True` | Zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041'). | - | - | - |
| `station_name` | `string` | `True` | Human-readable name of the hydrometric station (e.g. 'Sandy Mills'). | - | - | - |
| `sensor_ref` | `string` | `True` | Sensor reference code identifying the measurement type: '0001' for water level (metres), '0002' for temperature (degrees Celsius), '0003' for voltage (volts), 'OD' for Ordnance Datum level (metres). | - | - | - |
| `value` | `union` | `True` | Numeric sensor reading value. Units depend on sensor_ref: metres for water level ('0001') and OD ('OD'), degrees Celsius for temperature ('0002'), volts for voltage ('0003'). Null if the value could not be parsed from the upstream string representation. | - | - | - |
| `datetime` | `string` | `True` | ISO 8601 timestamp of the sensor reading as provided by the upstream API (e.g. '2024-01-15T12:00:00Z'). | - | - | - |
| `err_code` | `int32` | `True` | Upstream error code for the reading. A value of 99 indicates the reading is valid (OK). Other values indicate various error conditions. | - | - | - |

### Schemagroup `ie.gov.opw.waterlevel.avro`
<a id="schemagroup-iegovopwwaterlevelavro"></a>

#### Schema `ie.gov.opw.waterlevel.Station`
<a id="schema-iegovopwwaterlevelstation"></a>

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
| Namespace | ie.gov.opw.waterlevel |
| Type | `record` |
| Doc | Reference data for an OPW hydrometric station in Ireland, including location and region. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_ref` | `string` | Zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041'). | `-` |
| `station_name` | `string` | Human-readable name of the hydrometric station (e.g. 'Sandy Mills'). | `-` |
| `region_id` | `int` | Integer identifier of the OPW hydrometric region the station belongs to. | `-` |
| `longitude` | `double` | Longitude of the station location in WGS84 decimal degrees. | `-` |
| `latitude` | `double` | Latitude of the station location in WGS84 decimal degrees. | `-` |

#### Schema `ie.gov.opw.waterlevel.WaterLevelReading`
<a id="schema-iegovopwwaterlevelwaterlevelreading"></a>

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
| Name | WaterLevelReading |
| Namespace | ie.gov.opw.waterlevel |
| Type | `record` |
| Doc | A sensor reading from an OPW hydrometric station, covering water level, temperature, voltage, or Ordnance Datum. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_ref` | `string` | Zero-padded 10-digit station reference code uniquely identifying the hydrometric station (e.g. '0000001041'). | `-` |
| `station_name` | `string` | Human-readable name of the hydrometric station (e.g. 'Sandy Mills'). | `-` |
| `sensor_ref` | `string` | Sensor reference code identifying the measurement type: '0001' for water level (metres), '0002' for temperature (degrees Celsius), '0003' for voltage (volts), 'OD' for Ordnance Datum level (metres). | `-` |
| `value` | `null` \| `double` | Numeric sensor reading value. Units depend on sensor_ref: metres for water level ('0001') and OD ('OD'), degrees Celsius for temperature ('0002'), volts for voltage ('0003'). Null if the value could not be parsed from the upstream string representation. | `-` |
| `datetime` | `string` | ISO 8601 timestamp of the sensor reading as provided by the upstream API (e.g. '2024-01-15T12:00:00Z'). | `-` |
| `err_code` | `int` | Upstream error code for the reading. A value of 99 indicates the reading is valid (OK). Other values indicate various error conditions. | `-` |
