---
name: fabric-notebook-deployment
description: "Use when adding or modifying a Fabric notebook-hosted feeder. Covers Environment-backed hosting, approved plain-Python OneLake wheels, keyless Topology/Entra Kafka binding, scheduling, fresh-event acceptance and OneLake diagnostics."
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
  Environment with the producer + bridge wheels, unless the maintainer selected
  the plain-Python hosting path described under Learnings. The deploy script handles
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
- **A scheduled run requires fresh reference and telemetry events** correlated
  by event ID, envelope and payload across custom output and typed history.
  Query Kusto with the `https://kusto.kusto.windows.net` audience; old positive
  row counts and a `Completed` job are not delivery proof.
- **Pre-merge static validation is a blocking review criterion.** Every PR
  that adds or modifies a notebook MUST pass
  `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <slug>` with **zero
  blockers** before review. The validator enforces every other non-negotiable
  in this list mechanically (no `asyncio.run`, no `%pip install`, OneLake
  state-file path present, `notebookutils.notebook.exit` on failure path,
  `CONNECTION_STRING` not exposed as a notebook parameter, post-deploy hook
  AST-parses, hook references at least one `$Context.*` key, every
  `$PSScriptRoot` sibling exists, catalog opt-in matches notebook presence).
  The fleet-wide pass is run in CI and on demand via
  `pwsh tools/validate-fabric-deployment.ps1 -OutJson fabric-validation.json`.
- **Subscription ID is not required for notebook deployment.** The deploy
  script (`deploy-feeder-notebook.ps1`) and the underlying
  `deploy-fabric.ps1` authenticate Fabric REST calls via the signed-in user's
  Entra context — there is no Azure resource provisioned in pure notebook
  mode. The ghpages portal's Fabric Notebook deploy form therefore MUST NOT
  render a Subscription ID field, and the Cloud-Shell command MUST NOT
  append `-SubscriptionId`. Subscription is only meaningful for the ACI
  variant (`deploy-fabric-aci.ps1`).
- **Catalog opt-in is mandatory.** Whenever
  `feeders/<slug>/notebook/<slug>-feed.ipynb` exists, BOTH `catalog.json`
  (main) AND `app.js` SOURCES (ghpages branch) MUST set
  `"notebook": true` for that source. A missing flag hides the
  "Deploy to Fabric Notebook" button on the portal even though the
  notebook is wired and deployable. The validator above enforces this
  symmetry.

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
| B/2.5 | Build wheels (`pip wheel --no-deps`) → strip path-deps → create or reuse shared `feeder_env` (override with `-EnvironmentName`) → multipart-upload each wheel to `/staging/libraries` → PATCH `/staging/sparkcompute` (runtime 1.3) → POST `/staging/publish` → poll `publishDetails.state` until `Success` | `-SkipEnvironment` |
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
   `POLLING_INTERVAL`, `RUN_DURATION`, `ONCE_MODE`, `WORKSPACE_ID`.
   No `CONNECTION_STRING`.
3. **CS lookup** — `notebookutils.credentials.getToken('pbi')` → list ES →
   get topology → get source connection. ~15 lines using the Topology API.
   Sets `os.environ['CONNECTION_STRING']`.
4. **Run cell** — opens log file in Lakehouse Files, wraps everything in
   try/except, imports the feeder, runs `feeder.main()` **in a worker
   thread**, and calls `notebookutils.notebook.exit("OK" | "FAIL: …")` at
   the end.

See `references/fabric-notebook-runbook.md` for the exact cell sources.

## Continuous Polling Mode (preferred for real-time sources)

The default deployment model is **continuous polling**: the notebook runs
the feeder's native poll loop for a fixed duration (`RUN_DURATION`,
default 3300 s = 55 min), then exits cleanly. The Fabric scheduler
(set to 60 min) serves only as a restart safety net — it is NOT the
polling cadence.

**Why continuous > single-shot batch:**

- Fabric cold-starts a fresh Python kernel per scheduled invocation
  (~65–70 s overhead: compute allocation + environment activation).
- For a 30 s polling source, a 5-min schedule wastes 20% of wall-clock
  time on startup. A 1-min schedule is ~50% overhead.
- Continuous mode amortizes the cold start across 55 minutes of actual
  work. The effective overhead drops to ~2%.

**Parameters for continuous mode:**

```python
POLLING_INTERVAL = 30    # native source cadence (seconds)
RUN_DURATION     = 3300  # exit after 55 min (scheduler restarts at 60 min)
ONCE_MODE        = False # False = continuous loop
```

**Run cell pattern (continuous):**

```python
sys.argv = ['<source>', 'feed']   # no --once flag
t = threading.Thread(target=_worker, daemon=True)
t.start()
t.join(timeout=RUN_DURATION)      # ← key difference from single-shot
if t.is_alive():
    _log(f'Run duration {RUN_DURATION}s reached; exiting cleanly.')
elif _err:
    raise _err[0]
```

