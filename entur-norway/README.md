# Entur Norway SIRI Bridge

Real-time transit data bridge for [Entur Norway](https://developer.entur.org/) SIRI feeds to Apache Kafka.

Subscribes to Entur's SIRI 2.0 REST API feeds:
- **ET** (Estimated Timetable) — service journey reference data and stop-level predictions
- **VM** (Vehicle Monitoring) — live vehicle positions
- **SX** (Situation Exchange) — service disruptions and alerts

## Feeds

| CloudEvents type | Description |
|---|---|
| `no.entur.DatedServiceJourney` | Reference data: scheduled service journeys |
| `no.entur.EstimatedVehicleJourney` | Timetable predictions per service journey |
| `no.entur.MonitoredVehicleJourney` | Live vehicle positions |
| `no.entur.PtSituationElement` | Service disruptions and situation alerts |

## Usage

```bash
python -m entur_norway feed --connection-string "BootstrapServer=localhost:9092;EntityPath=entur-norway"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Kafka connection string | required |
| `POLLING_INTERVAL` | Polling interval in seconds | `30` |
| `MAX_SIZE` | Maximum records per SIRI request | `1000` |
| `KAFKA_ENABLE_TLS` | Set to `false` for plain Kafka | |

## Data Source

- API: <https://api.entur.io/realtime/v1/rest/>
- Docs: <https://developer.entur.org/pages-real-time-intro>
- License: NLOD (Norwegian Licence for Open Government Data)
