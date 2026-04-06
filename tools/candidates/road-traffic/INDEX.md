# Road Traffic Candidates

Real-time road traffic data sources covering speed, flow, incidents, roadworks, and travel times. DATEX II is the dominant European standard for traffic data interchange — multiple countries publish in this format. Commercial providers (TomTom, HERE) offer global coverage with free tiers. The Autobahn API bridge already exists in this repository.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Digitraffic Road Finland](digitraffic-road-finland.md) | Finland | **18/18** | REST + MQTT | TMS data, incidents, road weather; MQTT for push updates; same platform as Maritime |
| [Trafikverket Sweden](trafikverket-sweden.md) | Sweden | **18/18** | REST (custom query) + DATEX II | Comprehensive traffic data; CC0 license; delta change tracking |
| [NDW Netherlands](ndw-netherlands.md) | Netherlands | **18/18** | DATEX II v3 files | Per-minute traffic speeds; DATEX II reference implementation |
| [TfL Road Disruptions London](tfl-road-disruptions-london.md) | UK — London | **18/18** | REST | Incidents, roadworks, closures with GeoJSON geometry; no auth |
| [French Road Traffic](french-road-traffic.md) | **France (national)** | **18/18** | DATEX II | Real-time circulation + events on national roads; DATEX II reuse |
| [Madrid Real-Time Traffic](madrid-traffic.md) | Spain — Madrid | 17/18 | REST (XML) | Raw sensor data: intensity, occupancy, service levels; 5-min updates |
| [Singapore LTA Traffic](singapore-lta-traffic.md) | **Singapore** | 17/18 | REST (OData) | Speed bands, incidents, images, travel times; comprehensive platform |
| [Paris Bicycle Counters](paris-bicycle-counters.md) | France — Paris | 17/18 | REST (Opendatasoft) | 141 Eco-Compteur stations; hourly bicycle flow data |
| [Autobahn Germany](autobahn-germany.md) | Germany | 17/18 | REST | **Already implemented** in `autobahn/` directory |
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

8. **511 SF Bay Area** — representative US 511 system with WZDx work zone standard. Building WZDx support enables integration with other US state DOTs.

9. **TomTom / HERE** — commercial providers documented as reference. Free tiers useful for validation and gap-filling. Global coverage with OpenLR/TMC references enables cross-provider data fusion.

10. **Paris Bicycle Counters** — different traffic modality (cycling). Eco-Compteur pattern reusable for dozens of cities worldwide. J-1 daily freshness.

11. **Statens vegvesen (Norway)** — interesting for the GraphQL API pattern but hourly aggregates are less fresh than other sources.

12. **National Highways (England)** — solid data but the query-by-date model is better suited for analytics than real-time streaming.

13. **Autobahn (Germany)** — already implemented. No additional work needed.

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
- **Americas**: US (511 SF Bay Area, Autobahn-style state DOTs)
- **Global commercial**: TomTom (2,500/day free), HERE (1,000/month free)
- **Cycling**: Paris (141 Eco-Compteur stations — reusable pattern for dozens of cities)
- **Key standard**: DATEX II v3 — used by NDW, Trafikverket, Digitraffic, French DIR, and many other EU data publishers
- **Best protocol variety**: REST, MQTT (Digitraffic), GraphQL (vegvesen), custom query (Trafikverket), file download (NDW), OData (Singapore), XML (Madrid)

### Asia & Middle East — Deep Dive Round 5

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Istanbul IBB Traffic](istanbul-ibb-traffic.md) | Turkey — Istanbul | **15/18** | CKAN REST | Confirmed CKAN API; traffic + transit datasets; 16M city |

**Key finding**: Istanbul's IBB data portal runs a standard CKAN API. Verified working with traffic and transit datasets. This is the first confirmed open data traffic API in the Middle East/Turkey region.
