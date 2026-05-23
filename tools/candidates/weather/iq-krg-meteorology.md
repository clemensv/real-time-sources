# Kurdistan Regional Government (KRG) - Meteorology and Environment

- **Country/Region**: Kurdistan Region of Iraq (Erbil, Sulaymaniyah, Duhok governorates)
- **Endpoint**: Not discovered (no accessible API)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: None accessible
- **Score**: 0/18

## Overview

The Kurdistan Region of Iraq (KRI) operates semi-autonomous government institutions separate from the federal government in Baghdad. The KRG (Kurdistan Regional Government) has its own:
- **Meteorology Directorate** — weather forecasting and observations
- **Ministry of Environment** — air quality, water, and environmental monitoring
- **Ministry of Electricity** — power grid (separate from federal Iraq grid)
- **Ministry of Natural Resources** — oil and gas sector oversight

The KRG generally has **better-functioning institutions** than federal Iraq, with more international partnerships and technical capacity. This makes KRG data sources potentially more accessible than their federal counterparts.

However, discovery of real-time data endpoints from KRG agencies has proven difficult.

## Search Attempts

### Meteorology

Searched for:
- **Kurdish (Sorani)**: "بەرێوەبەرایەتی کەشناسی کوردستان داتای کەش"
- **English**: "Kurdistan meteorology directorate real-time weather API"
- **KRG portals**: Checked https://gov.krd/ (main KRG portal) — site is up but heavy Cloudflare protection blocks automated access

No real-time weather API discovered.

KRG meteorology likely reports into:
- **ICAO** — Erbil (ORBB) and Sulaymaniyah (ORSU) airports submit METARs (accessible via NOAA Aviation Weather, see `iq-noaa-metar-airports.md`)
- **WMO GTS** — Kurdistan weather stations may report via WMO Global Telecommunication System, but this is not publicly accessible

### Environment

Searched for:
- **Kurdish**: "وەزارەتی ژینگەی کوردستان"
- **English**: "KRG Ministry of Environment air quality monitoring"

No real-time air quality or environmental data API found.

### Electricity

Searched for:
- **Kurdish**: "وەزارەتی کارەبای کوردستان"
- **English**: "KRG electricity grid load outage map"

No real-time grid data found. (See separate `iq-krg-electricity.md` if that is created.)

## Known Context

The KRG has partnerships with international agencies and foreign governments that may collect but not publish real-time data:
- **U.S. Consulate Erbil** — may monitor air quality internally (not published)
- **European Union** — supports KRG institution building
- **University of Kurdistan** (Erbil) — may operate weather/environmental research stations (not published as open data)

## Alternative Coverage

Kurdistan-specific data accessible via international sources:
- **METARs** — Erbil (ORBB) and Sulaymaniyah (ORSU) airports (via NOAA Aviation Weather)
- **Earthquakes** — USGS and EMSC cover Kurdistan region (see seismology candidates)
- **Satellite** — NASA FIRMS fires, VIIRS flaring (cover KRG oil fields)

No Kurdistan-specific real-time data portals discovered beyond what federal Iraq or international sources provide.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No accessible source |
| Openness | 0 | No API discovered |
| Stability | 0 | N/A |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — KRG has better institutional capacity than federal Iraq, and there is reason to believe they collect weather, air quality, and grid data. **But no publicly accessible real-time API or data portal has been discovered.** KRG websites are online (unlike many federal sites) but heavily protected (Cloudflare, no automated access). Kurdistan data is currently accessible only via:
1. Aviation METARs (Erbil, Sulaymaniyah airports)
2. International sources (USGS, EMSC, NASA satellites)

If KRG ever launches an open data portal or publishes real-time environmental/weather data, it should be added. For now, no endpoint exists.
