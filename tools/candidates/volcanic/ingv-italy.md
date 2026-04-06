# INGV Volcanic Monitoring (Istituto Nazionale di Geofisica e Vulcanologia)

**Country/Region**: Italy
**Publisher**: INGV — Istituto Nazionale di Geofisica e Vulcanologia (National Institute of Geophysics and Volcanology)
**API Endpoint**: Various — `https://www.ingv.it/`, `https://webapps.ingv.it/`
**Documentation**: https://www.ingv.it/en/
**Protocol**: Web portal, some REST endpoints
**Auth**: None (public web access)
**Data Format**: HTML, PDF (bulletins), some JSON
**Update Frequency**: Weekly volcanic bulletins; real-time seismic data
**License**: Italian open government data (varies by dataset)

## What It Provides

INGV monitors Italy's active volcanoes — including some of the most famous and closely watched volcanoes in the world:

- **Etna** — Europe's most active volcano
- **Vesuvius** — The iconic volcano near Naples
- **Stromboli** — Continuously erupting for centuries
- **Vulcano** — Aeolian Islands
- **Campi Flegrei** — Caldera system near Naples (currently showing bradyseism/unrest)

INGV provides:
- **Weekly volcanic bulletins** — Detailed monitoring summaries per volcano
- **Seismic monitoring data** — Earthquake catalogs near volcanic areas
- **Deformation data** — Ground movement measurements (tilt, GPS, InSAR)
- **Gas emission measurements** — SO2, CO2 monitoring
- **Webcam imagery** — Real-time camera feeds

## API Details

INGV does not expose a unified public REST API for volcanic data. Access points include:

**Volcanic bulletins:**
```
https://webapps.ingv.it/bulletins/volcanic-bulletins
```
(Was unreachable during testing — connection failure)

**INGV main site:**
```
https://www.ingv.it/en/monitoring-and-infrastructures/volcano-monitoring
```
(Returned 404 during testing — site may be restructuring)

**Earthquake catalog API (seismic data):**
```
https://webservices.ingv.it/fdsnws/event/1/query?format=geojson&minmag=0&lat=37.75&lon=14.99&maxradius=0.5
```
FDSN web services for earthquakes near volcanic areas are available and well-structured.

**Osservatorio Etneo/Vesuviano specific pages** may have additional data.

## Freshness Assessment

Weekly volcanic bulletins provide regular updates. Seismic data via FDSN is near-real-time. The main web portals had availability issues during testing, making it difficult to assess all products.

## Entity Model

**Volcanic bulletin:**
- Volcano name
- Reporting period
- Seismicity summary (event count, magnitudes)
- Deformation measurements
- Gas emissions data
- Alert status
- Narrative assessment

**Seismic event (via FDSN):**
- Event ID, timestamp
- Location (lat, lon, depth)
- Magnitude
- Quality metrics

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Weekly bulletins, near-real-time seismicity |
| Openness | 2 | Public access but fragmented, some endpoints down |
| Stability | 2 | Major institution but web infrastructure issues |
| Structure | 2 | FDSN seismic API is good; volcanic bulletins are PDF/HTML |
| Identifiers | 2 | Volcano names, FDSN event IDs for seismicity |
| Additive Value | 3 | Italy's volcanoes are globally significant |
| **Total** | **13/18** | |

## Notes

- INGV is one of the world's premier volcanological institutions. The quality of monitoring is outstanding.
- However, the web infrastructure for public data access appears to be undergoing changes or experiencing reliability issues.
- The FDSN earthquake web service is the most reliable programmatic access point — use it for volcanic seismicity near Italian volcanoes.
- Campi Flegrei is currently a major focus due to ongoing bradyseismic crisis (ground uplift and increased seismicity since 2024).
- For structured volcanic monitoring data, consider INGV's publications and bulletins as periodic ingest rather than real-time feed.
- The INGV/Osservatorio Etneo provides some of the most detailed Etna monitoring data in the world.
