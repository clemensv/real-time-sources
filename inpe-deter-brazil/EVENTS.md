# INPE DETER Brazil - Deforestation Alerts Events

MQTT/5.0 transport variants for INPE DETER Brazil deforestation and related land-disturbance alerts. The UNS topic tree is deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert. Payloads are JSON binary-mode CloudEvents. QoS 1 is used for at-least-once alert delivery; consumers MUST deduplicate by alert_id. retain=false is used because DETER alerts are immutable historical events and retaining each alert_id topic would create an unbounded retained-message graveyard. A Message Expiry Interval of 604800 seconds bounds queued delivery for offline durable subscribers. The state_slug axis is a lowercased Brazilian UF code or unknown when INPE omits or publishes an unsupported UF; class_slug is a supported topic-safe lowercase-kebab DETER class or unknown.

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `BR.INPE.DETER.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`BR.INPE.DETER`](#messagegroup-brinpedeter) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `inpe-deter-brazil` |
| Kafka key | `{biome}/{alert_id}` |
| Deployed | False |

### Endpoint `BR.INPE.DETER.Mqtt`

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 binary-mode CloudEvents producer for the INPE DETER deforestation UNS topic tree. |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`BR.INPE.DETER.mqtt`](#messagegroup-brinpedetermqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `BR.INPE.DETER`
<a id="messagegroup-brinpedeter"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `BR.INPE.DETER.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `BR.INPE.DETER.DeforestationAlert`
<a id="message-brinpedeterdeforestationalert"></a>

INPE DETER deforestation alert for Amazon and Cerrado biomes.

| Field | Value |
| --- | --- |
| Name | DeforestationAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BR.INPE.DETER.jstruct/schemas/BR.INPE.DETER.DeforestationAlert`](#schema-brinpedeterdeforestationalert) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `BR.INPE.DETER.DeforestationAlert` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{biome}/{alert_id}` |
| `time` |  | `uritemplate` | `False` | `{view_date}T00:00:00Z` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BR.INPE.DETER.Kafka` | `KAFKA` | topic `inpe-deter-brazil`; key `{biome}/{alert_id}` |

### Messagegroup `BR.INPE.DETER.mqtt`
<a id="messagegroup-brinpedetermqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for INPE DETER Brazil deforestation and related land-disturbance alerts. The UNS topic tree is deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert. Payloads are JSON binary-mode CloudEvents. QoS 1 is used for at-least-once alert delivery; consumers MUST deduplicate by alert_id. retain=false is used because DETER alerts are immutable historical events and retaining each alert_id topic would create an unbounded retained-message graveyard. A Message Expiry Interval of 604800 seconds bounds queued delivery for offline durable subscribers. The state_slug axis is a lowercased Brazilian UF code or unknown when INPE omits or publishes an unsupported UF; class_slug is a supported topic-safe lowercase-kebab DETER class or unknown. |
| Transport bindings | `BR.INPE.DETER.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `BR.INPE.DETER.mqtt.DeforestationAlert`
<a id="message-brinpedetermqttdeforestationalert"></a>

INPE DETER deforestation alert for Amazon and Cerrado biomes.

| Field | Value |
| --- | --- |
| Name | DeforestationAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BR.INPE.DETER.jstruct/schemas/BR.INPE.DETER.DeforestationAlert`](#schema-brinpedeterdeforestationalert) |
| Base message chain | `/messagegroups/BR.INPE.DETER/messages/BR.INPE.DETER.DeforestationAlert` |
| Transport override | `MQTT/5.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `BR.INPE.DETER.DeforestationAlert` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{biome}/{alert_id}` |
| `time` |  | `uritemplate` | `False` | `{view_date}T00:00:00Z` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BR.INPE.DETER.Mqtt` | `MQTT/5.0` | topic `deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert` |
| QoS | 1 |
| Retain | False |
| Additional protocol metadata | `{"message_expiry_interval": 604800}` |

## Schemagroups

### Schemagroup `BR.INPE.DETER.jstruct`
<a id="schemagroup-brinpedeterjstruct"></a>

#### Schema `BR.INPE.DETER.DeforestationAlert`
<a id="schema-brinpedeterdeforestationalert"></a>

| Field | Value |
| --- | --- |
| Name | DeforestationAlert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/BR/INPE/DETER/DeforestationAlert` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/BR/INPE/DETER/DeforestationAlert` |
| Type | `object` |

###### Object `DeforestationAlert`
<a id="schema-node-deforestationalert"></a>

