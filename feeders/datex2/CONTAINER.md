# DATEX II Kafka, MQTT, and AMQP containers

DATEX II containers turn European road-traffic XML publications into CloudEvents for operational traffic dashboards, traveler-information services, safety analytics, and event-driven digital twins.

## Image contract

| Image | Dockerfile | Transport | State share |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-datex2:latest` | `Dockerfile` | Kafka/Event Hubs | Optional `DATEX2_STATE_FILE` / `STATE_FILE`. |
| `ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5 | Stateless per run; broker retained state stores LKV. |
| `ghcr.io/clemensv/real-time-sources-datex2-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 | Stateless per run. |

## Common environment

| Variable | Description | Default |
| --- | --- | --- |
| `DATEX2_SOURCES_FILE` | Path to a JSON catalog of DATEX II source entries. Mount your own copy to poll road authorities not shipped by default. | Packaged catalog |
| `DATEX2_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled templates. When unset, entries with `enabled: true` run. | enabled entries |
| `DATEX2_ENDPOINTS` | Legacy inline JSON endpoint list (`id`, `url`, `publication`, optional `country`, `operator`, `auth_header`) or `@file`. Takes precedence over the catalog when set. | unset |
| `DATEX2_MOCK` | Emit deterministic sample DATEX II events for tests. | `false` |
| `MAX_RECORDS_PER_FAMILY` | Caps records per event family during one cycle. | `25` |
| `POLLING_INTERVAL` | Seconds between polling cycles for Kafka container. | `300` |
| `LOG_LEVEL` | Python logging level. | `INFO` |
| `DATEX2_STATE_FILE` | Optional DATEX II-specific persistent dedupe state file path for Kafka/Event Hubs deployments. | unset |
| `STATE_FILE` | Optional generic persistent dedupe state file path for Kafka/Event Hubs deployments. | unset |
| `ONCE_MODE` | Run one polling cycle and exit. | `false` |

## Configuring sources

Sources are defined in the checked-in catalog `datex2_core/datex2_core/sources/datex2.sources.json` (packaged in every image). `DATEX2_SOURCES` selects entries by name or `*`; when unset, every entry with `enabled: true` runs. Mount your own catalog with `DATEX2_SOURCES_FILE`, and keep secrets out of the file with `${ENV_VAR}` placeholders (for example `"auth_header": "Bearer ${TRAFIKVERKET_KEY}"`). The legacy inline `DATEX2_ENDPOINTS` JSON still works and takes precedence when set.

### Known DATEX II sources

This image ships the four no-auth NDW (Netherlands) feeds enabled, three open CITA Luxembourg motorway corridors disabled, and a disabled key-protected Trafikverket (Sweden) template; add other publishers by mounting your own catalog.

| Catalog name | Status | Publisher | Public URL / notes |
| --- | --- | --- | --- |
| `ndw-measurement-sites` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/measurement_current.xml.gz` — MeasurementSiteTablePublication reference data. |
| `ndw-trafficspeed` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/trafficspeed.xml.gz` — MeasuredDataPublication speed/flow. |
| `ndw-traveltime` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/traveltime.xml.gz` — MeasuredDataPublication travel times. |
| `ndw-roadworks` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz` — SituationPublication roadworks/events. |
| `cita-luxembourg-a6` | Shipped disabled | CITA Luxembourg (LU) | `https://www.cita.lu/info_trafic/datex/trafficstatus_a6` — A6 motorway corridor (MeasuredDataPublication). |
| `cita-luxembourg-a1` | Shipped disabled | CITA Luxembourg (LU) | `https://www.cita.lu/info_trafic/datex/trafficstatus_a1` — A1 corridor. |
| `cita-luxembourg-a4` | Shipped disabled | CITA Luxembourg (LU) | `https://www.cita.lu/info_trafic/datex/trafficstatus_a4` — A4 corridor. |
| `trafikverket-sweden` | Shipped disabled template | Trafikverket (SE) | Key-protected; register at `https://data.trafikverket.se/`, export `TRAFIKVERKET_KEY`, set the feed `url`. |
| not shipped | Custom DATEX II publisher | Any national/regional road authority | Copy an entry, set `url` + `publication`, add `auth_header` for key-protected feeds. |

## Kafka

Set `CONNECTION_STRING=BootstrapServer=broker:9092;EntityPath=topic` and `KAFKA_ENABLE_TLS=false` for local Kafka, or pass an Event Hubs-compatible connection string.

Additional variables: `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `KAFKA_ENABLE_TLS`, `SASL_USERNAME`, `SASL_PASSWORD`, `SASL_MECHANISM`, `CLIENT_ID`, `GROUP_ID`.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2:latest
docker run --rm -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=datex2" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2:latest
```

## MQTT 5

Set `MQTT_BROKER_URL`, `MQTT_AUTH_MODE`, and optional username/password or TLS settings.

Additional variables: `MQTT_ENABLE_TLS`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CA_FILE`, `MQTT_CLIENT_ID`, `MQTT_AUTH_MODE`, `MQTT_TOKEN_SCOPE`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
```

## AMQP 1.0

Set `AMQP_HOST`, `AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, and `AMQP_TLS`. The AMQP producer uses binary CloudEvents content mode.

Additional variables: `AMQP_BROKER_URL`, `AMQP_PORT`, `AMQP_AUTH_MODE`, `AMQP_SAS_KEY_NAME`, `AMQP_SAS_KEY`, `AMQP_SAS_TOKEN_TTL_SECONDS`, `AMQP_ENTRA_AUDIENCE`, `AMQP_ENTRA_CLIENT_ID`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
docker run --rm -e AMQP_HOST="broker" -e AMQP_ADDRESS="datex2" -e AMQP_USERNAME="user" -e AMQP_PASSWORD="secret" ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
```

## Azure deployment templates

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventhub.json)
[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventgrid-mqtt.json)
[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-servicebus.json)

See [EVENTS.md](EVENTS.md) for event types, subjects, and transport bindings.
