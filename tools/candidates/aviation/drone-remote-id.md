# Drone Remote ID / UTM Data Sources (Investigation Report)

**Country/Region**: US (FAA), Europe (EASA), Global
**Publisher**: Various — FAA, EASA, drone manufacturers
**Protocol**: Bluetooth 4/5, WiFi Beacon/NAN (broadcast), Network Remote ID (internet)
**Auth**: Varies by implementation
**Data Format**: ASTM F3411 (Open Drone ID), EU delegated regulation 2019/945
**Update Frequency**: Real-time (broadcast every 1 second)
**License**: Regulatory framework — data is broadcast, reception is unrestricted

## What It Provides

Remote Identification (Remote ID) for drones is a regulatory mandate that requires unmanned
aircraft to broadcast identification and location information during flight. This creates a
new class of real-time position data similar to ADS-B but for drones.

**FAA Remote ID** (effective September 2023):
- Drone serial number or session ID
- Drone position (lat/lon/altitude)
- Drone velocity
- Control station position (Standard Remote ID) or takeoff location (Broadcast Module)
- Timestamp
- Emergency status

**EASA U-Space** (European drone traffic management):
- Network identification service
- Geo-awareness (geofencing data)
- Flight authorization
- Traffic information (drone-to-drone awareness)

## Current State of Data Accessibility

### What exists:

1. **Broadcast Remote ID (BLE/WiFi)**: Drones transmit via Bluetooth 4.0 LE Legacy Advertising,
   Bluetooth 5.0 Long Range, or WiFi Beacon/NAN. Anyone within radio range (~300m-1km) can
   receive these signals with appropriate hardware/software.

2. **Network Remote ID**: Drones report to a USS (UAS Service Supplier) via internet. The USS
   aggregates data and can provide it to authorized consumers.

3. **ASTM F3411 Open Drone ID**: The standard protocol for Remote ID messages. Open standard,
   well-documented.

### What's NOT yet accessible as a public API:

- No centralized public API for aggregated Remote ID data exists in the US or EU.
- FAA's FAADroneZone is a registration portal, not a tracking data feed.
- USS (UAS Service Suppliers) like DroneUp, Airbus UTM, Wing operate private APIs.
- DJI AeroScope is proprietary hardware/software for drone detection, not an open API.
- No public "OpenSky for drones" equivalent exists yet.

### Potential future sources:

- **FAA UAS Data Exchange**: The FAA is developing a UAS Data Exchange system. Not yet public.
- **EASA U-Space services**: EU member states are implementing U-Space, which will include
  network identification services. Netherlands, Switzerland, and Estonia are pilots.
- **Open Drone ID apps**: Android apps (OpenDroneID, DroneScanner) can receive broadcast
  Remote ID, but this is local reception only, not aggregated data.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time broadcast (1-second intervals) |
| Openness | 0 | No public aggregated API exists |
| Stability | 1 | Standards defined, but infrastructure still deploying |
| Structure | 2 | ASTM F3411 is well-specified, but no API to consume |
| Identifiers | 2 | Serial numbers, session IDs, operator IDs defined |
| Additive Value | 3 | Entirely new data domain — drone tracking |

**Total: 11/18 (potential), 2/18 (current accessibility)**

## Notes

- This is a forward-looking investigation. Remote ID is mandated and drones are broadcasting,
  but no centralized open data feed exists yet. It's a "when" not "if" question.
- For local drone detection, a Raspberry Pi with Bluetooth can receive ASTM F3411 Open Drone
  ID broadcasts. The `opendroneid` open-source project provides libraries for parsing.
- The broadcast protocol is intentionally open — anyone can receive it. The missing piece is
  aggregation and API access.
- DJI AeroScope hardware can detect DJI drones specifically (proprietary protocol), but this
  is a $10,000+ system aimed at airports and security, not a data API.
- Worth monitoring: the FAA's USS ecosystem and EASA's U-Space implementation are the most
  likely paths to aggregated public drone tracking data.
- The ASTM F3411 standard defines both Broadcast and Network Remote ID message formats.
  Network RID messages transit via internet to USS providers, creating the foundation for
  future API access.
