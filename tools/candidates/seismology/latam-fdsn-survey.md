# Latin American FDSN Seismology — Regional Survey

**Country/Region**: Latin America (Chile, Colombia, Ecuador, Mexico, Argentina, Costa Rica)
**Publisher**: Various national seismological agencies
**API Standard**: FDSN Web Services (fdsnws/event/1/)
**Protocol**: REST (FDSN standard)
**Auth**: None (typically)
**Data Format**: FDSN Text, QuakeML XML

## Overview

This survey documents the status of FDSN (International Federation of Digital Seismograph Networks) web service nodes across Latin America. The FDSN standard provides uniform access to earthquake catalogs — same query format, same output format, different base URLs.

## Nodes Tested — April 2026

| Country | Institution | FDSN Endpoint | Status | Notes |
|---------|------------|---------------|--------|-------|
| **Chile** | CSN | `evtdb.csn.uchile.cl/fdsnws/event/1/` | ❌ 404 | Defunct; use api.xor.cl instead |
| **Colombia** | SGC | `api.sgc.gov.co/fdsnws/event/1/` | ❌ 403 | Blocked |
| **Ecuador** | IGEPN | `cdsb.igepn.edu.ec/eq/events` | ❌ Connection failed | Non-standard path |
| **Mexico** | SSN/UNAM | `ssn.unam.mx` | ❌ Timeout | Server unreachable |
| **Argentina** | INPRES | Not found | ❌ | No known FDSN endpoint |
| **Costa Rica** | RSN/OVSICORI | Not found | ❌ | Joomla CMS only |
| **Peru** | IGP | Custom JSON API | ✅ Working | See igp-peru.md; non-FDSN format |

## Key Findings

### No Working FDSN Nodes in Latin America

This is the most important finding: despite Latin America being one of the most seismically active regions on Earth (Pacific Ring of Fire subduction zones in Chile, Peru, Ecuador, Colombia, Central America, and Mexico), **not a single FDSN event service node is operational** in the region.

Compare with Europe, where 7 FDSN nodes are confirmed working (see fdsn-network-survey.md).

### Why This Matters

- Latin American seismicity is covered by USGS and EMSC for M4+ events
- But local catalogs (M1-3) provide 10-100x more detail
- Chile alone records 20-40+ earthquakes per day (most M2-3)
- Subduction zone monitoring requires dense low-magnitude catalogs

### Workarounds

| Country | Alternative | Quality |
|---------|------------|---------|
| Chile | api.xor.cl/sismo (JSON) | ✅ Good — see chile-csn.md |
| Peru | IGP custom JSON | ✅ Fair — see igp-peru.md |
| Mexico | SSN JSON (when accessible) | ❓ Unknown |
| Colombia | SGC SPA (reverse engineer) | ❌ Difficult |
| Ecuador | None found | ❌ |
| Argentina | None found | ❌ |

## Integration Notes

- A generic FDSN adapter (built for European nodes) would instantly work if any LatAm node comes online
- USGS FDSN with geographic filtering (`minlatitude=-60&maxlatitude=15&minlongitude=-85&maxlongitude=-34`) captures LatAm events above reporting threshold
- The Chile CSN community API is the best available alternative to FDSN for the region

## Verdict

The Latin American FDSN gap is a missed opportunity. The region's seismological agencies have the data but lack the infrastructure to serve it via standard protocols. The generic FDSN adapter should include placeholder configurations for these nodes — when they come online (and they will), adding them is a one-line config change.
