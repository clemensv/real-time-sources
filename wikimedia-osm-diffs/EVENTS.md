# OpenStreetMap Minutely Diffs Events

This document describes the events emitted by the OpenStreetMap Minutely
Diffs bridge.

- [Org.OpenStreetMap.Diffs.State](#message-group-orgopenstreetmapdiffsstate)
  - [Org.OpenStreetMap.Diffs.ReplicationState](#message-orgopenstreetmapdiffsreplicationstate)
- [Org.OpenStreetMap.Diffs](#message-group-orgopenstreetmapdiffs)
  - [Org.OpenStreetMap.Diffs.MapChange](#message-orgopenstreetmapdiffsmapchange)

---

## Message Group: Org.OpenStreetMap.Diffs.State

---

### Message: Org.OpenStreetMap.Diffs.ReplicationState

Current replication state from the OSM minutely diff feed.

#### CloudEvents Attributes

| **Name** | **Value** |
|----------|-----------|
| `type` | `Org.OpenStreetMap.Diffs.ReplicationState` |
| `source` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` | `replication_state` |

#### Fields

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `sequence_number` | int64 | Monotonically increasing sequence number of the latest processed diff |
| `timestamp` | datetime | UTC timestamp associated with the replication state |

---

## Message Group: Org.OpenStreetMap.Diffs

---

### Message: Org.OpenStreetMap.Diffs.MapChange

An individual element change from the OSM minutely replication diff feed.

#### CloudEvents Attributes

| **Name** | **Value** |
|----------|-----------|
| `type` | `Org.OpenStreetMap.Diffs.MapChange` |
| `source` | `https://planet.openstreetmap.org/replication/minute` |
| `subject` | `{element_type}/{element_id}` |

#### Fields

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `change_type` | string | Change type: create, modify, or delete |
| `element_type` | string | OSM element type: node, way, or relation |
| `element_id` | int64 | Unique OSM element identifier |
| `version` | int32 | Element version number |
| `timestamp` | datetime | UTC timestamp of the element version |
| `changeset_id` | int64 | OSM changeset identifier |
| `user_name` | string? | Display name of the editing user |
| `user_id` | int64? | Numeric user identifier |
| `latitude` | double? | WGS-84 latitude (nodes only) |
| `longitude` | double? | WGS-84 longitude (nodes only) |
| `tags` | string | JSON-encoded key-value tag pairs |
| `sequence_number` | int64 | Replication sequence number |

#### Example

```json
{
  "specversion": "1.0",
  "type": "Org.OpenStreetMap.Diffs.MapChange",
  "source": "https://planet.openstreetmap.org/replication/minute",
  "subject": "node/317968498",
  "data": {
    "change_type": "delete",
    "element_type": "node",
    "element_id": 317968498,
    "version": 5,
    "timestamp": "2026-04-09T01:32:40+00:00",
    "changeset_id": 181074839,
    "user_name": "inserteunnombreaqui",
    "user_id": 22579655,
    "latitude": 21.0495463,
    "longitude": 105.839612,
    "tags": "{}",
    "sequence_number": 7062480
  }
}
```
