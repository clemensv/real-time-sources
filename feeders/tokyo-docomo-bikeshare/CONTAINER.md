# Tokyo Docomo Bikeshare container images (Kafka, MQTT, AMQP)

For the source overview see [README.md](README.md); for the CloudEvents contract and routing metadata see [EVENTS.md](EVENTS.md).

These images are configuration-only wrappers over the generalized `gbfs-bikeshare` feeder. They bake the Tokyo Docomo GBFS autodiscovery URL and `docomo-cycle-tokyo` system id, while secrets such as the ODPT consumer key arrive only at runtime.

## What ships in the box

| Variant | Image | Base image | Default command | State share |
|---|---|---|---|---|
| Kafka | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest` | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest` | inherited `python -m gbfs_bikeshare feed` | inherited GBFS `STATE_FILE` support |
| MQTT | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest` | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest` | inherited `python -m gbfs_bikeshare_mqtt feed` | no state-share mount in the BYO / Event Grid MQTT ACI templates |
| AMQP | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest` | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest` | inherited `python -m gbfs_bikeshare_amqp feed` | inherited GBFS `STATE_FILE` support |

## Baked source configuration

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `GBFS_FEEDS` | ✅ | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json` | Tokyo Docomo GBFS autodiscovery URL served by ODPT. |
| `GBFS_SYSTEM_IDS` | ✅ | `docomo-cycle-tokyo` | Stable GBFS system id used in CloudEvents subjects and transport keys. |
| `GBFS_API_KEY` | ✅ | — | ODPT consumer key supplied at runtime. The base image appends it as `acl:consumerKey=<key>`. |
| `GBFS_API_KEY_PARAM` | ❌ | `acl:consumerKey` | Query-string parameter name used with `GBFS_API_KEY`; keep the default for ODPT. |
| `POLL_INTERVAL` | ❌ | `60` | Station-status polling interval in seconds. |
| `REFERENCE_REFRESH_INTERVAL` | ❌ | `3600` | System and station reference refresh cadence in seconds. |
| `STATE_FILE` | ❌ | inherited image default | JSON dedupe state file path. Mount persistent storage for long-running ACI deployments. |
| `ONCE_MODE` | ❌ | `false` | Run one polling cycle and exit. |
| `LOG_LEVEL` | ❌ | `INFO` | Controls feeder log verbosity using standard Python logging levels such as `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. |

## Kafka image

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `CONNECTION_STRING` | ✅* | — | Event Hubs / Fabric Event Stream or plain `BootstrapServer=...;EntityPath=...` connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | ✅* | — | Bootstrap servers when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | ❌ | `gbfs-bikeshare` from base image unless overridden by connection string | Kafka topic to publish into. Use `tokyo-docomo-bikeshare` for this wrapper. |
| `SASL_USERNAME` | ❌ | — | SASL PLAIN username when not using `CONNECTION_STRING`. |
| `SASL_PASSWORD` | ❌ | — | SASL PLAIN password when not using `CONNECTION_STRING`. |
| `KAFKA_ENABLE_TLS` | ❌ | `true` | Disable only for local plaintext brokers or Docker E2E. |

`*` Provide either `CONNECTION_STRING` or the explicit bootstrap / SASL settings.

```bash
docker pull ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
docker run --rm   -e GBFS_API_KEY="<odpt-consumer-key>"   -e CONNECTION_STRING="BootstrapServer=<host:port>;EntityPath=tokyo-docomo-bikeshare"   -e KAFKA_ENABLE_TLS=false   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

### Azure templates

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template.json)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventhub.json)

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

```bash
docker pull ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
docker run --rm   -e GBFS_API_KEY="<odpt-consumer-key>"   -e MQTT_BROKER_URL="mqtt://broker:1883"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
```

### Azure templates

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-mqtt.json)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP image

### Environment variables

| Variable | Required | Default | Description |
|---|---:|---:|---|
| `AMQP_BROKER_URL` | ✅* | — | Broker URL such as `amqp://user:pass@host:5672` or `amqps://host:5671`. |
| `AMQP_HOST` / `AMQP_PORT` | ✅* | — | Alternate host / port inputs when not using `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | ❌ | `gbfs-bikeshare` from base image | Queue / topic / address name. Use `tokyo-docomo-bikeshare` for this wrapper. |
| `AMQP_AUTH_MODE` | ❌ | `password` | `password`, `sas`, or `entra`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | ❌ | — | SASL PLAIN credentials for generic brokers. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | ❌ | — | SAS token minting inputs for Service Bus emulator or SAS-authenticated Azure targets. |
| `AMQP_TLS` | ❌ | inferred from URL | Enable TLS. |
| `AMQP_CONTENT_MODE` | ❌ | `binary` | CloudEvents content mode; `binary` is recommended. |
| `AMQP_ENTRA_CLIENT_ID` | ❌ | — | Managed identity client id for `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_AUDIENCE` | ❌ | `https://servicebus.azure.net/.default` | Azure target audience for CBS token acquisition. |

`*` Provide either `AMQP_BROKER_URL` or `AMQP_HOST` / `AMQP_PORT`.

```bash
docker pull ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
docker run --rm   -e GBFS_API_KEY="<odpt-consumer-key>"   -e AMQP_BROKER_URL="amqp://user:pass@broker:5672"   -e AMQP_ADDRESS="tokyo-docomo-bikeshare"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
```

### Azure template

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-with-servicebus.json)

## Fabric and Azure notes

The wrapper inherits the `gbfs-bikeshare` runtime behavior. It emits the consolidated GBFS CloudEvents contract and requires consumers of the retired bespoke Tokyo event types to migrate to `org.gbfs.*` event names.
