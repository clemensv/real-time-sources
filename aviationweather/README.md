# AviationWeather.gov Bridge

## Overview

**AviationWeather.gov Bridge** polls the NOAA Aviation Weather Center API for METAR observations, SIGMET advisories, and station reference data, then sends them to a Kafka topic as CloudEvents. The tool tracks previously seen observations to avoid sending duplicates.

## Key Features

- **METAR Observations**: Fetch aviation weather observations for configurable ICAO stations from `https://aviationweather.gov/api/data/metar`.
- **SIGMET Advisories**: Fetch both US domestic and international SIGMETs from `https://aviationweather.gov/api/data/airsigmet` and `https://aviationweather.gov/api/data/isigmet`.
- **Station Reference Data**: Emit station metadata at startup and refresh periodically.
- **Deduplication**: Tracks last seen METAR observation time per station and SIGMET identity to avoid reprocessing.
- **Kafka Integration**: Send events to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=aviationweather
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/aviationweather
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m aviationweather`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to state file for deduplication. Defaults to `~/.aviationweather_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).
- `--stations`: Comma-separated list of ICAO station IDs to monitor (default: `KJFK,KLAX,KORD,KATL,EGLL,LFPG,EDDF,RJTT,YSSY,ZBAA`).
- `--metar-poll-interval`: METAR poll interval in seconds (default: 60).
- `--sigmet-poll-interval`: SIGMET poll interval in seconds (default: 120).

### Example Usage

#### Using a Connection String

```bash
python -m aviationweather --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m aviationweather --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

#### Custom Station List

```bash
python -m aviationweather --connection-string "<conn>" --stations "KJFK,KLAX,EGLL"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `AVIATIONWEATHER_LAST_POLLED_FILE`: File to store deduplication state.
- `AVIATIONWEATHER_STATIONS`: Comma-separated list of ICAO station IDs.

## Data Source

The NOAA Aviation Weather Center (AWC) provides publicly available aviation weather data via a REST API. METARs are updated approximately every minute. SIGMETs cover hazardous weather conditions including convective activity, turbulence, icing, and volcanic ash.

- **API base**: `https://aviationweather.gov/api/data/`
- **Documentation**: `https://aviationweather.gov/data/api/`
- **License**: US Public Domain

## License

[MIT](../LICENSE.md)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventhub.json)
