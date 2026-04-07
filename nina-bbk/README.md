# NINA/BBK German Civil Protection Warnings Bridge

This bridge polls Germany's NINA/BBK warning system for civil protection
warnings and forwards them to Apache Kafka, Azure Event Hubs, or Microsoft
Fabric Event Streams as CloudEvents.

## Data Source

- Map data API: `https://warnung.bund.de/api31/{provider}/mapData.json`
- Detail API: `https://warnung.bund.de/api31/warnings/{warning_id}.json`
- Format: JSON (CAP-structured)
- Authentication: none
- Coverage: Germany (federal, state, and municipal warnings)

## Providers

| Provider | Source |
|---|---|
| `mowas` | Federal civil protection (BBK) |
| `katwarn` | Municipal warning system |
| `biwapp` | Municipal warning app |
| `dwd` | German Weather Service |
| `lhp` | State flood centers |
| `police` | Police services |

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

```bash
python -m nina_bbk --bootstrap-servers "localhost:9092" --poll-interval 300
```

Or use a connection string:

```bash
python -m nina_bbk --connection-string "<connection-string>"
```

Limit to specific providers:

```bash
python -m nina_bbk --connection-string "<cs>" --providers "mowas,dwd"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `nina-bbk` |
| `SASL_USERNAME` | SASL username | none |
| `SASL_PASSWORD` | SASL password | none |
| `NINA_BBK_STATE_FILE` | State file path | `~/.nina_bbk_state.json` |
| `NINA_BBK_POLL_INTERVAL` | Poll interval (seconds) | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_nina_bbk.py
```
