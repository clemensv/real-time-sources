# Digitraffic Road — Finnish Road Traffic Data

Real-time road traffic data from the Finnish national road network operated by
Fintraffic. Telemetry is streamed via the Digitraffic MQTT service at
`wss://tie.digitraffic.fi/mqtt` and includes TMS sensor readings, road weather
sensor readings, traffic messages (incidents, road works, weight restrictions,
exempted transports), and maintenance vehicle tracking. Station metadata and
maintenance task type catalogs are fetched as reference data from the
Digitraffic REST API at startup.

## Data Source

- **Publisher**: Fintraffic
- **Documentation**: https://www.digitraffic.fi/en/road-traffic/
- **Protocol**: MQTT over WebSocket (telemetry), REST (reference data)
- **Auth**: None
- **License**: Creative Commons 4.0 BY
- **Update Frequency**: Real-time (sub-second via MQTT); reference data at startup

## Event Types

### Reference Data (emitted at startup from REST API)

| Type | Description |
|---|---|
| `fi.digitraffic.road.stations.TmsStation` | TMS station metadata (location, road address, sensors, free-flow speeds) |
| `fi.digitraffic.road.stations.WeatherStation` | Road weather station metadata (location, road address, sensors, collection interval) |
| `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType` | Maintenance task type catalog (multilingual names) |

### Telemetry (streamed continuously from MQTT)

| Type | Description |
|---|---|
| `fi.digitraffic.road.sensors.TmsSensorData` | Traffic measurement (speed, vehicle count) from a TMS station |
| `fi.digitraffic.road.sensors.WeatherSensorData` | Road weather measurement (temperature, wind, humidity) from a weather station |
| `fi.digitraffic.road.messages.TrafficAnnouncement` | Traffic incident or lane closure announcement |
| `fi.digitraffic.road.messages.RoadWork` | Active or planned road work with phases and restrictions |
| `fi.digitraffic.road.messages.WeightRestriction` | Weight restriction on a road or bridge |
| `fi.digitraffic.road.messages.ExemptedTransport` | Oversize or heavy transport advance notice |
| `fi.digitraffic.road.maintenance.MaintenanceTracking` | Maintenance vehicle position and task report |

See [EVENTS.md](EVENTS.md) for full payload documentation.

## Running

```shell
python -m digitraffic_road stream \
    --kafka-bootstrap-servers localhost:9092 \
    --kafka-topic-sensors digitraffic-road-sensors \
    --kafka-topic-messages digitraffic-road-messages \
    --kafka-topic-maintenance digitraffic-road-maintenance
```

Or with a connection string (topics configured via env vars):

```shell
python -m digitraffic_road stream \
    -c "BootstrapServer=localhost:9092"
```

Use `python -m digitraffic_road probe` to inspect live MQTT messages.

See [CONTAINER.md](CONTAINER.md) for Docker deployment.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventhub.json)
