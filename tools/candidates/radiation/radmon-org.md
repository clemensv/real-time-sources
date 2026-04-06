# Radmon.org (Community Radiation Monitoring)

**Country/Region**: Global (community-driven, strongest in Europe and North America)
**Publisher**: Radmon.org (independent community project)
**API Endpoint**: `https://radmon.org/radmon.php?function={function}&user={username}`
**Documentation**: https://radmon.org/index.php/api
**Protocol**: REST (PHP-based, simple query string API)
**Auth**: None for reads (account required for data submission)
**Data Format**: Plain text (simple string responses)
**Update Frequency**: Continuous (depends on user device submission frequency)
**License**: Not formally specified (community project)

## What It Provides

Radmon.org is a community-driven global radiation monitoring network for hobbyists and experimenters. Users connect Geiger counters — home-built, kit-built, or commercial — to submit background radiation readings. The platform provides:

- **Live radiation map** — Global map with real-time readings from all connected stations
- **Historical graphs** — Per-station radiation level history
- **Alert system** — Email notifications when readings exceed thresholds
- **Experimental mode** — Stations can operate in testing mode without triggering alerts

The project runs on a solar-powered Raspberry Pi 4 server.

## API Details

### Endpoints

The API uses a simple PHP query string pattern:

| Function | URL | Description |
|---|---|---|
| `lastreading` | `radmon.php?function=lastreading&user={name}` | Get latest reading for a user |
| `showmap` | `radmon.php?function=showmap` | Show the map (HTML) |

### Example Request

```
GET https://radmon.org/radmon.php?function=lastreading&user=simomax
```

### Sample Response

```
22 CPM on 2026-04-06 10:25:12UTC at Wastelands of Hoth
```

The response is plain text — a single line containing CPM value, timestamp, and location name.

### Submission API

Data submission supports multiple platforms:
- Windows application (dedicated)
- Linux BASH scripts
- Raspberry Pi (Python — pyradmon)
- Arduino/ESP
- Custom code via documented submission endpoints

## Freshness Assessment

Live data confirmed on 2026-04-06. The `lastreading` endpoint returned a fresh measurement from the current minute. The map endpoint was unreachable during testing (connection timeout — possibly due to the Raspberry Pi server's capacity). Data freshness depends entirely on individual station submission frequency.

## Entity Model

- **User/Station** — Identified by username. Has location name (free text), coordinates (displayed on map), and alert threshold settings.
- **Reading** — CPM value, timestamp (UTC), location name. No standardized units beyond CPM.
- **Mode** — Normal or Experimental (affects alert behavior and map display).

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Real-time submissions but dependent on individual user activity |
| Openness | 2 | Free to access, but no formal license; API underdocumented |
| Stability | 0 | Runs on a solar-powered Raspberry Pi — no SLA, hobby infrastructure |
| Structure | 0 | Plain text responses, no JSON, minimal API, no bulk data access |
| Identifiers | 1 | Username as identifier, free-text location names |
| Additive Value | 1 | Small community network, limited coverage compared to official networks |
| **Total** | **6/18** | |

## Notes

- Radmon.org is a passionate community project but not suitable for production-grade data integration. The Raspberry Pi infrastructure is a single point of failure.
- The API is minimal — single-user `lastreading` calls only. No bulk data retrieval, no JSON format, no station list endpoint.
- The map endpoint was intermittently unreachable, consistent with hobby-grade hosting.
- The project's value is in its community and educational aspects rather than as a reliable data source.
- For citizen radiation monitoring, Safecast provides a much more robust alternative with better API, data licensing, and infrastructure.
- Interesting as a "long tail" data source but not recommended for primary integration.
