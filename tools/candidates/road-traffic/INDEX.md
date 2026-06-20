# Road Traffic Candidates

Real-time road traffic data sources covering speed, flow, incidents, roadworks, and travel times. DATEX II is the dominant European standard for traffic data interchange — multiple countries publish in this format. Commercial providers (TomTom, HERE) offer global coverage with free tiers. The Autobahn API bridge already exists in this repository.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Trafikverket Sweden](trafikverket-sweden.md) | Sweden | **18/18** | REST (custom query) + DATEX II | Comprehensive traffic data; CC0 license; delta change tracking |
| [Luxembourg CITA DATEX](luxembourg-cita-datex.md) | Luxembourg | **17/18** | DATEX II | Live motorway traffic status feeds; compact DATEX validation target |
| [Singapore LTA Traffic](singapore-lta-traffic.md) | **Singapore** | 17/18 | REST (OData) | Speed bands, incidents, images, travel times; comprehensive platform |
| [Hong Kong TD Traffic](hong-kong-td-traffic.md) | **Hong Kong** | 16/18 | REST (XML) | TD detector speed/volume/occupancy at **30-second** cadence; keyless |
| [Statens vegvesen Norway](vegvesen-norway.md) | Norway | 16/18 | GraphQL + REST | Traffic volumes via GraphQL; NVDB road database |
| [National Highways England](national-highways-england.md) | UK — England | 16/18 | REST | WebTRIS traffic counts and speeds; strategic road network |
| [511 SF Bay Area](511-sf-bay-area.md) | US — Bay Area | 16/18 | REST | Traffic events, work zones (WZDx), tolls; representative US 511 system |
| [TomTom Traffic](tomtom-traffic.md) | **Global** | 16/18 | REST | Flow + incidents; free tier 2,500 req/day; OpenLR references |
| [HERE Traffic](here-traffic.md) | **Global** | 15/18 | REST | Flow + incidents; free tier 1,000 req/month; jam factor metric |

## Recommended Approach

1. **Build a Digitraffic Road bridge first** — same platform architecture as Digitraffic Maritime (already in the project). MQTT support enables true real-time push updates. Reuse code patterns from the maritime bridge.

2. **Build a Trafikverket bridge** — the custom query API with `CHANGEDSINCECHANGEID` makes delta polling extremely efficient. CC0 license is maximally permissive. Rich data: traffic flow, incidents, road conditions, weather, travel times.

3. **Build an NDW DATEX II bridge** — this is the reference implementation for DATEX II v3 in Europe. Building a DATEX II traffic parser here means the same parser works for French DIR traffic data and other EU countries. Per-minute updates for traffic speed/flow.

4. **Build a TfL Road Disruptions bridge** — zero auth, rich GeoJSON geometry, real-time incidents and roadworks. Complements the existing TfL Santander Cycles candidate and TfL parking — a comprehensive TfL bridge serves three data categories from one platform.

5. **Build a Madrid Traffic bridge** — rare open real-time raw sensor data with no auth. Pre-computed service levels (free flow → severe congestion) and 5-minute updates. Only open traffic API found in Spain.

6. **Build a Singapore LTA traffic bridge** — one API key unlocks speed bands, incidents, images, travel times, VMS messages, and carpark availability. Comprehensive city-state coverage.

7. **Build a French Road Traffic bridge** — DATEX II format means the same parser built for NDW works here. Adds French national road network to the European traffic data coverage.

8. **WSDOT Traveler API** — rare US state platform combining ferries, traffic, passes, weather, and border crossings. Washington is especially valuable because Puget Sound ferry operations make the feed more than a generic DOT API.

9. **511 SF Bay Area** — representative US 511 system with WZDx work zone standard. Building WZDx support enables integration with other US state DOTs.

10. **TomTom / HERE** — commercial providers documented as reference. Free tiers useful for validation and gap-filling. Global coverage with OpenLR/TMC references enables cross-provider data fusion.

11. **Paris Bicycle Counters** — different traffic modality (cycling). Eco-Compteur pattern reusable for dozens of cities worldwide. J-1 daily freshness.

