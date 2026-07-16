<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# GTFS Realtime

<sub>1,000+ transit agencies, vehicles, trips, alerts · Kafka · MQTT · AMQP · <a href="https://gtfs.org/">upstream</a> · <a href="https://gtfs.org/documentation/realtime/reference/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-4_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — 1,000+ transit agencies, vehicles, trips, alerts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#gtfs) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/gtfs.kql) &nbsp;·&nbsp;
[🗺️ **Fabric Map**](fabric/README.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://gtfs.org/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for the GTFS Realtime feeder and their runtime contract. See [README.md](README.md) for source overview and [EVENTS.md](EVENTS.md) for the CloudEvents schema/routing contract.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://gtfs.org/>
- API / data documentation: <https://gtfs.org/documentation/realtime/reference/>

<!-- upstream-links:end -->

## Why this container

These images package the upstream connector, CloudEvents normalization, and transport-specific publisher wiring into ready-to-run artifacts for Kafka, MQTT/UNS, AMQP deployments.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-gtfs` | Kafka | Topic(s): `gtfs`, key = `{agencyid}` |
| `ghcr.io/clemensv/real-time-sources-gtfs-mqtt` | MQTT 5.0 | Topic template `transit/intl/gtfs/gtfs/{agencyid}/static/agency/{row_id}` |
| `ghcr.io/clemensv/real-time-sources-gtfs-amqp` | AMQP 1.0 | Address `gtfs` |

Event families (base groups):

- `GeneralTransitFeedRealTime`
- `GeneralTransitFeedStatic`

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.12-slim` |
| Default entry point | Kafka: `["python", "-m", "gtfs_rt_bridge", "feed"]`; MQTT: `["python", "-m", "gtfs_mqtt", "feed"]`; AMQP: `["python", "-m", "gtfs_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| State | none required (streaming bridge) |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-gtfs:latest
docker pull ghcr.io/clemensv/real-time-sources-gtfs-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-gtfs-amqp:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams (connection string)

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-gtfs:latest
```

### With Kafka broker parameters (SASL/PLAIN)

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='gtfs' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-gtfs:latest
```

## Using the MQTT image

### With generic MQTT broker (username/password)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-gtfs-mqtt:latest
```

### With Azure Event Grid MQTT broker (Microsoft Entra)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-gtfs-mqtt:latest
```

## Using the AMQP image

### With generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/gtfs' \
  ghcr.io/clemensv/real-time-sources-gtfs-amqp:latest
```

### With Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='gtfs' \
  -e AMQP_AUTH_MODE=entra \
  ghcr.io/clemensv/real-time-sources-gtfs-amqp:latest
```

### With SAS-token CBS (Service Bus emulator / SAS-only)

```bash
docker run --rm \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='gtfs' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-gtfs-amqp:latest
```

## Environment variables

### Source configuration

| Variable | Description |
|---|---|
| `SCHEDULE_POLL_INTERVAL` | The number of seconds to wait between polling the GTFS schedule. |

### Common

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string for Kafka-mode publishing. |
| `KAFKA_ENABLE_TLS` | Set `false` for local/plain Kafka; default `true`. |
| `GTFS_SOURCES_FILE` | Optional path to a GTFS source catalog JSON file; defaults to the packaged catalog. |
| `GTFS_SOURCES` | Catalog selector: comma-separated source names, `*` for all, or unset for `enabled: true` only. |
| `GTFS_URLS` | Legacy comma-separated GTFS schedule feed URLs to download before publishing static entities; legacy URL/MDB config takes precedence over the catalog. |
| `GTFS_HEADERS` | Optional headers used when fetching the GTFS schedule feed URLs. |
| `GTFS_RT_URLS` | Legacy comma-separated GTFS-Realtime feed URLs to poll for trip updates, alerts, and vehicle positions; takes precedence over the catalog. |
| `GTFS_RT_HEADERS` | Optional headers used when fetching the GTFS-Realtime feed URLs. |
| `MDB_SOURCE_ID` | Legacy Mobility Database source ID used to resolve GTFS-Realtime and schedule URLs from the MDB cache. |
| `AGENCY` | Agency tag used in CloudEvents subject/key identity. |
| `ROUTE` | Optional route ID filter; leave unset or `*` to publish all routes from the configured realtime feeds. |
| `CACHE_DIR` | Directory used by the bridge to cache downloaded GTFS Schedule archives and Mobility Database metadata. |
| `SCHEDULE_CACHE_DIR` | Directory used by the Azure companion templates to cache downloaded GTFS schedule archives between polling cycles. |
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

## Configuring sources

GTFS has no universal default feed. With no legacy variables and no enabled catalog entries, the container still requires the operator to select or provide a feed. To use the packaged disabled MBTA example:

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  -e GTFS_SOURCES=mbta-boston \
  ghcr.io/clemensv/real-time-sources-gtfs:latest
```

### Catalog format

`GTFS_SOURCES_FILE` points at a JSON document with a top-level `sources` array. Each entry is one transit feed:

| Field | Description |
|---|---|
| `name` | Stable selector name used by `GTFS_SOURCES`. |
| `enabled` | Runs when `GTFS_SOURCES` is unset if `true`; disabled entries are examples/templates. |
| `description` | Human-readable source note. |
| `gtfs_rt_urls` | List of GTFS-Realtime protobuf endpoint URLs. |
| `gtfs_urls` | List of GTFS Schedule zip URLs. |
| `mdb_source_id` | Optional Mobility Database source ID alternative to explicit URLs. |
| `agency` | Agency tag emitted in CloudEvents subjects/keys. |
| `route` | Optional route filter; defaults to `*`. |
| `gtfs_rt_headers` / `gtfs_headers` | Optional request headers as an object or list of name/value pairs. |

### Selecting sources

- Unset `GTFS_SOURCES`: run only `enabled: true` entries. The shipped catalog has none enabled.
- `GTFS_SOURCES=*`: run all entries, including disabled examples/templates.
- `GTFS_SOURCES=mbta-boston,other`: run named entries in the requested order; unknown names fail fast.
- Legacy `GTFS_RT_URLS`, `GTFS_URLS`, or `MDB_SOURCE_ID` still creates one ad-hoc feed and bypasses the catalog.

### Keeping secrets out of the catalog

Catalog string values expand `${ENV_VAR}` at runtime:

```json
{
  "name": "keyed-operator",
  "enabled": true,
  "agency": "operator",
  "gtfs_rt_urls": ["https://operator.example/REPLACE_WITH_GTFS_RT_URL"],
  "gtfs_rt_headers": {"x-api-key": "${SOME_GTFS_KEY}"}
}
```

Mount a private catalog and pass the secret as an environment variable:

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  -e GTFS_SOURCES_FILE=/config/gtfs-sources.json \
  -e GTFS_SOURCES=keyed-operator \
  -e SOME_GTFS_KEY='<secret>' \
  -v "$PWD/gtfs-sources.json:/config/gtfs-sources.json:ro" \
  ghcr.io/clemensv/real-time-sources-gtfs:latest
```

### Known GTFS-Realtime sources

Use MobilityData’s [Mobility Database](https://database.mobilitydata.org/) and agency developer portals to find operator-specific GTFS Schedule and GTFS-Realtime feeds. Some are free and keyless; others require API keys or custom headers. The packaged catalog ships only disabled entries: `mbta-boston` (real keyless MBTA URLs), `mta-nyc` (real keyless Metropolitan Transportation Authority New York City feeds — subway, LIRR, Metro-North, and alerts, plus GTFS Schedule archives; high volume), `hsl-helsinki` (real keyless Helsinki Regional Transport feeds from `realtime.hsl.fi`, plus the HSL GTFS Schedule zip), `bkk-budapest` (BKK Budapest feeds from `go.bkk.hu`, realtime keyed via `?key=${BKK_API_KEY}`, keyless GTFS Schedule zip), `stm-montreal` (Societe de transport de Montreal feeds from `api.stm.info`, realtime keyed via the `apiKey` header from `${STM_API_KEY}`, keyless GTFS Schedule zip), `sncf-france` (keyless SNCF national-rail feeds from the French NAP proxy `proxy.transport.data.gouv.fr` — trip updates and service alerts for TGV / Intercites / TER, plus the keyless SNCF GTFS Schedule zip), `tfnsw-sydney` (Transport for NSW Sydney / NSW feeds, ready to enable with `TFNSW_API_KEY`), and `keyed-operator-template` (`REPLACE_WITH_*` placeholders plus `${SOME_GTFS_KEY}` headers).

### Kafka image

| Variable | Description |
|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list (`host:port,...`). |
| `KAFKA_TOPIC` | Destination topic (default from contract). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials for Kafka-compatible brokers. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URI (`mqtt://` or `mqtts://`). |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for password mode. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for Microsoft Entra JWT. |
| `MQTT_CLIENT_ID` | Client identifier; must be unique per broker namespace. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Full AMQP URI (`amqp://` or `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | Target queue/topic/address. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra ID token settings for CBS auth mode. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token settings for SAS CBS auth mode. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

## Deploying into Azure Container Instances

One deploy button is provided per ARM template file present in this folder:

- **azure-template-mqtt.json** (mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template-mqtt.json)
- **azure-template-with-eventgrid-mqtt.json** (with eventgrid mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template-with-eventgrid-mqtt.json)
- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schemas.
- [`xreg/gtfs.xreg.json`](xreg/gtfs.xreg.json) — authoritative xRegistry manifest.
