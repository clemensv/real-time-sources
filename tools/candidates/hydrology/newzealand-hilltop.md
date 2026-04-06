# New Zealand — Regional Council Hilltop Servers

**Country/Region**: New Zealand
**Publisher**: Regional Councils (e.g., Greater Wellington Regional Council — GWRC)
**API Endpoint**: `https://hilltop.gw.govt.nz/Data.hts` (GWRC example)
**Documentation**: https://www.hilltop.co.nz/ (vendor), individual council documentation varies
**Protocol**: REST (Hilltop Server protocol)
**Auth**: None
**Data Format**: XML
**Update Frequency**: Every 5 minutes (telemetered stations)
**License**: Varies by council — generally open/CC BY

## What It Provides

Real-time water level (stage), flow (discharge), rainfall, and water quality data from hydrometric stations across New Zealand. Each regional council operates its own Hilltop server instance. The Greater Wellington Regional Council (GWRC) server alone provides hundreds of monitoring sites covering rivers, streams, groundwater, and water-use take points.

## API Details

Hilltop Server exposes a standardized XML-based API. Key operations:

### Site List
```
GET https://hilltop.gw.govt.nz/Data.hts?Service=Hilltop&Request=SiteList&Location=LatLong
```
Returns XML with site names and coordinates.

### Measurement List (per site)
```
GET https://hilltop.gw.govt.nz/Data.hts
  ?Service=Hilltop
  &Request=MeasurementList
  &Site=Hutt%20River%20at%20Taita%20Gorge
```
Returns XML listing available measurements (Stage, Flow, derived measurements) with metadata including units, date ranges, and formats.

### Get Data (time series)
```
GET https://hilltop.gw.govt.nz/Data.hts
  ?Service=Hilltop
  &Request=GetData
  &Site=Hutt%20River%20at%20Taita%20Gorge
  &Measurement=Stage
  &TimeInterval=P1D
```

Sample response:
```xml
<Hilltop>
  <Agency>GWRC</Agency>
  <Measurement SiteName="Hutt River at Taita Gorge">
    <DataSource Name="Water Level" NumItems="1">
      <TSType>StdSeries</TSType>
      <Interpolation>Instant</Interpolation>
      <ItemInfo ItemNumber="1">
        <ItemName>Stage</ItemName>
        <Units>mm</Units>
      </ItemInfo>
    </DataSource>
    <Data DateFormat="Calendar" NumItems="1">
      <E><T>2026-04-06T00:05:00</T><I1>24450</I1></E>
      <E><T>2026-04-06T00:10:00</T><I1>24450</I1></E>
    </Data>
  </Measurement>
</Hilltop>
```

### Known Hilltop Server Instances

| Council | URL |
|---------|-----|
| Greater Wellington (GWRC) | `https://hilltop.gw.govt.nz/Data.hts` |
| Environment Canterbury | `https://data.ecan.govt.nz/data/...` |
| Horizons (Manawatū-Whanganui) | `https://hilltop.horizons.govt.nz/...` |
| Waikato Regional Council | Various endpoints |
| Others | Many NZ regional councils use Hilltop |

## Freshness Assessment

Probed 2026-04-06: Hutt River at Taita Gorge returned 5-minute stage data with the latest reading at 2026-04-06T22:10:00 NZST — effectively real-time. Data extends back to 1979 for this station. The `MeasurementList` confirmed active data through 2026-04-06.

## Entity Model

- **Site Name**: Descriptive string, e.g., `Hutt River at Taita Gorge` — functions as the primary identifier
- **Measurement Name**: `Stage`, `Flow`, `Water Temperature`, etc.
- **Agency**: Council abbreviation, e.g., `GWRC`
- **Kafka key**: `{agency}/sites/{url_encoded_site_name}`
- **CloudEvents subject**: `{agency}/sites/{url_encoded_site_name}`

Site names are stable but are human-readable strings rather than numeric codes. URL encoding is required.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute intervals, effectively real-time |
| Openness | 3 | No auth, open access |
| Stability | 2 | Per-council servers; Hilltop is a commercial product, widely deployed |
| Structure | 2 | XML format, custom Hilltop protocol (not a standard like OGC) |
| Identifiers | 2 | Site names are strings (not numeric codes), but stable within each council |
| Additive Value | 3 | New Zealand not covered by any existing source |
| **Total** | **15/18** | |

## Notes

- Hilltop Server is a commercial product by Hilltop Software (NZ) widely used by NZ regional councils, but also in Australia and other countries
- The API is not a standard (REST/OGC) but follows a consistent pattern across all council instances
- Site names use human-readable format with spaces and special characters — need URL encoding
- The `TimeInterval` parameter uses ISO 8601 durations (e.g., `P1D` for last day, `P7D` for last week)
- Each council maintains its own independent server — a comprehensive NZ solution would need to poll multiple servers
- The WaterUse.hts endpoint (separate from Data.hts) provides water-use consent/take data
- Stage values are in mm (millimetres), Flow in m³/sec
- Virtual Measurements (derived values like 7-day moving mean flow) are also available
- Long historical records available (some stations back to the 1970s)
