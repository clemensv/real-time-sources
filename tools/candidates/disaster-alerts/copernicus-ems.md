# Copernicus Emergency Management Service (EMS) Rapid Mapping
**Country/Region**: Global (EU-focused activation)
**Publisher**: European Commission / Copernicus Programme
**API Endpoint**: `https://emergency.copernicus.eu/mapping/list-of-activations-rapid` (web portal)
**Documentation**: https://emergency.copernicus.eu/mapping/
**Protocol**: Web portal (no REST API discovered)
**Auth**: None for public portal
**Data Format**: HTML, downloadable vector/raster products (GeoTIFF, SHP, PDF)
**Update Frequency**: Per-activation (hours to days after disaster event)
**License**: Copernicus data policy — free and open

## What It Provides
Copernicus EMS Rapid Mapping provides satellite-derived geospatial information for emergency response:
- **Rapid Mapping**: Satellite imagery analysis within hours of disaster activation
- **Risk & Recovery**: Post-disaster damage assessment and recovery monitoring
- Activation types: floods, earthquakes, fires, volcanic eruptions, industrial accidents, humanitarian crises
- Products: reference maps, delineation maps, grading maps (damage assessment)
- Activation by EU member states, EU institutions, or international partners

Each activation produces vector data (affected areas, damaged infrastructure) and raster products (satellite imagery overlays).

## API Details
- **Activation list**: `https://emergency.copernicus.eu/mapping/list-of-activations-rapid`
- **Individual activation**: `https://emergency.copernicus.eu/mapping/list-of-components/EMSR{number}`
- **Product download**: Each activation produces downloadable GIS packages
- **No REST API**: Probing `/feed`, `/api/`, RSS/Atom endpoints all returned 404
- **GIS services**: Products may be available via WMS/WFS for individual activations
- **Activation codes**: EMSR-prefixed sequential numbers (e.g., EMSR742)

## Probe Results
```
Main portal: HTTP 200 OK (HTML)
/mapping/feed: 404 Not Found
/mapping/list-of-activations-rapid/feed: 404 Not Found
/mapping/activations/feed: 404 Not Found
Assessment: Web portal functional, no public API or syndication feed
```

## Freshness Assessment
Variable. Rapid Mapping activations produce first products within 6-24 hours of activation request. Multiple product updates follow. However, data access is through a web portal requiring manual navigation — no automated feed for new activations.

## Entity Model
- **Activation** (EMSR number, title, country, activation date, type, status)
- **Component** (area of interest within activation)
- **Product** (reference map, delineation, grading — with version)
- **Geographic** (footprint polygon, country, coordinates)
- **Imagery** (satellite source, acquisition date, resolution)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Products within hours, but no automated feed |
| Openness | 2 | Free data, but web portal only |
| Stability | 3 | EU Copernicus programme, multi-decade funding |
| Structure | 1 | HTML portal, no REST API or RSS feed |
| Identifiers | 3 | Stable EMSR activation codes |
| Additive Value | 3 | Unique satellite-derived disaster mapping |
| **Total** | **14/18** | |

## Notes
- The lack of an RSS/Atom feed is surprising for a major EU programme — this may change
- GIS products (SHP, GeoTIFF) are high-value but require spatial data processing
- Activation data could potentially be scraped from the portal HTML
- Pairs well with GDACS and EFAS for a complete EU disaster data picture
- Copernicus Climate Data Store (CDS) has better API access for climate products
- Consider monitoring the portal for eventual API release
