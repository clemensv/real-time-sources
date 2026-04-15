# Puget Sound - Combined Container Group

Deploys Seattle- and Puget Sound-focused bridges as sidecars in a single
container group, sharing one Kafka/Event Hubs/Fabric Event Stream connection.

## Included Services

| Service | Coverage | Data |
|---|---|---|
| [Seattle 911](../../seattle-911/CONTAINER.md) | Seattle | Fire dispatch incidents |
| [Seattle street closures](../../seattle-street-closures/CONTAINER.md) | Seattle | Active street closures |
| [King County marine](../../king-county-marine/CONTAINER.md) | King County / Puget Sound | Buoy and mooring water quality |
| [EPA UV](../../epa-uv/CONTAINER.md) | Seattle | UV forecasts |
| [NWS forecasts](../../nws-forecasts/CONTAINER.md) | Seattle and central Puget Sound forecast zones | Land and marine forecast snapshots |
| [WSDOT](../../wsdot/CONTAINER.md) | Washington / Puget Sound | Ferries, mountain passes, roads, tolls, weather, traffic |
| [NOAA](../../noaa/CONTAINER.md) | Puget Sound CO-OPS stations | Water level, tide predictions, and available meteorology across Seattle-area stations |

## Scope choices

- The NOAA coverage is limited to these Puget Sound CO-OPS stations instead of
  polling the full national catalog: `9444090` Port Angeles, `9444900` Port
  Townsend, `9445958` Bremerton, `9446484` Tacoma, `9447130` Seattle,
  `9449424` Cherry Point, and `9449880` Friday Harbor.
- The EPA UV bridge is pinned to `Seattle,WA`.
- The NWS forecast bridge is pinned to Seattle-vicinity public and marine forecast zones: land `WAZ312`, `WAZ315`, `WAZ316`, `WAZ317`; marine `PZZ130`, `PZZ131`, `PZZ132`, `PZZ133`, `PZZ134`, `PZZ135`.
- The WSDOT bridge uses `REGION_FILTER=Northwest,Olympic` for traffic-flow
  scoping, but ferry, mountain-pass, weather, toll, and other statewide WSDOT
  feeds remain enabled because the bridge exposes them as part of its standard
  event families.

## Resource Requirements

Most bridges here are I/O-bound pollers. A small ACI group is sufficient.

| | Standard container | Heavier containers | Total |
|---|---|---|---|
| CPU | 0.1 cores | WSDOT 0.2, seven NOAA sidecars at 0.2 each | 2.1 cores |
| Memory | 0.3 GB | WSDOT 0.5, seven NOAA sidecars at 0.4 each | 4.8 GB |

## Deploy to Azure Container Instances

```powershell
./deploy.ps1 -ResourceGroupName pugetsound-rg -ConnectionString "Endpoint=sb://..." -WsdotAccessCode "<code>"
```

The script creates the resource group if needed and deploys the ARM template in
`westus2` by default.

## Run with Docker Compose

### With an Event Hub / Fabric Event Stream connection string

```powershell
$env:CONNECTION_STRING = "Endpoint=sb://..."
$env:WSDOT_ACCESS_CODE = "<code>"
docker compose up -d
```

### With a plain Kafka broker

```powershell
$env:KAFKA_BOOTSTRAP_SERVERS = "broker:9092"
$env:KAFKA_TOPIC = "pugetsound"
$env:KAFKA_ENABLE_TLS = "false"
$env:WSDOT_ACCESS_CODE = "<code>"
docker compose up -d
```

## Environment Variables

All containers accept the shared Kafka configuration:

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hub / Fabric Event Stream connection string | |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address | |
| `KAFKA_TOPIC` | Kafka topic | |
| `KAFKA_ENABLE_TLS` | Enable SSL/TLS for Kafka | `true` |
| `WSDOT_ACCESS_CODE` | Required WSDOT API access code | |

State is persisted to the shared volume so polling resumes cleanly after
restarts.

## Fabric

The Fabric assets in [fabric](fabric/README.md) create a raw CloudEvents landing
database and Event Stream. Existing bridge-local KQL is reused for WSDOT and
NOAA, and supplemental KQL fans out Seattle 911, Seattle street closures, King
County marine, EPA UV, and NWS forecast zones from the shared
`_cloudevents_dispatch` table.
