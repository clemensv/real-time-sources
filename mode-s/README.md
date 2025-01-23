# Mode-S Data Poller Usage Guide

## Overview

**Mode-S Data Poller** retrieves ADS-B data from dump1090 and sends updates to a Kafka topic.

### What is dump1090?

[dump1090](https://github.com/antirez/dump1090) is an open-source Mode S decoder specifically designed for RTLSDR devices. It captures ADS-B messages broadcast by aircraft and decodes them to provide real-time information about aircraft positions, velocities, and other parameters. dump1090 is commonly used with RTL-SDR dongles to set up low-cost ADS-B receivers.

### Recommended Forks and Tools

- **dump1090-fa**: The [FlightAware fork of dump1090](https://github.com/flightaware/dump1090) is the best-maintained version and includes additional features and improvements.
- **PiAware**: [PiAware](https://flightaware.com/adsb/piaware/install) is an easy way to set up dump1090-fa on a Raspberry Pi. It provides a complete package for ADS-B reception and integration with FlightAware.

### How dump1090 Receivers are Operated

dump1090 receivers are typically operated by connecting an RTL-SDR dongle to a computer or a Raspberry Pi. The software listens for ADS-B messages on 1090 MHz, decodes them, and provides the data via various endpoints, including a web interface and network ports.

### BEAST Endpoint

The BEAST endpoint is a binary protocol used by dump1090 to stream raw ADS-B messages over a network. By default, dump1090 provides this endpoint on port 30005. The Mode-S Data Poller connects to this endpoint to retrieve ADS-B data. Other receivers supporting BEAST output may also work with this tool.

## Key Features:
- **ADS-B Data Fetching**: Retrieve current ADS-B data from dump1090.
- **Kafka Integration**: Send ADS-B data updates as CloudEvents to a Kafka topic, supporting Microsoft Event Hubs and Microsoft Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or get it from the Microsoft Store if you are on Windows.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=mode-s
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/mode-s
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, run `mode_s.py`. It supports multiple subcommands:
- **Feed (`feed`)**: Continuously poll ADS-B data from dump1090 and send updates to a Kafka topic.

### **Feed (`feed`)**

Polls Mode-S data from dump1090 and sends them as CloudEvents to a Kafka topic. The events are formatted using CloudEvents in "structured" or "binary" mode.

Parameters:
- `--host`: Host name or IP address of dump1090 (default: $DUMP1090_HOST).
- `--port`: TCP port dump1090 listens on (default: $DUMP1090_PORT).
- `--ref-lat`: Latitude of the receiving antenna (default: $REF_LAT).
- `--ref-lon`: Longitude of the receiving antenna (default: $REF_LON).
- `--stationid`: Station ID for event source attribution (default: $STATIONID).
- `--kafka-bootstrap-servers`: Kafka servers (default: $KAFKA_BOOTSTRAP_SERVERS).
- `--kafka-topic`: Kafka topic to publish messages (default: $KAFKA_TOPIC).
- `--sasl-username`: Username for SASL authentication (default: $SASL_USERNAME).
- `--sasl-password`: Password for SASL authentication (default: $SASL_PASSWORD).
- `--connection-string`: Connection string for Microsoft Event Hubs or Fabric Event Streams (overrides other Kafka parameters; default: $CONNECTION_STRING).
- `--content-mode`: CloudEvent content mode (“structured” or “binary”; default: “structured”).

#### Example Usage:

```bash
mode_s.py feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>" --polling-interval 60
```

Alternatively, using a connection string for Microsoft Event Hubs or Microsoft Fabric Event Streams:

```bash
mode_s.py feed --connection-string "<your_connection_string>" --polling-interval 60
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

The connection string format is as follows:

```
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

When provided, the connection string is parsed to extract the Kafka configuration parameters:
- **Bootstrap Servers**: Derived from the `Endpoint` value.
- **Kafka Topic**: Derived from the `EntityPath` value.
- **SASL Username and Password**: The username is set to `'$ConnectionString'`, and the password is the entire connection string.

### Environment Variables
The tool supports the following environment variables to avoid passing them via the command line:
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers (comma-separated list).
- `KAFKA_TOPIC`: Kafka topic for publishing.
- `SASL_USERNAME`: SASL username for Kafka authentication.
- `SASL_PASSWORD`: SASL password for Kafka authentication.
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `POLLING_INTERVAL`: Polling interval in seconds.
- `DUMP1090_HOST`: Hostname or IP address of dump1090.
- `DUMP1090_PORT`: TCP port dump1090 listens on.
- `REF_LAT`: Latitude of your receiving antenna, required for decoding positions.
- `REF_LON`: Longitude of your receiving antenna, required for decoding positions.
- `STATIONID`: Station ID for event source attribution.

## State Management

The tool handles state internally for efficient API polling and sending updates.

