# UK Environment Agency Flood Monitoring API Bridge

This project bridges the [UK Environment Agency Flood Monitoring
API](https://environment.data.gov.uk/flood-monitoring/doc/reference) to Apache
Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams. It provides
real-time water level and flow data from approximately 4,000 monitoring stations
across England.

## UK EA Flood Monitoring API

The Environment Agency's real-time flood monitoring API provides access to water
level, flow, and rainfall data from monitoring stations across England. The
service is free to use, requires no authentication, and updates every 15
minutes.

- **Stations**: ~4,000 monitoring stations across England
- **Parameters**: Water Level, Flow, Rainfall, Wind, Temperature
- **Update Frequency**: Every 15 minutes
- **Data Format**: JSON (Linked Data)

## Installation

```bash
pip install .
```

## Usage

### List Stations

```bash
python -m uk_ea_flood_monitoring list
```

### Get Latest Reading for a Station

```bash
python -m uk_ea_flood_monitoring level <station_reference>
```

### Feed to Kafka

```bash
python -m uk_ea_flood_monitoring feed \
  --kafka-bootstrap-servers <servers> \
  --kafka-topic <topic> \
  --sasl-username <username> \
  --sasl-password <password>
```

### Feed with Connection String

```bash
python -m uk_ea_flood_monitoring feed \
  -c "Endpoint=sb://...;EntityPath=...;SharedAccessKeyName=...;SharedAccessKey=..."
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CONNECTION_STRING` | Microsoft Event Hubs or Fabric Event Stream connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated list of Kafka bootstrap servers |
| `KAFKA_TOPIC` | Kafka topic name |
| `SASL_USERNAME` | SASL PLAIN username |
| `SASL_PASSWORD` | SASL PLAIN password |
| `POLLING_INTERVAL` | Polling interval in seconds (default: 900) |

## Events

The bridge emits the following CloudEvents:

- `UK.Gov.Environment.EA.FloodMonitoring.Station` - Station reference data
  (sent once at startup)
- `UK.Gov.Environment.EA.FloodMonitoring.Reading` - Water level/flow readings
  (sent every polling interval)

See [EVENTS.md](EVENTS.md) for detailed event schemas.

## Container

See [CONTAINER.md](CONTAINER.md) for container deployment instructions.

## Database Schemas

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).
