# ADSBHub Community ADS-B Feed

**Country/Region**: Global (community receiver network)
**Publisher**: ADSBHub (community project)
**API Endpoint**: `data.adsbhub.org:5002` (TCP)
**Documentation**: https://www.adsbhub.org/howtogetdata.php
**Protocol**: TCP streaming (SBS/BaseStation format, port 30003 compatible)
**Auth**: IP whitelist (must contribute an ADS-B station to receive data)
**Data Format**: SBS/BaseStation text (comma-delimited lines)
**Update Frequency**: Real-time (continuous stream)
**License**: Unrestricted use — commercial and non-commercial both permitted

## What It Provides

ADSBHub is a community-driven ADS-B data aggregation network where members share their local
ADS-B receiver output and in return receive the aggregated feed from all other members. The
model is reciprocal: you contribute data, you get data.

The aggregated feed provides:
- Real-time aircraft positions (latitude, longitude, altitude)
- Aircraft identification (ICAO24 hex, callsign, registration)
- Speed, track, vertical rate
- Squawk codes
- On-ground status

Coverage depends on the number and location of active feeders. The network has global reach
but with variable density — strongest over Europe and North America where most hobbyist
receivers are located.

## API Details

**Data access**: TCP connection to `data.adsbhub.org` port `5002`.

The port is only opened for IP addresses registered in your ADSBHub profile. You can
register up to 4 IP addresses.

**Data format**: SBS/BaseStation (port 30003) format — a de facto standard in the ADS-B
hobbyist community. Each line is a comma-separated record:

```
MSG,3,1,1,A1B2C3,1,2026/04/06,11:00:00.000,2026/04/06,11:00:00.000,,38000,,,51.5,-0.1,,,,,,0
MSG,1,1,1,A1B2C3,1,2026/04/06,11:00:01.000,2026/04/06,11:00:01.000,BAW123,,,,,,,,,,,
MSG,4,1,1,A1B2C3,1,2026/04/06,11:00:02.000,2026/04/06,11:00:02.000,,,450,,180,,,,,,,0
```

SBS message types:
- MSG,1 — ES Identification and Category (callsign)
- MSG,2 — ES Surface Position
- MSG,3 — ES Airborne Position (lat, lon, altitude)
- MSG,4 — ES Airborne Velocity (speed, track, vertical rate)
- MSG,5 — Surveillance Altitude
- MSG,6 — Surveillance Squawk
- MSG,7 — Air-to-Air
- MSG,8 — All-Call Reply

**Feeding requirements**:
- Must operate at least one ADS-B receiving station
- Station connects to `data.adsbhub.org:5001` (feeding port)
- Supports Raw Beast hex format, SBS, or Compressed VRS protocols
- Station can act as TCP client (connects to ADSBHub) or server (ADSBHub connects to you)
- Compatible with dump1090, readsb, PiAware, Virtual Radar Server

**Registration**: Free at https://www.adsbhub.org/register.php

## Freshness Assessment

Real-time. The TCP feed is a continuous stream of SBS messages as they are received from
all contributing stations. Latency depends on the feeder network but is typically sub-second
for the data path from receiver to aggregated feed.

Could not directly verify (TCP connection requires registered IP and active feeder station),
but the SBS protocol and infrastructure are well-established.

## Entity Model

SBS/BaseStation format — positional fields:
- ICAO24 hex address (field 5)
- Callsign (MSG type 1)
- Latitude, Longitude (MSG type 3)
- Altitude (MSG types 2, 3, 5)
- Groundspeed, Track, Vertical Rate (MSG type 4)
- Squawk code (MSG type 6)
- On-ground flag

Identifiers: ICAO24 hex address (primary), callsign.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time continuous TCP stream |
| Openness | 1 | Free but requires contributing your own ADS-B station |
| Stability | 2 | Community project, single operator |
| Structure | 2 | SBS text format is well-known but not JSON/modern |
| Identifiers | 2 | ICAO24 hex, callsign — no registration/type enrichment |
| Additive Value | 2 | Alternative to ADS-B Exchange with unrestricted use policy |

**Total: 12/18**

## Notes

- The reciprocal sharing model is both the strength and limitation — you must operate
  ADS-B receiving hardware to participate. A Raspberry Pi with an RTL-SDR dongle (~$30
  total) is sufficient.
- Key advantage over ADS-B Exchange: "There are no restrictions on how the users will use
  the data. Everybody is allowed to publish the data for free or to use it for commercial
  purposes." This is explicitly more permissive than ADS-B Exchange's commercial terms.
- The SBS/BaseStation format is natively compatible with Virtual Radar Server, PlanePlotter,
  and many other ADS-B tracking applications. Parsing is trivial (CSV lines).
- Not suitable for projects that can't operate an ADS-B receiver, but an excellent choice
  for those that can.
- Similar model to AISHub in the maritime domain — reciprocal sharing communities serve a
  niche but dedicated user base.
- The TCP protocol means this is inherently a streaming source — no REST polling, no
  request/reply. Integration requires a persistent TCP connection.
