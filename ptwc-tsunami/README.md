# PTWC/NTWC Tsunami Bulletins Bridge

This bridge polls NOAA's tsunami warning Atom feeds for seismic event bulletins
and forwards them to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event
Streams as CloudEvents.

## Data Source

- PAAQ feed: `https://www.tsunami.gov/events/xml/PAAQAtom.xml` (Alaska/Pacific)
- PHEB feed: `https://www.tsunami.gov/events/xml/PHEBAtom.xml` (Pacific/Atlantic)
- Format: Atom XML with embedded XHTML summaries
- Authentication: none
- Coverage: Global (Pacific, Atlantic, and Caribbean)

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

```bash
python -m ptwc_tsunami --bootstrap-servers "localhost:9092" --poll-interval 300
```

Or use a connection string:

```bash
python -m ptwc_tsunami --connection-string "<connection-string>"
```

Limit to specific feeds:

```bash
python -m ptwc_tsunami --connection-string "<cs>" --feeds "PAAQ"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `ptwc-tsunami` |
| `SASL_USERNAME` | SASL username | none |
| `SASL_PASSWORD` | SASL password | none |
| `PTWC_TSUNAMI_STATE_FILE` | State file path | `~/.ptwc_tsunami_state.json` |
| `PTWC_TSUNAMI_POLL_INTERVAL` | Poll interval (seconds) | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_ptwc_tsunami.py
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventhub.json)
