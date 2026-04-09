# US CBP Border Wait Times

This bridge fetches real-time wait times at US land border crossings from the
US Customs and Border Protection (CBP) Border Wait Time API and publishes
them as CloudEvents into Apache Kafka.

## Data Source

The CBP publishes wait times at approximately 81 land border ports of entry
along the US-Canada and US-Mexico borders. Data includes delay in minutes
and number of open lanes for passenger vehicles, pedestrians, and commercial
vehicles, broken down by lane type (standard, SENTRI/NEXUS, Ready Lane, FAST).

- **API**: `https://bwt.cbp.gov/api/bwtnew`
- **Format**: JSON
- **Auth**: None (US Government public domain)
- **Update Frequency**: Approximately hourly
- **Coverage**: ~81 ports across Canadian and Mexican borders
- **Documentation**: https://bwt.cbp.gov/

## Event Types

| CloudEvents Type | Description |
|---|---|
| `gov.cbp.borderwait.Port` | Port of entry metadata (reference data) — name, border, crossing, hours, max lanes |
| `gov.cbp.borderwait.WaitTime` | Current wait times — delay in minutes, lanes open, operational status per lane type |

## Data Model

### Port (Reference)

Each port record includes:
- **port_number**: Six-digit CBP port code (stable key)
- **port_name**: City or locality name
- **border**: 'Canadian Border' or 'Mexican Border'
- **crossing_name**: Specific crossing facility name
- **hours**: Operating hours
- **passenger_vehicle_max_lanes / commercial_vehicle_max_lanes / pedestrian_max_lanes**: Maximum lane counts

### WaitTime (Telemetry)

Each wait time report includes flattened lane-level data:
- **Passenger Vehicles**: standard, NEXUS/SENTRI, Ready Lane — delay, lanes open, status
- **Pedestrians**: standard, Ready Lane — delay, lanes open, status
- **Commercial Vehicles**: standard, FAST — delay, lanes open, status
- **port_status**: Overall port status (typically 'Open')
- **construction_notice**: Active construction or closure notices

Operational status values: `no delay`, `delay`, `N/A`, `Lanes Closed`, `Update Pending`.

## Kafka Key

All events are keyed by `{port_number}` (the six-digit CBP port code), so
both port metadata and wait time readings for the same crossing share the
same partition.

## Upstream Links

- CBP Border Wait Times: https://bwt.cbp.gov/
- API endpoint: https://bwt.cbp.gov/api/bwtnew
- License: US Public Domain

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-eventhub.json)
