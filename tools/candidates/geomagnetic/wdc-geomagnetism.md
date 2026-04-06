# WDC for Geomagnetism (Kyoto & Edinburgh)

**Country/Region**: Global
**Publisher**: World Data Centre for Geomagnetism, Kyoto (Kyoto University) & Edinburgh (BGS)
**API Endpoint**: `https://wdc.kugi.kyoto-u.ac.jp/` (Kyoto); `https://www.bgs.ac.uk/geomagnetism/` (Edinburgh)
**Documentation**: https://wdc.kugi.kyoto-u.ac.jp/wdc/Sec3.html
**Protocol**: HTTP (file download, web forms) / HAPI (via INTERMAGNET BGS)
**Auth**: None (most data); contact required for quicklook data use
**Data Format**: IAGA-2002 (text), WDC format, GeoJSON, various
**Update Frequency**: Indices: hourly to monthly; Observatory data: varies
**License**: ICSU-WDS Data Sharing Principles (free for scientific use); no commercial use without permission

## What It Provides

The World Data Centres for Geomagnetism are ICSU-designated archives for geomagnetic data. WDC Kyoto is the primary centre for geomagnetic indices: Dst (disturbance storm time), AE (auroral electrojet), ASY/SYM (asymmetric/symmetric disturbance), and SQ (solar quiet). WDC Edinburgh (BGS) hosts the INTERMAGNET data portal and provides access to global observatory data.

These centres maintain the definitive historical record of Earth's magnetic field variations, with some data series going back to the 1800s. They are the authoritative source for research-grade geomagnetic indices.

## API Details

- **Kyoto Dst**: `https://wdc.kugi.kyoto-u.ac.jp/dst_realtime/` (real-time provisional), `https://wdc.kugi.kyoto-u.ac.jp/dst_final/` (final)
- **Kyoto AE**: `https://wdc.kugi.kyoto-u.ac.jp/ae_realtime/` (real-time provisional)
- **Data download**: Web forms for selecting time range, observatory, and format
- **NOAA mirror**: Kyoto Dst is mirrored at `https://services.swpc.noaa.gov/products/kyoto-dst.json` (JSON, no auth)
- **BGS INTERMAGNET HAPI**: `https://imag-data.bgs.ac.uk/GIN_V1/hapi/` (covered in INTERMAGNET document)
- **Formats**: IAGA-2002 text, WDC format (fixed-width), various custom formats per index
- **DOIs**: AE, Dst, ASY/SYM indices published with DOIs for citability

## Freshness Assessment

Real-time provisional Dst and AE indices are available with delays of hours to days. Final (definitive) indices are published with delays of months to years. The NOAA SWPC mirror provides near-real-time Kyoto Dst in JSON format. For operational use, the NOAA mirror is more accessible than Kyoto's web interface.

## Entity Model

- **Dst Index**: Hourly disturbance storm time index (nT), measuring ring current intensity
- **AE Index**: Auroral electrojet index (nT) with AU (upper) and AL (lower) envelopes, measuring auroral activity
- **ASY/SYM**: Asymmetric and symmetric disturbance indices at 1-minute resolution
- **Observatory**: WDC catalog of global geomagnetic observatories with metadata

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Real-time provisional available but delayed; definitive indices lag by months |
| Openness | 2 | Free for science; no commercial use; contact required for quicklook data |
| Stability | 3 | ICSU-designated archives; running since 1957 (IGY) |
| Structure | 1 | Legacy formats (fixed-width text, web forms); no modern REST API |
| Identifiers | 2 | Standard index names; observatory codes; DOIs for datasets |
| Additive Value | 2 | Authoritative indices; but NOAA SWPC provides easier access for key products |
| **Total** | **11/18** | |

## Notes

- For practical integration, use the NOAA SWPC mirrors for Dst and other indices rather than scraping the Kyoto web interface.
- The WDCs are research archives, not real-time data services — they prioritize accuracy over timeliness.
- The Dst index is crucial for quantifying geomagnetic storm intensity and is widely used in space weather research.
- AE index is the primary measure of auroral/substorm activity.
- INTERMAGNET (via BGS HAPI) provides the modern API access pattern for the underlying observatory data.
- Historical index data going back decades is the unique value proposition — no other source has this depth.
