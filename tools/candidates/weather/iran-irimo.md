# Iran IRIMO — Islamic Republic of Iran Meteorological Organization

**Country/Region**: Iran
**Publisher**: Iran Meteorological Organization (IRIMO)
**API Endpoint**: `https://www.irimo.ir/` (web portal — connection failed)
**Documentation**: https://www.irimo.ir/eng/
**Protocol**: Web portal (HTML)
**Auth**: N/A (connection failed)
**Data Format**: HTML, PDF bulletins
**Update Frequency**: 3-hourly synoptic; daily forecasts
**License**: Iranian government data

## What It Provides

IRIMO monitors weather across Iran — a large country (1.6 million km²) with extreme climate diversity: Caspian coast humidity, Zagros mountain snows, Dasht-e Kavir desert heat, and Persian Gulf maritime conditions.

Key data types:
- **Weather observations**: ~350 synoptic stations, 1,500+ climatological stations
- **Forecasts**: City and provincial forecasts
- **Warnings**: Dust storms (Iranian plateau), floods (Zagros), heat waves (Khuzestan — world's highest heat indices)
- **Agricultural meteorology**: Important for Iran's pistachio, saffron, and wheat production
- **Aviation weather**: Tehran Imam Khomeini, Mehrabad, Isfahan, Shiraz, Mashhad airports
- **Marine weather**: Persian Gulf and Gulf of Oman

### Regional Significance

- **Dust storms**: Iranian dust storms affect Iraq, Kuwait, Saudi Arabia, and Gulf states
- **Heat extremes**: Ahvaz and Bandar Mahshahr record some of the highest temperatures on Earth
- **Flash floods**: Zagros mountain runoff causes devastating flash floods
- **Caspian Sea**: Level changes and storms affect northern Iran

### Probe Results

Connection to `irimo.ir/eng/wd/720-Products-services.html` **failed** (connection timeout). Iranian web infrastructure may be:
1. Subject to network routing limitations
2. Behind national internet infrastructure (NIN)
3. Blocked or throttled for international access

### Alternative Data Access

- **WMO GTS**: Iran shares synoptic data via WMO Global Telecommunication System
- **ECMWF**: Global forecast models cover Iran
- **Aviation**: METAR/TAF for Iranian airports available through standard aviation data channels
- **NOAA/NCEI**: Historical Iranian climate data archived

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists; not accessible from international origins |
| Openness | 0 | Connection failed; no public API known |
| Stability | 1 | National meteorological service exists; web access unreliable internationally |
| Structure | 0 | Cannot verify |
| Identifiers | 1 | WMO station numbers exist in GTS |
| Additive Value | 2 | 85M population; extreme weather; dust storms; but data available through global channels |
| **Total** | **5/18** | |

## Verdict

Inaccessible from international origins. Iran has significant meteorological infrastructure serving 85 million people, but web access to IRIMO fails from outside Iran. Iranian weather data is partially available through WMO GTS and global forecast models. For practical purposes, ECMWF and Open-Meteo provide forecast coverage. A documented gap with limited workaround potential.
