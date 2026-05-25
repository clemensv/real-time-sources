# OpenStreetMap Minutely Diffs Bridge Events

MQTT/5.0 UNS variants of the Wikimedia OSM Diffs CloudEvents. The minutely diff stream is split into three non-retained firehose families (node, way, relation) under osm/intl/wikimedia/wikimedia-osm-diffs/<family>/{geohash5}/{element_id}/change with QoS 0 and retain=false, and one retained side-channel snapshot for the OSM replication sequence published to osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state with retain=true so late subscribers can see the most recent processed sequence number on connect.

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
| Messagegroups | 3 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `Org.OpenStreetMap.Diffs.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Org.OpenStreetMap.Diffs`](#messagegroup-orgopenstreetmapdiffs) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wikimedia-osm-diffs` |
| Kafka key | `{element_type}/{element_id}` |
| Deployed | False |

### Endpoint `Org.OpenStreetMap.Diffs.State.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Org.OpenStreetMap.Diffs.State`](#messagegroup-orgopenstreetmapdiffsstate) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wikimedia-osm-diffs` |
| Kafka key | `replication_state` |
| Deployed | False |

### Endpoint `WikimediaOsmDiffs.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`Org.OpenStreetMap.Diffs.mqtt`](#messagegroup-orgopenstreetmapdiffsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `Org.OpenStreetMap.Diffs`
<a id="messagegroup-orgopenstreetmapdiffs"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Org.OpenStreetMap.Diffs.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Org.OpenStreetMap.Diffs.MapChange`
<a id="message-orgopenstreetmapdiffsmapchange"></a>

An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.

| Field | Value |
| --- | --- |
| Name | MapChange |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Org.OpenStreetMap.Diffs.jstruct/schemas/Org.OpenStreetMap.Diffs.MapChange`](#schema-orgopenstreetmapdiffsmapchange) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `string` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{element_type}/{element_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Org.OpenStreetMap.Diffs.Kafka` | `KAFKA` | topic `wikimedia-osm-diffs`; key `{element_type}/{element_id}` |

### Messagegroup `Org.OpenStreetMap.Diffs.State`
<a id="messagegroup-orgopenstreetmapdiffsstate"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Org.OpenStreetMap.Diffs.State.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Org.OpenStreetMap.Diffs.ReplicationState`
<a id="message-orgopenstreetmapdiffsreplicationstate"></a>

Current replication state from the OpenStreetMap minutely diff feed. Emitted once per poll cycle to record which replication sequence was just processed. The state is read from https://planet.openstreetmap.org/replication/minute/state.txt.

| Field | Value |
| --- | --- |
| Name | ReplicationState |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Org.OpenStreetMap.Diffs.jstruct/schemas/Org.OpenStreetMap.Diffs.ReplicationState`](#schema-orgopenstreetmapdiffsreplicationstate) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Org.OpenStreetMap.Diffs.ReplicationState` |
| `source` |  | `string` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `replication_state` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Org.OpenStreetMap.Diffs.State.Kafka` | `KAFKA` | topic `wikimedia-osm-diffs`; key `replication_state` |

### Messagegroup `Org.OpenStreetMap.Diffs.mqtt`
<a id="messagegroup-orgopenstreetmapdiffsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 UNS variants of the Wikimedia OSM Diffs CloudEvents. The minutely diff stream is split into three non-retained firehose families (node, way, relation) under osm/intl/wikimedia/wikimedia-osm-diffs/<family>/{geohash5}/{element_id}/change with QoS 0 and retain=false, and one retained side-channel snapshot for the OSM replication sequence published to osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state with retain=true so late subscribers can see the most recent processed sequence number on connect. |
| Transport bindings | `WikimediaOsmDiffs.Mqtt` (MQTT/5.0) |
| Messages | 4 |

#### Message `Org.OpenStreetMap.Diffs.mqtt.Node`
<a id="message-orgopenstreetmapdiffsmqttnode"></a>

An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.

| Field | Value |
| --- | --- |
| Name | Node |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Org.OpenStreetMap.Diffs.jstruct/schemas/Org.OpenStreetMap.Diffs.MapChange`](#schema-orgopenstreetmapdiffsmapchange) |
| Base message chain | `/messagegroups/Org.OpenStreetMap.Diffs/messages/Org.OpenStreetMap.Diffs.MapChange` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `string` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{element_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `WikimediaOsmDiffs.Mqtt` | `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change` |
| Retain | False |

#### Message `Org.OpenStreetMap.Diffs.mqtt.Way`
<a id="message-orgopenstreetmapdiffsmqttway"></a>

An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.

| Field | Value |
| --- | --- |
| Name | Way |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Org.OpenStreetMap.Diffs.jstruct/schemas/Org.OpenStreetMap.Diffs.MapChange`](#schema-orgopenstreetmapdiffsmapchange) |
| Base message chain | `/messagegroups/Org.OpenStreetMap.Diffs/messages/Org.OpenStreetMap.Diffs.MapChange` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `string` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{element_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `WikimediaOsmDiffs.Mqtt` | `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change` |
| Retain | False |

#### Message `Org.OpenStreetMap.Diffs.mqtt.Relation`
<a id="message-orgopenstreetmapdiffsmqttrelation"></a>

An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.

| Field | Value |
| --- | --- |
| Name | Relation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Org.OpenStreetMap.Diffs.jstruct/schemas/Org.OpenStreetMap.Diffs.MapChange`](#schema-orgopenstreetmapdiffsmapchange) |
| Base message chain | `/messagegroups/Org.OpenStreetMap.Diffs/messages/Org.OpenStreetMap.Diffs.MapChange` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `string` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{element_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `WikimediaOsmDiffs.Mqtt` | `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change` |
| Retain | False |

#### Message `Org.OpenStreetMap.Diffs.mqtt.ReplicationState`
<a id="message-orgopenstreetmapdiffsmqttreplicationstate"></a>

Current replication state from the OpenStreetMap minutely diff feed. Emitted once per poll cycle to record which replication sequence was just processed. The state is read from https://planet.openstreetmap.org/replication/minute/state.txt.

| Field | Value |
| --- | --- |
| Name | ReplicationState |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Org.OpenStreetMap.Diffs.jstruct/schemas/Org.OpenStreetMap.Diffs.ReplicationState`](#schema-orgopenstreetmapdiffsreplicationstate) |
| Base message chain | `/messagegroups/Org.OpenStreetMap.Diffs.State/messages/Org.OpenStreetMap.Diffs.ReplicationState` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Org.OpenStreetMap.Diffs.ReplicationState` |
| `source` |  | `string` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `replication-state` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `WikimediaOsmDiffs.Mqtt` | `MQTT/5.0` | topic `osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `Org.OpenStreetMap.Diffs.jstruct`
<a id="schemagroup-orgopenstreetmapdiffsjstruct"></a>

#### Schema `Org.OpenStreetMap.Diffs.MapChange`
<a id="schema-orgopenstreetmapdiffsmapchange"></a>

| Field | Value |
| --- | --- |
| Name | MapChange |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Org/OpenStreetMap/Diffs/MapChange` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MapChange`
<a id="schema-node-mapchange"></a>

An individual element change from the OpenStreetMap minutely replication diff feed. Each event describes a create, modify, or delete of a node, way, or relation. Latitude and longitude are present only for node elements. Tags are JSON-encoded because xreg does not support map types natively. The geohash5 axis is the 5-character base32 geohash of the element's representative coordinate; relations without a derivable bounding box receive the sentinel 'nogeo' so they still publish onto the UNS tree.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Org/OpenStreetMap/Diffs/MapChange` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `change_type` | `string` | `True` | The type of change applied to the element in this replication diff: create, modify, or delete, corresponding to the OsmChange XML sections. | - | - | - |
| `element_type` | `string` | `True` | The OSM element type: node, way, or relation. Nodes carry geographic coordinates; ways and relations reference other elements. | - | - | - |
| `element_id` | `int64` | `True` | The unique numeric identifier of the OSM element within its element type namespace. Combined with element_type, this forms the globally unique OSM element identity. | - | - | - |
| `geohash5` | `string` | `True` | Five-character base32 geohash of the element's representative coordinate. For nodes, derived from latitude/longitude; for ways and relations, derived from the centroid of any embedded bbox. The sentinel 'nogeo' is emitted for elements with no resolvable coordinate (most relation deletes, member-only edits, etc.) so the UNS topic placeholder always resolves to a fixed-shape lowercase ASCII segment. | - | - | - |
| `version` | `int32` | `True` | The version number of this element. Each edit to an element increments the version by one. | - | - | - |
| `timestamp` | `datetime` | `True` | The UTC timestamp when this element version was created or last modified in the OSM database, as recorded in the OsmChange XML. | - | - | - |
| `changeset_id` | `int64` | `True` | The numeric identifier of the OSM changeset that contains this element change. A changeset groups related edits by a single user. | - | - | - |
| `user_name` | `union` | `False` | The display name of the OSM user who made this edit. May be null for redacted or anonymous edits. | - | - | - |
| `user_id` | `union` | `False` | The numeric user identifier of the OSM contributor. May be null for redacted or anonymous edits. | - | - | - |
| `latitude` | `union` | `False` | The WGS-84 latitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. | - | - | - |
| `longitude` | `union` | `False` | The WGS-84 longitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. | - | - | - |
| `tags` | `string` | `True` | JSON-encoded object of key-value tag pairs attached to this element. Tags describe the element's real-world features such as name, highway type, or building classification. Encoded as a JSON string because xreg does not natively support map types. | - | - | - |
| `sequence_number` | `int64` | `True` | The replication sequence number of the minutely diff file that contained this change. Useful for correlating changes back to specific replication state. | - | - | - |

#### Schema `Org.OpenStreetMap.Diffs.ReplicationState`
<a id="schema-orgopenstreetmapdiffsreplicationstate"></a>

| Field | Value |
| --- | --- |
| Name | ReplicationState |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Org/OpenStreetMap/Diffs/ReplicationState` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ReplicationState`
<a id="schema-node-replicationstate"></a>

The current replication state of the OpenStreetMap minutely diff feed. Published once per poll cycle. The sequence_number and timestamp are parsed from the Java-properties-style state.txt file at https://planet.openstreetmap.org/replication/minute/state.txt.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Org/OpenStreetMap/Diffs/ReplicationState` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sequence_number` | `int64` | `True` | The monotonically increasing sequence number of the latest processed minutely diff file. Each diff file corresponds to exactly one sequence number. | - | - | - |
| `timestamp` | `datetime` | `True` | The UTC timestamp associated with the replication state, indicating the point in time up to which the diff file covers OSM edits. | - | - | - |
| `source_url` | `union` | `False` | The replication state document URL from which this snapshot was parsed. Useful so subscribers can re-derive the diff file URL or compare across mirror feeds. Null when the bridge does not record the URL. | - | - | - |
