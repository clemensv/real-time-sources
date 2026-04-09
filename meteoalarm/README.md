# Meteoalarm European Weather Warnings Bridge

This bridge polls the EUMETNET Meteoalarm API for severe weather warnings from
30+ European national meteorological services and forwards them to Apache
Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams as CloudEvents.

## Data Source

- API: `https://feeds.meteoalarm.org/api/v1/warnings/feeds-{country}`
- Format: JSON (CAP-structured)
- Authentication: none
- Coverage: 30+ European countries

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

```bash
python -m meteoalarm --bootstrap-servers "localhost:9092" --poll-interval 300
```

Or use a connection string:

```bash
python -m meteoalarm --connection-string "<connection-string>"
```

Limit to specific countries:

```bash
python -m meteoalarm --connection-string "<cs>" --countries "germany,france,spain"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `meteoalarm` |
| `SASL_USERNAME` | SASL username | none |
| `SASL_PASSWORD` | SASL password | none |
| `METEOALARM_STATE_FILE` | State file path | `~/.meteoalarm_state.json` |
| `METEOALARM_POLL_INTERVAL` | Poll interval (seconds) | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_meteoalarm.py
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-eventhub.json)
