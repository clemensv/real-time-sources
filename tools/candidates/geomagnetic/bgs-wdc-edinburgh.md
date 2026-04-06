# BGS World Data Centre — Edinburgh

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | World Data Centre for Geomagnetism (Edinburgh) — British Geological Survey |
| **Operator**     | British Geological Survey (BGS), part of UKRI |
| **URL**          | https://wdc.bgs.ac.uk/dataportal/ |
| **Geomag Home**  | https://geomag.bgs.ac.uk/ |
| **Coverage**     | Global (World Data Centre — archives data from worldwide observatories) |
| **Update Freq.** | Archives: monthly to annual; BGS observatories: near-real-time |

## What It Does

The BGS operates one of the world's longest-running magnetic observatory networks (since 1843 at Greenwich, now at Eskdalemuir, Hartland, and Lerwick in the UK) and hosts the World Data Centre for Geomagnetism in Edinburgh — one of the primary global archives for geomagnetic data.

The WDC collects, validates, and distributes definitive geomagnetic data from observatories worldwide. It's one of several ICSU (now ISC) World Data Centres and works alongside WDC Kyoto (indices) and WDC Copenhagen (now DTU Space).

BGS also provides the geomagnetic field model used for UK navigation and surveys, and contributes to the World Magnetic Model (WMM) used by NATO and civilian navigation worldwide.

## Endpoints Probed

| Endpoint | Status | Notes |
|----------|--------|-------|
| WDC Data Portal | ✅ 200 | Modern Angular web application |
| `/dataportal/api/observations?...` | ✅ 200 | Returns HTML (SPA); not a REST API |
| Various BGS data service URLs | ❌ 404 | Multiple attempted API patterns failed |
| INTERMAGNET GIN (BGS-hosted) | ❌ 404 | GINServices endpoint not responding |

### The API Problem

BGS hosts the WDC data portal as a modern single-page application (Angular-based), but the backend data API is not publicly documented or accessible via direct URL. The SPA loads data through internal API calls that aren't designed for external consumption.

The `geomag.bgs.ac.uk/data_service/` and `imag-data.bgs.ac.uk/GIN/` endpoints that appear in older documentation all returned 404 — suggesting infrastructure changes or API deprecation.

BGS does provide data download tools through the portal's web interface, including:
- Hourly, daily, and annual mean values
- Magnetic indices (aa, Aa, Ap)
- Observatory definitive data in IAGA-2002 format
- Historical digitized records

But these are interactive web tools, not programmable APIs.

## Authentication & Licensing

- **Auth**: None for the web portal; no public API found.
- **License**: UK Open Government Licence (OGL). BGS data is freely available with attribution.

## Integration Notes

The BGS/WDC Edinburgh data is scientifically important — the aa index (longest continuous geomagnetic index, since 1868) and definitive observatory data are gold-standard products. But the lack of a working public API makes programmatic integration difficult.

Options:
1. **Use INTERMAGNET** — BGS observatories contribute to INTERMAGNET, which has a documented HAPI API
2. **Use NOAA SWPC** — Key derived indices (Kp, Dst) are available through NOAA
3. **Monitor portal updates** — BGS may be rebuilding their data services infrastructure

For UK magnetic data specifically, the INTERMAGNET HAPI API accessing stations ESK (Eskdalemuir), HAD (Hartland), and LER (Lerwick) is the most reliable programmatic path.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | No working public API; web portal only |
| **Data Freshness**           | 2     | Near-real-time for BGS stations (via INTERMAGNET) |
| **Format / Schema Quality**  | 2     | IAGA-2002 format standard; but no API to serve it |
| **Auth / Access Simplicity** | 2     | OGL license; but no programmable access |
| **Coverage Relevance**       | 3     | World Data Centre; global archive |
| **Operational Reliability**  | 3     | BGS/UKRI; running since 1843 |
| **Total**                    | **13 / 18** | |

## Verdict

⏭️ **Skip** — Scientifically important archive but no working public API. BGS magnetic data is accessible through INTERMAGNET (already documented) and key indices through NOAA SWPC (already documented). The WDC Edinburgh is the authoritative archive, but for real-time integration the data flows through other channels that have better APIs. Revisit if BGS launches a new data service API.
