# SIRI

[🐳 **Container images**](CONTAINER.md) · [📑 **Event schemas**](EVENTS.md) · [🗄️ **KQL schema**](kql/siri.kql)

SIRI (Service Interface for Real Time Information) is the CEN/European standard used by transit authorities and operators to publish live vehicle positions, estimated calls, and disruption information. The `siri` feeder turns those feeds into CloudEvents over **Kafka**, **MQTT**, and **AMQP** so journey planners, passenger-information systems, operations centers, and digital twins can react to vehicle movement and service status in real time.

The current parser normalizes SIRI Vehicle Monitoring (`VehicleActivity`) payloads and emits:

- `org.siri.Operator` — operator reference records observed in the current feed.
- `org.siri.VehiclePosition` — normalized vehicle-position telemetry.

> [!NOTE]
> You can configure `SIRI_DATA_TYPES=vm,et,sx`, but only payloads containing `VehicleActivity` elements produce telemetry events today.

## Transport variants

| Variant | Image | Default routing |
| --- | --- | --- |
| Kafka | `ghcr.io/clemensv/real-time-sources-siri-kafka` | topic `siri`, key `{operator_ref}/{vehicle_ref}` |
| MQTT | `ghcr.io/clemensv/real-time-sources-siri-mqtt` | `transit/siri/{operator_ref}/{vehicle_ref}/position` and `transit/siri/{operator_ref}/info` |
| AMQP | `ghcr.io/clemensv/real-time-sources-siri-amqp` | node `siri`, AMQP subject mirrors the CloudEvents subject |

## Configuring sources

The feeder ships a checked-in source catalog at `siri_core/siri_core/sources/siri-sources.json`. Use the catalog for repeatable deployments and keep the legacy single-source variables for one-off overrides.

