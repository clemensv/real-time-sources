# VATSIM Live Data Feed Bridge Events

This document describes the events emitted by the VATSIM bridge.

- [net.vatsim.pilots](#message-group-netvatsimpilots)
  - [net.vatsim.PilotPosition](#message-netvatsimpilotposition)
- [net.vatsim.controllers](#message-group-netvatsimcontrollers)
  - [net.vatsim.ControllerPosition](#message-netvatsimcontrollerposition)
- [net.vatsim.status](#message-group-netvatsimstatus)
  - [net.vatsim.NetworkStatus](#message-netvatsimnetworkstatus)

---

## Message Group: net.vatsim.pilots

---

### Message: net.vatsim.PilotPosition

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `net.vatsim.PilotPosition` |
| `source` | Source Feed URL | `string` | `True` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` | Pilot callsign | `uritemplate` | `False` | `{callsign}` |

#### Schema: PilotPosition

*Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `cid` | *int32* | VATSIM Certificate Identifier (CID) — unique numeric member ID. |
| `callsign` | *string* | ATC-style callsign chosen by the pilot for this session. |
| `latitude` | *double* | Aircraft latitude in decimal degrees (WGS-84). |
| `longitude` | *double* | Aircraft longitude in decimal degrees (WGS-84). |
| `altitude` | *int32* | Indicated altitude in feet above mean sea level. |
| `groundspeed` | *int32* | Ground speed in knots. |
| `heading` | *int32* | Magnetic heading in degrees (0-359). |
| `transponder` | *string* | Four-digit transponder (squawk) code. |
| `qnh_mb` | *int32* | Altimeter setting (QNH) in millibars. |
| `flight_rules` | *string (nullable)* | Flight rules: I or V. Null if no flight plan. |
| `aircraft_short` | *string (nullable)* | ICAO aircraft type designator. Null if no flight plan. |
| `departure` | *string (nullable)* | ICAO departure airport code. Null if no flight plan. |
| `arrival` | *string (nullable)* | ICAO arrival airport code. Null if no flight plan. |
| `route` | *string (nullable)* | Route string from flight plan. Null if no flight plan. |
| `cruise_altitude` | *string (nullable)* | Planned cruise altitude. Null if no flight plan. |
| `pilot_rating` | *int32* | VATSIM pilot rating bitmask. |
| `last_updated` | *datetime* | UTC timestamp of last position update. |

---

## Message Group: net.vatsim.controllers

---

### Message: net.vatsim.ControllerPosition

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `net.vatsim.ControllerPosition` |
| `source` | Source Feed URL | `string` | `True` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` | Controller callsign | `uritemplate` | `False` | `{callsign}` |

#### Schema: ControllerPosition

*Current state and frequency of an air traffic controller connected to the VATSIM virtual aviation network.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `cid` | *int32* | VATSIM Certificate Identifier (CID). |
| `callsign` | *string* | Controller position callsign. |
| `frequency` | *string* | Radio frequency in MHz. |
| `facility` | *int32* | VATSIM facility type code. |
| `rating` | *int32* | VATSIM ATC rating. |
| `text_atis` | *string (nullable)* | Controller ATIS text, lines joined by newline. |
| `last_updated` | *datetime* | UTC timestamp of last update. |

---

## Message Group: net.vatsim.status

---

### Message: net.vatsim.NetworkStatus

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `net.vatsim.NetworkStatus` |
| `source` | Source Feed URL | `string` | `True` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` | Status key | `uritemplate` | `False` | `{callsign}` |

#### Schema: NetworkStatus

*Aggregate VATSIM network status snapshot emitted once per poll cycle.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `callsign` | *string* | Constant key value 'status'. |
| `update_timestamp` | *datetime* | UTC timestamp of the VATSIM data snapshot. |
| `connected_clients` | *int32* | Total connected clients. |
| `unique_users` | *int32* | Unique connected user IDs. |
| `pilot_count` | *int32* | Number of pilots currently flying. |
| `controller_count` | *int32* | Number of controllers connected. |
