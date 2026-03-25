# Waterinfo VMM (Belgium/Flanders) Water Level Bridge

This project bridges water level data from the Belgian
[Waterinfo.be](https://waterinfo.vlaanderen.be/) KIWIS API (VMM provider) to
Apache Kafka, emitting CloudEvents.

**Waterinfo.be** is managed by the Flanders Environment Agency (VMM) and
Flanders Hydraulics Research. It provides real-time water and weather data for
Flanders (Belgium), including water level, discharge, rainfall, and more.

## Data

- **Stations**: ~1,785 monitoring stations across Flanders and Belgium
- **Water Level (15-min)**: ~1,109 time series measuring water level (H) in meters (15-minute intervals)
- **Polling interval**: 15 minutes

The API uses the KISTERS KIWIS protocol with VMM as the data source.

## Usage

### List stations

```bash
python -m waterinfo_vmm list
```

### Get latest water level for a station

```bash
python -m waterinfo_vmm level L04_007
```

### Feed to Kafka

Using a connection string (Azure Event Hubs):

```bash
python -m waterinfo_vmm feed -c "Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..."
```

Using explicit Kafka configuration:

```bash
python -m waterinfo_vmm feed \
    --kafka-bootstrap-servers your-server:9093 \
    --kafka-topic waterinfo-vmm \
    --sasl-username '$ConnectionString' \
    --sasl-password 'your-connection-string'
```

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents message definitions.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker container deployment info.

## API Reference

- **Base URL**: `https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS`
- **Protocol**: KISTERS KIWIS QueryServices
- **Provider**: VMM (Flanders Environment Agency), datasource=1
- **Key endpoints**:
  - `getStationList` — list all monitoring stations
  - `getTimeseriesValueLayer` — latest values for a timeseries group
  - `getTimeseriesValues` — historical time series data
  - `getGroupList` — list timeseries groups
- **Documentation**: [KIWIS API docs](https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&request=getrequestinfo)
- **No authentication required** for limited downloads; token available for heavy use

## Daily Volume Estimate

- ~1,109 water level stations × 96 readings/day (15 min) = ~106,000 readings/day
- Each CloudEvent ≈ 500 bytes → ~53 MB/day
- Plus ~1,785 station reference events at startup
