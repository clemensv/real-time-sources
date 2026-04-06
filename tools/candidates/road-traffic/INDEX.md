# Road Traffic Candidates

Real-time road traffic data sources covering speed, flow, incidents, roadworks, and travel times. DATEX II is the dominant European standard for traffic data interchange — multiple countries publish in this format. The Autobahn API bridge already exists in this repository.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Digitraffic Road Finland](digitraffic-road-finland.md) | Finland | **18/18** | REST + MQTT | TMS data, incidents, road weather; MQTT for push updates; same platform as Maritime |
| [Trafikverket Sweden](trafikverket-sweden.md) | Sweden | **18/18** | REST (custom query) + DATEX II | Comprehensive traffic data; CC0 license; delta change tracking |
| [NDW Netherlands](ndw-netherlands.md) | Netherlands | **18/18** | DATEX II v3 files | Per-minute traffic speeds; DATEX II reference implementation |
| [Statens vegvesen Norway](vegvesen-norway.md) | Norway | 16/18 | GraphQL + REST | Traffic volumes via GraphQL; NVDB road database |
| [National Highways England](national-highways-england.md) | UK — England | 16/18 | REST | WebTRIS traffic counts and speeds; strategic road network |
| [Autobahn Germany](autobahn-germany.md) | Germany | 17/18 | REST | **Already implemented** in `autobahn/` directory |

## Recommended Approach

1. **Build a Digitraffic Road bridge first** — same platform architecture as Digitraffic Maritime (already in the project). MQTT support enables true real-time push updates. Reuse code patterns from the maritime bridge.

2. **Build a Trafikverket bridge** — the custom query API with `CHANGEDSINCECHANGEID` makes delta polling extremely efficient. CC0 license is maximally permissive. Rich data: traffic flow, incidents, road conditions, weather, travel times.

3. **Build an NDW DATEX II bridge** — this is the reference implementation for DATEX II v3 in Europe. Building a DATEX II traffic parser here means the same parser works for traffic data from many EU countries. Per-minute updates for traffic speed/flow.

4. **Statens vegvesen (Norway)** — interesting for the GraphQL API pattern but hourly aggregates are less fresh than other sources. Good complement for Norwegian coverage.

5. **National Highways (England)** — solid data but the query-by-date model is better suited for analytics than real-time streaming. WebTRIS is well-documented and easy to integrate.

6. **Autobahn (Germany)** — already implemented. No additional work needed.

## Coverage Summary

- **Nordic countries**: Finland (Digitraffic), Sweden (Trafikverket), Norway (vegvesen)
- **Western Europe**: Netherlands (NDW), Germany (Autobahn — done), UK (National Highways)
- **Key standard**: DATEX II v3 — used by NDW, Trafikverket, Digitraffic, and many other EU data publishers
- **Best protocol variety**: REST, MQTT (Digitraffic), GraphQL (vegvesen), custom query (Trafikverket), file download (NDW)
