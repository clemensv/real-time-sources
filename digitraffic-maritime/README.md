# Digitraffic Maritime feeder

> See also: [CONTAINER.md](CONTAINER.md) · [EVENTS.md](EVENTS.md)

Digitraffic Maritime ingests Finland's open marine traffic feeds from Fintraffic and republishes them as CloudEvents.

> Source: Fintraffic / digitraffic.fi, license CC 4.0 BY.

## Source scope

- **AIS stream** from `wss://meri.digitraffic.fi:443/mqtt` (vessel locations + metadata)
- **Port call APIs** (`/port-calls`, `/vessel-details`, `/ports`) for visit telemetry plus companion reference data

The feeder preserves five event families:

- `fi.digitraffic.marine.ais.VesselLocation`
- `fi.digitraffic.marine.ais.VesselMetadata`
- `fi.digitraffic.marine.portcall.PortCall`
- `fi.digitraffic.marine.portcall.VesselDetails`
- `fi.digitraffic.marine.portcall.PortLocation`

## Transport variants

| Variant | Image | Transport | Default target |
|---|---|---|---|
| Kafka | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest` | Kafka protocol / Event Hubs compatible | Topic `digitraffic-maritime` |
| MQTT | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime-mqtt:latest` | MQTT 5.0, CloudEvents binary mode | UNS topics under `maritime/fi/fintraffic/digitraffic-maritime/...` |
| AMQP | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime-amqp:latest` | AMQP 1.0, CloudEvents binary mode | Address `digitraffic-maritime` |

## Repository layout

```text
digitraffic-maritime/
  digitraffic_maritime/                  # shared source integration (AIS + port-calls)
  digitraffic_maritime_producer/         # generated Kafka producer
  digitraffic_maritime_mqtt_producer/    # generated MQTT producer
  digitraffic_maritime_amqp_producer/    # generated AMQP producer
  digitraffic_maritime_mqtt/             # MQTT feeder app
  digitraffic_maritime_amqp/             # AMQP feeder app
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
  xreg/digitraffic_maritime.xreg.json
```

## Quick start

### Kafka image

```bash
docker run --rm \
  -e CONNECTION_STRING='BootstrapServer=<host:9092>;EntityPath=digitraffic-maritime' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### MQTT image

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtt://broker:1883' \
  -e DIGITRAFFIC_MODE='port-calls' \
  -e ONCE_MODE='true' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime-mqtt:latest
```

### AMQP image

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://user:password@broker:5672/digitraffic-maritime' \
  -e DIGITRAFFIC_MODE='port-calls' \
  -e ONCE_MODE='true' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime-amqp:latest
```

## Azure deployment templates

- `azure-template.json` (Kafka, BYO Event Hub/Event Stream)
- `azure-template-with-eventhub.json` (Kafka + new Event Hub)
- `azure-template-mqtt.json` (MQTT, BYO broker)
- `azure-template-with-eventgrid-mqtt.json` (MQTT + Event Grid namespace)
- `azure-template-with-servicebus.json` (AMQP + Service Bus)

## Related

- [Digitraffic Maritime portal](https://www.digitraffic.fi/en/marine-traffic/)
- [Fintraffic](https://www.fintraffic.fi)
- [Kystverket AIS feeder](../kystverket-ais/README.md)
