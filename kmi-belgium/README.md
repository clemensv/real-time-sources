# KMI Belgium Weather Observation Bridge

This bridge fetches real-time automatic weather station observations from the [Royal Meteorological Institute of Belgium (KMI/RMI)](https://opendata.meteo.be/) and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits two event types into the `kmi-belgium` topic, both keyed by `{station_code}`:

| Event Type | Description |
|---|---|
| `BE.Gov.KMI.Weather.Station` | Reference data for each active AWS station, derived from the latest observation features and emitted at startup |
| `BE.Gov.KMI.Weather.WeatherObservation` | Ten-minute AWS weather observations including precipitation, temperature, wind, humidity, pressure, sunshine, radiation, and soil temperatures |

The upstream API does not publish station names. Station reference events therefore contain the station code and WGS84 coordinates only.

## Upstream API

- **Base URL**: `https://opendata.meteo.be/service/aws/ows`
- **Protocol**: OGC WFS 2.0 with GeoJSON output
- **Feature type**: `aws:aws_10min`
- **Auth**: None (open data, CC BY 4.0)
- **Cadence**: 10-minute intervals
- **Polling shape**: `GetFeature` sorted by descending `timestamp`, optionally filtered with `CQL_FILTER=timestamp >= '{last_timestamp}'`
- **Coverage**: ~14 active Belgian AWS stations

## Source Files

| File | Description |
|---|---|
| [xreg/kmi_belgium.xreg.json](xreg/kmi_belgium.xreg.json) | xRegistry manifest (authoritative contract) |
| [kmi_belgium/kmi_belgium.py](kmi_belgium/kmi_belgium.py) | Runtime bridge |
| [generate_producer.ps1](generate_producer.ps1) | xrcg generator wrapper |
| [kmi_belgium_producer/](kmi_belgium_producer/) | Generated producer package (created from the xRegistry manifest) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Container deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |

## Running Locally

Generate the producer package first:

```powershell
.\generate_producer.ps1
```

Then run the bridge:

```powershell
poetry install
poetry run kmi-belgium list
poetry run kmi-belgium --connection-string "BootstrapServer=localhost:9092;EntityPath=kmi-belgium" feed
```

## Deployment Options

### Option 1: Run as a Python process

Use `poetry run kmi-belgium feed` with a Kafka or Event Hubs connection string and a persistent state file.

### Option 2: Run as a Docker container

Build or pull the image and configure it with environment variables as documented in [CONTAINER.md](CONTAINER.md).

### Option 3: Deploy to Azure Container Instances

Run the published container image in Azure Container Instances or another container host and bind a persistent volume for the state file.

### Option 4: Fabric notebook hosting

Deploy as a scheduled Microsoft Fabric notebook via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1) — see [`notebook/kmi-belgium-feed.ipynb`](notebook/kmi-belgium-feed.ipynb).
