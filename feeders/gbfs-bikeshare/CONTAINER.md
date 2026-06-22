# GBFS Bikeshare Kafka, MQTT, and AMQP containers

For the source overview see [README.md](README.md); for the CloudEvents contract and routing metadata see [EVENTS.md](EVENTS.md).

GBFS Bikeshare containers turn station inventory, dock availability, and dockless vehicle telemetry from configurable GBFS systems into CloudEvents for mobility operations dashboards, trip planners, city analytics, and event-driven digital twins.

## Image contract

| Image | Dockerfile | Transport | State share |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest` | `Dockerfile` | Kafka/Event Hubs | Optional `STATE_FILE`. |
| `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5 | Optional `STATE_FILE`; broker retained state stores LKV. |
| `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 | Optional `STATE_FILE`. |

## Common environment

| Variable | Description | Default |
| --- | --- | --- |
| `GBFS_SOURCES_FILE` | Path to a GBFS source catalog JSON file. See [README.md#configuring-sources](README.md#configuring-sources). | Packaged catalog |
| `GBFS_SOURCES` | Comma-separated catalog entry `name`s, or `*` for all entries including disabled templates. Unset runs entries with `enabled: true`. | enabled entries |
| `GBFS_FEEDS` | Legacy quick override: comma-separated GBFS auto-discovery URLs, `@file`, or path to a file containing one URL per line. Takes precedence over the catalog when set. | unset |
| `GBFS_SYSTEM_IDS` | Optional comma-separated system-id overrides aligned positionally with `GBFS_FEEDS`. | unset |
| `GBFS_API_KEY` | Optional runtime upstream API key, or comma-separated keys aligned with `GBFS_FEEDS`. Catalog entries should use `${ENV_VAR}` in their `api_key` field instead. | unset |
| `GBFS_API_KEY_PARAM` | Query-string parameter name used with `GBFS_API_KEY` or a catalog `api_key`. A comma-separated list may be aligned with multiple `GBFS_FEEDS`. | `acl:consumerKey` |
| `POLL_INTERVAL` | Telemetry polling interval in seconds. | `60` |
| `REFERENCE_REFRESH_INTERVAL` | Station and system reference-data refresh cadence in seconds. | `3600` |
| `STATE_FILE` | JSON dedupe state file. Mount persistent storage here for long-running deployments. | image-specific home-file path |
| `ONCE_MODE` | Run one polling cycle and exit. Required for Fabric notebook hosting and useful for smoke tests. | `false` |
| `GBFS_MOCK` | Emit deterministic offline GBFS sample events once; used by CI flow tests. | `false` |
| `LOG_LEVEL` | Standard Python logging level. | `INFO` |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. | maintainer contact |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. | maintainer e-mail |

## Configuring sources

The default image includes `gbfs_bikeshare_core/sources/gbfs-bikeshare.sources.json`, with enabled keyless public feeds such as `citibike-nyc`, `divvy-chicago`, and `bike-share-toronto`. Set `GBFS_SOURCES` to select names from that catalog, or mount your own JSON file and set `GBFS_SOURCES_FILE`.

Catalog entries support `name`, `enabled`, `description`, `autodiscovery_url`, optional `system_id`, optional `api_key`, and optional `api_key_param`. Secrets should be written as `${ENV_VAR}` in the catalog and supplied with `-e` at runtime. The full catalog format, known-source table, and non-GBFS roadmap list live in [README.md#configuring-sources](README.md#configuring-sources).

Example with a mounted private catalog and runtime secret:

```powershell
docker run --rm `
  -v ${PWD}\my-gbfs.sources.json:/app/gbfs.sources.json:ro `
  -e GBFS_SOURCES_FILE="/app/gbfs.sources.json" `
  -e GBFS_SOURCES="private-operator" `
  -e PRIVATE_GBFS_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

Quick override without a catalog:

```powershell
docker run --rm `
  -e GBFS_FEEDS="https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json" `
  -e GBFS_SYSTEM_IDS="citibike-nyc" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

## Kafka image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

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

### Docker examples

Local Kafka / Event Hubs-compatible connection string:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc" `
  -e CONNECTION_STRING="BootstrapServer=<host:port>;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

