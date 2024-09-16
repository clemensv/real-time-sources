## Usage

To use the `pegelonline` tool, you can run the following commands directly from the command line:

### 1. List All Stations

To retrieve a list of all available stations providing water level data:

```bash
pegelonline list
```

This command will output a list of all stations, each with its unique identifier (`uuid`) and short name.

### 2. Fetch Water Level for a Specific Station

To get the current water level for a specific station, use the station's short name:

```bash
pegelonline level <shortname>
```

Replace `<shortname>` with the desired station's short name (e.g., `KOLN` for the Cologne station).

**Example:**

```bash
pegelonline level KOLN
```

This will display the current water level measurement in a formatted JSON output.

### 3. Feed Water Level Updates to a Kafka Topic or Event Hub

To continuously stream water level updates to a specified Kafka topic or Microsoft Event Hub:

```bash
pegelonline feed --kafka-bootstrap-servers <servers> --kafka-topic <topic> --sasl-username <username> --sasl-password <password> --polling-interval <interval>
```

Alternatively, you can use a connection string for Microsoft Event Hub:

```bash
pegelonline feed --connection-string <connection_str> --polling-interval <interval>
```

#### Options

- `--kafka-bootstrap-servers <servers>`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic <topic>`: Kafka topic to send messages to.
- `--sasl-username <username>`: Username for SASL PLAIN authentication.
- `--sasl-password <password>`: Password for SASL PLAIN authentication.
- `--connection-string <connection_str>`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `--polling-interval <interval>`: Polling interval in seconds (default is 60 seconds).

#### Example

To stream updates to a Kafka topic:

```bash
pegelonline feed --kafka-bootstrap-servers "your.kafka.server:9092" --kafka-topic "your-kafka-topic" --sasl-username "your-username" --sasl-password "your-password" --polling-interval 30
```

This command will continuously fetch water level data from all stations and send updates to the specified Kafka topic or Event Hub at the defined polling interval.