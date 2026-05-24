# Seattle Fire 911 Bridge

## Overview

**Seattle Fire 911 Bridge** polls the City of Seattle Open Data feed for Seattle Fire Department 911 dispatches and forwards them to Kafka as CloudEvents.

The upstream is the official **Seattle Real Time Fire 911 Calls** dataset on `data.seattle.gov`. The dataset is updated every 5 minutes and exposes machine-readable JSON, CSV, and XML through the Socrata SODA API.

## Upstream Audit

The relevant upstream surface for this source is:

| Family | Transport | Identity | Keep/Drop | Why |
|---|---|---|---|---|
| Fire 911 calls dataset | Socrata SODA JSON `/resource/kzjm-xkqj.json` | `incident_number` | Keep | This is the live dispatch feed. |
| Dataset metadata | Socrata view metadata `/api/views/kzjm-xkqj` | n/a | Keep for docs only | Useful for field descriptions, not a business entity stream. |
| CSV/XML/RDF exports | Alternate renderings of same dataset | `incident_number` | Drop | Duplicate presentation of the same records. |
| Seattle police/public safety datasets nearby | Separate datasets | separate | Drop | Different upstream semantics and lifecycle. |

This source models the live dispatch feed only. The dataset does not expose a separate reference catalog for incident types or stations, so there is no reference-data event family to emit.

## Event Model

- **Incident** — one Seattle Fire Department 911 dispatch record keyed by `incident_number`

Dropped upstream fields:

- `report_location` — duplicate geometry presentation of `latitude` and `longitude`
- Socrata `:@computed_region_*` fields — platform-derived geographies, not authoritative incident fields

## Running

```bash
python -m seattle_911 --connection-string "BootstrapServer=localhost:9092;EntityPath=seattle-911"
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `SEATTLE_911_LAST_POLLED_FILE` | State file path for dedupe and resume state |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-eventhub.json)

## Fabric Notebook Hosting

This source can also be hosted in Microsoft Fabric as a scheduled notebook
feeder. See [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1)
and the notebook at [`notebook/seattle-911-feed.ipynb`](notebook/seattle-911-feed.ipynb).

## Upstream Links

- Dataset page: https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj
- SODA endpoint: https://data.seattle.gov/resource/kzjm-xkqj.json
- Socrata API docs: https://dev.socrata.com/

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-seattle-911-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variant for Seattle Fire 911 dispatch incidents. Topics are non-retained QoS-1 event messages under civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}. The incident_type_slug field is the deterministic lowercase kebab-case routing key derived from the display incident_type; incident_number preserves the CloudEvents subject/Kafka key for per-incident subscriptions. Message expiry is 86400 seconds for queued/offline delivery only; this event stream does not use retained MQTT state.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/seattle_911.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}` | `US.WA.Seattle.Fire911.Incident` | QoS 1, retain=false, expiry=86400s |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.
