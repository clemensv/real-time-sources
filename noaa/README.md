# NOAA Data Poller Usage Guide

## Overview

**NOAA Data Poller** is a tool designed to interact with the NOAA (National Oceanic and Atmospheric Administration) API to fetch real-time environmental data from various NOAA stations. The tool can retrieve data such as water levels, air temperature, wind, and predictions, and send this data to a Kafka topic using SASL PLAIN authentication, making it suitable for integration with systems like Microsoft Event Hubs or Microsoft Fabric Event Streams.

## Key Features:
- **NOAA Data Polling**: Retrieve data for various NOAA products, including water levels, predictions, air temperature, wind, and more.
- **Station Support**: Poll data for all NOAA stations or specify a single station.
- **Kafka Integration**: Send NOAA data to a Kafka topic using SASL PLAIN authentication.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=noaa
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/noaa
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `noaa` command. It supports several arguments for configuring the polling process and sending data to Kafka.

The events sent to Kafka are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

### Command-Line Arguments

- `--last-polled-file`: Path to the file where the last polled times for each station and product are stored. Defaults to `~/.noaa_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).
- `--station`: (Optional) Station ID to poll data for. If not provided, data for all stations will be polled.

### Example Usage

#### Poll All Stations and Send Data to Kafka
```bash
noaa --connection-string "<your_connection_string>"
```

#### Poll a Specific Station and Send Data to Kafka
```bash
noaa --connection-string "<your_connection_string>" --station "<station_id>"
```

#### Using Kafka Parameters Directly
If you do not want to use a connection string, you can provide the Kafka parameters directly:

```bash
noaa --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

The tool supports providing a **connection string** for Microsoft Event Hubs or Microsoft Fabric Event Streams. This connection string simplifies the configuration by consolidating the Kafka bootstrap server, topic, username, and password.

#### Format:
```
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

When provided, the connection string is parsed to extract the following details:
- **Bootstrap Servers**: Derived from the `Endpoint` value.
- **Kafka Topic**: Derived from the `EntityPath` value.
- **SASL Username and Password**: The username is set to `'$ConnectionString'`, and the password is the entire connection string.

### Environment Variables

The tool also supports the following environment variables to avoid passing them via the command line:
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `NOAA_LAST_POLLED_FILE`: File to store the last polled times for each station and product.

## NOAA Products Supported

The following NOAA products are supported by the tool:
- **Water Level**: `water_level`
- **Predictions**: `predictions`
- **Air Temperature**: `air_temperature`
- **Wind**: `wind`
- **Air Pressure**: `air_pressure`
- **Water Temperature**: `water_temperature`
- **Conductivity**: `conductivity`
- **Visibility**: `visibility`
- **Humidity**: `humidity`
- **Salinity**: `salinity`

## Data Management

The tool polls NOAA data periodically and saves the last polled time in a file. This ensures that the tool only fetches new data in subsequent polling cycles.