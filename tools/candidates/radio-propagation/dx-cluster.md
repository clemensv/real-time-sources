# DX Cluster (Amateur Radio Spot Network)

**Country/Region**: Global
**Publisher**: Various (DX Spider, AR-Cluster, CC Cluster node operators)
**API Endpoint**: `telnet://dxc.ve7cc.net:23` (and many other nodes)
**Documentation**: https://www.dxcluster.info/, https://dxheat.com/, https://www.hamqth.com/dxc.php
**Protocol**: Telnet (legacy), WebSocket (modern aggregators), REST (aggregator APIs)
**Auth**: Callsign required for Telnet login (any valid amateur callsign)
**Data Format**: Plain text (Telnet), JSON (web aggregators)
**Update Frequency**: Real-time (spots appear within seconds)
**License**: Community data; free to use

## What It Provides

DX Cluster is a distributed network of interconnected servers that relay amateur radio "DX spots" — reports of interesting or distant radio contacts. When an amateur radio operator hears a distant station, they post a spot with the callsign, frequency, and a brief comment. These spots propagate across the global DX Cluster network within seconds, alerting other operators to active propagation paths.

The network has been running since the late 1980s, making it one of the oldest real-time crowd-sourced data networks in existence.

## API Details

- **Telnet access**: Connect to any DX Cluster node (e.g., `dxc.ve7cc.net:23`, `dxc.nc7j.com:7373`) with a callsign as login
- **Commands**: `DX {freq} {callsign} {comment}` (post spot), `SH/DX` (show recent), `SH/DX {callsign}` (filter)
- **Web aggregators** (easier integration):
  - DXHeat: `https://dxheat.com/dxc/` — web-based DX cluster with filtering
  - HamQTH: `https://www.hamqth.com/dxc_search.php` — searchable archive
  - DXWatch: `https://dxwatch.com/` — real-time map and spot feed
  - RBN (Reverse Beacon Network): `https://reversebeacon.net/` — automated CW/RTTY/FT8 spotting
- **Spot fields**: Timestamp, spotter callsign, spotted callsign, frequency (kHz), comment, band, mode (when detectable)
- **RBN API**: `https://reversebeacon.net/spots.php?format=json` — automated spots with SNR and speed
- **Filtering**: By band, mode, DXCC entity, spotter, time range (varies by aggregator)

## Freshness Assessment

DX Cluster spots propagate globally within seconds. The Telnet protocol provides a genuine real-time text stream of spots. Web aggregators add slight delay (1-10 seconds). The Reverse Beacon Network (RBN) is particularly interesting as it's fully automated — software-defined receivers decode CW, RTTY, and FT8 signals and post spots without human intervention.

## Entity Model

- **Spot**: Spotter callsign + spotted callsign + frequency + timestamp + comment
- **Station**: Amateur callsign with optional grid locator
- **DX Cluster Node**: Server in the distributed network (DX Spider, AR-Cluster, CC Cluster software)
- **Band/Mode**: Derived from frequency; mode from comment or automated detection

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time; seconds latency |
| Openness | 2 | Free but requires amateur callsign for Telnet; web aggregators are open |
| Stability | 3 | Running since late 1980s; highly distributed network |
| Structure | 1 | Telnet is unstructured text; aggregator APIs vary |
| Identifiers | 3 | Amateur callsigns are globally unique; frequencies are precise |
| Additive Value | 2 | Overlaps with PSKReporter/WSPR but adds human-curated spots and CW/SSB |
| **Total** | **14/18** | |

## Notes

- DX Cluster is the oldest of the radio propagation monitoring networks — predating the internet as we know it.
- The Reverse Beacon Network (RBN) is a modernized, automated version that's more suitable for machine consumption.
- Telnet protocol integration is unusual for modern systems but still widely used in amateur radio.
- Web aggregators (DXHeat, DXWatch) provide more accessible interfaces but may have rate limits or require attribution.
- The human-curated nature of spots adds qualitative information (comments like "loud signal", "QSL via bureau") not available from automated systems.
- For propagation analysis, PSKReporter and WSPRnet provide more systematic data; DX Cluster adds the human perspective.
