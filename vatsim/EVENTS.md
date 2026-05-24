# Table of Contents

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
*Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `net.vatsim.PilotPosition` |
| `source` |  | `` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

#### Schema:
##### Object: PilotPosition
*Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network. Updated every 15 seconds at the source.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `cid` | *int32* | - | `True` | VATSIM Certificate Identifier (CID) ù unique numeric member ID. |
| `callsign` | *string* | - | `True` | ATC-style callsign chosen by the pilot for this session (e.g. 'BAW123', 'N12345'). |
| `latitude` | *double* | degree (░) | `True` | Aircraft latitude in decimal degrees (WGS-84). Positive is north. |
| `longitude` | *double* | degree (░) | `True` | Aircraft longitude in decimal degrees (WGS-84). Positive is east. |
| `altitude` | *int32* | foot (ft) | `True` | Indicated altitude of the aircraft in feet above mean sea level. |
| `groundspeed` | *int32* | knot (kn) | `True` | Ground speed of the aircraft in knots. |
| `heading` | *int32* | degree (░) | `True` | Magnetic heading of the aircraft in degrees (0-359). |
| `transponder` | *string* | - | `True` | Four-digit transponder (squawk) code currently set by the pilot. |
| `qnh_mb` | *int32* | millibar (mb) | `True` | Altimeter setting (QNH) in millibars / hectopascals as reported by the pilot client. |
| `flight_rules` | *string* (optional) | - | `False` | Flight rules filed in the flight plan: 'I' for Instrument Flight Rules, 'V' for Visual Flight Rules. Null if no flight plan is filed. |
| `aircraft_short` | *string* (optional) | - | `False` | ICAO aircraft type designator from the filed flight plan (e.g. 'B738', 'A320'). Null if no flight plan is filed. |
| `departure` | *string* (optional) | - | `False` | ICAO code of the departure airport from the filed flight plan. Null if no flight plan is filed. |
| `arrival` | *string* (optional) | - | `False` | ICAO code of the arrival airport from the filed flight plan. Null if no flight plan is filed. |
| `route` | *string* (optional) | - | `False` | Route string from the filed flight plan. Null if no flight plan is filed. |
| `cruise_altitude` | *string* (optional) | - | `False` | Planned cruise altitude or flight level from the filed flight plan (e.g. '36000' or 'FL350'). Null if no flight plan is filed. |
| `pilot_rating` | *int32* | - | `True` | VATSIM pilot rating bitmask. 0 = New Member (P0), 1 = PPL, 3 = IR, 7 = CMEL, 15 = ATPL. |
| `last_updated` | *string* | - | `True` | UTC timestamp of the last position update received by the VATSIM data servers (RFC3339 string). |
## Message Group: net.vatsim.controllers
---
### Message: net.vatsim.ControllerPosition
*Current state and frequency of an air traffic controller connected to the VATSIM virtual aviation network.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `net.vatsim.ControllerPosition` |
| `source` |  | `` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

#### Schema:
##### Object: ControllerPosition
*Current state and frequency of an air traffic controller or observer connected to the VATSIM virtual aviation network.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `cid` | *int32* | - | `True` | VATSIM Certificate Identifier (CID) ù unique numeric member ID. |
| `callsign` | *string* | - | `True` | Controller position callsign (e.g. 'EGLL_TWR', 'KJFK_APP'). |
| `frequency` | *string* | - | `True` | Radio frequency the controller is operating on, in MHz with three decimal places (e.g. '118.500'). |
| `facility` | *int32* | - | `True` | VATSIM facility type code. 0 = Observer, 1 = Flight Service Station, 2 = Delivery, 3 = Ground, 4 = Tower, 5 = Approach/Departure, 6 = Center/Enroute. |
| `rating` | *int32* | - | `True` | VATSIM ATC rating. 1 = OBS, 2 = S1, 3 = S2, 4 = S3, 5 = C1, 6 = C2, 7 = C3, 8 = I1, 9 = I2, 10 = I3, 11 = SUP, 12 = ADM. |
| `text_atis` | *string* (optional) | - | `False` | Controller information or ATIS text, with individual lines joined by newline characters. Null when the controller has not set any ATIS text. |
| `last_updated` | *string* | - | `True` | UTC timestamp of the last update received by the VATSIM data servers (RFC3339 string). |
## Message Group: net.vatsim.status
---
### Message: net.vatsim.NetworkStatus
*Aggregate network status snapshot from the VATSIM data feed, emitted once per poll cycle.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `net.vatsim.NetworkStatus` |
| `source` |  | `` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

#### Schema:
##### Object: NetworkStatus
*Aggregate VATSIM network status snapshot emitted once per poll cycle, summarising connected client counts.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `callsign` | *string* | - | `True` | Constant key value 'status' used to identify this network status record. |
| `update_timestamp` | *string* | - | `True` | UTC timestamp of the VATSIM data snapshot as reported by the data feed (RFC3339 string). |
| `connected_clients` | *int32* | - | `True` | Total number of clients (pilots, controllers, observers) currently connected to the network. |
| `unique_users` | *int32* | - | `True` | Number of unique VATSIM user IDs currently connected. |
| `pilot_count` | *int32* | - | `True` | Number of pilots currently connected and flying. |
| `controller_count` | *int32* | - | `True` | Number of controllers (including observers) currently connected and providing ATC services. |

---

## Message Group: net.vatsim.mqtt

MQTT/5.0 transport variant for VATSIM live network data. Non-retained QoS-1 streams split pilots, controllers, and network facility status into distinct UNS topic branches under aviation-network/intl/vatsim/vatsim/...

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `aviation-network/intl/vatsim/vatsim/pilots/{callsign}/pilot-position` | `net.vatsim.PilotPosition` | `false` | `1` | `` |
| `aviation-network/intl/vatsim/vatsim/controllers/{callsign}/controller-position` | `net.vatsim.ControllerPosition` | `false` | `1` | `` |
| `aviation-network/intl/vatsim/vatsim/facilities/{facility}/facility-status` | `net.vatsim.NetworkStatus` | `false` | `1` | `` |
