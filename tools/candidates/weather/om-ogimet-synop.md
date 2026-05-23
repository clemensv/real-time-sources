# WMO SYNOP Observations (Oman Stations via OGIMET)

- **Country/Region**: Global (filter for Oman WMO stations)
- **Endpoint**: `https://www.ogimet.com/cgi-bin/getsynop` (SYNOP decoder), `https://www.ogimet.com/cgi-bin/gsynres` (recent observations)
- **Protocol**: HTTP GET (text-based responses)
- **Auth**: None
- **Format**: Plain text (FM-12 SYNOP coded format or decoded HTML tables)
- **Freshness**: Hourly (standard WMO GTS exchange intervals)
- **Docs**: https://www.ogimet.com/
- **Score**: 9/18

## Overview

**OGIMET** is a public service operated by volunteers that archives and decodes meteorological observations exchanged via the **WMO Global Telecommunication System (GTS)**. It provides access to:
- **SYNOP** land surface observations (FM-12 SYNOP coded reports from WMO member stations)
- **METAR** aviation observations (parsed)
- **TEMP** upper-air soundings (radiosondes)
- **BUOY** maritime buoy observations

For Oman, OGIMET archives observations from WMO-registered weather stations operated by the Directorate General of Meteorology (DGMET). Known Oman WMO station codes (WMO block 41, Oman):
- **41256** — Muscat (Seeb International Airport, OOMS)
- **41316** — Salalah Airport (OOSA)
- **41240** — Khasab (Musandam Peninsula)
- **41112** — Sohar
- **41184** — Sur
- **41260** — Masirah Island (strategic location for Arabian Sea weather)

SYNOP reports include:
- Temperature, dewpoint (°C)
- Pressure (hPa, sea-level and station)
- Wind direction and speed (degrees, m/s)
- Visibility (meters)
- Present weather (fog, rain, dust, sandstorm, etc.)
- Cloud cover and height
- Precipitation accumulation (mm, past 6/12/24 hours)

## Endpoint Analysis

**Accessible but HTML-based** — OGIMET's SYNOP query interface returns observations in either:
1. **Decoded HTML tables** (human-readable)
2. **Raw SYNOP coded format** (FM-12 five-figure groups, requires decoding)

Sample query (Muscat station 41256, recent 24 hours):
```
GET https://www.ogimet.com/cgi-bin/gsynres?ind=41256&lang=en&decoded=yes&ndays=1&ano=2026&mes=05&day=23&hora=06
```

This returns an HTML table with:
```
Station  Date/Time        Temp  Dewp  Wind   Pres   Visibility  Weather
41256    2026-05-23 06:00  39°C  14°C  070/05  1006mb  8000m      NSC (no significant clouds)
```

Raw SYNOP code for the same observation (if `decoded=no`):
```
AAXX 23064
41256 21506 01604 10390 20140 30071 40062 58005 80000
```

Decoding the SYNOP manually:
- `AAXX 23064` — report type (AAXX = SYNOP land), day 23, hour 06 UTC
- `41256` — WMO station identifier (Muscat)
- `21506` — wind 070° at 5 m/s
- `10390` — temperature 39.0°C
- `20140` — dewpoint 14.0°C
- `30071` — pressure 1007.1 hPa (station level, needs correction for sea level)
- `40062` — pressure 1006.2 hPa (sea level)
- `58005` — additional indicators
- `80000` — cloud group (NSC = no significant clouds)

### Challenges with OGIMET

- **Not a formal API**: OGIMET is a volunteer service with no official API documentation, SLA, or versioning. Query parameters are discovered by trial-and-error or reading user forums.
- **HTML scraping required**: Decoded output is HTML tables (not JSON). Raw SYNOP output requires implementing a FM-12 SYNOP decoder (non-trivial).
- **Irregular availability**: Some WMO stations report hourly, some every 3 or 6 hours, some only during synoptic times (00, 06, 12, 18 UTC). Oman stations typically report hourly but coverage can be spotty during equipment failures.
- **Duplication with METARs**: For airport stations (OOMS Muscat, OOSA Salalah), **SYNOP and METAR report the same physical observations** but in different formats. METAR (via Aviation Weather API) is easier to parse and already explored as a candidate.
- **Delay**: OGIMET archives WMO GTS data, which has a delay (typically 10-30 minutes from observation time to GTS distribution to OGIMET ingestion). Not as fast as direct METAR from Aviation Weather API.

