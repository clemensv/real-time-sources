# OGIMET — Global Synoptic Data Aggregator

**Country/Region**: Global
**Publisher**: OGIMET (personal project by Guillermo Ballester Valor)
**API Endpoint**: `https://ogimet.com/cgi-bin/getsynop`
**Documentation**: https://ogimet.com/synops.phtml.en (usage notes)
**Protocol**: CGI (HTTP GET, plain text response)
**Auth**: None (open access)
**Data Format**: Plain text (raw SYNOP/METAR messages, comma-delimited metadata)
**Update Frequency**: Near-real-time (follows WMO synoptic schedule)
**License**: Informational use — data sourced from WMO GTS

## What It Provides

OGIMET is a long-running personal project that collects and redistributes weather observations from the WMO Global Telecommunication System (GTS). It provides access to:

- **SYNOP Reports** (`getsynop`): Raw surface synoptic observation messages (FM-12 format) from WMO member stations worldwide. Queried by WMO station block number and time range.

- **METAR Reports**: Aviation weather reports from airports worldwide.

- **BUOY Reports**: Ocean buoy observations.

- **TEMP/Radiosonde**: Upper-air sounding data.

- **Display Services**: Various rendered observation displays (web pages, not API).

## API Details

The `getsynop` CGI endpoint returns raw SYNOP data:
```
GET https://ogimet.com/cgi-bin/getsynop?block=03772&begin=202604060000&end=202604061800
```

Response is plain text with comma-delimited metadata followed by the raw SYNOP message:
```
03772,2026,04,06,00,00,AAXX 06004 03772 05982 12603 10053 20002 30232 40263 53013 ...
```

Fields: WMO block, year, month, day, hour, minute, then the raw SYNOP code (FM-12 SYNOP format).

Parameters:
- `block`: WMO station number (5 digits)
- `begin`/`end`: Time range in `YYYYMMDDHHMM` format

No authentication. SYNOP decoding requires knowledge of WMO code tables.

## Freshness Assessment

- Data follows WMO synoptic hours (00, 03, 06, 09, 12, 15, 18, 21 UTC for main synoptic hours).
- Reports from automated stations can arrive at intermediate times (every 30 minutes).
- Probed live — received data for current date (2026-04-06) with reports at 00:00 through 10:30 UTC.
- Latency appears to be minutes to an hour after the observation time.

## Entity Model

- **Station**: WMO block number (5-digit international identifier, e.g., 03772 = London/Heathrow).
- **Report**: Timestamped raw SYNOP message in FM-12 format.
- **Parameters** (encoded within SYNOP): temperature, dewpoint, pressure, wind, weather, clouds, precipitation, sunshine — requires FM-12 decoding.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time, but synoptic schedule (3–6 hourly), some lag |
| Openness | 3 | No auth, free access |
| Stability | 1 | Personal project, single operator, disclaimer warns against critical use |
| Structure | 1 | Raw SYNOP text requires FM-12 decoding — complex binary-coded format |
| Identifiers | 3 | WMO station numbers — the international standard |
| Additive Value | 3 | Global coverage — any WMO station worldwide, irreplaceable for some regions |
| **Total** | **13/18** | |

## Notes

- OGIMET's unique value is global coverage — you can query any WMO station on Earth, including stations in countries that don't provide open APIs.
- The FM-12 SYNOP format is a legacy WMO encoding that requires a specialized decoder. Libraries like `pysynop` or `synop-decode` can parse it, but it's not trivial.
- The disclaimer is explicit: "The information in these pages must be taken as merely informative. No any critical mission should use this data."
- The site has been running since ~2005, which is both impressive (longevity) and concerning (single point of failure).
- OGIMET is heavily used by weather enthusiasts, amateur meteorologists, and researchers who need data from stations not covered by any open API.
- The CGI endpoint occasionally returns HTTP 500 errors — reliability is inconsistent.
- For production use, WMO GTS data should be sourced from official channels. But for research and supplementary data, OGIMET fills a unique niche.
