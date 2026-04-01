# German Waters Bridge

Aggregates water level and discharge data from German state open data portals and
emits CloudEvents to Kafka endpoints (Event Hubs, Fabric Event Streams, etc.).

This bridge pulls data exclusively from **official government open data sources** —
no commercial aggregators.

## Data Sources

| Provider      | State                    | Stations | Data format                 | License        |
|---------------|--------------------------|----------|-----------------------------|----------------|
| `bayern_gkd`  | Bayern                   | ~664     | JSON embedded in HTML map   | CC-BY 4.0      |
| `nrw_hygon`   | Nordrhein-Westfalen      | ~300     | WISKI-Web JSON              | dl-de/zero-2-0 |
| `sh_lkn`      | Schleswig-Holstein       | ~72      | HTML tooltips               | dl-de/zero-2-0 |
| `nds_nlwkn`   | Niedersachsen            | ~200     | Azure REST API JSON         | dl-de/by-2-0   |
| `sa_lhw`      | Sachsen-Anhalt           | ~99      | WISKI-Web JSON              | dl-de/zero-2-0 |
| `he_hlnug`    | Hessen                   | ~186     | WISKI-Web3 JSON             | dl-de/zero-2-0 |
| `sn_lfulg`    | Sachsen                  | ~190     | ArcGIS REST GeoJSON         | dl-de/zero-2-0 |
| `bw_hvz`      | Baden-Württemberg        | ~333     | JS array                    | dl-de/by-2-0   |
| `bb_lfu`      | Brandenburg              | ~270     | OpenLayers Features in HTML | dl-de/zero-2-0 |
| `th_tlubn`    | Thüringen                | ~68      | Leaflet markers in HTML     | dl-de/zero-2-0 |
| `mv_lung`     | Mecklenburg-Vorpommern   | ~227     | HTML table                  | dl-de/zero-2-0 |
| `be_senumvk`  | Berlin                   | ~115     | OpenLayers Features in HTML | dl-de/zero-2-0 |

**Total: ~2,724 stations** across 12 federal states.

### Bayern GKD (Gewässerkundlicher Dienst)

- Source: https://www.gkd.bayern.de/de/fluesse/wasserstand
- Water levels (~664 gauges) and discharge
- Data includes coordinates, river name, current value, and timestamp
- Extracted from the embedded `LfUMap.init()` JSON on the map page

### NRW Hydrologie (LANUV)

- Source: https://hydrologie.nrw.de/
- WISKI-Web JSON at `/data/internet/layers/10/index.json` with ~300 gauges
- Real-time water level readings regenerated every ~15 minutes

### Schleswig-Holstein HSI

- Source: https://hsi-sh.de/
- HTML page with embedded station tooltips containing current readings
- Only local Landespegel (station numbers starting with 11) are emitted

### Niedersachsen NLWKN

- Source: https://www.pegelonline.nlwkn.niedersachsen.de/
- Azure-hosted REST API returning ~200 gauges with 15-min water level readings

### Sachsen-Anhalt LHW

- Source: https://hvz.lsaurl.de/
- WISKI-Web JSON at `/data/internet/layers/1030/index.json` with ~214 total gauges
- Filtered to ~99 LHW-owned state stations (excludes WSV federal and neighboring state gauges)

### Hessen HLNUG

- Source: https://www.hlnug.de/static/pegel/wiskiweb3/
- WISKI-Web3 JSON with water level (layer 10) and discharge (layer 20) for ~186 gauges

### Sachsen LfULG

- Source: https://luis.sachsen.de/
- ArcGIS MapServer REST query returning ~190 gauges as GeoJSON with WGS84 coordinates
- Includes water level, discharge, timestamps, trend, and alarm stage thresholds

### Baden-Württemberg HVZ

- Source: https://www.hvz.baden-wuerttemberg.de/
- JavaScript array `HVZ_Site.PEG_DB` at `/js/hvz_peg_stmn.js` with ~333 stations
- Column layout defined in `/js/hvz_peg_var.js` (72+ fields per station)

### Brandenburg LfU

- Source: https://pegelportal.brandenburg.de/
- OpenLayers Feature objects embedded in HTML with ~270 local Brandenburg gauges
- Coordinates in ETRS89/UTM33N, auto-converted to WGS84

### Thüringen TLUBN

- Source: https://hnz.thueringen.de/hw-portal/
- Leaflet circleMarker objects embedded in HTML with ~68 gauges
- Station names fetched from per-station detail pages

### Mecklenburg-Vorpommern LUNG

- Source: https://pegelportal-mv.de/pegel_list.html
- HTML table with ~227 gauges including water level, discharge, and alarm stage
- Station coordinates not available (only pixel positions on map)

### Berlin SenUMVK

- Source: https://wasserportal.berlin.de/
- OpenLayers Feature objects embedded in HTML with ~115 surface water gauges
- Coordinates in UTM 33N, auto-converted to WGS84

## Events

Two CloudEvent types are emitted:

- **`DE.Waters.Hydrology.Station`** — station metadata (emitted once at startup)
- **`DE.Waters.Hydrology.WaterLevelObservation`** — current water level and discharge readings

## Usage

```bash
# List available providers
python -m german_waters list-providers

# List stations from all providers
python -m german_waters list

# List stations from a specific provider
python -m german_waters list --providers bayern_gkd

# List stations excluding a provider
python -m german_waters list --exclude-providers sh_lkn

# Feed to Kafka (Event Hubs / Fabric Event Stream)
python -m german_waters feed -c "Endpoint=sb://..."
```

## Environment Variables

| Variable              | Description                                    |
|-----------------------|------------------------------------------------|
| `CONNECTION_STRING`   | Event Hubs / Fabric connection string          |
| `PROVIDERS`           | Comma-separated provider keys to include       |
| `EXCLUDE_PROVIDERS`   | Comma-separated provider keys to exclude       |
| `POLLING_INTERVAL`    | Seconds between data fetches (default: 900)    |
| `STATE_FILE`          | Path to deduplication state file               |

## Docker

```bash
docker build -t german-waters .
docker run -e CONNECTION_STRING="Endpoint=sb://..." german-waters
```
