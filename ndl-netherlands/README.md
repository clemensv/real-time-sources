# Netherlands NDL EV Charging Bridge

This bridge downloads the OCPI v2.2 data published by the Dutch Nationale
Databank Laadinfrastructuur (NDL) at `https://opendata.ndw.nu` and forwards
charging-location metadata, EVSE status changes, and tariff data to Apache
Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams as CloudEvents.

The upstream files are gzip-compressed JSON snapshots updated every few minutes.
The bridge polls these files, emits all location and tariff reference data on
the first cycle, and then tracks EVSE status changes using a local state file
so only deltas are produced on subsequent cycles.

## Data Source

- Locations: `https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz`
- Tariffs: `https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz`
- Format: gzip-compressed JSON (OCPI v2.2)
- Authentication: none
- Typical volume: ~87,000 locations, ~219,000 EVSEs, ~115,000 tariffs

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

Start the bridge and publish events to Kafka:

```bash
python -m ndl_netherlands \
  --bootstrap-servers "localhost:9092" \
  --poll-interval 300
```

Or use an Event Hubs or Fabric Event Streams connection string:

```bash
python -m ndl_netherlands --connection-string "<connection-string>"
```

Run a single poll cycle and exit:

```bash
python -m ndl_netherlands --connection-string "<connection-string>" --once
```

## Environment Variables

The bridge accepts these environment variables when the corresponding command
line options are not supplied:

| Variable | Description | Default |
|---|---|---|
| `NDL_CONNECTION_STRING` | Event Hubs / Fabric connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_SASL_USERNAME` | SASL/PLAIN username | none |
| `KAFKA_SASL_PASSWORD` | SASL/PLAIN password | none |
| `NDL_CHARGING_TOPIC` | Kafka topic for locations and EVSE events | `ndl-charging` |
| `NDL_TARIFFS_TOPIC` | Kafka topic for tariff events | `ndl-charging-tariffs` |
| `NDL_STATE_FILE` | State file for change detection | `~/.ndl_netherlands_state.json` |
| `NDL_POLL_INTERVAL` | Poll interval in seconds | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_ndl_netherlands.py
```

The repo-wide Docker Kafka flow test can also be run from the workspace root:

```bash
pytest tests/docker_e2e/test_docker_kafka_flow.py -v -k NdlNetherlands
```
