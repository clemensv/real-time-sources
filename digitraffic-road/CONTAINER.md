# Digitraffic Road container images

This document covers the published OCI images for the Digitraffic Road feeder and their runtime contract. See [README.md](README.md) for source overview and [EVENTS.md](EVENTS.md) for the CloudEvents schema/routing contract.

## Why this container

These images package the upstream connector, CloudEvents normalization, and transport-specific publisher wiring into ready-to-run artifacts for Kafka deployments.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-digitraffic-road` | Kafka | Topic(s): `digitraffic-road-maintenance`, `digitraffic-road-messages`, `digitraffic-road-sensors`, key = `{domain}`, `{situation_id}`, `{station_id}`, `{station_id}/{sensor_id}`, `{task_id}` |

Event families (base groups):

- `fi.digitraffic.road.sensors`
- `fi.digitraffic.road.messages`
- `fi.digitraffic.road.maintenance`
- `fi.digitraffic.road.stations`
- `fi.digitraffic.road.maintenance.tasks`

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.12-slim` |
| Default entry point | Kafka: `["python", "-m", "digitraffic_road", "stream"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| State | none required (streaming bridge) |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams (connection string)

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

### With Kafka broker parameters (SASL/PLAIN)

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='digitraffic-road-maintenance' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

## Environment variables

### Common

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string for Kafka-mode publishing. |
| `KAFKA_ENABLE_TLS` | Set `false` for local/plain Kafka; default `true`. |

### Kafka image

| Variable | Description |
|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list (`host:port,...`). |
| `KAFKA_TOPIC` | Destination topic (default from contract). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials for Kafka-compatible brokers. |

## Deploying into Azure Container Instances

One deploy button is provided per ARM template file present in this folder:

- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schemas.
- [`xreg/digitraffic_road.xreg.json`](xreg/digitraffic_road.xreg.json) — authoritative xRegistry manifest.
