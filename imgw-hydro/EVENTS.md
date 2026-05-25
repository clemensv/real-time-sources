# IMGW-PIB Hydrological Data Bridge Events

This bridge fetches real-time hydrological data from the Polish Institute of Meteorology and Water Management (IMGW-PIB) public API and forwards it to Apache Kafka or Microsoft Azure Event Hubs as CloudEvents.

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

### Endpoint `PL.Gov.IMGW.Hydro.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`PL.Gov.IMGW.Hydro`](#messagegroup-plgovimgwhydro) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `imgw-hydro` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `PL.Gov.IMGW.Hydro`
<a id="messagegroup-plgovimgwhydro"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `PL.Gov.IMGW.Hydro.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `PL.Gov.IMGW.Hydro.Station`
<a id="message-plgovimgwhydrostation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/PL.Gov.IMGW.Hydro.jstruct/schemas/PL.Gov.IMGW.Hydro.Station`](#schema-plgovimgwhydrostation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `PL.Gov.IMGW.Hydro.Station` |
| `source` |  | `string` | `False` | `https://danepubliczne.imgw.pl` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `PL.Gov.IMGW.Hydro.Kafka` | `KAFKA` | topic `imgw-hydro`; key `{station_id}` |

#### Message `PL.Gov.IMGW.Hydro.WaterLevelObservation`
<a id="message-plgovimgwhydrowaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/PL.Gov.IMGW.Hydro.jstruct/schemas/PL.Gov.IMGW.Hydro.WaterLevelObservation`](#schema-plgovimgwhydrowaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `PL.Gov.IMGW.Hydro.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://danepubliczne.imgw.pl` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `PL.Gov.IMGW.Hydro.Kafka` | `KAFKA` | topic `imgw-hydro`; key `{station_id}` |

## Schemagroups

### Schemagroup `PL.Gov.IMGW.Hydro.jstruct`
<a id="schemagroup-plgovimgwhydrojstruct"></a>

#### Schema `PL.Gov.IMGW.Hydro.Station`
<a id="schema-plgovimgwhydrostation"></a>

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
| $id | `https://example.com/schemas/PL/Gov/IMGW/Hydro/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/PL/Gov/IMGW/Hydro/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:pl": "id_stacji"}` | - | - |
| `station_name` | `string` | `True` |  | altnames=`{"lang:pl": "stacja"}` | - | - |
| `river` | `union` | `False` |  | altnames=`{"lang:pl": "rzeka"}` | - | - |
| `voivodeship` | `union` | `False` |  | altnames=`{"lang:pl": "wojewodztwo"}` | - | - |
| `longitude` | `union` | `False` |  | - | - | - |
| `latitude` | `union` | `False` |  | - | - | - |

#### Schema `PL.Gov.IMGW.Hydro.WaterLevelObservation`
<a id="schema-plgovimgwhydrowaterlevelobservation"></a>

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
| $id | `https://example.com/schemas/PL/Gov/IMGW/Hydro/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/PL/Gov/IMGW/Hydro/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:pl": "id_stacji"}` | - | - |
| `station_name` | `string` | `True` |  | altnames=`{"lang:pl": "stacja"}` | - | - |
| `river` | `union` | `False` |  | altnames=`{"lang:pl": "rzeka"}` | - | - |
| `voivodeship` | `union` | `False` |  | altnames=`{"lang:pl": "wojewodztwo"}` | - | - |
| `water_level` | `double` | `True` |  | altnames=`{"lang:pl": "stan_wody"}` | - | - |
| `water_level_timestamp` | `datetime` | `True` |  | altnames=`{"lang:pl": "stan_wody_data_pomiaru"}` | - | - |
| `water_temperature` | `union` | `False` |  | altnames=`{"lang:pl": "temperatura_wody"}` | - | - |
| `water_temperature_timestamp` | `union` | `False` |  | altnames=`{"lang:pl": "temperatura_wody_data_pomiaru"}` | - | - |
| `discharge` | `union` | `False` |  | altnames=`{"lang:pl": "przeplyw"}` | - | - |
| `discharge_timestamp` | `union` | `False` |  | altnames=`{"lang:pl": "przeplyw_data"}` | - | - |
| `ice_phenomenon_code` | `union` | `False` |  | altnames=`{"lang:pl": "zjawisko_lodowe"}` | - | - |
| `overgrowth_code` | `union` | `False` |  | altnames=`{"lang:pl": "zjawisko_zarastania"}` | - | - |

### Schemagroup `PL.Gov.IMGW.Hydro.avro`
<a id="schemagroup-plgovimgwhydroavro"></a>

#### Schema `PL.Gov.IMGW.Hydro.Station`
<a id="schema-plgovimgwhydrostation"></a>

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
| Namespace | PL.Gov.IMGW.Hydro |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `river` | `null` \| `string` |  | `-` |
| `voivodeship` | `null` \| `string` |  | `-` |
| `longitude` | `null` \| `double` |  | `-` |
| `latitude` | `null` \| `double` |  | `-` |

#### Schema `PL.Gov.IMGW.Hydro.WaterLevelObservation`
<a id="schema-plgovimgwhydrowaterlevelobservation"></a>

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
| Namespace | PL.Gov.IMGW.Hydro |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `river` | `null` \| `string` |  | `-` |
| `voivodeship` | `null` \| `string` |  | `-` |
| `water_level` | `double` |  | `-` |
| `water_level_timestamp` | `string` |  | `-` |
| `water_temperature` | `null` \| `double` |  | `-` |
| `water_temperature_timestamp` | `null` \| `string` |  | `-` |
| `discharge` | `null` \| `double` |  | `-` |
| `discharge_timestamp` | `null` \| `string` |  | `-` |
| `ice_phenomenon_code` | `null` \| `string` |  | `-` |
| `overgrowth_code` | `null` \| `string` |  | `-` |
