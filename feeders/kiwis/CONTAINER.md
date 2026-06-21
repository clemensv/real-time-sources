# KiWIS container contract

[Overview](README.md) · [Events](EVENTS.md) · [xRegistry contract](xreg/kiwis.xreg.json)

The KiWIS images publish hydrological station reference data, timeseries metadata, and latest observation values from configurable KISTERS KiWIS REST endpoints as CloudEvents.

## Image contract

| Image tag | Transport | Dockerfile | State |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-kiwis:latest` | Kafka/Event Hubs/Fabric | `Dockerfile.kafka` | `KIWIS_STATE_FILE` optional |
| `ghcr.io/clemensv/real-time-sources-kiwis-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | `KIWIS_STATE_FILE` optional |
| `ghcr.io/clemensv/real-time-sources-kiwis-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | `KIWIS_STATE_FILE` optional |

## Common environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `KIWIS_ENDPOINTS` | CSV/JSON endpoint list or `@file`: `kiwis_id,base_url,datasource,station_filter,timeseries_filter,ts_ids,period,api_key`. | SEPA Scotland sample |
| `KIWIS_MOCK` | `true` emits one offline station, timeseries, and value for E2E. | `false` |
| `KIWIS_MAX_TIMESERIES` | Safety cap for discovered timeseries per endpoint. | `10` |
| `POLLING_INTERVAL` | Seconds between polling cycles. | `300` |
| `KIWIS_STATE_FILE` | JSON dedupe state path used by container and Azure templates. | none |
| `STATE_FILE` | Alternate state file environment variable used by Fabric notebook hosting. | none |
| `LOG_LEVEL` | Python logging level. | `INFO` |

## Kafka

```powershell
docker run --rm -e CONNECTION_STRING='BootstrapServer=broker:9092;EntityPath=kiwis' -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-kiwis:latest
```

Kafka also accepts `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, and `SASL_PASSWORD`.

## MQTT

```powershell
docker run --rm -e MQTT_BROKER_URL='broker:1883' -e MQTT_USERNAME=user -e MQTT_PASSWORD=secret ghcr.io/clemensv/real-time-sources-kiwis-mqtt:latest
```

MQTT variables: `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, plus the common KiWIS variables.

## AMQP 1.0

```powershell
docker run --rm -e AMQP_BROKER_URL='amqp://user:password@broker:5672/kiwis' ghcr.io/clemensv/real-time-sources-kiwis-amqp:latest
```

AMQP variables: `AMQP_BROKER_URL`, `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_TLS`, plus common KiWIS variables.

## Azure templates

This source ships generated templates for Kafka/Event Hubs, MQTT/Event Grid namespace, and AMQP/Service Bus. Use the portal buttons after the PR is merged; no live Azure/Fabric deployment was performed in this PR.
