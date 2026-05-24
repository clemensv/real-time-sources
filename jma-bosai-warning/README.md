# JMA Bosai Weather Warnings + Tsunami Alerts

This source polls public Japan Meteorological Agency (JMA) Bosai endpoints and emits CloudEvents to Kafka. It also includes an MQTT/UNS feeder for weather warning and office-reference records.

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

- Fabric notebook hosting is available via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1).

## Runtime

Kafka:

```powershell
python -m jma_bosai_warning feed --connection-string "BootstrapServer=localhost:9092;EntityPath=jma-bosai-warning" --once
```

MQTT/UNS:

```powershell
python -m jma_bosai_warning_mqtt feed --broker-url mqtt://localhost:1883 --once
```

MQTT topics:

- `alerts/jp/jma/jma-bosai-warning/{prefecture}/REFERENCE/{office_code}/{area_code}/office` (retained office reference records)
- `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/warning` (non-retained weather warning records)

Configuration is via environment variables or CLI flags. Required Kafka configuration is either `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS`.
