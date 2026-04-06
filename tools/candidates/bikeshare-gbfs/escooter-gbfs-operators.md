# E-Scooter / Micromobility GBFS Operators

**Region**: Global (Europe-focused)
**Publishers**: Dott, Bird, Lime, Bolt, Voi
**Protocol**: GBFS 2.2–3.0
**Auth**: None
**Data Format**: JSON (GBFS)
**Update Frequency**: Real-time
**License**: Varies by operator

## What It Provides

Five major e-scooter/micromobility operators publish GBFS feeds for their fleets across hundreds of cities. These feeds provide real-time vehicle locations, battery levels, and availability — using the same GBFS standard as bikeshare systems. Combined, they represent over 500 city-level feeds in the MobilityData catalog.

## Operator Summary

| Operator | Catalog Entries | GBFS Version | URL Pattern | Auth |
|----------|----------------|--------------|-------------|------|
| **Dott** | ~339 cities | 2.3 | `https://gbfs.api.ridedott.com/public/v2/{city}/gbfs.json` | None |
| **Bird** | ~124 cities | 2.3 | `https://mds.bird.co/gbfs/v2/public/{city}/gbfs.json` | None |
| **Lime** | ~45 cities | 2.2 | `https://data.lime.bike/api/partners/v2/gbfs/{city}/gbfs.json` | None |
| **Bolt** | ~18 cities | 3.0 | `https://mds.bolt.eu/gbfs/3/{id}/gbfs` | None |
| **Voi** | ~15 cities | 2.3 / 3.0 | `https://api.voiapp.io/gbfs/{country}/{uuid}/v2/{id}/gbfs.json` | None* |

*Voi's generic endpoint returns 401 — city-specific URLs from the GBFS catalog are required.

**TIER is notably absent** — despite being a major operator (and nextbike's parent company), TIER has zero entries in the MobilityData GBFS catalog. Their `tier-services.io` GBFS endpoints are unreachable.

## Verified Working Endpoints

```
# Dott
https://gbfs.api.ridedott.com/public/v2/paris/gbfs.json        ✅
https://gbfs.api.ridedott.com/public/v2/london/gbfs.json       ✅
https://gbfs.api.ridedott.com/public/v2/brussels/gbfs.json     ✅

# Bird
https://mds.bird.co/gbfs/v2/public/helsinki/gbfs.json          ✅
https://mds.bird.co/gbfs/v2/public/paris/gbfs.json             ✅

# Lime
https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json    ✅
https://data.lime.bike/api/partners/v2/gbfs/berlin/gbfs.json   ✅

# Bolt
https://mds.bolt.eu/gbfs/3/336/gbfs                            ✅ (Brussels, v3.0)

# Voi (via Entur aggregator — Norway)
https://api.entur.io/mobility/v2/gbfs/v3/voioslo/gbfs          ✅ (v3.0)
```

## Key GBFS Feeds

E-scooter GBFS feeds typically include:
- `free_bike_status` — Real-time location and battery level of each available vehicle
- `vehicle_types` — Scooter/bike classifications
- `geofencing_zones` — Operating boundaries, no-ride zones, slow zones, parking zones
- `system_pricing_plans` — Per-minute pricing

Unlike station-based bikeshare, e-scooters are **free-floating** — the `free_bike_status` feed is the primary data source, providing individual vehicle coordinates and battery percentages.

## Freshness Assessment

E-scooter GBFS feeds update frequently (30–60 second TTL). Vehicle locations change continuously as riders pick up and drop off scooters. Battery levels update as vehicles are used and recharged. Geofencing zones are relatively static but can change with city regulations.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, 30–60s TTL |
| Openness | 3 | No auth, publicly accessible |
| Stability | 2 | Commercial operators may change endpoints without notice |
| Structure | 3 | Standard GBFS schema |
| Identifiers | 3 | Vehicle IDs, operator system IDs |
| Additive Value | 3 | 500+ city feeds; complements station-based bikeshare with free-floating micromobility |
| **Total** | **17/18** | |

## Notes

- All five operators are in the MobilityData GBFS catalog. A generic GBFS bridge handles them alongside bikeshare systems.
- The volume is significant — Dott alone has 339 city feeds. A GBFS bridge that consumes the catalog automatically gets all of these.
- Geofencing zones are particularly valuable — they encode city-specific regulations (no-ride zones, speed limits, parking requirements) in a machine-readable format.
- E-scooter data is more volatile than station-based bikeshare — vehicles move constantly, new vehicles are deployed, and fleet sizes change with demand.
- TIER's absence from the GBFS catalog is notable since they own nextbike. Their GBFS infrastructure may be in transition.
- Bolt is already publishing GBFS 3.0 — the newest version of the standard.
