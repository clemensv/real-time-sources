# GraceDB Gravitational Wave Candidate Alerts

GraceDB (Gravitational-Wave Candidate Event Database) is a public database
maintained by the LIGO/Virgo/KAGRA collaboration that tracks gravitational wave
candidate events (superevents) detected by the worldwide network of
gravitational wave observatories.

This bridge polls the GraceDB public REST API for new superevents and forwards
them to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

## Source

- **API**: https://gracedb.ligo.org/api/superevents/?format=json
- **Auth**: None (public read access)
- **Update frequency**: Events posted within seconds of detection; bridge polls
  every 2 minutes
- **Coverage**: Global — LIGO Hanford (H1), LIGO Livingston (L1), Virgo (V1),
  KAGRA (K1)

## Events

The bridge emits a single event type, documented in [EVENTS.md](EVENTS.md):

- `org.ligo.gracedb.Superevent` — Gravitational wave candidate superevent with
  ID, category, false alarm rate, labels, preferred pipeline event metadata.

## Related

- [GraceDB Web Interface](https://gracedb.ligo.org/)
- [GraceDB API Docs](https://gracedb.ligo.org/documentation/rest.html)
- [LIGO Scientific Collaboration](https://www.ligo.org/)

## Fabric notebook hosting

This source can also be hosted as a scheduled Fabric notebook via
[`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1)
which deploys `gracedb/notebook/gracedb-feed.ipynb` to a Fabric workspace.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-with-eventhub.json)

## Transports

This source now ships separate Kafka, MQTT, and AMQP containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-gracedb-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variant for GraceDB superevents. Non-retained QoS-1 event stream routed by category, physics group, and superevent id under seismic/intl/ligo/gracedb/...

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/gracedb.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `seismic/intl/ligo/gracedb/{category}/{group}/{superevent_id}/superevent` | `org.ligo.gracedb.Superevent` | QoS 1, retain=false |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion feeder

This source also ships an AMQP 1.0 companion container, `ghcr.io/clemensv/real-time-sources-gracedb-amqp:latest`, for queue-oriented consumers using generic AMQP brokers or Azure Service Bus. It emits the same CloudEvents and payload schemas as the Kafka and MQTT variants on a single broker address (default `gracedb`).

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=gracedb   ghcr.io/clemensv/real-time-sources-gracedb-amqp:latest
```

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-amqp.json)

