---
name: fabric-notebook-deployment
description: "Use when adding or modifying a Fabric notebook-hosted feeder for a source in this repo. Covers per-source Fabric Environment build (poetry wheel + path-dep stripping), CustomEndpoint connection-string lookup via the public Topology API, Lakehouse + KQL + Environment binding, scheduling, and OneLake-based diagnostics for scheduled runs."
argument-hint: "Describe the source, its workspace, eventhouse and KQL database, and whether a Fabric Environment already exists."
---

# Fabric Notebook Deployment

## When to Use

- Adding a `notebook/<source>-feed.ipynb` to an existing source so it can run
  inside Microsoft Fabric without ACI.
- Wiring the notebook into the `tools/deploy-fabric/deploy-feeder-notebook.ps1`
  orchestrator (per-source Fabric Environment, schedule, Lakehouse binding).
- Debugging a scheduled Fabric notebook run that fails with
  `System_Cancelled_Session_Statements_Failed`.

## Non-Negotiables

- **Never call `asyncio.run()` directly inside a notebook cell.** Fabric
  notebook kernels run inside a live asyncio loop. Every bridge in this repo
  ultimately calls `asyncio.run(...)` inside its `main()`. Run the bridge in
  a worker thread that owns its own loop. See `references/fabric-notebook-runbook.md`
  for the canonical snippet.
- **Never `%pip install` from a notebook cell.** Build a per-source Fabric
  Environment with the producer + bridge wheels. The deploy script handles
  this end-to-end. `%pip install` slows scheduled runs by 60–120 s and breaks
  air-gapped capacities.
- **Never retrieve Event Stream connection strings via the legacy 7-step MWC
  token chain.** Use the public Topology API
  (`GET /v1/workspaces/{ws}/eventstreams/{es}/topology` +
  `/sources/{src}/connection`). One scope, one call per source.
- **Never upload Environment libraries with the JSON `InlineBase64` style.**
  The Environment `staging/libraries` endpoint requires `multipart/form-data`
  via `Invoke-WebRequest -Form`. JSON uploads silently fail to publish.
- **Strip `Requires-Dist: foo @ file:///abs/path` from every wheel before
  upload.** Poetry bakes path-deps into wheel METADATA; pip in the Fabric
  environment cannot resolve them. Use
  `tools/deploy-fabric/strip-wheel-pathdeps.py`.
- **Every notebook must write a structured log to
  `/lakehouse/default/Files/feeder-state/<source>/last-run.log`** AND surface
  failures via `notebookutils.notebook.exit("FAIL: …")`. The Fabric REST APIs
  do **not** expose cell output; OneLake is the only programmatic diagnostic
  channel.
- **A scheduled run is not validated until `KQL count > 0`** in the source's
  reference and telemetry tables, queried via Kusto with the
  `https://kusto.kusto.windows.net` audience.

## Source Folder Additions

```
<source>/
  notebook/
    <source>-feed.ipynb       # parameters, CS lookup, thread-isolated run
```

## Deployment Pipeline (deploy-feeder-notebook.ps1)

Stages in order — none are optional unless explicitly skipped via the listed
flag:

| Stage | What | Skip flag |
|-------|------|-----------|
| A     | Delegates to `deploy-fabric.ps1 -SkipArm` for KQL DB + Event Stream + topology + CS retrieval | — |
| B/1   | Resolve workspace                                                     | — |
| B/2   | Resolve KQL DB                                                        | — |
| B/2.5 | Build wheels (`pip wheel --no-deps`) → strip path-deps → create or reuse `<source>-feeder-env` → multipart-upload each wheel to `/staging/libraries` → PATCH `/staging/sparkcompute` (runtime 1.3) → POST `/staging/publish` → poll `publishDetails.state` until `Success` | `-SkipEnvironment` |
| B/3   | Auto-discover single Lakehouse → patch notebook `metadata.dependencies` with Lakehouse + KQL + Environment + parameters cell | `-DefaultLakehouse` overrides |
| B/4   | Upload notebook                                                       | — |
| B/5a  | POST `/jobs/instances?jobType=RunNotebook` for an immediate run       | `-NoTriggerNow` |
| B/5b  | POST `/jobs/RunNotebook/schedules` with Cron schedule                 | `-NoSchedule`, `-ScheduleIntervalMinutes <5-60>` |

