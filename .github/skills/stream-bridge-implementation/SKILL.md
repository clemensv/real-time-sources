---
name: stream-bridge-implementation
description: "Use when implementing the runtime bridge (feeder) for a source in this repo. Covers pollers, websocket or MQTT clients, raw TCP decoders, family-aware normalization, generated producer wiring, state and dedupe logic, source-local testing, mandatory KQL schema generation and KQL Optimizer review, mandatory expert review of the contract and generated schemas, and the Fabric notebook hosting option for poll-based sources (both new sources and retrofits of already-shipped sources)."
argument-hint: "Describe the transport, auth, polling or reconnect behavior, resume state needs, and the event families the runtime must emit. For a notebook-only retrofit, pass the source id and the literal 'retrofit'."
---

# Stream Bridge Implementation

This is the **main skill for building feeders** in this repo. It covers
both the runtime bridge implementation and the Fabric notebook hosting
option that poll-based feeders must ship alongside the container. The
notebook flow used to live in a separate `notebook-feeder-retrofit`
skill; it has been folded in here so a single skill owns the whole
feeder.

## When to Use

- Implement a new runtime bridge after the xreg contract is clear.
- Refactor a runtime to align with regenerated producer output.
- Add state, dedupe, reconnect, or emit-order logic.
- Add Fabric notebook hosting to a brand-new poll-based source
  (concurrent with bridge implementation).
