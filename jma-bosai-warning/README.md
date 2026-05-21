# JMA Bosai Weather Warnings + Tsunami Alerts

This source polls public Japan Meteorological Agency (JMA) Bosai endpoints and emits CloudEvents to Kafka.

## Upstream channels reviewed

| Family | Endpoint | Identity | Cadence | Decision |
|---|---|---|---|---|
| Warning office catalog | `https://www.jma.go.jp/bosai/common/const/area.json` (`offices`) | `office_code` | Slow-changing reference | Keep as `Office` reference events. |
| Weather warnings | `https://www.jma.go.jp/bosai/warning/data/warning/{office}.json` | `office_code` + inner `area_code` | As issued; polled every 60s by default | Keep as `WeatherWarning`. |
| Active tsunami list | `https://www.jma.go.jp/bosai/tsunami/data/list.json` | `event_id` + `serial` | As issued; polled every 30s by default | Keep as `TsunamiAlert`. |
| Tsunami detail files | `https://www.jma.go.jp/bosai/tsunami/data/{json}` | `event_id` + `serial` | Per active alert | Keep as enrichment for affected coastal regions. |

Weather warnings and tsunami alerts use different stable identity shapes, so the xRegistry contract defines separate message groups and Kafka endpoints.

## Events

See [EVENTS.md](EVENTS.md) for CloudEvents type, subject, key, and payload details.

## Runtime

```powershell
python -m jma_bosai_warning feed --connection-string "BootstrapServer=localhost:9092;EntityPath=jma-bosai-warning" --once
```

Configuration is via environment variables or CLI flags. Required Kafka configuration is either `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS`.
