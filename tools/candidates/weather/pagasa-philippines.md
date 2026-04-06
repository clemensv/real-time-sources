# PAGASA — Philippine Atmospheric, Geophysical and Astronomical Services Administration

**Country/Region**: Philippines
**Publisher**: PAGASA, Department of Science and Technology (DOST)
**API Endpoint**: `https://bagong.pagasa.dost.gov.ph/` (web portal — no public REST API discovered)
**Documentation**: https://bagong.pagasa.dost.gov.ph/
**Protocol**: Web portal (HTML); internal API behind SPA
**Auth**: N/A (no public API)
**Data Format**: HTML (web), internal JSON
**Update Frequency**: Hourly observations; typhoon bulletins every 6 hours
**License**: Philippine government public data

## What It Provides

PAGASA is the Philippines' national meteorological agency and one of the most operationally critical weather services in Asia. The Philippines is hit by an average of **20 typhoons per year**, making PAGASA's forecasts literally life-or-death for 115 million people.

The website provides:
- **Current weather conditions**: Temperature, rainfall, wind for major stations
- **Typhoon tracking**: Active tropical cyclone advisories and forecast tracks
- **Severe weather bulletins**: Thunderstorm, heavy rainfall, storm surge warnings
- **Climate data**: Historical observations and climate normals
- **Flood advisories**: In coordination with DPWH and local agencies
- **Marine weather**: Sea conditions for inter-island shipping
- **Astronomical data**: Sunrise/sunset, moon phases

### Probe Results

The homepage at `bagong.pagasa.dost.gov.ph` returned current weather data:
- Temperature: 28°C
- Wind: 10.8 km/hr SE
- High/Low: 34°C/23°C
- Clear skies

However, no public REST API was discovered:
- `/api/weather` → 404
- `/api/public-service/weather/forecast` → 404
- The site appears to use server-side rendering rather than a client-side SPA with API calls

## API Details

PAGASA does not currently expose a documented public REST API. The website serves pre-rendered HTML pages. This is a significant gap given the Philippines' extreme disaster exposure and the operational importance of PAGASA data.

### Known Data Access Paths

1. **PAGASA website**: HTML scraping is possible but fragile and not recommended
2. **NDRRMC (National Disaster Risk Reduction and Management Council)**: May have machine-readable alert feeds
3. **Project NOAH (Nationwide Operational Assessment of Hazards)**: Previously had APIs at `noah.up.edu.ph` but status is uncertain
4. **GTS/WIS**: PAGASA contributes to WMO Global Telecommunication System — data available through ECMWF/NOAA
5. **JTWC (Joint Typhoon Warning Center)**: US military typhoon tracking covers Western Pacific

## Freshness Assessment

Website shows fresh data (current hour). PAGASA issues typhoon bulletins every 6 hours during active cyclone events, with interim updates for rapidly developing situations. However, without an API, this freshness isn't programmatically accessible.

## Entity Model

- **Weather Station**: Named stations across the Philippines (~100 synoptic stations)
- **Tropical Cyclone**: Named storms with track coordinates, intensity, forecast cone
- **Weather Warning**: Area-based warnings with severity levels (color-coded)
- **Observation**: Temperature, rainfall, wind, pressure, humidity

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Data is current on website; no API to access it |
| Openness | 1 | No public API; web-only access |
| Stability | 2 | Government agency; website operational but no API commitment |
| Structure | 0 | HTML only; no machine-readable format available |
| Identifiers | 1 | Station names on website; no standard IDs exposed |
| Additive Value | 3 | Critical for Western Pacific typhoon coverage; 115M population; highest typhoon frequency |
| **Total** | **9/18** | |

## Integration Notes

- Currently **not recommended** for integration due to lack of public API
- Monitor for API development — PAGASA has been modernizing (the "bagong" redesigned site)
- Alternative: Use JTWC or ECMWF tropical cyclone data for Western Pacific coverage
- If PAGASA develops an API, it would be one of the highest-value additions — Philippine typhoon data is globally significant
- The Philippines' NDRRMC may be a better target for machine-readable disaster alerts

## Verdict

High importance, low accessibility. PAGASA covers one of the world's most typhoon-exposed regions but has no public API. The website shows they have the data infrastructure — they just haven't exposed it programmatically. This is a source to watch and revisit. In the meantime, Western Pacific typhoon coverage can be partially addressed through JTWC, ECMWF, and JMA tropical cyclone products.
