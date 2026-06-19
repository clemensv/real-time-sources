# E2E Validation Checklist — Session 2026-06-08-215528

> Generated from `CHECKLIST_TEMPLATE.md` at 2026-06-08 22:07 UTC+2
> Subscription: Vasters | Fabric Workspace: ContosoRealTimeTest

---

## Source: `australia-wildfires`

### Azure ACI + Event Hubs (Kafka) Validation

Template: `azure-template-with-eventhub.json` | Container: `Dockerfile` or `Dockerfile.kafka`

- [x] Resource group `e2e-australia-wildfires-eh-20260608220753` created
- [x] Event Hubs namespace deployed (Standard, 1 TU)
- [x] Event Hub entity created
- [x] Connection string obtained
- [x] ACI container deployed and reached Running state
- [x] Messages received on Event Hub (count: 18)
- [x] CloudEvents envelope validated (structured mode: content-type=application/cloudevents+json, type/source/subject in body)
- [x] Kafka key matches xreg subject template (e.g. NSW/662350)
- [x] Payload validates against xreg JsonStructure schema (all 13 required fields present)
- [x] Resource group deleted (async)

**Result**: PASS
**Notes**: Structured CloudEvents mode; 18 messages; key=subject; schema valid

### Azure ACI + Service Bus (AMQP) Validation

Template: `azure-template-with-servicebus.json` | Container: `Dockerfile.amqp`

- [x] Resource group `e2e-australia-wildfires-sb-20260608222131` created
- [x] Service Bus namespace deployed (Standard)
- [x] Queue `australia-wildfires` created
- [x] ACI container deployed and reached Running state
- [x] Messages received on Service Bus (count: 30, from 117 queued)
- [x] AMQP message properties validated (`cloudEvents:type`, `cloudEvents:source`, `cloudEvents:subject` present)
- [x] Payload validates against xreg JsonStructure schema (all 13 required fields present)
- [x] Resource group deleted (async)

**Result**: PASS
**Notes**: Required assigning `Azure Service Bus Data Receiver` RBAC role to test identity (ARM template does not do this). Role scoped to SB namespace. 20 messages schema-validated with 0 errors.

**Issue discovered**: ARM template does not grant the deploying user Listen rights. `validate_servicebus.ps1` must assign this role itself. See fix needed in test tooling.

### Azure ACI + Event Grid MQTT Validation

Template: `azure-template-with-eventgrid-mqtt.json` | Container: `Dockerfile.mqtt`

- [x] Resource group `e2e-australia-wildfires-eg-20260608222903` created
- [x] Event Grid namespace deployed with MQTT broker enabled
- [x] Topic space `wildfire/au/#` created; publisher RBAC role assigned to MSI
- [x] ACI container deployed and reached Running state (logged "Published 43 incidents")
- [x] Resource group deleted (async)
- [ ] ~~Messages received via MQTT subscription~~ — **FAILED**
- [ ] ~~MQTT user properties validated~~ — **FAILED**

**Result**: FAIL — Issue #840
**Notes**: Feeder connects without credentials (ARM template sets `MQTT_AUTH_MODE=entra` but `app.py` never reads it). EG MQTT namespace shows 0 connections and 0 published messages in metrics. Feeder logs "Published" because paho queues messages silently when disconnected. External subscription also blocked: RBAC roles (`EventGrid TopicSpaces Subscriber`) do not suffice for MQTT broker auth from external clients without registered client certificates. See [#840](https://github.com/clemensv/real-time-sources/issues/840).

### Azure ACI + BYO MQTT Broker Validation

Template: `azure-template-mqtt.json` | Container: `Dockerfile.mqtt`

- [x] SKIPPED — requires pre-existing MQTT broker; not automated in E2E

**Result**: SKIP
**Notes**: Manual validation only; requires external MQTT broker.

### Fabric Notebook Validation

- [x] Notebook deployed via `deploy-feeder-notebook.ps1 -BuildWheelsLocally`
- [x] Notebook run triggered (job instance ID: obtained via Fabric REST API)
- [x] Notebook run completed successfully (status: Completed)
- [x] KQL `_cloudevents_dispatch` table has rows (count: 19 new rows in run window)
- [x] At least one typed table has rows (table: `FireIncident`, count: 19)
- [x] Data freshness within expected cadence (ingested within ~21s of run)
- [x] Map item verified (if applicable): N/A
- [x] Dashboard item verified (if applicable): N/A
- [x] Fabric items cleaned up (notebook deleted)

**Result**: PASS
**Notes**: Notebook run completed in ~21s. 19 new fire incident rows ingested. All 13 schema fields present.

### Issues Filed

| Issue # | Title | Action |
|---------|-------|--------|
| [#840](https://github.com/clemensv/real-time-sources/issues/840) | australia-wildfires MQTT feeder: Entra JWT auth not implemented; feeder silently fails to connect to Event Grid MQTT namespace | Created |
| [#839](https://github.com/clemensv/real-time-sources/issues/839) | (pre-existing) Minor issue; not a blocker | Pre-existing |

---

## Summary

| Metric | Count |
|--------|-------|
| Sources tested | 1 (australia-wildfires) |
| ACI+EH passes | 1 |
| ACI+SB passes | 1 |
| ACI+EG passes | 0 |
| Fabric passes | 1 |
| Failures | 1 (ACI+EG MQTT) |
| Skipped | 1 (BYO MQTT) |
| Issues filed | 1 (#840) |
| Issues amended | 0 |
| Total runtime | ~90 min |

### Tooling issues to fix before next run

1. `validate_servicebus.ps1` must assign `Azure Service Bus Data Receiver` role to test identity automatically (use `az role assignment create` against the SB namespace before receiving)
2. `validate_mqtt.ps1` topic pattern is wrong (`sources/{source}/#` → should be derived from xreg topic space template)
3. `validate_mqtt.ps1` cannot connect to EG MQTT from local machine using RBAC role alone — needs certificate-based client registration or alternative approach
4. EG MQTT ARM template needs to either (a) document that external MQTT validation requires certificate auth, or (b) create a test subscriber client and permission binding as part of template deployment


