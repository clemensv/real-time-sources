# Switzerland NADAM (NADos Automatisches Messnetz)

**Country/Region**: Switzerland
**Publisher**: National Emergency Operations Centre (NAZ / Nationale Alarmzentrale), ENSI, and MeteoSwiss
**API Endpoint**: `https://www.naz.ch/en/aktuell/tagesmittelwerte.html` (portal); `https://www.naz.ch/api/data/nadam` (unconfirmed)
**Documentation**: https://www.naz.ch/
**Protocol**: Web portal (JavaScript-rendered); data shared via EURDEP
**Auth**: None (public portal)
**Data Format**: HTML/JavaScript (dynamically loaded); data contributed to EURDEP
**Update Frequency**: Continuous (10-minute measurement intervals), daily averages published
**License**: Swiss government open data

## What It Provides

Switzerland operates the NADAM network (Netz für automatische Dosisleistungsüberwachung — Automatic Dose Rate Monitoring Network) consisting of approximately 76 monitoring stations across the country. The network is operated by the NAZ in cooperation with ENSI (Swiss Federal Nuclear Safety Inspectorate) and MeteoSwiss.

The network provides:

- **Ambient gamma dose rate** — Continuous measurement in nSv/h
- **Daily averages** — Published on the NAZ website
- **Measurement results** — Historical data accessible through the portal
- **Specialized monitoring** — Additional dense networks around Swiss nuclear power plants (Beznau, Gösgen, Leibstadt, Mühleberg)

## API Details

### NAZ Web Portal

The portal at `https://www.naz.ch/` provides daily average values and measurement results. However, the pages are rendered by JavaScript — both `tagesmittelwerte.html` and `messresultate.html` returned "Loading..." responses, indicating the content is dynamically loaded client-side.

### Attempted API Endpoints

- `https://www.naz.ch/api/data/nadam` — Returned "Loading..." (JavaScript-rendered page, not an API)
- `https://www.naz.ch/api/data/nadam/stations` — Same JavaScript-rendered response
- `https://data.ensi.ch` — Connection failed
- `https://www.raddata.ch` — Connection failed

### EURDEP Access

Swiss stations contribute to EURDEP. Accessible via the WFS with "CH" prefix:

```
GET https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0
    &request=GetFeature
    &typeName=opendata:eurdep_latestValue
    &outputFormat=application/json
    &CQL_FILTER=id LIKE 'CH%'
```

## Freshness Assessment

The NAZ portal is live but JavaScript-rendered — data is not directly accessible without executing JavaScript. Swiss monitoring data flows to EURDEP and was confirmed there (2026-04-06). The NADAM network provides 10-minute interval data internally, with daily averages published on the web portal.

## Entity Model

- **Station** — NADAM monitoring station with ID (CHxxxx), coordinates, name, elevation.
- **Measurement** — Ambient gamma dose rate in nSv/h, 10-minute intervals, aggregated to daily averages.
- **Nuclear Power Plant Zone** — Additional monitoring networks around Swiss NPPs.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | 10-minute measurement intervals, daily averages published |
| Openness | 1 | JavaScript-rendered portal, no confirmed REST API |
| Stability | 3 | Swiss government infrastructure (NAZ/ENSI) |
| Structure | 0 | No programmatic API confirmed; JS-rendered portal |
| Identifiers | 2 | Station IDs in CHxxxx format via EURDEP |
| Additive Value | 1 | ~76 stations, small country, accessible via EURDEP |
| **Total** | **10/18** | |

## Notes

- Switzerland's NADAM data is best accessed through EURDEP rather than directly.
- The NAZ website uses heavy JavaScript rendering — even the API-like URLs (`/api/data/nadam`) appear to be SPA routes rather than REST endpoints.
- ENSI (the nuclear safety regulator) may have additional data endpoints for power plant-specific monitoring, but `data.ensi.ch` was unreachable during testing.
- Switzerland also participates in the European Radiological Data Exchange Platform (EURDEP) and contributes data to the IAEA.
- The relatively small number of stations (76) across a small, mountainous country means the network provides good spatial coverage for Switzerland's size.
