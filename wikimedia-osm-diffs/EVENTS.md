# Table of Contents

- [Org.OpenStreetMap.Diffs](#message-group-orgopenstreetmapdiffs)
  - [Org.OpenStreetMap.Diffs.MapChange](#message-orgopenstreetmapdiffsmapchange)
- [Org.OpenStreetMap.Diffs.State](#message-group-orgopenstreetmapdiffsstate)
  - [Org.OpenStreetMap.Diffs.ReplicationState](#message-orgopenstreetmapdiffsreplicationstate)
- [Org.OpenStreetMap.Diffs.mqtt](#message-group-orgopenstreetmapdiffsmqtt)
  - [Org.OpenStreetMap.Diffs.mqtt.Node](#message-orgopenstreetmapdiffsmqttnode)
  - [Org.OpenStreetMap.Diffs.mqtt.Way](#message-orgopenstreetmapdiffsmqttway)
  - [Org.OpenStreetMap.Diffs.mqtt.Relation](#message-orgopenstreetmapdiffsmqttrelation)
  - [Org.OpenStreetMap.Diffs.mqtt.ReplicationState](#message-orgopenstreetmapdiffsmqttreplicationstate)

---

## Message Group: Org.OpenStreetMap.Diffs
---
### Message: Org.OpenStreetMap.Diffs.MapChange
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{element_type}/{element_id}` |

#### Schema:
##### Object: MapChange
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event describes a create, modify, or delete of a node, way, or relation. Latitude and longitude are present only for node elements. Tags are JSON-encoded because xreg does not support map types natively. The geohash5 axis is the 5-character base32 geohash of the element's representative coordinate; relations without a derivable bounding box receive the sentinel 'nogeo' so they still publish onto the UNS tree.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `change_type` | *string* | - | `True` | The type of change applied to the element in this replication diff: create, modify, or delete, corresponding to the OsmChange XML sections. |
| `element_type` | *string* | - | `True` | The OSM element type: node, way, or relation. Nodes carry geographic coordinates; ways and relations reference other elements. |
| `element_id` | *int64* | - | `True` | The unique numeric identifier of the OSM element within its element type namespace. Combined with element_type, this forms the globally unique OSM element identity. |
| `geohash5` | *string* (optional) | - | `False` | Five-character base32 geohash of the element's representative coordinate. For nodes, derived from latitude/longitude; for ways and relations, derived from the centroid of any embedded bbox. The sentinel 'nogeo' is emitted for elements with no resolvable coordinate (most relation deletes, member-only edits, etc.) so the UNS topic placeholder always resolves to a fixed-shape lowercase ASCII segment. Null only on legacy payloads predating the MQTT axis. |
| `version` | *int32* | - | `True` | The version number of this element. Each edit to an element increments the version by one. |
| `timestamp` | *datetime* | - | `True` | The UTC timestamp when this element version was created or last modified in the OSM database, as recorded in the OsmChange XML. |
| `changeset_id` | *int64* | - | `True` | The numeric identifier of the OSM changeset that contains this element change. A changeset groups related edits by a single user. |
| `user_name` | *string* (optional) | - | `False` | The display name of the OSM user who made this edit. May be null for redacted or anonymous edits. |
| `user_id` | *int64* (optional) | - | `False` | The numeric user identifier of the OSM contributor. May be null for redacted or anonymous edits. |
| `latitude` | *double* (optional) | - | `False` | The WGS-84 latitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `longitude` | *double* (optional) | - | `False` | The WGS-84 longitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `tags` | *string* | - | `True` | JSON-encoded object of key-value tag pairs attached to this element. Tags describe the element's real-world features such as name, highway type, or building classification. Encoded as a JSON string because xreg does not natively support map types. |
| `sequence_number` | *int64* | - | `True` | The replication sequence number of the minutely diff file that contained this change. Useful for correlating changes back to specific replication state. |
## Message Group: Org.OpenStreetMap.Diffs.State
---
### Message: Org.OpenStreetMap.Diffs.ReplicationState
*Current replication state from the OpenStreetMap minutely diff feed. Emitted once per poll cycle to record which replication sequence was just processed. The state is read from https://planet.openstreetmap.org/replication/minute/state.txt.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Org.OpenStreetMap.Diffs.ReplicationState` |
| `source` |  | `` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `replication_state` |

#### Schema:
##### Object: ReplicationState
*The current replication state of the OpenStreetMap minutely diff feed. Published once per poll cycle. The sequence_number and timestamp are parsed from the Java-properties-style state.txt file at https://planet.openstreetmap.org/replication/minute/state.txt.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `sequence_number` | *int64* | - | `True` | The monotonically increasing sequence number of the latest processed minutely diff file. Each diff file corresponds to exactly one sequence number. |
| `timestamp` | *datetime* | - | `True` | The UTC timestamp associated with the replication state, indicating the point in time up to which the diff file covers OSM edits. |
| `source_url` | *string* (optional) | - | `False` | The replication state document URL from which this snapshot was parsed. Useful so subscribers can re-derive the diff file URL or compare across mirror feeds. Null when the bridge does not record the URL. |
## Message Group: Org.OpenStreetMap.Diffs.mqtt
---
### Message: Org.OpenStreetMap.Diffs.mqtt.Node
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{element_id}` |

#### Schema:
##### Object: MapChange
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event describes a create, modify, or delete of a node, way, or relation. Latitude and longitude are present only for node elements. Tags are JSON-encoded because xreg does not support map types natively. The geohash5 axis is the 5-character base32 geohash of the element's representative coordinate; relations without a derivable bounding box receive the sentinel 'nogeo' so they still publish onto the UNS tree.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `change_type` | *string* | - | `True` | The type of change applied to the element in this replication diff: create, modify, or delete, corresponding to the OsmChange XML sections. |
| `element_type` | *string* | - | `True` | The OSM element type: node, way, or relation. Nodes carry geographic coordinates; ways and relations reference other elements. |
| `element_id` | *int64* | - | `True` | The unique numeric identifier of the OSM element within its element type namespace. Combined with element_type, this forms the globally unique OSM element identity. |
| `geohash5` | *string* (optional) | - | `False` | Five-character base32 geohash of the element's representative coordinate. For nodes, derived from latitude/longitude; for ways and relations, derived from the centroid of any embedded bbox. The sentinel 'nogeo' is emitted for elements with no resolvable coordinate (most relation deletes, member-only edits, etc.) so the UNS topic placeholder always resolves to a fixed-shape lowercase ASCII segment. Null only on legacy payloads predating the MQTT axis. |
| `version` | *int32* | - | `True` | The version number of this element. Each edit to an element increments the version by one. |
| `timestamp` | *datetime* | - | `True` | The UTC timestamp when this element version was created or last modified in the OSM database, as recorded in the OsmChange XML. |
| `changeset_id` | *int64* | - | `True` | The numeric identifier of the OSM changeset that contains this element change. A changeset groups related edits by a single user. |
| `user_name` | *string* (optional) | - | `False` | The display name of the OSM user who made this edit. May be null for redacted or anonymous edits. |
| `user_id` | *int64* (optional) | - | `False` | The numeric user identifier of the OSM contributor. May be null for redacted or anonymous edits. |
| `latitude` | *double* (optional) | - | `False` | The WGS-84 latitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `longitude` | *double* (optional) | - | `False` | The WGS-84 longitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `tags` | *string* | - | `True` | JSON-encoded object of key-value tag pairs attached to this element. Tags describe the element's real-world features such as name, highway type, or building classification. Encoded as a JSON string because xreg does not natively support map types. |
| `sequence_number` | *int64* | - | `True` | The replication sequence number of the minutely diff file that contained this change. Useful for correlating changes back to specific replication state. |
---
### Message: Org.OpenStreetMap.Diffs.mqtt.Way
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{element_id}` |

#### Schema:
##### Object: MapChange
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event describes a create, modify, or delete of a node, way, or relation. Latitude and longitude are present only for node elements. Tags are JSON-encoded because xreg does not support map types natively. The geohash5 axis is the 5-character base32 geohash of the element's representative coordinate; relations without a derivable bounding box receive the sentinel 'nogeo' so they still publish onto the UNS tree.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `change_type` | *string* | - | `True` | The type of change applied to the element in this replication diff: create, modify, or delete, corresponding to the OsmChange XML sections. |
| `element_type` | *string* | - | `True` | The OSM element type: node, way, or relation. Nodes carry geographic coordinates; ways and relations reference other elements. |
| `element_id` | *int64* | - | `True` | The unique numeric identifier of the OSM element within its element type namespace. Combined with element_type, this forms the globally unique OSM element identity. |
| `geohash5` | *string* (optional) | - | `False` | Five-character base32 geohash of the element's representative coordinate. For nodes, derived from latitude/longitude; for ways and relations, derived from the centroid of any embedded bbox. The sentinel 'nogeo' is emitted for elements with no resolvable coordinate (most relation deletes, member-only edits, etc.) so the UNS topic placeholder always resolves to a fixed-shape lowercase ASCII segment. Null only on legacy payloads predating the MQTT axis. |
| `version` | *int32* | - | `True` | The version number of this element. Each edit to an element increments the version by one. |
| `timestamp` | *datetime* | - | `True` | The UTC timestamp when this element version was created or last modified in the OSM database, as recorded in the OsmChange XML. |
| `changeset_id` | *int64* | - | `True` | The numeric identifier of the OSM changeset that contains this element change. A changeset groups related edits by a single user. |
| `user_name` | *string* (optional) | - | `False` | The display name of the OSM user who made this edit. May be null for redacted or anonymous edits. |
| `user_id` | *int64* (optional) | - | `False` | The numeric user identifier of the OSM contributor. May be null for redacted or anonymous edits. |
| `latitude` | *double* (optional) | - | `False` | The WGS-84 latitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `longitude` | *double* (optional) | - | `False` | The WGS-84 longitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `tags` | *string* | - | `True` | JSON-encoded object of key-value tag pairs attached to this element. Tags describe the element's real-world features such as name, highway type, or building classification. Encoded as a JSON string because xreg does not natively support map types. |
| `sequence_number` | *int64* | - | `True` | The replication sequence number of the minutely diff file that contained this change. Useful for correlating changes back to specific replication state. |
---
### Message: Org.OpenStreetMap.Diffs.mqtt.Relation
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event represents a single create, modify, or delete operation on a node, way, or relation in the OSM database. The diff files are OsmChange XML documents published every 60 seconds at https://planet.openstreetmap.org/replication/minute/.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` |  | `` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `{geohash5}/{element_id}` |

#### Schema:
##### Object: MapChange
*An individual element change from the OpenStreetMap minutely replication diff feed. Each event describes a create, modify, or delete of a node, way, or relation. Latitude and longitude are present only for node elements. Tags are JSON-encoded because xreg does not support map types natively. The geohash5 axis is the 5-character base32 geohash of the element's representative coordinate; relations without a derivable bounding box receive the sentinel 'nogeo' so they still publish onto the UNS tree.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `change_type` | *string* | - | `True` | The type of change applied to the element in this replication diff: create, modify, or delete, corresponding to the OsmChange XML sections. |
| `element_type` | *string* | - | `True` | The OSM element type: node, way, or relation. Nodes carry geographic coordinates; ways and relations reference other elements. |
| `element_id` | *int64* | - | `True` | The unique numeric identifier of the OSM element within its element type namespace. Combined with element_type, this forms the globally unique OSM element identity. |
| `geohash5` | *string* (optional) | - | `False` | Five-character base32 geohash of the element's representative coordinate. For nodes, derived from latitude/longitude; for ways and relations, derived from the centroid of any embedded bbox. The sentinel 'nogeo' is emitted for elements with no resolvable coordinate (most relation deletes, member-only edits, etc.) so the UNS topic placeholder always resolves to a fixed-shape lowercase ASCII segment. Null only on legacy payloads predating the MQTT axis. |
| `version` | *int32* | - | `True` | The version number of this element. Each edit to an element increments the version by one. |
| `timestamp` | *datetime* | - | `True` | The UTC timestamp when this element version was created or last modified in the OSM database, as recorded in the OsmChange XML. |
| `changeset_id` | *int64* | - | `True` | The numeric identifier of the OSM changeset that contains this element change. A changeset groups related edits by a single user. |
| `user_name` | *string* (optional) | - | `False` | The display name of the OSM user who made this edit. May be null for redacted or anonymous edits. |
| `user_id` | *int64* (optional) | - | `False` | The numeric user identifier of the OSM contributor. May be null for redacted or anonymous edits. |
| `latitude` | *double* (optional) | - | `False` | The WGS-84 latitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `longitude` | *double* (optional) | - | `False` | The WGS-84 longitude of the node in decimal degrees. Present only when element_type is node; null for ways and relations. |
| `tags` | *string* | - | `True` | JSON-encoded object of key-value tag pairs attached to this element. Tags describe the element's real-world features such as name, highway type, or building classification. Encoded as a JSON string because xreg does not natively support map types. |
| `sequence_number` | *int64* | - | `True` | The replication sequence number of the minutely diff file that contained this change. Useful for correlating changes back to specific replication state. |
---
### Message: Org.OpenStreetMap.Diffs.mqtt.ReplicationState
*Current replication state from the OpenStreetMap minutely diff feed. Emitted once per poll cycle to record which replication sequence was just processed. The state is read from https://planet.openstreetmap.org/replication/minute/state.txt.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Org.OpenStreetMap.Diffs.ReplicationState` |
| `source` |  | `` | `False` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` |  | `uritemplate` | `False` | `replication-state` |

#### Schema:
##### Object: ReplicationState
*The current replication state of the OpenStreetMap minutely diff feed. Published once per poll cycle. The sequence_number and timestamp are parsed from the Java-properties-style state.txt file at https://planet.openstreetmap.org/replication/minute/state.txt.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `sequence_number` | *int64* | - | `True` | The monotonically increasing sequence number of the latest processed minutely diff file. Each diff file corresponds to exactly one sequence number. |
| `timestamp` | *datetime* | - | `True` | The UTC timestamp associated with the replication state, indicating the point in time up to which the diff file covers OSM edits. |
| `source_url` | *string* (optional) | - | `False` | The replication state document URL from which this snapshot was parsed. Useful so subscribers can re-derive the diff file URL or compare across mirror feeds. Null when the bridge does not record the URL. |
