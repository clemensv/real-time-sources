<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# Pegelonline

<sub>federal waterways, ~3,000 stations · Kafka · MQTT · AMQP · <a href="https://www.pegelonline.wsv.de/">upstream</a> · <a href="https://www.pegelonline.wsv.de/webservice/dokuRestapi">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — federal waterways, ~3,000 stations

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#pegelonline) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#pegelonline/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/pegelonline.kql) &nbsp;·&nbsp;
[🗺️ **Fabric Map**](fabric/README.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.pegelonline.wsv.de/)

</td></tr></table>
<!-- source-hero:end -->

## At a glance

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany (federal waterways)</td></tr>
<tr><td valign="middle">🏛️</td><td valign="middle"><b>Authority</b></td><td valign="middle"><a href="https://www.wsv.bund.de/">Wasserstraßen- und Schifffahrtsverwaltung des Bundes (WSV)</a></td></tr>
<tr><td valign="middle">📊</td><td valign="middle"><b>Coverage</b></td><td valign="middle">~1,200 stations on rivers, canals, estuaries</td></tr>
<tr><td valign="middle">⏱️</td><td valign="middle"><b>Cadence</b></td><td valign="middle">15-minute upstream sampling, 60-second poll</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT 5.0 · AMQP 1.0</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle"><code>Station</code> · <code>CurrentMeasurement</code></td></tr>
<tr><td valign="middle">📜</td><td valign="middle"><b>License</b></td><td valign="middle"><a href="https://www.govdata.de/dl-de/by-2-0">DL-DE→BY 2.0</a> (open)</td></tr>
<tr><td valign="middle">🔐</td><td valign="middle"><b>Auth</b></td><td valign="middle">None — public REST</td></tr>
</table>

