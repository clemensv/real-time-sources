# Statens vegvesen (Norwegian Public Roads Administration)

**Country/Region**: Norway
**Publisher**: Statens vegvesen (Norwegian Public Roads Administration)
**API Endpoint**: `https://trafikkdata.atlas.vegvesen.no/` (Trafikkdata portal) and `https://nvdbapiles-v3.atlas.vegvesen.no/` (NVDB API)
**Documentation**: https://trafikkdata.atlas.vegvesen.no/ and https://nvdbapiles-v3.atlas.vegvesen.no/dokumentasjon/
**Protocol**: GraphQL (Trafikkdata) / REST (NVDB API)
**Auth**: None (Trafikkdata) / API key for some NVDB endpoints
**Data Format**: JSON (GraphQL responses) / JSON (REST)
**Update Frequency**: Hourly traffic counts (Trafikkdata); road network data periodically updated (NVDB)
**License**: Norwegian Licence for Open Government Data (NLOD)

## What It Provides

Statens vegvesen operates two complementary data platforms for Norwegian road traffic:

1. **Trafikkdata**: Traffic volume and speed data from 4,000+ measurement points across the Norwegian road network. Provides hourly, daily, monthly, and annual average traffic (ÅDT). Covers both car and bicycle traffic.

2. **NVDB (Nasjonal Vegdatabank)**: The national road database containing comprehensive road network data including road geometry, speed limits, tunnels, bridges, traffic signs, and more.

## API Details

**Trafikkdata GraphQL API:**
```graphql
POST https://trafikkdata-api.atlas.vegvesen.no/
{
  trafficRegistrationPoints(searchQuery: {roadCategoryIds: [E, R, F]}) {
    id
    name
    location {
      coordinates { latLon { lat lon } }
      municipality { name number }
      county { name number }
    }
    trafficRegistrationType
  }
}
```

Traffic data queries:
```graphql
{
  trafficData(trafficRegistrationPointId: "44656V72812") {
    volume {
      byHour(from: "2024-01-01T00:00:00+01:00", to: "2024-01-02T00:00:00+01:00") {
        edges {
          node {
            from
            to
            total { volumeNumbers { volume } }
            byDirection { ... }
          }
        }
      }
    }
  }
}
```

**NVDB REST API v3:**
```
GET https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekter/105?inkluder=egenskaper,lokasjon&srid=4326
```
Object type 105 = speed limits, 482 = traffic counts, etc.

## Freshness Assessment

Trafikkdata provides hourly aggregated traffic counts — data is available within 1–2 hours of the measurement period. This is not real-time per-vehicle data but rather hourly aggregates suitable for traffic analysis and trend monitoring. NVDB road network data is periodically updated as road conditions change. For real-time incident data, Norway's DATEX II feed (via vegvesen.no) provides immediate updates.

## Entity Model

- **Traffic Registration Point**: Measurement station with ID, name, location, type (volume/speed/class)
- **Traffic Volume**: Hourly/daily/monthly counts by direction and vehicle class
- **Road Object**: NVDB entities (speed limits, tunnels, bridges, signs) with geometry
- **Road Network**: Road segments with attributes and linear referencing
- **Municipality/County**: Administrative geography linked to measurement points

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly aggregates, not real-time per-vehicle |
| Openness | 3 | NLOD license, no auth for Trafikkdata GraphQL |
| Stability | 3 | Government-operated, versioned APIs |
| Structure | 3 | GraphQL (Trafikkdata) and REST (NVDB) — well-structured |
| Identifiers | 3 | Registration point IDs, NVDB object IDs, road references |
| Additive Value | 2 | Good Norwegian coverage; GraphQL is unusual and powerful for traffic data |
| **Total** | **16/18** | |

## Notes

- The GraphQL API for traffic data is notable — it allows precise queries for exactly the data needed, avoiding over-fetching. Few traffic data platforms offer GraphQL.
- Norway's road network includes many tunnels and ferries (fjord crossings) — the data reflects this unique geography.
- The NVDB API provides 400+ object types covering every aspect of road infrastructure. Object type 482 provides traffic counting station data cross-referenced with the Trafikkdata platform.
- For real-time incidents and roadworks, vegvesen.no also publishes DATEX II feeds (not fully explored here).
- The Trafikkdata portal at https://trafikkdata.atlas.vegvesen.no/ provides a web UI for exploring traffic data — useful for understanding the data model before building a bridge.
