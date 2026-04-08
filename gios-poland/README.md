# GIOŚ Poland Air Quality Poller

## Overview

**GIOŚ Poland Air Quality Poller** polls the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality API for station metadata, sensor reference data, hourly measurements, and air quality index values, and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen measurement timestamps per sensor to avoid sending duplicates.

## Key Features

- **Station Reference Data**: Fetches all ~250 monitoring stations with location and administrative data at startup.
- **Sensor Reference Data**: Fetches sensor details (pollutant type) for each station at startup.
- **Hourly Measurements**: Polls measurements for PM10, PM2.5, SO₂, NO₂, O₃, CO, and benzene.
- **Air Quality Index**: Polls the Polish AQI with sub-indices per pollutant.
- **Deduplication**: Tracks last seen measurement timestamps to avoid reprocessing.
- **Kafka Integration**: Sends events to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=gios-poland
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/gios-poland
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m gios_poland`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where last seen timestamps per sensor are stored. Defaults to `~/.gios_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m gios_poland --connection-string "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=mykey;SharedAccessKey=secret123;EntityPath=gios-poland"
```

#### Using Kafka Parameters

```bash
python -m gios_poland \
    --kafka-bootstrap-servers "localhost:9092" \
    --kafka-topic "gios-poland" \
    --sasl-username "user" \
    --sasl-password "pass"
```
