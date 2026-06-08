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
2. **Immediate teardown** — clean up each source's resources before moving
   to the next. Never leave orphaned resources.
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

#### Step 1: Deploy Infrastructure

```powershell
$rg = "e2e-<source>-eh-<timestamp>"
az group create --name $rg --location <region> --subscription <sub>
az eventhubs namespace create --name <ns> --resource-group $rg --sku Standard
az eventhubs eventhub create --name <source> --namespace-name <ns> --resource-group $rg
```

#### Step 2: Deploy Container

```powershell
az deployment group create --resource-group $rg \
    --template-file azure-template-with-eventhub.json --parameters ...
```

#### Step 3: Validate Messages

Use the Event Hubs SDK (Kafka consumer) to consume from the hub. Validate:
- [ ] At least 1 message received within timeout
- [ ] Each message has CloudEvents Kafka headers (`ce_type`, `ce_source`, `ce_subject`)
- [ ] Kafka key matches the subject template from the xreg manifest
- [ ] Payload validates against the JsonStructure schema in the xreg

#### Step 4: Teardown

```powershell
az group delete --name $rg --yes --no-wait
```

### Variant: ACI + Service Bus (AMQP)

For each source with `feeders/<source>/azure-template-with-servicebus.json`:

#### Step 1: Deploy Infrastructure

```powershell
$rg = "e2e-<source>-sb-<timestamp>"
az group create --name $rg --location <region> --subscription <sub>
az servicebus namespace create --name <ns> --resource-group $rg --sku Standard
```

The ARM template typically creates the topic/queue within the deployment.

#### Step 2: Deploy Container

```powershell
az deployment group create --resource-group $rg \
    --template-file azure-template-with-servicebus.json --parameters ...
```

#### Step 3: Validate Messages

Use the Service Bus SDK to receive from the topic/queue. Validate:
- [ ] At least 1 message received within timeout
- [ ] AMQP application properties contain CloudEvents attributes with `cloudEvents:` prefix
  (per CloudEvents AMQP binding: `cloudEvents:type`, `cloudEvents:source`, `cloudEvents:subject`)
- [ ] Content-type is `application/cloudevents+json` (structured) or `application/json` (binary)
- [ ] Payload validates against the JsonStructure schema in the xreg

#### Step 4: Teardown

```powershell
az group delete --name $rg --yes --no-wait
```

### Variant: ACI + Event Grid MQTT

For each source with `feeders/<source>/azure-template-with-eventgrid-mqtt.json`:

#### Step 1: Deploy Infrastructure

```powershell
$rg = "e2e-<source>-eg-<timestamp>"
az group create --name $rg --location <region> --subscription <sub>
```

The ARM template provisions the Event Grid namespace with MQTT enabled,
client identities, topic spaces, and permission bindings.

#### Step 2: Deploy Container

```powershell
az deployment group create --resource-group $rg \
    --template-file azure-template-with-eventgrid-mqtt.json --parameters ...
```

#### Step 3: Validate Messages

Use a MQTT v5 client to subscribe to the feeder's topic tree. Validate:
- [ ] At least 1 PUBLISH received within timeout
- [ ] MQTT v5 user properties contain CloudEvents attributes with `ce-` prefix
  (per CloudEvents MQTT binding: `ce-type`, `ce-source`, `ce-subject`)
- [ ] Topic path follows the UNS structure declared in the xreg MQTT messagegroup
- [ ] Payload validates against the JsonStructure schema in the xreg

**Authentication**: The ARM template creates a test client registration. The
agent reads the client credentials from the deployment outputs or from the
`read-only-test-client` registration pattern.

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

### Step 6: Cleanup

```powershell
# Delete the notebook
DELETE /v1/workspaces/{wsId}/items/{notebookId}
```

Do NOT delete the KQL database or Map — those are shared/persistent
infrastructure, not per-test ephemeral resources. Only the notebook
(and its scheduled job) are test artifacts.

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

