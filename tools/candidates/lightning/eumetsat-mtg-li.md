# EUMETSAT MTG Lightning Imager (MTG-LI)

**Country/Region**: Europe, Africa, Atlantic, Middle East (geostationary at 0° longitude)
**Publisher**: EUMETSAT (European Organisation for the Exploitation of Meteorological Satellites)
**Browse API**: `https://api.eumetsat.int/data/browse/1.0.0/collections/{COLLECTION_ID}?format=json`
**Search API**: `https://api.eumetsat.int/data/search-products/1.0.0/os?pi={COLLECTION_ID}&format=json`
**Token endpoint**: `https://api.eumetsat.int/token` (OAuth2)
**Documentation**: https://data.eumetsat.int/
**Protocol**: REST / OpenSearch over HTTPS, OAuth2 for download
**Auth**: Search/Browse: None (anonymous). Download: Free EUMETSAT EO Portal registration + OAuth2 token.
**Data Format**: NetCDF
**Update Frequency**: ~10-minute product cadence
**License**: Free for registered users — EUMETSAT Data Policy

## What It Provides

The Lightning Imager (LI) on Meteosat Third Generation (MTG-I1, launched December 2022) is the European counterpart to NOAA's GLM. It detects total lightning — both CG and IC — from geostationary orbit, covering Europe, Africa, the Middle East, and the Atlantic Ocean. This is the first European geostationary lightning imager.

### Available Collections

Six distinct LI product types confirmed via the EUMETSAT Data Store API:

| Collection ID | Product | Products/Day |
|---|---|---|
| `EO:EUM:DAT:0691` | **LI Lightning Flashes** | ~130 |
| `EO:EUM:DAT:0782` | LI Lightning Groups | — |
| `EO:EUM:DAT:0690` | LI Lightning Events Filtered | — |
| `EO:EUM:DAT:0686` | LI Accumulated Flashes | — |
| `EO:EUM:DAT:0687` | LI Accumulated Flash Area | — |
| `EO:EUM:DAT:0688` | LI Accumulated Flash Radiance | — |

The L2 event-level products (Flashes, Groups, Events) contain individual lightning detections with coordinates, time, and energy. The accumulated products provide gridded aggregations suitable for mapping and trends.

## API Details

### Browse Collections (No auth)

```
GET https://api.eumetsat.int/data/browse/1.0.0/collections/EO:EUM:DAT:0691?format=json
```

Returns collection metadata including description, temporal extent, and spatial coverage.

### Search Products (No auth)

```
GET https://api.eumetsat.int/data/search-products/1.0.0/os?pi=EO:EUM:DAT:0691&dtstart=2026-04-06T00:00:00Z&dtend=2026-04-06T12:00:00Z&format=json
```

Returns product listings with download URLs, file sizes, and temporal coverage.

### Download (Requires free registration + OAuth2 token)

1. Register at https://eoportal.eumetsat.int/ (free)
2. Obtain OAuth2 token from `https://api.eumetsat.int/token`
3. Download NetCDF products using token

### Sample Product ID

```
W_XX-EUMETSAT-Darmstadt,IMG+SAT,MTI1+LI-2-LFL--FD--x-x--ARC-x_C_EUMT_20260406111019_L2PF_OPE_20260406110002_20260406111002_N__O_0067_0000
```

### Visualization

https://view.eumetsat.int/ (EUMETView) provides web-based visualization of LI products.

## Freshness Assessment

Operational. Product cadence confirmed at ~10 minutes (product time windows like 11:00:02Z–11:10:02Z). 788 flash products generated in the most recent 6-day window — approximately 130 products per day. The MTG-LI is fully operational as of 2026.

## Entity Model

- **Flash** — complete lightning discharge with coordinates, time, energy (L2 product)
- **Group** — clustered events within a flash
- **Event** — individual optical pulse (most granular)
- **Accumulated Flash** — gridded aggregation over time windows (accumulated products)
- **Accumulated Flash Area/Radiance** — spatial and energetic aggregations

This mirrors the GLM data model — the two instruments are functionally equivalent.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | ~10-minute product cadence, operational |
| Openness | 2 | Browse/search open; download requires free registration |
| Stability | 3 | EUMETSAT operational infrastructure |
| Structure | 3 | NetCDF, well-documented API with OpenSearch |
| Identifiers | 2 | Product IDs and internal event IDs |
| Additive Value | 3 | Only open total lightning source for Eastern Hemisphere (Europe/Africa) |
| **Total** | **16/18** | |

## Notes

- The MTG-LI is the European counterpart to NOAA's GLM. Together, GLM (Western Hemisphere) and MTG-LI (Eastern Hemisphere centered on 0° longitude) provide near-global geostationary lightning coverage.
- Free registration at EUMETSAT EO Portal removes the auth barrier in practice — this is "free as in beer" data.
- The OpenSearch/REST API design is modern and well-documented — significantly better than navigating traditional meteorological data archives.
- Six product types provide both event-level (for research/alerting) and accumulated (for mapping/trends) data.
- NetCDF format requires specialized libraries but is standard in meteorological data processing.
- Coverage gap: Far East Asia, Pacific, and the Americas east of ~60°W are outside MTG-I1's field of view. For those regions, use NOAA GLM (GOES) or ground-based networks.
