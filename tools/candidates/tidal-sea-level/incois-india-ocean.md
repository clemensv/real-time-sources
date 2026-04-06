# India INCOIS — Indian National Centre for Ocean Information Services

**Country/Region**: India (Indian Ocean)
**Publisher**: Indian National Centre for Ocean Information Services (INCOIS), Ministry of Earth Sciences
**API Endpoint**: `https://incois.gov.in/` (web portal), `https://tsunami.incois.gov.in/` (tsunami warning)
**Documentation**: https://incois.gov.in/, https://tsunami.incois.gov.in/
**Protocol**: Web portal (HTML); data services via web applications
**Auth**: Registration for some data products
**Data Format**: HTML, NetCDF, HDF5 (scientific formats)
**Update Frequency**: Real-time for tsunami alerts; hourly-daily for ocean observations
**License**: Indian government / ESSO (Earth System Science Organization)

## What It Provides

INCOIS is India's ocean information center and a critical node in the Indian Ocean Tsunami Warning System (IOTWS), established after the devastating 2004 Indian Ocean tsunami that killed ~230,000 people.

### Key Data Products

- **Tsunami Early Warning**: Real-time seismic monitoring and tsunami threat assessment for the Indian Ocean
- **Ocean State Forecast (OSF)**: Wave height, sea surface temperature, currents for Indian coastline
- **Potential Fishing Zones (PFZ)**: Satellite-derived advisories for 4 million Indian fishermen
- **Coral Bleaching Alert System**: Based on sea surface temperature anomalies
- **Oil Spill Advisory**: Trajectory prediction for marine pollution events
- **Algal Bloom Monitoring**: Harmful algal bloom detection
- **Sea Level Monitoring**: Tide gauge network along Indian coast
- **Ocean buoy data**: Moored and drifting buoy observations

### Indian Ocean Tsunami Warning Centre (ITEWC)

INCOIS operates the ITEWC, which:
- Monitors earthquakes in the Indian Ocean region in real-time
- Issues tsunami bulletins within 8-10 minutes of a major submarine earthquake
- Covers the entire Indian Ocean basin (26 member countries)
- Operates a network of DART (Deep-ocean Assessment and Reporting of Tsunamis) buoys

### Probe Results

- `incois.gov.in/portal/datainfo/drss.jsp` → 404
- `incois.gov.in/MarineServices/tsunamiservices/tsunamialert.jsp` → 404
- `tsunami.incois.gov.in/ITEWS/bview/latestalert.do` → Connection failed

The web endpoints return 404 or connection failures. INCOIS web infrastructure may be:
1. Reorganized (URL paths have changed)
2. Behind authentication
3. Using internal network for data delivery

## Entity Model

- **Earthquake**: For tsunami assessment — magnitude, depth, location, origin time
- **Tsunami Bulletin**: Threat level (Watch, Advisory, Warning), affected coastlines, arrival times
- **Ocean Buoy**: Moored/drifting buoy readings (temperature, pressure, wave height)
- **Tide Gauge**: Sea level observations from coastal stations
- **Ocean Grid**: Model output on regular lat/lon grids (NetCDF format)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Tsunami alerts are minutes-latency; ocean data hourly-daily; but endpoints unreachable |
| Openness | 1 | Some public data; registration required for others; endpoints returning 404 |
| Stability | 2 | Well-funded national center; operational since 2004 tsunami; web URLs may have changed |
| Structure | 1 | Scientific data formats (NetCDF); web endpoints not functioning |
| Identifiers | 2 | Buoy IDs; tide gauge station codes; earthquake IDs from seismic networks |
| Additive Value | 3 | Indian Ocean tsunami warning; 26-country coverage; PFZ serves 4M fishermen |
| **Total** | **11/18** | |

## Integration Notes

- Tsunami warning data would be extremely valuable but endpoints need rediscovery
- INCOIS data may be accessible through alternative URLs or through data.gov.in
- The DART buoy data could complement NOAA NDBC buoy coverage in the Indian Ocean
- PFZ (Potential Fishing Zones) is a unique data product — satellite-derived fishing advisories
- Scientific formats (NetCDF) require specialized parsing
- INCOIS contributes to IOC/UNESCO tsunami warning system — data may be available through IOC channels

## Verdict

Important Indian Ocean data center with unreliable web endpoints. INCOIS is operationally critical for Indian Ocean tsunami warning and provides unique products (PFZ for fishermen, coral bleaching alerts). The endpoints tested returned 404 or connection failures, suggesting URL restructuring. Worth revisiting with updated URLs — the underlying data infrastructure is well-established and well-funded.
