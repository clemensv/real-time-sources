# SIRI

[🐳 **Container images**](CONTAINER.md) · [📑 **Event schemas**](EVENTS.md) · [🗄️ **KQL schema**](kql/siri.kql)

The `siri` feeder is a generic SIRI bridge that emits CloudEvents over **Kafka**, **MQTT**, and **AMQP**. It keeps the existing SIRI 2.0 `VehicleActivity` parser and adds provider profiles so the same bridge can be pointed at multiple SIRI-compatible services.

## Provider profiles

- **`bods`** — UK Bus Open Data Service bulk ZIP download; API key sent as query parameter.
- **`trafiklab`** — Sweden Trafiklab per-operator endpoints; API key sent as header and the URL template can expand `{operator}` and `{data_type}`.
- **`custom`** — direct SIRI endpoint URL supplied by the user; API key can be attached as headers and query parameters.

## What the feeder emits

The bridge currently normalizes **SIRI Vehicle Monitoring** payloads and emits two event families:

- `org.siri.Operator` — operator reference records observed in the current feed.
- `org.siri.VehiclePosition` — normalized `VehicleActivity` telemetry records.

> [!NOTE]
> The parser is still focused on `VehicleActivity`. You can configure `SIRI_DATA_TYPES=vm,et,sx`, but only payloads that contain `VehicleActivity` elements produce telemetry events today.

## Transport variants

| Variant | Image | Default routing |
| --- | --- | --- |
| Kafka | `ghcr.io/clemensv/real-time-sources-siri-kafka` | topic `siri`, key `{operator_ref}/{vehicle_ref}` |
| MQTT | `ghcr.io/clemensv/real-time-sources-siri-mqtt` | `transit/siri/{operator_ref}/{vehicle_ref}/position` and `transit/siri/{operator_ref}/info` |
| AMQP | `ghcr.io/clemensv/real-time-sources-siri-amqp` | node `siri`, AMQP subject mirrors the CloudEvents subject |

## Configuration

Source configuration is shared across all three transports:

| Setting | CLI | Environment | Notes |
| --- | --- | --- | --- |
| provider | `--provider` | `SIRI_PROVIDER` | `bods`, `trafiklab`, `custom` (default `bods`) |
| source URL | `--siri-url` | `SIRI_URL` | Optional for `bods`; template/default for `trafiklab`; required for `custom` |
| API key | `--api-key` | `SIRI_API_KEY` | Required for authenticated providers |
| operators | `--operators` | `SIRI_OPERATORS` | Optional comma-separated filter / URL-template expansion values |
| data types | `--data-types` | `SIRI_DATA_TYPES` | Comma-separated `vm,et,sx`; default `vm` |
| polling interval | `--polling-interval` | `POLLING_INTERVAL` | Default `30` seconds |
| state file | `--state-file` | `STATE_FILE` | Restart-safe dedupe state |
| single-cycle run | `--once` | `ONCE_MODE` | Used by Docker E2E and the Fabric notebook |

## Quick examples

### BODS

```bash
docker run --rm \
  -e SIRI_PROVIDER=bods \
  -e SIRI_API_KEY="<bods-api-key>" \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

### Trafiklab

```bash
docker run --rm \
  -e SIRI_PROVIDER=trafiklab \
  -e SIRI_URL="https://api.trafiklab.se/siri2.x/{data_type}/{operator}" \
  -e SIRI_API_KEY="<trafiklab-api-key>" \
  -e SIRI_OPERATORS="skane/skanetrafiken,stockholm/sl" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  ghcr.io/clemensv/real-time-sources-siri-mqtt:latest
```

### Custom

```bash
docker run --rm \
  -e SIRI_PROVIDER=custom \
  -e SIRI_URL="https://example.test/siri/vm" \
  -e SIRI_API_KEY="<api-key>" \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/siri" \
  ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

## Fabric notebook hosting

Because this source is a poller, it also ships a Fabric notebook feeder in [`notebook/siri-feed.ipynb`](notebook/siri-feed.ipynb), deployable with `tools/deploy-fabric/deploy-feeder-notebook.ps1`.

## Repository layout

```text
siri/
  xreg/siri.xreg.json
  siri_core/
  siri_kafka/
  siri_mqtt/
  siri_amqp/
  siri_producer/
  siri_mqtt_producer/
  siri_amqp_producer/
  kql/
  notebook/
  tests/
```
