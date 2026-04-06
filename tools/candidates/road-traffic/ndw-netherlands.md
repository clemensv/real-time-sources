# NDW Netherlands Road Traffic

**Country/Region**: Netherlands
**Publisher**: NDW (Nationale Databank Wegverkeersgegevens) / Rijkswaterstaat
**API Endpoint**: `https://opendata.ndw.nu/`
**Documentation**: https://opendata.ndw.nu/ and https://docs.ndw.nu/
**Protocol**: File download (DATEX II v3)
**Auth**: None
**Data Format**: XML (DATEX II v3), compressed with gzip
**Update Frequency**: Every 1 minute (traffic speed/flow), every 15 minutes (travel times)
**License**: Dutch government open data

## What It Provides

NDW operates the Netherlands' national traffic data portal, publishing comprehensive real-time and near-real-time data for the Dutch road network. Data streams include current traffic speeds, travel times, traffic flow measurements, incident/roadwork situations, variable message sign states, and matrix signal information. The portal uses DATEX II v3 — the European standard for traffic data exchange.

## API Details

All data is distributed as gzip-compressed XML files, updated continuously:

**Real-time traffic data:**
| File | Size | Update | Content |
|------|------|--------|---------|
| `trafficspeed.xml.gz` | 1.0 MB | 1 min | Current speeds per road segment |
| `traveltime.xml.gz` | 2.5 MB | 1 min | Travel times between measurement points |
| `measurement.xml.gz` | 13 MB | varies | Traffic volume measurements |
| `actueel_beeld.xml.gz` | 244 KB | 1 min | Current traffic situation overview |

**Situation data:**
| File | Size | Update | Content |
|------|------|--------|---------|
| `planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz` | 19 MB | 15 min | Roadworks and events |
| `tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz` | 131 KB | 1 min | Temporary road closures |
| `tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz` | 22 KB | 1 min | Temporary speed limits |
| `veiligheidsgerelateerde_berichten_srti.xml.gz` | 18 KB | 1 min | Safety-related traffic information |

**Signage and infrastructure:**
| File | Size | Update | Content |
|------|------|--------|---------|
| `dynamische_route_informatie_paneel.xml.gz` | 652 KB | 1 min | Variable message signs (DRIPs) |
| `Matrixsignaalinformatie.xml.gz` | 1.0 MB | 1 min | Matrix signal information |

**Also includes EV charging and parking data** (see ev-charging and parking candidates).

All files use DATEX II v3 schema (migrated from v2.3 as of April 2026).

## Freshness Assessment

Traffic speed and travel time data update every minute — this is as real-time as file-based distribution gets. Situation data (roadworks, closures) updates in near real-time. The NDW portal is the authoritative Dutch national traffic data source fed by thousands of road sensors, cameras, and traffic management systems. Exceptional freshness.

## Entity Model

- **Measurement Site**: Road sensor with ID, location, road reference
- **Traffic Speed**: Current speed per road segment (km/h), per lane
- **Travel Time**: Measured travel time between points (seconds)
- **Traffic Flow**: Vehicle count per measurement period, by vehicle class
- **Situation**: Incident/roadwork with type, location, duration, severity
- **VMS/DRIP**: Variable message sign content and state
- **Matrix Signal**: Lane control signals (open, closed, speed limit, merge)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Per-minute updates for traffic speed/flow |
| Openness | 3 | No auth, no registration, direct file download |
| Stability | 3 | Government-operated, DATEX II v3 standard |
| Structure | 3 | DATEX II v3 — strict, well-defined XML schema |
| Identifiers | 3 | Measurement site IDs, situation IDs, road references |
| Additive Value | 3 | Comprehensive Dutch traffic data; model for DATEX II integration |
| **Total** | **18/18** | |

## Notes

- NDW is a DATEX II reference implementation. Building a DATEX II v3 parser for NDW data enables integration with traffic data from many European countries (Sweden, Finland, Germany, UK, etc.) that use the same standard.
- The file-based distribution model requires periodic downloading and diffing. A bridge would fetch compressed XML files, parse DATEX II, compare with previous state, and emit change events.
- The sheer volume of data is significant — `measurement.xml.gz` alone is 13 MB compressed. Efficient parsing and selective processing are important.
- NDW also publishes EV charging (OCPI) and truck parking (DATEX II) data on the same portal — a single platform for multiple data domains.
- DATEX II v3 migration was recently completed (April 2026) — ensure any parser handles v3 schema, not v2.3.
- Reference data (measurement site locations, road network geometry) is available as shapefiles for cross-referencing.
