# USGS Earthquake Hazards Program - Real-time Earthquake Feed Events

MQTT/5.0 transport variant for USGS earthquake events. Non-retained QoS-1 event stream routed by contributor network, magnitude bucket, and event code under seismic/intl/usgs/usgs-earthquakes/... Buckets are m0 for <1 or unknown, m1..m6 for [1,7), and m7plus for >=7.

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

### Endpoint `USGS.Earthquakes.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`USGS.Earthquakes`](#messagegroup-usgsearthquakes) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `usgs-earthquakes` |
| Kafka key | `{net}/{code}` |
| Deployed | False |

### Endpoint `USGS.Earthquakes.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`USGS.Earthquakes.mqtt`](#messagegroup-usgsearthquakesmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `USGS.Earthquakes`
<a id="messagegroup-usgsearthquakes"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `USGS.Earthquakes.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `USGS.Earthquakes.Event`
<a id="message-usgsearthquakesevent"></a>

USGS earthquake event data from the Earthquake Hazards Program.

| Field | Value |
| --- | --- |
| Name | Event |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.Earthquakes.jstruct/schemas/USGS.Earthquakes.Event`](#schema-usgsearthquakesevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.Earthquakes.Event` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{net}/{code}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Earthquakes.Kafka` | `KAFKA` | topic `usgs-earthquakes`; key `{net}/{code}` |

### Messagegroup `USGS.Earthquakes.mqtt`
<a id="messagegroup-usgsearthquakesmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for USGS earthquake events. Non-retained QoS-1 event stream routed by contributor network, magnitude bucket, and event code under seismic/intl/usgs/usgs-earthquakes/... Buckets are m0 for <1 or unknown, m1..m6 for [1,7), and m7plus for >=7. |
| Transport bindings | `USGS.Earthquakes.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `USGS.Earthquakes.mqtt.Event`
<a id="message-usgsearthquakesmqttevent"></a>

USGS earthquake event data from the Earthquake Hazards Program.

| Field | Value |
| --- | --- |
| Name | Event |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.Earthquakes.jstruct/schemas/USGS.Earthquakes.Event`](#schema-usgsearthquakesevent) |
| Base message chain | `/messagegroups/USGS.Earthquakes/messages/USGS.Earthquakes.Event` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.Earthquakes.Event` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{net}/{code}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Earthquakes.Mqtt` | `MQTT/5.0` | topic `seismic/intl/usgs/usgs-earthquakes/{net}/{magnitude_bucket}/{code}/quake` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `seismic/intl/usgs/usgs-earthquakes/{net}/{magnitude_bucket}/{code}/quake` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `USGS.Earthquakes.jstruct`
<a id="schemagroup-usgsearthquakesjstruct"></a>

#### Schema `USGS.Earthquakes.Event`
<a id="schema-usgsearthquakesevent"></a>

| Field | Value |
| --- | --- |
| Name | Event |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/Earthquakes/Event` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/Earthquakes/Event` |
| Type | `object` |

###### Object `Event`
<a id="schema-node-event"></a>

USGS earthquake event data from the Earthquake Hazards Program.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | `string` | `True` | Unique identifier for the earthquake event. | - | - | - |
| `magnitude` | `double` | `False` | Magnitude of the earthquake. | - | - | - |
| `mag_type` | `string` | `False` | Method or algorithm used to calculate the magnitude (e.g. ml, md, mb, mww). | - | - | - |
| `place` | `string` | `False` | Textual description of the named geographic region near the event. | - | - | - |
| `event_time` | `string` | `True` | Time of the earthquake event in ISO-8601 format. | - | - | - |
| `updated` | `string` | `True` | Time when the event was most recently updated in ISO-8601 format. | - | - | - |
| `url` | `string` | `False` | Link to USGS Event Page for this event. | - | - | - |
| `detail_url` | `string` | `False` | Link to GeoJSON detail feed for this event. | - | - | - |
| `felt` | `union` | `False` | Number of felt reports submitted to the DYFI system. | - | - | - |
| `cdi` | `union` | `False` | Maximum reported community determined intensity (DYFI). | - | - | - |
| `mmi` | `union` | `False` | Maximum estimated instrumental intensity (ShakeMap). | - | - | - |
| `alert` | `union` | `False` | PAGER alert level (green, yellow, orange, red). | - | - | - |
| `status` | `string` | `True` | Review status of the event (automatic, reviewed, deleted). | - | - | - |
| `tsunami` | `int32` | `True` | Flag indicating whether the event has a tsunami advisory (1=yes, 0=no). | - | - | - |
| `sig` | `int32` | `False` | Significance of the event, a number describing how significant the event is (0-1000). | - | - | - |
| `net` | `string` | `True` | ID of the data contributor network. | - | - | - |
| `code` | `string` | `True` | Identifying code assigned by the corresponding source for the event. | - | - | - |
| `sources` | `string` | `False` | Comma-separated list of network contributors. | - | - | - |
| `nst` | `int32` | `False` | Number of seismic stations used to determine earthquake location. | - | - | - |
| `dmin` | `double` | `False` | Horizontal distance from the epicenter to the nearest station (degrees). | - | - | - |
| `rms` | `double` | `False` | Root-mean-square travel time residual (seconds). | - | - | - |
| `gap` | `double` | `False` | Largest azimuthal gap between azimuthally adjacent stations (degrees). | - | - | - |
| `event_type` | `string` | `False` | Type of seismic event (earthquake, quarry blast, etc.). | - | - | - |
| `latitude` | `double` | `True` | Latitude of the earthquake epicenter in decimal degrees. | - | - | - |
| `longitude` | `double` | `True` | Longitude of the earthquake epicenter in decimal degrees. | - | - | - |
| `depth` | `double` | `False` | Depth of the earthquake in kilometers. | - | - | - |
| `magnitude_bucket` | `string` | `True` | Topic-safe magnitude bucket: m0 for magnitude <1 or unknown, m1..m6 for [1,7), and m7plus for magnitude >=7. | - | - | - |

### Schemagroup `USGS.Earthquakes.avro`
<a id="schemagroup-usgsearthquakesavro"></a>

#### Schema `USGS.Earthquakes.Event`
<a id="schema-usgsearthquakesevent"></a>

| Field | Value |
| --- | --- |
| Name | Event |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS earthquake event data from the Earthquake Hazards Program. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Event |
| Namespace | USGS.Earthquakes |
| Type | `record` |
| Doc | USGS earthquake event data from the Earthquake Hazards Program. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `id` | `string` | Unique identifier for the earthquake event. | `-` |
| `magnitude` | `double` \| `null` | Magnitude of the earthquake. | `-` |
| `magnitude_bucket` | `string` | Topic-safe magnitude bucket: m0 for magnitude <1 or unknown, m1..m6 for [1,7), and m7plus for magnitude >=7. | `m0` |
| `mag_type` | `string` \| `null` | Method or algorithm used to calculate the magnitude (e.g. ml, md, mb, mww). | `-` |
| `place` | `string` \| `null` | Textual description of the named geographic region near the event. | `-` |
| `event_time` | `string` | Time of the earthquake event in ISO-8601 format. | `-` |
| `updated` | `string` | Time when the event was most recently updated in ISO-8601 format. | `-` |
| `url` | `string` \| `null` | Link to USGS Event Page for this event. | `-` |
| `detail_url` | `string` \| `null` | Link to GeoJSON detail feed for this event. | `-` |
| `felt` | `int` \| `null` | Number of felt reports submitted to the DYFI system. | `-` |
| `cdi` | `double` \| `null` | Maximum reported community determined intensity (DYFI). | `-` |
| `mmi` | `double` \| `null` | Maximum estimated instrumental intensity (ShakeMap). | `-` |
| `alert` | `string` \| `null` | PAGER alert level (green, yellow, orange, red). | `-` |
| `status` | `string` | Review status of the event (automatic, reviewed, deleted). | `-` |
| `tsunami` | `int` | Flag indicating whether the event has a tsunami advisory (1=yes, 0=no). | `-` |
| `sig` | `int` \| `null` | Significance of the event, a number describing how significant the event is (0-1000). | `-` |
| `net` | `string` | ID of the data contributor network. | `-` |
| `code` | `string` | Identifying code assigned by the corresponding source for the event. | `-` |
| `sources` | `string` \| `null` | Comma-separated list of network contributors. | `-` |
| `nst` | `int` \| `null` | Number of seismic stations used to determine earthquake location. | `-` |
| `dmin` | `double` \| `null` | Horizontal distance from the epicenter to the nearest station (degrees). | `-` |
| `rms` | `double` \| `null` | Root-mean-square travel time residual (seconds). | `-` |
| `gap` | `double` \| `null` | Largest azimuthal gap between azimuthally adjacent stations (degrees). | `-` |
| `event_type` | `string` \| `null` | Type of seismic event (earthquake, quarry blast, etc.). | `-` |
| `latitude` | `double` | Latitude of the earthquake epicenter in decimal degrees. | `-` |
| `longitude` | `double` | Longitude of the earthquake epicenter in decimal degrees. | `-` |
| `depth` | `double` \| `null` | Depth of the earthquake in kilometers. | `-` |
