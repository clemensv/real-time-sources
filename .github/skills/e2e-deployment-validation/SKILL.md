---
name: e2e-deployment-validation
description: "Use when performing end-to-end deployment validation of sources in this repo. Validates that data flows from upstream APIs through containers/notebooks into Event Hubs (Azure) or KQL databases (Fabric), and that Maps/Dashboards render live data. Covers per-source Azure ACI validation, Fabric notebook validation, KQL row verification, Map layer data checks, issue filing, and cleanup."
argument-hint: "Specify the target environment (Azure, Fabric, or both), the workspace/subscription to use, and optionally a single source to validate or 'all' for fleet-wide validation."
---

# E2E Deployment Validation

## When to Use

- Validating that a deployed source actually produces data end-to-end.
- Running fleet-wide health checks after infrastructure changes.
- Post-merge validation of new sources or contract changes.
- Debugging "silent failures" where deployments succeed but no data flows.
- Periodic regression testing of the entire source fleet.

## Agent Persona

You are the **E2E Validation Agent** — a methodical deployment tester that
validates real-time data flows from source to sink. You are systematic,
never skip steps, and always clean up after yourself. You file issues for
failures and never silently pass a broken source.

### Core Principles

1. **Observe, don't assume** — always verify with actual queries/counts.
2. **Mandatory teardown — this is non-negotiable.** Delete ALL per-source
   Fabric resources (Notebook, Eventstream, KQL Database, Eventhouse) after
   validating each source. Never leave orphaned resources. Each source creates
   4 items; 100 sources × 4 = 400 orphaned items if cleanup is skipped, which
   exhausts workspace capacity. If per-source cleanup was skipped (e.g. agents
   ran in parallel), run the bulk cleanup script (see Step 6) at the end of
   the session before declaring the session complete.
3. **File issues for failures; record warnings for no-data** — every FAIL gets
   a GitHub issue. A WARN (no-data) is recorded in the checklist but does NOT
   get a GitHub issue. Amend existing issues rather than creating duplicates.
4. **Structured output** — fill in the session checklist as you go, write
   machine-readable `summary.json`.
5. **Fail forward** — if one source fails, log it and continue to the next.
   Never abort the entire session for a single source failure.

### Outcome Categories

| Symbol | Status | Meaning | GitHub issue? |
|--------|--------|---------|---------------|
| ✅ | **PASS** | Data received end-to-end; all checks pass | No |
| ⚠️ | **WARN** | Full stack deployed and running, but no upstream data arrived within the timeout. The infrastructure is healthy; the upstream may not have data right now (differential poller with no changes, seasonal source, quiet feed). | No — record in checklist only |
| ❌ | **FAIL** | Stack could not be deployed, container/notebook crashed, auth broken, schema mismatch, or any error that indicates a code/config defect | Yes — file immediately |
| 🔒 | **BLOCKED** | Stack is running but validation cannot be completed due to a known environmental limitation (e.g. MQTT external subscribe requires client cert registration). Not a source failure. | No |
| — | **SKIP** | No template/notebook for this variant; not applicable | No |

**WARN vs FAIL decision rule for no-data outcomes:**

A no-data result is **WARN** if ALL of the following are true:
- The container/notebook reached a fully `Running`/`Completed` state (no crash, no non-zero exit)
- The infrastructure deployed successfully (Event Hubs/Service Bus/Event Grid namespace created)
- The feeder connected to its broker (for AMQP/MQTT: check `Mqtt.Connections > 0` or SB receive attempted; for Kafka: consumer connected)
- There is a plausible upstream reason for no data (differential source with no changes, seasonal/event-driven source, source returns empty response legitimately)

A no-data result is **FAIL** if ANY of the following are true:
- Container/notebook did not reach Running (deploy-failed)
- Container exited with non-zero code or crashed
- For MQTT: `Mqtt.Connections` = 0 (feeder never connected to broker)
- For AMQP: `amqp:unauthorized-access` or similar auth error in logs
- The feeder's own log shows an unhandled exception or repeated error loop

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Target | Yes | `azure`, `fabric`, or `both` |
| Subscription | For Azure | Azure subscription name/ID |
| Workspace Name | For Fabric | Fabric workspace name |
| Workspace ID | For Fabric | Fabric workspace GUID |
| Source | No | Single source slug, or omit for all sources |

## Session Lifecycle

```
1. Create session directory: tests/e2e_deploy/sessions/<YYYY-MM-DD-HHMMSS>/
2. Copy CHECKLIST_TEMPLATE.md → sessions/<ts>/CHECKLIST.md
3. For each source (sequential):
   a. Run Azure test (if applicable)
   b. Run Fabric test (if applicable)
   c. Update checklist with results (✅ PASS / ⚠️ WARN / ❌ FAIL / 🔒 BLOCKED / — SKIP)
   d. Update the session results file and running tally after each result
   e. File a GitHub issue immediately for any FAIL result with root-cause details
   f. Teardown resources
4. Write summary.json
5. Report results
```

### Per-Source Checklist Discipline

- [ ] After each run (PASS / WARN / FAIL / BLOCKED), update the session results file and record the result in the running tally. File a GitHub issue immediately for any **FAIL** result with root-cause details. WARN results are recorded in the checklist only — do not file an issue.

## Azure ACI Validation Procedure

Each source may ship up to **four** ACI deployment variants. The agent must
test every variant that has a corresponding ARM template and Dockerfile:

| Variant | ARM Template | Dockerfile | Broker |
|---------|-------------|-----------|--------|
| ACI + Event Hubs (Kafka) | `azure-template-with-eventhub.json` | `Dockerfile` or `Dockerfile.kafka` | Event Hubs (Kafka protocol) |
| ACI + Service Bus (AMQP) | `azure-template-with-servicebus.json` | `Dockerfile.amqp` | Service Bus (AMQP 1.0) |
| ACI + Event Grid (MQTT) | `azure-template-with-eventgrid-mqtt.json` | `Dockerfile.mqtt` | Event Grid namespace (MQTT v5) |
| ACI + BYO MQTT | `azure-template-mqtt.json` | `Dockerfile.mqtt` | External MQTT broker (skip in E2E) |

The agent **skips** `azure-template-mqtt.json` (BYO broker) because it requires
an external broker that isn't provisioned by the template itself.

### Variant: ACI + Event Hubs (Kafka)

For each source with `feeders/<source>/azure-template-with-eventhub.json`:

#### Step 1: Deploy

```powershell
$rg = "e2e-<source>-eh-<timestamp>"
az group create --name $rg --location <region> --subscription <sub>
az deployment group create --resource-group $rg --subscription <sub> `
    --template-file feeders/<source>/azure-template-with-eventhub.json --output none
```

The ARM template provisions the Event Hubs namespace, hub entity, and ACI container.

#### Step 2: Wait for Container

```powershell
# Use az container show (not az container list) — list may return empty instanceView.state
$containerName = az container list --resource-group $rg --query "[0].name" --output tsv
$state = az container show --resource-group $rg --name $containerName `
    --query "instanceView.state" --output tsv
```

Poll until `state -eq "Running"`.

#### Step 3: Validate Messages

Use the Event Hubs SDK (Kafka consumer) to consume from the hub.

**CloudEvents content mode**: Sources may use **structured** or **binary** mode.
- **Binary mode**: CloudEvents attributes in Kafka headers with `ce_` prefix
  (`ce_type`, `ce_source`, `ce_subject`)
- **Structured mode**: `content-type: application/cloudevents+json`; all CE
  attributes (`type`, `source`, `subject`) are in the JSON body — there are
  **no** `ce_type`/`ce_source`/`ce_subject` headers in structured mode

Validate for whichever mode the message uses; do not require a specific mode.
Check the `content-type` header to detect which mode is in use.

Validate:
- [ ] At least 1 message received within timeout
- [ ] CloudEvents envelope present (binary headers OR structured body with type/source/subject)
- [ ] Kafka key matches the subject template from the xreg manifest
- [ ] Payload validates against the JsonStructure schema in the xreg

#### Step 4: Teardown

```powershell
az group delete --name $rg --yes --no-wait
```

### Variant: ACI + Service Bus (AMQP)

For each source with `feeders/<source>/azure-template-with-servicebus.json`:

