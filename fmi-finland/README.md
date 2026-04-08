# FMI Finland Air Quality Bridge

This bridge polls the Finnish Meteorological Institute (FMI) open OGC WFS
service for hourly air quality observations and republishes them as structured
CloudEvents to Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

It emits two event families:

- `fi.fmi.opendata.airquality.Station` — station reference data
- `fi.fmi.opendata.airquality.Observation` — hourly aggregated measurements per
  station and timestamp

## Upstream Source

- **Provider**: Finnish Meteorological Institute (FMI)
- **API**: `https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0`
- **Transport**: OGC WFS 2.0 over HTTP GET
- **Authentication**: none
- **License**: CC BY 4.0

## Upstream Channel Review

The FMI air quality WFS surface reviewed for this bridge is:

| Family | Transport | Identity | Cadence | Decision |
|---|---|---|---|---|
| `urban::observations::airquality::hourly::simple` | WFS stored query | station `fmisid` + observation hour | hourly | Keep. Simplest record-per-parameter representation, easy to aggregate into observation events. |
| `urban::observations::airquality::hourly::multipointcoverage` | WFS stored query | station `fmisid` + observation hour | hourly | Drop. Same underlying measurements, denser XML representation. |
| `urban::observations::airquality::hourly::timevaluepair` | WFS stored query | station `fmisid` + observation hour | hourly | Drop. Same underlying measurements, alternate presentation only. |
| `fmi::ef::stations` | WFS stored query | station `fmisid` | slow-changing reference data | Keep. Required station metadata feed for reference events. |

The bridge models the requested pollutant and index parameters:
`AQINDEX_PT1H_avg`, `PM10_PT1H_avg`, `PM25_PT1H_avg`, `NO2_PT1H_avg`,
`O3_PT1H_avg`, `SO2_PT1H_avg`, and `CO_PT1H_avg`.

## Practical Note About Station Resolution

The simple observation feed does not reliably expose the station `fmisid` in
the `gml:id` field. In live responses, values such as `BsWfsElement.1.1.1`
appear instead. Therefore, the bridge resolves stations primarily through the
station registry and coordinate matching, and only uses numeric `gml:id`
segments as a fallback.

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

List known stations:

```powershell
python -m fmi_finland list
```

Run the feed with a plain Kafka broker:

```powershell
$env:KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
$env:KAFKA_TOPIC="fmi-finland-airquality"
python -m fmi_finland feed
```

Run the feed with an Event Hubs or Fabric connection string:

```powershell
$env:CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=fmi-finland-airquality"
python -m fmi_finland feed
```

## Configuration

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs or plain Kafka connection string | unset |
| `KAFKA_BOOTSTRAP_SERVERS` | Explicit Kafka bootstrap server list | unset |
| `KAFKA_TOPIC` | Kafka topic name | `fmi-finland-airquality` |
| `SASL_USERNAME` | Optional SASL username for Kafka | unset |
| `SASL_PASSWORD` | Optional SASL password for Kafka | unset |
| `POLLING_INTERVAL` | Polling interval in seconds | `3600` |
| `STATION_REFRESH_INTERVAL` | Reference data re-emission interval in seconds | `86400` |
| `STATE_FILE` | Deduplication state file | `~/.fmi_finland_state.json` |

## Testing

```powershell
python -m pytest tests\test_fmi_finland_unit.py -v --no-cov
python -m pytest tests\test_fmi_finland_integration.py -v --no-cov
```
