# Elexon BMRS (GB Electricity Market) Poller

## Overview

**Elexon BMRS Poller** polls the Elexon Balancing Mechanism Reporting Service (BMRS) API for the latest GB electricity market data and sends it to a Kafka topic as CloudEvents. The tool tracks previously seen settlement periods to avoid sending duplicates.

## Key Features

- **Generation Mix Polling**: Fetch the latest generation outturn summary (MW by fuel type) from the BMRS API.
- **Demand Outturn Polling**: Fetch the latest national demand outturn data.
- **Deduplication**: Tracks last seen settlement periods in a state file to avoid reprocessing.
- **Kafka Integration**: Send events to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=elexon-bmrs
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/elexon-bmrs
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m elexon_bmrs`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where last seen settlement period timestamps are stored. Defaults to `~/.bmrs_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m elexon_bmrs --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m elexon_bmrs --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `BMRS_LAST_POLLED_FILE`: File to store last seen settlement period timestamps for deduplication.

## Data Source

The Elexon Balancing Mechanism Reporting Service (BMRS) provides real-time and near-real-time data about the GB electricity market. The data is published under the CC-BY 4.0 licence and requires no authentication.

- **API base**: `https://data.elexon.co.uk/bmrs/api/v1/`
- **Generation outturn**: `https://data.elexon.co.uk/bmrs/api/v1/generation/outturn/summary?format=json`
- **Demand outturn**: `https://data.elexon.co.uk/bmrs/api/v1/demand/outturn?format=json`
- **BMRS home page**: `https://www.elexon.co.uk/data/balancing-mechanism-reporting-agent/`

## License

[MIT](../LICENSE.md)
