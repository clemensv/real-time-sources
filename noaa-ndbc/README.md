# NOAA NDBC Buoy Observations Poller

## Overview

**NOAA NDBC Buoy Observations Poller** polls the National Data Buoy Center (NDBC) station table, the composite `latest_obs.txt` feed, and selected `realtime2` family files, then sends them to a Kafka topic as CloudEvents. The bridge emits station reference data first and tracks previously seen timestamps per station and feed family to avoid sending duplicates.

## Key Features

- **Reference Data First**: Emits `BuoyStation` reference events from the NDBC station table before telemetry polling begins.
- **Composite Latest Observations**: Fetches the standard buoy observation feed from `https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt`.
- **Realtime2 Coverage**: Polls the `srad`, `ocean`, `dart`, `cwind`, `supl`, `spec`, and `rain` realtime2 families when available for a station.
- **Family-Aware Deduplication**: Tracks last seen observation timestamps per station and feed family in a state file to avoid reprocessing.
- **Kafka Integration**: Send buoy observations to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=noaa-ndbc
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/noaa-ndbc
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m noaa_ndbc`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where last seen timestamps per station are stored. Defaults to `~/.ndbc_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m noaa_ndbc --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m noaa_ndbc --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `NDBC_LAST_POLLED_FILE`: File to store last seen timestamps per station for deduplication.

## Event Families

All events are keyed by `station_id`. Full CloudEvents and field documentation lives in [EVENTS.md](EVENTS.md).

| Event Type | Upstream Source | Description |
|------------|-----------------|-------------|
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation` | NDBC station table | Reference metadata for the observing platform |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation` | `latest_obs.txt` | Standard meteorological and oceanographic snapshot |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation` | `realtime2/*.srad` | Shortwave and longwave radiation telemetry |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation` | `realtime2/*.ocean` | Depth-tagged ocean chemistry and physical measurements |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement` | `realtime2/*.dart` | DART tsunami buoy water-column measurements |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation` | `realtime2/*.cwind` | Ten-minute wind averages plus hourly gust extrema |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement` | `realtime2/*.supl` | Hourly pressure minima and one-minute wind maxima |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary` | `realtime2/*.spec` | Swell, wind-wave, and wave-steepness summary values |
| `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement` | `realtime2/*.rain` | One-hour precipitation accumulation |

## Data Source

The NOAA National Data Buoy Center (NDBC) maintains a network of approximately 1,300 buoys and coastal stations that measure meteorological and oceanographic conditions. The bridge covers the standard observation composite feed plus selected realtime2 channel families for radiation, ocean chemistry, DART, wind extrema, wave summaries, and rainfall. Data is updated approximately every 5 minutes for the composite feed, with station-specific realtime2 products published on their own cadences.

- **Latest observations**: `https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt`
- **NDBC home page**: `https://www.ndbc.noaa.gov/`

## License

[MIT](../LICENSE.md)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template-with-eventhub.json)
