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

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variant for Entur Norway SIRI real-time feeds. Non-retained QoS-1 streams route Estimated Timetable, Vehicle Monitoring, and Situation Exchange payloads by raw SIRI identifiers under transit/no/entur/entur-norway/... Missing routing fields are emitted as the literal unknown by the bridge.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/entur-norway.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `transit/no/entur/entur-norway/et/{operator_ref}/{line_ref}/{service_journey_id}/estimated-vehicle-journey` | `no.entur.EstimatedVehicleJourney` | QoS 1, retain=false |
| `transit/no/entur/entur-norway/vm/{operator_ref}/{line_ref}/{service_journey_id}/monitored-vehicle-journey` | `no.entur.MonitoredVehicleJourney` | QoS 1, retain=false |
| `transit/no/entur/entur-norway/sx/{severity}/{situation_number}/situation` | `no.entur.PtSituationElement` | QoS 1, retain=false |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion

This source also ships an AMQP 1.0 companion feeder (`Dockerfile.amqp`) alongside the Kafka and MQTT variants. It publishes the same CloudEvents to a single AMQP address named after the source, with CloudEvent `subject` and AMQP application properties mirroring the Kafka key/MQTT topic axes for broker-side filtering. Use `azure-template-with-servicebus.json` to deploy the AMQP feeder to Azure Service Bus with Entra ID/CBS authentication, or set `AMQP_BROKER_URL` for a generic AMQP 1.0 broker.
