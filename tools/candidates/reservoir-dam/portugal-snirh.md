# Portugal SNIRH — Dam and Reservoir Data

**Country/Region**: Portugal (~60 major dams + hundreds of smaller dams)
**Publisher**: APA (Agência Portuguesa do Ambiente) / SNIRH (Sistema Nacional de Informação de Recursos Hídricos)
**API Endpoint**: `https://snirh.apambiente.pt/` (web portal)
**Documentation**: https://snirh.apambiente.pt/
**Protocol**: Web portal; some WMS/WFS geospatial services
**Auth**: None for public access (some data requires free registration)
**Data Format**: HTML, CSV downloads, WMS/WFS
**Update Frequency**: Near real-time for telemetric stations; daily for some; monthly for others
**License**: Portuguese government open data

## What It Provides

SNIRH is Portugal's national water resources information system, providing:

- **Reservoir storage** (hm³ and percentage) for major Portuguese dams
- **River flow** and water levels at gauging stations
- **Precipitation** from rain gauges
- **Groundwater levels** from piezometers
- **Water quality** data from monitoring stations

Portugal has ~260 large dams, many critical for hydroelectric power (which provides ~25-30% of Portugal's electricity) and irrigation in the dry Alentejo region. Major reservoirs include Alqueva (Europe's largest artificial lake by surface area), Castelo de Bode (Lisbon's water supply), and Aguieira.

The system includes telemetric stations reporting in near-real-time and conventional stations with less frequent updates.

## API Details

The SNIRH portal returned 403 during testing, but it's normally browser-accessible. Access methods:

- **Web portal**: Interactive map and station selection at `snirh.apambiente.pt`
- **Data downloads**: CSV/Excel exports per station and parameter
- **WMS/WFS**: Geospatial services may be available through the GIS components

The portal allows querying by:
- Station type (hydrometric, meteorological, reservoir, water quality)
- River basin (Douro, Tejo, Guadiana, Mondego, etc.)
- Parameter (storage, flow, rainfall, temperature)
- Time period

## Freshness Assessment

Moderate. Telemetric stations report near-real-time data. However, the portal can be slow and data availability varies by station. Reservoir storage data is typically updated daily or weekly depending on the dam operator.

## Entity Model

- **Station**: code, name, type, river basin, lat/lon, altitude, operator
- **Reservoir**: name, river, capacity (hm³), dam height, purpose
- **Observation**: timestamp, parameter, value, unit, quality flag
- **River Basin**: name, area, major rivers, major reservoirs

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time for telemetric stations; daily/weekly for reservoirs |
| Openness | 2 | Public access; some data requires registration; no formal REST API |
| Stability | 2 | Government agency; portal sometimes slow/unreliable |
| Structure | 1 | Web portal with downloads; potential WFS but not well-documented |
| Identifiers | 2 | Station codes; river basin classification; links to WISE |
| Additive Value | 2 | Iberian Peninsula coverage; Alqueva (largest EU artificial lake); complements Spain SAIH |
| **Total** | **11/18** | |

## Notes

- Portugal and Spain share several major river basins (Douro/Duero, Tejo/Tajo, Guadiana) — SNIRH complements the Spanish SAIH for complete Iberian water resource monitoring.
- Alqueva Dam on the Guadiana is the largest artificial lake in the EU by surface area — a showcase Portuguese water infrastructure project.
- Hydropower is a major part of Portugal's renewable energy mix, making reservoir data economically relevant.
- The Albufeira Convention between Portugal and Spain governs transboundary water flows — monitoring data from both countries is needed for compliance.
- Web scraping is likely necessary for automated access — the portal is ASP-based with form-based queries.
- Consider combining with IPMA (Portuguese Met Service) for rainfall data to complete the water cycle picture.
