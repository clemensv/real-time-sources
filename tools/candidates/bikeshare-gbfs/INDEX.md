# Bikeshare / GBFS Candidates

Real-time bikeshare and micromobility data sources. GBFS (General Bikeshare Feed Specification) is the dominant standard — the MobilityData catalog lists 1,315 systems across 50+ countries. A single bridge built against this catalog unlocks the vast majority of the world's bikeshare data. E-scooter operators (Dott, Bird, Lime, Bolt, Voi) add another 500+ city feeds through the same standard.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [MobilityData GBFS Catalog](mobilitydata-gbfs-catalog.md) | **Global** | **18/18** | GBFS | Master catalog of 1,315 systems; single bridge unlocks everything |
| [Taipei YouBike](taipei-youbike.md) | **Taiwan** | **17/18** | REST (proprietary) | 9,070 stations — NOT in GBFS catalog; needs dedicated bridge |
| [Seoul Ddareungi](seoul-ddareungi.md) | **South Korea** | 16/18 | REST (proprietary) | 3,223 stations — NOT in GBFS catalog; needs API key |
| [Tokyo Docomo Bikeshare](tokyo-docomo-bikeshare.md) | Japan — Tokyo | **18/18** | GBFS 2.3 | 1,794 stations via ODPT; largest Asian GBFS system |
| [Citi Bike NYC](citibike-nyc.md) | US — NYC | 17/18 | GBFS 1.1 | Largest US bikeshare; Lyft-operated |
| [Santander Cycles London](santander-cycles-london.md) | UK — London | 17/18 | REST/XML (TfL) | Not in GBFS catalog — needs dedicated bridge |
| [Vélib' Paris](velib-paris.md) | France — Paris | 17/18 | GBFS + Opendatasoft | Largest European system; dual API endpoints |
| [Barcelona Bicing](barcelona-bicing.md) | Spain — Barcelona | 17/18 | GBFS 3.0 | 543 stations; PBSC platform (same as Buenos Aires, Rio, Toronto) |
| [Oslo Bysykkel](oslo-bysykkel.md) | Norway — Oslo | 17/18 | GBFS 2.3 | Urban Sharing platform (Oslo, Bergen, Milan, Edinburgh); 10s TTL |
| [Montreal BIXI](montreal-bixi.md) | Canada — Montreal | 16/18 | GBFS 1.0 | 873 stations; pioneering bikeshare (since 2009) |
| [Dublin Bikes](dublin-bikes.md) | Ireland — Dublin | 17/18 | GBFS 2.3 | JCDecaux CycloCity platform (Dublin, Nantes, Lyon, Seville, etc.) |
| [E-Scooter GBFS Operators](escooter-gbfs-operators.md) | **Global** | 17/18 | GBFS 2.2–3.0 | Dott (339 cities), Bird (124), Lime (45), Bolt (18), Voi (15) |
| [Bay Wheels SF](bay-wheels-sf.md) | US — Bay Area | 16/18 | GBFS 1.1 | Lyft-operated; hybrid dock+dockless |
| [Capital Bikeshare DC](capital-bikeshare-dc.md) | US — DC | 16/18 | GBFS 1.1 | Lyft-operated; multi-jurisdictional |
| [nextbike](nextbike.md) | **Pan-European** | 17/18 | GBFS 2.3 | 300+ cities across 30+ countries |

## Recommended Approach

1. **Build a generic GBFS bridge** using the MobilityData catalog as the discovery mechanism. This single bridge covers 1,315 systems including Citi Bike, Bay Wheels, Capital Bikeshare, Vélib', nextbike, BIXI, Bicing, Oslo, Divvy, all e-scooter operators, and hundreds more. Support GBFS 1.0, 1.1, 2.x, and 3.0 schemas.

2. **Build a Taipei YouBike bridge** — the largest Asian bikeshare (9,070 stations) uses a proprietary JSON API, not GBFS. Taiwan has zero GBFS catalog entries.

3. **Build a Seoul Ddareungi bridge** — South Korea's largest bikeshare (3,223 stations) uses Seoul's Open Data API with a proprietary format. Requires API key registration.

4. **Build a TfL Santander Cycles bridge** separately — London uses a proprietary TfL API format not in the GBFS catalog.

5. The Lyft-operated systems (Citi Bike, Bay Wheels, Capital Bikeshare, Divvy, BIKETOWN, Ecobici Mexico City) are covered by the generic GBFS bridge — no separate work needed.

## Platform Patterns

The GBFS ecosystem is dominated by a few operator platforms. Building support for one system on a platform effectively covers all systems on that platform:

- **Lyft GBFS**: NYC, SF, DC, Chicago, Portland, Mexico City — `gbfs.lyft.com/gbfs/1.1/{city}/`
- **PBSC Urban Solutions**: Barcelona, Buenos Aires, Rio de Janeiro, Toronto — `{city}.publicbikesystem.net/customer/gbfs/v3.0/`
- **Urban Sharing**: Oslo, Bergen, Trondheim, Milan, Edinburgh — `gbfs.urbansharing.com/{domain}/`
- **nextbike (TIER)**: 300+ European cities — `gbfs.nextbike.net/maps/gbfs/v2/nextbike_{id}/`
- **JCDecaux CycloCity**: Dublin, Nantes, Lyon, Toulouse, Seville — `api.cyclocity.fr/contracts/{city}/`
- **Dott**: 339 cities — `gbfs.api.ridedott.com/public/v2/{city}/`
- **Bird**: 124 cities — `mds.bird.co/gbfs/v2/public/{city}/`

## Cargo Bike GBFS

Seven cargo bike share systems publish GBFS: carvelo (CH), Beryl Hackney (London), WESTcargo (Bristol), Gothenburg Cargo, LastenVelo (Freiburg), FaRe Lastenrad, and stadtRad Lastenrad. All are in the GBFS catalog and covered by the generic bridge.

## Coverage Summary

- **Americas**: US (NYC, SF, DC, Chicago, Portland), Canada (Montreal, Toronto), Mexico (CDMX), Brazil (Rio), Argentina (Buenos Aires) — via GBFS catalog
- **Europe**: UK (London — TfL), France (Paris), Spain (Barcelona), Italy (Milan), Ireland (Dublin), Germany/Austria/Switzerland/Poland (nextbike), Nordics (Oslo, Bergen, Trondheim) — via GBFS catalog + nextbike
- **Asia**: Japan (Tokyo Docomo — GBFS), **Taiwan (YouBike — proprietary)**, **South Korea (Seoul — proprietary)**
- **Micromobility**: Dott, Bird, Lime, Bolt, Voi — 500+ city feeds via GBFS catalog
- **Not in GBFS**: TIER (despite owning nextbike), Helsinki City Bikes (discontinued 2023)
