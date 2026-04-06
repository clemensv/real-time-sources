# Bikeshare / GBFS Candidates

Real-time bikeshare and micromobility data sources. GBFS (General Bikeshare Feed Specification) is the dominant standard — a single bridge built against the MobilityData catalog can unlock hundreds of city systems.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [MobilityData GBFS Catalog](mobilitydata-gbfs-catalog.md) | **Global** | **18/18** | GBFS | Master catalog of 800+ systems; single bridge unlocks everything |
| [Citi Bike NYC](citibike-nyc.md) | US — NYC | 17/18 | GBFS 1.1 | Largest US bikeshare; Lyft-operated |
| [Santander Cycles London](santander-cycles-london.md) | UK — London | 17/18 | REST/XML (TfL) | Not in GBFS catalog — needs dedicated bridge |
| [Vélib' Paris](velib-paris.md) | France — Paris | 17/18 | GBFS + Opendatasoft | Largest European system; dual API endpoints |
| [Bay Wheels SF](bay-wheels-sf.md) | US — Bay Area | 16/18 | GBFS 1.1 | Lyft-operated; hybrid dock+dockless |
| [Capital Bikeshare DC](capital-bikeshare-dc.md) | US — DC | 16/18 | GBFS 1.1 | Lyft-operated; multi-jurisdictional |
| [nextbike](nextbike.md) | **Pan-European** | 17/18 | GBFS 2.3 | 300+ cities across 30+ countries |

## Recommended Approach

1. **Build a generic GBFS bridge** using the MobilityData catalog as the discovery mechanism. This single bridge covers Citi Bike, Bay Wheels, Capital Bikeshare, Vélib', nextbike, and hundreds of other systems. Support GBFS 1.1, 2.x, and 3.0 schemas.

2. **Build a TfL Santander Cycles bridge** separately — London uses a proprietary API format not in the GBFS catalog.

3. The Lyft-operated systems (Citi Bike, Bay Wheels, Capital Bikeshare, Divvy) are individually documented here as reference and test cases, but they require zero additional work beyond the generic GBFS bridge.

## Coverage Summary

- **Americas**: US (NYC, SF, DC, Chicago, etc.), Canada, Brazil, Argentina, Mexico — via GBFS catalog
- **Europe**: UK (London — TfL), France (Paris), Germany, Austria, Switzerland, Poland, Nordics — via GBFS catalog + nextbike
- **Other**: UAE, Asia-Pacific, Africa — via GBFS catalog
