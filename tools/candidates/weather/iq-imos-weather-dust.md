# Iraqi Meteorological Organization & Seismology (IMOS) - Weather & Dust Storm Monitoring

- **Country/Region**: Iraq
- **Endpoint**: `https://meteoseism.gov.iq` (unreachable)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: None accessible
- **Score**: 0/18

## Overview

Iraq faces some of the most severe dust storm conditions in the world. Climate change, desertification, upstream dam construction (reducing Tigris/Euphrates flow), and drought have made dust storms increasingly frequent and intense. These storms:
- Close airports (Baghdad International, Basra, Erbil)
- Cause respiratory health crises (hospitalization spikes)
- Reduce visibility to near-zero on highways
- Are a major quality-of-life issue for Iraqi civilians

Dust storm forecasting and real-time monitoring is **critical data** for Iraq, with high public interest and practical utility.

The Iraqi Meteorological Organization & Seismology (IMOS) is responsible for weather observation and dust storm warnings, but its public-facing infrastructure appears to be offline.

## Endpoint Analysis

**Site unreachable** — same accessibility issues as the seismology endpoint:

```
curl https://meteoseism.gov.iq
# Result: HTTP 403 Forbidden
```

No weather API, no dust storm alert feed, no METAR station data discovered from IMOS sources.

## Search Attempts (Arabic)

Searched for:
- "عواصف ترابية العراق الوقت الحقيقي"
- "محطات الطقس العراق API"
- "meteoseism.gov.iq توقعات الطقس"
- "تحذيرات العواصف الترابية بغداد"

No structured real-time data feeds found from official Iraqi sources.

## Alternative Coverage

Since IMOS is offline, alternative weather data for Iraq:

1. **Aviation METARs** (for major airports):
   - ORBI (Baghdad International)
   - ORMM (Basra International)
   - ORBB (Erbil International)
   - ORSU (Sulaymaniyah International)
   
   Available via NOAA Aviation Weather Center, ICAO global feeds, or aviationweather.gov. These include visibility and present weather (dust indicators).

2. **Satellite-derived dust products**:
   - NASA MODIS/VIIRS aerosol optical depth
   - NOAA GOES (limited coverage, Iraq is on edge)
   - EUMETSAT Meteosat (better Iraq coverage)
   - Copernicus Atmosphere Monitoring Service (CAMS) — dust forecasts
   
   These are gridded products, not station-based.

3. **WMO Global Telecommunication System (GTS)** — Iraq weather stations report into GTS via SYNOP format, but these feeds are not directly accessible without institutional agreements.

## Status

IMOS weather services are not publicly accessible. Iraq has weather stations (at airports, some agricultural sites, military bases) but there is no open real-time data feed.

The dust storm crisis makes this a high-value data gap, but **no accessible source exists from Iraqi government agencies**.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No endpoint accessible |
| Openness | 0 | No data access |
| Stability | 0 | Website offline |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — High-value data (dust storms are a crisis in Iraq), but no accessible endpoint. Document as a critical gap. If IMOS restores public data access, this should be top priority for addition. Aviation METARs provide partial coverage (airports only, limited dust detail).
