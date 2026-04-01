# European Water Services - Combined Container Group

Deploys all 12 European waterway information services as sidecars in a single
container group, sharing one Kafka/Event Hub connection.

## Included Services

| Service | Country | Data |
|---------|---------|------|
| [Pegelonline](../../pegelonline/CONTAINER.md) | Germany | Water levels, flow rates |
| [CHMI Hydro](../../chmi-hydro/CONTAINER.md) | Czech Republic | Water levels, discharge, temperature |
| [IMGW Hydro](../../imgw-hydro/CONTAINER.md) | Poland | Water levels, discharge, temperature |
| [SMHI Hydro](../../smhi-hydro/CONTAINER.md) | Sweden | Water levels, discharge |
| [Hub'Eau Hydrometrie](../../hubeau-hydrometrie/CONTAINER.md) | France | Water levels, flow rates |
| [UK EA Flood Monitoring](../../uk-ea-flood-monitoring/CONTAINER.md) | England | River levels, flood data |
| [RWS Waterwebservices](../../rws-waterwebservices/CONTAINER.md) | Netherlands | Water levels |
| [Waterinfo VMM](../../waterinfo-vmm/CONTAINER.md) | Belgium (Flanders) | Water levels |
| [NVE Hydro](../../nve-hydro/CONTAINER.md) | Norway | Water levels, discharge |
| [SYKE Hydro](../../syke-hydro/CONTAINER.md) | Finland | Water levels, discharge |
| [BAFU Hydro](../../bafu-hydro/CONTAINER.md) | Switzerland | Water levels, discharge, temperature |
| [German Waters](../../german-waters/README.md) | Germany (state agencies) | Water levels, discharge |

## Resource Requirements

All 12 containers share the CPU allocation. Most containers request 0.1 CPU and
0.3 GB memory; German Waters requests 0.2 CPU and 0.5 GB due to its larger
workload (12 state providers, ~2,700 stations). These bridges are I/O-bound
(HTTP polling + Kafka producing) and typically use <0.1 CPU cores at steady state.

| | Standard container | German Waters | Total (12 containers) |
|---|---|---|---|
| CPU | 0.1 cores | 0.2 cores | 1.3 cores |
| Memory | 0.3 GB | 0.5 GB | 3.8 GB |

## Deploy to Azure Container Instances

### PowerShell (Az module)

```powershell
./deploy.ps1 -ResourceGroupName eurowater-rg -ConnectionString "Endpoint=sb://..."
```

### Azure CLI (Bash)

```bash
./deploy.sh eurowater-rg "Endpoint=sb://..."
```

Both scripts create the resource group if it doesn't exist (default region:
`westeurope`) and deploy the ARM template.

### ARM Template Direct

```bash
az deployment group create \
    --resource-group eurowater-rg \
    --template-file azure-template.json \
    --parameters connectionStringSecret="Endpoint=sb://..."
```

## Run with Docker Compose

All containers share the same Kafka target via environment variables.

### With an Event Hub / Fabric Event Stream connection string

```bash
CONNECTION_STRING="Endpoint=sb://..." docker compose up -d
```

### With a plain Kafka broker

```bash
KAFKA_BOOTSTRAP_SERVERS=broker:9092 \
KAFKA_TOPIC=eurowater \
KAFKA_ENABLE_TLS=false \
docker compose up -d
```

### Stop

```bash
docker compose down
```

## Environment Variables

All containers accept the same Kafka configuration:

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hub / Fabric Event Stream connection string | |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address (alternative to connection string) | |
| `KAFKA_TOPIC` | Kafka topic name (alternative to connection string) | |
| `KAFKA_ENABLE_TLS` | Enable SSL/TLS for the Kafka connection | `true` |
| `NVE_API_KEY` | API key for NVE Hydro (Norway) | |

State files are persisted to a shared volume (`/mnt/fileshare` on ACI,
`eurowater-data` Docker volume) so containers resume from where they left off
after restarts.
