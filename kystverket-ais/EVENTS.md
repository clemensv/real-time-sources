# Kystverket AIS Bridge Usage Guide Events

MQTT/5.0 non-retained UNS variants of the Kystverket AIS CloudEvents. Each event family (position-report, static, aid-to-navigation) gets a dedicated topic with the kebab family literal baked as the trailing segment. QoS 0, retain=false — there is no LKV slot for a firehose.

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

### Endpoint `NO.Kystverket.AIS.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`NO.Kystverket.AIS`](#messagegroup-nokystverketais) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ais` |
| Kafka key | `{mmsi}` |
| Deployed | False |

### Endpoint `NO.Kystverket.AIS.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`NO.Kystverket.AIS.mqtt`](#messagegroup-nokystverketaismqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |

## Messagegroups

### Messagegroup `NO.Kystverket.AIS`
<a id="messagegroup-nokystverketais"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `NO.Kystverket.AIS.Kafka` (KAFKA) |
| Messages | 7 |

#### Message `NO.Kystverket.AIS.PositionReportClassA`
<a id="message-nokystverketaispositionreportclassa"></a>

| Field | Value |
| --- | --- |
| Name | PositionReportClassA |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.PositionReportClassA`](#schema-nokystverketaispositionreportclassa) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.PositionReportClassA` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

#### Message `NO.Kystverket.AIS.StaticVoyageData`
<a id="message-nokystverketaisstaticvoyagedata"></a>

| Field | Value |
| --- | --- |
| Name | StaticVoyageData |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.StaticVoyageData`](#schema-nokystverketaisstaticvoyagedata) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.StaticVoyageData` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

#### Message `NO.Kystverket.AIS.PositionReportClassB`
<a id="message-nokystverketaispositionreportclassb"></a>

| Field | Value |
| --- | --- |
| Name | PositionReportClassB |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.PositionReportClassB`](#schema-nokystverketaispositionreportclassb) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.PositionReportClassB` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

#### Message `NO.Kystverket.AIS.StaticDataClassB`
<a id="message-nokystverketaisstaticdataclassb"></a>

| Field | Value |
| --- | --- |
| Name | StaticDataClassB |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.StaticDataClassB`](#schema-nokystverketaisstaticdataclassb) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.StaticDataClassB` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

#### Message `NO.Kystverket.AIS.AidToNavigation`
<a id="message-nokystverketaisaidtonavigation"></a>

| Field | Value |
| --- | --- |
| Name | AidToNavigation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.AidToNavigation`](#schema-nokystverketaisaidtonavigation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.AidToNavigation` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

#### Message `NO.Kystverket.AIS.PositionReport`
<a id="message-nokystverketaispositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.PositionReport`](#schema-nokystverketaispositionreport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.PositionReport` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

#### Message `NO.Kystverket.AIS.ShipStatic`
<a id="message-nokystverketaisshipstatic"></a>

