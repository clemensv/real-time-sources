---
name: fabric-notebook-deployment
description: "Use when adding or modifying a Fabric notebook-hosted feeder. Covers native TLS dependencies, Spark Environment bindings, approved plain-Python OneLake wheels, named-source Topology/Entra binding, state preservation, scheduling and fresh output/history acceptance."
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

- **Prefer the workspace managed identity, not SAS.** Verify support for the
  selected source connection, transport and destination, then configure the
  identity with least-privilege roles and the correct token audience. Verify
  which principal actually runs and publishes; a delegated user token from
  notebook credentials does not prove workspace-identity use. Do not retrieve
  access keys by default. If workspace identity is unsupported, record the
  exact limitation and obtain approval for a fallback, with another supported
  Entra flow preferred over SAS. Never enable key authentication silently.
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
- **Job completion and broker acknowledgement are not ingestion proof.**
  Require a successful runtime log and fresh reference/telemetry events
  matched between custom output and typed KQL history. See E2E verification
  below; an old nonzero table count cannot validate a new run.
- **Preserve Spark Environment bindings.** Use the Spark kernel
  (`synapse_pyspark`) for the verified Environment-backed hosting path and
  read back Environment, Lakehouse and child KQL database IDs after upload.
  The current shared deployer forces Python and removes the Environment
  binding; do not use it against migrated schematized items until fixed.
- **Native import success does not prove TLS support.** Proton can compile
  with TLS stubs when OpenSSL development files are absent. Verify
  `from proton import SSL; assert SSL.present()` in a clean compatible Linux
  container and at notebook startup. Record the wheel hash, ABI/platform,
  build inputs and TLS check. Supply a valid CA bundle; never disable TLS
  verification.
- **Select the exact named CustomEndpoint.** Handle list pagination and HTTP
  failures; reject missing or duplicate matches. Do not select the first
  endpoint or expose its connection string as a notebook parameter.
- **Preserve dedupe state.** Never delete it to make validation pass.
  Separately named state for a changed binding requires an explicit replay
  decision; retain the previous state.
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

## Legacy deployment pipeline (deploy-feeder-notebook.ps1)

The sequence below describes existing tooling, not a verified schematized
deployment recipe. Its ingestion setup and kernel/Environment rewriting
must be corrected before reuse for migrated sources. The isolated Pegelonline
pilot established the requirements below; its implementation and acceptance
receipts are separate work and are not included with this guidance.

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

Upload public dependencies as `environment.yml` and custom wheels through
multipart library upload; `requirements.txt` was rejected by the tested API.
Publish and wait for `publishDetails.state == Success` with a finite deadline,
then read back the definition. A publish acknowledgement is not readiness.

For asynchronous operations, honor `Retry-After` and reconcile the accepted
operation through documented public operation-state/result APIs. A regional
Location or response-parsing failure is not permission to repeat a mutation.
For an accepted notebook run, reconcile its job ID before considering retry.
Retry safe reads with bounded backoff; do not rerun the whole deploy script
after an ambiguous mutation.

## Notebook Cell Contract

Four cells, in this order:

1. **Markdown intro** — what the notebook does, link to source README.
2. **Parameters** (`parameters` tag) — `EVENTSTREAM_NAME`, `STATE_FILE`,
   `POLLING_INTERVAL`, `RUN_DURATION`, `ONCE_MODE`, `WORKSPACE_ID`.
   No `CONNECTION_STRING`.
3. **Binding/authentication lookup** — resolve the exact Eventstream and named
   source through paginated public APIs. Prefer workspace-identity token
   authentication. Use source access keys only for an approved fallback.
   Check HTTP status and uniqueness; keep credentials in memory and out of logs.
4. **Run cell** — opens log file in Lakehouse Files, wraps everything in
   try/except, imports the feeder, runs it **in a worker thread**, and records
   exceptions and logged publish errors. Call
   `notebookutils.notebook.exit("OK" | "FAIL: ...")` outside that handler so
   notebook exit control flow is not swallowed. A one-shot timeout is failure.

See `references/fabric-notebook-runbook.md` for the exact cell sources.

## Run mode and scheduling

Choose bounded one-shot polling or continuous polling explicitly for the
source and approved operating window. Continuous polling can amortize compute
startup, but requires cooperative shutdown, producer flush/close and a verified
worker exit. A daemon thread remains alive while the kernel runs;
`join(timeout=...)` does not stop it. Never report timeout as clean completion.
If the worker cannot stop, report failure and stop the job/session before
reusing its state or starting another worker.

For one-shot runs, use `ONCE_MODE=True` and a finite `RUN_DURATION`. Obtain
approval for schedule interval and expiry, read them back and observe an actual
scheduled run after manual acceptance. Avoid overlapping writers to the same
state file; reconcile any still-running invocation before restarting.
Measure whole-job duration rather than assuming a fixed startup allowance.
In the 2026-11-16 pilot, worker execution took about 38 seconds but the entire
scheduled job took about 266 seconds. This is an observation, not a sizing
guarantee. Schedule interval does not establish data freshness.

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
$tok = az_m account get-access-token --resource https://kusto.kusto.windows.net --query accessToken -o tsv
$body = @{ db='<source>_nb'; csl="['<TableName>'] | count" } | ConvertTo-Json
irm "https://<cluster>.z1.kusto.fabric.microsoft.com/v1/rest/query" -Method Post `
  -Headers @{Authorization="Bearer $tok"; 'Content-Type'='application/json'} -Body $body
```

For schematized ingestion, Eventstream owns base-table creation. Supply no
base-table DDL, ingestion mappings or dispatch update policies. Discover actual
table names/types and registered version selections before querying. Preserve
legacy KQL artifacts for non-Fabric users; legacy dispatch counts are not a
schematized acceptance criterion.

After source readiness, capture the run/job ID and time boundary, read its
OneLake log, and match fresh events from every selected family between custom
output and typed history. Compare IDs, payloads, source, subject and time;
verify output `dataschema` against exact registered version URIs. Record any
documented storage normalization, such as nullable strings becoming empty
strings. Inspect runtime validation logs when broker sends succeed but storage
does not advance. Old counts and synthetic events do not prove acceptance.

For non-schematized dispatch/update-policy ingestion, check the dispatch table
and each selected typed table separately:

1. `['_cloudevents_dispatch'] | count`
2. `['<ActualTypedTableName>'] | count`

A non-zero dispatch count with a zero typed-table count means the
update policy never fired against the new events. This is exactly the
failure mode the eventstream-topology timing bug produced before
`Wait-EventStreamTopologyReady` was added to `deploy-fabric.ps1`.
Reporting only dispatch counts hides update-policy regressions.
Both counts are diagnostic checks, not sufficient acceptance: require fresh
events from every selected family matched across custom output, dispatch and
typed history. Keep raw receipts and deployment coordinates outside Git and PR
bodies; publish sanitized verdicts.

Use the response shape of the selected Kusto endpoint: the tested v1 query
returns Tables/Rows; v2 can return frames. Do not parse either as the other.
Persist a non-secret receipt outside Git and PR bodies with item IDs,
schema/version selections, package and definition hashes, run-specific counts
and schedule readback.

The generated metadata gap is tracked in
[xregistry/codegen#693](https://github.com/xregistry/codegen/issues/693).
The pilot's producer subclass is temporary, not a fleet pattern. Once fixed,
regenerate through the enforced generator and remove the boundary override
only after tests and new output/history acceptance pass. Do not hand-edit
generated producers or assume the issue's implementation has shipped.

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
- Verified schematized notebook: `feeders/pegelonline/notebook/pegelonline-feed.ipynb`
