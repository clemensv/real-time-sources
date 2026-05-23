# Iraq Ports (Umm Qasr, Khor Al-Zubair) - AIS Vessel Tracking

- **Country/Region**: Iraq (southern ports on Persian Gulf)
- **Endpoint**: No dedicated Iraq port authority API discovered
- **Protocol**: N/A (commercial AIS aggregators only)
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: N/A
- **Docs**: None
- **Score**: 0/18

## Overview

Iraq has three major ports on the Persian Gulf (Basra region):
- **Umm Qasr** — largest port, container and bulk cargo, near Kuwait border
- **Khor Al-Zubair** — second-largest, general cargo and ro-ro
- **Al-Faw Grand Port** — under construction (mega-project, not yet operational as of 2025)

These ports are critical for Iraq's economy:
- 90%+ of Iraq's imports arrive via Umm Qasr (food, medicine, consumer goods)
- Oil exports flow via offshore terminals (not the commercial ports)
- Ports are managed by General Company for Ports of Iraq (GCPI)

AIS (Automatic Identification System) vessel tracking would show:
- Vessels calling at Umm Qasr and Khor Al-Zubair
- Queue/congestion at ports
- Estimated arrival times
- Vessel types (container, bulk, tanker)

## Endpoint Analysis

**No public port authority AIS API found** — searched for:
- GCPI website (`gcpi.iq`, `ports.gov.iq`) — no accessible site found
- Ministry of Transport AIS feed — no endpoint
- Commercial AIS aggregators (MarineTraffic, VesselFinder, FleetMon) block automated access and require paid subscriptions

Checked for open AIS sources:
- **AISHub** (community AIS network) — no Iraq coastal receivers registered
- **AISSstream** (WebSocket AIS feed) — covers Iraq Persian Gulf area in theory (global terrestrial AIS coverage), but currently broken in repo
- **Norway Kystverket** / **Finland Digitraffic** — only cover their national waters, not Iraq

## Alternative Coverage

Iraq port AIS could potentially be accessed via:

1. **AISstream (when fixed)** — global terrestrial AIS WebSocket, should cover Iraq if coastal receivers are active in Kuwait/Iran/UAE
2. **Satellite AIS** — companies like Spire, Orbcomm, exactEarth provide satellite-based global AIS, but all are commercial (paid APIs)
3. **Regional port APIs** — checked if Kuwait or Iran publish AIS for their waters (which might include Iraq ports at edge of coverage), but no public API found
4. **Commercial aggregators** — MarineTraffic/VesselFinder have Iraq coverage but require paid subscriptions

**No free, open, real-time AIS source exists for Iraq ports.**

## Iraq Port Traffic Significance

- Umm Qasr is a **critical chokepoint** for Iraq's economy (almost all imports)
- Port congestion and delays are newsworthy (affect commodity prices, food availability)
- Vessel arrival data could track sanctions compliance (which countries' ships call at Iraq)

This would be **high-value data if it existed in accessible form**, but it does not.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No accessible source |
| Openness | 0 | Commercial APIs only |
| Stability | 0 | N/A |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A (though MMSI would be standard if AIS existed) |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — Iraq ports are economically critical but no free/open real-time AIS source exists. GCPI does not publish AIS. Commercial aggregators (MarineTraffic, etc.) have Iraq coverage but require paid subscriptions. **AISstream (already in repo but currently broken)** is the most promising path — if/when it is fixed, it should provide Iraq Persian Gulf AIS coverage via global terrestrial receiver network. For now, no implementation is possible without paid commercial data.
