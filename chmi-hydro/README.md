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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-with-eventhub.json)