- **Retrofit** an already-shipped poll-based source with a Fabric
  notebook (the dedicated retrofit workflow lives in
  [Fabric Notebook Hosting → Retrofit Workflow](#retrofit-workflow-for-already-shipped-sources)
  below). When dispatching a fleet of retrofit agents in parallel,
  invoke this skill once per source and scope each agent to the
  retrofit workflow.

## Inputs

- transport type and auth model
- poll or reconnect behavior
- state and dedupe requirements
- generated producer methods and placeholder arguments
- reference data endpoints and refresh cadence

## Non-Negotiables

- The runtime is not allowed to paper over a sloppy contract.
- If generated producer methods or upstream subtype signals imply more event families than the bridge emits, stop and fix the contract first.
- Do not normalize semantically different upstream shapes into one generic dict or class just because the transport loop is shared.
- Preserve the family-specific fields and discriminators that justified the contract split in the first place.
- Do not patch, rewrite, or vendor modified copies of `xrcg`-generated producer or data-class code to make the runtime work; import and use the generated packages as emitted.
- The bridge must emit Kafka keys, CloudEvent subjects, and payload shapes that satisfy the checked-in xreg contract, including nullability behavior.
- **HTTP pollers must use bounded retry handling for transient upstream failures.** A long-running `requests` poller is not allowed to rely on a bare `requests.Session()` with no `HTTPAdapter`/`Retry` policy for connect resets, read timeouts, 429s, and 5xx responses.
- **State and dedupe must advance only after Kafka delivery succeeds.** If the bridge batches `send_*` calls with `flush_producer=False`, it must treat `producer.flush(timeout=...)` returning a non-zero remainder as a failed poll and leave dedupe state, resume cursors, `last_seen` timestamps, and persisted checkpoints untouched. Do not mark rows, incidents, or event IDs as seen before delivery is durable.
- **The bridge must emit reference data as events, not just telemetry.** If the xreg contract defines reference event types (station metadata, sensor catalogs, zone definitions, route tables, task type catalogs), the bridge must fetch that data via REST at startup and emit it as CloudEvents before or alongside the telemetry stream. Reference data should be re-fetched periodically (typically every few hours or daily, depending on the source) so downstream consumers can maintain temporally consistent views. Reference data goes to the same Kafka topic as the telemetry it contextualizes, using the same key model. Repo analogs: `pegelonline` (stations at startup), `usgs-iv` (sites refreshed weekly), `chmi-hydro` (stations before observations), `noaa-ndbc` (buoy stations). See: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events
- **A failed reference refresh must not discard a still-usable cached catalog.** Station, site, community, route, and timeseries metadata should be refreshed into a new snapshot and swapped in only after success. If refresh fails and a prior cache exists, keep polling with the cached reference data instead of turning a transient metadata outage into a full bridge outage.
- **Multi-endpoint pollers must isolate failures to the failing slice whenever possible.** One bad dataset, station batch, endpoint, or reference-detail lookup should not abort the rest of the cycle if the remaining slices can still emit valid events.
- Runtime work for a new source is not complete until the relevant repo-level Docker E2E test passes when the source is meant to participate in the shared container test suite.
- If Docker E2E reports key, subject, or JsonStructure schema failures, treat that as contract or runtime drift and fix the source instead of weakening the test.
- When Docker E2E evidence is needed for manual verification or debugging, the harness must support an explicit opt-in parameter that writes consumed Kafka messages and container logs to disk.

## Procedure

1. Choose the runtime pattern that matches the source: poller, websocket, MQTT, or raw TCP.
2. Structure the bridge using the runtime patterns in [runtime checklist](references/runtime-checklist.md).
3. Parse source configuration and Kafka configuration from CLI args and environment variables.
4. **Emit reference data first.** If the contract defines reference event types, fetch the metadata via REST at startup and emit it as CloudEvents before entering the telemetry loop. Track when reference data was last emitted and re-fetch periodically (interval depends on the source's metadata volatility). Reference events use the same producer topic and key model as the related telemetry.
5. **For HTTP pollers, create a retrying session and design partial-failure behavior up front.** Mount bounded retries for transient GET failures, decide what constitutes one isolated slice of work (dataset, station batch, endpoint, family), and define the cached reference snapshot that can survive a failed refresh.
6. Normalize upstream payloads into the correct generated data classes per family and pass subject or key placeholders explicitly, matching the xreg-declared shape and nullability rules, while consuming the generated producer packages unchanged.
    - **Map upstream field names to English schema field names.** If the upstream JSON uses `id`, `uuid`, or non-English names (e.g. `id_stacji`), remap to the schema name (e.g. `station_id`) before constructing data classes.
    - **Parse datetime strings with `datetime.datetime.fromisoformat()`.** Do not pass raw strings to datetime-typed fields.
    - **Never use `key_mapper` lambdas.** Pass key template values as positional arguments to the generated producer send methods. Custom key mappers bypass contract validation and cause E2E key-format failures.
    - **When xrcg emits multiple `*EventProducer` classes, instantiate all of them.** Message groups generate separate producer classes. A bridge that imports or constructs only the first producer class and then calls `send_*` methods owned by other message groups will fail with `AttributeError` at runtime. Repo analogs: `dwd`, `entsoe`, `vatsim`, `wsdot`.
7. Add state, dedupe, reconnect, and emit-order behavior where the source requires it without erasing family-specific meaning.
    - **Do not mutate dedupe or resume state before a successful flush.** Collect candidate state updates during the batch, flush Kafka with an explicit timeout, verify the flush remainder is zero, and only then commit in-memory and persisted state.
    - **Build refreshed reference catalogs separately and swap them in only after success.** If the refresh fails and an older cache exists, keep using the older cache and continue polling unaffected telemetry slices.
    - **Catch upstream failures at the smallest practical boundary.** Skip the failing dataset, endpoint, or batch, log it, and continue with the rest of the cycle whenever the remaining work is still valid.
8. Add unit and integration tests, and keep Docker compatibility in mind if the source should join the repo-wide container tests.
    - **When the bridge batches sends with `flush_producer=False`, add a flush-failure unit test.** Mock `producer.flush(timeout=...)` (or `producer.producer.flush(timeout=...)`) to return a non-zero remainder and assert that dedupe state, `last_seen` markers, resume cursors, and persisted checkpoints do not advance. If the bridge retries on the next poll, assert the same records are still eligible to send.
    - **For HTTP pollers, add two resilience tests, not one vague one.** First, simulate a timeout or connection reset during reference refresh and assert that the old cached station, community, site, route, or timeseries catalog remains in use instead of being cleared. Second, simulate one failed dataset, endpoint, or station batch inside a multi-slice poll and assert that only the failing slice is skipped while unaffected slices still emit.
    - **For multi-group sources, add a one-cycle feed test that exercises every emitted family.** Mock upstream responses for each family, use fake producer classes per generated message group, and assert the runtime emits at least one event through each expected `send_*` path. This catches bridges that import or instantiate only one generated producer class and then call methods owned by another class.
9. **Update Docker E2E test to validate both reference and telemetry event types.** Use `reference_types` and `telemetry_types` parameters in `_run_kafka_flow_test` to verify both categories are emitted.
10. Run the relevant Docker E2E test and treat failures there as unfinished implementation work, not optional follow-up.
11. **Generate the mandatory KQL DDL** for the source as described in [Mandatory KQL Schema](#mandatory-kql-schema-not-optional) below. Run `tools/generate-kql-from-xreg.ps1` to produce `<source>/kql/<source>.kql` from the xreg manifest, commit it, and ensure the source's `catalog.json` entry has a `kql` reference. The KQL script defines the `_cloudevents_dispatch` ingestion table, per-event-type typed tables, JSON mappings, materialized views, and update policies that fan out events from the dispatch table into typed tables. Without it, deployed KQL databases land everything in a single untyped `_cloudevents_dispatch` and downstream queries / Eventhouse Maps / Activator rules cannot work.
12. **If the source is a poller, add Fabric notebook hosting** as described in [Fabric Notebook Hosting](#fabric-notebook-hosting-poll-based-feeders) below: author `<source>/notebook/<source>-feed.ipynb` from the canonical pegelonline template, set `notebook: true` in `catalog.json`, and run the notebook validation block. Streaming bridges skip this step.
13. **Dispatch the mandatory expert review** described in [Mandatory Expert Review](#mandatory-expert-review-gate-before-declaring-the-feeder-done) below. Do not declare the feeder done until the xRegistry Expert, JSON Structure Expert, Avro Schema Expert, **and KQL Optimizer** have each signed off.

## Outputs

- a runtime bridge aligned with the xreg contract
- reference data emission at startup (and periodic refresh) for sources that define reference types
- consistent producer calls with explicit placeholder values
- source-local tests that cover parsing, state, and emission behavior
- a passing repo-level Docker E2E test when the source participates in the shared container suite
- a generated, committed `<source>/kql/<source>.kql` script with `_cloudevents_dispatch` + per-event-type typed tables + JSON mappings + update policies, reviewed by the KQL Optimizer
- a Fabric notebook (`<source>/notebook/<source>-feed.ipynb`) and `catalog.json` `notebook: true` flag for every poll-based source
- a clean expert-review pass from the xRegistry, JSON Structure, Avro Schema, and KQL Optimizer reviewers before the feeder is declared done

## Mandatory KQL Schema (not optional)

Every source MUST ship a `<source>/kql/<source>.kql` script that is
applied to the source's Eventhouse KQL database at deploy time. The
script is generated from the xreg manifest; you do not hand-write it.

### Why this is mandatory

The Fabric `deploy-fabric.ps1` and `deploy-feeder-notebook.ps1`
deployers look up `<source>/kql/<source>.kql` on the `main` branch
and apply it via `.execute database script <|` when present. When it
is absent, both deployers print **"No KQL script — database schema
step will be skipped"** and the database is left with only the
auto-provisioned `_cloudevents_dispatch` table. Downstream
consumers — Fabric Maps tied to per-type Kusto data sources, Activator
rules, materialized `*Latest` views, KQL-backed dashboards, time
filters on typed columns — all fail because there are no typed tables
to query. The bridge silently appears to "work" while the data is
unusable for the actual analytical scenarios the source exists for.

A source without a KQL script is **not done**, regardless of whether
Docker E2E passes.

### How to generate it

Run the canonical generator:

```powershell
cd <source>
New-Item -ItemType Directory -Force -Path kql | Out-Null
..\tools\generate-kql-from-xreg.ps1 `
    -XregPath xreg\<source>.xreg.json `
    -OutputPath kql\<source>.kql `
    -Qualified `
    -Namespace <PascalCase.Namespace>
```

**Always pass both `-Qualified` and `-Namespace`.** They are not optional.

- `-Qualified` forwards `--qualified-table-names` to avrotize `s2k`/`a2k`,
  producing fully-qualified table, mapping, and materialized-view names of
  the form `['<namespace>.<TypeName>']` so the same Eventhouse can host
  multiple sources without collision.
- `-Namespace <PascalCase.Namespace>` forwards `--namespace` to avrotize
  so the emitted KQL tables AND the update-policy `where type == '...'`
  filter use the **exact same token the bridge emits as the CloudEvents
  `type` attribute**. Without this, avrotize derives the namespace from
  the JsonStructure schema's `$root`/`namespace`, which is often lowercase
  (`jp.tepco.denkiyoho.SupplyCapacity`) while bridges emit PascalCase
  (`JP.TEPCO.Denkiyoho.SupplyCapacity`) — the case mismatch silently
  breaks every update policy and **no typed table ever receives a row**.

Choose the `-Namespace` value to **match the `envelopemetadata.type.value`
prefix** in the xreg manifest. For sources with a single messagegroup,
this is the messagegroup name (e.g., `JP.JMA.Amedas`, `DE.DWD.Pollenflug`,
`JP.TEPCO.Denkiyoho`). For sources with multiple messagegroups in
different namespaces (e.g., `jma-bosai-warning` has both `JP.JMA.Warning`
and `JP.JMA.Tsunami`), omit `-Namespace` and rely on the generator's
per-schema rewrite — verify the resulting `type ==` literals match the
bridge's emitted types before deploying.

Also commit a thin `kql/create-kql-script.ps1` wrapper modeled on
`dwd/kql/create-kql-script.ps1` so regeneration after xreg changes is
a one-liner. The wrapper must pass `-Qualified` and (where applicable)
`-Namespace`.

### What the generated script contains

For each schema in the xreg manifest the generator emits, in order:

1. `.create-merge table [_cloudevents_dispatch]` — the dispatch
   ingestion table (specversion, type, source, id, time, subject,
   datacontenttype, dataschema, data) with a JSON mapping that pulls
   `$.specversion` … `$.data`. Idempotent across multiple `.kql`
   scripts in the same DB.
2. `.create-merge table ['<ns>.<Type>']` — one typed table per
   message type with Kusto columns derived from the JsonStructure
   schema fields plus the envelope columns `___type`, `___source`,
   `___id`, `___time`, `___subject`.
3. JSON mappings: a `..._json_flat` mapping for direct ingestion of
   the data payload, and a `..._json_ce_structured` mapping for
   CloudEvents-structured ingestion that pulls fields from `$.data.*`.
4. Materialized `*Latest` views for reference event types
   (`arg_max(___time, *) by ___type, ___source, ___subject`).
5. Update policy on each typed table that filters
   `_cloudevents_dispatch` by `specversion == '1.0' and type ==
   '<Type>'`, projects every field with the right type coercion, and
   propagates the envelope columns. `IsTransactional = false`,
   `PropagateIngestionProperties = true`.

### Applying it to existing deployed databases

If a source was deployed before the KQL script existed, apply the
script post-hoc:

```powershell
# Get the Eventhouse cluster URI from the Fabric API:
$tok = az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv
$eh  = irm "https://api.fabric.microsoft.com/v1/workspaces/$WsId/eventhouses/$EhId" -Headers @{Authorization="Bearer $tok"}
$cluster = $eh.properties.queryServiceUri

# Apply the .kql script using the dispatch-style mgmt call:
$kustoTok = az account get-access-token --resource https://kusto.kusto.windows.net --query accessToken -o tsv
$csl  = ".execute database script <|`n" + (Get-Content "<source>/kql/<source>.kql" -Raw)
$body = @{ db = "<source_db>"; csl = $csl } | ConvertTo-Json -Compress
irm "$cluster/v1/rest/mgmt" -Method POST -Headers @{
    Authorization  = "Bearer $kustoTok"
    "Content-Type" = "application/json"
} -Body $body
```

The script is idempotent thanks to `.create-merge` and
`.create-or-alter` — running it twice does no harm.

### catalog.json

After generating the script, add a `kql` reference to the source's
`catalog.json` entry so the gh-pages portal surfaces the schema:

```jsonc
{
  "source": "<source>",
  ...
  "kql": "<source>/kql/<source>.kql",
  ...
}
```

Keep the existing key order. If a `notebook` flag is set, the `kql`
key precedes it.

## Mandatory Expert Review (gate before declaring the feeder done)

Before opening or merging a PR that ships a new bridge or that changes
the contract a bridge emits against, **dispatch a review by all three
of the following expert agents** and act on every finding they raise:

1. **xRegistry Expert** — reviews `xreg/<source>.xreg.json`. Validates
   message group layout, CloudEvents type / source / subject modeling,
   Kafka endpoint configuration, key templates aligning with subject
   templates, reference-data event types appearing alongside telemetry
   in the same message group, and the manifest's overall compliance
   with xRegistry spec. Reviewer must read the actual checked-in
   manifest, not paraphrased prose.
2. **JSON Structure Expert** — reviews every embedded JsonStructure
   schema in the manifest. Confirms exhaustive schema-level and
   field-level descriptions grounded in upstream docs; correct use of
   native extended primitives (`datetime`, `date`, `time`, `duration`,
   `uri`, `uuid`, `binary`, `jsonpointer`) instead of `string + format`
   where a native type exists; correct nullability via type unions
   (no `anyOf`); `$ref` nested inside `type`; units/symbols on
   measured values; `altnames` for upstream JSON key names;
   `altenums`/`descriptions` for documented labels; validation
   keywords for ranges/formats/patterns. Every schema must pass
   `jstruct check` and the reviewer must confirm it.
3. **Avro Schema Expert** — reviews the Avro shape that `xrcg`
   generates from the JsonStructure schemas (or that the manifest
   declares directly when a source ships an avro group). Validates
   that the Avro schema is round-trip-stable through the Kafka
   producer, that nullable fields in the JsonStructure manifest
   produce `["null", T]` unions in Avro and vice versa, that field
   names are valid Avro identifiers (no hyphens, no reserved words),
   that enum symbols are valid, that record namespaces do not
   collide, and that the generated `_data` and `_kafka_producer`
   sub-packages are byte-stable across regenerations (a noisy diff
   on regeneration usually points at a contract problem the Avro
   expert should flag).
4. **KQL Optimizer** — reviews `<source>/kql/<source>.kql` and any
   handwritten KQL functions or update policies shipped alongside it.
   Validates that the `_cloudevents_dispatch` ingestion table and
   mapping match the CloudEvents structured envelope; that one typed
   table exists per CloudEvent type with the correct column types
   derived from the JsonStructure schema; that JSON ingestion mappings
   include both flat and CE-structured variants where the source
   ingests via either path; that update policies fan out from
   `_cloudevents_dispatch` filtered on `specversion == '1.0' and type
   == '<TYPE>'`, project every schema field with the right Kusto type
   coercion (`toreal`, `toint`, `todatetime`, `tostring`, `todynamic`,
   `tobool`), and propagate the CloudEvents envelope columns
   (`___type`, `___source`, `___id`, `___time`, `___subject`); that
   materialized `*Latest` views are defined for reference event types
   (SCD-1 via `arg_max(___time, *)` on the natural key); that table,
   mapping, and view names use the qualified-namespace form
   (`['<lowered.namespace>.<TypeName>']`) so multiple sources can
   share an Eventhouse without collisions; and that update-policy
   queries are efficient (no unnecessary `mv-expand`, no
   `tostring(dynamic)` round-trips when the source column is already
   typed). Reviewer must read the actual generated `.kql` and the
   xreg manifest, not paraphrased prose.

### How to dispatch the review

Use the `task` tool with `agent_type` set to the named custom agent
("xRegistry Expert", "JSON Structure Expert", "Avro Schema Expert",
"KQL Optimizer"). Provide each agent with:

- The path(s) to the xreg manifest, generated producer, and (for the
  KQL Optimizer) the generated `<source>/kql/<source>.kql`.
- A short summary of the upstream source, the event families, and
  the bridge's transport pattern.
- A direct prompt to inspect the files in the working tree, not to
  rely on hearsay or the prose summary alone.
- A request for an explicit go/no-go verdict plus a list of any
  blocking findings.

These reviews are **mandatory**, not advisory. A `nit:` from any of
the four reviewers can be deferred; a blocking finding must be fixed
before the PR is merged. Record the verdict from each reviewer in the
PR body so the maintainer can see all three signed off.

### When the review must be re-run

Re-run the relevant expert reviews whenever:

- A schema in the xreg manifest gains, loses, or renames a field.
- A subject or key template changes.
- A new message group or event family is added.
- The producer is regenerated against a new `xrcg` version.
- A Docker E2E test surfaces a schema, key, or subject mismatch that
  the bridge is being changed to accommodate (the reviewer must
  confirm the fix is in the contract, not just papered over in the
  bridge).

A bridge change that does not touch the contract (e.g., adding a
retry policy or restructuring an internal helper) does not require
re-review.

## Fabric Notebook Hosting (poll-based feeders)

Every poll-based feeder ships a Fabric notebook hosting option
alongside the container. The notebook is **not** an alternative to
the Docker bridge — it is a second deployment surface that runs the
same bridge code on a Fabric schedule. Streaming bridges
(WebSocket / MQTT / raw TCP / SSE firehose) are out of scope for the
notebook flow and must skip this artifact.

The deployment pipeline this notebook plugs into is documented in
[`fabric-notebook-deployment`](../fabric-notebook-deployment/SKILL.md).
This skill owns the *authoring* of the notebook; the fabric skill
owns the deployment plumbing.

### Eligibility (gate before adding a notebook)

A source qualifies for notebook hosting if **all** of the following
are true:

1. `<SOURCE>/` exists and contains `<SOURCE>/pyproject.toml`,
   `xreg/<SOURCE>.xreg.json`, and a bridge module exposing
   `def main()`.
2. The bridge supports **single-cycle execution** — either via a
   `--once` CLI flag (preferred) or via an `ONCE_MODE` environment
   variable that exits after one polling cycle. For new sources,
   build `--once` in from day one. For retrofits, verify by grepping
   the bridge module for `--once|once_mode|ONCE_MODE`.
3. The bridge is **poll-based**, not a long-lived stream. Heuristic:
   the bridge calls `time.sleep`, `asyncio.sleep`, or has a
   `POLLING_INTERVAL` env var, and does **not** open a persistent
   socket.
4. The source has (or will have) a Docker E2E test that passes on
   `main`. Without that, the bridge's contract is unverified and the
   notebook will inherit the same drift.
5. `<SOURCE>/notebook/<SOURCE>-feed.ipynb` does **not** already exist
   (retrofit-only check; new sources create it as part of bootstrap).

### Authoring the notebook

The canonical template is
`pegelonline/notebook/pegelonline-feed.ipynb`. **Copy verbatim**, then
perform the substitutions in
[`references/notebook-substitution-table.md`](references/notebook-substitution-table.md).
The substitutions are exact and mechanical; do not paraphrase.

Critical substitutions:

| From (pegelonline) | To |
|---|---|
| `from pegelonline import pegelonline as feeder` | `from <PKG> import <MODULE> as feeder` |
| `sys.argv = ['pegelonline', 'feed', '--once']` | `sys.argv = [<bridge argv-0>, <subcommand>, '--once']` |
| `sys.argv = ['pegelonline', 'feed']` (else branch) | same as above without `--once` |
| `/lakehouse/default/Files/feeder-state/pegelonline/` | `/lakehouse/default/Files/feeder-state/<SOURCE>/` |
| `Pegelonline Feeder (Fabric Notebook)` (title) | `<Display Name> Feeder (Fabric Notebook)` |
| `pegelonline-ingest` (default `EVENTSTREAM_NAME`) | `<SOURCE>-ingest` (the deploy script overwrites this) |
| Markdown copy describing the source | one-paragraph adaptation from `<SOURCE>/README.md` |

Resolve `<PKG>`, `<MODULE>`, `<bridge argv-0>`, and `<subcommand>` by
inspecting `<SOURCE>/pyproject.toml` (`[tool.poetry.scripts]` or the
package layout) and the bridge module's `argparse` setup. **Do not
guess.** If the bridge has no CLI subcommand (calls `main()` with no
args), drop the subcommand element and use
`sys.argv = ['<SOURCE>', '--once']` instead.

Do **not** change the four-cell structure, the CS-lookup cell, the
worker-thread run cell, or the OneLake log path layout. Those are
load-bearing — see
[`fabric-notebook-deployment`](../fabric-notebook-deployment/SKILL.md).

### Three notebook-only invariants (load-bearing)

These rules come from the Fabric kernel and the deploy pipeline; they
are non-negotiable:

- **No `asyncio.run()` in cells.** The Fabric kernel owns the loop;
  run `feeder.main()` in a worker thread.
- **No `%pip install` in cells.** Wheels live in the per-source
  Environment; the deploy script builds and uploads them.
- **OneLake is the only diagnostic channel** for scheduled runs. The
  notebook must log to
  `/lakehouse/default/Files/feeder-state/<source>/last-run.log` and
  call `notebookutils.notebook.exit("FAIL: …")` on error — Fabric
  REST does not expose cell output.

### Catalog flag

Edit `catalog.json` to add `"notebook": true` to the `<SOURCE>` entry.
Keep the existing key order; insert `notebook` after `kql`. If the
entry does not exist, the source is not published in the portal and
should not have a notebook button — fix that first or abort.

### Notebook validation (run before opening a PR)

```powershell
# Notebook JSON well-formed
python -c "import json; json.load(open('$SOURCE/notebook/$SOURCE-feed.ipynb'))"

# Bridge unit tests still pass
cd $SOURCE; python -m pytest tests/ -x --no-header -q; cd ..

# If you added --once, run the new unit test specifically:
cd $SOURCE; python -m pytest tests/test_once_mode.py -v; cd ..

# Notebook params cell actually contains the placeholders the deploy script patches
$nb = Get-Content "$SOURCE/notebook/$SOURCE-feed.ipynb" -Raw
foreach ($k in 'EVENTSTREAM_NAME','STATE_FILE','POLLING_INTERVAL','ONCE_MODE','WORKSPACE_ID') {
    if ($nb -notmatch "(?m)^\s*$k\s*=") { throw "Missing placeholder: $k" }
}

# Notebook does NOT contain forbidden patterns
foreach ($bad in 'asyncio\.run\(','%pip install','CONNECTION_STRING\s*=\s*"','primaryConnectionString.*=') {
    if ($nb -match $bad) { throw "Forbidden pattern present: $bad" }
}
```

### Documentation touch

Add a one-sentence "Fabric notebook hosting" bullet to
`<SOURCE>/README.md` linking to
`tools/deploy-fabric/deploy-feeder-notebook.ps1`. Do **not** create a
separate doc, and do **not** edit `EVENTS.md` or `CONTAINER.md` just
for the notebook addition.

### Retrofit workflow (for already-shipped sources)

When the bridge already exists on `main` and only needs notebook
hosting added (the case the old `notebook-feeder-retrofit` skill
covered), follow this scoped workflow. It is designed to be
dispatched in parallel — one agent per source — by an orchestrator.

**Single-source scope.** One agent processes one source. Do not loop
over sources in a single agent. Bundling multiple sources into one
PR is not allowed.

1. **Branch + folder**

   ```powershell
   git checkout main
   git pull --ff-only
   git checkout -b notebook-retrofit-$SOURCE
   New-Item -ItemType Directory -Force -Path "$SOURCE/notebook" | Out-Null
   ```

2. **Run the eligibility gate.** If any check fails, write a
   one-line skip reason to `tmp/notebook-retrofit-skipped.log`
   (append) and call `task_complete` with the reason. Do **not** open
   a PR. The discovery helper at
   [`references/notebook-eligibility-discovery.ps1`](references/notebook-eligibility-discovery.ps1)
   prints the eligible-source set for the orchestrator.

3. **Add `--once` if missing.** If the eligibility gate fails on the
   single-cycle requirement but the bridge is clearly a poller, you
   may add a `--once` flag to the argparse setup and a single-cycle
   exit branch in the polling loop, modeled after
   `pegelonline/pegelonline/pegelonline.py`. Add a unit test that
   asserts `--once` causes `main()` to return after exactly one cycle
   (mock the upstream HTTP). If the bridge is not written with a
   clean polling loop you can interrupt, abort instead.

4. **Author the notebook and flip the catalog flag** per the
   sections above.

5. **Run the notebook validation block** above; fix and re-run on any
   failure.

6. **Commit and open the PR.**

   ```powershell
   git add "$SOURCE/notebook/" "$SOURCE/README.md" catalog.json
   # include bridge + test changes only if you added --once
   git commit -m "feat($SOURCE): Fabric notebook hosting option

   Adds notebook/$SOURCE-feed.ipynb following the pegelonline pattern.
   Flips catalog.json notebook flag so the gh-pages portal exposes the
   Fabric Notebook deploy button.

   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   git push -u origin notebook-retrofit-$SOURCE
   gh pr create --base main --title "feat($SOURCE): Fabric notebook hosting option" `
     --body "Retrofit by stream-bridge-implementation skill (notebook hosting section). Validated locally: notebook JSON ok, bridge tests pass, parameters cell complete, no forbidden patterns. The wheel-bundle workflow (.github/workflows/publish-notebook-wheels.yml) will pick up this source on next push to main and publish wheels to the notebook-wheels release."
   ```

7. **Do not run a live Fabric deployment from the retrofit agent.**
   The wheel-publish workflow runs on PR merge and the portal
   exposes the button once `update-ghpages-catalog.yml` syncs the
   flag. End-to-end Fabric validation is performed manually by the
   maintainer (or by a separate verification agent) once the PR is
   merged. Each Fabric deployment consumes capacity time, creates
   workspaces/environments/notebooks, and competes with other agents
   for the shared workspace; serial verification is cheaper than
   parallel deployment.

### Optional: Post-Deploy Hook

If the source needs **additional Fabric wiring** beyond the generic
deployer's 6 steps (e.g. wiring Map layers, importing a Dashboard,
attaching an Environment), drop a `<SOURCE>/fabric/post-deploy.ps1`
script. Both `deploy-fabric.ps1` and `deploy-feeder-notebook.ps1`
auto-discover the hook (local working tree first, raw-GitHub fallback)
and invoke it with a populated `-Context` hashtable as the **last
deployment step**.

This is **opt-in**: most sources do not need a hook and should not
add one. Add a hook only if your source genuinely has post-bootstrap
wiring that today is a manual portal click and that you can automate
via REST or a Kusto control command.

**Hook contract:** the script accepts a `[hashtable] $Context`
parameter with all relevant IDs the deployer created. Common keys:
`Source`, `Mode` (`notebook` for the notebook deployer, absent for the
container deployer), `WorkspaceId`, `WorkspaceName`, `EventhouseId`,
`EventhouseClusterUri`, `DatabaseId`, `DatabaseName`, `RawBase`,
`Repo`, `Branch`, `TempDir`. Container deployer additionally provides
`EventstreamId`, `ContainerGroupName`, `ConnectionString`. Notebook
deployer additionally provides `NotebookId`, `NotebookName`. Hooks
must also accept explicit named parameters so they can be re-run
standalone; must `exit 0` when there is no work to do; and must throw
on real failure (the deployer treats hook failure as deployment
failure). Reference implementation: `dwd/fabric/post-deploy.ps1`. Full
documentation: `tools/deploy-fabric/README.md`.

### Notebook-hosting things that are not allowed

- Deploying to Fabric from the agent. Hand-off to manual verification.
- Editing wheels, the deploy script, the publish workflow, or anything
  under `tools/deploy-fabric/`. Those are infrastructure; this skill
  only consumes them.
- Editing [`fabric-notebook-deployment`](../fabric-notebook-deployment/SKILL.md)
  or `.github/copilot-instructions.md` from a feeder retrofit — the
  feeder agent is a consumer of those.
- Bundling multiple sources into one notebook retrofit PR. One source,
  one PR.
- Skipping the eligibility gate.
- Inventing new notebook cell structure, alternative CS-lookup
  techniques, or new log-file locations. Copy verbatim from
  `pegelonline`.
- Forcing a streaming bridge (websocket/MQTT/SSE) into the polling
  notebook model. Abort instead.
- Calling `asyncio.run()` inside a notebook cell.
- Adding a `CONNECTION_STRING` parameter to a Fabric notebook (look
  it up at runtime via the Topology API instead).

### Known notebook pitfalls

- **Hyphenated source ids** (e.g. `bafu-hydro`): the bridge package and
  generated producer dir use underscores (`bafu_hydro_producer`).
  `deploy-feeder-notebook.ps1` handles this; the wheel-publish workflow
  was patched to handle it in #249. If you see
  `Missing generated producer for <src>` in CI, that's the same class
  of bug — hyphen-vs-underscore in another consumer.
- **Lakehouse attachment** is automatic. The deploy script auto-binds
  the workspace's only Lakehouse (or aborts if there are 0 or 2+). Do
  **not** add Lakehouse-selection logic to the notebook itself.
- **Stage A connection-string warning is harmless.** If
  `Get-EventStreamConnectionString` in `deploy-fabric.ps1` fails with
  a JSON parse warning, the notebook flow still succeeds — the
  notebook resolves the CS at runtime via the Topology API.

## References

- [Runtime checklist](references/runtime-checklist.md)
- [Notebook substitution table](references/notebook-substitution-table.md)
- [Notebook eligibility discovery](references/notebook-eligibility-discovery.ps1)
- [`fabric-notebook-deployment`](../fabric-notebook-deployment/SKILL.md) — deployment pipeline the notebook plugs into
- [`xreg-source-contract`](../xreg-source-contract/SKILL.md) — contract authoring (consumed by the mandatory expert review)
- `pegelonline/notebook/pegelonline-feed.ipynb` — canonical notebook template
- `tools/deploy-fabric/deploy-feeder-notebook.ps1` — parameter names the deploy script overwrites; the notebook MUST declare all of them
