<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="United States" width="64" height="48"><br>
<sub><b>United States</b></sub>
</td>
<td valign="middle">

# USGS NWIS Water Quality

<sub>~3,000 continuous WQ sites · Kafka · MQTT · AMQP · <a href="https://waterdata.usgs.gov/">upstream</a> · <a href="https://waterservices.usgs.gov/docs/water-quality-samples/water-quality-samples-details/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> United States — ~3,000 continuous WQ sites

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#usgs-nwis-wq) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#usgs-nwis-wq/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/usgs_nwis_wq.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://waterdata.usgs.gov/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the USGS NWIS Water Quality feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

## Transitional configuration

This feed contains continuous sensor observations, not laboratory samples.
Legacy acquisition remains default. Choose the native `usgs-waterdata`
feeder for new or unmapped series. Kafka, MQTT and AMQP share the same opt-in
frozen-contract acquisition; MQTT no longer publishes synthetic examples.

| Variable | Default | Meaning |
|---|---|---|
| `USGS_API_MODE` | `legacy` | `waterdata` opts into verified transitional acquisition; legacy rollback ends at WaterServices retirement. |
| `USGS_SITES` | None | Required in waterdata mode: explicit comma-separated numeric or `USGS-` prefixed site IDs. |
| `USGS_PARAMETERS` | `USGS_WQ_PARAMETER_CODES`, else none | Required explicit parameter selection in waterdata mode. Every site/parameter must be enrolled. |
| `USGS_ENROLLMENT_FILE` | None | Required in waterdata mode: reviewed JSON enrollment with captured IV and WQ site metadata and transport `routing_state`. |
| `USGS_REPLAY_START` | Enrollment `baseline` | Initial offset-aware update-time baseline; a committed new-path cursor takes precedence. |
| `USGS_STATE_FILE` | `STATE_FILE`, else legacy state path + `.waterdata` | New-path checkpoint; never implicitly overwrites legacy dedupe state. Give every transport its own path. |
| `WQ_LOOKBACK_HOURS` | `2` | Retained observation-time window, including corrections within that window. Must be positive. |
| `USGS_API_KEY` | None | Optional USGS API key, kept out of logs. |
| `POLLING_INTERVAL` | `300` seconds (Kafka/MQTT), `600` (AMQP) | Delay after catch-up. Two-hour fixed `last_modified` windows replay without delay until caught up. |

Operator-configured example (replace the paths and selected site):

```powershell
docker run --rm `
  --mount "type=bind,source=C:\operator\reviewed-enrollment.json,target=/config/enrollment.json,readonly" `
  -e USGS_API_MODE=waterdata -e USGS_SITES=<reviewed-site-number> -e USGS_PARAMETERS=00010 `
  -e USGS_ENROLLMENT_FILE=/config/enrollment.json `
  -e "CONNECTION_STRING=BootstrapServer=broker:9092;EntityPath=usgs-wq" `
  -e KAFKA_ENABLE_TLS=false -e ONCE_MODE=true `
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

The same acquisition settings work with the existing MQTT/AMQP authentication
variables and image suffixes. The operator enrollment supplies transport
`routing_state`; the historical WaterML FIPS state remains in payload metadata.
The unchanged CloudEvents source remains the
historical WaterServices URL. Kafka `EntityPath` wins over topic defaults.
Unknown selected series, units, qualifiers or missing snapshots fail before
emission. Keep actual enrollment, provenance and observation evidence outside
Git. The [synthetic enrollment](enrollment/synthetic-example.json) documents the
offline test shape only. Strict Docker migration E2E requires
`USGS_E2E_ENROLLMENT_FILE` pointing to a reviewed file outside the checkout; the
harness stages it only into the test build context, never a published image.
USGS data is US Government public domain.

Images run as UID `10001`; mounted state directories must be writable by that
user. Their healthcheck tests process liveness, not observation freshness.
The deterministic `vendor/` core wheel comes from the authoritative
`feeders/usgs-waterdata/usgs_waterdata_core` package. Regenerate/check it with
the repository USGS vendor-wheel helper
(`python feeders\usgs-iv\vendor_core.py`, then
`python feeders\usgs-iv\vendor_core.py --check`, Python 3.11+). CI import smoke
and the local notebook wheel builder verify and include that same wheel without
an unpublished PyPI dependency. Notebook users explicitly set acquisition variables and an accessible
reviewed enrollment path. No example-site default is installed.

Handwritten AMQP subclasses wait for remote broker acceptance and honor TLS
while [codegen#699](https://github.com/xregistry/codegen/issues/699) is unresolved.
Password connections explicitly select SASL PLAIN; insecure mechanisms are
allowed only for configured non-TLS AMQP. CBS authentication remains unchanged.
MQTT uses one application-owned connection for both families and confirms every
QoS 1 PUBACK before checkpointing. Missing or rejected acknowledgements and
local enqueue errors fail the cycle. This boundary addresses
[codegen#700](https://github.com/xregistry/codegen/issues/700).
The [codegen#698](https://github.com/xregistry/codegen/issues/698) JSON boundary
omits absent optional fields instead of sending schema-invalid nulls. None of
these boundaries changes generated files.

Network-restricted builders can select an approved TLS package index with
`--build-arg PIP_INDEX_URL=https://your-approved-index/simple`. Public PyPI
remains the build default; TLS verification stays enabled.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://waterdata.usgs.gov/>
- Continuous-observation API documentation: <https://api.waterdata.usgs.gov/docs/ogcapi/>

<!-- upstream-links:end -->

## Why this container

