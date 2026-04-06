# Transpower — New Zealand Electricity System Operator

**Country/Region**: New Zealand
**Publisher**: Transpower New Zealand Ltd (state-owned TSO)
**API Endpoint**: Various endpoints on `www.transpower.co.nz` (undocumented)
**Documentation**: https://www.transpower.co.nz/system-operator/key-information/maps-and-dashboards
**Protocol**: REST / WebSocket (dashboard backends)
**Auth**: None for public dashboards
**Data Format**: JSON
**Update Frequency**: 5 minutes (generation), real-time (frequency)
**License**: Publicly accessible

## What It Provides

Transpower operates New Zealand's high-voltage transmission grid and the electricity system. New Zealand's grid is particularly interesting: ~80% renewable (hydro, geothermal, wind), split across two islands connected by HVDC inter-island link.

Data available via dashboards:

- **Live generation**: Current output by power station and fuel type (hydro, geothermal, wind, gas, coal, diesel, co-gen)
- **Demand**: North Island and South Island demand
- **Frequency**: Grid frequency (50 Hz)
- **HVDC link**: Power flow between North and South Islands
- **Reservoir levels**: Hydro lake storage levels (critical for NZ's hydro-dependent grid)
- **Spot prices**: Wholesale prices by node (NZ operates a nodal pricing market)

Transpower's Electricity Market Information (EMI) portal provides the most comprehensive access: https://www.emi.ea.govt.nz/

## API Details

Transpower's live data is served through dashboard applications that use backend JSON/WebSocket endpoints. During testing, direct JSON endpoint probes returned 404:

```
GET https://www.transpower.co.nz/em6/data/live_gen.json → 404
GET https://www.transpower.co.nz/em6/data/s_generation.json → 404
```

The EMI (Electricity Market Information) portal run by the Electricity Authority is likely a better programmatic access point:
- https://www.emi.ea.govt.nz/Wholesale/Datasets
- Provides CSV/JSON downloads for generation, pricing, demand, hydro storage

The live generation dashboard renders data client-side, suggesting a JavaScript-accessible API that could be reverse-engineered from the page source.

## Freshness Assessment

Dashboard data updates every 5 minutes for generation and demand. Grid frequency is near-real-time. Spot prices settle at 5-minute (real-time) and 30-minute (final) intervals. Hydro lake levels update daily.

## Entity Model

- **Power Station**: Individual plant names and IDs
- **Fuel Type**: Hydro, Geothermal, Wind, Gas, Coal, Diesel, Co-Gen
- **Island**: North Island (NI), South Island (SI)
- **Node**: ~200+ pricing nodes across the grid
- **HVDC**: Inter-island link flow in MW (positive = South→North)
- **Reservoir**: Lake names with storage in GWh

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute real-time updates on dashboards |
| Openness | 2 | Data is public but API endpoints are undocumented |
| Stability | 2 | Dashboard URLs have changed historically; no formal API commitment |
| Structure | 1 | No verified JSON API endpoint; dashboard scraping required |
| Identifiers | 2 | Plant names, NZ-specific node codes |
| Additive Value | 3 | Only source for NZ grid — unique hydro/geothermal mix, Southern Hemisphere coverage |
| **Total** | **13/18** | |

## Notes

- New Zealand's grid is a fascinating case study: ~80% renewable, with hydro storage acting as a giant "battery" — but vulnerable to dry years ("dry year risk" is a real grid reliability concern).
- The EMI portal (Electricity Authority) may provide better programmatic access than Transpower directly.
- Geothermal baseload (~1,000 MW) is a unique feature — NZ and Iceland are the only countries where geothermal is a major grid contributor.
- The inter-island HVDC link data is inherently interesting — it connects two electrically separate grids.
- Consider partnering with the `electricitymap` open-source contributors who have already reverse-engineered NZ data feeds.
