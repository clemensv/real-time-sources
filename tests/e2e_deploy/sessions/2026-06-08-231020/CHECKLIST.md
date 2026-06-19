# E2E Validation Checklist — Session 2026-06-08-231020

> Generated from `CHECKLIST_TEMPLATE.md` at 2026-06-08 23:10:20 UTC
> Subscription: Vasters | Fabric Workspace: N/A

---

## Source: `{SOURCE_NAME}`

### Azure ACI + Event Hubs (Kafka) Validation

Template: `azure-template-with-eventhub.json` | Container: `Dockerfile` or `Dockerfile.kafka`

- [ ] Resource group `e2e-{SOURCE_NAME}-eh-{TS}` created
- [ ] Event Hubs namespace deployed (Standard, 1 TU)
- [ ] Event Hub entity created
- [ ] Connection string obtained
- [ ] ACI container deployed and reached Running state
- [ ] Messages received on Event Hub (count: ___)
- [ ] CloudEvents envelope validated (`ce_type`, `ce_source`, `ce_subject`)
- [ ] Kafka key matches xreg subject template
- [ ] Payload validates against xreg JsonStructure schema
- [ ] Resource group deleted

**Result**: {PASS | FAIL | SKIP | N/A}
**Notes**: ___

### Azure ACI + Service Bus (AMQP) Validation

Template: `azure-template-with-servicebus.json` | Container: `Dockerfile.amqp`

- [ ] Resource group `e2e-{SOURCE_NAME}-sb-{TS}` created
- [ ] Service Bus namespace deployed (Standard)
- [ ] Topic/queue created
- [ ] ACI container deployed and reached Running state
- [ ] Messages received on Service Bus (count: ___)
- [ ] AMQP message properties validated (CloudEvents content-type, `cloudEvents:` prefixed attributes)
- [ ] Payload validates against xreg JsonStructure schema
- [ ] Resource group deleted

**Result**: {PASS | FAIL | SKIP | N/A}
**Notes**: ___

### Azure ACI + Event Grid MQTT Validation

Template: `azure-template-with-eventgrid-mqtt.json` | Container: `Dockerfile.mqtt`

- [ ] Resource group `e2e-{SOURCE_NAME}-eg-{TS}` created
- [ ] Event Grid namespace deployed with MQTT broker enabled
- [ ] Client/topic-space/permission bindings created
- [ ] ACI container deployed and reached Running state
- [ ] Messages received via MQTT subscription (count: ___)
- [ ] MQTT user properties validated (`ce-type`, `ce-source`, `ce-subject`)
- [ ] Payload validates against xreg JsonStructure schema
- [ ] Resource group deleted

**Result**: {PASS | FAIL | SKIP | N/A}
**Notes**: ___

### Azure ACI + BYO MQTT Broker Validation

Template: `azure-template-mqtt.json` | Container: `Dockerfile.mqtt`

- [ ] SKIPPED — requires pre-existing MQTT broker; not automated in E2E

**Result**: SKIP
**Notes**: Manual validation only; requires external MQTT broker.

### Fabric Notebook Validation

- [ ] Notebook deployed via `deploy-feeder-notebook.ps1 -BuildWheelsLocally`
- [ ] Notebook run triggered (job instance ID: ___)
- [ ] Notebook run completed successfully (status: ___)
- [ ] KQL `_cloudevents_dispatch` table has rows (count: ___)
- [ ] At least one typed table has rows (table: ___, count: ___)
- [ ] Data freshness within expected cadence (minutes ago: ___)
- [ ] Map item verified (if applicable): {YES | N/A}
- [ ] Dashboard item verified (if applicable): {YES | N/A}
- [ ] Fabric items cleaned up (notebook deleted)

**Result**: {PASS | FAIL | SKIP | N/A}
**Notes**: ___

### Issues Filed

| Issue # | Title | Action |
|---------|-------|--------|
| ___ | ___ | Created / Amended |

---

<!-- Repeat the "Source" section above for each source in the run -->

## Summary

| Metric | Count |
|--------|-------|
| Sources tested | ___ |
| ACI+EH passes | ___ |
| ACI+SB passes | ___ |
| ACI+EG passes | ___ |
| Fabric passes | ___ |
| Failures | ___ |
| Skipped | ___ |
| Issues filed | ___ |
| Issues amended | ___ |
| Total runtime | ___ |