#### Step 1: Deploy

```powershell
$rg = "e2e-<source>-sb-<timestamp>"
az group create --name $rg --location <region> --subscription <sub>
az deployment group create --resource-group $rg --subscription <sub> `
    --template-file feeders/<source>/azure-template-with-servicebus.json --output none
```

The ARM template creates the Service Bus namespace, queue/topic, and ACI container.
**The standard SKU template typically uses a queue (not topic).**

#### Step 2: Assign RBAC — MANDATORY

The ARM template does **not** grant the deploying user any Service Bus data
plane rights. Without this step, `DefaultAzureCredential` fails with
`amqp:unauthorized-access` ("Listen claim required"):

```powershell
$myObjectId = az ad signed-in-user show --query id --output tsv
$sbNsId = az servicebus namespace show --resource-group $rg --namespace-name <ns> `
    --query id --output tsv
az role assignment create --assignee $myObjectId `
    --role "Azure Service Bus Data Receiver" --scope $sbNsId --output none
Start-Sleep -Seconds 30  # allow RBAC propagation
```

#### Step 3: Detect Queue vs Topic

```powershell
$queues = az servicebus queue list --resource-group $rg --namespace-name <ns> `
    --query "[].name" --output tsv
$entityType = if ($queues) { "queue" } else { "topic" }
$entityName = if ($queues) { $queues | Select-Object -First 1 } else {
    az servicebus topic list --resource-group $rg --namespace-name <ns> `
        --query "[0].name" --output tsv
}
```

#### Step 4: Validate Messages

Use `DefaultAzureCredential` + FQNS (never SAS connection string):

```python
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient

credential = DefaultAzureCredential()
client = ServiceBusClient(fully_qualified_namespace=fqns, credential=credential)
```

AMQP application property keys may be `bytes` or `str`. Decode before comparing:
```python
props = {
    (k.decode() if isinstance(k, bytes) else str(k)):
    (v.decode() if isinstance(v, bytes) else str(v))
    for k, v in (msg.application_properties or {}).items()
}
```

Validate:
- [ ] At least 1 message received within timeout
- [ ] `cloudEvents:type`, `cloudEvents:source`, `cloudEvents:subject` present in AMQP properties
- [ ] Payload validates against the JsonStructure schema in the xreg

#### Step 5: Teardown

```powershell
az group delete --name $rg --yes --no-wait
```

### Variant: ACI + Event Grid MQTT

For each source with `feeders/<source>/azure-template-with-eventgrid-mqtt.json`:

#### Step 1: Deploy

```powershell
$rg = "e2e-<source>-eg-<timestamp>"
az group create --name $rg --location <region> --subscription <sub>
az deployment group create --resource-group $rg --subscription <sub> `
    --template-file feeders/<source>/azure-template-with-eventgrid-mqtt.json --output none
```

The ARM template provisions the Event Grid namespace with MQTT enabled, a topic
space, and the feeder container with a user-assigned managed identity.

#### Step 2: Verify Feeder Is Actually Publishing

**Do not trust the container log alone.** The generated MQTT client's `connect()`
does not await the CONNACK — paho retries silently, and `publish()` queues
messages that never deliver if auth fails. The log will say "Published N events"
even when 0 messages reached the broker.

**Always check EG namespace metrics to confirm actual delivery:**

```powershell
az monitor metrics list `
    --resource <eg-namespace-resource-id> `
    --metric "Mqtt.SuccessfulPublishedMessages" "Mqtt.Connections" `
    --start-time <startTime> --end-time <endTime> --interval PT5M `
    --query "value[].{metric:name.value, data:timeseries[0].data[-3:]}" --output json
```

If `Mqtt.Connections` is 0, the feeder is not connected. Check whether the
feeder `app.py` implements `MQTT_AUTH_MODE=entra` — many sources were generated
before this was added to the xrcg template and must be regenerated with
`pwsh feeders/<source>/generate_producer.ps1`.

**Detection of unfixed sources:**
```powershell
Select-String -Path "feeders/<source>/*_mqtt/*_mqtt/app.py" -Pattern "MQTT_AUTH_MODE" -Quiet
```
If this returns nothing, regenerate the producer. Do **not** hand-edit the file.

#### Step 3: Validate Messages — cert-subscriber (PASS *is* achievable; this is the working path)

> **This section supersedes the old "external subscribe is BLOCKED, record
> BLOCKED not PASS" guidance.** That guidance was wrong: it stemmed from a
> validator bug (subscribing to a bare `#`), not a platform limit. The
> cert-subscriber below reaches **PASS** for live sources.

Event Grid MQTT namespaces reject an external subscriber that merely holds the
`EventGrid TopicSpaces Subscriber` RBAC role — RBAC is not the MQTT transport
for the JWT. You must register a client **certificate** (ThumbprintMatch) with
a Subscriber permission binding, then subscribe to the topic space's **actual
`topicTemplates`**. Use the committed tooling — do not reinvent it:

```powershell
# 1. Register a short-lived cert client bound to the topic space's client group
#    with a Subscriber permission binding (writes cert files to -OutputDirectory):
pwsh tools/Register-EventGridMqttTestClient.ps1 `
    -ResourceGroup $rg -NamespaceName <ns> -SubscriptionId <sub> `
    -OutputDirectory $certDir

# 2. Subscribe with that cert and count CloudEvents over the poll window.
#    validate_mqtt.ps1 resolves the live namespace + first topic space itself
#    and derives the subscribe filter from the live topicTemplates:
$count = & pwsh tests/e2e_deploy/validate_mqtt.ps1 -ResourceGroup $rg -CertDir $certDir
```

**The load-bearing rule — root cause of the long-standing "issue #840" 105×
WARNs:** subscribe to the topic space's live `topicTemplates` (they already end
in `/#`), **never a bare `#`**. A bare `#` is *broader* than the topic-space
template, so the broker returns **SUBACK reason code 135 (Not authorized)** and
silently delivers nothing; the template itself is **granted (reason code 1)**
and receives every published message regardless of topic depth. The old
validator subscribed to `#`, never inspected the `on_subscribe` SUBACK, and
reported 0 — producing 105 false WARNs across the fleet. **Always inspect the
SUBACK reason code**, and derive the filter from the **live topic space**
(`az eventgrid namespace topic-space ...`), not from the xreg manifest.

The generated client strips the `ce-` prefix from CloudEvents attribute names,
so MQTT v5 user properties carry **bare names** (`type`, `source`, `subject` —
not `ce-type`/`ce-source`/`ce-subject`).

**`validate_mqtt.ps1` return contract → outcome:**

| Return | Meaning | Outcome |
|--------|---------|---------|
| `>= 1` | messages received and CloudEvents properties validated | ✅ **PASS** |
| `0` | connected, SUBACK granted (reason 1), but feeder published nothing in the window (legitimately quiet source) | ⚠️ **WARN (no-data)** |
| `-1` | genuine block: no EG namespace/topic space found, cert registration failed, CONNACK rejected, or SUBACK rejected (reason >= 128) | ⚠️ **WARN (blocked)** — investigate |

Cross-check Step 2 first: if `Mqtt.Connections` = 0 the feeder never connected →
that is a ❌ **FAIL** (feeder bug), not a subscriber-side block. A `-1` with
`Mqtt.Connections > 0` is a validator/cert-side block, not a source defect.

Always delete `$certDir` afterwards — it holds a private key (see Cleanup).

#### Step 4: Teardown

```powershell
az group delete --name $rg --yes --no-wait
```

## Fabric Notebook Validation Procedure

For each source that has `feeders/<source>/notebook/`:

### Step 1: Deploy Notebook

```powershell
pwsh tools/deploy-fabric/deploy-feeder-notebook.ps1 `
    -Source <source> `
    -Workspace <workspace-name> `
    -OnceMode True `
    -BuildWheelsLocally `
    -NoSchedule
