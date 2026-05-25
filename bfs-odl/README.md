# BfS ODL — Ambient Gamma Dose Rate Monitoring

This bridge fetches real-time ambient gamma dose rate data from the German
Federal Office for Radiation Protection (Bundesamt für Strahlenschutz, BfS)
ODL (Ortsdosisleistung) monitoring network and publishes it as CloudEvents
into Apache Kafka.

## Data Source

The BfS operates approximately 1,700 stationary measurement probes across
Germany as part of the IMIS (Integrated Measuring and Information System)
network. Each probe continuously samples ambient gamma radiation and reports
hourly averaged dose rate values.

- **API**: OGC Web Feature Service (WFS) at `https://www.imis.bfs.de/ogc/opendata/ows`
- **Format**: GeoJSON
- **Auth**: None (open data)
- **Update Frequency**: Hourly (1-hour aggregated measurements)
- **Coverage**: ~1,700 stations across Germany
- **Documentation**: https://odlinfo.bfs.de/ODL/EN/service/data-interface/data-interface_node.html

## Event Types

| CloudEvents Type | Description |
|---|---|
| `de.bfs.odl.Station` | Station metadata (reference data) — location, elevation, status |
| `de.bfs.odl.DoseRateMeasurement` | 1-hour averaged gamma dose rate — gross, cosmic, terrestrial components |

## Data Model

### Station (Reference)

Each station record includes:
- **station_id** (`kenn`): 9-digit BfS identifier derived from the official municipality key
- **station_code** (`id`): Alphanumeric code like `DEZ0305`
- **name**: Municipality or locality name
- **postal_code** (`plz`): German 5-digit PLZ
- **site_status**: 1 = in operation
- **height_above_sea**: Elevation in meters (determines cosmic radiation component)
- **longitude / latitude**: WGS84 coordinates

### Dose Rate Measurement (Telemetry)

Each measurement reports:
- **value**: Gross ambient gamma dose rate in µSv/h (typically 0.05–0.18 for normal background)
- **value_cosmic**: Cosmic radiation component (altitude-dependent)
- **value_terrestrial**: Terrestrial component (geology-dependent)
- **validated**: Quality control flag (1 = validated)
- **nuclide**: Measurement type, always `Gamma-ODL-Brutto`
- **start_measure / end_measure**: 1-hour measurement window in UTC

## Kafka Key

All events are keyed by `{station_id}` (the 9-digit `kenn` identifier), so
both station metadata and dose rate readings for the same probe share the
same partition.

## MQTT / Unified Namespace

A separate container (`bfs-odl-mqtt`) publishes the same data as MQTT 5.0
binary-mode CloudEvents into a UNS topic tree:

```
radiation/de/bfs/bfs-odl/{state}/{station_id}/info
radiation/de/bfs/bfs-odl/{state}/{station_id}/dose-rate
```

The `{state}` axis is derived from the first two digits of the station
Kennziffer (AGS Bundesland code). All messages are retained with QoS 1.
See [CONTAINER.md](CONTAINER.md) for MQTT-specific details.

## Upstream Links

- BfS ODL Info: https://odlinfo.bfs.de/
- Data interface documentation: https://odlinfo.bfs.de/ODL/EN/service/data-interface/data-interface_node.html
- Data structure PDF: https://odlinfo.bfs.de/SharedDocs/Downloads/ODL/EN/datenbereitstellung-en.pdf
- Terms of use: https://www.imis.bfs.de/geoportal/resources/sitepolicy.html

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-with-eventhub.json)

## Fabric notebook hosting

This bridge can also run as a scheduled Fabric notebook
(`notebook/bfs-odl-feed.ipynb`) deployed via
[`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1),
which builds a per-source Fabric Environment, binds Lakehouse + KQL +
Event Stream, and schedules single-cycle runs of `bfs-odl feed --once`.

## AMQP 1.0 companion feeder

This source also ships an AMQP 1.0 companion container, `ghcr.io/clemensv/real-time-sources-bfs-odl-amqp:latest`, for queue-oriented consumers using generic AMQP brokers or Azure Service Bus. It emits the same CloudEvents and payload schemas as the Kafka and MQTT variants on a single broker address (default `bfs-odl`).

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=bfs-odl   ghcr.io/clemensv/real-time-sources-bfs-odl-amqp:latest
```

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-amqp.json)

