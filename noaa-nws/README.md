# NOAA NWS Weather Alerts Poller

## Overview

**NOAA NWS Weather Alerts Poller** polls the National Weather Service (NWS) Weather Alerts API for active weather alerts across the United States and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen alert IDs to avoid sending duplicates.

## Key Features

- **NWS Alerts Polling**: Fetch active weather alerts from the NWS API at `https://api.weather.gov/alerts/active`.
- **Deduplication**: Tracks seen alert IDs in a state file to avoid reprocessing.
- **Kafka Integration**: Send weather alerts to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=noaa-nws
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/noaa-nws
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m noaa_nws`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where seen alert IDs are stored. Defaults to `~/.nws_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m noaa_nws --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m noaa_nws --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `NWS_LAST_POLLED_FILE`: File to store seen alert IDs for deduplication.

## NWS Alert Properties

Each weather alert includes these properties:

| Property | Description |
|----------|-------------|
| `alert_id` | NWS alert ID |
| `area_desc` | Description of affected area |
| `sent` | When the alert was sent |
| `effective` | When the alert becomes effective |
| `expires` | When the alert expires |
| `status` | Alert status (Actual, Exercise, System, Test, Draft) |
| `message_type` | Message type (Alert, Update, Cancel) |
| `category` | Category (Met, Geo, Safety, etc.) |
| `severity` | Severity (Extreme, Severe, Moderate, Minor, Unknown) |
| `certainty` | Certainty (Observed, Likely, Possible, Unlikely, Unknown) |
| `urgency` | Urgency (Immediate, Expected, Future, Past, Unknown) |
| `event` | Event type name |
| `sender_name` | Name of the sending office |
| `headline` | Alert headline |
| `description` | Full description |
