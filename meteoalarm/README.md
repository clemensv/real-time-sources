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
