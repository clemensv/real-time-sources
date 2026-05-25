# Nepal BIPAD Portal — Real-Time River Monitoring Bridge Events

This project provides a bridge between the [Nepal BIPAD Portal](https://bipadportal.gov.np/) river monitoring API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams.

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

### Endpoint `np.gov.bipad.hydrology.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`np.gov.bipad.hydrology`](#messagegroup-npgovbipadhydrology) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `nepal-bipad-hydrology` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `np.gov.bipad.hydrology`
<a id="messagegroup-npgovbipadhydrology"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `np.gov.bipad.hydrology.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `np.gov.bipad.hydrology.RiverStation`
<a id="message-npgovbipadhydrologyriverstation"></a>

Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds.

| Field | Value |
| --- | --- |
| Name | RiverStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/np.gov.bipad.hydrology.jstruct/schemas/np.gov.bipad.hydrology.RiverStation`](#schema-npgovbipadhydrologyriverstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `np.gov.bipad.hydrology.RiverStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `np.gov.bipad.hydrology.Kafka` | `KAFKA` | topic `nepal-bipad-hydrology`; key `{station_id}` |

#### Message `np.gov.bipad.hydrology.WaterLevelReading`
<a id="message-npgovbipadhydrologywaterlevelreading"></a>

Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal, including current water level, alert status, and trend direction.

| Field | Value |
| --- | --- |
| Name | WaterLevelReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/np.gov.bipad.hydrology.jstruct/schemas/np.gov.bipad.hydrology.WaterLevelReading`](#schema-npgovbipadhydrologywaterlevelreading) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `np.gov.bipad.hydrology.WaterLevelReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `np.gov.bipad.hydrology.Kafka` | `KAFKA` | topic `nepal-bipad-hydrology`; key `{station_id}` |

## Schemagroups

### Schemagroup `np.gov.bipad.hydrology.jstruct`
<a id="schemagroup-npgovbipadhydrologyjstruct"></a>

#### Schema `np.gov.bipad.hydrology.RiverStation`
<a id="schema-npgovbipadhydrologyriverstation"></a>

| Field | Value |
| --- | --- |
| Name | RiverStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://bipadportal.gov.np/schemas/np/gov/bipad/hydrology/RiverStation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/np/gov/bipad/hydrology/RiverStation` |
| Type | `object` |

###### Object `RiverStation`
<a id="schema-node-riverstation"></a>

Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility. | - | - | - |
| `title` | `string` | `True` | Human-readable name of the river station, typically in the format 'River at Location' (e.g. 'Babai at Chepang'). | - | - | - |
| `basin` | `string` | `True` | Name of the river basin the station belongs to (e.g. 'Bagmati', 'Narayani', 'Koshi', 'Karnali', 'Mahakali', 'Babai'). | - | - | - |
| `latitude` | `double` | `True` | Latitude coordinate of the station in WGS84 decimal degrees, extracted from the GeoJSON point geometry. | - | - | - |
| `longitude` | `double` | `True` | Longitude coordinate of the station in WGS84 decimal degrees, extracted from the GeoJSON point geometry. | - | - | - |
| `elevation` | `union` | `False` | Elevation of the station in meters above sea level, as reported by the BIPAD portal. Null when not available. | - | - | - |
| `danger_level` | `union` | `False` | Configured danger water level threshold in meters for the station. Water levels above this indicate a danger condition. Null when not configured. | - | - | - |
| `warning_level` | `union` | `False` | Configured warning water level threshold in meters for the station. Water levels above this indicate a warning condition. Null when not configured. | - | - | - |
| `description` | `union` | `False` | Free-text description of the station, may include historical notes, relocation history, or elevation corrections. Null when not provided. | - | - | - |
| `data_source` | `string` | `True` | Origin system providing the station data, typically 'hydrology.gov.np' for Nepal Department of Hydrology and Meteorology stations. | - | - | - |
| `province` | `union` | `False` | Nepal province administrative code for the station location. Null when not assigned. | - | - | - |
| `district` | `union` | `False` | Nepal district administrative code for the station location. Null when not assigned. | - | - | - |
| `municipality` | `union` | `False` | Nepal municipality or rural municipality administrative code for the station location. Null when not assigned. | - | - | - |
| `ward` | `union` | `False` | Nepal ward-level administrative code for the station location. Null when not assigned. | - | - | - |

#### Schema `np.gov.bipad.hydrology.WaterLevelReading`
<a id="schema-npgovbipadhydrologywaterlevelreading"></a>

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
| $id | `https://bipadportal.gov.np/schemas/np/gov/bipad/hydrology/WaterLevelReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/np/gov/bipad/hydrology/WaterLevelReading` |
| Type | `object` |

###### Object `WaterLevelReading`
<a id="schema-node-waterlevelreading"></a>

Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal, including current water level, alert status, and trend direction.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility. | - | - | - |
| `title` | `string` | `True` | Human-readable name of the river station at the time of the reading. | - | - | - |
| `basin` | `string` | `True` | Name of the river basin the station belongs to at the time of the reading. | - | - | - |
| `water_level` | `union` | `False` | Current water level at the station in meters. Null when the station has no current reading available. | - | - | - |
| `danger_level` | `union` | `False` | Configured danger water level threshold in meters. Null when not configured. | - | - | - |
| `warning_level` | `union` | `False` | Configured warning water level threshold in meters. Null when not configured. | - | - | - |
| `status` | `string` | `True` | Current alert status of the station relative to configured thresholds. Known values: 'BELOW WARNING LEVEL', 'WARNING', 'DANGER'. | - | - | - |
| `trend` | `string` | `True` | Direction of water level change. Known values: 'STEADY', 'RISING', 'FALLING'. | - | - | - |
| `water_level_on` | `string` | `True` | ISO 8601 timestamp of when the water level was measured, in Nepal Standard Time (+05:45). | - | - | - |

### Schemagroup `np.gov.bipad.hydrology.avro`
<a id="schemagroup-npgovbipadhydrologyavro"></a>

#### Schema `np.gov.bipad.hydrology.RiverStation`
<a id="schema-npgovbipadhydrologyriverstation"></a>

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
| Name | RiverStation |
| Namespace | np.gov.bipad.hydrology |
| Type | `record` |
| Doc | Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility. | `-` |
| `title` | `string` | Human-readable name of the river station, typically in the format 'River at Location'. | `-` |
| `basin` | `string` | Name of the river basin the station belongs to. | `-` |
| `latitude` | `double` | Latitude coordinate of the station in WGS84 decimal degrees. | `-` |
| `longitude` | `double` | Longitude coordinate of the station in WGS84 decimal degrees. | `-` |
| `elevation` | `null` \| `int` | Elevation of the station in meters above sea level. Null when not available. | `-` |
| `danger_level` | `null` \| `double` | Configured danger water level threshold in meters. Null when not configured. | `-` |
| `warning_level` | `null` \| `double` | Configured warning water level threshold in meters. Null when not configured. | `-` |
| `description` | `null` \| `string` | Free-text description of the station. Null when not provided. | `-` |
| `data_source` | `string` | Origin system providing the station data, typically 'hydrology.gov.np'. | `-` |
| `province` | `null` \| `int` | Nepal province administrative code. Null when not assigned. | `-` |
| `district` | `null` \| `int` | Nepal district administrative code. Null when not assigned. | `-` |
| `municipality` | `null` \| `int` | Nepal municipality administrative code. Null when not assigned. | `-` |
| `ward` | `null` \| `int` | Nepal ward-level administrative code. Null when not assigned. | `-` |

#### Schema `np.gov.bipad.hydrology.WaterLevelReading`
<a id="schema-npgovbipadhydrologywaterlevelreading"></a>

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
| Namespace | np.gov.bipad.hydrology |
| Type | `record` |
| Doc | Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Unique integer identifier of the river station. | `-` |
| `title` | `string` | Human-readable name of the river station at the time of the reading. | `-` |
| `basin` | `string` | Name of the river basin the station belongs to. | `-` |
| `water_level` | `null` \| `double` | Current water level at the station in meters. Null when no reading available. | `-` |
| `danger_level` | `null` \| `double` | Configured danger water level threshold in meters. Null when not configured. | `-` |
| `warning_level` | `null` \| `double` | Configured warning water level threshold in meters. Null when not configured. | `-` |
| `status` | `string` | Current alert status: 'BELOW WARNING LEVEL', 'WARNING', or 'DANGER'. | `-` |
| `trend` | `string` | Direction of water level change: 'STEADY', 'RISING', or 'FALLING'. | `-` |
| `water_level_on` | `string` | ISO 8601 timestamp of when the water level was measured. | `-` |