The USGS NWIS Water Quality source is exposed as a polling API upstream. These container images package polling cadence control, stateful dedupe, CloudEvents production, and transport/auth wiring so operators can deploy a ready-to-run feeder instead of building source-specific integration code.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-usgs-nwis-wq` | Apache Kafka 2.x | JSON CloudEvents on one topic; key template `{site_number}/{parameter_code}` |
| `ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-mqtt` | MQTT 5.0 | Unified-Namespace topic template `(see EVENTS.md)` |
| `ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-amqp` | AMQP 1.0 | Binary CloudEvents to AMQP node `usgs-nwis-wq` |

Event families in this source:

- **USGS.WaterQuality.Sites** — `MonitoringSite`.
- **USGS.WaterQuality.Readings** — `WaterQualityReading`.

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` (source Dockerfiles) |
| Default entry point | Kafka `["python", "-m", "usgs_nwis_wq", "feed"]`; MQTT `["python", "-m", "usgs_nwis_wq_mqtt", "feed"]`; AMQP `["python", "-m", "usgs_nwis_wq_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | process exits cleanly on `SIGTERM` |
| Persistent state | `USGS_WQ_LAST_POLLED_FILE`; mount a host volume for restart-safe dedupe/checkpoint behavior |
| Image tags | `:latest` and immutable release/sha tags published from repository CI |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
docker pull ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL/PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_WQ_LAST_POLLED_FILE=/state/usgs-nwis-wq.json \
  -e KAFKA_BOOTSTRAP_SERVERS="<host:port>" \
  -e KAFKA_TOPIC="<topic>" \
  -e SASL_USERNAME="<username>" \
  -e SASL_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_WQ_LAST_POLLED_FILE=/state/usgs-nwis-wq.json \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

## Using the MQTT image

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_WQ_LAST_POLLED_FILE=/state/usgs-nwis-wq.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_WQ_LAST_POLLED_FILE=/state/usgs-nwis-wq.json \
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  -e MQTT_CLIENT_ID="<unique-client-id>" \
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-mqtt:latest
```

## Using the AMQP image

### With AMQP 1.0 and Microsoft Entra ID (CBS put-token)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_WQ_LAST_POLLED_FILE=/state/usgs-nwis-wq.json \
  -e AMQP_HOST="<namespace>.servicebus.windows.net" \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS="usgs-nwis-wq" \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE="https://servicebus.azure.net/.default" \
  -e AMQP_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-amqp:latest
```

### With AMQP 1.0 and SAS-token CBS

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_WQ_LAST_POLLED_FILE=/state/usgs-nwis-wq.json \
  -e AMQP_HOST="servicebus-emulator" \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS="usgs-nwis-wq" \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey" \
  -e AMQP_SAS_KEY="<sas-key>" \
  ghcr.io/clemensv/real-time-sources-usgs-nwis-wq-amqp:latest
```

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `STATE_FILE` | Path to the JSON dedupe / resume state file. Mount persistent storage here for long-running deployments. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `USGS_WQ_PARAMETER_CODES` | Comma-separated USGS parameter codes (for example `00010` water temperature, `00300` dissolved oxygen) to request. |
| `USGS_WQ_SITES` | Comma-separated USGS site numbers to poll for water-quality data. |
| `USGS_WQ_STATES` | Comma-separated two-letter US state codes to scope water-quality sites. |

### Kafka image

| Variable | Description |
|---|---|
| `USGS_WQ_LAST_POLLED_FILE` | Path to dedupe/checkpoint state file. |
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string (optional alternative to explicit Kafka variables). |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | Kafka destination topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL/PLAIN credentials for Kafka. |
| `POLLING_INTERVAL` | Poll interval in seconds. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |

### MQTT image

| Variable | Description |
|---|---|
| `USGS_WQ_LAST_POLLED_FILE` | Path to dedupe/checkpoint state file. |
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for `MQTT_AUTH_MODE=password`. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID. |
| `MQTT_CLIENT_ID` | MQTT client ID (must be unique per broker). |
| `POLLING_INTERVAL` | Poll interval in seconds. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_HOST` | MQTT broker host (component-level alternative to `MQTT_BROKER_URL`). |
| `MQTT_PORT` | MQTT broker port (component-level alternative to `MQTT_BROKER_URL`). |
| `MQTT_TLS` | Set `true` to use TLS (`mqtts`) for the component-level connection. |

### AMQP image

| Variable | Description |
|---|---|
| `USGS_WQ_LAST_POLLED_FILE` | Path to dedupe/checkpoint state file. |
| `AMQP_BROKER_URL` | Full AMQP URL form (`amqp://` or `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component endpoint settings when URL form is not used. |
| `AMQP_ADDRESS` | AMQP node/address name. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra-ID CBS settings. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token CBS settings. |
| `POLLING_INTERVAL` | Poll interval in seconds. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |

## Deploying into Azure Container Instances

The candidate templates configure Azure Files checkpoint volumes with storage
Shared Key disabled. ACI uses a dedicated user-assigned managed identity and
the required **Storage File Data SMB MI Admin** role on the dedicated state
account. Existing broker identities, state paths and image dependencies are
unchanged. See the [shared template contract](../../tools/aci_files_identity.md)
for supported API versions, regeneration and mount/restart acceptance.
Live mounting has not passed acceptance; cloud release remains blocked.

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fusgs-nwis-wq%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fusgs-nwis-wq%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fusgs-nwis-wq%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fusgs-nwis-wq%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fusgs-nwis-wq%2Fazure-template.json)

## Related

- [README.md](README.md) — project overview and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schema details.
- [`xreg/usgs_nwis_wq.xreg.json`](xreg/usgs_nwis_wq.xreg.json) — source contract used to generate producer bindings.