The daemon thread is abandoned on timeout — the feeder's asyncio loop
dies with the thread. No explicit cancellation is needed.

**Schedule configuration (safety net):**

```json
{ "type": "Cron", "interval": 60 }
```

Set to 60 min regardless of source cadence. The scheduler's only job is
to restart the notebook if it exits (timeout, crash, or capacity
reclaim). The actual polling frequency is controlled by
`POLLING_INTERVAL` inside the running notebook.

**When to use single-shot instead:**

- Sources that genuinely run once and exit (one-off data loads, daily
  digests with >1 h cadence). These keep `ONCE_MODE = True` and
  `t.join()` (no timeout).

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

The canonical test workspace for this repo is **`ContosoRealTimeTest`**.
Use it for every pre-merge live deploy so orphan environments
(occasional Fabric 400 UnknownError on env-delete) concentrate in one
place that the maintainers know to sweep.

Query the KQL DB via REST with the `https://kusto.kusto.windows.net`
audience (NOT `kusto.fabric.microsoft.com`):

```powershell
$tok = az account get-access-token --resource https://kusto.kusto.windows.net --query accessToken -o tsv
$body = @{ db='<source>_nb'; csl="['<TableName>'] | count" } | ConvertTo-Json
irm "https://<cluster>.z1.kusto.fabric.microsoft.com/v2/rest/query" -Method Post `
  -Headers @{Authorization="Bearer $tok"; 'Content-Type'='application/json'} -Body $body
```

For non-schematized dispatch/update-policy ingestion, check both:

1. `['_cloudevents_dispatch'] | count` — the raw landing table fed by
   the eventstream.
2. At least one typed table such as `['Measurement'] | count` —
   produced by the update-policy projection over `_cloudevents_dispatch`.

A non-zero dispatch count with a zero typed-table count means the
update policy never fired against the new events. This is exactly the
failure mode the eventstream-topology timing bug produced before
`Wait-EventStreamTopologyReady` was added to `deploy-fabric.ps1`.
Reporting only dispatch counts hides update-policy regressions.
Both counts are diagnostic checks, not sufficient acceptance: require fresh
events from every selected family matched across custom output, dispatch and
typed history. Keep raw receipts and deployment coordinates outside Git and PR
bodies; publish sanitized verdicts.

Pegelonline reference: 785 stations × 1 = 785 reference rows;
telemetry: 736 measurements after one cycle.

## Things That Are Not Allowed

- Hand-editing wheels after `strip-wheel-pathdeps.py` runs.
- Calling `asyncio.run()`, `asyncio.get_event_loop().run_until_complete()`,
  or `loop.run_forever()` directly in a notebook cell.
- Adding a `CONNECTION_STRING` parameter to the notebook — it must be looked
  up at run time via the Topology API.
- Skipping the Lakehouse binding (the log-file diagnostic depends on it).
- Bypassing the selected dependency host by inlining `%pip install`.
- Using the legacy `Get-FabricClusterUrl` / `Get-FabricMwcToken` chain. It
  has been removed from `deploy-fabric.ps1`.

## Learnings

- An approved plain-Python host can load verified producer/core/bridge wheels
  from OneLake without a Spark Environment or cell pip installation; preserve
  OneLake state/logs and bounded worker execution.
  Use the USGS [notebook generator](../../../feeders/usgs-waterdata/create_notebook.py)
  as the example, not a mechanical copy of an Environment-bound notebook.
  Read back the deployed kernel and dependency bindings and verify active wheel
  versions; a host choice does not authorize clearing another notebook's Environment.
- For the USGS `fabric-entra` Kafka path, NotebookUtils accepted the full
  namespace resource URI `https://<service-issued-namespace>/`, while the global
  Event Hubs resource failed in that runtime.
  Reuse [fabric_kafka_config](../../../feeders/usgs-waterdata/usgs_waterdata_core/usgs_waterdata_core/delivery.py):
  explicit opt-in, TLS, no username/password, refreshed OAuth callback, and
  audience/expiry guards; do not infer support for every runtime or protocol.
  Read back the actual publishing principal: delegated-user success is not
  workspace-managed-identity proof.
- Topology connection responses can bundle access keys even when only endpoint
  metadata is needed; discard keys without logging, persisting or using them.
  A credentialless `BootstrapServer` binding still needs explicit TLS before
  the OAuth helper runs; reject disabled TLS rather than silently overriding it.
  Never enable local auth or fetch keys to make a keyless test pass.
- Scheduled acceptance requires an actual scheduled invocation, successful
  OneLake diagnostics and fresh correlated events, not just schedule creation.
  Retain the same checkpoint between manual and scheduled runs, read back cadence
  and expiry, and pause validation schedules after the required invocation.
  Force the notebook's local OneLake state backend rather than inheriting ACI's
  remote-checkpoint environment.

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