```

Key parameter notes:
- **`-Workspace`** (not `-WorkspaceName`) — the display name of the Fabric workspace
- **`-OnceMode True`** — a string parameter (not a switch); controls `ONCE_MODE` env var
- **`-BuildWheelsLocally`** — builds fresh wheels from the local repo. **Always use this**
  for E2E validation to avoid stale pre-built wheel bundles (e.g. from GitHub releases
  that predate setuptools-scm integration). Without this, you may get old 0.1.0 wheels.
- **`-NoSchedule`** — skips creating a recurring schedule; the agent triggers manually

The script outputs the notebook ID and workspace ID needed for subsequent steps.

### Step 2: Trigger and Wait

The deploy script with `-NoSchedule` already triggers one immediate run (Step B/5a).
If you need to trigger additional runs:
```
POST /v1/workspaces/{wsId}/items/{notebookId}/jobs/instances?jobType=RunNotebook
```
Poll until `status == "Completed"` or timeout.

**Failure diagnosis**: If the job reports `Failed`, check the OneLake log first:
```
GET https://onelake.dfs.fabric.microsoft.com/{wsId}/{lakehouseId}/Files/feeder-state/<source>/last-run.log
Authorization: Bearer <storage-token>   # scope: https://storage.azure.com
x-ms-version: 2021-06-08
```
The log shows import success, argv, and any caught exceptions. If the log ends
abruptly after "Running feeder.main()", the crash escaped the exception handler
(likely `SystemExit` from argparse or a native segfault from confluent-kafka).

### Step 3: Validate KQL Data

This is the core validation — **the data must actually land in typed tables**.

#### 3a: Discover the KQL Database

```
GET /v1/workspaces/{wsId}/kqlDatabases/{dbId}
```
Find the database matching the source name. The response includes the critical
`queryServiceUri` in the `properties` object — this is the Kusto cluster endpoint
needed for all subsequent queries.

```json
{
  "properties": {
    "queryServiceUri": "https://trd-XXXXX.z4.kusto.fabric.microsoft.com",
    "ingestionServiceUri": "https://ingest-trd-XXXXX.z4.kusto.fabric.microsoft.com"
  }
}
```

**Token scope for KQL queries**: `https://kusto.kusto.windows.net` (NOT the Fabric API token).

#### 3b: Query Dispatch Table

Use the **query endpoint**:
```
POST {queryServiceUri}/v1/rest/query
Content-Type: application/json
Authorization: Bearer <kusto-token>

{ "db": "<source_name>", "csl": "_cloudevents_dispatch | count" }
```
This table receives ALL events before update policies route them.
If this is zero, the event stream / ingestion path is broken.

#### 3c: Query Typed Tables

Use the **management endpoint** (not query) for `.show tables`:

```
POST {queryServiceUri}/v1/rest/mgmt
Content-Type: application/json
Authorization: Bearer <kusto-token>

{ "db": "<source_name>", "csl": ".show tables" }
```

Filter out `_cloudevents_dispatch` from the result. Then for each typed table,
use the **query endpoint**:
```
POST {queryServiceUri}/v1/rest/query

{ "db": "<source_name>", "csl": "['<table>'] | count" }
```

Note: table names with dots must be quoted: `['AU.Gov.Emergency.Wildfires.FireIncident']`.

**Pass criteria**: At least one typed table has rows > 0. If dispatch has
rows but typed tables don't, the update policy is broken (common failure
mode — the KQL script wasn't applied, or the JSON mapping is wrong).

#### 3d: Validate Data Freshness

```kql
_cloudevents_dispatch
| summarize MaxTime = max(ingestion_time())
| project MinutesAgo = datetime_diff('minute', now(), MaxTime)
```
Data should be recent (within the source's expected polling cadence).

### Step 4: Validate Map Items (if applicable)

Maps are created by `fabric/post-deploy.ps1` hooks. Validation:

#### 4a: Discover Map Items

```
GET /v1/workspaces/{wsId}/items?type=Map
```
Filter by source name in `displayName`.

#### 4b: Validate Map Has Data Layers

Retrieve the map definition:
```
GET /v1/workspaces/{wsId}/items/{mapId}
POST /v1/workspaces/{wsId}/items/{mapId}/getDefinition
```

The map definition (`map.json`) contains layers with KQL queries as data
sources. For each Kusto-backed layer:
- Execute the layer's KQL query against the source's database
- Verify the query returns > 0 rows
- This proves the map would render data points to a user

If the map uses PMTiles/GeoJSON layers (static geometry), only the
Kusto-backed dynamic layers need row-count validation.

#### 4c: Determine Map Item Source

Maps in this repo are sourced from:
1. **`fabric/post-deploy.ps1`** hooks that programmatically create/wire layers
2. **Manual** one-off creations in the workspace

The agent validates by checking if `feeders/<source>/fabric/post-deploy.ps1`
exists and references map wiring. If it does, the map is expected. If
it doesn't but a map item exists, note it as "manually created" in the
checklist.

### Step 5: Validate Dashboard Items (if applicable)

Dashboards are less common. Similar approach:
- Discover via `GET /v1/workspaces/{wsId}/items` (type filters)
- Verify the dashboard's data sources resolve to non-empty tables

### Step 6: Cleanup — MANDATORY, non-negotiable

**Every Fabric E2E test run MUST delete ALL per-source resources it created,
immediately after validation is complete.** This is not optional. Skipping
cleanup causes the workspace to accumulate hundreds of orphaned items (each
source creates 1 Eventhouse + 1 KQL database + 1 Eventstream + 1 Notebook),
which exhausts Fabric workspace capacity limits and makes future test runs
unreliable.

**Resources to delete after each source test (in this order):**

```powershell
$wsId   = "<workspace-id>"
$fabTok = az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv
$h      = @{Authorization="Bearer $fabTok"}

# 1. Cancel any running notebook jobs first
$jobs = (irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$notebookId/jobs/instances" -Headers $h).value
foreach ($job in $jobs | Where-Object { $_.status -in 'InProgress','NotStarted' }) {
    irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$notebookId/jobs/instances/$($job.id)/cancel" -Method Post -Headers $h
}

# 2. Delete notebook (also removes its schedule)
irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$notebookId" -Method Delete -Headers $h

# 3. Delete Eventstream
irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$eventstreamId" -Method Delete -Headers $h

# 4. Delete KQL Database (child of Eventhouse — must go before Eventhouse)
irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventhouses/$eventhouseId/kqlDatabases/$kqlDbId" -Method Delete -Headers $h
# OR via items endpoint:
irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$kqlDbId" -Method Delete -Headers $h

# 5. Delete Eventhouse
irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$eventhouseId" -Method Delete -Headers $h
```

**Items to PRESERVE (never delete):**
- `feeder_state_lake` Lakehouse — shared diagnostic store, not per-test
- `feeder_env` Environment — shared wheel store, rebuilt per-source but reused
- Any Map items (`*-map`) — persistent visualizations committed to the repo
- Any Dashboard items — persistent shared dashboards
- OneLake log files under `feeder-state/<source>/last-run.log` — keep for audit

**Bulk cleanup after a multi-source session:**

If individual cleanup was skipped (e.g. agents ran in parallel), clean up all
test artifacts at the end of the session with:

```powershell
$wsId   = "<workspace-id>"
$fabTok = az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv
$h      = @{Authorization="Bearer $fabTok"}
$items  = (irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items" -Headers $h).value

# Preserve list — do NOT delete these
$preserve = @('feeder_state_lake','feeder_env')
$preserveTypes = @('Map','KQLDashboard','Lakehouse','SQLEndpoint')

$toDelete = $items | Where-Object {
    $_.displayName -notin $preserve -and $_.type -notin $preserveTypes
} | Sort-Object type  # KQLDatabase before Eventhouse

foreach ($item in $toDelete) {
    Write-Host "Deleting $($item.type): $($item.displayName)"
    try {
        irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$($item.id)" -Method Delete -Headers $h -ErrorAction Stop
        Start-Sleep -Milliseconds 200
    } catch {
        Write-Warning "Failed to delete $($item.displayName): $_"
    }
}
```

**This bulk cleanup MUST be run at the end of every E2E session, regardless of
whether per-source cleanup was done.** A clean workspace is a prerequisite for
the next session — do not leave the workspace for someone else to sweep.

## KQL Validation Strategy — Reusable Yet Adaptable

The KQL validation is **schema-driven** — it derives expectations from the
xreg manifest rather than hardcoding table names per source.

### Schema-Driven Table Discovery

```python
# Pseudocode for deriving expected tables from xreg
import json

def get_expected_tables(xreg_path):
    """Derive expected KQL table names from the xreg manifest."""
    with open(xreg_path) as f:
        xreg = json.load(f)

    tables = []
    for group_key, group in xreg.get("messagegroups", {}).items():
        for msg_key, msg in group.get("messages", {}).items():
            # Convention: table name = PascalCase of message key
            table_name = msg_key.replace("-", "_").title().replace("_", "")
            tables.append({
                "message_key": msg_key,
                "table_name": table_name,
                "is_reference": "reference" in msg.get("metadata", {}).get("description", "").lower()
            })
    return tables
```

### Adaptive Validation Per Source

Not every source produces data on demand. The agent must adapt:

| Source Pattern | Validation Strategy |
|---------------|-------------------|
| **Continuous stream** (AIS, Bluesky) | Expect rows within 60s |
| **Frequent poller** (5-15 min) | Wait up to 20 min |
| **Hourly poller** | Wait up to 90 min or check existing data |
| **Event-driven** (earthquakes, alerts) | May have zero rows legitimately — check dispatch only |
| **Seasonal** (pollen, wildfires) | Check if upstream currently has data; skip if off-season |

The agent reads the source's notebook parameters (`POLLING_INTERVAL`,
`RUN_DURATION`) to determine the expected cadence and adjust timeouts
accordingly.

