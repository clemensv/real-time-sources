# UK Environment Agency Flood Monitoring API Bridge Events

This project bridges the [UK Environment Agency Flood Monitoring API](https://environment.data.gov.uk/flood-monitoring/doc/reference) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams. It provides real-time water level and flow data from approximately 4,000 monitoring stations across England.

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

### Endpoint `UK.Gov.Environment.EA.FloodMonitoring.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`UK.Gov.Environment.EA.FloodMonitoring`](#messagegroup-ukgovenvironmenteafloodmonitoring) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `uk-ea-flood-monitoring` |
| Kafka key | `{station_reference}` |
| Deployed | False |

## Messagegroups

### Messagegroup `UK.Gov.Environment.EA.FloodMonitoring`
<a id="messagegroup-ukgovenvironmenteafloodmonitoring"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `UK.Gov.Environment.EA.FloodMonitoring.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `UK.Gov.Environment.EA.FloodMonitoring.Station`
<a id="message-ukgovenvironmenteafloodmonitoringstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/UK.Gov.Environment.EA.FloodMonitoring.jstruct/schemas/UK.Gov.Environment.EA.FloodMonitoring.Station`](#schema-ukgovenvironmenteafloodmonitoringstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `UK.Gov.Environment.EA.FloodMonitoring.Station` |
| `source` |  | `string` | `False` | `https://environment.data.gov.uk/flood-monitoring` |
| `subject` |  | `uritemplate` | `False` | `{station_reference}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `UK.Gov.Environment.EA.FloodMonitoring.Kafka` | `KAFKA` | topic `uk-ea-flood-monitoring`; key `{station_reference}` |

#### Message `UK.Gov.Environment.EA.FloodMonitoring.Reading`
<a id="message-ukgovenvironmenteafloodmonitoringreading"></a>

| Field | Value |
| --- | --- |
| Name | Reading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/UK.Gov.Environment.EA.FloodMonitoring.jstruct/schemas/UK.Gov.Environment.EA.FloodMonitoring.Reading`](#schema-ukgovenvironmenteafloodmonitoringreading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `UK.Gov.Environment.EA.FloodMonitoring.Reading` |
| `source` |  | `string` | `False` | `https://environment.data.gov.uk/flood-monitoring` |
| `subject` |  | `uritemplate` | `False` | `{station_reference}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `UK.Gov.Environment.EA.FloodMonitoring.Kafka` | `KAFKA` | topic `uk-ea-flood-monitoring`; key `{station_reference}` |

## Schemagroups

### Schemagroup `UK.Gov.Environment.EA.FloodMonitoring.jstruct`
<a id="schemagroup-ukgovenvironmenteafloodmonitoringjstruct"></a>

#### Schema `UK.Gov.Environment.EA.FloodMonitoring.Station`
<a id="schema-ukgovenvironmenteafloodmonitoringstation"></a>

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
| $id | `https://example.com/schemas/UK/Gov/Environment/EA/FloodMonitoring/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/UK/Gov/Environment/EA/FloodMonitoring/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_reference` | `string` | `True` |  | - | - | - |
| `label` | `string` | `True` |  | - | - | - |
| `river_name` | `union` | `False` |  | - | - | - |
| `catchment_name` | `union` | `False` |  | - | - | - |
| `town` | `union` | `False` |  | - | - | - |
| `lat` | `double` | `True` |  | - | - | - |
| `long` | `double` | `True` |  | - | - | - |
| `notation` | `string` | `True` |  | - | - | - |
| `status` | `union` | `False` |  | - | - | - |
| `date_opened` | `union` | `False` |  | - | - | - |

#### Schema `UK.Gov.Environment.EA.FloodMonitoring.Reading`
<a id="schema-ukgovenvironmenteafloodmonitoringreading"></a>

| Field | Value |
| --- | --- |
| Name | Reading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/UK/Gov/Environment/EA/FloodMonitoring/Reading` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Reading`
<a id="schema-node-reading"></a>

Reading

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/UK/Gov/Environment/EA/FloodMonitoring/Reading` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_reference` | `string` | `True` |  | - | - | - |
| `date_time` | `datetime` | `True` |  | - | - | - |
| `measure` | `string` | `True` |  | - | - | - |
| `value` | `double` | `True` |  | - | - | - |

### Schemagroup `UK.Gov.Environment.EA.FloodMonitoring.avro`
<a id="schemagroup-ukgovenvironmenteafloodmonitoringavro"></a>

#### Schema `UK.Gov.Environment.EA.FloodMonitoring.Station`
<a id="schema-ukgovenvironmenteafloodmonitoringstation"></a>

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
| Namespace | UK.Gov.Environment.EA.FloodMonitoring |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_reference` | `string` |  | `-` |
| `label` | `string` |  | `-` |
| `river_name` | `null` \| `string` |  | `-` |
| `catchment_name` | `null` \| `string` |  | `-` |
| `town` | `null` \| `string` |  | `-` |
| `lat` | `double` |  | `-` |
| `long` | `double` |  | `-` |
| `notation` | `string` |  | `-` |
| `status` | `null` \| `string` |  | `-` |
| `date_opened` | `null` \| `string` |  | `-` |

#### Schema `UK.Gov.Environment.EA.FloodMonitoring.Reading`
<a id="schema-ukgovenvironmenteafloodmonitoringreading"></a>

| Field | Value |
| --- | --- |
| Name | Reading |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Reading |
| Namespace | UK.Gov.Environment.EA.FloodMonitoring |
| Type | `record` |
| Doc | Reading |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_reference` | `string` |  | `-` |
| `date_time` | `string` |  | `-` |
| `measure` | `string` |  | `-` |
| `value` | `double` |  | `-` |
