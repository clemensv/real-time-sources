# FMI — Finnish Meteorological Institute Open Data

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Finnish Meteorological Institute (Ilmatieteen laitos) — Open Data |
| **Operator**     | Finnish Meteorological Institute (FMI) |
| **URL**          | https://www.ilmatieteenlaitos.fi/ |
| **API Base**     | `https://opendata.fmi.fi/wfs` |
| **Coverage**     | Finland, Scandinavia, Arctic region |
| **Update Freq.** | Varies by product; 10-second to hourly for magnetic data |

## What It Does

FMI operates Finland's network of magnetic observatories (Sodankylä, Nurmijärvi, and others) and the "Auroras Now!" service — one of the most popular aurora monitoring tools in the Nordic countries. Their open data platform provides access to magnetic observations through a standard OGC Web Feature Service (WFS) API.

Finland's location under the auroral oval makes it an ideal place for geomagnetic monitoring. The Sodankylä Geophysical Observatory has been operating since 1914 — over a century of continuous magnetic field measurements.

FMI's open data portal provides a wide range of environmental observations including weather, marine, air quality, and geomagnetic data. The WFS API supports standard XML/GML queries.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| WFS GetCapabilities | ✅ 200 | Full OGC WFS 2.0 capabilities document (XML) |
| Open Data portal | ✅ 200 | Finnish-language portal with English docs |
| Auroras Now! page | ✅ 200 | HTML frameset (legacy design) |

### WFS API Structure

```
https://opendata.fmi.fi/wfs?request=GetFeature&storedquery_id=fmi::observations::magnetometer::simple&...
```

The WFS service uses OGC-standard stored queries. Relevant stored queries for geomagnetic data include:
- `fmi::observations::magnetometer::simple` — Magnetometer observations
- `fmi::observations::magnetometer::multipointcoverage` — Grid format

Parameters: `starttime`, `endtime`, `timestep`, `fmisid` (station ID).

Output is GML (Geography Markup Language) — standard but verbose XML. Simple feature responses can also be requested as CSV.

## Authentication & Licensing

- **Auth**: API key required (free registration at `https://ilmatieteenlaitos.fi/avoin-data`).
- **Rate Limits**: Documented in registration terms; reasonable for non-commercial use.
- **License**: Creative Commons Attribution 4.0 (CC BY 4.0). Open data.

## Integration Notes

The WFS/GML approach is standards-compliant but heavyweight compared to REST/JSON. The GML responses are verbose XML that requires specialized parsing. This is typical of European national met services that adopted OGC standards in the 2000s.

The free API key registration is straightforward. The stored query pattern means you need to know the query IDs in advance (the GetCapabilities response lists them all).

For aurora monitoring specifically, FMI provides:
- All-sky camera images (direct visual aurora observations)
- Magnetometer data (magnetic disturbance = proxy for aurora intensity)
- Riometer data (cosmic noise absorption = ionospheric disturbance indicator)

The "Auroras Now!" service at `aurorasnow.fmi.fi` is a legacy frameset-based website — functional but not API-friendly. The real data access is through the WFS.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | OGC WFS standard; documented but complex |
| **Data Freshness**           | 3     | 10-second magnetometer data; near-real-time |
| **Format / Schema Quality**  | 2     | GML/XML standard but verbose |
| **Auth / Access Simplicity** | 2     | Free API key registration; CC BY 4.0 |
| **Coverage Relevance**       | 2     | Finnish/Nordic; auroral zone specific |
| **Operational Reliability**  | 3     | National met service; century-old observatory network |
| **Total**                    | **14 / 18** | |

## Verdict

⚠️ **Maybe** — FMI provides genuine real-time magnetometer data from the auroral zone, which is scientifically valuable for space weather monitoring. The WFS/GML approach is technically sound but developer-unfriendly compared to REST/JSON sources (USGS, NOAA SWPC). The API key registration is a small hurdle. Recommended only if Nordic/auroral-zone ground magnetometer data is specifically needed — otherwise, NOAA SWPC and USGS provide more accessible global coverage.
