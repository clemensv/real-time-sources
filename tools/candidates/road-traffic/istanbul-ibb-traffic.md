# Istanbul Metropolitan Municipality (İBB) Open Data — Traffic & Transit

**Country/Region**: Turkey (Istanbul)
**Publisher**: Istanbul Metropolitan Municipality (İstanbul Büyükşehir Belediyesi — İBB)
**API Endpoint**: `https://data.ibb.gov.tr/api/3/action/`
**Documentation**: https://data.ibb.gov.tr/ (CKAN-based open data portal)
**Protocol**: REST (CKAN API v3)
**Auth**: None (anonymous access for most datasets)
**Data Format**: JSON, CSV (via CKAN datastore)
**Update Frequency**: Varies — hourly traffic density, daily transit metrics, real-time air quality
**License**: Istanbul Metropolitan Municipality Open Data License

## What It Provides

Istanbul's open data portal is one of the most comprehensive municipal data platforms in the Middle East and a gateway into the data infrastructure of a 16-million-person megacity straddling two continents.

The portal runs on CKAN — the same platform used by data.gov.uk, data.gov, and other national open data portals — which means it has a well-documented, standardized API. The transportation and mobility datasets are particularly rich:

### Transport & Traffic Datasets Confirmed
- **Hourly Traffic Density Data Set** — Vehicle counts, average/max/min speeds across Istanbul grid cells (61 monthly resources since 2020)
- **Istanbul Traffic Index** — City-wide traffic congestion index (daily min, max, avg)
- **Variable Message Board Routes** — Real-time electronic sign content on highways
- **Variable Message Board Density Data** — Traffic density from electronic monitoring points
- **Maritime Route Data** — Ferry routes and schedules (Istanbul has major water transit)
- **İSBike Stations** — Bikeshare station status (GBFS-compatible)

### Other Real-Time/Near-Real-Time Datasets
- **Air Quality Monitoring** — Station-level pollutant readings
- **Earthquake Scenario Analysis** — Risk modeling data
- **Parking Data** — Municipal parking occupancy
- **Energy Consumption** — District-level electricity usage

## API Details

CKAN standard API with datastore search:

```
# List all datasets
GET https://data.ibb.gov.tr/api/3/action/package_list

# Search datasets
GET https://data.ibb.gov.tr/api/3/action/package_search?q=traffic&rows=10

# Get dataset metadata
GET https://data.ibb.gov.tr/api/3/action/package_show?id=hourly-traffic-density-data-set

# Query datastore records
GET https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id={id}&limit=100
```

### Probed Response — Dataset Metadata (April 2026)

The traffic density dataset contains **61 monthly CSV resources** dating from January 2020, with data including:
- Geographic grid cell coordinates
- Unique vehicle counts per cell
- Average speed, maximum speed, minimum speed
- Hourly granularity

Traffic Index dataset contains daily congestion metrics with min/max/average index values — updated automatically (last modified September 2025).

### Search Confirmed Working

```json
{
  "success": true,
  "result": {
    "count": 6,
    "results": [
      {"name": "istanbul-trafik-indeksi", "title": "Istanbul Traffic Index"},
      {"name": "hourly-traffic-density-data-set", "title": "Hourly Traffic Density Data Set"},
      {"name": "goruntu-isleme-yoluyla-elde-edilen-arac-verisii", "title": "Vehicle Data from Image Processing"}
    ]
  }
}
```

## Freshness Assessment

Mixed. The traffic density data is updated monthly (batch uploads), while the traffic index is updated daily. Some datasets are more static (earthquake scenarios). The datastore API provides SQL-like query capabilities for efficient filtering. The bikeshare data appears to have real-time web service endpoints.

## Entity Model

- **Grid Cell**: Geographic partition of Istanbul for traffic density aggregation
- **Traffic Index**: Daily city-wide metric with min/max/average
- **Transit Route**: Identified by route ID, with stops and schedules
- **Station**: Air quality monitoring stations with lat/lon
- **Resource**: Time-partitioned data files (monthly CSVs for traffic)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Traffic index is daily; hourly density uploaded monthly; some real-time endpoints |
| Openness | 3 | No auth for most datasets; CKAN is a standardized open-source platform |
| Stability | 2 | Municipal platform; active since 2020; metadata_modified dates are recent |
| Structure | 3 | CKAN standard API; CSV/JSON formats; well-documented schema |
| Identifiers | 2 | Dataset IDs are URL-slugs; resource UUIDs; grid cell IDs for traffic |
| Additive Value | 3 | Only open data source for Istanbul — 16M megacity bridging Europe/Asia |
| **Total** | **15/18** | |

## Integration Notes

- CKAN API is well-documented: https://docs.ckan.org/en/latest/api/
- The datastore_search endpoint enables SQL-like queries with filters, sorting, and field selection
- Some datasets may have bilingual titles (Turkish primary, English secondary)
- The bikeshare endpoint (İSBike) likely follows GBFS standard — worth separate investigation
- Traffic density data is best suited for periodic batch import rather than real-time polling
- Istanbul Traffic Index at daily granularity could be polled once daily
- CloudEvents mapping: one event per traffic index update; batch events for grid cell updates
- Consider pairing with Istanbul transit smart card (İstanbulkart) data if available

## Verdict

Istanbul's open data portal provides solid municipal data from a strategically important megacity. The CKAN platform ensures API stability and standardization. The traffic density and transit datasets fill a major gap in Middle Eastern coverage. While not all data is truly real-time, the daily traffic index and the potential for bikeshare/transit real-time feeds make this a valuable addition.
