# Hub'Eau Hydrométrie API Bridge

This project bridges the [Hub'Eau Hydrométrie
API](https://hubeau.eaufrance.fr/page/api-hydrometrie) to Apache Kafka, Azure
Event Hubs, or Microsoft Fabric Event Streams. It provides real-time water level
(height) and flow (discharge) data from approximately 6,300 monitoring stations
across France.

## Hub'Eau Hydrométrie API

Hub'Eau is a service provided by the French Ministry for an Ecological
Transition. The Hydrométrie API provides access to real-time water level and flow
data from hydrometric stations across metropolitan France and overseas
territories.

- **Stations**: ~6,300 monitoring stations
- **Parameters**: Water height (H, mm), Discharge (Q, L/s)
- **Update Frequency**: 5-60 minutes depending on station
- **Data Format**: JSON, GeoJSON

## Installation

```bash
pip install .
```

## Usage

### List Stations

```bash
python -m hubeau_hydrometrie list
```

### Get Latest Observations for a Station

```bash
python -m hubeau_hydrometrie level <code_station>
```

### Feed to Kafka

```bash
python -m hubeau_hydrometrie feed \
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
| `POLLING_INTERVAL` | Polling interval in seconds (default: 300) |

## Events

See [EVENTS.md](EVENTS.md) for detailed event schemas.

## Container

See [CONTAINER.md](CONTAINER.md) for container deployment instructions.

## Database Schemas

See [DATABASE.md](../DATABASE.md) for database integration.
