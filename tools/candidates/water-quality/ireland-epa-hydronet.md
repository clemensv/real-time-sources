# Irish EPA HydroNet — Water Quality Monitoring

**Country/Region**: Ireland
**Publisher**: Environmental Protection Agency (EPA), Ireland
**API Endpoint**: `https://epawebapp.epa.ie/hydronet/` (HydroNet portal); `https://epa.ie/our-services/monitoring--assessment/freshwater--marine/`
**Documentation**: https://www.epa.ie/our-services/monitoring--assessment/freshwater--marine/
**Protocol**: Web portal; possible WISKI/Kisters backend
**Auth**: Unknown (likely none for public data)
**Data Format**: HTML (portal), CSV (downloads)
**Update Frequency**: Mix of real-time (continuous monitors) and periodic (discrete sampling)
**License**: Irish Government open data

## What It Provides

The Irish EPA operates comprehensive water quality monitoring across Ireland, covering:

- **River water quality**: ~3,000+ monitoring stations on ~13,000 river sites
- **Lake water quality**: monitoring of significant lakes
- **Transitional and coastal waters**: estuarine and marine monitoring
- **Groundwater quality**: borehole monitoring network

Parameters monitored:
- Physico-chemical: temperature, pH, dissolved oxygen, conductivity, BOD, ammonia, nutrients (N, P)
- Biological: Q-value (macroinvertebrate biotic index — Ireland's signature water quality metric), diatoms, fish
- Chemical: priority substances, pesticides, metals
- Hydromorphological: river habitat assessments

The EPA also operates a real-time continuous monitoring network (HydroNet) with multi-parameter sondes at key locations, measuring temperature, pH, DO, conductivity, and turbidity at 15-minute intervals.

## API Details

**HydroNet**: The EPA's HydroNet system (likely built on Kisters WISKI, similar to BOM Australia and other national hydrology systems) provides:
- Real-time hydrometric data (river levels, flows)
- Some real-time water quality from continuous monitors
- Web-based visualization

The HydroNet portal was unreachable during testing (connection timeout). The system may have been relocated or restructured.

**Alternative data access**:
- EPA Maps: `https://gis.epa.ie/EPAMaps/` — GIS-based data viewer
- Catchments.ie: `https://www.catchments.ie/` — WFD catchment data including water quality
- EPA open data: `https://data.gov.ie/` — datasets published by EPA

**WFD reporting**: Ireland's water quality status is reported under the EU Water Framework Directive, and the data feeds into EEA Waterbase.

## Freshness Assessment

Mixed. Continuous monitoring stations provide real-time data (15-min intervals), but these are relatively few in number. The bulk of water quality data comes from discrete sampling programs with lab analysis delays. The Q-value biological assessments are conducted on a 3-year rolling cycle.

## Entity Model

- **Station**: EPA station code, name, river/lake/coastal water, county, WFD water body
- **Sample**: station, date, sampling purpose, sample type
- **Measurement**: determinand, value, unit, detection limit
- **Q-Value**: biological quality rating (Q1-Q5 scale), assessment year

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Some real-time continuous data; mostly discrete sampling |
| Openness | 2 | Public data; API access uncertain; portal was unreachable |
| Stability | 2 | Government agency but web infrastructure showed connectivity issues |
| Structure | 1 | Web portal oriented; API not well-documented |
| Identifiers | 2 | EPA station codes; WFD water body references |
| Additive Value | 2 | Ireland-specific; Q-value biological index is unique |
| **Total** | **10/18** | |

## Notes

- The HydroNet portal was unreachable during testing — this is a concern for reliability.
- Ireland's Q-value system (a macroinvertebrate-based biotic index) is a well-regarded biological water quality assessment method and produces a distinctive dataset.
- The EPA is part of the broader EU WFD reporting framework, so much of their data eventually appears in EEA Waterbase, albeit with significant delay.
- The Catchments.ie portal may provide better structured access to WFD water quality data than the EPA's own systems.
- Ireland has a relatively small but well-monitored river network — the data quality is generally high.
- Recommend investigating the Kisters WISKI API endpoints (similar to BOM Australia's Water Data Online) — the EPA may use the same underlying infrastructure.
