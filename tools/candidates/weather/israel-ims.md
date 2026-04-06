# Israel Meteorological Service (IMS) — Real-Time Observations

**Country/Region**: Israel
**Publisher**: Israel Meteorological Service (שירות המטאורולוגי הישראלי)
**API Endpoint**: `https://ims.gov.il/sites/default/files/ims_data/xml_files/imslasthour.xml`
**Documentation**: https://ims.gov.il/en/ObsArchive (observation archive page)
**Protocol**: HTTP file polling (XML)
**Auth**: None (anonymous access)
**Data Format**: XML
**Update Frequency**: 10-minute intervals (6 observations per hour per station)
**License**: Israeli government public data

## What It Provides

The IMS publishes a single XML file containing the last hour of observations from all active weather stations across Israel. The file updates every 10 minutes and provides a rich set of meteorological parameters.

Israel's network covers a remarkably diverse climate range in a small area — from Mediterranean coast to Dead Sea desert, Negev arid zone to snow-capable Golan Heights. The monitoring network is dense relative to the country's size.

Parameters per observation:
- **Temperature**: Current (TD), maximum (TDmax), minimum (TDmin), ground temperature (TG)
- **Humidity**: Relative humidity (RH)
- **Pressure**: Station-level barometric pressure (BP)
- **Radiation**: Global (Grad), direct (NIP), diffuse (DiffR) — valuable for solar energy applications
- **Precipitation**: Rainfall accumulation (Rain)
- **Wind**: Speed (WS), direction (WD), gust speed (WSmax), gust direction (WDmax), 1-minute max (WS1mm), 10-minute max (Ws10mm), wind direction standard deviation (STDwd)

## API Details

The data is served as a static XML file that gets regenerated every 10 minutes:

```
GET https://ims.gov.il/sites/default/files/ims_data/xml_files/imslasthour.xml
```

### Probed Response (live, April 6, 2026, 23:10 UTC)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<RealTimeData>
  <HebrewVariablesNames>
    <TD>טמפרטורה</TD>
    <RH>לחות יחסית</RH>
    <WS>מהירות הרוח</WS>
    <!-- ... 15+ parameters ... -->
  </HebrewVariablesNames>
  <Observation>
    <stn_name>AVNE ETAN</stn_name>
    <stn_num>2</stn_num>
    <time_obs>2026-04-06T23:10:00</time_obs>
    <RH>93</RH>
    <TD>9.6</TD>
    <TDmax>9.7</TDmax>
    <TDmin>9.6</TDmin>
    <TG>9.9</TG>
    <Rain>0</Rain>
    <WD>90</WD>
    <WS>0.5</WS>
    <WSmax>0.8</WSmax>
    <STDwd>10.9</STDwd>
  </Observation>
  <!-- Multiple stations, 6 observations each (10-min intervals over 1 hour) -->
</RealTimeData>
```

Key observations from probe:
- Multiple stations reporting (AVNE ETAN, BET ZAYDA, ZEMAH, and more)
- 6 observation records per station (every 10 minutes for the past hour)
- Each record has ~18 parameters
- Timestamps in ISO 8601 format (local Israel time)
- Empty elements for unavailable parameters (not all stations have all sensors)
- Station identified by `stn_num` (numeric) and `stn_name` (text)

## Freshness Assessment

Excellent. Data was fresh within 10 minutes at time of probe. The 10-minute reporting interval is among the highest temporal resolution for freely available weather APIs. The radiation parameters (global, direct, diffuse) are particularly valuable for solar energy forecasting — Israel's solar industry is world-class.

## Entity Model

- **Station**: `stn_num` (numeric ID), `stn_name` (text name)
- **Observation**: Timestamped at 10-minute intervals; ~18 meteorological parameters
- **Parameter**: Variable code (TD, RH, WS, etc.) with Hebrew name mapping in header
- No WMO station numbers visible — uses internal IMS numbering

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute observations; confirmed live |
| Openness | 3 | No auth, anonymous HTTP access |
| Stability | 2 | Government service; static file URL may change without notice |
| Structure | 2 | Well-formed XML but needs parsing; Hebrew parameter headers; no JSON alternative |
| Identifiers | 2 | Internal station numbers; no WMO codes in feed |
| Additive Value | 3 | Only source for Israeli weather obs; unique climate diversity; solar radiation data |
| **Total** | **15/18** | |

## Integration Notes

- Poll every 10 minutes to match the observation cycle
- XML parsing straightforward — flat structure with repeated `<Observation>` elements
- Station dedup by `stn_num` + `time_obs`
- Hebrew variable names in header can be mapped to English via a static lookup
- The solar radiation parameters (Grad, NIP, DiffR) are rare in free weather APIs — high value for energy sector
- Consider supplementing with IMS forecast data if available
- Israel's timezone is IST (UTC+2) with daylight saving — timestamps need careful handling
- CloudEvents mapping: one event per station-observation, or batch per file refresh
- No CORS headers expected — server-side polling required

## Verdict

A clean, high-frequency, no-auth weather data source from a region with zero current coverage in the repository. The 10-minute resolution and solar radiation parameters are standout features. The XML format requires parsing but the structure is simple. Fills a critical Middle East gap.
