# Synoptic Data (formerly MesoWest) — Mesonet API

**Country/Region**: Global (focus on US, expanding worldwide)
**Publisher**: Synoptic Data PBC (formerly MesoWest, University of Utah)
**API Endpoint**: `https://api.synopticdata.com/v2/`
**Documentation**: https://docs.synopticdata.com/
**Protocol**: REST API
**Auth**: API Key (required; free tier available, commercial tiers for higher volume)
**Data Format**: JSON
**Update Frequency**: Real-time (as observations arrive)
**License**: Proprietary / commercial with free tier

## What It Provides

Synoptic Data is the world's largest aggregator of surface weather station observations, providing a single API for data from 170,000+ stations across 320+ networks in 100+ countries:

- **Real-Time Observations**: Latest observations from ASOS, AWOS, RAWS, DOT road weather, mesonets, citizen weather stations, and hundreds of other networks. Parameters include:
  - Temperature, dewpoint, humidity
  - Wind speed, direction, gusts
  - Precipitation (multiple intervals)
  - Pressure (altimeter, sea-level, station)
  - Visibility, sky cover, weather codes
  - Road surface temperature, soil temperature
  - Specialized variables (160+ total)

- **Time Series**: Historical observations for any station over any time range.

- **Nearest Station**: Find the closest station(s) to a lat/lon point.

- **Latest Observations**: Get the most recent observation from stations in an area.

- **Statistics**: Daily/monthly min, max, mean; percentile distributions.

- **Quality Control**: Multi-level QC flags on all observations (range checks, spatial consistency, persistence).

- **Push Streaming**: Server-sent events for real-time data push (commercial tier).

- **Precipitation Service**: Normalized precipitation data across networks with different reporting intervals.

## API Details

Standard REST API with API key authentication:
```
GET https://api.synopticdata.com/v2/stations/latest?token={API_KEY}&stid=KSLC&within=60
```

Key query patterns:
- `stations/latest`: Most recent observations.
- `stations/timeseries`: Historical time series.
- `stations/nearesttime`: Observation nearest to a specified time.
- `stations/metadata`: Station metadata search.
- `stations/precipitation`: Precipitation aggregation.
- `stations/statistics`: Statistical summaries.

Supports spatial queries (radius, bounding box, state, country), network filtering, variable selection, and time windowing.

Free tier: Limited API calls per month (appropriate for development and small-scale use). Commercial tiers for production and high-volume access.

## Freshness Assessment

- Observations arrive within seconds to minutes of measurement.
- Over 1 billion API calls served annually.
- Adding 15,000+ stations per year as networks expand.
- Real-time QC applied as data enters the system.

## Entity Model

- **Station**: STID (station identifier), unique per network. Rich metadata: name, network, lat/lon, elevation, state/country, timezone, status.
- **Network**: Named collection of stations (e.g., "NWS/FAA", "Colorado DOT", "Oklahoma Mesonet").
- **Observation**: Variable + value + timestamp + QC flags.
- **Variable**: 160+ variables with standardized naming (e.g., `air_temp`, `wind_speed`, `precip_accum_one_hour`).

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time observations as they arrive, push streaming available |
| Openness | 1 | Free tier exists but limited; production use requires commercial license |
| Stability | 3 | Established company (spun out from University of Utah), 1B+ API calls/year |
| Structure | 3 | Well-documented REST API, consistent JSON, rich QC metadata |
| Identifiers | 3 | Standard station IDs, 160+ named variables, network classifications |
| Additive Value | 3 | 170,000+ stations, 320+ networks, global coverage, multi-level QC |
| **Total** | **16/18** | |

## Notes

- Synoptic Data is the commercial evolution of the academic MesoWest project at the University of Utah.
- The aggregation value is immense — a single API call can return data from federal (NOAA), state (DOT, mesonet), and private networks that would otherwise require dozens of separate integrations.
- The quality control layer adds significant value — each observation carries QC flags from basic range checks through spatial and percentile analysis.
- The free tier is useful for evaluation and small projects but not for production integration.
- Probed endpoint returned HTTP 401 (no token) — confirms API is active and enforces authentication.
- For US-focused applications, IEM (free, open) may be a better choice. Synoptic Data's strength is global aggregation and commercial-grade SLAs.
- The push streaming feature (SSE) is notable — few weather data providers offer server-push delivery.
