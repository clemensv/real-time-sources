# Hong Kong EPD AQHI Bridge

This bridge fetches the Hong Kong Environmental Protection Department's
[Air Quality Health Index (AQHI)](https://www.aqhi.gov.hk/) feed and emits
CloudEvents into Apache Kafka or Azure Event Hubs, MQTT 5.0, and AMQP 1.0.

## Data Model

The bridge emits two event types into the `hongkong-epd-aqhi` topic, keyed by
`{station_id}`:

| Event Type | Description |
|---|---|
| `HK.Gov.EPD.AQHI.Station` | Reference data for the 18 AQHI monitoring stations |
| `HK.Gov.EPD.AQHI.AQHIReading` | Latest AQHI reading per station, derived from the 24-hour XML feed |

## Upstream Feed Review

- **Feed**: `https://www.aqhi.gov.hk/epd/ddata/html/out/24aqhi_Eng.xml`
- **Transport**: HTTP polling of a public XML file
- **Auth**: None
- **Cadence**: Hourly
- **Identity**: Stable station IDs derived from the published station names
- **Feed coverage reviewed**:

| Family | Transport | Identity | Cadence | Decision |
|---|---|---|---|---|
| AQHI 24-hour history feed | XML file over HTTP | `station_id` | Hourly | Keep — bridge emits the latest reading per station |
| Station metadata | Hard-coded from EPD station map and feed station roster | `station_id` | Rarely changes | Keep — emitted as reference events |

The public feed is a single XML channel. It contains 24 hours of AQHI history
for 18 stations. The bridge keeps the latest record per station and publishes
reference data first so downstream consumers can build a temporally consistent
view.

## Source Files

| File | Description |
|---|---|
| [xreg/hongkong_epd.xreg.json](xreg/hongkong_epd.xreg.json) | xRegistry manifest |
| [hongkong_epd/hongkong_epd.py](hongkong_epd/hongkong_epd.py) | Runtime bridge |
| [hongkong_epd_producer/](hongkong_epd_producer/) | Generated producer (xrcg 0.10.1) |
| [hongkong_epd_mqtt_producer/](hongkong_epd_mqtt_producer/) | Generated MQTT producer (xrcg 0.10.6) |
| [hongkong_epd_mqtt/](hongkong_epd_mqtt/) | MQTT/UNS feeder app |
| [Dockerfile.mqtt](Dockerfile.mqtt) | MQTT container image |
| [notebook/hongkong-epd-feed.ipynb](notebook/hongkong-epd-feed.ipynb) | Fabric notebook hosting (deployed via [tools/deploy-fabric/deploy-feeder-notebook.ps1](../tools/deploy-fabric/deploy-feeder-notebook.ps1)) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-with-eventhub.json)

## AMQP 1.0 companion feeder

This source now ships Kafka, MQTT, and AMQP 1.0 transport variants. The AMQP container (`ghcr.io/clemensv/real-time-sources-hongkong-epd-amqp:latest`) publishes the same CloudEvents payloads as the Kafka and MQTT feeders to a single broker address named `hongkong-epd` by default, using binary-mode AMQP 1.0 for generic brokers or Azure Service Bus.

Run locally against an AMQP 1.0 broker:

```bash
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=hongkong-epd \
  -e AMQP_USERNAME=admin \
  -e AMQP_PASSWORD=admin \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-hongkong-epd-amqp:latest
```

Deploy to Azure Service Bus with `azure-template-with-servicebus.json` (also mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus queue, storage-backed state share, a user-assigned managed identity, and an Azure Container Instance configured for AMQP CBS / Entra ID authentication.

