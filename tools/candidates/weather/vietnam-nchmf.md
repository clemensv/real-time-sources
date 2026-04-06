# Vietnam NCHMF — National Centre for Hydro-Meteorological Forecasting

**Country/Region**: Vietnam
**Publisher**: National Centre for Hydro-Meteorological Forecasting (NCHMF), Vietnam Meteorological and Hydrological Administration (VNMHA)
**API Endpoint**: `https://nchmf.gov.vn/` (web portal)
**Documentation**: https://nchmf.gov.vn/
**Protocol**: Web portal (HTML)
**Auth**: N/A
**Data Format**: HTML, Vietnamese language
**Update Frequency**: 3-hourly synoptic observations; typhoon bulletins every 3-6 hours
**License**: Vietnamese government data

## What It Provides

Vietnam stretches 1,650 km along the South China Sea coast, facing extreme weather from all directions: South China Sea typhoons from the east, Mekong River flooding from the west, and monsoon rainfall across the central highlands.

NCHMF monitors:
- **Typhoons**: Vietnam is hit by 6-8 typhoons annually (locally called "bão")
- **Monsoon forecasting**: Northeast monsoon (October-March) and Southwest monsoon (May-September)
- **Flooding**: Mekong Delta flooding (annual event affecting millions)
- **Flash floods**: Central highlands and northern mountains
- **Drought**: Central and southern Vietnam during El Niño years
- **Marine weather**: Critical for Vietnam's 3,400 km coastline and fishing fleet
- **Air quality**: Hanoi regularly experiences poor AQ (winter rice straw burning + traffic)

### Probe Results

Website was not directly probed but NCHMF is known to be a web-only service with:
- Forecast maps and bulletins in Vietnamese
- Typhoon tracking pages during active storms
- River water level data for major basins

No public REST API has been documented.

### Alternative Data Paths

- **WMO GTS**: Vietnam shares synoptic data internationally
- **Mekong River Commission**: Covers Vietnamese stations on the Mekong
- **JMA**: Japanese collaboration on typhoon forecasting
- **ECMWF**: Global model coverage

## Entity Model

- **Weather Station**: ~200+ stations across 63 provinces
- **River Basin**: Red River, Mekong Delta, Central Vietnam rivers
- **Typhoon**: Named storms in South China Sea/Western Pacific
- **Province**: 63 provinces with separate forecasts

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists but not API-accessible |
| Openness | 0 | No public API; Vietnamese language website |
| Stability | 1 | National agency; operational but no API |
| Structure | 0 | HTML only |
| Identifiers | 1 | Station names; WMO IDs in GTS |
| Additive Value | 3 | 100M population; major typhoon exposure; Mekong Delta flooding |
| **Total** | **6/18** | |

## Verdict

High importance, no API. Vietnam's 100 million people face typhoons, monsoon floods, and Mekong Delta challenges. NCHMF has operational data but no public API. The Mekong River Commission provides partial coverage for Vietnam's hydrological data. Documented as a gap.
