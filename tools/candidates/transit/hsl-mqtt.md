# HSL MQTT — Helsinki Real-Time Vehicle Positions (High-Frequency Push)

**Country/Region**: Finland (Helsinki Region)
**Publisher**: HSL (Helsinki Region Transport)
**API Endpoint**: `mqtt.hsl.fi` (MQTT broker, port 8883/TLS or 443/WSS)
**Documentation**: https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/
**Protocol**: MQTT 3.1.1 (publish/subscribe messaging)
**Auth**: None — anonymous connections allowed
**Data Format**: JSON payloads on MQTT topics
**Update Frequency**: Real-time — vehicle positions at ~1 second intervals
**License**: Open data (HSL open data license)

## What It Provides

HSL publishes a high-frequency MQTT stream of vehicle positions for every bus, tram, metro train, commuter train, and ferry in the Helsinki region. This is one of the highest-frequency open transit data streams in the world:

- **Buses**: ~1,400 vehicles, positions at ~1 Hz
- **Trams**: ~100 vehicles
- **Metro**: trains on both lines (M1, M2)
- **Commuter trains**: ~200 vehicles (VR-operated)
- **Ferries**: Suomenlinna ferry and others

## API Details

### MQTT Connection

```
Host: mqtt.hsl.fi
Port: 8883 (MQTT over TLS) or 443 (WebSocket over TLS)
Protocol: MQTT 3.1.1
Auth: anonymous (no credentials needed)
```

### Topic Structure

Topics follow a hierarchical structure:
```
/hfp/v2/journey/ongoing/vp/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{lat}/{lon}
```

- Transport modes: `bus`, `tram`, `train`, `subway`, `ferry`
- Wildcards: subscribe to `/hfp/v2/journey/ongoing/vp/tram/#` for all trams
- Geohash filtering: subscribe to topics with specific lat/lon prefixes for geographic filtering

### Message Payload (JSON)

```json
{
  "VP": {
    "desi": "7",
    "dir": "1",
    "oper": 22,
    "veh": 814,
    "tst": "2024-01-15T12:34:56.789Z",
    "tsi": 1705319696,
    "spd": 12.5,
    "hdg": 180,
    "lat": 60.1699,
    "long": 24.9384,
    "acc": 0.5,
    "dl": -15,
    "odo": 12345,
    "drst": 0,
    "oday": "2024-01-15",
    "jrn": 123,
    "line": 456,
    "start": "12:30",
    "stop": 1234,
    "route": "1007",
    "occu": 0
  }
}
```

Fields: designation (`desi`), direction, operator, vehicle, timestamp, speed, heading, lat/lon, acceleration, delay (seconds), odometer, door status, occupancy.

## Freshness Assessment

Outstanding. This is raw, unfiltered vehicle telemetry at ~1 Hz — as fresh as transit data gets. Every vehicle reports its position roughly once per second. The MQTT broker handles thousands of concurrent connections. Data includes not just position but speed, heading, acceleration, door status, delay, and occupancy — a remarkably rich telemetry stream.

## Entity Model

- **VehiclePosition (VP)**: desi (route designation), dir (direction), oper (operator ID), veh (vehicle number), lat/lon, spd (speed m/s), hdg (heading degrees), acc (acceleration m/s²), dl (delay seconds, negative=early), odo (odometer meters), drst (door status 0/1), occu (occupancy 0-100), stop (next stop ID), route, jrn (journey ID)
- Topic metadata encodes transport mode, operator, vehicle, route, direction, headsign, start time, next stop, and geographic position
- IDs reference HSL's GTFS system

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | ~1 Hz vehicle telemetry — as real-time as it gets            |
| Openness        | 3     | Anonymous MQTT — no auth, no registration, no rate limits     |
| Stability       | 3     | Running for years; core HSL infrastructure                    |
| Structure       | 3     | Clean MQTT topics + JSON; well-documented topic hierarchy     |
| Identifiers     | 3     | GTFS-compatible, HSL-prefixed IDs                             |
| Additive Value  | 3     | MQTT is new protocol territory — push-based, high-frequency   |
| **Total**       | **18/18** |                                                           |

## Notes

- This is a dream source for a CloudEvents bridge. MQTT is natively event-driven — messages arrive as they're published, no polling needed. An MQTT-to-CloudEvents bridge would be architecturally elegant.
- The topic hierarchy enables sophisticated filtering: subscribe to just trams, just a specific route, just vehicles in a geographic area — all through MQTT topic wildcards.
- At ~1 Hz for ~1,700 vehicles, this stream produces roughly 100,000 messages per minute — a substantial but manageable volume for a bridge.
- The door status field (`drst`) tells you when a vehicle opens/closes its doors — enabling dwell-time analysis.
- The delay field (`dl`) gives real-time delay in seconds — negative values mean the vehicle is running early.
- HSL also publishes the same data via GTFS-RT and the Digitransit GraphQL API, but the MQTT stream is the highest-fidelity source with the lowest latency.
- WebSocket access (port 443) makes this accessible from web browsers — useful for prototyping.
