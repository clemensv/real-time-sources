# DXHeat

**Country/Region**: Global
**Publisher**: DXHeat.com (community project)
**API Endpoint**: `https://dxheat.com/dxc/`
**Documentation**: https://dxheat.com/
**Protocol**: HTTP (HTML/JSON), WebSocket
**Auth**: None (web), Callsign (DX cluster connection)
**Data Format**: HTML (web interface), DX cluster spot format
**Update Frequency**: Real-time (continuous DX spot aggregation)
**License**: Free for amateur radio use

## What It Provides

DXHeat is a modern DX cluster aggregator — it collects real-time DX spots from multiple cluster nodes worldwide and presents them in a clean, filterable web interface with band-by-band propagation visualization. The site aggregates spots from traditional DX clusters, the Reverse Beacon Network, and other sources into a unified view of who's working who on which bands right now.

The interface includes real-time band activity maps, propagation indicators, and filtering by band, mode, continent, and time. While it doesn't expose a formal REST API, the web interface loads data dynamically via AJAX calls that can be consumed programmatically.

## API Details

- **Web interface**: `https://dxheat.com/dxc/` — real-time spot display with AJAX data loading
- **Data loading**: Dynamic JavaScript-driven data fetching (inspectable via browser dev tools)
- **DX Cluster access**: Underlying data comes from telnet DX cluster network
- **Filtering**: Band, mode, continent, spotter location, time window
- **No formal API**: Data consumption requires web scraping or cluster protocol access
- **Companion data**: Solar indices display, propagation maps, contest activity

## Freshness Assessment

Spots appear in near-real-time — seconds after being posted to the DX cluster network. The web interface auto-refreshes. During contest weekends, thousands of spots flow through per minute.

Confirmed live: web interface returned 200 OK with active spot data.

## Entity Model

- **DX Spot**: Spotter callsign, DX callsign, frequency (kHz), time (UTC), comment, band, mode
- **Propagation path**: Spotter location → DX station location
- **Band activity**: Aggregate spot counts per band per time unit

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, seconds latency |
| Openness | 2 | Free web access; no formal API; underlying cluster requires callsign |
| Stability | 2 | Community project; web scraping is fragile |
| Structure | 1 | No formal API; HTML/AJAX scraping required |
| Identifiers | 2 | Callsigns, frequencies, timestamps |
| Additive Value | 2 | Aggregated DX cluster view; complements RBN and PSKReporter |
| **Total** | **12/18** | |

## Notes

- Confirmed live: website returns spot data.
- The lack of a formal API is the main limitation — data extraction requires scraping or going to the underlying DX cluster sources directly.
- For programmatic access, the DX Cluster (already cataloged) or RBN are better choices.
- DXHeat's value is as a curated, filtered aggregation layer — useful as a human reference but less suitable for automated consumption.
- Pairs with DX Cluster and RBN for spot data, and HamQSL for propagation indices displayed alongside spots.