### Reusability Mechanism

The KQL validation logic is a **shared module** (`validate_kql.ps1`) that:
1. Takes a source name and workspace context
2. Auto-discovers the KQL database from the workspace
3. Parses the source's `kql/<source>.kql` to extract table names
4. Queries each table for row counts
5. Returns a structured result

```powershell
# validate_kql.ps1 interface
param(
    [string]$Source,
    [string]$WorkspaceId,
    [string]$DatabaseName,
    [string]$QueryUri,
    [string]$Token,
    [int]$MinRows = 1
)
# Returns: @{ dispatch_count; typed_tables = @{ name = count }; pass = $true/$false }
```

### Map Validation Module

Similarly, map validation is a shared module that:
1. Discovers map items in the workspace
2. Retrieves map definitions
3. Extracts Kusto-backed layer queries
4. Executes each query and reports row counts
5. Handles the case where no map exists (N/A, not failure)

## Issue Filing Protocol

### Title Pattern
```
[E2E] <source> - <target>: <failure-category>
```

### Outcome Classification

| Result | When | Action |
|--------|------|--------|
| **PASS** | ≥1 message received, checks pass | Record ✅ in checklist |
| **WARN** | Stack running, broker connected, but 0 messages (upstream has no data) | Record ⚠️ in checklist; no GitHub issue |
| **FAIL** | Any deploy failure, crash, auth error, schema mismatch | Record ❌ in checklist; file GitHub issue immediately |
| **BLOCKED** | Known env limitation (e.g. MQTT subscribe blocked) | Record 🔒 in checklist; no new issue unless root cause is new |

### Failure Categories (for FAIL issues only)
- `no-data` — container/notebook ran but no events arrived AND infrastructure/auth is broken (not just quiet upstream)
- `dispatch-only` — events in dispatch but not in typed tables (update policy broken)
- `schema-mismatch` — payload doesn't match xreg schema
- `deploy-failed` — container/notebook failed to start or reach Running state
- `timeout` — exceeded wait time due to a defect (not quiet upstream)
- `map-empty` — map exists but layers return zero rows
- `stale-data` — data exists but is older than expected cadence

### Warning Categories (for WARN checklist entries only, no issue filed)
- `no-data-upstream` — stack healthy, broker connected, upstream returned no data (differential poller, seasonal source, no current events)

### Deduplication

Before creating an issue, search:
```
gh issue list --label e2e-validation --state open --search "[E2E] <source> - <target>"
```
If found: append a comment with the new session ID and error details.
If not found: create a new issue.

## Outputs

Per session:
- `sessions/<ts>/CHECKLIST.md` — filled-in per-source checklist (✅/⚠️/❌/🔒/—)
- `sessions/<ts>/summary.json` — machine-readable pass/warn/fail/skip counts
- `sessions/<ts>/log.txt` — full execution log
- `sessions/<ts>/<source>-azure-result.json` — per-source Azure result (status: pass|warn|fail|blocked|skip)
- `sessions/<ts>/<source>-fabric-result.json` — per-source Fabric result

## References

- [validate_kql.ps1](references/validate_kql.ps1) — KQL validation module
- [validate_map.ps1](references/validate_map.ps1) — Map validation module
- [source_cadence.json](references/source_cadence.json) — per-source expected data cadence
- [CHECKLIST_TEMPLATE.md](../../tests/e2e_deploy/CHECKLIST_TEMPLATE.md) — session checklist template

## Operational Pitfalls (from real runs)

### 1. Stale pre-built wheels

The GitHub release artifacts may contain old wheels (e.g. v0.1.0 from before
setuptools-scm integration). Always use `-BuildWheelsLocally` to build from
the current repo HEAD. The deploy script will remove old wheels from OneLake
before uploading the fresh ones.

### 2. argparse --once vs ONCE_MODE env var

Notebooks do NOT pass `--once` in `sys.argv`. The `ONCE_MODE=true` env var
(set by the parameter cell) controls the argparse default. Some feeders have
`--once` on the top-level parser (not the feed subparser), so passing it after
`feed` in argv would cause `sys.exit(2)`.

### 3. KQL API endpoint confusion

- **Query endpoint** (`/v1/rest/query`): for KQL queries like `T | count`
- **Management endpoint** (`/v1/rest/mgmt`): for control commands like `.show tables`
- Both use the same `queryServiceUri` base URL but different paths
- Token scope: `https://kusto.kusto.windows.net` for both

### 4. Event Stream ingestion lag

After a notebook run completes, data may take 30–90 seconds to flow through
the Event Stream and appear in the `_cloudevents_dispatch` table. Wait at
least 60 seconds before querying KQL after a successful notebook run.

### 5. Seasonal/event-driven sources

Sources like `australia-wildfires` are event-driven — they may have zero
events if no incidents are active. But if they DO fetch data, it should
flow end-to-end (dispatch + typed). During the June 2026 validation run,
australia-wildfires returned 37 active fire incidents from VIC and NSW.

### 6. `az container list` returns empty state

`az container list --resource-group $rg` may return `null`/empty
`instanceView.state`. Always use `az container show --name <name>` to get
the correct running state:

```powershell
$containerName = az container list --resource-group $rg --query "[0].name" --output tsv
$state = az container show --resource-group $rg --name $containerName `
    --query "instanceView.state" --output tsv
```

### 7. Service Bus ARM templates don't grant Listen rights

SB ARM templates for this repo do NOT grant the deploying identity any data
plane rights. `DefaultAzureCredential` will fail with `amqp:unauthorized-access`
("Listen claim required"). **Before** calling `validate_servicebus.ps1`, assign
the receiver role and wait 30 s for propagation:

```powershell
$myOid = az ad signed-in-user show --query id --output tsv
$sbId  = az servicebus namespace show --resource-group $rg --namespace-name <ns> `
    --query id --output tsv
az role assignment create --assignee $myOid `
    --role "Azure Service Bus Data Receiver" --scope $sbId --output none
