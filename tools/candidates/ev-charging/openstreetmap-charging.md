# OpenStreetMap — EV Charging Data via Overpass API

**Country/Region**: Global
**Publisher**: OpenStreetMap Foundation / community contributors
**API Endpoint**: `https://overpass-api.de/api/interpreter` (Overpass API)
**Documentation**: https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dcharging_station
**Protocol**: Overpass QL / REST
**Auth**: None
**Data Format**: JSON / XML / CSV
**Real-Time Status**: No — community-maintained map data; no real-time connector status
**Update Frequency**: Continuous community edits (minutes-level for popular areas)
**Station Count**: 200,000+ charging_station nodes globally (estimate)
**License**: Open Data Commons Open Database License (ODbL)

## What It Provides

OpenStreetMap (OSM) is the world's largest collaborative mapping project, and its EV charging data has grown substantially as the EV market expands. Stations are tagged with `amenity=charging_station` and include rich metadata about connectors, power levels, operators, networks, access conditions, and more. The Overpass API enables programmatic querying of OSM data with spatial and tag-based filters.

OSM charging station data is particularly strong in Europe (especially Germany, France, Netherlands) and increasingly comprehensive in North America and Asia.

## API Details

**Overpass API query for charging stations in a bounding box:**
```
[out:json][timeout:60];
node["amenity"="charging_station"](47.3,5.9,47.8,10.5);
out body;
```

**Common tags on charging_station nodes:**
- `amenity=charging_station` — primary tag
- `operator=*` — network/operator name
- `network=*` — charging network
- `socket:type2=*` — number of Type 2 sockets
- `socket:type2_combo=*` — CCS connectors
- `socket:chademo=*` — CHAdeMO connectors
- `socket:type2:output=*` — power in kW per socket type
- `capacity=*` — total number of charging spaces
- `authentication:*` — RFID, app, NFC, etc.
- `fee=*` — whether charging is free or paid
- `opening_hours=*` — access hours
- `ref:OCM=*` — cross-reference to Open Charge Map ID
- `ref:EU:EVSE=*` — eMI3 EVSE ID (where known)

**Rate limits:** Overpass API is free but has fair-use limits. Large queries should be throttled. The global Overpass instance at overpass-api.de is community-operated.

**Alternative access:**
- Planet file download for bulk processing
- Geofabrik extracts for per-country data
- Nominatim for geocoding

## Freshness Assessment

OSM data freshness depends on community activity. In well-mapped areas (Western Europe, US urban centers), new charging stations are typically added within weeks of opening. In less-mapped areas, data can be months or years old. There is no real-time connector status — OSM records what exists, not whether it's currently available.

The `check_date` tag is sometimes used to record when a feature was last verified by a mapper.

## Entity Model

- **Node**: A charging station point with latitude/longitude
- **Tags**: Key-value pairs describing properties (operator, sockets, power, etc.)
- **Relations**: Some stations are mapped as ways (areas) rather than nodes
- **Socket types**: Type 2, Type 2 Combo (CCS), CHAdeMO, Type 1 (J1772), Tesla Supercharger, Schuko, etc.

OSM uses a flat tag model — there's no hierarchical EVSE/connector structure like OCPI. Each socket type is a separate tag on the station node.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Community-maintained; no real-time status; varies by region |
| Openness | 3 | ODbL license; free API; full data dumps available |
| Stability | 3 | 20+ year project; massive community; multiple API mirrors |
| Structure | 2 | Flat tag model; no OCPI hierarchy; inconsistent tagging across regions |
| Identifiers | 1 | OSM node IDs (unstable — can change on edits); optional EVSE cross-refs |
| Additive Value | 2 | Global coverage; complements authoritative sources; ODbL allows remixing |
| **Total** | **12/18** | |

## Notes

- OSM is the "Wikipedia of maps" for EV charging — comprehensive, community-maintained, and globally available, but with variable quality and no real-time status.
- The main value for a bridge is as a fallback/complement for regions where no authoritative government source exists.
- OSM's `ref:EU:EVSE` tag enables cross-referencing with eMI3/OICP EVSE IDs — useful for linking OSM geometry to real-time status from roaming platforms.
- Many EV apps (Chargemap, PlugShare) and data platforms incorporate OSM data as a baseline layer.
- The ODbL license requires attribution and share-alike — any derived database must also be ODbL-licensed.
- For bulk access, Geofabrik country extracts (https://download.geofabrik.de/) are more efficient than Overpass queries.
- The OSM tagging scheme for charging stations is well-documented: https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dcharging_station
