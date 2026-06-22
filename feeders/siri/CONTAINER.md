# SIRI Kafka, MQTT, and AMQP containers

[📘 **Overview**](README.md) · [📑 **Event schemas**](EVENTS.md) · [🗄️ **KQL schema**](kql/siri.kql)

SIRI containers turn European transit real-time feeds into CloudEvents for passenger information, dispatch operations, mobility analytics, and event-driven digital twins. The same source catalog and legacy single-source variables are shared by the Kafka, MQTT, and AMQP images.

## Image contract

| Image | Dockerfile | Transport | State share |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-siri-kafka:latest` | `Dockerfile` | Kafka/Event Hubs | Optional `STATE_FILE`. |
| `ghcr.io/clemensv/real-time-sources-siri-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5 | Optional `STATE_FILE`; broker retained state stores LKV. |
| `ghcr.io/clemensv/real-time-sources-siri-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 | Optional `STATE_FILE`. |

## Common environment

| Variable | Description | Default |
| --- | --- | --- |
| `SIRI_SOURCES_FILE` | Path to a SIRI source catalog JSON file. See [README.md#configuring-sources](README.md#configuring-sources). | Packaged catalog |
| `SIRI_SOURCES` | Comma-separated catalog entry `name`s, or `*` for all entries including disabled templates. Unset runs entries with `enabled: true`. | enabled entries |
| `SIRI_PROVIDER` | Legacy single-source provider profile. `bods`, `trafiklab`, `entur`, or `custom`; non-default values take precedence over the catalog. | `bods` |
| `SIRI_URL` | Legacy single-source endpoint URL or provider URL template; takes precedence over the catalog whenever set. | provider default |
| `SIRI_API_KEY` / `BODS_API_KEY` | Optional runtime upstream API key. Catalog entries should use `${ENV_VAR}` in their `api_key` or `headers` fields instead. | unset |
| `SIRI_OPERATORS` / `OPERATORS` | Optional comma-separated operator filter or `{operator}` URL-template values. | unset |
| `SIRI_DATA_TYPES` | Comma-separated `vm`, `et`, `sx` request families; the bridge emits events from Vehicle Monitoring payloads. | `vm` |
| `SIRI_HEADERS` | Optional semicolon-separated `Name=Value` request headers sent on every SIRI request. | unset |
| `SIRI_ET_CLIENT_NAME` | Convenience value for the `ET-Client-Name` header; provider `entur` gets a default when unset. | provider default |
| `POLLING_INTERVAL` | Poll interval in seconds. | `30` |
| `STATE_FILE` | JSON dedupe state file. Mount persistent storage here for long-running deployments. | `~/.siri_state.json` |
| `ONCE_MODE` | Run one polling cycle and exit. Required for Fabric notebook hosting and useful for smoke tests. | `false` |
| `LOG_LEVEL` | Standard Python logging level. | `INFO` |

## Configuring sources

The default image includes `siri_core/sources/siri-sources.json`, with `uk-bods-bulk-archive` enabled. Set `SIRI_SOURCES` to select names from that catalog, or mount your own JSON file and set `SIRI_SOURCES_FILE`.

Catalog entries support `name`, `enabled`, `description`, `provider`, `siri_url` / `base_url`, optional `api_key`, optional `operators`, optional `data_types`, optional `headers`, and optional `et_client_name`. Secrets should be written as `${ENV_VAR}` in the catalog and supplied with `-e` at runtime. The full catalog format, selector behavior, and known-source table live in [README.md#configuring-sources](README.md#configuring-sources).

Example with a mounted private catalog and runtime secret:

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

Legacy quick override without a catalog:

```powershell
docker run --rm `
  -e SIRI_PROVIDER=custom `
  -e SIRI_URL="https://example.test/siri/vm" `
  -e SIRI_API_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=siri" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

### Catalog format

```json
{
  "sources": [
    {
      "name": "uk-bods-bulk-archive",
      "enabled": true,
      "description": "UK Bus Open Data Service public bulk SIRI Vehicle Monitoring archive.",
      "provider": "bods",
      "siri_url": "https://data.bus-data.dft.gov.uk/avl/download/bulk_archive",
      "data_types": ["vm"]
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | ✅ | Stable catalog selector used by `SIRI_SOURCES`. |
| `enabled` | ❌ | Defaults to `true`; disabled templates are skipped unless `SIRI_SOURCES=*` or selected by name. |
| `description` | ✅ | Human-readable operator, geography, access, and key requirements. |
| `provider` | ❌ | Provider profile: `bods`, `trafiklab`, `entur`, or `custom`. |
| `siri_url` / `base_url` | ❌* | Direct endpoint URL or provider URL template. Required for `custom`; otherwise provider defaults apply. |
| `api_key` | ❌ | Optional upstream API key. Use `${ENV_VAR}` so secrets come from the runtime environment. |
| `operators` | ❌ | Array of operator filters or `{operator}` URL-template values. |
| `data_types` | ❌ | Array containing `vm`, `et`, and/or `sx`. |
| `headers` | ❌ | Object of request headers sent with every request. |
| `et_client_name` | ❌ | Convenience value for Entur-style `ET-Client-Name`. |

`*` `siri_url` can also be written as `base_url` for catalog readability.

### Selecting sources

- Unset `SIRI_SOURCES` — poll every catalog entry with `enabled: true`.
- `SIRI_SOURCES=uk-bods-bulk-archive,my-private-feed` — poll only those entries, in that order.
- `SIRI_SOURCES=*` — load every entry, including disabled templates.
- Unknown names fail fast with a `ValueError` that lists known names.

### Keeping secrets out of the catalog

Use `${BODS_API_KEY}` or `${SIRI_API_KEY}` placeholders in the mounted catalog and pass the secret as an environment variable. Do not commit catalog copies containing concrete keys.

```powershell
docker run --rm `
  -v ${PWD}\my-siri.sources.json:/app/siri-sources.json:ro `
  -e SIRI_SOURCES_FILE="/app/siri-sources.json" `
  -e SIRI_SOURCES="uk-bods-filtered" `
  -e BODS_API_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=siri" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

### Known SIRI sources

| Source | URL / portal | Key requirement |
| --- | --- | --- |
| UK BODS bulk archive | `https://data.bus-data.dft.gov.uk/avl/download/bulk_archive` | No key for the public bulk archive. |
| UK BODS filtered datafeed | `https://data.bus-data.dft.gov.uk/avl/datafeed` | API key required. |
| Norway Entur SIRI-Lite | `https://api.entur.io/realtime/v1/rest/{data_type}` | Send `ET-Client-Name`; no API key documented for the public endpoint. |
| Sweden / Nordic Trafiklab SIRI | `https://opendata.samtrafiken.se/siri/{operator}/{data_type}?key=${TRAFIKLAB_SIRI_API_KEY}` | Trafiklab API key required; disabled catalog entry `trafiklab-sweden` is ready to enable with `SIRI_SOURCES=trafiklab-sweden`. |
| Ireland NTA developer portal | `https://developer.nationaltransport.ie/` | Registration / subscription required; use the issued endpoint URL in a private catalog. |

## Kafka image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

### Environment variables

| Variable | Required | Default | Description |
| --- | ---: | ---: | --- |
| `CONNECTION_STRING` | ✅* | — | Event Hubs / Fabric Event Stream or plain `BootstrapServer=...;EntityPath=...` connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | ✅* | — | Bootstrap servers when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | ❌ | `siri` | Kafka topic to publish into. |
| `SASL_USERNAME` | ❌ | — | SASL PLAIN username when not using `CONNECTION_STRING`. |
| `SASL_PASSWORD` | ❌ | — | SASL PLAIN password when not using `CONNECTION_STRING`. |
| `KAFKA_ENABLE_TLS` | ❌ | `true` | Disable only for local plaintext brokers or Docker E2E. |

`*` Provide either `CONNECTION_STRING` or explicit bootstrap / SASL settings.

### Docker examples

```powershell
docker run --rm `
  -e SIRI_SOURCES="uk-bods-bulk-archive" `
  -e CONNECTION_STRING="BootstrapServer=<host:port>;EntityPath=siri" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

```powershell
docker run --rm `
  -e SIRI_PROVIDER=custom `
  -e SIRI_URL="https://example.test/siri/vm" `
  -e KAFKA_BOOTSTRAP_SERVERS="broker:9093" `
  -e KAFKA_TOPIC="siri" `
  -e SASL_USERNAME="<user>" `
  -e SASL_PASSWORD="<password>" `
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

## MQTT image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-siri-mqtt:latest
```

### Environment variables

| Variable | Required | Default | Description |
| --- | ---: | ---: | --- |
| `MQTT_BROKER_URL` | ✅* | — | Broker URL such as `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` | ✅* | — / `1883` | Alternate host / port inputs when not using `MQTT_BROKER_URL`. |
| `MQTT_ENABLE_TLS` | ❌ | inferred from URL / `false` | Enable broker TLS. |
| `MQTT_AUTH_MODE` | ❌ | `anonymous` | `anonymous`, `userpass`, or `entra`. |
| `MQTT_USERNAME` | ❌ | — | Username for `userpass`; also used by some brokers for Entra / namespace routing. |
| `MQTT_PASSWORD` | ❌ | — | Password for `userpass`. |
| `MQTT_CLIENT_ID` | ❌ | empty | MQTT client identifier. |
| `MQTT_ENTRA_CLIENT_ID` | ❌ | — | Managed identity client id for `MQTT_AUTH_MODE=entra`. |
| `MQTT_ENTRA_AUDIENCE` | ❌ | `https://eventgrid.azure.net/` | JWT audience for Event Grid namespace MQTT. |

`*` Provide either `MQTT_BROKER_URL` or `MQTT_HOST` / `MQTT_PORT`.

### Docker examples

Generic broker with password:

```powershell
docker run --rm `
  -e SIRI_SOURCES="uk-bods-bulk-archive" `
  -e MQTT_BROKER_URL="mqtt://broker:1883" `
  -e MQTT_AUTH_MODE="userpass" `
  -e MQTT_USERNAME="<user>" `
  -e MQTT_PASSWORD="<password>" `
  ghcr.io/clemensv/real-time-sources-siri-mqtt:latest
```

Event Grid namespace MQTT with Entra ID:

```powershell
docker run --rm `
  -e SIRI_SOURCES="uk-bods-bulk-archive" `
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" `
  -e MQTT_AUTH_MODE="entra" `
  -e MQTT_USERNAME="<client-authentication-name>" `
  -e MQTT_ENTRA_CLIENT_ID="<managed-identity-client-id>" `
  ghcr.io/clemensv/real-time-sources-siri-mqtt:latest
```

## AMQP image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

### Environment variables

| Variable | Required | Default | Description |
| --- | ---: | ---: | --- |
| `AMQP_BROKER_URL` | ✅* | — | Full AMQP URL form such as `amqp://user:password@host:5672/siri`. |
| `AMQP_HOST` / `AMQP_PORT` | ✅* | — / `5672` | Alternate host / port inputs when not using `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | ❌ | `siri` | AMQP node/address. |
| `AMQP_TLS` | ❌ | auth-dependent | Enable TLS. |
| `AMQP_AUTH_MODE` | ❌ | `password` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | ❌ | — | Generic broker credentials for `password`. |
| `AMQP_ENTRA_AUDIENCE` | ❌ | `https://servicebus.azure.net/.default` | Entra CBS audience. |
| `AMQP_ENTRA_CLIENT_ID` | ❌ | — | Managed identity client id for Entra auth. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | ❌ | — | SAS CBS credentials. |

`*` Provide either `AMQP_BROKER_URL` or `AMQP_HOST` / `AMQP_PORT`.

### Docker examples

Generic broker with SASL PLAIN:

```powershell
docker run --rm `
  -e SIRI_SOURCES="uk-bods-bulk-archive" `
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/siri" `
  ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

Service Bus with Entra ID:

```powershell
docker run --rm `
  -e SIRI_SOURCES="uk-bods-bulk-archive" `
  -e AMQP_HOST="<namespace>.servicebus.windows.net" `
  -e AMQP_ADDRESS="siri" `
  -e AMQP_TLS=true `
  -e AMQP_AUTH_MODE=entra `
  -e AMQP_ENTRA_CLIENT_ID="<managed-identity-client-id>" `
  ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

Service Bus emulator / SAS:

```powershell
docker run --rm `
  -e SIRI_SOURCES="uk-bods-bulk-archive" `
  -e AMQP_HOST="<service-bus-host>" `
  -e AMQP_ADDRESS="siri" `
  -e AMQP_AUTH_MODE=sas `
  -e AMQP_SAS_KEY_NAME="<key-name>" `
  -e AMQP_SAS_KEY="<key>" `
  ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

## Azure templates

The source ships templates for:

- `azure-template.json` — Kafka container against an existing Kafka/Event Hubs endpoint
- `azure-template-with-eventhub.json` — Kafka container plus a new Event Hubs namespace
- `azure-template-mqtt.json` — MQTT container against an existing broker
- `azure-template-with-eventgrid-mqtt.json` — MQTT container plus an Event Grid namespace broker
- `azure-template-with-servicebus.json` — AMQP container plus a Service Bus namespace

All templates expose the legacy single-source parameters (`siriProvider`, `siriUrl`, `siriApiKey`, `siriOperators`) and can be paired with catalog selection through `SIRI_SOURCES_FILE` / `SIRI_SOURCES` when the template is extended or a custom container group is used.
