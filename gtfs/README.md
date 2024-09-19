# GTFS and GTFS-RT API Bridge Usage Guide

## Overview

**GTFS and GTFS-RT API Bridge** is a tool that fetches GTFS (General Transit Feed Specification) Realtime and Static data from various transit agency sources, processes the data, and publishes it to Kafka topics using SASL PLAIN authentication. This tool can be integrated with systems like Microsoft Event Hubs or Microsoft Fabric Event Streams.

GTFS is a set of open data standards for public transportation schedules and
associated geographic information. GTFS-RT is a real-time extension to GTFS that
allows public transportation agencies to provide real-time updates about their
fleet. Over 2000 transit agencies worldwide provide GTFS and GTFS-RT data.

The [Mobility Database](mobilitydatabase.org) provides a comprehensive list of GTFS
and GTFS-RT feeds from around the world. 

## Key Features:
- **GTFS-RT Data Polling**: Poll GTFS Realtime feeds for vehicle positions, trip updates, and alerts.
- **GTFS Static Data Processing**: Fetch GTFS static data (routes, stops, schedules) and send it to Kafka topics.
- **Kafka Integration**: Supports sending data to Kafka topics using SASL PLAIN authentication.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=gtfs
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/gtfs
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `gtfs` command. It supports several arguments for configuring the polling process and sending data to Kafka.

The events sent to Kafka are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

### `feed` Command-Line Arguments

- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).
- `--gtfs-rt-urls`: URL(s) for GTFS Realtime feeds.
- `--gtfs-urls`: URL(s) for GTFS Static schedule feeds.
- `--mdb-source-id`: Mobility Database source ID for GTFS Realtime or Static feeds.
- `--agency`: Agency ID to poll data for.
- `--route`: (Optional) Route ID to poll data for. If not provided, data for all routes will be polled.
- `--poll-interval`: Interval in seconds to wait between polling vehicle locations.
- `--force-schedule-refresh`: Force a refresh of the GTFS schedule data.

### Example Usage

#### Poll GTFS-RT and Send Data to Kafka
```bash
gtfs feed --connection-string "<your_connection_string>"
```

#### Poll a Specific Route for Vehicle Data
```bash
gtfs feed --connection-string "<your_connection_string>" --route "<route_id>"
```

#### Using Kafka Parameters Directly
If you do not want to use a connection string, you can provide the Kafka parameters directly:

```bash
gtfs feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

You can provide a **connection string** for Microsoft Event Hubs or Microsoft Fabric Event Streams to simplify the configuration by consolidating the Kafka bootstrap server, topic, username, and password.

#### Format:
```
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

### Additional Commands

#### Print GTFS Realtime Feed Data
Prints the GTFS-RT data for a single request:

```bash
gtfs printfeed --gtfs-rt-url "<gtfs_rt_url>"
```

#### List Agencies
Lists the agencies in the Mobility Database:

```bash
gtfs agencies
```

#### List Routes
Lists the routes from a GTFS Static feed:

```bash
gtfs routes --gtfs-url "<gtfs_url>"
```

#### List Stops
Lists the stops for a given route:

```bash
gtfs stops --route "<route_id>" --gtfs-url "<gtfs_url>"
```

## Environment Variables

You can avoid passing parameters via the command line by setting the following environment variables:
- `KAFKA_BOOTSTRAP_SERVERS`: List of Kafka bootstrap servers.
- `KAFKA_TOPIC`: Kafka topic to send messages to.
- `SASL_USERNAME`: Username for SASL PLAIN authentication.
- `SASL_PASSWORD`: Password for SASL PLAIN authentication.
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `GTFS_RT_URLS`: Comma-separated list of GTFS Realtime feed URLs.
- `GTFS_URLS`: Comma-separated list of GTFS Static schedule feed URLs.
- `MDB_SOURCE_ID`: Mobility Database source ID for the GTFS feed.
- `AGENCY`: Agency ID to poll data for.

### CloudEvents Mode
You can specify the CloudEvents mode (either `structured` or `binary`) when sending data to Kafka:

```bash
gtfs feed --cloudevents-mode structured
```