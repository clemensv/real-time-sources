# BODC UK National Tide Gauge Network

**Country/Region**: United Kingdom (England, Scotland, Wales, Northern Ireland)
**Publisher**: British Oceanographic Data Centre (BODC), part of the National Oceanography Centre (NOC)
**API Endpoint**: `https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/` (download portal)
**Documentation**: https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/
**Protocol**: HTTP file download (raw + processed data files)
**Auth**: Free BODC registration required for raw data downloads
**Data Format**: CSV, ASCII (fixed-width format)
**Update Frequency**: Raw data: near real-time (continuous feed); Processed data: monthly (4-week delay)
**License**: Open data for processed historical files; registration required for raw/latest-month data

## What It Provides

The UK National Tide Gauge Network consists of 43 tide gauges around the UK coast, established after the catastrophic 1953 east coast flooding. BODC is responsible for remote monitoring, weekly data retrieval, and quality control.

Data products:
- **Raw/near-real-time data**: Unprocessed data covering the past month to today, updated continuously. Available for download (requires free registration) and as daily/weekly/monthly plot images.
- **Processed (QC'd) data**: Quality-controlled sea surface elevation from 1915 to ~2 months ago. Free download without registration for annual and monthly files.
- **Multiple channels**: Primary and secondary measurement channels.

Coverage spans the entire UK coastline with some of the longest continuous tide gauge records in the world (Newlyn from 1915, Dover from 1924).

## API Details

Access is file-based rather than a REST API:

- **Processed annual/monthly files**: `https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/processed/` — free download of CSV files organized by station and year/month
- **Raw data files**: `https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/raw/` — requires BODC login, covers last month to current day
- **Plot images**: Real-time/near-real-time plots for each station (1-day, 1-week, 1-month views) at `/raw/images/{StationName}_{1|2|3}.png`

Data format: Heights in metres above chart datum. Times in GMT.

Station list (43 gauges): Aberdeen, Avonmouth, Bangor, Barmouth, Bournemouth, Cromer, Devonport, Dover, Fishguard, Harwich, Heysham, Hinkley, Holyhead, Ilfracombe, Immingham, Jersey, Kinlochbervie, Leith, Lerwick, Liverpool (Gladstone Dock), Llandudno, Lowestoft, Milford Haven, Millport, Mumbles, Newhaven, Newlyn, Newport, North Shields, Portbury, Port Ellen, Port Erin, Portpatrick, Portrush, Portsmouth, Sheerness, Stornoway, St. Mary's, Tobermory, Ullapool, Weymouth, Whitby, Wick, Workington.

## Freshness Assessment

Mixed. Raw data is near-real-time but requires registration and is unprocessed. Quality-controlled processed data runs about 4 weeks behind. The plot images provide a visual real-time view without download. For true operational real-time data, the UK Environment Agency's flood monitoring API or the NTSLF (National Tidal & Sea Level Facility at NOC) may be more appropriate.

## Entity Model

- **Station**: name, chart datum reference (mostly Ordnance Datum Newlyn), lat/lon
- **Observation**: timestamp (GMT), sea surface elevation (m above chart datum), primary/secondary channel, QC flag
- **Annual File**: station + year, containing all hourly observations

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Raw data is near-real-time but behind a login; processed is monthly |
| Openness | 2 | Processed historical data is free; raw/recent data requires registration |
| Stability | 3 | Operational since 1953, government-funded, world-class QC |
| Structure | 1 | File-based downloads, no REST API; format is consistent but access is manual |
| Identifiers | 2 | Station names (not codes), cross-refs to PSMSL; no standardized IDs |
| Additive Value | 2 | UK-specific but among the world's longest continuous sea level records |
| **Total** | **12/18** | |

## Notes

- The BODC raw data feed is useful for near-real-time UK coastal monitoring but lacks a proper REST API.
- These same stations also report to the IOC SLSMF, often with lower latency. The BODC value proposition is in datum-referenced, quality-controlled historical data.
- For real-time operational UK tide data, consider the Environment Agency's flood monitoring real-time API (already partially covered) or the NTSLF at NOC.
- The latest-month processed data is available by request with a fee — a barrier for automated ingestion.
- Very long historical records (100+ years at some stations) make this valuable for sea level trend analysis.
