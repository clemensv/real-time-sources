# HamQSL Solar/Propagation Indices

**Country/Region**: Global
**Publisher**: N0NBH (Paul Herrman)
**API Endpoint**: `https://www.hamqsl.com/solarxml.php`
**Documentation**: https://www.hamqsl.com/solar.html
**Protocol**: REST (XML)
**Auth**: None
**Data Format**: XML
**Update Frequency**: ~15-30 minutes (aggregates from NOAA SWPC and other sources)
**License**: Free for amateur radio / non-commercial use

## What It Provides

HamQSL aggregates solar and geomagnetic indices into a single, easy-to-consume XML endpoint tailored for ham radio operators. It combines solar flux (SFI), A-index, K-index, X-ray flux, sunspot number, proton flux, electron flux, and aurora activity into one call. It also includes HF propagation condition assessments per band (80m through 10m) for day and night paths.

This is the "dashboard in a single API call" for space weather as it affects radio propagation. Most ham radio logging software and propagation widgets consume this exact endpoint.

## API Details

- **Solar XML**: `GET /solarxml.php` — single XML document with all indices
- **Key fields**: `solarflux`, `aindex`, `kindex`, `xray`, `sunspots`, `protonflux`, `electonflux`, `aurora`, `normalization`
- **Band conditions**: `calculatedconditions` → per-band `band` elements with `name`, `time` (day/night), and condition (Good/Fair/Poor)
- **Signal noise**: `signalnoise` with per-band S-meter readings
- **Updated timestamp**: `updated` field with UTC datetime
- **No auth required**: Public XML endpoint
- **Single call**: All data in one request — no pagination or multiple calls needed

## Freshness Assessment

Data is refreshed every 15-30 minutes, aggregating from NOAA SWPC and other sources. The `updated` field shows the exact refresh time.

Confirmed live: returned data updated 2026-04-06 11:14 GMT. Solar flux 118, K-index 2, sunspots 99, X-ray B6.7, proton flux 297 (elevated — consistent with the SWPC electron flux alert).

## Entity Model

- **Solar indices**: `solarflux` (SFU), `aindex`, `kindex`, `xray` (GOES X-ray class), `sunspots`, `protonflux` (pfu), `electonflux` (pfu)
- **Geomagnetic**: `aurora` (activity level), `normalization`
- **Band conditions**: Band name (80m-10m), time-of-day, qualitative condition, S/N reading
- **Source**: N0NBH aggregation, `source` URL field

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 15-30 minute refresh, aggregated from upstream sources |
| Openness | 3 | No auth, public XML endpoint |
| Stability | 2 | Single-operator service; widely used but not institutionally backed |
| Structure | 2 | XML format (not JSON, but well-structured and small) |
| Identifiers | 2 | Timestamps; band names; no unique event IDs |
| Additive Value | 2 | Convenient aggregation of propagation-relevant indices in one call |
| **Total** | **13/18** | |

## Notes

- Confirmed live: all indices returned fresh data consistent with current space weather conditions.
- This is essentially a convenience aggregation — all the underlying data comes from NOAA SWPC.
- The band condition assessments (Good/Fair/Poor per band) are derived calculations, not raw measurements.
- XML format is small (~2KB) and easy to parse.
- Extremely widely used in the ham radio community — de facto standard for propagation widgets.
- Single point of failure: one operator maintains this. If N0NBH goes down, hundreds of ham radio apps lose their propagation display.
- Pairs with DSCOVR (raw solar wind data upstream of this aggregation) and PSKReporter/RBN (observed propagation vs. these predictions).
