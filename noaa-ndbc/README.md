# NOAA NDBC Buoy Observations Poller

## Overview

**NOAA NDBC Buoy Observations Poller** polls the National Data Buoy Center (NDBC) for the latest buoy observations across the United States and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen observation timestamps per station to avoid sending duplicates.

## Key Features

- **NDBC Observations Polling**: Fetch the latest buoy observations from `https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt`.
- **Deduplication**: Tracks last seen observation timestamp per station in a state file to avoid reprocessing.
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

## NDBC Buoy Observation Properties

Each buoy observation includes these properties:

| Property | Type | Unit | Description |
|----------|------|------|-------------|
| `station_id` | string | — | NDBC station identifier |
| `latitude` | double | degrees | Station latitude |
| `longitude` | double | degrees | Station longitude |
| `timestamp` | string | — | ISO timestamp of observation |
| `wind_direction` | double | degrees | Wind direction |
| `wind_speed` | double | m/s | Wind speed |
| `gust` | double | m/s | Wind gust speed |
| `wave_height` | double | meters | Significant wave height |
| `dominant_wave_period` | double | seconds | Dominant wave period |
| `average_wave_period` | double | seconds | Average wave period |
| `mean_wave_direction` | double | degrees | Mean wave direction |
| `pressure` | double | hPa | Sea level pressure |
| `air_temperature` | double | celsius | Air temperature |
| `water_temperature` | double | celsius | Sea surface temperature |
| `dewpoint` | double | celsius | Dewpoint temperature |

## Data Source

The NOAA National Data Buoy Center (NDBC) maintains a network of approximately 1,300 buoys and coastal stations that measure meteorological and oceanographic conditions. Observations include wind, waves, atmospheric pressure, air and sea surface temperatures. Data is updated approximately every 5 minutes.

- **Latest observations**: `https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt`
- **NDBC home page**: `https://www.ndbc.noaa.gov/`

## License

[MIT](../LICENSE.md)