When the publish LRO is slow (≥3 min), do not abort — poll up to 10 min
before declaring failure. Spurious `InternalServerError` from `/kqlDatabases`
GET is common during Fabric warmup; retry the script.

## Notebook Cell Contract

Four cells, in this order:

1. **Markdown intro** — what the notebook does, link to source README.
2. **Parameters** (`parameters` tag) — `EVENTSTREAM_NAME`, `STATE_FILE`,
   `POLLING_INTERVAL`, `ONCE_MODE`, `WORKSPACE_ID`. No `CONNECTION_STRING`.
3. **CS lookup** — `notebookutils.credentials.getToken('pbi')` → list ES →
   get topology → get source connection. ~15 lines using the Topology API.
   Sets `os.environ['CONNECTION_STRING']`.
4. **Run cell** — opens log file in Lakehouse Files, wraps everything in
   try/except, imports the feeder, runs `feeder.main()` **in a worker
   thread**, and calls `notebookutils.notebook.exit("OK" | "FAIL: …")` at
   the end.

See `references/fabric-notebook-runbook.md` for the exact cell sources.

## Diagnosing Failures

A failed `jobInstance` only returns
`errorCode: System_Cancelled_Session_Statements_Failed` and
`message: "System cancelled the Spark session due to statement execution failures"`.
The cell-level error is **not** in the REST response. To diagnose:

1. Read `/lakehouse/default/Files/feeder-state/<source>/last-run.log` via the
   OneLake DFS endpoint with a `https://storage.azure.com` token:
   `GET https://onelake.dfs.fabric.microsoft.com/{ws}/{lakehouseId}/Files/feeder-state/<source>/last-run.log`
2. If the log file does not exist, the run failed before the very first cell
   executed — usually a missing Environment library, a Lakehouse not bound,
   or a malformed notebook payload.
3. Inspect `/v1/workspaces/{ws}/spark/livySessions` for capacity exhaustion
   or `cancellationReason`.

## E2E Verification (mandatory before declaring done)

Query the KQL DB via REST with the `https://kusto.kusto.windows.net`
audience (NOT `kusto.fabric.microsoft.com`):

```powershell
$tok = az account get-access-token --resource https://kusto.kusto.windows.net --query accessToken -o tsv
$body = @{ db='<source>_nb'; csl="['<TableName>'] | count" } | ConvertTo-Json
irm "https://<cluster>.z1.kusto.fabric.microsoft.com/v2/rest/query" -Method Post `
  -Headers @{Authorization="Bearer $tok"; 'Content-Type'='application/json'} -Body $body
```

The deployment is verified when both **reference** and **telemetry** counts
are non-zero. Pegelonline reference: 785 stations × 1 = 785; telemetry: 736
measurements after one cycle.

## Things That Are Not Allowed

- Hand-editing wheels after `strip-wheel-pathdeps.py` runs.
- Calling `asyncio.run()`, `asyncio.get_event_loop().run_until_complete()`,
  or `loop.run_forever()` directly in a notebook cell.
- Adding a `CONNECTION_STRING` parameter to the notebook — it must be looked
  up at run time via the Topology API.
- Skipping the Lakehouse binding (the log-file diagnostic depends on it).
- Bypassing the per-source Fabric Environment by inlining `%pip install`.
- Using the legacy `Get-FabricClusterUrl` / `Get-FabricMwcToken` chain. It
  has been removed from `deploy-fabric.ps1`.

## References

- `references/fabric-notebook-runbook.md` — exact cell sources, deploy
  flag matrix, troubleshooting log.
- Public Topology API:
  <https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/topology/get-eventstream-source-connection>
- Tools:
  - `tools/deploy-fabric/deploy-feeder-notebook.ps1`
  - `tools/deploy-fabric/deploy-fabric.ps1` (Topology API CS lookup)
  - `tools/deploy-fabric/strip-wheel-pathdeps.py`
- Reference implementation: `pegelonline/notebook/pegelonline-feed.ipynb`
