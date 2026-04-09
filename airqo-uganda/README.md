# AirQo Uganda Air Quality Poller

## Overview

**AirQo Uganda Air Quality Poller** polls the AirQo API for the latest air quality measurements from low-cost sensors deployed across Uganda and East Africa, and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen measurement timestamps per device to avoid sending duplicates.

## Key Features

- **Site Reference Data**: Fetches site metadata from the public AirQo grids summary endpoint at startup.
- **Air Quality Polling**: Fetches the latest PM2.5, PM10, temperature, and humidity measurements from AirQo sensors.
- **Deduplication**: Tracks last seen measurement timestamp per device in a state file to avoid reprocessing.
- **Kafka Integration**: Sends measurements to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=airqo-uganda
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/airqo-uganda
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m airqo_uganda`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--api-key`: AirQo API key for authenticated endpoints (env: `AIRQO_API_KEY`).
- `--state-file`: Path to the file where last seen timestamps per device are stored. Defaults to `~/.airqo_uganda_state.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).
- `--polling-interval`: Polling interval in seconds (default: 300).

### Example Usage

#### Using a Connection String

```bash
python -m airqo_uganda --connection-string "<your_connection_string>" --api-key "<your_api_key>"
```

#### Using Kafka Parameters Directly

```bash
python -m airqo_uganda --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>" --api-key "<your_api_key>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `AIRQO_API_KEY`: API key for authenticated AirQo endpoints.
- `STATE_FILE`: File to store last seen timestamps per device for deduplication.
- `POLLING_INTERVAL`: Polling interval in seconds.

## AirQo Measurement Properties

Each air quality measurement includes these properties:

| Property | Type | Unit | Description |
|----------|------|------|-------------|
| `site_id` | string | — | AirQo site identifier |
| `device` | string | — | Device name |
| `device_id` | string | — | AirQo device identifier |
| `timestamp` | string | — | ISO timestamp of measurement |
| `pm2_5_raw` | double | µg/m³ | Raw PM2.5 concentration |
| `pm2_5_calibrated` | double | µg/m³ | Calibrated PM2.5 concentration |
| `pm10_raw` | double | µg/m³ | Raw PM10 concentration |
| `pm10_calibrated` | double | µg/m³ | Calibrated PM10 concentration |
| `temperature` | double | °C | Ambient air temperature |
| `humidity` | double | % | Relative humidity |
| `latitude` | double | degrees | Measurement location latitude |
| `longitude` | double | degrees | Measurement location longitude |
| `frequency` | string | — | Measurement frequency |

## Data Source

AirQo operates a network of over 100 low-cost air quality sensors primarily deployed across Uganda, with expanding coverage in East Africa. The sensors measure particulate matter (PM2.5 and PM10), temperature, and humidity. Data is updated approximately every hour and includes both raw sensor readings and machine-learning-calibrated values.

- **API endpoint**: `https://api.airqo.net/api/v2/`
- **AirQo home page**: `https://airqo.net/`
- **API documentation**: `https://docs.airqo.net/`

## License

[MIT](../LICENSE.md)
