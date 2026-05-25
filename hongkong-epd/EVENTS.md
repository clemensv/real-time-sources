# Hong Kong EPD AQHI Bridge Events

MQTT/5.0 transport variants of the HK EPD AQHI CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under air-quality/hk/epd/hongkong-epd/{district}/{station_id}/... The {district} placeholder is the Hong Kong 18-district administrative area where the station is located, normalized to lowercase snake_case.

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

### Endpoint `HK.Gov.EPD.AQHI.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`HK.Gov.EPD.AQHI`](#messagegroup-hkgovepdaqhi) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `hongkong-epd-aqhi` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `HK.Gov.EPD.AQHI.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`HK.Gov.EPD.AQHI.mqtt`](#messagegroup-hkgovepdaqhimqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `HK.Gov.EPD.AQHI`
<a id="messagegroup-hkgovepdaqhi"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `HK.Gov.EPD.AQHI.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `HK.Gov.EPD.AQHI.Station`
<a id="message-hkgovepdaqhistation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/HK.Gov.EPD.AQHI.jstruct/schemas/HK.Gov.EPD.AQHI.Station`](#schema-hkgovepdaqhistation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `HK.Gov.EPD.AQHI.Station` |
| `source` |  | `string` | `False` | `https://www.aqhi.gov.hk` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `HK.Gov.EPD.AQHI.Kafka` | `KAFKA` | topic `hongkong-epd-aqhi`; key `{station_id}` |

#### Message `HK.Gov.EPD.AQHI.AQHIReading`
<a id="message-hkgovepdaqhiaqhireading"></a>

| Field | Value |
| --- | --- |
| Name | AQHIReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/HK.Gov.EPD.AQHI.jstruct/schemas/HK.Gov.EPD.AQHI.AQHIReading`](#schema-hkgovepdaqhiaqhireading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `HK.Gov.EPD.AQHI.AQHIReading` |
| `source` |  | `string` | `False` | `https://www.aqhi.gov.hk` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `HK.Gov.EPD.AQHI.Kafka` | `KAFKA` | topic `hongkong-epd-aqhi`; key `{station_id}` |

### Messagegroup `HK.Gov.EPD.AQHI.mqtt`
<a id="messagegroup-hkgovepdaqhimqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the HK EPD AQHI CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under air-quality/hk/epd/hongkong-epd/{district}/{station_id}/... The {district} placeholder is the Hong Kong 18-district administrative area where the station is located, normalized to lowercase snake_case. |
| Transport bindings | `HK.Gov.EPD.AQHI.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `HK.Gov.EPD.AQHI.mqtt.Station`
<a id="message-hkgovepdaqhimqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/HK.Gov.EPD.AQHI.jstruct/schemas/HK.Gov.EPD.AQHI.Station`](#schema-hkgovepdaqhistation) |
| Base message chain | `/messagegroups/HK.Gov.EPD.AQHI/messages/HK.Gov.EPD.AQHI.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `HK.Gov.EPD.AQHI.Station` |
| `source` |  | `string` | `False` | `https://www.aqhi.gov.hk` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `HK.Gov.EPD.AQHI.Mqtt` | `MQTT/5.0` | topic `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `HK.Gov.EPD.AQHI.mqtt.AQHIReading`
<a id="message-hkgovepdaqhimqttaqhireading"></a>

| Field | Value |
| --- | --- |
| Name | AQHIReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/HK.Gov.EPD.AQHI.jstruct/schemas/HK.Gov.EPD.AQHI.AQHIReading`](#schema-hkgovepdaqhiaqhireading) |
| Base message chain | `/messagegroups/HK.Gov.EPD.AQHI/messages/HK.Gov.EPD.AQHI.AQHIReading` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `HK.Gov.EPD.AQHI.AQHIReading` |
| `source` |  | `string` | `False` | `https://www.aqhi.gov.hk` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `HK.Gov.EPD.AQHI.Mqtt` | `MQTT/5.0` | topic `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/aqhi` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/aqhi` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `HK.Gov.EPD.AQHI.jstruct`
<a id="schemagroup-hkgovepdaqhijstruct"></a>

#### Schema `HK.Gov.EPD.AQHI.Station`
<a id="schema-hkgovepdaqhistation"></a>

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
| $id | `https://www.aqhi.gov.hk/schemas/HK/Gov/EPD/AQHI/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for a Hong Kong EPD AQHI monitoring station. The EPD operates a network of General Stations and Roadside Stations across Hong Kong. Station coordinates are derived from the EPD station map.

| Field | Value |
| --- | --- |
| $id | `https://www.aqhi.gov.hk/schemas/HK/Gov/EPD/AQHI/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable station identifier derived from the station name in snake_case, for example central_western or mong_kok. | - | - | - |
| `station_name` | `string` | `True` | Station name as published in the EPD AQHI feed, for example 'Central/Western' or 'Mong Kok'. | - | - | - |
| `station_type` | `string` | `True` | Station classification. General Stations measure ambient background air quality and Roadside Stations are positioned near roads to capture traffic-related pollution. | altenums=`["General Stations", "Roadside Stations"]` | - | - |
| `district` | `string` | `True` | Hong Kong 18-district administrative area where the monitoring station is located, normalized to lowercase snake_case. Used as the {district} segment of the MQTT/UNS topic. Examples: central-and-western, wan-chai, yau-tsim-mong. | - | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the monitoring station. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `union` | `False` | WGS84 longitude of the monitoring station. | unit=`degree` symbol=`°` | - | - |

#### Schema `HK.Gov.EPD.AQHI.AQHIReading`
<a id="schema-hkgovepdaqhiaqhireading"></a>

| Field | Value |
| --- | --- |
| Name | AQHIReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.aqhi.gov.hk/schemas/HK/Gov/EPD/AQHI/AQHIReading` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AQHIReading`
<a id="schema-node-aqhireading"></a>

Air Quality Health Index (AQHI) reading for a Hong Kong EPD monitoring station. AQHI quantifies health risk from air pollution on a scale of 1 to 10+ and is calculated from concentrations of nitrogen dioxide, sulphur dioxide, ozone, and PM2.5. Published hourly by the EPD.

| Field | Value |
| --- | --- |
| $id | `https://www.aqhi.gov.hk/schemas/HK/Gov/EPD/AQHI/AQHIReading` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable station identifier in snake_case. | - | - | - |
| `station_name` | `string` | `True` | Station name as published in the EPD AQHI feed. | - | - | - |
| `station_type` | `string` | `True` | Station classification: General Stations or Roadside Stations. | altenums=`["General Stations", "Roadside Stations"]` | - | - |
| `district` | `string` | `True` | Hong Kong 18-district administrative area where the monitoring station is located, normalized to lowercase snake_case. Used as the {district} segment of the MQTT/UNS topic. | - | - | - |
| `reading_time` | `datetime` | `True` | Observation timestamp parsed from the feed DateTime field. The XML feed publishes RFC 2822 timestamps and the bridge emits ISO 8601 values. | - | - | - |
| `aqhi` | `integer` | `True` | AQHI value. Scale: 1 to 3 Low health risk, 4 to 6 Moderate, 7 High, 8 to 10 Very High, and above 10 Serious. Value 11 is used in the feed to indicate 10+ Serious. | - | minimum=`1` | - |
| `health_risk_category` | `union` | `False` | Health risk category derived from the AQHI value: Low, Moderate, High, Very High, or Serious. | altenums=`["Low", "Moderate", "High", "Very High", "Serious"]` | - | - |
