# Blitzortung Lightning — African Coverage

- **Country/Region**: Pan-African (coverage varies by receiver density)
- **Endpoint**: `https://map.blitzortung.org/GEOjson/Data/Strokes/{region}/{timestamp}/`
- **Protocol**: WebSocket / REST
- **Auth**: Community participation (share receiver data for access)
- **Format**: GeoJSON, JSON
- **Freshness**: Real-time (lightning strikes within seconds)
- **Docs**: https://www.blitzortung.org/
- **Score**: 11/18

## Overview

Blitzortung is a citizen science lightning detection network. While most receivers are
in Europe and the Americas, the network has growing coverage in Africa, particularly
in South Africa and East Africa.

Africa has some of the most intense thunderstorm activity on Earth:
- **Congo Basin**: The world's highest lightning frequency (Lake Maracaibo challenged but
  the Congo Basin region is consistently extreme)
- **Lake Victoria**: Legendary for violent thunderstorms, particularly at night
- **South African Highveld**: Intense summer convective storms
- **West Africa Squall Lines**: Massive mesoscale convective systems crossing the Sahel

Lightning data is valuable for:
- Severe weather nowcasting
- Wildfire ignition detection
- Aviation safety
- Power grid protection (lightning causes outages)

## Endpoint Analysis

The Blitzortung network uses a community-based data sharing model. Real-time data
is accessible to those who contribute receiver stations.

Public-facing data:
- Map at https://map.blitzortung.org/ shows live strikes
- GeoJSON data feed available for regions (Africa = region 5)
- WebSocket connections for real-time strike data

The existing `blitzortung` candidate in the `lightning` domain already covers the
global network. This document adds African context.

African receiver stations are concentrated in:
- South Africa (several stations)
- Kenya (Nairobi area)
- Tanzania (limited)
- Morocco (limited)
- Nigeria (emerging)

Coverage is sparse in Central and West Africa due to limited receiver infrastructure.

## Integration Notes

- **Existing candidate**: The `lightning/blitzortung.md` candidate already covers the
  network globally. An Africa bridge uses the same protocol with region filtering.
- **Region 5**: Africa is Blitzortung region 5. Filter data accordingly.
- **Coverage gaps**: Most of Africa lacks receiver stations. Detection efficiency is
  much lower than in Europe. Strikes are detected but location accuracy suffers.
- **Complement with satellites**: EUMETSAT MTG Lightning Imager provides uniform African
  coverage from geostationary orbit — no ground stations needed.
- **Wildfire link**: Lightning-ignited fires in Africa's dry savannas are significant.
  Correlate lightning strikes with MODIS thermal hotspots.
- **Agricultural insurance**: Parametric crop insurance products in Africa use lightning
  data as a proxy for convective storm damage.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (seconds) |
| Openness | 1 | Community participation model |
| Stability | 2 | Citizen science, coverage depends on receivers |
| Structure | 2 | GeoJSON, WebSocket |
| Identifiers | 1 | Strike IDs (transient) |
| Richness | 2 | Strike location, time, amplitude, type |
