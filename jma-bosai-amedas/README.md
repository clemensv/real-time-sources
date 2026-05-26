# JMA Bosai AMeDAS Bridge

This source bridges the Japan Meteorological Agency (JMA / 気象庁) Bosai AMeDAS public data feed into Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams as CloudEvents.

AMeDAS (Automated Meteorological Data Acquisition System) automatically observes regional weather conditions across Japan. JMA documents the network as monitoring precipitation, wind direction and speed, temperature, humidity, sunshine duration, and snow depth for disaster prevention and mitigation.

## Upstream data channels reviewed

| Family | Transport | Endpoint | Identity | Cadence | Decision |
|---|---|---|---|---|---|
| Latest snapshot time | HTTPS text | `https://www.jma.go.jp/bosai/amedas/data/latest_time.txt` | snapshot timestamp | 10 minutes | Keep as poll cursor/dedupe state. |
| Observation map | HTTPS JSON | `https://www.jma.go.jp/bosai/amedas/data/map/{YYYYMMDDHHMM}00.json` | five-digit station code | 10 minutes | Keep as `JP.JMA.Amedas.Observation`. |
| Per-station observation detail | HTTPS JSON | `https://www.jma.go.jp/bosai/amedas/data/point/{station_code}/{YYYYMMDD_HH}.json` | five-digit station code | 10 minutes | Keep as opt-in enrichment for configured station codes because fetching all ~1300 station files every cycle would be high request volume. |
| Station metadata | HTTPS JSON | `https://www.jma.go.jp/bosai/amedas/const/amedastable.json` | five-digit station code | slow-changing | Keep as `JP.JMA.Amedas.Station`, emitted at startup and weekly. |

## Event model

Single message group and Kafka endpoint: `JP.JMA.Amedas` / `JP.JMA.Amedas.Kafka`.

Both event types use the identical CloudEvents subject and Kafka key template:

```text
jp.jma.amedas/{station_code}
```

- `Station`: reference data from `amedastable.json`; latitude and longitude are converted from `[degrees, minutes]` to decimal degrees.
- `Observation`: ten-minute station telemetry from the map snapshot, including optional measurement values and companion QC flags. When `POINT_STATION_CODES` is set, selected stations are enriched from the per-station point endpoint with gust, gust direction/time, maximum temperature/time, and minimum temperature/time fields.

See [EVENTS.md](EVENTS.md) for the CloudEvents and schema contract.

## Running

```powershell
pip install -e ./jma_bosai_amedas_producer/jma_bosai_amedas_producer_data
pip install -e ./jma_bosai_amedas_producer/jma_bosai_amedas_producer_kafka_producer
pip install -e .
python -m jma_bosai_amedas feed --connection-string "BootstrapServer=localhost:9092;EntityPath=jma-bosai-amedas" --no-kafka-enable-tls
```

Configuration is available through CLI flags and environment variables. `CONNECTION_STRING` is required for container use unless explicit Kafka settings are supplied. `KAFKA_TOPIC` defaults to `jma-bosai-amedas`, `POLLING_INTERVAL` defaults to `600`, `STATION_METADATA_REFRESH_HOURS` defaults to `168`, and `STATE_FILE` defaults to `./state/jma-bosai-amedas.json`. `POINT_STATION_CODES` is empty by default; set it to comma-separated station codes or `all` to fetch per-station detail files, with `POINT_REQUEST_DELAY` defaulting to `0.25` seconds between detail requests.

- Fabric notebook hosting is available through [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1) for scheduled single-cycle polling in Microsoft Fabric.


## MQTT and AMQP companion transports

This source now ships separate Kafka, MQTT, and AMQP containers. MQTT publishes binary-mode CloudEvents to the UNS topic tree below; AMQP publishes the same CloudEvents to the configured AMQP address with subject and routing axes in message/application properties.

Topic templates:
- `weather/jp/jma/jma-bosai-amedas/{prefecture}/{station_code}/info`
- `weather/jp/jma/jma-bosai-amedas/{prefecture}/{station_code}/observation`

- MQTT image: `ghcr.io/clemensv/real-time-sources-jma-bosai-amedas-mqtt:latest` (`Dockerfile.mqtt`)
- AMQP image: `ghcr.io/clemensv/real-time-sources-jma-bosai-amedas-amqp:latest` (`Dockerfile.amqp`)
- Azure templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`.
