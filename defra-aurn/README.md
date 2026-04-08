# Defra AURN Bridge Usage Guide

## Overview

This bridge polls the UK Defra Automatic Urban and Rural Network (AURN) SOS
Timeseries API and republishes station metadata, timeseries metadata, and fresh
 hourly observations to Kafka as CloudEvents in structured JSON mode.

It is a poller. It fetches reference data first, then polls every known
timeseries. Fresh containers use a six-hour bootstrap lookback so they can emit
the latest available telemetry even when the upstream feed lags a few hours;
steady-state polling then returns to the most recent two-hour window and emits
only values it has not seen before.

## Data Source

- **Provider**: UK Air / Defra AURN
- **Base URL**: `https://uk-air.defra.gov.uk/sos-ukair/api/v1`
- **Transport**: REST (52°North SOS Timeseries API)
- **Authentication**: None
- **Update cadence**: Hourly
- **Data license**: Open Government Licence v3.0

## API Surface Reviewed

The upstream API families reviewed for this source are:

| Family | Endpoint | Keep? | Reason |
|---|---|---|---|
| Stations | `GET /stations` | Keep | Reference data for monitoring locations and labels |
| Phenomena | `GET /phenomena` | Drop as standalone family | Already carried in timeseries metadata as `phenomenon_id` and `phenomenon_label` |
| Categories | `GET /categories` | Drop as standalone family | Current API mirrors `phenomena`; modeled as fields on timeseries metadata |
| Timeseries list | `GET /timeseries` | Keep | Enumerates all station × pollutant combinations |
| Timeseries detail | `GET /timeseries/{id}?expanded=true` | Keep | Needed for pollutant and category metadata |
| Observation values | `GET /timeseries/{id}/getData` | Keep | Telemetry feed |

## Event Model

The bridge emits three CloudEvents types:

| CloudEvents `type` | Category | Key / Subject |
|---|---|---|
| `uk.gov.defra.aurn.Station` | Reference | `{station_id}` |
| `uk.gov.defra.aurn.Timeseries` | Reference | `{timeseries_id}` |
| `uk.gov.defra.aurn.Observation` | Telemetry | `{timeseries_id}` |

Station events describe the monitoring network. Timeseries events describe the
station-and-pollutant combinations that produce observations. Observation events
carry hourly pollutant values with ISO 8601 UTC timestamps.

## Measurements

The AURN network covers 300+ UK monitoring locations and publishes pollutant
timeseries including ozone, nitrogen dioxide, sulfur dioxide, PM2.5, PM10,
carbon monoxide, and heavy-metal related particulate measurements where
available.

## Installation

From this repository:

```powershell
pip install defra_aurn_producer\defra_aurn_producer_data
pip install defra_aurn_producer\defra_aurn_producer_kafka_producer
pip install -e .
```

## Running the bridge

### Event Hubs or Fabric Event Streams

```powershell
python -m defra_aurn feed --connection-string "Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=defra-aurn"
```

### Plain Kafka

```powershell
python -m defra_aurn feed --connection-string "BootstrapServer=localhost:9092;EntityPath=defra-aurn" --kafka-enable-tls false
```

You can also provide the Kafka settings with environment variables.

## Feed configuration

| Argument | Environment variable | Description |
|---|---|---|
| `--connection-string` | `CONNECTION_STRING` | Event Hubs or `BootstrapServer=...;EntityPath=...` connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Topic name, default `defra-aurn` |
| `--sasl-username` | `SASL_USERNAME` | SASL username |
| `--sasl-password` | `SASL_PASSWORD` | SASL password |
| `--polling-interval` | `POLLING_INTERVAL` | Polling interval in seconds, default `3600` |
| `--state-file` | `STATE_FILE` | De-duplication state file, default `~/.defra_aurn_state.json` |
| `--kafka-enable-tls` | `KAFKA_ENABLE_TLS` | Enable TLS, default `true` |

## Runtime behavior

1. Fetch all stations and emit `uk.gov.defra.aurn.Station`.
2. Fetch all timeseries, expand each one, and emit `uk.gov.defra.aurn.Timeseries`.
3. Poll every timeseries with a six-hour bootstrap lookback on first start, then
   use the last two hours of values on steady-state loops.
4. Emit only observations newer than the last stored timestamp per timeseries.
5. Refresh reference data periodically so downstream consumers do not have to
   fetch station context out of band.

## Coordinates

The upstream station GeoJSON uses `geometry.coordinates[0]` as latitude and
`geometry.coordinates[1]` as longitude. That is the reverse of normal GeoJSON
ordering, and the bridge preserves the actual upstream semantics rather than the
convention.