Start-Sleep -Seconds 30
```

Using a SAS `RootManageSharedAccessKey` connection string for receiving will also
fail with `amqp:client-error`. Always use DefaultAzureCredential + FQNS.

### 8. Event Grid MQTT has a two-layer authZ chain — both layers break independently

The EG MQTT ARM template creates a user-assigned managed identity and assigns it
`EventGrid TopicSpaces Publisher` on the topic space. The ACI container gets the
identity and three env vars: `MQTT_AUTH_MODE=entra`, `MQTT_ENTRA_AUDIENCE`,
`MQTT_ENTRA_CLIENT_ID`. These two authZ layers are separate and both failed:

**Layer 1 — Feeder → EG broker (publish path):**
Early xrcg-generated MQTT `app.py` files did not read `MQTT_AUTH_MODE`,
`MQTT_ENTRA_AUDIENCE`, or `MQTT_ENTRA_CLIENT_ID`. Sources not yet regenerated
with a current xrcg template will connect with no credentials and receive
CONNACK rc=5. Detect with `Select-String -Path "feeders/<source>/*_mqtt/*_mqtt/app.py" -Pattern "MQTT_AUTH_MODE" -Quiet`.
If missing, regenerate via `generate_producer.ps1` — do not hand-edit. Mark
the feeder-publishing step as **FAIL** and file a **new** issue per source;
do not reference the closed issue #840.

**Layer 2 — Test validator → EG broker (subscribe path):**
`EventGrid TopicSpaces Subscriber` RBAC alone does **not** authorize external MQTT
connections from non-Azure clients. A registered client certificate or an Entra JWT
whose subject matches a registered `Microsoft.EventGrid/namespaces/clients` entry
is required. The ARM template does not create a `clients` resource, so there is no
registered test identity to authenticate with even if the validator acquired a token.
Connections from local dev or CI return CONNACK rc=5 (Not authorized).

Use Azure Monitor metrics (`Mqtt.Connections`, `Mqtt.SuccessfulPublishedMessages`)
as the only available validation proxy for Layer 1. Mark the external-subscribe
step as **BLOCKED** (not a source failure); mark the feeder-publishing step as
**FAIL** (with a new per-source issue) if metrics show 0 connections.

### 9. Generated MQTT client's `connect()` is not awaited

The generated paho-based MQTT client's `connect()` method is fire-and-forget.
If authentication fails (e.g. no Entra token), paho retries silently and
`publish()` queues messages that are never delivered. The container log will
report "Published N events" even when 0 messages reached the broker.

**Always verify via Event Grid metrics, not container logs alone.**
See also issue #840 for the Entra auth gap in the MQTT feeder.

### 10. Structured vs binary CloudEvents over Kafka

Sources may emit in **structured** mode (`content-type: application/cloudevents+json`
with CE attributes in the JSON body) or **binary** mode (CE attributes as Kafka
`ce_*` headers). The validator must accept both. Check the `content-type` header
to determine mode; in structured mode there are **no** `ce_type`/`ce_source`/
`ce_subject` Kafka headers.

### 16. "Before-first-cell + 404 log" — three distinct root causes

When a Fabric notebook job fails with `System_Cancelled_Session_Statements_Failed`
**and** `last-run.log` is HTTP 404 (never written), the failure happened before
any Python executed. Three distinct causes:

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| First-ever deploy, 404 log | `-SkipEnvironment` used on first deploy — no wheels in Lakehouse | Re-deploy without `-SkipEnvironment` |
| SyntaxError in **any** cell | Fabric pre-compiles **all** cells before executing cell 0; any bare `if X:` with empty body or other SyntaxError aborts the session | Fix the syntax error in the offending cell |
| Fabric capacity not ready | Environment not yet published, or capacity in cooldown | Retry after 10 min |

The SyntaxError variant was triggered by the old `deploy-feeder-notebook.ps1`
`Ensure-OneShotStateCleanup` function, which injected a bare `if ONCE_MODE:\n`
with no body into the run cell. Fixed in commit `85adb3dde`. Notebooks deployed
before that fix must be manually corrected.

**Detection:** Use `GET /lakehouse/.../Files/feeder-state/<source>/last-run.log`
with `https://storage.azure.com` audience. If 404 after a failed run, it's
always a before-cell-0 failure — check for SyntaxError first.

### 17. Fabric pre-compiles all cells before executing any

A SyntaxError in **any** cell (even the last one) causes
`System_Cancelled_Session_Statements_Failed` before cell 0 ever runs.
The OneLake `last-run.log` stays 404 because no Python executes.

**Common injected SyntaxErrors:**
- Bare `if ONCE_MODE:` with no body (old deploy script)
- Bare `if condition:` with only a comment body (`# nothing`)
- Missing `pass` in any empty conditional block

**Prevention:** Run `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <slug>`
before every deploy. The validator AST-parses the run cell and catches empty
conditional bodies.

### 18. `--force-reinstall` on PyPI deps → SIGKILL at ~27 s, no log

`confluent_kafka` (and other C-extension packages) with `--force-reinstall`
re-downloads and recompiles even when cached. Fabric SIGKILLs the kernel at
~27 s; no exception handler runs, `last-run.log` is never written.

**Fix:** Use `--upgrade` for PyPI deps; keep `--force-reinstall --no-deps` only
for local wheels (pure Python, fast). The fleet-wide fix was applied in
commit `85adb3dde`.

### 19. Old AMQP `app.py` missing `AMQP_AUTH_MODE=entra`

22 sources shipped with xrcg-generated AMQP `app.py` files that only read
`AMQP_USERNAME`/`AMQP_PASSWORD` and ignore `AMQP_AUTH_MODE`. These sources
silently connect with no credentials against Azure Service Bus (which requires
Entra auth) and get an `amqp:unauthorized-access` error.

**Detection:**
```powershell
Select-String -Path "feeders/*_amqp/*_amqp/app.py" -Pattern "AMQP_AUTH_MODE" -Quiet
```
If this returns nothing, the file is old. **Fix:** regenerate with
`generate_producer.ps1` (latest xrcg template has full Entra support).

### 20. ACI startup failures — two distinct patterns

**Pattern A — Wrong GHCR image tag:**
ARM template uses `ghcr.io/...-kafka:latest` but published image is
`ghcr.io/...:latest` (no `-kafka` suffix). Container immediately enters
`ImagePullBackoff`.
Detection: `az container show --query "containers[0].instanceView.events"`

**Pattern B — Missing required env vars:**
Source uses argparse and a required argument has no default. If the env var
that maps to it is absent from the ARM template, argparse exits with code 2
and the container terminates immediately. No application log is written.
Detection: exit code 2 in container events; check argparse `required=True`
parameters against the ARM template env vars.

### 21. Non-canonical notebook patterns fail silently

Notebooks that deviate from the 4-cell canonical structure (markdown → parameters
→ CS-lookup → run) fail in ways that produce no diagnostic output:

- `asyncio.run()` in a cell → `RuntimeError: This event loop is already running`
  (Fabric kernel owns the loop)
- `%pip install` in a cell → 60–120 s startup overhead; SIGKILL on some capacities
- Missing `notebookutils.notebook.exit()` → scheduled run shows "Completed" even
  when the feeder crashed mid-run
- `CONNECTION_STRING` as a notebook parameter → exposed in Fabric UI; use
  Topology API lookup instead

**Fix:** Run `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <slug>`
before deploying. The validator enforces the canonical structure.

### 22. `--once` placed on top-level parser instead of `feed` subparser

28 feeders had `--once` defined on the top-level `ArgumentParser` rather than
on the `feed` subparser. `CMD ["python", "-m", "module", "feed", "--once"]`
in a Dockerfile caused `sys.exit(2)` because `feed` consumed the argv and
`--once` was not recognized by the subparser.

**Flat-parser feeders (no subparsers):** Apply an argv shim that strips `feed`
before `parse_args()`, and update the Dockerfile CMD to include `feed`.
**Subparser feeders:** Add `--once` to the `feed` subparser in addition to the
top-level parser (keep both for backwards compat).

Fixed fleet-wide in PR #904.

### 23. `noaa` measurement events silently dropped before first emission

The `noaa` bridge instantiated measurement dataclasses without a required
`region` field. The missing field caused a crash on the first measurement
record — before any events were emitted to Kafka. Container log showed the
bridge starting normally; no error was surfaced until the first poll cycle.

Additionally, the visibility-measurement path called the generated producer
with positional arguments in the wrong order, passing `None` as the
CloudEvents `source` attribute (which the producer silently accepted, emitting
a malformed event).

**Detection:** E2E test returns 0 messages for `noaa` despite container running.
**Fix:** PR #906.

### 24. `test-noaa` CI workflow used Poetry against a setuptools `pyproject.toml`

The `test-noaa.yml` workflow installed Poetry and ran `poetry install`, but
`feeders/noaa/pyproject.toml` uses `setuptools` as the build backend (no
`[tool.poetry]` table). `poetry install` failed with:
`"Either [project.version] or [tool.poetry.version] is required in package mode."`

This caused the CI job to fail on every PR touching `feeders/noaa/**` — a
pre-existing failure that masked real test regressions.