INPE DETER deforestation alert for Amazon and Cerrado biomes.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `alert_id` | `string` | `True` | Stable reference ID from INPE (gid). | - | - | - |
| `biome` | enum `['amazon', 'cerrado']` | `True` | Biome of the alert: amazon or cerrado. | - | - | - |
| `classname` | `string` | `True` | Deforestation class: DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CS_DESORDENADO, etc. | - | - | - |
| `view_date` | `string` | `True` | Observation date in YYYY-MM-DD format. | - | - | - |
| `satellite` | `string` | `True` | Satellite name (CBERS-4, Amazonia-1, etc.). | - | - | - |
| `sensor` | `string` | `True` | Sensor name (AWFI, WFI, MSI). | - | - | - |
| `area_km2` | `double` | `True` | Area of the deforestation polygon in square kilometers. | - | - | - |
| `municipality` | `union` | `False` | Municipality name. | - | - | - |
| `state_code` | `union` | `False` | Brazilian state code (UF), e.g. PA, MT, when provided by INPE; null when omitted. The topic-safe state_slug field is used for MQTT routing. | - | - | - |
| `path_row` | `union` | `False` | Satellite path/row identifier. | - | - | - |
| `publish_month` | `union` | `False` | Publication month in YYYY-MM-DD format. | - | - | - |
| `centroid_latitude` | `double` | `True` | Latitude of the polygon centroid in decimal degrees. | - | - | - |
| `centroid_longitude` | `double` | `True` | Longitude of the polygon centroid in decimal degrees. | - | - | - |
| `state_slug` | `string` | `False` | Lowercased Brazilian state code (UF), e.g. pa, mt, used as a topic-safe MQTT routing axis; unknown when INPE omits the UF. | - | pattern=`^([a-z]{2}\\|unknown)$` | - |
| `class_slug` | enum `['desmatamento-cr', 'desmatamento-veg', 'degradacao', 'mineracao', 'cs-desordenado', 'cs-geometrico', 'cicatriz-de-queimada', 'corte-seletivo', 'unknown']` | `False` | Lowercase-kebab normalized DETER class used as a topic-safe MQTT routing axis, e.g. desmatamento-cr, degradacao, mineracao. | - | pattern=`^[a-z0-9][a-z0-9-]*$` | - |

### Schemagroup `BR.INPE.DETER.avro`
<a id="schemagroup-brinpedeteravro"></a>

#### Schema `BR.INPE.DETER.DeforestationAlert`
<a id="schema-brinpedeterdeforestationalert"></a>

| Field | Value |
| --- | --- |
| Name | DeforestationAlert |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | INPE DETER deforestation alert for Amazon and Cerrado biomes. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DeforestationAlert |
| Namespace | BR.INPE.DETER |
| Type | `record` |
| Doc | INPE DETER deforestation alert for Amazon and Cerrado biomes. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `alert_id` | `string` | Stable reference ID from INPE (gid). | `-` |
| `biome` | `string` | Biome of the alert: amazon or cerrado. | `-` |
| `classname` | `string` | Deforestation class: DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CS_DESORDENADO, etc. | `-` |
| `view_date` | `string` | Observation date in YYYY-MM-DD format. | `-` |
| `satellite` | `string` | Satellite name (CBERS-4, Amazonia-1, etc.). | `-` |
| `sensor` | `string` | Sensor name (AWFI, WFI, MSI). | `-` |
| `area_km2` | `double` | Area of the deforestation polygon in square kilometers. | `-` |
| `municipality` | `string` \| `null` | Municipality name. | `-` |
| `state_code` | `string` \| `null` | Brazilian state code (UF), e.g. PA, MT, when provided by INPE; null when omitted. The topic-safe state_slug field is used for MQTT routing. | `-` |
| `state_slug` | `string` | Lowercased Brazilian state code (UF), e.g. pa, mt, used as a topic-safe MQTT routing axis; unknown when INPE omits or publishes an unsupported UF. | `unknown` |
| `class_slug` | `string` | Lowercase-kebab normalized DETER class used as a topic-safe MQTT routing axis; unknown when the class is omitted or outside the supported DETER vocabulary. | `unknown` |
| `path_row` | `string` \| `null` | Satellite path/row identifier. | `-` |
| `publish_month` | `string` \| `null` | Publication month in YYYY-MM-DD format. | `-` |
| `centroid_latitude` | `double` | Latitude of the polygon centroid in decimal degrees. | `-` |
| `centroid_longitude` | `double` | Longitude of the polygon centroid in decimal degrees. | `-` |
