# Table of Contents

- [Blitzortung.Lightning](#message-group-blitzortunglightning)
  - [Blitzortung.Lightning.LightningStroke](#message-blitzortunglightninglightningstroke)
- [Blitzortung.Lightning.mqtt](#message-group-blitzortunglightningmqtt)
  - [Blitzortung.Lightning.mqtt.LightningStroke](#message-blitzortunglightningmqttlightningstroke)

---

## Message Group: Blitzortung.Lightning
---
### Message: Blitzortung.Lightning.LightningStroke
*Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. Each event represents one source-scoped stroke identifier with its observation time, coordinates, upstream delay and accuracy values, and optionally the detector participation flags carried in the public sta object.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Blitzortung.Lightning.LightningStroke` |
| `source` |  | `` | `False` | `wss://live.lightningmaps.org/` |
| `subject` |  | `uritemplate` | `False` | `{source_id}/{stroke_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: LightningStroke
*One located lightning stroke from the public LightningMaps / Blitzortung live websocket feed. The stroke identity is the tuple of source_id and stroke_id because the upstream browser client tracks the last seen stroke id separately for each source stream.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `source_id` | *int32* | - | `True` | Upstream live-source identifier from the src field. The public LightningMaps websocket treats stroke ids as source-scoped, so this field is part of the stable event identity. |
| `stroke_id` | *string* | - | `True` | Source-scoped stroke identifier from the upstream id field, stringified so the Kafka key and CloudEvents subject can be resolved directly from the payload. |
| `event_time` | *string* | - | `True` | ISO-8601 UTC timestamp derived from the upstream time field, which the public live websocket emits in Unix epoch milliseconds. |
| `event_timestamp_ms` | *int64* | - | `True` | Original upstream time value in Unix epoch milliseconds from the public live websocket. |
| `latitude` | *double* | - | `True` | Latitude of the located lightning stroke in decimal degrees from the upstream lat field. |
| `longitude` | *double* | - | `True` | Longitude of the located lightning stroke in decimal degrees from the upstream lon field. |
| `server_id` | *int32* (optional) | - | `False` | Upstream server identifier from the srv field that produced the current live batch. The public documentation reviewed during implementation does not publish a stable human-readable enumeration for these ids. |
| `server_delay_ms` | *int32* (optional) | millisecond (ms) | `False` | Delay between the upstream server receiving or computing the stroke and sending it to the live client, in milliseconds, from the public del field. |
| `accuracy_diameter_m` | *double* (optional) | meter (m) | `False` | Estimated accuracy diameter in meters from the upstream dev field. The public LightningMaps client renders an accuracy circle with radius dev/2, which indicates the value is expressed as a diameter rather than a raw algorithm score. |
| `detector_participations` | array of *unknown* | - | `True` | Detector participation entries expanded from the upstream sta object when the client asks the public live feed to include station details. An empty array means the upstream batch did not include detector participation details for this stroke. |
## Message Group: Blitzortung.Lightning.mqtt
---
### Message: Blitzortung.Lightning.mqtt.LightningStroke
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Blitzortung.Lightning.mqtt.LightningStroke` |
| `source` |  | `` | `False` | `wss://live.lightningmaps.org/` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{geohash7}/{stroke_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: LightningStroke
*MQTT/UNS variant of the Blitzortung LightningStroke event. Extends the Kafka schema with the required geohash5 and geohash7 axes (derived in the bridge from latitude/longitude) so the MQTT topic placeholders resolve from real payload fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `source_id` | *int32* | - | `True` | Upstream live-source identifier from the src field. The public LightningMaps websocket treats stroke ids as source-scoped, so this field is part of the stable event identity. |
| `stroke_id` | *string* | - | `True` | Source-scoped stroke identifier from the upstream id field, stringified so the Kafka key and CloudEvents subject can be resolved directly from the payload. |
| `event_time` | *string* | - | `True` | ISO-8601 UTC timestamp derived from the upstream time field, which the public live websocket emits in Unix epoch milliseconds. |
| `event_timestamp_ms` | *int64* | - | `True` | Original upstream time value in Unix epoch milliseconds from the public live websocket. |
| `latitude` | *double* | - | `True` | Latitude of the located lightning stroke in decimal degrees from the upstream lat field. |
| `longitude` | *double* | - | `True` | Longitude of the located lightning stroke in decimal degrees from the upstream lon field. |
| `server_id` | *int32* (optional) | - | `False` | Upstream server identifier from the srv field that produced the current live batch. The public documentation reviewed during implementation does not publish a stable human-readable enumeration for these ids. |
| `server_delay_ms` | *int32* (optional) | millisecond (ms) | `False` | Delay between the upstream server receiving or computing the stroke and sending it to the live client, in milliseconds, from the public del field. |
| `accuracy_diameter_m` | *double* (optional) | meter (m) | `False` | Estimated accuracy diameter in meters from the upstream dev field. The public LightningMaps client renders an accuracy circle with radius dev/2, which indicates the value is expressed as a diameter rather than a raw algorithm score. |
| `detector_participations` | array of *unknown* | - | `True` | Detector participation entries expanded from the upstream sta object when the client asks the public live feed to include station details. An empty array means the upstream batch did not include detector participation details for this stroke. |
| `geohash5` | *string* | - | `True` | 5-character geohash of the stroke (latitude, longitude) using the standard base-32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. Used as the UNS '{geohash5}' topic placeholder. |
| `geohash7` | *string* | - | `True` | 7-character geohash of the stroke (latitude, longitude). Approx. 153 m x 153 m cells at the equator. Used as the UNS '{geohash7}' topic placeholder for fine-grained location subscriptions. |
