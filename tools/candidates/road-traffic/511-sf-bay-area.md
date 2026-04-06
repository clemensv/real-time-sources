# 511 SF Bay Area

**Country/Region**: US — San Francisco Bay Area (California)
**Publisher**: Metropolitan Transportation Commission (MTC)
**API Endpoint**: `http://api.511.org/traffic/events?api_key={key}`
**Documentation**: https://511.org/open-data/traffic
**Protocol**: REST
**Auth**: API key required (free, request at 511.org/open-data/token)
**Data Format**: JSON
**Update Frequency**: Real-time
**License**: Open data

## What It Provides

511.org is the San Francisco Bay Area's official traveler information system, operated by MTC. The open data API provides real-time traffic events (incidents, closures), work zone data in WZDx (Work Zone Data Exchange) format, and toll/express lane pricing. It serves as a representative example of the US 511 system model used across many states — though each state runs its own 511 independently.

## API Details

**Traffic events (incidents, closures):**
```
GET http://api.511.org/traffic/events?api_key={key}
```

**Work zones (WZDx standard):**
```
GET http://api.511.org/traffic/wzdx?api_key={key}
```

**Toll programs and pricing:**
```
GET http://api.511.org/toll/programs?api_key={key}
```

Rate limit: 60 requests per hour (default).

The API returns confirmed-working 401 responses without a key, confirming the endpoint is live and active.

## Freshness Assessment

Traffic events update in real-time as incidents occur. Work zone data updates as construction schedules change. Toll pricing reflects current express lane rates. The system is actively maintained by MTC as the Bay Area's primary traffic information platform.

## Entity Model

- **Traffic Event**: Incident with type, location, severity, description
- **Work Zone**: Construction zone with geometry, schedule, lane impacts (WZDx standard)
- **Toll Program**: Express lane pricing with current rates

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time traffic events |
| Openness | 2 | Free API key required (easy registration) |
| Stability | 3 | Government-operated (MTC), well-established |
| Structure | 3 | JSON, WZDx standard for work zones |
| Identifiers | 3 | Event IDs, road references |
| Additive Value | 2 | Bay Area coverage; representative of US 511 model |
| **Total** | **16/18** | |

## Notes

- 511.org is one example of the US 511 system model. Each state/region operates independently — there is no single national 511 API. Key systems include 511NY (New York), FL511 (Florida), and various state DOTs.
- The WZDx (Work Zone Data Exchange) format is a US federal standard for construction zone data. Supporting WZDx here could enable integration with other state DOTs publishing the same format.
- California also offers Caltrans PeMS (Performance Measurement System) with 39,000+ freeway detectors — but PeMS requires account approval and is more of a data warehouse than a real-time API.
- API key registration is straightforward and free.
- Rate limits (60/hour) are modest — suitable for periodic polling, not high-frequency streaming.
