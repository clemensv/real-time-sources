# RWS Waterwebservices (Netherlands) Water Level Bridge

This project bridges water level data from the Dutch
[Rijkswaterstaat Waterwebservices](https://waterwebservices.rijkswaterstaat.nl/)
API to Apache Kafka, emitting CloudEvents.

**Rijkswaterstaat** (RWS) is the executive agency of the Dutch Ministry of
Infrastructure and Water Management. It manages the main waterways, roads, and
water systems in the Netherlands and publishes real-time water data through the
Waterwebservices API.

## Data

- **Stations**: ~785 monitoring locations measuring water level across the Netherlands
- **Water Level**: Water height (WATHTE) for surface water (OW) in cm, 10-minute intervals
- **Polling interval**: 10 minutes

The API is a POST-based JSON REST service. No authentication required. Data is
published under CC0 (public domain).

## Usage

### List stations

```bash
python -m rws_waterwebservices list
```

### Get latest water level for a station

```bash
python -m rws_waterwebservices level HOlv
```

### Feed to Kafka

Using a connection string (Azure Event Hubs):

```bash
python -m rws_waterwebservices feed -c "Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..."
```

Using explicit Kafka configuration:

```bash
python -m rws_waterwebservices feed \
    --kafka-bootstrap-servers your-server:9093 \
    --kafka-topic rws-waterwebservices \
    --sasl-username '$ConnectionString' \
    --sasl-password 'your-connection-string'
```

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents message definitions.

## MQTT / Unified Namespace

An MQTT 5.0 feeder publishes the same data into a UNS topic tree:
`hydro/nl/rws/rws-waterwebservices/{station_code}/{info|water-level}`.
See [CONTAINER.md](CONTAINER.md) for the MQTT container image and environment variables.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker container deployment info.

## Fabric notebook hosting

This source can also run as a scheduled Microsoft Fabric notebook via
[`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1),
which packages the bridge as a Fabric Environment and schedules
`notebook/rws-waterwebservices-feed.ipynb` to run one polling cycle per tick.

## API Reference

- **Base URL**: `https://ddapi20-waterwebservices.rijkswaterstaat.nl`
- **Protocol**: POST-based JSON REST
- **Key endpoints**:
  - `METADATASERVICES/OphalenCatalogus` — catalog of available parameters
  - `ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen` — latest observations
  - `ONLINEWAARNEMINGENSERVICES/OphalenWaarnemingen` — historical observations
- **Swagger**: `https://ddapi20-waterwebservices.rijkswaterstaat.nl/swagger-ui/index.html`
- **No authentication required**
- **License**: CC0 (public domain)

## Daily Volume Estimate

- ~785 water level stations × 144 readings/day (10 min) = ~113,000 readings/day
- Each CloudEvent ≈ 500 bytes → ~57 MB/day
- Plus ~785 station reference events at startup

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-with-eventhub.json)

## AMQP 1.0 companion feeder

This source now ships the standard Kafka + MQTT + AMQP transport trio. The AMQP companion runs from `rws_waterwebservices_amqp/`, uses the generated `rws_waterwebservices_amqp_producer/` package, and publishes the same CloudEvents and schemas documented in `EVENTS.md` to one AMQP 1.0 address (default `rws-waterwebservices`). It supports generic AMQP 1.0 brokers with SASL PLAIN and Azure Service Bus / Event Hubs with CBS token authentication.

Build and run locally:

```bash
docker build -f Dockerfile.amqp -t rws-waterwebservices-amqp .
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/rws-waterwebservices \
  -e ONCE_MODE=true \
  rws-waterwebservices-amqp
```

For Azure Service Bus, deploy `azure-template-with-servicebus.json` (also mirrored at `infra/azure-template-amqp.json`) or run the container with `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_TLS=true`, and `AMQP_ADDRESS=rws-waterwebservices`.