## Integration Notes

- **Value-add over METARs**: SYNOP provides observations from **non-airport stations** that don't issue METARs:
  - **Masirah Island** (41260) — remote island in Arabian Sea, important for cyclone tracking and marine weather
  - **Khasab** (41240) — northern Musandam Peninsula, captures Gulf of Oman maritime weather
  - **Sohar, Sur** — coastal/inland stations not at international airports
  
  These stations are **not covered by METAR feeds**, so SYNOP is the only public source for their observations.

- **SYNOP decoding**: Implementing a full FM-12 SYNOP decoder is complex (100+ page WMO spec). Alternatives:
  - Use OGIMET's decoded HTML output (scraping required)
  - Use a third-party SYNOP library (e.g., `pysynop` for Python, but maintenance is sporadic)
  - Only ingest a **subset** of SYNOP fields (temperature, pressure, wind) and skip complex groups (cloud layers, special phenomena)

- **Overlap with Aviation Weather API**: For OOMS (Muscat) and OOSA (Salalah), SYNOP and METAR provide **redundant data** from the same sensors. METARs are easier to parse (well-documented format, JSON API available). SYNOP's advantage is coverage of **non-airport stations**.

- **Global vs. Oman-specific**: OGIMET serves all WMO stations worldwide. A bridge for Oman SYNOP would be a **regional filter** of a global data source. Better approach: build a **global SYNOP bridge** (all WMO stations) with geographic filtering, similar to the USGS earthquake approach.

- **Keying strategy**: Use WMO station identifier (e.g., `41256` for Muscat) as CloudEvents subject and Kafka key. Station metadata (name, lat/lon, elevation) is available from WMO Publication No. 9 Volume A (station catalog).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly for most Oman stations (some 3-hourly or synoptic-times-only) |
| Openness | 2 | Public access (no auth), but no formal API, OGIMET is volunteer-run |
| Stability | 1 | OGIMET has operated for 20+ years but is a volunteer service (no SLA, no versioning) |
| Structure | 1 | HTML scraping or FM-12 SYNOP coded format (both require parsing effort) |
| Identifiers | 3 | WMO station IDs are globally standardized and permanent |
| Additive value | 0 | Overlaps with METAR for airports; non-airport stations (Masirah, Khasab) are additive but niche |

**Verdict**: ⏭️ Reference

**Rationale**: SYNOP observations via OGIMET provide access to **non-airport weather stations in Oman** (Masirah Island, Khasab, Sohar, Sur) that don't issue METARs. These stations are valuable for regional weather coverage (Arabian Sea maritime conditions, interior desert, northern Musandam).

However:
- **Parsing complexity**: OGIMET is not a formal API; HTML scraping or SYNOP decoding required.
- **Overlap with METARs**: Airport stations (OOMS, OOSA) already covered by Aviation Weather API.
- **Global scope**: SYNOP is a **global data source** (all WMO stations). If the repo builds a SYNOP bridge, it should be **global** (or at least regional for Middle East/Arabian Peninsula), not Oman-only.

**Recommended approach**:
1. **Prioritize Aviation Weather API METARs** (OOMS, OOSA, OOSN, OOTH) for Oman airport weather — these are easier to parse and already JSON-formatted.
2. If the repo wants **global weather station coverage**, build a **global SYNOP bridge** using OGIMET or another WMO GTS aggregator. This would cover Oman's non-airport stations (Masirah, Khasab) as a side effect of global coverage.
3. If the repo wants **Oman-specific non-airport weather**, contact DGMET directly to inquire about a real-time API for their station network. SYNOP via OGIMET is a fallback but not ideal.

**Do not build an Oman-only SYNOP bridge** — the data source is global, and the effort to parse SYNOP (or scrape OGIMET HTML) is the same whether filtering for 6 Oman stations or 10,000 global stations. Scope it globally if built.
