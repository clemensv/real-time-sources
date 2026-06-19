# E2E Validation Checklist — Session 2026-06-10-205957

> Subscription: Vasters (041abda7-3870-4275-ae24-6bf4c5300523) | Fabric Workspace: ContosoRealTimeTest (ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb)

## Summary

| Source | Azure EH | Azure SB | Azure EG MQTT | Fabric | Issues |
|--------|----------|----------|---------------|--------|--------|
| nextbus | ⚠️ WARN | ⚠️ WARN | ⚠️ WARN | ✅ PASS | — |
| nws-alerts | ✅ PASS | ⚠️ WARN | ⚠️ WARN | ✅ PASS | — |
| tfl-road-traffic | — | — | ⚠️ WARN | — | — |
| tokyo-docomo-bikeshare | — | — | ⚠️ WARN | — | — |
| wallonia-issep | ✅ PASS | ✅ PASS | ⚠️ WARN | ❌ FAIL | #1152 |
| waterinfo-vmm | ✅ PASS | ✅ PASS | ⚠️ WARN | ❌ FAIL | #1150 |

## Source: `nextbus`

### Azure Event Hubs
- Status: ⚠️ WARN
- Details: no-data-upstream: stack running, feeder connected, upstream returned no events within timeout
- Messages: 0
- Error: no-data: no Event Hub messages received
- Cleanup: resource group delete requested (e2e-nextbus-eh-20260613001224)

### Azure Service Bus
- Status: ⚠️ WARN
- Details: no-data-upstream: stack running, feeder connected, upstream returned no events within timeout
- Messages: 0
- Error: no-data: no Service Bus messages received
- Cleanup: resource group delete requested (e2e-nextbus-sb-20260613001339)

### Azure Event Grid MQTT
- Status: ⚠️ WARN
- Details: subscriber connected (cert OK); feeder publishing (Connections=0.4); 0 msgs in subscribe window
- Messages: 0
- Cleanup: resource group delete requested (e2e-nextbus-eg-20260613001430)

### Fabric Notebook
- Status: ✅ PASS
- Details: dispatch and typed tables populated
- Dispatch rows: 227
- Typed tables: nextbus.Message=0, nextbus.RouteConfig=221, nextbus.Schedule=6, nextbus.VehiclePosition=0
- Job status: Completed
- Cleanup: complete

## Source: `nws-alerts`

### Azure Event Hubs
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 1
- Cleanup: resource group delete requested (e2e-nws-alerts-eh-20260612130634)

### Azure Service Bus
- Status: ⚠️ WARN
- Details: no-data-upstream: stack running, feeder connected, upstream returned no events within timeout
- Messages: 0
- Error: no-data: no Service Bus messages received
- Cleanup: resource group delete requested (e2e-nws-alerts-sb-20260612130805)

### Azure Event Grid MQTT
- Status: ⚠️ WARN
- Details: no-data-upstream: stack running, feeder connected, upstream returned no events within timeout
- Messages: 0
- Error: no-data: subscriber connected but 0 messages and Mqtt.Connections=0
- Cleanup: resource group delete requested (e2e-nws-alerts-eg-20260613055918)

### Fabric Notebook
- Status: ✅ PASS
- Details: dispatch and typed tables populated
- Dispatch rows: 286
- Typed tables: WeatherAlert=286
- Job status: Completed
- Cleanup: complete

## Source: `tfl-road-traffic`

### Azure Event Grid MQTT
- Status: ⚠️ WARN
- Details: subscriber connected (cert OK); feeder publishing (Connections=0.6); 0 msgs in subscribe window
- Messages: 0
- Cleanup: resource group delete requested (e2e-tfl-road-traffic-eg-20260617160534)

## Source: `tokyo-docomo-bikeshare`

### Azure Event Grid MQTT
- Status: ⚠️ WARN
- Details: subscriber connected (cert OK); feeder publishing (Connections=0); 0 msgs in subscribe window
- Messages: 0
- Cleanup: resource group delete requested (e2e-tokyo-docomo-bikeshare-eg-20260617132052)

## Source: `wallonia-issep`

### Azure Event Hubs
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 1
- Cleanup: resource group delete requested (e2e-wallonia-issep-eh-20260612172737)

### Azure Service Bus
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 8
- Cleanup: resource group delete requested (e2e-wallonia-issep-sb-20260612173002)

### Azure Event Grid MQTT
- Status: ⚠️ WARN
- Details: subscriber connected (cert OK); feeder publishing (Connections=0.6); 0 msgs in subscribe window
- Messages: 0
- Cleanup: resource group delete requested (e2e-wallonia-issep-eg-20260613023727)

### Fabric Notebook
- Status: ❌ FAIL
- Dispatch rows: 0
- Typed tables: 
- Error: Response status code does not indicate success: 404 (Not Found).
- Cleanup: complete

## Source: `waterinfo-vmm`

### Azure Event Hubs
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 1
- Cleanup: resource group delete requested (e2e-waterinfo-vmm-eh-20260612173519)

### Azure Service Bus
- Status: ✅ PASS
- Details: messages received and validator passed
- Messages: 10
- Cleanup: resource group delete requested (e2e-waterinfo-vmm-sb-20260612173855)

### Azure Event Grid MQTT
- Status: ⚠️ WARN
- Details: subscriber connected (cert OK); feeder publishing (Connections=0); 0 msgs in subscribe window
- Messages: 0
- Cleanup: resource group delete requested (e2e-waterinfo-vmm-eg-20260613024426)

### Fabric Notebook
- Status: ❌ FAIL
- Dispatch rows: 0
- Typed tables: 
- Job status: Timeout
- Error: Timed out after 1200s
- Cleanup: complete
