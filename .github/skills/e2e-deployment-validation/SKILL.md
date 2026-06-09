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
3. **File issues for everything** — every failure gets a GitHub issue.
   Amend existing issues rather than creating duplicates.
4. **Structured output** — fill in the session checklist as you go, write
   machine-readable `summary.json`.
5. **Fail forward** — if one source fails, log it and continue to the next.
   Never abort the entire session for a single source failure.

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
   c. Update checklist with results
   d. Teardown resources
4. Write summary.json
5. Report results
```

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
feeder `app.py` implements `MQTT_AUTH_MODE=entra` (many early feeders do not —
see issue #840).

#### Step 3: Validate Messages (Known Limitation)

**External MQTT subscription to Event Grid MQTT namespaces is blocked** from
non-Azure machines without explicit client certificate registration. RBAC roles
(`EventGrid TopicSpaces Subscriber`) alone are insufficient — the namespace also
requires the subscriber to authenticate with a registered certificate or an Entra
JWT whose subject matches a registered client.

Until the tooling supports creating test client registrations with certificates,
the MQTT E2E validation reports as **BLOCKED** (not PASS, not FAIL).

The topic subscription pattern must be derived from the xreg manifest's topic
space template — not hardcoded. The generated client strips the `ce-` prefix from
CloudEvents attribute names before setting MQTT v5 user properties (bare names:
`type`, `source`, `subject` — not `ce-type`, `ce-source`, `ce-subject`).

**Mark result as FAIL and file/reference issue #840** if the feeder is not
publishing (0 connections in metrics). Mark as **BLOCKED** if feeder is
publishing but external subscription cannot be verified.

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

### Failure Categories
- `no-data` — container/notebook ran but no events arrived
- `dispatch-only` — events in dispatch but not in typed tables (update policy broken)
- `schema-mismatch` — payload doesn't match xreg schema
- `deploy-failed` — container/notebook failed to start
- `timeout` — exceeded wait time
- `map-empty` — map exists but layers return zero rows
- `stale-data` — data exists but is older than expected cadence

### Deduplication

Before creating an issue, search:
```
gh issue list --label e2e-validation --state open --search "[E2E] <source> - <target>"
```
If found: append a comment with the new session ID and error details.
If not found: create a new issue.

## Outputs

Per session:
- `sessions/<ts>/CHECKLIST.md` — filled-in per-source checklist
- `sessions/<ts>/summary.json` — machine-readable pass/fail/skip counts
- `sessions/<ts>/log.txt` — full execution log
- `sessions/<ts>/<source>-azure-result.json` — per-source Azure result
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
The feeder's `app.py` ignores all three env vars. It connects with no credentials
and gets CONNACK rc=5. The managed identity role assignment in the ARM template is
wasted. The fix is in the feeder code (issue #840), not the ARM template.

**Layer 2 — Test validator → EG broker (subscribe path):**
`EventGrid TopicSpaces Subscriber` RBAC alone does **not** authorize external MQTT
connections from non-Azure clients. A registered client certificate or an Entra JWT
whose subject matches a registered `Microsoft.EventGrid/namespaces/clients` entry
is required. The ARM template does not create a `clients` resource, so there is no
registered test identity to authenticate with even if the validator acquired a token.
Connections from local dev or CI return CONNACK rc=5 (Not authorized).

Use Azure Monitor metrics (`Mqtt.Connections`, `Mqtt.SuccessfulPublishedMessages`)
as the only available validation proxy until both layers are fixed. Mark the
external-subscribe step as BLOCKED; mark the feeder-publishing step as FAIL if
metrics show 0 connections.

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