The bridge turns the German [WSV PegelOnline](https://www.pegelonline.wsv.de/)
REST API into a real-time CloudEvents stream that consumers can subscribe to
instead of polling REST themselves. It handles the boring parts — ETag-aware
polling, per-station dedupe state, JsonStructure-validated payloads, identity
plumbing, retries — and ships as three drop-in transport variants.

**Who uses it.** Flood early-warning and civil protection (react to rising
gauges within one poll cycle across a basin); inland shipping operations
(Rhine, Mosel, Elbe fairway-depth thresholds at Kaub, Maxau, Emmerich, …);
hydropower and water-management dispatch (intraday market bidding with
up-to-the-minute headwater/tailwater); environmental compliance and research
(long-running dedupe-aware ingestion into Fabric Eventhouse / ADX / lakes);
insurance and risk (parametric flood triggers, live exposure dashboards).

## 60-second quick start

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/pegelonline.json \
  -e CONNECTION_STRING="Endpoint=sb://<ns>.servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=pegelonline" \
  ghcr.io/clemensv/real-time-sources-pegelonline-kafka:latest
```

That's it. The first cycle emits ~1,200 `Station` reference events; every
subsequent 60 s cycle emits only the gauges with new measurements (typically
~50–200 events). Mount `./state` to persist dedupe across restarts.

MQTT and AMQP variants take the same form — see
[CONTAINER.md](CONTAINER.md) for the per-transport env-var matrix.

## Architecture

```mermaid
flowchart LR
    A[WSV PegelOnline<br/>REST API] -->|HTTPS poll<br/>ETag-aware| B[pegelonline_core<br/>poller + dedupe]
    B -->|Station ref| C{{xRegistry contract<br/>pegelonline.xreg.json}}
    B -->|CurrentMeasurement| C
    C --> D[pegelonline_kafka]
    C --> E[pegelonline_mqtt]
    C --> F[pegelonline_amqp]
    D -->|key=station_id<br/>ce_* headers| K[(Kafka /<br/>Event Hubs /<br/>Fabric Event Stream)]
    E -->|UNS topic tree<br/>QoS 1, retained| M[(MQTT 5.0 broker /<br/>Event Grid namespace)]
    F -->|AMQP message<br/>Entra ID via CBS| Q[(Service Bus /<br/>Event Hubs AMQP /<br/>Artemis)]
```

All three variants share the upstream poller (`pegelonline_core`), the
xRegistry contract (`xreg/pegelonline.xreg.json`), and the CloudEvents
schemas — switching transport never changes the data model.

## Sample event

<details>
<summary><b><code>de.wsv.pegelonline.CurrentMeasurement</code></b> — live water-level reading (click to expand)</summary>

```json
{
  "specversion": "1.0",
  "type": "de.wsv.pegelonline.CurrentMeasurement",
  "source": "https://www.pegelonline.wsv.de/webservices/rest-api/v2",
  "id": "01985f6c-2f55-7c4f-9d2a-3a8e64c4e2a1",
  "time": "2026-05-27T07:30:00Z",
  "subject": "stations/MAXAU/water-level",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "MAXAU",
    "station_uuid": "85d52e5a-d92a-4d97-8d62-cf2b91d6f0ff",
    "water_shortname": "RHEIN",
    "timestamp": "2026-05-27T07:30:00+02:00",
    "value": 482.0,
    "unit": "cm",
    "state_mnw": "above",
    "state_mhw": "below",
    "trend": 1
  }
}
```

The Kafka record carries the same JSON in the value, the CloudEvents
attributes as `ce_*` headers (binary content mode), and the Kafka key
set to `MAXAU` (the `{station_id}` template). On MQTT the same JSON
is published to `hydro/de/wsv/pegelonline/RHEIN/MAXAU/water-level`
(QoS 1, retained, CloudEvents attributes as MQTT 5 user properties).
On AMQP the same JSON is the application body with the CloudEvents
attributes as `cloudEvents:*` application properties.

See [EVENTS.md](EVENTS.md) for the full schemas of both event types
(`Station` and `CurrentMeasurement`) and the JsonStructure constraints.

</details>

## Transport variants

| Variant | Container image | Targets | Wire shape |
|---|---|---|---|
| **🟥 Kafka** | `ghcr.io/clemensv/real-time-sources-pegelonline-kafka` | Apache Kafka 2.x · Azure Event Hubs · Fabric Event Streams · Confluent · Redpanda · Aiven · MSK | Single topic, binary CloudEvents (`ce_*` headers), key = `{station_id}` |
| **🟪 MQTT** | `ghcr.io/clemensv/real-time-sources-pegelonline-mqtt` | Mosquitto · EMQX · HiveMQ · Azure Event Grid namespace · Fabric Real-Time Hub MQTT broker | UNS tree `hydro/de/wsv/pegelonline/{water}/{station}/...`, QoS 1, retained, CloudEvents as MQTT 5 user properties |
| **🟦 AMQP** | `ghcr.io/clemensv/real-time-sources-pegelonline-amqp` | Azure Service Bus · Azure Event Hubs (AMQP surface) · ActiveMQ Artemis · Qpid · RabbitMQ AMQP 1.0 plugin | Single AMQP node, binary CloudEvents, SASL PLAIN or Entra ID via AMQP CBS (no SAS-key rotation) |

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

Pegelonline targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/), and the bundled [Fabric Map](fabric/README.md) visualizes the live state on a basemap.

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#pegelonline) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `pegelonline` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/pegelonline/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source pegelonline `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#pegelonline/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source pegelonline `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#pegelonline/fabric-aci)

#### Fabric Map visualization &nbsp;<sub><i>(optional, post-deploy)</i></sub>

After either hosting model has events flowing, run [`fabric/post-deploy.ps1`](fabric/README.md) (or `tools/deploy-fabric/deploy-fabric.ps1 -Source pegelonline -Workspace <ws>`) to provision the bundled Fabric Map item and wire its Kusto-backed layers onto a basemap. The map updates live as new events arrive.


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Configuration

<details>
<summary>Full environment-variable reference (click to expand)</summary>

| Variable | Variant | Purpose | Default |
|---|---|---|---|
| `CONNECTION_STRING` | Kafka | Kafka 2.x SASL/PLAIN over TLS, or Azure Event Hubs / Fabric Event Stream connection string | required |
| `MQTT_BROKER_URL` | MQTT | `mqtts://host:8883` or `mqtt://host:1883` | required |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | MQTT | Username/password for SASL or Event Grid SAS | optional |
| `MQTT_AAD_*` | MQTT | Entra ID JWT enhanced auth for Event Grid namespace | optional |
| `AMQP_BROKER_URL` | AMQP | `amqp[s]://[user[:pass]@]host[:port]/<entity>` | required (or Entra/CBS env) |
| `AMQP_CBS_*` | AMQP | Entra ID for Service Bus / Event Hubs CBS put-token | optional |
| `STATE_FILE` | all | Path to dedupe state file (mount a volume!) | `/state/pegelonline.json` |
| `POLL_INTERVAL_SECONDS` | all | Upstream poll cadence | `60` |
| `STATIONS_REFRESH_SECONDS` | all | Station-catalog re-emit cadence | `3600` |
| `ONCE` | all | Run a single poll cycle and exit (for cron/Fabric notebook) | `false` |
| `LOG_LEVEL` | all | `DEBUG` / `INFO` / `WARNING` / `ERROR` | `INFO` |

