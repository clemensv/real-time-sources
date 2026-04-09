# DWD Pollenflug (German Pollen Forecast) Bridge

## Overview

**DWD Pollenflug Bridge** polls the Deutscher Wetterdienst (DWD) pollen forecast API for the latest daily pollen forecasts across Germany and sends them to a Kafka topic as CloudEvents. The tool tracks the `last_update` timestamp from the API to avoid sending duplicate forecasts.

## Data Source

The DWD publishes pollen forecasts via the open data portal at:
- **API Endpoint**: `https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json`
- **Update Frequency**: Daily on weekdays around 11:00 CET
- **License**: Open data under the DWD Geodatenzugangsgesetz (free for all uses with attribution)

The forecast covers **8 pollen types** across **27 German forecast regions**:

| German Name | English Name |
|---|---|
| Hasel | Hazel |
| Erle | Alder |
| Birke | Birch |
| Esche | Ash |
| Gräser (Graeser) | Grasses |
| Roggen | Rye |
| Beifuß (Beifuss) | Mugwort |
| Ambrosia | Ragweed |

Intensity values range from 0 (no load) to 3 (high load) with intermediate half-step values (0-1, 1-2, 2-3).

## Key Features

- **Daily Pollen Forecast Polling**: Fetches pollen forecasts for all 27 German regions.
- **Reference Data Emission**: Emits region metadata at startup so consumers can correlate forecasts.
- **German→English Mapping**: Maps German pollen type names to English in the event schema.
- **Deduplication**: Tracks the `last_update` timestamp to avoid reprocessing unchanged data.
- **Kafka Integration**: Sends forecasts to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=dwd-pollenflug
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/dwd-pollenflug
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m dwd_pollenflug`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the state file where the last seen update timestamp is stored. Defaults to `~/.dwd_pollenflug_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m dwd_pollenflug --connection-string "BootstrapServer=mybroker:9092;EntityPath=dwd-pollenflug"
```

#### Using Explicit Kafka Parameters

```bash
python -m dwd_pollenflug \
    --kafka-bootstrap-servers mybroker:9092 \
    --kafka-topic dwd-pollenflug
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | Set to `false` to disable TLS (default: `true`) |
| `DWD_POLLENFLUG_LAST_POLLED_FILE` | Path to the state file |
