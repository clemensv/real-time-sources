# Hub'Eau Hydrométrie API Bridge Events

This project bridges the [Hub'Eau Hydrométrie API](https://hubeau.eaufrance.fr/page/api-hydrometrie) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams. It provides real-time water level (height) and flow (discharge) data from approximately 6,300 monitoring stations across France.

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

### Endpoint `FR.Gov.Eaufrance.HubEau.Hydrometrie.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`FR.Gov.Eaufrance.HubEau.Hydrometrie`](#messagegroup-frgoveaufrancehubeauhydrometrie) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `hubeau-hydrometrie` |
| Kafka key | `{code_station}` |
| Deployed | False |

## Messagegroups

### Messagegroup `FR.Gov.Eaufrance.HubEau.Hydrometrie`
<a id="messagegroup-frgoveaufrancehubeauhydrometrie"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `FR.Gov.Eaufrance.HubEau.Hydrometrie.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `FR.Gov.Eaufrance.HubEau.Hydrometrie.Station`
<a id="message-frgoveaufrancehubeauhydrometriestation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FR.Gov.Eaufrance.HubEau.Hydrometrie.jstruct/schemas/FR.Gov.Eaufrance.HubEau.Hydrometrie.Station`](#schema-frgoveaufrancehubeauhydrometriestation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FR.Gov.Eaufrance.HubEau.Hydrometrie.Station` |
| `source` |  | `string` | `False` | `https://hubeau.eaufrance.fr/api/v2/hydrometrie` |
| `subject` |  | `uritemplate` | `False` | `{code_station}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FR.Gov.Eaufrance.HubEau.Hydrometrie.Kafka` | `KAFKA` | topic `hubeau-hydrometrie`; key `{code_station}` |

#### Message `FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation`
<a id="message-frgoveaufrancehubeauhydrometrieobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/FR.Gov.Eaufrance.HubEau.Hydrometrie.jstruct/schemas/FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation`](#schema-frgoveaufrancehubeauhydrometrieobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation` |
| `source` |  | `string` | `False` | `https://hubeau.eaufrance.fr/api/v2/hydrometrie` |
| `subject` |  | `uritemplate` | `False` | `{code_station}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `FR.Gov.Eaufrance.HubEau.Hydrometrie.Kafka` | `KAFKA` | topic `hubeau-hydrometrie`; key `{code_station}` |

## Schemagroups

### Schemagroup `FR.Gov.Eaufrance.HubEau.Hydrometrie.jstruct`
<a id="schemagroup-frgoveaufrancehubeauhydrometriejstruct"></a>

#### Schema `FR.Gov.Eaufrance.HubEau.Hydrometrie.Station`
<a id="schema-frgoveaufrancehubeauhydrometriestation"></a>

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
| $id | `https://example.com/schemas/FR/Gov/Eaufrance/HubEau/Hydrometrie/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/FR/Gov/Eaufrance/HubEau/Hydrometrie/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `code_station` | `string` | `True` |  | - | - | - |
| `libelle_station` | `string` | `True` |  | - | - | - |
| `code_site` | `union` | `False` |  | - | - | - |
| `longitude_station` | `double` | `True` |  | - | - | - |
| `latitude_station` | `double` | `True` |  | - | - | - |
| `libelle_cours_eau` | `union` | `False` |  | - | - | - |
| `libelle_commune` | `union` | `False` |  | - | - | - |
| `code_departement` | `union` | `False` |  | - | - | - |
| `en_service` | `union` | `False` |  | - | - | - |
| `date_ouverture_station` | `union` | `False` |  | - | - | - |

#### Schema `FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation`
<a id="schema-frgoveaufrancehubeauhydrometrieobservation"></a>

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
| $id | `https://example.com/schemas/FR/Gov/Eaufrance/HubEau/Hydrometrie/Observation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Observation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/FR/Gov/Eaufrance/HubEau/Hydrometrie/Observation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `code_station` | `string` | `True` |  | - | - | - |
| `date_obs` | `datetime` | `True` |  | - | - | - |
| `resultat_obs` | `double` | `True` |  | - | - | - |
| `grandeur_hydro` | `string` | `True` |  | - | - | - |
| `libelle_methode_obs` | `union` | `False` |  | - | - | - |
| `libelle_qualification_obs` | `union` | `False` |  | - | - | - |

### Schemagroup `FR.Gov.Eaufrance.HubEau.Hydrometrie.avro`
<a id="schemagroup-frgoveaufrancehubeauhydrometrieavro"></a>

#### Schema `FR.Gov.Eaufrance.HubEau.Hydrometrie.Station`
<a id="schema-frgoveaufrancehubeauhydrometriestation"></a>

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
| Namespace | FR.Gov.Eaufrance.HubEau.Hydrometrie |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `code_station` | `string` |  | `-` |
| `libelle_station` | `string` |  | `-` |
| `code_site` | `null` \| `string` |  | `-` |
| `longitude_station` | `double` |  | `-` |
| `latitude_station` | `double` |  | `-` |
| `libelle_cours_eau` | `null` \| `string` |  | `-` |
| `libelle_commune` | `null` \| `string` |  | `-` |
| `code_departement` | `null` \| `string` |  | `-` |
| `en_service` | `null` \| `boolean` |  | `-` |
| `date_ouverture_station` | `null` \| `string` |  | `-` |

#### Schema `FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation`
<a id="schema-frgoveaufrancehubeauhydrometrieobservation"></a>

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
| Namespace | FR.Gov.Eaufrance.HubEau.Hydrometrie |
| Type | `record` |
| Doc | Observation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `code_station` | `string` |  | `-` |
| `date_obs` | `string` |  | `-` |
| `resultat_obs` | `double` |  | `-` |
| `grandeur_hydro` | `string` |  | `-` |
| `libelle_methode_obs` | `null` \| `string` |  | `-` |
| `libelle_qualification_obs` | `null` \| `string` |  | `-` |
