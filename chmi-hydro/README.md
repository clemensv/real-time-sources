# ČHMÚ Hydrological Data Bridge

This bridge fetches real-time hydrological data from the Czech
Hydrometeorological Institute (ČHMÚ) open data portal and forwards it to
Apache Kafka or Microsoft Azure Event Hubs as CloudEvents.

The ČHMÚ provides real-time water level, discharge, and water temperature data
for hundreds of hydrological stations across the Czech Republic, updated every
10 minutes.

## Data Source

- **API Endpoint**: https://opendata.chmi.cz/hydrology/now/
- **Data Format**: JSON (individual files per station)
- **Update Frequency**: Every 10 minutes
- **Authentication**: None required (open data)
- **License**: Open data from ČHMÚ (Český hydrometeorologický ústav)

## Data Attribution

Zdrojem dat je Český hydrometeorologický ústav (ČHMÚ). The data source is the
Czech Hydrometeorological Institute.

## Events

See [EVENTS.md](EVENTS.md) for details on the CloudEvents produced by this
bridge.

## Deployment

See [CONTAINER.md](CONTAINER.md) for container deployment instructions.

## Usage

### List all stations

```bash
python -m chmi_hydro list
```

### Get water level for a specific station

```bash
python -m chmi_hydro level 0-203-1-001000
```

### Feed data to Kafka

```bash
python -m chmi_hydro feed --connection-string "<connection_string>" --topic chmi-hydro
```

Or using environment variables:

```bash
export KAFKA_BROKER=localhost:9092
export KAFKA_TOPIC=chmi-hydro
python -m chmi_hydro feed
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `KAFKA_CONNECTION_STRING` or `CONNECTION_STRING` | Kafka/Event Hubs connection string | None |
| `KAFKA_BROKER` | Kafka bootstrap server | None |
| `KAFKA_TOPIC` | Kafka topic name | `chmi-hydro` |
| `POLLING_INTERVAL` | Polling interval in seconds | `600` |

## Setup

```bash
pip install -r requirements.txt
pip install -e .
```

## Testing

```bash
pytest tests/test_chmi_hydro_unit.py      # Unit tests (no network)
pytest tests/test_chmi_hydro_e2e.py        # End-to-end tests (hits real API)
pytest tests/test_chmi_hydro_container.py  # Container tests (requires Docker)
```
