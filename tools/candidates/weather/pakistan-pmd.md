# Pakistan Meteorological Department (PMD) — Weather Observations

**Country/Region**: Pakistan
**Publisher**: Pakistan Meteorological Department (PMD)
**API Endpoint**: `https://nwfc.pmd.gov.pk/` (National Weather Forecasting Centre), `https://www.pmd.gov.pk/`
**Documentation**: https://www.pmd.gov.pk/
**Protocol**: Web portal (HTML) — API access blocked (403)
**Auth**: N/A (access denied)
**Data Format**: HTML
**Update Frequency**: Synoptic (3-hourly observations), forecasts daily
**License**: Pakistan government data

## What It Provides

PMD operates Pakistan's national weather observation network covering approximately 100+ stations across geographically extreme terrain — from the Karakoram glaciers (K2 region) to the Thar Desert, and from monsoon-prone Sindh coast to continental Punjab.

The PMD website and NWFC portal provide:
- **Current observations**: Temperature, rainfall, wind, humidity from stations nationwide
- **Monsoon bulletins**: Critical during July–September monsoon season
- **Tropical cyclone advisories**: For Arabian Sea cyclones
- **Flood warnings**: In coordination with FFD (Flood Forecasting Division)
- **Seasonal outlooks**: Pre-monsoon, monsoon, winter forecasts
- **Seismic monitoring**: PMD also operates Pakistan's seismological network
- **Air quality**: Limited monitoring in major cities

### Probe Results

Both PMD endpoints returned **HTTP 403 Forbidden**:
- `https://nwfc.pmd.gov.pk/new/latest-observations.php` → 403
- `https://www.pmd.gov.pk/rmc/rmc_files/real_time_bulletin.php` → 403

The 403 response suggests either:
1. Geographic IP blocking (common for South Asian government sites)
2. User-agent filtering
3. Cloudflare or WAF protection
4. Intentional access restriction

The seismic endpoint `seismic.pmd.gov.pk` also returned 403 in earlier repository research.

## API Details

No public API discovered. PMD's data is primarily delivered through:
1. HTML web pages (server-side rendered)
2. PDF bulletins uploaded periodically
3. Media briefings during major weather events

### Alternative Data Paths

- **Pakistan Open Data Portal** (`data.gov.pk`): May have some PMD datasets
- **Regional Specialized Meteorological Centre (RSMC) New Delhi**: IMD provides cyclone advisories that cover Pakistan's maritime zone
- **WMO GTS**: PMD synoptic observations are shared via GTS and available through ECMWF/NOAA
- **GLOF monitoring**: Pakistan's NDMA tracks glacial lake outburst floods — critical for northern areas

## Freshness Assessment

Cannot be verified due to 403 access denial. PMD issues weather bulletins multiple times daily and increases frequency during monsoon season and cyclone events. The underlying data infrastructure exists but is not programmatically accessible.

## Entity Model

- **Station**: ~100 synoptic stations; named by city (Lahore, Karachi, Islamabad, Peshawar, Quetta, etc.)
- **Observation**: Temperature, rainfall, wind, humidity, pressure
- **Bulletin**: PDF/HTML forecasts issued 2-4 times daily
- **Warning**: Monsoon, flood, cyclone, heat wave advisories

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists but not accessible via API |
| Openness | 0 | HTTP 403 on all endpoints tested |
| Stability | 1 | Government service exists; no public API guarantee |
| Structure | 0 | HTML/PDF only; no machine-readable format accessible |
| Identifiers | 1 | Station names implied; no standard IDs exposed |
| Additive Value | 3 | 230M population; monsoon/flood critical; glacial monitoring; no current coverage |
| **Total** | **6/18** | |

## Integration Notes

- **Not currently viable** for integration — all endpoints return 403
- Pakistan's 2022 catastrophic floods (1/3 of country submerged) underscored the critical importance of Pakistani hydro-met data
- Alternative paths: ECMWF global models, WMO GTS data via NOAA, or contact PMD directly for API access
- The seismic monitoring data would be particularly valuable — Pakistan sits on the India-Eurasia collision zone
- Monitor for open data initiatives — Pakistan has been expanding data.gov.pk

## Verdict

Inaccessible but critically important. Pakistan's 230M people face monsoons, floods, cyclones, earthquakes, and glacial hazards. PMD has the data but does not expose it through public APIs. The 403 responses across all endpoints suggest deliberate access restriction. This is a gap that matters — Pakistan's 2022 floods killed 1,700+ people and displaced 33 million. Worth revisiting and potentially pursuing through official channels.