| Field | Value |
| --- | --- |
| Name | ShipStatic |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.ShipStatic`](#schema-nokystverketaisshipstatic) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.ShipStatic` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Kafka` | `KAFKA` | topic `ais`; key `{mmsi}` |

### Messagegroup `NO.Kystverket.AIS.mqtt`
<a id="messagegroup-nokystverketaismqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 non-retained UNS variants of the Kystverket AIS CloudEvents. Each event family (position-report, static, aid-to-navigation) gets a dedicated topic with the kebab family literal baked as the trailing segment. QoS 0, retain=false — there is no LKV slot for a firehose. |
| Transport bindings | `NO.Kystverket.AIS.Mqtt` (MQTT/5.0) |
| Messages | 3 |

#### Message `NO.Kystverket.AIS.mqtt.PositionReport`
<a id="message-nokystverketaismqttpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.PositionReport`](#schema-nokystverketaispositionreport) |
| Base message chain | `/messagegroups/NO.Kystverket.AIS/messages/NO.Kystverket.AIS.PositionReport` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.PositionReport` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Mqtt` | `MQTT/5.0` | topic `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report` |
| Retain | False |

#### Message `NO.Kystverket.AIS.mqtt.ShipStatic`
<a id="message-nokystverketaismqttshipstatic"></a>

| Field | Value |
| --- | --- |
| Name | ShipStatic |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.ShipStatic`](#schema-nokystverketaisshipstatic) |
| Base message chain | `/messagegroups/NO.Kystverket.AIS/messages/NO.Kystverket.AIS.ShipStatic` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.ShipStatic` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Mqtt` | `MQTT/5.0` | topic `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/static` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/static` |
| Retain | False |

#### Message `NO.Kystverket.AIS.mqtt.AidToNavigation`
<a id="message-nokystverketaismqttaidtonavigation"></a>

| Field | Value |
| --- | --- |
| Name | AidToNavigation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/NO.Kystverket.AIS.jstruct/schemas/NO.Kystverket.AIS.AidToNavigation`](#schema-nokystverketaisaidtonavigation) |
| Base message chain | `/messagegroups/NO.Kystverket.AIS/messages/NO.Kystverket.AIS.AidToNavigation` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `NO.Kystverket.AIS.AidToNavigation` |
| `source` |  | `string` | `False` | `urn:ais:kystverket:tcp` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `NO.Kystverket.AIS.Mqtt` | `MQTT/5.0` | topic `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation` |
| Retain | False |

## Schemagroups

### Schemagroup `NO.Kystverket.AIS.jstruct`
<a id="schemagroup-nokystverketaisjstruct"></a>

#### Schema `NO.Kystverket.AIS.PositionReportClassA`
<a id="schema-nokystverketaispositionreportclassa"></a>

| Field | Value |
| --- | --- |
| Name | PositionReportClassA |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/PositionReportClassA` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PositionReportClassA`
<a id="schema-node-positionreportclassa"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/PositionReportClassA` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `int32` | `True` |  | - | - | - |
| `navigation_status` | `int32` | `False` |  | - | - | - |
| `rate_of_turn` | `double` | `False` |  | - | - | - |
| `speed_over_ground` | `double` | `False` |  | - | - | - |
| `position_accuracy` | `int32` | `False` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `course_over_ground` | `double` | `False` |  | - | - | - |
| `true_heading` | `int32` | `False` |  | - | - | - |
| `timestamp` | `string` | `True` |  | - | - | - |
| `station_id` | `string` | `False` |  | - | - | - |
| `msg_type` | `int32` | `False` |  | - | - | - |

#### Schema `NO.Kystverket.AIS.StaticVoyageData`
<a id="schema-nokystverketaisstaticvoyagedata"></a>

| Field | Value |
| --- | --- |
| Name | StaticVoyageData |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/StaticVoyageData` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StaticVoyageData`
<a id="schema-node-staticvoyagedata"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/StaticVoyageData` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `int32` | `True` |  | - | - | - |
| `imo_number` | `int32` | `False` |  | - | - | - |
| `callsign` | `string` | `False` |  | - | - | - |
| `ship_name` | `string` | `False` |  | - | - | - |
| `ship_type` | `int32` | `False` |  | - | - | - |
| `dimension_to_bow` | `int32` | `False` |  | - | - | - |
| `dimension_to_stern` | `int32` | `False` |  | - | - | - |
| `dimension_to_port` | `int32` | `False` |  | - | - | - |
| `dimension_to_starboard` | `int32` | `False` |  | - | - | - |
| `draught` | `double` | `False` |  | - | - | - |
| `destination` | `string` | `False` |  | - | - | - |
| `eta_month` | `int32` | `False` |  | - | - | - |
| `eta_day` | `int32` | `False` |  | - | - | - |
| `eta_hour` | `int32` | `False` |  | - | - | - |
| `eta_minute` | `int32` | `False` |  | - | - | - |
| `timestamp` | `string` | `True` |  | - | - | - |
| `station_id` | `string` | `False` |  | - | - | - |

#### Schema `NO.Kystverket.AIS.PositionReportClassB`
<a id="schema-nokystverketaispositionreportclassb"></a>

| Field | Value |
| --- | --- |
| Name | PositionReportClassB |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/PositionReportClassB` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PositionReportClassB`
<a id="schema-node-positionreportclassb"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/PositionReportClassB` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `int32` | `True` |  | - | - | - |
| `speed_over_ground` | `double` | `False` |  | - | - | - |
| `position_accuracy` | `int32` | `False` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `course_over_ground` | `double` | `False` |  | - | - | - |
| `true_heading` | `int32` | `False` |  | - | - | - |
| `timestamp` | `string` | `True` |  | - | - | - |
| `station_id` | `string` | `False` |  | - | - | - |
| `msg_type` | `int32` | `False` |  | - | - | - |

#### Schema `NO.Kystverket.AIS.StaticDataClassB`
<a id="schema-nokystverketaisstaticdataclassb"></a>

| Field | Value |
| --- | --- |
| Name | StaticDataClassB |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/StaticDataClassB` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StaticDataClassB`
<a id="schema-node-staticdataclassb"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/NO/Kystverket/AIS/StaticDataClassB` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `int32` | `True` |  | - | - | - |
| `part_number` | `int32` | `False` |  | - | - | - |
| `ship_name` | `string` | `False` |  | - | - | - |
| `ship_type` | `int32` | `False` |  | - | - | - |
| `callsign` | `string` | `False` |  | - | - | - |
| `dimension_to_bow` | `int32` | `False` |  | - | - | - |
| `dimension_to_stern` | `int32` | `False` |  | - | - | - |
| `dimension_to_port` | `int32` | `False` |  | - | - | - |
| `dimension_to_starboard` | `int32` | `False` |  | - | - | - |
| `timestamp` | `string` | `True` |  | - | - | - |
| `station_id` | `string` | `False` |  | - | - | - |

#### Schema `NO.Kystverket.AIS.AidToNavigation`
<a id="schema-nokystverketaisaidtonavigation"></a>

| Field | Value |
| --- | --- |
| Name | AidToNavigation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/NO/Kystverket/AIS/AidToNavigation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AidToNavigation`
<a id="schema-node-aidtonavigation"></a>

Aid-to-Navigation report (Type 21) projected onto the UNS axes.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/NO/Kystverket/AIS/AidToNavigation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `string` | `True` | Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. | - | pattern=`^[0-9]{9}$` | - |
| `flag` | `string` | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. | - | pattern=`^[a-z]{2}$\\|^xx$` | - |
| `ship_type` | `string` | `True` | Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet. | - | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `msg_type` | enum `['position-report', 'static', 'aid-to-navigation']` | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. | - | - | - |
| `name` | `string` | `False` | Aid-to-Navigation name as broadcast. | - | - | - |
| `aid_type` | `int32` | `True` | AtoN type code (0..31) per ITU-R M.1371. | - | - | - |
| `latitude` | `double` | `True` | Reported latitude in WGS-84 decimal degrees. | - | - | - |
| `longitude` | `double` | `True` | Reported longitude in WGS-84 decimal degrees. | - | - | - |
| `position_accuracy` | `int32` | `False` | 1 if high-accuracy (DGPS), else 0. | - | - | - |
| `timestamp` | `string` | `False` | ISO-8601 receive time as supplied by the upstream NMEA tag. | - | - | - |
| `station_id` | `string` | `False` | Kystverket base-station identifier. | - | - | - |
| `ais_msg_type` | `int32` | `True` | Original ITU-R M.1371 message ID (21). | - | - | - |

#### Schema `NO.Kystverket.AIS.PositionReport`
<a id="schema-nokystverketaispositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/NO/Kystverket/AIS/PositionReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PositionReport`
<a id="schema-node-positionreport"></a>

AIS position report (Type 1/2/3/18/19) projected onto the UNS axes.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/NO/Kystverket/AIS/PositionReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `string` | `True` | Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. | - | pattern=`^[0-9]{9}$` | - |
| `flag` | `string` | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. | - | pattern=`^[a-z]{2}$\\|^xx$` | - |
| `ship_type` | `string` | `True` | Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet. | - | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `msg_type` | enum `['position-report', 'static', 'aid-to-navigation']` | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. | - | - | - |
| `latitude` | `double` | `True` | Reported latitude in WGS-84 decimal degrees. | - | - | - |
| `longitude` | `double` | `True` | Reported longitude in WGS-84 decimal degrees. | - | - | - |
| `speed_over_ground` | `double` | `False` | Speed over ground in knots. | - | - | - |
| `course_over_ground` | `double` | `False` | Course over ground in degrees (0..359.9). | - | - | - |
| `true_heading` | `int32` | `False` | True heading in degrees (0..359, 511 = not available). | - | - | - |
| `navigation_status` | `int32` | `False` | ITU navigation status code (0..15). 0 for Class-B. | - | - | - |
| `rate_of_turn` | `double` | `False` | Rate of turn in AIS-encoded units. 0 for Class-B. | - | - | - |
| `position_accuracy` | `int32` | `False` | 1 if high-accuracy (DGPS), else 0. | - | - | - |
| `timestamp` | `string` | `False` | ISO-8601 receive time as supplied by the upstream NMEA tag. | - | - | - |
| `station_id` | `string` | `False` | Kystverket base-station identifier from the NMEA tag block. | - | - | - |
| `ais_msg_type` | `int32` | `True` | Original ITU-R M.1371 message ID (1, 2, 3, 18, or 19). | - | - | - |

#### Schema `NO.Kystverket.AIS.ShipStatic`
<a id="schema-nokystverketaisshipstatic"></a>

| Field | Value |
| --- | --- |
| Name | ShipStatic |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/NO/Kystverket/AIS/ShipStatic` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ShipStatic`
<a id="schema-node-shipstatic"></a>

AIS static and voyage-related data (Type 5 / Type 24) projected onto the UNS axes.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/NO/Kystverket/AIS/ShipStatic` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `string` | `True` | Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. | - | pattern=`^[0-9]{9}$` | - |
| `flag` | `string` | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. | - | pattern=`^[a-z]{2}$\\|^xx$` | - |
| `ship_type` | `string` | `True` | Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet. | - | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `msg_type` | enum `['position-report', 'static', 'aid-to-navigation']` | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. | - | - | - |
| `ship_name` | `string` | `False` | Vessel name as broadcast (max 20 chars, trimmed). | - | - | - |
| `callsign` | `string` | `False` | Radio call sign as broadcast (max 7 chars). | - | - | - |
| `imo_number` | `int32` | `False` | IMO number (7-digit). 0 if not assigned or for Class-B. | - | - | - |
| `ship_type_code` | `int32` | `True` | Raw ITU-R M.1371 ship type code (0..99). | - | - | - |
| `destination` | `string` | `False` | Voyage destination string (max 20 chars). Empty for Type 24. | - | - | - |
| `eta` | `string` | `False` | Voyage ETA as ISO-8601 string. Empty if absent (Type 24). | - | - | - |
| `draught` | `double` | `False` | Maximum present static draught in metres. 0.0 if absent. | - | - | - |
| `dim_to_bow` | `int32` | `False` | Distance from reference point to bow in metres. | - | - | - |
| `dim_to_stern` | `int32` | `False` | Distance from reference point to stern in metres. | - | - | - |
| `dim_to_port` | `int32` | `False` | Distance from reference point to port side in metres. | - | - | - |
| `dim_to_starboard` | `int32` | `False` | Distance from reference point to starboard side in metres. | - | - | - |
| `timestamp` | `string` | `False` | ISO-8601 receive time as supplied by the upstream NMEA tag. | - | - | - |
| `station_id` | `string` | `False` | Kystverket base-station identifier. | - | - | - |
| `ais_msg_type` | `int32` | `True` | Original ITU-R M.1371 message ID (5 or 24). | - | - | - |