**Fix:** Replace Poetry install steps with `pip install -e ".[dev]"`. The
`conftest.py` adds producer sub-packages to `sys.path` directly, so they
don't need to be pip-installed separately (PR #906).

**General rule:** Before attributing a CI failure to your PR changes, check
if the same job was already failing on `main`:
```powershell
gh api "/repos/clemensv/real-time-sources/actions/workflows/<workflow>.yml/runs?branch=main&per_page=5" |
  ConvertFrom-Json | Select-Object -ExpandProperty workflow_runs |
  Select-Object conclusion
```

### 25. Stale worktrees from merged PRs accumulate silently

After merging PRs from worktrees, the worktrees remain on disk and in
`git worktree list`. Stale worktrees:
- Confuse `git worktree list` output
- Hold file locks on Windows that can block future `git` operations
- Can be mistaken for in-progress work in future sessions

**Cleanup after each session:**
```powershell
git worktree list  # identify merged branches
git worktree remove --force <path>  # for each merged worktree
```

**Detection of already-merged branches before creating new PRs:**
```powershell
git -C <worktree> log main..HEAD --oneline
# If empty: branch is already merged; no PR needed
```

### 26. Transient Docker Hub network failures are not code failures

GitHub Actions runners intermittently fail to pull `python:3.10-slim` or
`docker/dockerfile:1.6` from Docker Hub with:
- `context deadline exceeded`
- `net/http: request canceled while waiting for connection`
- `read: connection reset by peer`

These are infrastructure failures, not code regressions. **Never revert or
modify source code** based solely on a Docker build failure.

**Protocol:**
1. Check the error message — if it contains `registry-1.docker.io` or
   `auth.docker.io` and a network error, it is transient.
2. Rerun only the failed jobs: `gh run rerun <run-id> --repo <repo> --failed`
3. Wait for the rerun before merging. Do not merge with `--admin` to bypass
   Docker build checks unless the overall run status is `completed/success`
   (which means GitHub Actions considers the run green despite stale job
   entries in the PR checks UI).

### 11. MQTT user properties use bare names (no `ce-` prefix)

The generated MQTT client's `_ce_headers_to_mqtt5_properties` helper strips the
`ce-` prefix before setting MQTT v5 user properties. Messages arrive with `type`,
`source`, `subject` user properties — not `ce-type`, `ce-source`, `ce-subject`.
The CloudEvents MQTT binding spec requires the prefix; this is a known generator
compliance issue. The validator must accept both prefixed and bare forms.

### 12. Fabric notebook terminal run status is "Completed"

When polling Fabric notebook run status via the REST API, the terminal-success
status is `"Completed"` — not `"Succeeded"`. Include both `"Completed"` and
`"Failed"` (and `"Cancelled"`) in your terminal status set:

```powershell
$terminal = @("Completed", "Failed", "Cancelled", "DeadLettered")
```

### 13. ARM templates with role assignments require Owner or User Access Administrator

Several ARM templates in this repo (`azure-template-with-eventgrid-mqtt.json`)
include `Microsoft.Authorization/roleAssignments` resources. The deploying identity
must have `Microsoft.Authorization/roleAssignments/write` permission — i.e. **Owner**
or **User Access Administrator** — on the subscription or resource group.

**Contributor alone is not sufficient.** If the deploying identity only has
Contributor, the ARM deployment will fail at the role assignment step with:
```
The client does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/write'
```

Before deploying, verify the identity's role:
```powershell
$myOid = az ad signed-in-user show --query id --output tsv
az role assignment list --assignee $myOid --subscription <sub> `
    --query "[?roleDefinitionName=='Owner' || roleDefinitionName=='User Access Administrator'].roleDefinitionName"
