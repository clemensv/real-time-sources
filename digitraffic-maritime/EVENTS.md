# Digitraffic Marine AIS Bridge Events

This document describes the events emitted by the Digitraffic Marine AIS bridge.

- [fi.digitraffic.marine.ais](#message-group-fidigitrafficmarineais)
  - [fi.digitraffic.marine.ais.VesselLocation](#message-fidigitrafficmarineaisvessellocation)
  - [fi.digitraffic.marine.ais.VesselMetadata](#message-fidigitrafficmarineaisvestselmetadata)

---

## Message Group: fi.digitraffic.marine.ais

All events share these common CloudEvents attributes:

| **Name** | **Value** |
|----------|-----------|
| `source` | `wss://meri.digitraffic.fi/mqtt` |

The `type` attribute is set to the fully qualified message name.

---

### Message: fi.digitraffic.marine.ais.VesselLocation

AIS vessel position report. Published whenever a vessel broadcasts its
position via AIS (message types 1, 2, 3, 18, 19). The MMSI is extracted
from the MQTT topic and used as the Kafka partition key.

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `fi.digitraffic.marine.ais.VesselLocation` |
| `source` | `wss://meri.digitraffic.fi/mqtt` |

#### Fields:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `mmsi` | integer | Maritime Mobile Service Identity |
| `time` | integer | AIS timestamp (epoch seconds) |
| `sog` | number | Speed over ground (knots) |
| `cog` | number | Course over ground (degrees) |
| `navStat` | integer | Navigational status (0=under way, 1=at anchor, etc.) |
| `rot` | integer | Rate of turn (degrees/min, -128=not available) |
| `posAcc` | boolean | Position accuracy (true=DGPS < 10m) |
| `raim` | boolean | RAIM flag |
| `heading` | integer | True heading (degrees, 511=not available) |
| `lon` | number | Longitude (decimal degrees, WGS-84) |
| `lat` | number | Latitude (decimal degrees, WGS-84) |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "fi.digitraffic.marine.ais.VesselLocation",
  "source": "wss://meri.digitraffic.fi/mqtt",
  "id": "...",
  "time": "2026-04-02T13:37:17Z",
  "datacontenttype": "application/json",
  "data": {
    "mmsi": 230629000,
    "time": 1775137137,
    "sog": 10.7,
    "cog": 326.6,
    "navStat": 0,
    "rot": 0,
    "posAcc": true,
    "raim": false,
    "heading": 325,
    "lon": 20.345818,
    "lat": 60.03802
  }
}
```

---

### Message: fi.digitraffic.marine.ais.VesselMetadata

AIS vessel static and voyage data. Published when vessel metadata is
updated (AIS message types 5 and 24). Contains vessel name, dimensions,
destination, and other static information.

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `fi.digitraffic.marine.ais.VesselMetadata` |
| `source` | `wss://meri.digitraffic.fi/mqtt` |

#### Fields:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `mmsi` | integer | Maritime Mobile Service Identity |
| `timestamp` | integer | Metadata update timestamp (epoch milliseconds) |
| `name` | string | Vessel name (up to 20 chars) |
| `callSign` | string | Radio callsign (up to 7 chars) |
| `imo` | integer | IMO ship identification number |
| `type` | integer | Ship and cargo type code (0-99) |
| `draught` | integer | Maximum static draught (1/10 m) |
| `eta` | integer | Estimated time of arrival (encoded MMDDHHMM) |
| `destination` | string | Destination port (up to 20 chars) |
| `posType` | integer | Position fixing device type |
| `refA` | integer | Distance from bow (meters) |
| `refB` | integer | Distance from stern (meters) |
| `refC` | integer | Distance from port side (meters) |
| `refD` | integer | Distance from starboard (meters) |

#### Example:

```json
{
  "specversion": "1.0",
  "type": "fi.digitraffic.marine.ais.VesselMetadata",
  "source": "wss://meri.digitraffic.fi/mqtt",
  "id": "...",
  "time": "2026-04-02T13:37:06Z",
  "datacontenttype": "application/json",
  "data": {
    "mmsi": 538007963,
    "timestamp": 1668075026035,
    "destination": "UST LUGA",
    "name": "ARUNA CIHAN",
    "draught": 68,
    "eta": 733376,
    "posType": 15,
    "refA": 160,
    "refB": 33,
    "refC": 20,
    "refD": 12,
    "callSign": "V7WW7",
    "imo": 9543756,
    "type": 70
  }
}
```
