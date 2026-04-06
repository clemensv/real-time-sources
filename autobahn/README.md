# German Autobahn Traffic Bridge

This bridge polls the German Autobahn API at
`https://verkehr.autobahn.de/o/autobahn` and forwards current roadworks,
traffic warnings, closures, entry and exit closures, weight-limit
restrictions, lorry parking metadata, electric charging station metadata, and
webcams to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams
as CloudEvents.

The API exposes current state rather than a change feed. The bridge therefore
polls the configured roads and resources, reuses ETags for conditional GETs,
and diffs the latest snapshot against its local state file to emit `appeared`,
`updated`, and `resolved` events.

## Data Source

- API endpoint: `https://verkehr.autobahn.de/o/autobahn`
- Format: JSON over HTTPS
- Authentication: none
- Update model: current-state snapshots with ETag support
- Coverage: all German Autobahns returned by the roads index

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

List the available Autobahns:

```bash
python -m autobahn roads
```

Start the bridge and publish events to Kafka:

```bash
python -m autobahn feed \
  --kafka-bootstrap-servers "localhost:9092" \
  --kafka-topic "autobahn" \
  --poll-interval 300
```

Or use an Event Hubs or Fabric Event Streams connection string:

```bash
python -m autobahn feed --connection-string "<connection-string>"
```

Limit the scan to selected roads and resources:

```bash
python -m autobahn feed \
  --connection-string "<connection-string>" \
  --roads A1,A3,A7 \
  --resources roadworks,warning,closure
```

## Environment Variables

The bridge accepts these environment variables when the corresponding command
line options are not supplied:

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs or Fabric Event Streams connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `autobahn` |
| `SASL_USERNAME` | SASL/PLAIN username | none |
| `SASL_PASSWORD` | SASL/PLAIN password | none |
| `KAFKA_ENABLE_TLS` | Use TLS when not using SASL | `true` |
| `AUTOBAHN_STATE_FILE` | State file for ETags and last-seen snapshots | `~/.autobahn_state.json` |
| `AUTOBAHN_POLL_INTERVAL` | Poll interval in seconds | `300` |
| `AUTOBAHN_RESOURCES` | Comma-separated resource list or `*` | all six resources |
| `AUTOBAHN_ROADS` | Comma-separated road list or `*` | all roads |
| `AUTOBAHN_REQUEST_CONCURRENCY` | Maximum concurrent Autobahn API requests | `16` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Modeling Notes

The upstream API uses resource-specific schemas and semantic `display_type`
values. The bridge preserves that split instead of flattening everything into a
single item type:

- Road-event payloads: roadworks, short-term roadworks, closures, entry/exit closures, weight-limit restrictions.
- Warning payloads: traffic warnings with delay, speed, and abnormal-traffic metadata.
- Parking payloads: lorry parking sites with parsed amenity and capacity fields.
- Charging payloads: charging stations with parsed charging-point details.
- Webcam payloads: camera metadata and media links.

CloudEvents `subject` and the Kafka key use the upstream `identifier`, which is
stable across the live network within each resource family.

## Testing

```bash
pytest tests/test_autobahn_unit.py
```

The repo-wide Docker Kafka flow test can also be run from the workspace root:

```bash
pytest tests/docker_e2e/test_docker_kafka_flow.py -v -k Autobahn
```