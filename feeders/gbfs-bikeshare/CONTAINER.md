# GBFS bikeshare container images

For the source overview see [README.md](README.md); for the CloudEvents contract and routing metadata see [EVENTS.md](EVENTS.md).

This source ships three transport-specific images that all consume the same `GBFS_FEEDS` configuration surface.

| Variant | Image | Default command |
|---|---|---|
| Kafka | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-kafka:latest` | `python -m gbfs_bikeshare feed` |
| MQTT | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest` | `python -m gbfs_bikeshare_mqtt feed` |
| AMQP | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest` | `python -m gbfs_bikeshare_amqp feed` |

## Common source configuration

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `GBFS_FEEDS` | ✅ | — | Comma-separated GBFS autodiscovery URLs, `@file`, or path to a file containing one URL per line. |
| `GBFS_SYSTEM_IDS` | ❌ | — | Optional comma-separated system-id overrides aligned positionally with `GBFS_FEEDS`. |
| `POLL_INTERVAL` | ❌ | `60` | Telemetry polling interval in seconds. |
| `REFERENCE_REFRESH_INTERVAL` | ❌ | `3600` | Station and system reference-data refresh cadence in seconds. |
| `STATE_FILE` | ❌ | image-specific home-file path | JSON dedupe state file. Mount persistent storage here for long-running deployments. |
| `ONCE_MODE` | ❌ | `false` | When `true`, run one polling cycle and exit. Required for Fabric notebook hosting and useful for smoke tests. |
| `LOG_LEVEL` | ❌ | `INFO` | Standard Python logging level. |

## Kafka image

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `CONNECTION_STRING` | ✅* | — | Event Hubs / Fabric Event Stream or plain `BootstrapServer=...;EntityPath=...` connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | ✅* | — | Bootstrap servers when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | ❌ | `gbfs-bikeshare` | Kafka topic to publish into. |
| `SASL_USERNAME` | ❌ | — | SASL PLAIN username when not using `CONNECTION_STRING`. |
| `SASL_PASSWORD` | ❌ | — | SASL PLAIN password when not using `CONNECTION_STRING`. |
| `KAFKA_ENABLE_TLS` | ❌ | `true` | Disable only for local plaintext brokers or Docker E2E. |

`*` Provide either `CONNECTION_STRING` or the explicit bootstrap / SASL settings.

### Docker example

```bash
docker run --rm \
  -e GBFS_FEEDS="https://gbfs.citibikenyc.com/gbfs/gbfs.json" \
  -e CONNECTION_STRING="BootstrapServer=<host:port>;EntityPath=gbfs-bikeshare" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-kafka:latest
```

### Azure templates

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template.json)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-with-eventhub.json)

## MQTT image

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `MQTT_BROKER_URL` | ✅* | — | Broker URL such as `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` | ✅* | — | Alternate host / port inputs when not using `MQTT_BROKER_URL`. |
| `MQTT_TLS` / `MQTT_ENABLE_TLS` | ❌ | inferred from URL | Enable broker TLS. |
| `MQTT_AUTH_MODE` | ❌ | `anonymous` | `anonymous`, `userpass`, `tls-cert`, or `entra`. |
| `MQTT_USERNAME` | ❌ | — | Username for `userpass`; also used by some brokers for Entra / namespace routing. |
| `MQTT_PASSWORD` | ❌ | — | Password for `userpass`. |
| `MQTT_CLIENT_ID` | ❌ | source-derived | MQTT client identifier. |
| `MQTT_CA_FILE` | ❌ | system trust | Optional CA bundle path. |
| `MQTT_CLIENT_CERT` | ❌ | — | Client certificate PEM for `tls-cert`. |
| `MQTT_CLIENT_KEY` | ❌ | — | Client private key PEM for `tls-cert`. |
| `MQTT_ENTRA_CLIENT_ID` | ❌ | — | Managed identity client id for `MQTT_AUTH_MODE=entra`. |
| `MQTT_ENTRA_AUDIENCE` | ❌ | `https://eventgrid.azure.net/` | JWT audience for Event Grid namespace MQTT. |

`*` Provide either `MQTT_BROKER_URL` or `MQTT_HOST` / `MQTT_PORT`.

### Docker example

```bash
docker run --rm \
  -e GBFS_FEEDS="https://gbfs.citibikenyc.com/gbfs/gbfs.json" \
  -e MQTT_BROKER_URL="mqtt://broker:1883" \
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest
```

### Azure templates

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-mqtt.json)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP image

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `AMQP_BROKER_URL` | ✅* | — | Broker URL such as `amqp://user:pass@host:5672` or `amqps://host:5671`. |
| `AMQP_HOST` / `AMQP_PORT` | ✅* | — | Alternate host / port inputs when not using `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | ❌ | `gbfs-bikeshare` | Queue / topic / address name. |
| `AMQP_AUTH_MODE` | ❌ | `password` | `password`, `sas`, or `entra`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | ❌ | — | SASL PLAIN credentials for generic brokers. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | ❌ | — | SAS token minting inputs for Service Bus emulator or SAS-authenticated Azure targets. |
| `AMQP_TLS` | ❌ | inferred from URL | Enable TLS. |
| `AMQP_CONTENT_MODE` | ❌ | `binary` | CloudEvents content mode; `binary` is the recommended default. |
| `AMQP_ENTRA_CLIENT_ID` | ❌ | — | Managed identity client id for `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_AUDIENCE` | ❌ | `https://servicebus.azure.net/.default` | Azure target audience for CBS token acquisition. |

`*` Provide either `AMQP_BROKER_URL` or `AMQP_HOST` / `AMQP_PORT`.

### Docker example

```bash
docker run --rm \
  -e GBFS_FEEDS="https://gbfs.citibikenyc.com/gbfs/gbfs.json" \
  -e AMQP_BROKER_URL="amqp://user:pass@broker:5672" \
  -e AMQP_ADDRESS="gbfs-bikeshare" \
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest
```

### Azure template

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-with-servicebus.json)

## Fabric notebook hosting

Poll-based sources in this repo must ship a notebook-hosting option. Use:

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source gbfs-bikeshare -Workspace <workspace>
```

The notebook reads `GBFS_FEEDS` from its parameter cell, runs the Kafka feeder once, resolves the Fabric Event Stream connection string at runtime, and writes diagnostics to `/lakehouse/default/Files/feeder-state/gbfs-bikeshare/last-run.log`.
