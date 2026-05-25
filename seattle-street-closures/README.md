# Seattle Street Closures Bridge

## Overview

**Seattle Street Closures Bridge** polls the City of Seattle Open Data street closures dataset and emits one event per permitted closed street segment occurrence window.

The upstream dataset is the official **Street Closures** feed published by the Seattle Department of Transportation on `data.seattle.gov`. The dataset covers short-term street closures from issued street-use permits for non-construction activities such as block parties, play streets, farmers markets, and temporary activations.

## Upstream Audit

| Family | Transport | Identity | Keep/Drop | Why |
|---|---|---|---|---|
| Street Closures dataset | Socrata SODA JSON `/resource/ium9-iqtc.json` | `permit_number|segkey|start_date|end_date` | Keep | This is the closure event feed. |
| GeoJSON render | `/resource/ium9-iqtc.geojson` | same | Drop as separate family | Same records, alternate representation. |
| Dataset metadata | `/api/views/ium9-iqtc` | n/a | Keep for docs only | Useful for descriptions, not a separate stream. |
| Street use permit datasets | separate Socrata datasets | permit model | Drop | Upstream permit-issuance tables are not the closure event feed. |
| Street Network Database (SND) | separate Socrata dataset | `segkey` | Drop | Useful join table, but not part of the requested closure stream and it does not share the closure event identity. |

The bridge models closure rows only. It intentionally does not model permit issuance tables or the citywide street network as event families because they follow different lifecycles and identities.

## Event Model

- **StreetClosure** — one closed street segment occurrence window keyed by `closure_id`

The bridge derives `closure_id` from `permit_number`, `segkey`, `start_date`, and `end_date` because `permit_number` alone is not unique enough for closure rows.

## Running

```bash
python -m seattle_street_closures --connection-string "BootstrapServer=localhost:9092;EntityPath=seattle-street-closures"
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `SEATTLE_STREET_CLOSURES_STATE_FILE` | Path to persisted snapshot state |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template-with-eventhub.json)

## Upstream Links

- Dataset page: https://data.seattle.gov/Built-Environment/Street-Closures/ium9-iqtc
- SODA endpoint: https://data.seattle.gov/resource/ium9-iqtc.json
- API docs: https://dev.socrata.com/foundry/data.seattle.gov/ium9-iqtc

## Fabric notebook hosting

This bridge can also run as a scheduled Microsoft Fabric notebook (`notebook/seattle-street-closures-feed.ipynb`); deploy it via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1).


## MQTT and AMQP companion feeders

This source now ships separate MQTT and AMQP companion containers in addition to the Kafka/Event Hubs feeder. The MQTT container publishes binary-mode CloudEvents to the UNS topic templates declared in `xreg/`; the AMQP container publishes the same CloudEvents to an AMQP 1.0 address named `seattle-street-closures` by default.

- MQTT image: `ghcr.io/clemensv/real-time-sources-seattle-street-closures-mqtt:latest`
- AMQP image: `ghcr.io/clemensv/real-time-sources-seattle-street-closures-amqp:latest`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `infra/azure-template-amqp.json`, `infra/azure-template-with-servicebus.json`
