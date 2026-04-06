# Bangladesh Meteorological Department (BMD) — Weather & Cyclone Monitoring

**Country/Region**: Bangladesh
**Publisher**: Bangladesh Meteorological Department (BMD)
**API Endpoint**: `https://bmd.gov.bd/` (web portal only)
**Documentation**: https://bmd.gov.bd/
**Protocol**: Web portal (HTML)
**Auth**: N/A (no public API)
**Data Format**: HTML, XML sitemaps
**Update Frequency**: 3-hourly synoptic observations; cyclone bulletins every 3 hours during active storms
**License**: Bangladesh government data

## What It Provides

BMD monitors weather across one of the world's most climate-vulnerable countries. Bangladesh — low-lying, densely populated, at the mouth of the Ganges-Brahmaputra delta — faces cyclones, monsoon floods, river erosion, and heat waves with devastating regularity.

The BMD website provides:
- **Current weather observations**: Temperature, rainfall, humidity from ~100 stations
- **Cyclone warnings**: Bay of Bengal tropical cyclone tracking and landfall forecasts
- **Monsoon forecasts**: Critical for 170M people in a flood-prone nation
- **River level bulletins**: In coordination with FFWC (Flood Forecasting & Warning Centre)
- **Marine weather**: For Bay of Bengal shipping and fishing
- **Climate data**: Historical records and climate normals

### Probe Results

The BMD website at `bmd.gov.bd` loaded successfully, returning minimal HTML with references to:
- Bangla sitemap: `https://bmd.gov.bd/web/bangla_bmd.xml`
- English sitemap: `https://bmd.gov.bd/web/english_bmd.xml`

The site appears to be a modern SPA but no API endpoints were discoverable. The sitemap references suggest structured content exists but isn't exposed as a REST API.

## API Details

No public API found. BMD's data infrastructure includes:
1. **FFWC (Flood Forecasting & Warning Centre)**: Operates river level monitoring — `www.ffwc.gov.bd`
2. **SPARRSO**: Bangladesh's satellite data agency
3. **BMD Agromet Bulletins**: Agricultural weather advisories
4. **WMO GTS**: BMD shares synoptic observations internationally via GTS

### FFWC — Potential Alternative

The Flood Forecasting & Warning Centre at `ffwc.gov.bd` may have more machine-readable data — it monitors water levels at ~100+ river gauge stations across Bangladesh and issues flood forecasts. This is arguably more operationally critical than the weather data for Bangladesh.

## Freshness Assessment

Cannot verify through API. BMD issues observations 8 times daily (3-hourly synoptic schedule) and increases to hourly during severe weather. Cyclone bulletins are issued every 3 hours during active Bay of Bengal storms — these bulletins are the primary warning mechanism for coastal Bangladesh.

## Entity Model

- **Weather Station**: ~100 stations; major cities and coastal points
- **Cyclone**: Named storms in Bay of Bengal with track, intensity, forecast
- **River Gauge**: FFWC stations on major rivers (Padma, Jamuna, Meghna)
- **Warning Area**: Coastal districts for cyclone warnings; river basins for flood warnings

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists but no API to access it |
| Openness | 1 | Website loads; no API discovered |
| Stability | 1 | Government service; web presence but no API commitment |
| Structure | 0 | HTML/PDF only; sitemaps suggest some structure |
| Identifiers | 1 | Station names; no standard IDs exposed |
| Additive Value | 3 | 170M in extreme climate vulnerability; Bay of Bengal cyclones; monsoon floods |
| **Total** | **7/18** | |

## Integration Notes

- **Not currently viable** as a direct data source
- The FFWC (Flood Forecasting) is potentially a better target — flood data is Bangladesh's most critical real-time need
- Alternative: ECMWF cyclone tracking covers Bay of Bengal; India's IMD RSMC New Delhi issues cyclone advisories for the Bay of Bengal
- The Ganges-Brahmaputra monitoring is partially available through Nepal's BIPAD portal (upstream)
- Bangladesh contributed significantly to RIMES (Regional Integrated Multi-Hazard EWS)
- Monitor for open data initiatives — Bangladesh has been investing in e-governance

## Verdict

Critical importance, no API. Bangladesh is one of the most climate-vulnerable countries on Earth — 170 million people in a low-lying delta facing cyclones, monsoon floods, and sea level rise. BMD has data but no public API. The FFWC flood forecasting system may be a more productive target for machine-readable data. Currently a documented gap.
