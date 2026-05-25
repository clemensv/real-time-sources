# PegelOnline → Apache Kafka, MQTT/UNS & AMQP 1.0 Events

Kafka-transport variants of the PegelOnline CloudEvents, adding per-message Kafka key for partitioning.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 4 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `de.wsv.pegelonline.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`de.wsv.pegelonline.kafka`](#messagegroup-dewsvpegelonlinekafka) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `pegelonline` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `de.wsv.pegelonline.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`de.wsv.pegelonline.mqtt`](#messagegroup-dewsvpegelonlinemqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

### Endpoint `de.wsv.pegelonline.Amqp`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `AMQP/1.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`de.wsv.pegelonline.amqp`](#messagegroup-dewsvpegelonlineamqp) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "amqps://localhost:5671/pegelonline"}]` |

## Messagegroups

### Messagegroup `de.wsv.pegelonline`
<a id="messagegroup-dewsvpegelonline"></a>

| Field | Value |
| --- | --- |
| Messages | 2 |

#### Message `de.wsv.pegelonline.Station`
<a id="message-dewsvpegelonlinestation"></a>

Reference catalog entry for one WSV PegelOnline gauge installation. Emitted at bridge startup and periodically refreshed so downstream consumers can interpret CurrentMeasurement events without an out-of-band lookup. Sourced from `GET /stations.json` on the PegelOnline REST API v2.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.Station`](#schema-dewsvpegelonlinestation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Message `de.wsv.pegelonline.CurrentMeasurement`
<a id="message-dewsvpegelonlinecurrentmeasurement"></a>

Latest 15-minute water-level reading (W timeseries) for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Telemetry counterpart to the Station reference event; both share the `station_id` keying.

| Field | Value |
| --- | --- |
| Name | CurrentMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.CurrentMeasurement`](#schema-dewsvpegelonlinecurrentmeasurement) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.CurrentMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

### Messagegroup `de.wsv.pegelonline.kafka`
<a id="messagegroup-dewsvpegelonlinekafka"></a>

| Field | Value |
| --- | --- |
| Description | Kafka-transport variants of the PegelOnline CloudEvents, adding per-message Kafka key for partitioning. |
| Transport bindings | `de.wsv.pegelonline.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `de.wsv.pegelonline.kafka.Station`
<a id="message-dewsvpegelonlinekafkastation"></a>

Reference catalog entry for one WSV PegelOnline gauge installation. Emitted at bridge startup and periodically refreshed so downstream consumers can interpret CurrentMeasurement events without an out-of-band lookup. Sourced from `GET /stations.json` on the PegelOnline REST API v2.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.Station`](#schema-dewsvpegelonlinestation) |
| Base message chain | `/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.Station` |
| Transport override | `KAFKA` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.wsv.pegelonline.Kafka` | `KAFKA` | topic `pegelonline`; key `{station_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| Additional protocol metadata | `{"metadata.key": {"description": "Kafka partition key — stable station identifier matching the CloudEvent subject.", "type": "uritemplate", "value": "{station_id}"}}` |

#### Message `de.wsv.pegelonline.kafka.CurrentMeasurement`
<a id="message-dewsvpegelonlinekafkacurrentmeasurement"></a>

Latest 15-minute water-level reading (W timeseries) for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Telemetry counterpart to the Station reference event; both share the `station_id` keying.

| Field | Value |
| --- | --- |
| Name | CurrentMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.CurrentMeasurement`](#schema-dewsvpegelonlinecurrentmeasurement) |
| Base message chain | `/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.CurrentMeasurement` |
| Transport override | `KAFKA` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.CurrentMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.wsv.pegelonline.Kafka` | `KAFKA` | topic `pegelonline`; key `{station_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| Additional protocol metadata | `{"metadata.key": {"description": "Kafka partition key — stable station identifier matching the CloudEvent subject.", "type": "uritemplate", "value": "{station_id}"}}` |

### Messagegroup `de.wsv.pegelonline.mqtt`
<a id="messagegroup-dewsvpegelonlinemqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the PegelOnline CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/de/wsv/pegelonline/... |
| Transport bindings | `de.wsv.pegelonline.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `de.wsv.pegelonline.mqtt.Station`
<a id="message-dewsvpegelonlinemqttstation"></a>

Reference catalog entry for one WSV PegelOnline gauge installation. Emitted at bridge startup and periodically refreshed so downstream consumers can interpret CurrentMeasurement events without an out-of-band lookup. Sourced from `GET /stations.json` on the PegelOnline REST API v2.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.Station`](#schema-dewsvpegelonlinestation) |
| Base message chain | `/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.wsv.pegelonline.Mqtt` | `MQTT/5.0` | topic `hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `de.wsv.pegelonline.mqtt.CurrentMeasurement`
<a id="message-dewsvpegelonlinemqttcurrentmeasurement"></a>

Latest 15-minute water-level reading (W timeseries) for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Telemetry counterpart to the Station reference event; both share the `station_id` keying.

| Field | Value |
| --- | --- |
| Name | CurrentMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.CurrentMeasurement`](#schema-dewsvpegelonlinecurrentmeasurement) |
| Base message chain | `/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.CurrentMeasurement` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.CurrentMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.wsv.pegelonline.Mqtt` | `MQTT/5.0` | topic `hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/water-level` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/water-level` |
| QoS | 1 |
| Retain | True |

### Messagegroup `de.wsv.pegelonline.amqp`
<a id="messagegroup-dewsvpegelonlineamqp"></a>

| Field | Value |
| --- | --- |
| Description | AMQP 1.0 transport variants of the PegelOnline CloudEvents, sent in binary CloudEvents mode to a single AMQP node ('pegelonline') — works with generic brokers (ActiveMQ Artemis, RabbitMQ AMQP 1.0 plugin, Qpid Dispatch) and with Azure Service Bus / Event Hubs via CBS + Entra ID or SAS-token. Routing key is the CloudEvent subject (`{station_id}`); per-waterway routing is exposed as the `water_shortname` AMQP application property so brokers and SB/EH subscription filters can route without cracking the JSON body. |
| Transport bindings | `de.wsv.pegelonline.Amqp` (AMQP/1.0) |
| Messages | 2 |

#### Message `de.wsv.pegelonline.amqp.Station`
<a id="message-dewsvpegelonlineamqpstation"></a>

Reference catalog entry for one WSV PegelOnline gauge installation. Emitted at bridge startup and periodically refreshed so downstream consumers can interpret CurrentMeasurement events without an out-of-band lookup. Sourced from `GET /stations.json` on the PegelOnline REST API v2.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.Station`](#schema-dewsvpegelonlinestation) |
| Base message chain | `/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.Station` |
| Transport override | `AMQP/1.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.wsv.pegelonline.Amqp` | `AMQP/1.0` | address `-` |

##### Transport options

| Option | Value |
| --- | --- |
| Application properties | `{"water_shortname": {"description": "Lowercase ASCII water-body shortname (e.g. 'rhein'); supplied by the bridge from the station catalog so message routers / filters can route by waterway without cracking the JSON body.", "type": "uritemplate", "value": "{water_shortname}"}}` |

#### Message `de.wsv.pegelonline.amqp.CurrentMeasurement`
<a id="message-dewsvpegelonlineamqpcurrentmeasurement"></a>

Latest 15-minute water-level reading (W timeseries) for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Telemetry counterpart to the Station reference event; both share the `station_id` keying.

| Field | Value |
| --- | --- |
| Name | CurrentMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.CurrentMeasurement`](#schema-dewsvpegelonlinecurrentmeasurement) |
| Base message chain | `/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.CurrentMeasurement` |
| Transport override | `AMQP/1.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.wsv.pegelonline.CurrentMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.wsv.pegelonline.Amqp` | `AMQP/1.0` | address `-` |

##### Transport options

| Option | Value |
| --- | --- |
| Application properties | `{"water_shortname": {"description": "Lowercase ASCII water-body shortname (e.g. 'rhein'); supplied by the bridge from the station catalog so message routers / filters can route by waterway without cracking the JSON body.", "type": "uritemplate", "value": "{water_shortname}"}}` |

## Schemagroups

### Schemagroup `de.wsv.pegelonline.jstruct`
<a id="schemagroup-dewsvpegelonlinejstruct"></a>

#### Schema `de.wsv.pegelonline.Station`
<a id="schema-dewsvpegelonlinestation"></a>

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
| $id | `https://schemas.real-time-sources.dev/de/wsv/pegelonline/Station/v1` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/de/wsv/pegelonline/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

WSV PegelOnline gauge installation. Each instance represents one physical Pegelmessstelle on a federally administered German inland or coastal waterway. Sourced from `GET /stations.json` on the PegelOnline REST API v2 (https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Emitted as reference data at bridge startup and re-emitted periodically.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable UUID assigned by WSV to identify the gauge installation; persists across station renaming, relocation within the same Pegelmessstelle, and timeseries reconfiguration. Sourced from the upstream `uuid` field. Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic `{station_id}` segment, and the AMQP message subject for every event emitted by this source. | altnames=`{"json": "uuid"}` | - | - |
| `number` | `string` | `True` | Official PegelOnline station number. Carries multiple agency-scoped numbering schemes within the same field: WSV Pegelmessstellennummer (6–8 digits) for German federal gauges; partner-agency identifiers such as Austrian via-donau station numbers (4–5 digits), small Regierungspräsidium-IDs for Bodensee gauges (3-digit numbers e.g. '906' KONSTANZ), and German state-agency IDs (e.g. Ruhrverband 13-digit Messstellennummer). Numeric-only across all observed providers; length is provider-specific. National / agency-scoped identifier — not globally unique across data providers; prefer `station_id` (UUID) for cross-system joins. | - | pattern=`^[0-9]+$` | - |
| `shortname` | `string` | `True` | Operator-assigned display label for the gauge (≤40 characters). May differ from the town name when multiple gauges share a town. Mutable — do not use as a routing key or stable identifier. | - | - | - |
| `longname` | `string` | `True` | Canonical gauge name as used in WSV publications (≤255 characters). Mutable — do not use as a routing key. | - | - | - |
| `km` | `union` | `False` | Position along the federal waterway expressed as river-kilometre downstream from the waterway's official origin (e.g. Rhine-km 0 at the Old Rhine Bridge in Konstanz). The decimal fraction is the hectometre offset within the kilometre. Negative values occur on tributaries where the kilometre count is measured upstream from a confluence (e.g. Ohře gauge LOUNY at km -61.4 of the Elbe/Ohře system). **Optional**: absent or null for tidal / coastal gauges (Küstenpegel on the North Sea and Baltic) and for waterways without a kilometre reference. Sourced from the upstream `km` field. Unit: km. | unit=`km` symbol=`km` | - | - |
| `agency` | `string` | `True` | Free-form name of the Wasserstraßen- und Schifffahrtsamt (WSA) operating the gauge — e.g. 'WSA RHEIN', 'WSA ELBE'. Sourced from the upstream `agency` field. Provided so downstream consumers can attribute observations to the operating authority; not a stable identifier and not suitable as a routing key. | - | - | - |
| `longitude` | `double` | `True` | WGS84 decimal-degree longitude of the gauge installation; positive east of the prime meridian. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `longitude` field. | unit=`deg` symbol=`°` | maximum=`180`<br>minimum=`-180` | - |
| `latitude` | `double` | `True` | WGS84 decimal-degree latitude of the gauge installation; positive north of the equator. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `latitude` field. | unit=`deg` symbol=`°` | maximum=`90`<br>minimum=`-90` | - |
| `water` | `schema` | `True` | Federal waterway the gauge measures. See the nested Water schema for routing semantics. | - | - | - |

#### Schema `de.wsv.pegelonline.CurrentMeasurement`
<a id="schema-dewsvpegelonlinecurrentmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | CurrentMeasurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/de/wsv/pegelonline/CurrentMeasurement/v1` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/de/wsv/pegelonline/CurrentMeasurement` |
| Type | `object` |

###### Object `CurrentMeasurement`
<a id="schema-node-currentmeasurement"></a>

Latest 15-minute water-level reading for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Carries only the W (water-level) timeseries; other timeseries (Q discharge, LT water temperature) are not emitted by this source.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable UUID of the gauge this reading was taken at. References the `station_id` of the corresponding Station reference event. Used as the CloudEvents `subject` and the Kafka partition key so all readings for a given gauge land on the same partition / topic key. | altnames=`{"json": "uuid"}` | - | - |
| `timestamp` | `datetime` | `True` | Wall-clock time the upstream reading was taken, in ISO 8601 / RFC 3339 with an explicit UTC offset. PegelOnline publishes the value in Europe/Berlin local time, so the offset shifts between `+01:00` (CET) and `+02:00` (CEST) across the DST boundary — preserve the offset when storing. Sourced from the upstream `timestamp` field. | - | - | - |
| `value` | `double` | `True` | Water-level reading on the W (water-level) timeseries, in centimetres above the gauge's Pegelnullpunkt (PNP — a geodetically fixed datum specific to each gauge, see https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Typical operational range is 0–1500 cm; flood events at major Rhine gauges can exceed 1000 cm. Negative readings are valid at gauges whose normal pool is below PNP (e.g. tidal Elbe at low water). Unit: cm. | unit=`cm` symbol=`cm` | maximum=`2500`<br>minimum=`-1000` | - |
| `stateMnwMhw` | enum `['low', 'normal', 'high', 'unknown', 'commented', 'out-dated']` | `False` | Categorical classification of the current water level against the gauge's long-term mean low water (MNW) and mean high water (MHW) reference values, as computed by the upstream feed. Omitted by upstream when the gauge has no MNW/MHW reference series configured (treat absence as 'unknown'). | altenums=`{"lang:en": {"commented": "Value carries an operator comment overriding the automatic classification", "high": "Above MHW", "low": "Below the gauge's mean low water (MNW) reference", "normal": "Between MNW and the gauge's mean high water (MHW) reference", "out-dated": "Reading is stale relative to the gauge's configured freshness window (typically 90 minutes) — do not treat as authoritative", "unknown": "MNW/MHW reference values are not configured for this station"}}` | - | - |
| `stateNswHsw` | enum `['normal', 'high', 'unknown', 'commented', 'out-dated']` | `False` | Categorical classification of the current water level against the highest navigable water level (HSW) reference for the reach, as computed by the upstream feed. Drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Note: upstream never emits 'low' on this series — HSW is an upper bound only. Omitted by upstream when the gauge has no HSW reference (treat absence as 'unknown'). | altenums=`{"lang:en": {"commented": "Value carries an operator comment overriding the automatic classification", "high": "At or above HSW — navigation typically suspended on the affected reach", "normal": "Below the highest navigable water level (HSW / Höchster Schifffahrtswasserstand)", "out-dated": "Reading is stale relative to the gauge's configured freshness window", "unknown": "HSW reference value is not configured for this station"}}` | - | - |
| `trend` | enum `[-1, 0, 1]` | `False` | Short-term trend of the water level relative to the previous reading, as classified by the upstream feed. First-class signal for flood-monitoring dashboards. Sourced from the upstream `trend` field; omitted when upstream cannot compute a trend (e.g. first reading after a gap). | altenums=`{"lang:en": {"-1": "Falling — current value is below the previous reading", "0": "Steady — within the upstream classification's noise band of the previous reading", "1": "Rising — current value is above the previous reading"}}` | - | - |

### Schemagroup `de.wsv.pegelonline.avro`
<a id="schemagroup-dewsvpegelonlineavro"></a>

#### Schema `de.wsv.pegelonline.Station`
<a id="schema-dewsvpegelonlinestation"></a>

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
| Namespace | de.wsv.pegelonline |
| Type | `record` |
| Doc | WSV PegelOnline gauge installation. Each record represents one physical Pegelmessstelle on a federally administered German inland or coastal waterway. Sourced from GET /stations.json on the PegelOnline REST API v2. Emitted as reference data at bridge startup and re-emitted periodically. Avro mirror of the JsonStructure Station schema — keep field semantics in sync. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Stable UUID assigned by WSV to identify the gauge installation; persists across renaming, relocation, and timeseries reconfiguration. Sourced from the upstream 'uuid' field. Used as the CloudEvents subject and the Kafka partition key. | `-` |
| `number` | `string` | Official WSV Pegelmessstellennummer (6-8 digit numeric identifier) used in published German hydrology bulletins. National identifier only - not globally unique outside Germany; prefer station_id for joins. | `-` |
| `shortname` | `string` | Operator-assigned display label for the gauge (<=40 characters). May differ from the town name when multiple gauges share a town. Mutable - do not use as a routing key or stable identifier. | `-` |
| `longname` | `string` | Canonical gauge name as used in WSV publications (<=255 characters). Mutable - do not use as a routing key. | `-` |
| `km` | `null` \| `double` | Position along the federal waterway expressed as river-kilometre downstream from the waterway's official origin (e.g. Rhine-km 0 at the Old Rhine Bridge in Konstanz). Decimal fraction is the hectometre offset within the km. Null for tidal / coastal gauges and for waterways without a km reference. Unit: km. | `-` |
| `agency` | `string` | Free-form name of the Wasserstrassen- und Schifffahrtsamt (WSA) operating the gauge - e.g. 'WSA RHEIN', 'WSA ELBE'. Sourced from the upstream 'agency' field. Not a stable identifier and not suitable as a routing key. | `-` |
| `longitude` | `double` | WGS84 decimal-degree longitude of the gauge installation; positive east of the prime meridian, range -180..180. Surveyed to the gauge structure, not to the river centreline. Unit: degrees. | `-` |
| `latitude` | `double` | WGS84 decimal-degree latitude of the gauge installation; positive north of the equator, range -90..90. Surveyed to the gauge structure, not to the river centreline. Unit: degrees. | `-` |
| `water` | record `Water` | Federal waterway the gauge measures, sourced from the upstream nested 'water' object. Acts as the routing hierarchy for the MQTT Unified Namespace topology. | `-` |

#### Schema `de.wsv.pegelonline.CurrentMeasurement`
<a id="schema-dewsvpegelonlinecurrentmeasurement"></a>

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
| Name | CurrentMeasurement |
| Namespace | de.wsv.pegelonline |
| Type | `record` |
| Doc | Latest 15-minute water-level reading (W timeseries) for one WSV PegelOnline gauge. Sourced from GET /stations/{uuid}/W/currentmeasurement.json on the PegelOnline REST API v2. Avro mirror of the JsonStructure CurrentMeasurement schema - keep field semantics in sync. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Stable UUID of the gauge this reading was taken at. References the station_id of the corresponding Station reference event. Sourced from the upstream 'uuid' field. | `-` |
| `timestamp` | `long` | Wall-clock time the upstream reading was taken, encoded here as Unix milliseconds since 1970-01-01T00:00:00Z. PegelOnline publishes the value as ISO 8601 with an explicit Europe/Berlin offset (CET +01:00 / CEST +02:00); the bridge converts to UTC milliseconds for Avro encoding. | `-` |
| `value` | `double` | Water-level reading on the W timeseries, in centimetres above the gauge's Pegelnullpunkt (PNP - a geodetically fixed datum specific to each gauge). Typical operational range 0..1500 cm; flood events at major Rhine gauges exceed 1000 cm. Negative readings are valid at gauges whose normal pool is below PNP. Unit: cm. | `-` |
| `stateMnwMhw` | `null` \| enum `StateMnwMhw` | MNW/MHW classification as computed by the upstream feed. Null when the gauge has no MNW/MHW reference series configured. Symbol 'out_dated' means the reading is stale relative to the gauge's freshness window (typically 90 minutes) - do not treat as authoritative. | `-` |
| `stateNswHsw` | `null` \| enum `StateNswHsw` | HSW classification as computed by the upstream feed - drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Null when the gauge has no HSW reference. Upstream never emits 'low' on this series; HSW is an upper bound only. | `-` |
| `trend` | `null` \| `int` | Short-term trend of the water level relative to the previous reading: -1 falling, 0 steady, +1 rising. Sourced from the upstream 'trend' field. Null when upstream cannot compute a trend (e.g. first reading after a gap). | `-` |
