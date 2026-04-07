# Nextbus Bridge Events

This document describes the events emitted by the Nextbus Bridge.

- [Feed Events](#feed-events)
  - [nextbus.vehiclePosition](#message-nextbusvehicleposition)
- [Reference Events](#reference-events)
  - [nextbus.routeConfig](#message-nextbusrouteconfig)
  - [nextbus.schedule](#message-nextbusschedule)
  - [nextbus.messages](#message-nextbusmessages)

---

## Feed Events

Vehicle position events are emitted to the "feed" Event Hub on every polling
cycle (default: every 10 seconds). Only new or updated vehicle positions are
forwarded — the bridge tracks the last report time per vehicle and skips
duplicates.

**Event Hub**: Configured via `--feed-event-hub-name`
**Partition key**: `{agency_tag}`
**Envelope**: CloudEvents/1.0, structured JSON (`application/cloudevents+json`)

---

### Message: nextbus.vehiclePosition

A real-time vehicle position report for a transit vehicle.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `nextbus.vehiclePosition` |
| `source` | Data origin | URI | Yes | `https://retro.umoiq.com/service/publicXMLFeed` |
| `subject` | Vehicle identifier | string | Yes | `{agency_tag}/{vehicle_id}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |
| `time` | Timestamp of the report | datetime | Yes | ISO 8601 |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `agency` | string | Yes | Transit agency tag (e.g., `ttc`) |
| `routeTag` | string | Yes | Route identifier |
| `dirTag` | string | No | Direction tag |
| `id` | string | Yes | Vehicle identifier |
| `lat` | string | Yes | Vehicle latitude |
| `lon` | string | Yes | Vehicle longitude |
| `predictable` | string | No | Whether the vehicle position is predictable (`true`/`false`) |
| `heading` | string | Yes | Vehicle heading in degrees |
| `speedKmHr` | string | Yes | Vehicle speed in km/h |
| `timestamp` | double | Yes | Unix epoch timestamp of the report (seconds) |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "nextbus.vehiclePosition",
  "source": "https://retro.umoiq.com/service/publicXMLFeed",
  "subject": "ttc/4207",
  "id": "...",
  "datacontenttype": "application/json",
  "time": "2025-01-15T18:45:12",
  "data": {
    "agency": "ttc",
    "routeTag": "504",
    "dirTag": "504_0_504A",
    "id": "4207",
    "lat": "43.6438",
    "lon": "-79.3821",
    "predictable": "true",
    "heading": "175",
    "speedKmHr": "23",
    "timestamp": 1736967912.0
  }
}
```

---

## Reference Events

Reference data events are emitted to the "reference" Event Hub (when configured)
and refreshed every hour. These include route configurations, schedules, and
service messages. Only changed data is re-sent — the bridge checksums each
response and skips unchanged payloads.

**Event Hub**: Configured via `--reference-event-hub-name`
**Envelope**: CloudEvents/1.0, structured JSON (`application/cloudevents+json`)

---

### Message: nextbus.routeConfig

Complete route configuration including stops, paths, and directions.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `nextbus.routeConfig` |
| `source` | Data origin | URI | Yes | `https://retro.umoiq.com/service/publicXMLFeed` |
| `subject` | Route identifier | string | Yes | `{agency_tag}/{route_tag}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |
| `time` | Timestamp of emission | datetime | Yes | ISO 8601 |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `agency` | string | Yes | Transit agency tag |
| `routeTag` | string | Yes | Route identifier |
| `routeConfig` | string | Yes | JSON-encoded route configuration object (stops, paths, directions) |

**Partition key**: `route/{agency_tag}/{route_tag}`

#### Example:

```json
{
  "specversion": "1.0",
  "type": "nextbus.routeConfig",
  "source": "https://retro.umoiq.com/service/publicXMLFeed",
  "subject": "ttc/504",
  "id": "...",
  "datacontenttype": "application/json",
  "time": "2025-01-15T18:00:00+00:00",
  "data": {
    "agency": "ttc",
    "routeTag": "504",
    "routeConfig": "{\"route\":{\"tag\":\"504\",\"title\":\"504-King\",\"stop\":[...],\"direction\":[...],\"path\":[...]}}"
  }
}
```

---

### Message: nextbus.schedule

Route schedule data for a transit route.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `nextbus.schedule` |
| `source` | Data origin | URI | Yes | `https://retro.umoiq.com/service/publicXMLFeed` |
| `subject` | Route identifier | string | Yes | `{agency_tag}/{route_tag}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |
| `time` | Timestamp of emission | datetime | Yes | ISO 8601 |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `agency` | string | Yes | Transit agency tag |
| `routeTag` | string | Yes | Route identifier |
| `schedule` | string | Yes | JSON-encoded schedule object (timetable blocks, stop times) |

**Partition key**: `schedule/{agency_tag}/{route_tag}`

#### Example:

```json
{
  "specversion": "1.0",
  "type": "nextbus.schedule",
  "source": "https://retro.umoiq.com/service/publicXMLFeed",
  "subject": "ttc/504",
  "id": "...",
  "datacontenttype": "application/json",
  "time": "2025-01-15T18:00:00+00:00",
  "data": {
    "agency": "ttc",
    "routeTag": "504",
    "schedule": "{\"route\":{\"tag\":\"504\",\"title\":\"504-King\",\"scheduleClass\":\"CurrentSvc\",\"tr\":[...]}}"
  }
}
```

---

### Message: nextbus.messages

Service messages (alerts, detours, announcements) for a transit route.

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|----------|-----------------|----------|--------------|-----------|
| `type` | Event type | string | Yes | `nextbus.messages` |
| `source` | Data origin | URI | Yes | `https://retro.umoiq.com/service/publicXMLFeed` |
| `subject` | Route identifier | string | Yes | `{agency_tag}/{route_tag}` |
| `datacontenttype` | Content type | string | Yes | `application/json` |
| `time` | Timestamp of emission | datetime | Yes | ISO 8601 |

#### Data Schema:

| **Field** | **Type** | **Required** | **Description** |
|-----------|----------|--------------|-----------------|
| `agency` | string | Yes | Transit agency tag |
| `routeTag` | string | Yes | Route identifier |
| `messages` | string | Yes | JSON-encoded messages object (service alerts, detour notices) |

**Partition key**: `messages/{agency_tag}/{route_tag}`

#### Example:

```json
{
  "specversion": "1.0",
  "type": "nextbus.messages",
  "source": "https://retro.umoiq.com/service/publicXMLFeed",
  "subject": "ttc/504",
  "id": "...",
  "datacontenttype": "application/json",
  "time": "2025-01-15T18:00:00+00:00",
  "data": {
    "agency": "ttc",
    "routeTag": "504",
    "messages": "{\"route\":{\"tag\":\"504\",\"message\":[{\"text\":\"Diversion in effect due to construction.\"}]}}"
  }
}
```