| Variable | Purpose | Default |
| --- | --- | --- |
| `SIRI_SOURCES_FILE` | Path to a JSON catalog with SIRI source entries. Mount your own copy when you need private, regional, or key-protected services. | Packaged catalog |
| `SIRI_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled templates. When unset, entries with `enabled: true` run. | enabled entries |
| `SIRI_PROVIDER` | Legacy single-source provider profile. `bods`, `trafiklab`, `entur`, or `custom`. Takes precedence over the catalog when set to a non-default value. | `bods` |
| `SIRI_URL` | Legacy single-source endpoint URL or provider URL template. Takes precedence over the catalog whenever set. | provider default |
| `SIRI_API_KEY` / `BODS_API_KEY` | Optional upstream API key. Catalog entries should use `${ENV_VAR}` placeholders instead of inline secrets. | unset |
| `SIRI_OPERATORS` / `OPERATORS` | Optional comma-separated operator filter or `{operator}` URL-template values. | unset |
| `SIRI_DATA_TYPES` | Comma-separated `vm`, `et`, `sx` request families. | `vm` |
| `SIRI_HEADERS` | Optional semicolon-separated `Name=Value` request headers sent on every SIRI request. | unset |
| `SIRI_ET_CLIENT_NAME` | Convenience value for the `ET-Client-Name` header; provider `entur` gets a default when unset. | provider default |
| `POLLING_INTERVAL` | Poll interval in seconds. | `30` |
| `STATE_FILE` | Restart-safe dedupe state file. | `~/.siri_state.json` |
| `ONCE_MODE` | Run one polling cycle and exit. | `false` |

`SIRI_URL` or a non-default `SIRI_PROVIDER` preserves the legacy single-source path exactly: the feeder builds one `FeedConfig` from `SIRI_PROVIDER`, `SIRI_URL`, `SIRI_API_KEY` / `BODS_API_KEY`, `SIRI_OPERATORS` / `OPERATORS`, `SIRI_DATA_TYPES`, `SIRI_HEADERS`, and `SIRI_ET_CLIENT_NAME`, then ignores the catalog.

### Catalog format

```json
{
  "description": "SIRI source catalog...",
  "sources": [
    {
      "name": "uk-bods-bulk-archive",
      "enabled": true,
      "description": "UK Bus Open Data Service public bulk SIRI Vehicle Monitoring archive.",
      "provider": "bods",
      "siri_url": "https://data.bus-data.dft.gov.uk/avl/download/bulk_archive",
      "data_types": ["vm"]
    },
    {
      "name": "private-operator",
      "enabled": false,
      "description": "Private SIRI endpoint template.",
      "provider": "custom",
      "siri_url": "https://operator.example/siri/vm",
      "api_key": "${SIRI_API_KEY}",
      "headers": {"X-Api-Key": "${SIRI_API_KEY}"},
      "operators": ["operator-a"],
      "data_types": ["vm"],
      "et_client_name": "my-application"
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | ✅ | Stable catalog selector used by `SIRI_SOURCES`. |
| `enabled` | ❌ | Defaults to `true`; disabled templates are skipped unless `SIRI_SOURCES=*` or selected by name. |
| `description` | ✅ | Human-readable operator, geography, access, and key requirements. |
| `provider` | ❌ | Provider profile: `bods`, `trafiklab`, `entur`, or `custom`. Defaults to `bods`. |
| `siri_url` / `base_url` | ❌* | Direct SIRI endpoint URL or provider URL template. Required for `custom`; otherwise provider defaults apply. |
| `api_key` | ❌ | Optional upstream API key. Use `${ENV_VAR}` so secrets come from the runtime environment. |
| `operators` | ❌ | Array of operator filters or `{operator}` URL-template values. |
| `data_types` | ❌ | Array containing `vm`, `et`, and/or `sx`; the bridge currently emits events from `vm` payloads. |
| `headers` | ❌ | Object of request headers sent with every request. |
| `et_client_name` | ❌ | Convenience value for Entur-style `ET-Client-Name`. |

`*` `siri_url` can also be written as `base_url` for catalog readability.

### Selecting sources

- Unset `SIRI_SOURCES` — poll every catalog entry with `enabled: true`.
- `SIRI_SOURCES=uk-bods-bulk-archive,my-private-feed` — poll only those entries, in that order.
- `SIRI_SOURCES=*` — load every entry, including disabled templates. This is mostly useful for validation after editing a private catalog.
- Unknown names fail fast with a `ValueError` that lists known names.

### Keeping secrets out of the catalog

Put placeholders in the catalog and provide the secret at runtime:

```powershell
docker run --rm `
  -v ${PWD}\my-siri.sources.json:/app/siri-sources.json:ro `
  -e SIRI_SOURCES_FILE="/app/siri-sources.json" `
  -e SIRI_SOURCES="private-operator" `
  -e SIRI_API_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=siri" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

### Known SIRI sources

| Source | Provider profile | URL / portal | Key requirement | Notes |
| --- | --- | --- | --- | --- |
| UK Bus Open Data Service (BODS) bulk archive | `bods` | `https://data.bus-data.dft.gov.uk/avl/download/bulk_archive` | No key for the public bulk archive; BODS datafeed endpoints use an API key. | Checked into the default catalog as `uk-bods-bulk-archive`. |
| UK BODS filtered datafeed | `bods` | `https://data.bus-data.dft.gov.uk/avl/datafeed` | API key required. | Use legacy `SIRI_URL` or a private catalog entry when you need operator-specific filtering. |
| Norway Entur SIRI-Lite | `entur` | `https://api.entur.io/realtime/v1/rest/{data_type}` | No API key documented for the public endpoint; send an `ET-Client-Name` header. | Supports `vm`, `et`, and `sx` URL expansion. |
| Sweden / Nordic Trafiklab SIRI | `custom` | `https://opendata.samtrafiken.se/siri/{operator}/{data_type}?key=${TRAFIKLAB_SIRI_API_KEY}` | Trafiklab API key required in the documented `key` query parameter. | Checked into the default catalog as disabled `trafiklab-sweden`; set `SIRI_SOURCES=trafiklab-sweden` and provide `TRAFIKLAB_SIRI_API_KEY` to enable the ready-to-enable regional VM feed. |
| Ireland National Transport Authority developer portal | `custom` | `https://developer.nationaltransport.ie/` | Registration / subscription required. | Use the endpoint URL issued by NTA in a private catalog entry; do not commit personal URLs or keys. |

## Quick examples

### Catalog default: BODS to Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

### Trafiklab to MQTT

```bash
docker run --rm \
  -e SIRI_PROVIDER=trafiklab \
  -e SIRI_URL="https://api.trafiklab.se/siri2.x/{data_type}/{operator}" \
  -e SIRI_API_KEY="<trafiklab-api-key>" \
  -e SIRI_OPERATORS="skane/skanetrafiken,stockholm/sl" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  ghcr.io/clemensv/real-time-sources-siri-mqtt:latest
```

### Custom endpoint to AMQP

```bash
docker run --rm \
  -e SIRI_PROVIDER=custom \
  -e SIRI_URL="https://example.test/siri/vm" \
  -e SIRI_API_KEY="<api-key>" \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/siri" \
  ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

### Entur to Kafka

```bash
docker run --rm \
  -e SIRI_PROVIDER=entur \
  -e SIRI_DATA_TYPES=vm \
  -e SIRI_ET_CLIENT_NAME="my-application-name" \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
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
