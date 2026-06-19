# E2E Validation Checklist — Session 2026-06-10-213244

> Generated from CHECKLIST_TEMPLATE.md at 2026-06-10T21:32:44.334+02:00
> Subscription: Vasters | Fabric Workspace: N/A

---

## Source: entsoe

### Azure ACI + Event Hubs (Kafka) Validation

Template: azure-template-with-eventhub.json | Container: Dockerfile

- Result: PASS
- Messages received: 1
- Notes: validated structured CloudEvents

### Azure ACI + Service Bus (AMQP) Validation

Template: azure-template-with-servicebus.json | Container: Dockerfile.amqp

- Result: FAIL
- Messages received: 0
- Notes: no-data: no Service Bus messages received

### Azure ACI + Event Grid MQTT Validation

Template: azure-template-with-eventgrid-mqtt.json | Container: Dockerfile.mqtt

- Result: BLOCKED
- Messages observed: 25149
- Notes: Mqtt.Connections > 0; feeder publishing observed, external subscribe blocked

### Issues Filed

| Issue # | Title | Action |
|---------|-------|--------|
| 920 | [E2E] entsoe - azure-sb: no-data | amended |