Explicit Kafka bootstrap and SASL:

```powershell
docker run --rm `
  -e GBFS_SOURCES="divvy-chicago" `
  -e KAFKA_BOOTSTRAP_SERVERS="broker:9093" `
  -e KAFKA_TOPIC="gbfs-bikeshare" `
  -e SASL_USERNAME="<user>" `
  -e SASL_PASSWORD="<password>" `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

### Azure templates

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-with-eventhub.json)

## MQTT image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest
```

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `MQTT_BROKER_URL` | ✅* | — | Broker URL such as `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` | ✅* | — / `1883` | Alternate host / port inputs when not using `MQTT_BROKER_URL`. |
| `MQTT_TLS` / `MQTT_ENABLE_TLS` | ❌ | inferred from URL / `false` | Enable broker TLS. |
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

### Docker examples

Generic broker with password:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc" `
  -e MQTT_BROKER_URL="mqtt://broker:1883" `
  -e MQTT_AUTH_MODE="userpass" `
  -e MQTT_USERNAME="<user>" `
  -e MQTT_PASSWORD="<password>" `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest
```

Event Grid namespace MQTT with Entra ID:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc" `
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" `
  -e MQTT_AUTH_MODE="entra" `
  -e MQTT_USERNAME="<client-authentication-name>" `
  -e MQTT_ENTRA_CLIENT_ID="<managed-identity-client-id>" `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest
```

### Azure templates

[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest
```

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `AMQP_BROKER_URL` | ✅* | — | Broker URL such as `amqp://user:pass@host:5672` or `amqps://host:5671`. |
| `AMQP_HOST` / `AMQP_PORT` | ✅* | — / `5672` | Alternate host / port inputs when not using `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | ❌ | `gbfs-bikeshare` | Queue / topic / address name. |
| `AMQP_AUTH_MODE` | ❌ | `password` | `password`, `sas`, or `entra`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | ❌ | — | SASL PLAIN credentials for generic brokers. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | ❌ | — | SAS token minting inputs for Service Bus emulator or SAS-authenticated Azure targets. |
| `AMQP_TLS` | ❌ | inferred from URL | Enable TLS. |
| `AMQP_CONTENT_MODE` | ❌ | `binary` | CloudEvents content mode; `binary` is the recommended default. |
| `AMQP_ENTRA_CLIENT_ID` | ❌ | — | Managed identity client id for `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_AUDIENCE` | ❌ | `https://servicebus.azure.net/.default` | Azure target audience for CBS token acquisition. |

`*` Provide either `AMQP_BROKER_URL` or `AMQP_HOST` / `AMQP_PORT`.

### Docker examples

Generic broker with SASL PLAIN:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc" `
  -e AMQP_BROKER_URL="amqp://user:pass@broker:5672" `
  -e AMQP_ADDRESS="gbfs-bikeshare" `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest
```

Service Bus with Entra ID:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc" `
  -e AMQP_BROKER_URL="amqps://<namespace>.servicebus.windows.net:5671" `
  -e AMQP_ADDRESS="gbfs-bikeshare" `
  -e AMQP_AUTH_MODE="entra" `
  -e AMQP_ENTRA_CLIENT_ID="<managed-identity-client-id>" `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest
```

Service Bus emulator / SAS:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc" `
  -e AMQP_HOST="servicebus-emulator" `
  -e AMQP_PORT="5672" `
  -e AMQP_ADDRESS="gbfs-bikeshare" `
  -e AMQP_AUTH_MODE="sas" `
  -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey" `
  -e AMQP_SAS_KEY="<key>" `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest
```

### Azure template

[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgbfs-bikeshare%2Fazure-template-with-servicebus.json)

## Fabric notebook hosting

Poll-based sources in this repo ship a notebook-hosting option. Use:

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source gbfs-bikeshare -Workspace <workspace>
```

The notebook runs the Kafka feeder once, resolves the Fabric Event Stream connection string at runtime, and writes diagnostics to `/lakehouse/default/Files/feeder-state/gbfs-bikeshare/last-run.log`.