The full per-deployment-shape env-var matrix (Entra ID via CBS or
OAUTH2-JWT, SAS-token CBS, Service Bus emulator, etc.) lives in
[CONTAINER.md](CONTAINER.md). The runtime entry point for every image
is `python -m pegelonline_{kafka,mqtt,amqp} feed`; the image's default
`CMD` invokes it for you.

</details>

## Data model

Two event types, both in message group `de.wsv.pegelonline`:

- **`Station`** — reference event, emitted at startup and refreshed every
  `STATIONS_REFRESH_SECONDS`. Carries the station identity, river/water
  body name, geo coordinates, gauge zero / PNP datum, and the long-name
  used by WSV publications. Subject: `stations/{station_id}/info`.
- **`CurrentMeasurement`** — telemetry event, emitted per gauge per poll
  cycle whenever the upstream value or timestamp has changed. Carries
  the timestamp, value, unit, trend, and threshold-state flags
  (above/below MNW, MHW, etc.). Subject: `stations/{station_id}/water-level`.

Both events are keyed by `{station_id}` so a consumer joining a
`Station`-keyed KTable with a `CurrentMeasurement`-keyed stream always
sees the temporally consistent station metadata for each measurement —
see [Streamifying reference data for temporal consistency with
telemetry events](https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events)
for the design rationale.

The complete JsonStructure schemas (with units, validation constraints,
and Avro round-trip) are in [EVENTS.md](EVENTS.md).

## Repository layout

```text
pegelonline/
├── xreg/pegelonline.xreg.json     # shared xRegistry contract
├── pegelonline_core/              # transport-agnostic poller
├── pegelonline_kafka/             # Kafka feeder application
├── pegelonline_mqtt/              # MQTT/UNS feeder application
├── pegelonline_amqp/              # AMQP 1.0 feeder application
├── pegelonline_producer/          # xRegistry-generated Kafka producer
├── pegelonline_mqtt_producer/     # xRegistry-generated MQTT producer
├── pegelonline_amqp_producer/     # xRegistry-generated AMQP producer
├── kql/pegelonline.kql            # Eventhouse table + update policies
├── notebook/pegelonline-feed.ipynb # Fabric Notebook feeder
├── fabric/                        # 8-layer Fabric Map
├── Dockerfile.kafka               # builds the Kafka feeder image
├── Dockerfile.mqtt                # builds the MQTT feeder image
├── Dockerfile.amqp                # builds the AMQP feeder image
└── tests/                         # unit + integration tests
```

## Prerequisites (for self-hosted runs)

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS to `pegelonline.wsv.de` — no credentials required.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted at `/state` so dedupe state survives
  restarts. **Without it, dedupe restarts cold on every container start.**

---

<sub>
📚 <a href="../README.md">← Back to catalog</a> &nbsp;·&nbsp;
🌐 <a href="https://clemensv.github.io/real-time-sources/#pegelonline">Portal entry</a> &nbsp;·&nbsp;
📑 <a href="EVENTS.md">EVENTS.md</a> &nbsp;·&nbsp;
🐳 <a href="CONTAINER.md">CONTAINER.md</a> &nbsp;·&nbsp;
🗄️ <a href="kql/pegelonline.kql">KQL schema</a> &nbsp;·&nbsp;
🗺️ <a href="fabric/README.md">Fabric Map</a> &nbsp;·&nbsp;
↗ <a href="https://www.pegelonline.wsv.de/">pegelonline.wsv.de</a> &nbsp;·&nbsp;
📖 <a href="https://www.pegelonline.wsv.de/webservice/dokuRestapi">REST API docs</a>
</sub>
