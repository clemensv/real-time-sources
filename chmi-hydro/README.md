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

- **Fabric notebook hosting (recommended for Fabric users):** Deploy this bridge as a scheduled Fabric notebook with `tools/deploy-fabric/deploy-feeder-notebook.ps1`. It auto-builds the per-source Environment, looks up the Event Stream connection string at runtime, and schedules `chmi-hydro feed --once`.

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

## MQTT / Unified Namespace transport

In addition to the Kafka image documented in `CONTAINER.md`, this source
also ships an MQTT 5.0 feeder built from `Dockerfile.mqtt`. It publishes
the same Station reference and WaterLevelObservation telemetry into a
Unified-Namespace topic tree:

```
hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/info
hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/water-level
```

All messages are sent in CloudEvents *binary* mode with QoS 1 and
`retain=true` so any new subscriber immediately sees the latest known
state per station. The `{stream_name}` segment is normalized to lowercase
kebab-case (umlauts and accented characters folded to ASCII, all other
non-alphanumeric characters replaced with `-`) so the topic is safe for
every MQTT 5 broker.

See `CONTAINER.md` for the full deployment contract (environment
variables, broker examples, subscription patterns).

## AMQP 1.0 companion feeder

This source now ships the standard Kafka + MQTT + AMQP transport trio. The AMQP companion runs from `chmi_hydro_amqp/`, uses the generated `chmi_hydro_amqp_producer/` package, and publishes the same CloudEvents and schemas documented in `EVENTS.md` to one AMQP 1.0 address (default `chmi-hydro`). It supports generic AMQP 1.0 brokers with SASL PLAIN and Azure Service Bus / Event Hubs with CBS token authentication.

Build and run locally:

```bash
docker build -f Dockerfile.amqp -t chmi-hydro-amqp .
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/chmi-hydro \
  -e ONCE_MODE=true \
  chmi-hydro-amqp
```

For Azure Service Bus, deploy `azure-template-with-servicebus.json` (also mirrored at `infra/azure-template-amqp.json`) or run the container with `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_TLS=true`, and `AMQP_ADDRESS=chmi-hydro`.

