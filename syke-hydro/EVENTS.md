# SYKE Hydrology Bridge Usage Guide Events

**SYKE Hydrology Bridge** connects to the Finnish Environment Institute's (SYKE) hydrological monitoring network — via the [Hydrology OData API](https://rajapinnat.ymparisto.fi/api/Hydrologiarajapinta/1.1/odata) — and forwards water level and discharge observations to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format.

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

### Endpoint `FI.SYKE.Hydrology.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`FI.SYKE.Hydrology`](#messagegroup-fisykehydrology) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `syke-hydro` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `FI.SYKE.Hydrology`
<a id="messagegroup-fisykehydrology"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `FI.SYKE.Hydrology.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `FI.SYKE.Hydrology.Station`
<a id="message-fisykehydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FI.SYKE.Hydrology.jstruct/schemas/FI.SYKE.Hydrology.Station`](#schema-fisykehydrologystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FI.SYKE.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://rajapinnat.ymparisto.fi` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FI.SYKE.Hydrology.Kafka` | `KAFKA` | topic `syke-hydro`; key `{station_id}` |

#### Message `FI.SYKE.Hydrology.WaterLevelObservation`
<a id="message-fisykehydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FI.SYKE.Hydrology.jstruct/schemas/FI.SYKE.Hydrology.WaterLevelObservation`](#schema-fisykehydrologywaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FI.SYKE.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://rajapinnat.ymparisto.fi` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FI.SYKE.Hydrology.Kafka` | `KAFKA` | topic `syke-hydro`; key `{station_id}` |

## Schemagroups

### Schemagroup `FI.SYKE.Hydrology.jstruct`
<a id="schemagroup-fisykehydrologyjstruct"></a>

#### Schema `FI.SYKE.Hydrology.Station`
<a id="schema-fisykehydrologystation"></a>

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
| $id | `https://example.com/schemas/FI/SYKE/Hydrology/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/FI/SYKE/Hydrology/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:fi": "Paikka_Id"}` | - | - |
| `name` | `string` | `True` |  | altnames=`{"lang:fi": "Nimi"}` | - | - |
| `river_name` | `string` | `False` |  | altnames=`{"lang:fi": "PaaVesalNimi"}` | - | - |
| `water_area_name` | `string` | `False` |  | altnames=`{"lang:fi": "VesalNimi"}` | - | - |
| `municipality` | `string` | `False` |  | altnames=`{"lang:fi": "KuntaNimi"}` | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |

#### Schema `FI.SYKE.Hydrology.WaterLevelObservation`
<a id="schema-fisykehydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/FI/SYKE/Hydrology/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/FI/SYKE/Hydrology/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:fi": "Paikka_Id"}` | - | - |
| `water_level` | `union` | `False` | Water level reading value in centimetres. Null when the station does not report a water level in the current polling window. | altnames=`{"lang:fi": "Arvo"}` | - | - |
| `water_level_unit` | `union` | `False` | Unit of measurement for water_level. Constant 'cm' when present, null when water_level is null. | - | - | - |
| `water_level_timestamp` | `union` | `False` | RFC3339 UTC timestamp (with 'Z' suffix) of the water level observation, derived from the SYKE 'Aika' field. Null when no water level is available. | altnames=`{"lang:fi": "Aika"}` | - | - |
| `discharge` | `union` | `False` | Discharge (flow) reading value in cubic metres per second. Null for stations that do not measure discharge. | altnames=`{"lang:fi": "Arvo"}` | - | - |
| `discharge_unit` | `union` | `False` | Unit of measurement for discharge. Constant 'm3/s' when present, null when discharge is null. | - | - | - |
| `discharge_timestamp` | `union` | `False` | RFC3339 UTC timestamp (with 'Z' suffix) of the discharge observation, derived from the SYKE 'Aika' field. Null when no discharge is available. | altnames=`{"lang:fi": "Aika"}` | - | - |

### Schemagroup `FI.SYKE.Hydrology.avro`
<a id="schemagroup-fisykehydrologyavro"></a>

#### Schema `FI.SYKE.Hydrology.Station`
<a id="schema-fisykehydrologystation"></a>

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
| Namespace | FI.SYKE.Hydrology |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `name` | `string` |  | `-` |
| `river_name` | `null` \| `string` |  | `-` |
| `water_area_name` | `null` \| `string` |  | `-` |
| `municipality` | `null` \| `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

#### Schema `FI.SYKE.Hydrology.WaterLevelObservation`
<a id="schema-fisykehydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Namespace | FI.SYKE.Hydrology |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `water_level` | `null` \| `double` |  | `-` |
| `water_level_unit` | `null` \| `string` |  | `-` |
| `water_level_timestamp` | `null` \| `string` |  | `-` |
| `discharge` | `null` \| `double` |  | `-` |
| `discharge_unit` | `null` \| `string` |  | `-` |
| `discharge_timestamp` | `null` \| `string` |  | `-` |
