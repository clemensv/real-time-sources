# supercharge.info — Tesla Supercharger Database

**Country/Region**: Global (all Tesla Supercharger locations worldwide)
**Publisher**: supercharge.info community
**API Endpoint**: `https://supercharge.info/service/supercharge/allSites`
**Documentation**: https://supercharge.info/ (community project)
**Protocol**: REST
**Auth**: None (public endpoint)
**Data Format**: JSON
**Real-Time Status**: No — tracks construction status (Open/Construction/Plan/Closed), not real-time stall availability
**Update Frequency**: Community-maintained, updated as sites open/change
**Station Count**: 7,000+ Tesla Supercharger sites globally
**License**: Community data, CC BY-SA 4.0 for plug icons; data usage terms not explicitly stated

## What It Provides

supercharge.info is a long-running community project that tracks every Tesla Supercharger location worldwide. The `/allSites` endpoint returns a comprehensive JSON array of all Supercharger sites with detailed information including location, stall count, power level, plug types (TPC, NACS, CCS1, CCS2, GB/T), construction status, opening dates, and whether the site is open to non-Tesla EVs.

## API Details

**All Sites:**
```
GET https://supercharge.info/service/supercharge/allSites
```

No authentication required. Returns a JSON array where each site includes:
- `id` — unique numeric ID
- `locationId` — slug-style location identifier
- `name` — human-readable site name
- `status` — OPEN, CONSTRUCTION, PLAN, CLOSED, EXPANDING
- `address` — street, city, state, zip, country, region
- `gps` — latitude, longitude
- `dateOpened` — opening date
- `stallCount` — number of charging stalls
- `powerKilowatt` — max power (125, 150, 250, 325 kW)
- `solarCanopy` — solar canopy present
- `battery` — on-site battery storage
- `otherEVs` — whether non-Tesla EVs can charge (NACS/CCS availability)
- `stalls` — breakdown by version (v2, v3, v4, accessible, trailerFriendly)
- `plugs` — breakdown by plug type (tpc, nacs, ccs1, ccs2, gbt, type2, multi)
- `parkingId` — parking type
- `facilityName` — host business name
- `facilityHours` — operating hours
- `plugshareId` — cross-reference to PlugShare
- `osmId` — cross-reference to OpenStreetMap

**Example record (Ashburn, VA):**
```json
{
  "id": 2204,
  "name": "Ashburn, VA",
  "status": "OPEN",
  "gps": {"latitude": 39.008355, "longitude": -77.501839},
  "stallCount": 8,
  "powerKilowatt": 250,
  "otherEVs": true,
  "stalls": {"v3": 8},
  "plugs": {"tpc": 0, "nacs": 8},
  "facilityName": "Harris Teeter"
}
```

The response also includes sites globally — USA, Canada, Europe, China, Asia Pacific, with country and region metadata.

**Atom feed for updates:**
```
GET https://supercharge.info/service/supercharge/feed/atom.xml
```

## Freshness Assessment

supercharge.info tracks Supercharger infrastructure status (open, under construction, planned, closed) — it does not provide real-time stall availability (whether a specific stall is currently occupied). The data is updated by community contributors who monitor Tesla's announcements, construction permits, and on-site observations.

For tracking the Tesla Supercharger network buildout: excellent. For real-time availability: not available here. Tesla's own API provides stall-level availability but is not publicly documented.

## Entity Model

- **Site**: A Supercharger location with address, GPS, status
- **Stalls**: Count and version breakdown (V2 = 150kW, V3 = 250kW, V4 = 325kW+)
- **Plugs**: Type breakdown (TPC = Tesla Proprietary, NACS = North American Charging Standard, CCS1, CCS2, GB/T, Type 2)
- **Status**: OPEN, CONSTRUCTION, PLAN, CLOSED, EXPANDING
- Cross-references to PlugShare and OpenStreetMap

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Community-maintained site status; no real-time stall availability |
| Openness | 3 | Open API, no auth required, public data |
| Stability | 2 | Community project; has been running for 10+ years but no formal SLA |
| Structure | 3 | Clean JSON with rich plug/stall/power detail and cross-references |
| Identifiers | 2 | Numeric IDs + location slugs; PlugShare and OSM cross-references |
| Additive Value | 2 | Tesla-specific; overlaps with AFDC for US; unique global Tesla view |
| **Total** | **13/18** | |

## Notes

- Tesla operates the world's largest fast-charging network. supercharge.info is the definitive community tracker.
- The `otherEVs` flag and detailed plug-type breakdown (`nacs`, `ccs1`, `ccs2`, `gbt`) make this valuable for tracking Tesla's NACS rollout and non-Tesla access expansion.
- The V4 Supercharger data (325 kW+) provides early visibility into next-gen infrastructure.
- For actual real-time Supercharger stall availability, Tesla's private API (used by the Tesla app) provides stall-level status, but it's undocumented and access is restricted.
- The Atom feed enables change tracking for new site openings and status changes.
- Data covers all regions: North America, Europe, Asia Pacific, Middle East.
