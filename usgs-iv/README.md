# USGS Water Services - Instantaneous Value Service Usage Guide

## Overview

**USGS-IV** is a tool designed to interact with the [USGS Water Services](https://waterservices.usgs.gov/) Instantaneous Value Service API to fetch water level data for rivers in the United States. The tool can retrieve water level data from individual stations, list available stations, or continuously poll the API to send water level updates to a Kafka topic.

## Key Features:
- **Water Level Fetching**: Retrieve current water level data for specific stations from the USGS Instantaneous Value Service API.
- **Station Listing**: List all available monitoring stations.
- **Kafka Integration**: Send water level updates as CloudEvents to a Kafka topic, supporting Microsoft Event Hubs and Microsoft Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or get it from the Microsoft Store if you are on Windows.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=usgs-iv
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/usgs-iv
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `usgs-iv` command. It supports multiple subcommands:
- **List Stations (`sites`)**: Fetch and display all available monitoring stations.
- **Feed Stations (`feed`)**: Continuously poll usgs-iv API for water levels and send updates to a Kafka topic.

### **List Stations (`sites`)**

Fetches and displays all available monitoring stations from the usgs-iv API.

#### Example Usage:

```bash
usgs-iv sites
```

### **Feed Stations (`feed`)**

Polls the usgs-iv API for water level measurements and sends them as
CloudEvents to a Kafka topic. The events are formatted using CloudEvents
structured JSON format and described in [EVENTS.md](EVENTS.md).

- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream [connection string](#connection-string-for-microsoft-event-hubs-or-fabric-event-streams) (overrides other Kafka parameters).


#### Example Usage:

```bash
usgs-iv feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>" --polling-interval 60
```

Alternatively, using a connection string for Microsoft Event Hubs or Microsoft Fabric Event Streams:

```bash
usgs-iv feed --connection-string "<your_connection_string>" --polling-interval 60
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

## State Management

The tool handles state internally for efficient API polling and sending updates.