12. **Statens vegvesen (Norway)** — interesting for the GraphQL API pattern but hourly aggregates are less fresh than other sources.

13. **National Highways (England)** — solid data but the query-by-date model is better suited for analytics than real-time streaming.

14. **Autobahn (Germany)** — already implemented. No additional work needed.

## Sources Investigated but Not Viable

- **Google Traffic**: No public API for raw traffic flow/speed data (only routing APIs)
- **INRIX**: Commercial only, no free tier, enterprise licensing
- **Waze for Cities**: Government agencies only; data via BigQuery
- **Japan VICS**: Broadcast-only system (FM/infrared beacons to vehicles); no web API
- **Italy ANAS/Autostrade**: No public real-time API; historical accident statistics only
- **Spain DGT (national)**: Web map only (etraffic); no documented REST API
- **South Korea ITS**: API exists but Korean-only registration, connectivity issues
- **VicRoads (Australia)**: Web map only (VicTraffic); no public API
- **Main Roads WA**: No public API found

## Coverage Summary

- **Nordic countries**: Finland (Digitraffic), Sweden (Trafikverket), Norway (vegvesen)
- **Western Europe**: Netherlands (NDW), Germany (Autobahn — done), UK (TfL London + National Highways), France (DIR via DATEX II), Spain (Madrid)
- **Asia-Pacific**: Singapore (LTA DataMall — comprehensive)
- **Americas**: US (511 SF Bay Area, WSDOT Washington, Autobahn-style state DOTs)
- **Global commercial**: TomTom (2,500/day free), HERE (1,000/month free)
- **Cycling**: Paris (141 Eco-Compteur stations — reusable pattern for dozens of cities)
- **Key standard**: DATEX II v3 — used by NDW, Trafikverket, Digitraffic, French DIR, and many other EU data publishers
- **Best protocol variety**: REST, MQTT (Digitraffic), GraphQL (vegvesen), custom query (Trafikverket), file download (NDW), OData (Singapore), XML (Madrid)

### Asia & Middle East — Deep Dive Round 5

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Istanbul IBB Traffic](istanbul-ibb-traffic.md) | Turkey — Istanbul | **15/18** | CKAN REST | Confirmed CKAN API; traffic + transit datasets; 16M city |

**Key finding**: Istanbul's IBB data portal runs a standard CKAN API. Verified working with traffic and transit datasets. This is the first confirmed open data traffic API in the Middle East/Turkey region.

## Round 2026-05 — Gulf + Satellite EO sweep

Added in May 2026 by the Gulf (KW/AE/OM/SA/BH/QA/IQ) and satellite-EO (NASA/ESA/NOAA/EUMETSAT/JAXA/ISRO/KARI/CNSA/Other) research fleets.

| Candidate | File | Score | Verdict |
|---|---|---|---|
| RTA Dubai - Real-Time Traffic and Transport Data | [ae-rta-dubai-traffic.md](ae-rta-dubai-traffic.md) | ?/18 | — |
| Kuwait Roads and Traffic Management | [kw-kuwait-roads-traffic.md](kw-kuwait-roads-traffic.md) | ?/18 | ❌ |

## Round 2026-06 — Asia (SG / HK / TW) real-time sweep

Targeted verification of the three most mature Asian real-time ecosystems. SG and TW road traffic are already covered (Singapore LTA Traffic 17/18; Taiwan's road data sits in the TDX/transit notes), so the one **new** road-traffic gap surfaced was Hong Kong.

| Candidate | File | Score | Verdict |
|---|---|---|---|
| Hong Kong TD Traffic (detector speed/volume/occupancy) | [hong-kong-td-traffic.md](hong-kong-td-traffic.md) | 16/18 | **Build** — confirmed live at 30s, keyless; HK had weather/AQHI/transit but no road traffic |

Full sweep (implemented vs. noted vs. gaps across SG/HK/TW) recorded in [`_research-rounds/2026-06-asia-sg-hk-tw-realtime-sweep.md`](../_research-rounds/2026-06-asia-sg-hk-tw-realtime-sweep.md).

