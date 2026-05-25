# Paris Bicycle Counters Poller Events

MQTT/5.0 transport variants for Paris bicycle counters. Topics route by stable MQTT-safe counter_id (upstream id_compteur; values containing /, +, #, or NUL are dropped) under traffic/fr/paris/paris-bicycle-counters/{counter_id}/... . Counter reference records are retained QoS 1; hourly bicycle counts are non-retained QoS 1 events.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `FR.Paris.OpenData.Velo.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`FR.Paris.OpenData.Velo`](#messagegroup-frparisopendatavelo) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `paris-bicycle-counters` |
| Kafka key | `{counter_id}` |
| Deployed | False |

### Endpoint `FR.Paris.OpenData.Velo.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`FR.Paris.OpenData.Velo.mqtt`](#messagegroup-frparisopendatavelomqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `FR.Paris.OpenData.Velo`
<a id="messagegroup-frparisopendatavelo"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `FR.Paris.OpenData.Velo.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `FR.Paris.OpenData.Velo.Counter`
<a id="message-frparisopendatavelocounter"></a>

| Field | Value |
| --- | --- |
| Name | Counter |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FR.Paris.OpenData.Velo.jstruct/schemas/FR.Paris.OpenData.Velo.Counter`](#schema-frparisopendatavelocounter) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FR.Paris.OpenData.Velo.Counter` |
| `source` |  | `string` | `False` | `https://opendata.paris.fr/explore/dataset/comptage-velo-compteurs` |
| `subject` |  | `uritemplate` | `False` | `{counter_id}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FR.Paris.OpenData.Velo.Kafka` | `KAFKA` | topic `paris-bicycle-counters`; key `{counter_id}` |

#### Message `FR.Paris.OpenData.Velo.BicycleCount`
<a id="message-frparisopendatavelobicyclecount"></a>

| Field | Value |
| --- | --- |
| Name | BicycleCount |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FR.Paris.OpenData.Velo.jstruct/schemas/FR.Paris.OpenData.Velo.BicycleCount`](#schema-frparisopendatavelobicyclecount) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FR.Paris.OpenData.Velo.BicycleCount` |
| `source` |  | `string` | `False` | `https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs` |
| `subject` |  | `uritemplate` | `False` | `{counter_id}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |
| `time` |  | `uritemplate` | `False` | `{date}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FR.Paris.OpenData.Velo.Kafka` | `KAFKA` | topic `paris-bicycle-counters`; key `{counter_id}` |

### Messagegroup `FR.Paris.OpenData.Velo.mqtt`
<a id="messagegroup-frparisopendatavelomqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for Paris bicycle counters. Topics route by stable MQTT-safe counter_id (upstream id_compteur; values containing /, +, #, or NUL are dropped) under traffic/fr/paris/paris-bicycle-counters/{counter_id}/... . Counter reference records are retained QoS 1; hourly bicycle counts are non-retained QoS 1 events. |
| Transport bindings | `FR.Paris.OpenData.Velo.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `FR.Paris.OpenData.Velo.mqtt.Counter`
<a id="message-frparisopendatavelomqttcounter"></a>

| Field | Value |
| --- | --- |
| Name | Counter |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FR.Paris.OpenData.Velo.jstruct/schemas/FR.Paris.OpenData.Velo.Counter`](#schema-frparisopendatavelocounter) |
| Base message chain | `/messagegroups/FR.Paris.OpenData.Velo/messages/FR.Paris.OpenData.Velo.Counter` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FR.Paris.OpenData.Velo.Counter` |
| `source` |  | `string` | `False` | `https://opendata.paris.fr/explore/dataset/comptage-velo-compteurs` |
| `subject` |  | `uritemplate` | `False` | `{counter_id}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FR.Paris.OpenData.Velo.Mqtt` | `MQTT/5.0` | topic `traffic/fr/paris/paris-bicycle-counters/{counter_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/fr/paris/paris-bicycle-counters/{counter_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `FR.Paris.OpenData.Velo.mqtt.BicycleCount`
<a id="message-frparisopendatavelomqttbicyclecount"></a>

| Field | Value |
| --- | --- |
| Name | BicycleCount |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FR.Paris.OpenData.Velo.jstruct/schemas/FR.Paris.OpenData.Velo.BicycleCount`](#schema-frparisopendatavelobicyclecount) |
| Base message chain | `/messagegroups/FR.Paris.OpenData.Velo/messages/FR.Paris.OpenData.Velo.BicycleCount` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FR.Paris.OpenData.Velo.BicycleCount` |
| `source` |  | `string` | `False` | `https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs` |
| `subject` |  | `uritemplate` | `False` | `{counter_id}` |
| `id` |  | `uritemplate` | `False` | `{ce_id}` |
| `time` |  | `uritemplate` | `False` | `{date}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FR.Paris.OpenData.Velo.Mqtt` | `MQTT/5.0` | topic `traffic/fr/paris/paris-bicycle-counters/{counter_id}/count` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/fr/paris/paris-bicycle-counters/{counter_id}/count` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `FR.Paris.OpenData.Velo.jstruct`
<a id="schemagroup-frparisopendatavelojstruct"></a>

#### Schema `FR.Paris.OpenData.Velo.Counter`
<a id="schema-frparisopendatavelocounter"></a>

| Field | Value |
| --- | --- |
| Name | Counter |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.io/paris-bicycle-counters/Counter/v1` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Counter`
<a id="schema-node-counter"></a>

Reference record describing a permanent bicycle counting station in Paris, including its identifier, display name, directional channel, installation date, and geographic coordinates.

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.io/paris-bicycle-counters/Counter/v1` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `counter_id` | `string` | `True` | Unique identifier for the counting channel, combining the site ID and channel ID (mapped from 'id_compteur'). | altnames=`{"lang:fr": "id_compteur"}`<br>alternates=`[{"description": "Original French field name in the Paris Open Data API.", "name": "id_compteur"}]` | - | - |
| `counter_name` | `string` | `True` | Human-readable name of the counter including street name and direction (mapped from 'nom_compteur'). | altnames=`{"lang:fr": "nom_compteur"}`<br>alternates=`[{"description": "Original French field name in the Paris Open Data API.", "name": "nom_compteur"}]` | - | - |
| `channel_name` | `union` | `False` | Directional channel label for the counter, e.g. 'SE-NO' or 'E-O' (mapped from 'channel_name'). | - | - | - |
| `installation_date` | `union` | `False` | Date when the counter was installed, in ISO 8601 date format (YYYY-MM-DD). | - | - | - |
| `longitude` | `union` | `False` | Longitude of the counter location in decimal degrees (WGS 84). | - | - | - |
| `latitude` | `union` | `False` | Latitude of the counter location in decimal degrees (WGS 84). | - | - | - |
| `ce_id` | `string` | `True` | Deterministic CloudEvents id for the retained counter reference record. | - | - | - |

#### Schema `FR.Paris.OpenData.Velo.BicycleCount`
<a id="schema-frparisopendatavelobicyclecount"></a>

| Field | Value |
| --- | --- |
| Name | BicycleCount |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.io/paris-bicycle-counters/BicycleCount/v1` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BicycleCount`
<a id="schema-node-bicyclecount"></a>

Hourly bicycle count observation from a permanent counting station in Paris, reporting the number of bicycles detected during a one-hour window.

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.io/paris-bicycle-counters/BicycleCount/v1` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `counter_id` | `string` | `True` | Unique identifier for the counting channel (mapped from 'id_compteur'). | altnames=`{"lang:fr": "id_compteur"}`<br>alternates=`[{"description": "Original French field name in the Paris Open Data API.", "name": "id_compteur"}]` | - | - |
| `counter_name` | `string` | `True` | Human-readable name of the counter including street name and direction (mapped from 'nom_compteur'). | altnames=`{"lang:fr": "nom_compteur"}`<br>alternates=`[{"description": "Original French field name in the Paris Open Data API.", "name": "nom_compteur"}]` | - | - |
| `count` | `union` | `False` | Number of bicycles counted during the one-hour window (mapped from 'sum_counts'). | alternates=`[{"description": "Original French field name in the Paris Open Data API.", "name": "sum_counts"}]` | - | - |
| `date` | `datetime` | `True` | Start of the one-hour counting window in ISO 8601 format with timezone offset. | - | - | - |
| `longitude` | `union` | `False` | Longitude of the counter location in decimal degrees (WGS 84). | - | - | - |
| `latitude` | `union` | `False` | Latitude of the counter location in decimal degrees (WGS 84). | - | - | - |
| `ce_id` | `string` | `True` | Deterministic CloudEvents id composed from counter_id and hourly count date for subscriber deduplication. | - | - | - |