```

If the deployment fails at role assignment, either elevate the identity or
pre-create the role assignment manually and use `--mode Incremental` to skip
the already-created resource.

### 14. Fabric bulk DELETE hits 429 rate limits at scale

When deleting 30+ KQL Databases or Eventhouses in quick succession, the Fabric
REST API returns `429 Too Many Requests`. The workaround is to retry with
backoff and sort deletions to process KQL Databases before Eventhouses:

```powershell
foreach ($item in $toDelete) {
    $ok = $false
    for ($i = 0; $i -lt 3 -and -not $ok; $i++) {
        try {
            irm "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items/$($item.id)" `
                -Method Delete -Headers $h -ErrorAction Stop | Out-Null
            $ok = $true
            Start-Sleep -Milliseconds 800   # throttle between deletes
        } catch {
            if ($_.Exception.Response.StatusCode -eq 429) {
                Start-Sleep -Seconds 5      # back off on rate limit
            } else {
                Write-Warning "FAILED $($item.type) $($item.displayName): $_"
                $ok = $true                 # don't retry non-429
            }
        }
    }
}
```

A 800 ms inter-delete delay allows ~75 deletes/minute — sufficient for
workspace cleanup without triggering the rate limiter. The bulk cleanup
script in Step 6 already includes these retry semantics.

### 15. Fabric authZ — Entra token audience matters

The Fabric REST API uses the `https://api.fabric.microsoft.com` resource (NOT
`https://analysis.windows.net/powerbi/api`). Using the wrong audience returns
`403 Unauthorized` even with a valid signed-in identity.

KQL queries use a different resource: `https://kusto.kusto.windows.net` — this
is the same audience for all Fabric KQL endpoints regardless of whether the
cluster URL contains `kusto.fabric.microsoft.com`. Using `kusto.fabric.microsoft.com`
as the audience will result in `401 Unauthorized`.

Summary:
- Fabric REST API management: `https://api.fabric.microsoft.com`
- KQL REST queries: `https://kusto.kusto.windows.net`
- OneLake DFS: `https://storage.azure.com`

### Pitfall #16: Notebook crashes before log cell — no OneLake diagnostic available

**Symptom**: `System_Cancelled_Session_Statements_Failed`, OneLake `last-run.log` returns 404.

**Cause**: A cell *before* the run cell (typically the pip-install cell or the CS-lookup cell) raised an unhandled exception. Since the log file is opened in the run cell, earlier failures leave no trace.

**Diagnoses**:
1. Check Lakehouse Files for wheels: `GET https://onelake.dfs.fabric.microsoft.com/{ws}/{lhId}/Files/wheels/{source}/` — if empty, the deploy was run with `-SkipEnvironment` but wheels had never been uploaded. Re-run without `-SkipEnvironment`.
2. Check the pip-install cell for `subprocess.check_call` — if it raises, the kernel dies silently. Capture stderr by removing `stdout=subprocess.DEVNULL` temporarily.
3. If wheels are present but CS-lookup cell crashes, add explicit error logging before the CS-lookup call.

**Fix**: Always run the deploy script without `-SkipEnvironment` for the first deploy of a source (wheels have never been uploaded). `-SkipEnvironment` is safe only when wheels are already in the Lakehouse from a prior run.

**Extended diagnosis — distinguishing two "before-first-cell" root causes:**

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| 404 log + no Lakehouse wheels | `-SkipEnvironment` on first deploy | Re-run without flag |
| 404 log + wheels present + passes validator | **SyntaxError in any cell** (see #17) | Fix notebook source |
| 404 log + wheels present + known good notebook | Fabric capacity / Environment not published | Wait 10 min, retry; check `/staging/sparkcompute` publish status |

### Pitfall #17: SyntaxError in any cell causes the entire session to fail before cell 0 executes

**Symptom**: `System_Cancelled_Session_Statements_Failed`, OneLake `last-run.log` returns 404, even though wheels are present and the notebook otherwise looks correct.

**Root cause**: Fabric pre-compiles **all** cells as a single AST before executing any of them. A SyntaxError in cell 5 will abort the session before cell 0 runs — so no Python ever executes, and the log file is never created.

**Most common sources of injected SyntaxErrors in this repo:**

1. **Deploy script `Ensure-OneShotStateCleanup` injection** (now fixed in `deploy-feeder-notebook.ps1`): The function injected Python lines by appending strings to the `cell.source` array without trailing `\n`. Jupyter concatenates `source` array elements with no separator, so multi-line injections become one long line. `if ONCE_MODE:` followed immediately by `os.remove(STATE_FILE)` becomes `if ONCE_MODE:        os.remove(STATE_FILE)` — valid as one line. But `if ONCE_MODE:` injected alone (with the body as a separate element that is not properly indented) becomes a bare `if ONCE_MODE:` with no body → `SyntaxError: expected an indented block`.

2. **Notebook files committed before the deploy script fix**: If a notebook was deployed and then committed to the repo with the injected SyntaxError baked in, all future redeploys will fail until the notebook source is corrected.

**Detection**: Inspect the run cell source programmatically — look for any bare `if ...:` that has an empty string or only whitespace as the next array element:
```powershell
$nb = Get-Content "feeders/<source>/notebook/<source>-feed.ipynb" | ConvertFrom-Json
$nb.cells | ForEach-Object { $i = 0 } {
    $src = $_.source -join ""
    if ($src -match "if [^:]+:\s*$") { Write-Host "BARE IF in cell $i" }
    $i++
}
```

**Fix**: Edit the notebook source so `if ONCE_MODE:` has a proper body:
```python
if ONCE_MODE:
    sys.argv.append('--once')
```

After fixing, re-validate with `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <source>` and confirm 0 blockers.

### Pitfall #18: `--force-reinstall` on PyPI deps causes silent SIGKILL before any log is written

**Symptom**: `System_Cancelled_Session_Statements_Failed`, OneLake `last-run.log` returns 404. Wheels are present. No SyntaxError in notebook. The session is killed approximately 27–30 seconds after kernel start.

**Root cause**: Using `--force-reinstall` for binary C extensions (specifically `confluent_kafka`) in the pip-install cell forces pip to re-download and recompile the extension even when it is already cached in the Fabric Environment. This process takes >27 s. Fabric SIGKILLs the kernel process after its per-cell timeout. SIGKILL bypasses all Python exception handlers and `try/except` blocks — no log file is written, the run cell never starts.

**Detection**: Check the pip-install cell for `--force-reinstall` combined with PyPI packages (not local wheels):
```python
# BAD — kills the kernel via SIGKILL after ~27s
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q',
    '--upgrade', '--force-reinstall',   # <-- this flag
    'avro>=1.11.3', 'confluent_kafka>=2.5.3', ...])

# GOOD — fast upgrade check, no recompile if already present
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q',
    '--upgrade',                        # no --force-reinstall
    'avro>=1.11.3', 'confluent_kafka>=2.5.3', ...])
```

`--force-reinstall` is fine for **local wheels** (pure Python, no compilation):
```python
# OK — local wheels are pure Python, fast even with force-reinstall
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q',
    '--force-reinstall', '--no-deps'] + local_wheels)
```

**Fleet check**: If a fleet-wide `System_Cancelled_Session_Statements_Failed` pattern appears across many sources after a deploy script change, first check whether `--force-reinstall` was added to the PyPI line:
```powershell
Select-String -Path "feeders\*\notebook\*-feed.ipynb" -Pattern "force-reinstall" | Where-Object { $_ -match "confluent_kafka|avro|cloudevents" }
```

### Pitfall #19: AMQP companion app ignores `AMQP_AUTH_MODE=entra` in older generated sources

**Symptom**: ACI container deploys and appears to start (reaches `Running` state), container log shows no output at all or very little, 0 messages received on Service Bus queue/topic.

**Root cause**: Sources regenerated before the xrcg template gained Entra auth support have an AMQP `app.py` that only reads `AMQP_USERNAME` / `AMQP_PASSWORD`. The `azure-template-with-servicebus.json` ARM template sets `AMQP_AUTH_MODE=entra`, `AMQP_ENTRA_AUDIENCE`, and `AMQP_ENTRA_CLIENT_ID` — but the old app.py ignores all three and connects to Service Bus with empty credentials → AMQP auth failure → 0 messages.

**Detection**: Check for `AMQP_AUTH_MODE` in the source's AMQP app.py:
```powershell
Select-String -Path "feeders/<source>/*_amqp/*_amqp/app.py" -Pattern "AMQP_AUTH_MODE" -Quiet
```
If this returns `False`, the source needs regeneration.

**Fleet-wide check**:
```powershell
$files = Get-ChildItem "feeders" -Recurse -Filter "app.py" | Where-Object { $_.FullName -match "_amqp\\" }
$missing = $files | Where-Object { -not (Select-String -Path $_.FullName -Pattern "AMQP_AUTH_MODE" -Quiet) }
Write-Host "$($missing.Count) sources need regeneration"
```

**Fix**: For each affected source, run `pwsh feeders/<source>/generate_producer.ps1` to regenerate with the latest xrcg template. Do NOT hand-edit the generated app.py. Commit the regenerated files and verify `AMQP_AUTH_MODE` is present.

**Note**: This failure is distinct from a container startup failure — the container reaches `Running` state and may log initial startup messages, but then produces nothing. Always check SB queue depth after 60–120 s, not just container state.

### Pitfall #20: ACI container never reaches `Running` — wrong image tag or missing required env vars

**Symptom**: `az container show` reports `Waiting` or `Terminated` indefinitely. The ARM template deploys without error, but the container never becomes `Running` within the 180 s poll window.

**Root cause A — Wrong GHCR image tag**: The ARM template references a GHCR image tag that does not exist (e.g. `ghcr.io/clemensv/real-time-sources-<source>-kafka:latest` when the published image is `ghcr.io/clemensv/real-time-sources-<source>:latest`). The container runtime can't pull the image → `ImagePullBackoff` → never `Running`.

**Detection**: Check container events via:
```powershell
az container show --resource-group $rg --name $containerName --query "containers[0].instanceView.events" --output json
```
Look for `Failed to pull image` or `ErrImagePull` events.

**Fix**: Correct the image tag in the ARM template. The canonical tag pattern is `ghcr.io/clemensv/real-time-sources-<source>:latest` (no transport suffix on the primary Kafka image). AMQP and MQTT variants use `:latest` on their respective images.

**Root cause B — Missing required env vars that cause immediate exit**: Some feeders require specific env vars to start (e.g. `GBFS_FEEDS` for gbfs-bikeshare). If the ARM template doesn't pass them, the feeder calls `sys.exit(1)` immediately after argparse fails → container state goes `Terminated` within seconds.

**Detection**: Check container exit code and logs:
```powershell
az container logs --resource-group $rg --name $containerName
az container show --resource-group $rg --name $containerName --query "containers[0].instanceView.currentState" --output json
```
An exit code of 2 indicates argparse failure (missing required argument).

**Fix**: Add the missing env vars to the ARM template. Check the feeder's `__main__.py` or `argparse` setup for required arguments with no `default` value.

### Pitfall #21: Non-canonical notebook patterns fail silently in Fabric

**Symptom**: Notebook deploys, runs, exits `OK`, but 0 messages appear in KQL tables. Or notebook fails with obscure import errors that don't appear in other sources.

**Root cause**: The notebook diverges from the canonical 4-cell pattern in ways that work locally but fail in Fabric:
- Using `azure-eventhub` (`EventHubProducerClient`) instead of the Kafka (`confluent_kafka`) pattern used by the rest of the fleet
- Calling feeder helper functions directly (`feeder.poll_and_submit()`) instead of `feeder.main()` — misses env var setup that `main()` performs
- `t.join()` with no timeout — notebook runs indefinitely, never exits, Fabric eventually kills it
- Log cell comes AFTER the pip-install cell — pip failures leave no trace

**Detection**: Any notebook that fails consistently without a clear log should be checked against the canonical pattern. Compare with `feeders/pegelonline/notebook/pegelonline-feed.ipynb`.

Required canonical structure:
1. Markdown intro
2. Parameters cell (with `parameters` tag): `EVENTSTREAM_NAME`, `STATE_FILE`, `POLLING_INTERVAL`, `RUN_DURATION`, `ONCE_MODE`, `WORKSPACE_ID`
3. Early-log + pip-install cell: **opens log file first**, then installs wheels
4. CS-lookup cell: Topology API pattern
5. Run cell: `feeder.main()` via worker thread, `t.join(timeout=RUN_DURATION)`, `notebookutils.notebook.exit("OK"|"FAIL: ...")`

**Validator**: Run `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <source>` — it enforces the structural rules mechanically. A notebook that passes the validator with 0 blockers is structurally sound. A notebook that bypasses the validator may look fine but break in Fabric.


---

## Fleet Matrix Operations & Result Reconciliation

Running the **full** source × target matrix (≈105 sources × {fabric, azure-eh,
azure-sb, azure-eg}) is a multi-hour operation. These rules keep a long run
correct, resumable, and honestly reported. They were all learned the hard way
on real fleet runs — treat them as load-bearing, not advisory.

### Result-file reconciliation (stale files mask fresh truth)

The matrix is reconstructed from per-cell result JSON on disk, and **two naming
schemes coexist**:

- **Full-name** (current harness): `<src>-azure-eventgrid-mqtt-result.json`,
  `<src>-azure-eventhub-result.json`, `<src>-azure-servicebus-result.json`,
  `<src>-fabric-result.json`.
- **Legacy short-name**: `<src>-azure-eg-result.json`, `<src>-azure-eh-...`,
  `<src>-azure-sb-...`.

When you render or tally the matrix you **must**:

1. **Normalize** both schemes to one canonical `(source, target)` key
   (`azure-eg`/`azure-eh`/`azure-sb`/`fabric`). A full-name file with
   `target: "azure"` + a `variant` field maps to the same cell as its
   short-name twin.
2. **Dedup by latest mtime** per `(source, target)`. A stale short-name file
   left over from a prior run will otherwise **mask a fresh full-name PASS** and
   re-introduce a phantom WARN/FAIL. Always pick the newest file per cell.
3. **Reconcile after every targeted re-run.** When you re-run one cell to fix a
   FAIL, the runner may write the full-name file while an old short-name file
   still sits next to it. Delete or overwrite the stale twin, or the rendered
   matrix will show the old result. Most "the fix didn't take" confusion on long
   runs is actually a stale result file, not a real regression.

### Runner-queue saturation (don't fire the whole fleet at once)

Firing 40–105 deployments (or CI runs) simultaneously **saturates the shared
runner/control-plane queue**: jobs sit in `queued` rather than failing, and a
naive tally reads them as hangs. Throttle to a small concurrency (the session's
`rerun_eg_fleet.ps1` used a bounded driver) and let waves drain. Note that
**merging a PR cancels that branch's queued CI runs** — a useful lever when you
have intentionally over-queued and want to reclaim the queue.

### Env-key gating — SKIP keyless sources *before* deploy (never mid-deploy)

`tests/e2e_deploy/check_env_keys.ps1` is the authoritative map of which sources
need which API-key env vars (e.g. `aisstream`→`AISSTREAM_API_KEY`,
`entsoe`→`ENTSOE_SECURITY_TOKEN`, `billetto`, `nasa-firms`, `uk-bods-siri`). It
returns `$null` when nothing is missing. **Gate on it and mark the cell SKIP /
🔒 BLOCKED *before* provisioning** when the key is absent. A keyless deploy of a
secret-requiring source does not fail cleanly — the ARM `securestring` parameter
(see next item) prompts on stdin and **hangs the whole non-interactive run
forever**. Secrets for a run come from the out-of-repo creds file
(`c:\rts-creds\test-creds.json`), never from the repo.

### ARM `securestring` params with `minLength:1` and no `defaultValue` → stdin-hang

This single template defect produced dozens of false "deploy-failed (exit -1)"
cells. A `securestring`/`string` ARM parameter with `minLength: 1` and **no**
`defaultValue` makes `az deployment group create` **prompt on stdin** when the
corresponding env var is absent (auth-free sources like `dmi`, or any keyless
run). In a non-interactive E2E that prompt blocks until timeout. **Fix the
template, not the harness:** add `"defaultValue": ""` to every such parameter
across the source's `eventhub` / `servicebus` / `eventgrid-mqtt` templates
(repo precedents: `dmi`, `gbfs-bikeshare`, `siri`, `ticketmaster`). Same class
as the `gbfsFeeds` param stdin-hang (give it a working default, e.g. Citi Bike
NYC). This is a *real bug* under "Real Bugs Are Blockers", not a test nuisance.

### Notebook parameter `\n`-gluing corruption → `NameError` on a param

**Symptom:** a Fabric notebook run dies with `NameError: name
'EVENTSTREAM_NAME' is not defined` (or `RUN_DURATION`, etc.) at the
connection-string cell, even though the params cell visibly assigns it.

**Root cause:** elements of the `.ipynb` `cell.source` array end with the
**two-character literal sequence** `\` + `n` instead of a real newline. The
deploy converter does `($cell.source -join '')` then `-split "<real newline>"`,
so a literal-`\n` line never splits — the `# === PARAMETERS ===` comment header
glues onto the `EVENTSTREAM_NAME = ...` line and **comments it out**. The
variable is then undefined downstream.

**Fix:** heal any source element ending in literal `\n` → real newline right
after load (lossless — a well-formed element never ends with a literal `\n`),
and repair the checked-in notebook. Scan the whole fleet for the pattern when
you find one; it tends to come from a bad programmatic notebook edit, not from
Jupyter. Related: Pitfall #17 (any SyntaxError fails the whole session before
cell 0) and Pitfall #21 (non-canonical notebook structure).

### Rendering the matrix

After reconciliation, tally per target: `<n> pass / <n> warn / <n> FAIL`, plus a
fleet total over all cells. A healthy full-fleet end state is **green/yellow**:
0 FAIL, with WARNs explained (no-data slow pollers, EG cert-propagation timing,
upstream seasonally idle). Never report a run "green" while any cell is FAIL or
while result files are unreconciled — a FAIL is a deploy/crash/auth/schema
defect that must be fixed or explicitly escalated to the user with its reason.

## Static Analysis as a Validation Gate

A full E2E deployment validates runtime behavior — containers start, connect,
and emit events. But it does NOT catch type-safety issues that cause subtle
data corruption (e.g., passing a raw string where a datetime is expected, so
downstream `.year` access crashes). These bugs survive live validation because
the Avro encoder accepts strings via its fallback path.

**Mandatory pre-deployment static validation:**

Before declaring any fleet-wide validation run complete, verify that `mypy`
CI is green. The mypy workflow with MYPYPATH catches:

- Wrong constructor arguments to generated data classes
- Missing nullable handling (passing `None` to non-Optional fields)
- Method/attribute errors on producer classes
- Incorrect enum conversions

A passing E2E test with a failing mypy CI means the bridge "works" but has
latent type bugs that will crash on downstream access patterns.

### Schema-runtime nullability alignment

If E2E validation reveals a feeder that crashes or silently drops records
because an upstream field is unexpectedly `null`, the fix is almost always
in the xreg schema (add null to the type union), NOT in the bridge
(adding a `try/except` or `or ""`). The schema must match upstream reality:

1. Check whether the upstream API actually guarantees the field (API docs
   + live payload inspection)
2. If the field CAN be null upstream, add `"null"` to the type union in
   the jstruct schema
3. Remove the field from `required` if it has an `enum` constraint
   (xrcg won't generate `Optional[EnumType]` otherwise)
4. Regenerate the producer (`generate_producer.ps1`)
5. Remove the `# type: ignore[arg-type]` from the bridge code
6. Verify mypy passes clean

### CI test workflow packaging pattern

When validating that feeder tests pass in CI, the most common failure mode
is `ERROR: No matching distribution found for <local-package>`. Every
feeder's test workflow must install generated producer packages and local
sub-packages (e.g., `*_core`) explicitly via `pip install -e ./<path>`
BEFORE `pip install -e '.[dev]'`. Reference: `test-pegelonline.yml`,
`test-gtfs.yml`. Common local packages to install first:

```
pip install -e ./<src>_producer/<src>_producer_data
pip install -e ./<src>_producer/<src>_producer_kafka_producer
pip install -e ./<src>_mqtt_producer/<src>_mqtt_producer_data        # if mqtt
pip install -e ./<src>_mqtt_producer/<src>_mqtt_producer_mqtt_client # if mqtt
pip install -e ./<src>_amqp_producer/<src>_amqp_producer_data       # if amqp
pip install -e ./<src>_amqp_producer/<src>_amqp_producer_amqp_producer # if amqp
pip install -e ./<src>_core                                          # if exists
pip install -e '.[dev]'
```
