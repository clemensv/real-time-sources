---
name: feeder-release-checklist
description: "Use this checklist BEFORE merging any feeder change in this repo (new source, new transport variant, contract change, schema change, env-var change, deploy template change, doc change). Covers schema description quality, transport completeness (Kafka + MQTT + AMQP), ghpages portal deploy buttons, README + CONTAINER.md business-value framing, env-var documentation, ARM templates, EVENTS.md regen, Docker E2E coverage. EVERY item must be ticked or explicitly justified as not-applicable before the PR is shippable."
argument-hint: "Name of the feeder being released and the scope of the change (new transport, contract bump, doc refresh, etc.)."
---

# Feeder Release Checklist

This is a hard gate. Before any feeder PR is considered shippable in
this repo, every item below must be **passed** (✅) or explicitly
declared **N/A** with a one-line justification in the PR description.
"I'll do it later" is not an acceptable status — open a follow-up
issue and tick a separate box for it.

Pass criteria are stated as observable artifacts (file content, test
exit code, deployed button) — not "I think I did this".

## Use specialist sub-agents wherever they exist

Several sections below are best validated by **specialist agents
available via the `task` tool**. When you are running this checklist
inside an agent runtime that exposes them, delegating is **strongly
preferred** over self-review — these agents are tuned for the exact
artifact under review and produce higher-signal findings than a
generalist sweep. Launch them in parallel (one `task` call per agent,
all in the same response) and feed their findings back into the
checklist before ticking the relevant bullets.

| When you reach… | Delegate to | What to ask for |
|---|---|---|
| Section 1 — schema descriptions, JsonStructure extensions, key/subject design, **Avro/JsonStructure parity and per-field `doc`/`description` coverage in both formats** | **xRegistry Expert** + **JSON Structure Expert** (parallel) | Full review of `xreg/<source>.xreg.json` for contract correctness, key/subject alignment, exhaustive field descriptions grounded in upstream docs **on every record/field of every schema in every format (JsonStructure AND Avro)**, JSON Structure extension coverage on every measured value, anyOf/composition violations, `$id`/`name` uniqueness, Avro/JsonStructure drift |
| Section 4 — test rigor | **code-review** | High-signal review of new/changed test files for spec-compliant assertions, missing reference-event validation, hidden workarounds for upstream bugs |
| Section 5 / 6 — Dockerfile, ARM template, identity / role-assignment correctness | **code-review** | Review Dockerfile + every `azure-template-*.json` for missing OCI labels, broken `path =` refs, missing UAMI / role assignments, missing state file share |
| Any KQL ships under `kql/` or `fabric/` | **KQL Optimizer** | Review every `.kql` file for performance, table/column drift against the current xreg schema, and idiomatic Kusto |
| Any Fabric asset ships under `fabric/` (Eventstreams, Eventhouses, notebooks, pipelines) | **Fabric Deployer** | Review item definitions, deployment scripts, and connection wiring for current Fabric REST API + `fab` CLI patterns |
| Section 8 — README + CONTAINER.md business-value framing and consumer clarity | **code-review** | Critique whether the first 200 words of README.md actually convey business value to a non-domain reader; flag stale snippets, missing transports, missing buttons |

If the agent runtime does **not** expose a given specialist agent
locally, fall back to self-review and note `(no specialist agent
available)` next to the affected bullet so the gate stays honest.

Do not skip the checklist bullets themselves just because an agent
ran — the agent's findings are inputs to your tick/justification, not
a replacement for it.

## 0. Scope check

- [ ] **Transport scope declared.** State which transports the feeder
      supports: Kafka, MQTT, AMQP, or any subset. Any transport not
      shipped must have an explicit "not planned" or "tracked in
      issue #N" note.
- [ ] **Change scope declared.** New source / new transport variant /
      contract change / schema change / env-var change / deploy
      template change / doc-only refresh. Drives which sections below
      apply.

## 1. xRegistry contract quality (`xreg/<source>.xreg.json`)

> **Delegate first:** launch **xRegistry Expert** and **JSON Structure
> Expert** in parallel via `task` against `xreg/<source>.xreg.json`.
> Use their findings to tick the bullets below. If neither agent is
> available locally, self-review and annotate `(no specialist)`.

- [ ] **Subject + Kafka key alignment.** Every CloudEvents message
      declares a `subject` of type `uritemplate`. Every Kafka endpoint
      declares `protocoloptions.options.key` and the template matches
      the subject template **exactly**. Multi-part identities stay
      aligned across both. See
      `.github/instructions/xregistry-keying.instructions.md`.
- [ ] **Keys come from stable domain identifiers.** Station IDs, MMSI,
      alert IDs, gauge numbers — never mutable names or descriptive
      labels.
- [ ] **Distinct identity shapes ⇒ separate messagegroups.** If event
      families use different key models, they live in separate groups
      and separate Kafka endpoints.
- [ ] **Schemas are JsonStructure, not anyOf.** No `anyOf`. No
      conditional composition. Nullable / alternative fields use type
      unions or `choice`.
- [ ] **Every schema and every field has an exhaustive description**
      grounded in the upstream API docs, **in every schema format
      shipped (JsonStructure AND Avro)**. "string", "the value",
      "TBD", or single-sentence placeholders are not acceptable.
      Descriptions must explain the **business meaning**, the
      **unit / encoding**, the **valid range** if applicable, the
      **upstream documentation reference**, and the **consumer's
      intended use** where non-obvious. For Avro this means every
      `record` carries a `doc`, every `field` carries a `doc`, and
      every named `enum` / `fixed` carries a `doc` — no exceptions.
      The Avro descriptions must say the same thing as the
      JsonStructure descriptions (they describe the same fields);
      keeping them in sync is part of the release.
- [ ] **JSON Structure extensions used where they add fidelity.**
      `unit` / `symbol` on measured values, `altnames` for upstream
      JSON keys, `altenums` / `descriptions` for documented labels,
      validation keywords for ranges / formats / patterns. Missing
      extensions on a measured field is a defect.
- [ ] **Reference data modeled as named event types** in the same
      message group as the telemetry it describes, with the same key
      model and topic. Station lists, sensor catalogs, zone
      definitions — these are events, not out-of-band context.
- [ ] **Schema `$id` and `name` are globally unique.** Same `name`
      across multiple schemas breaks avrotize deduplication.
- [ ] **Both schema formats ship and stay in sync.** This repo
      requires **both** a JsonStructure schemagroup **and** a
      parallel Avro schemagroup for every source. They are not
      alternatives — Avro is a required downstream artifact and must
      be checked in alongside the jstruct schemas. When fields, types,
      enums, required-ness, or descriptions change in one, the other
      must be updated in the same PR. Drift between the two formats
      is a blocker.

## 2. Generated producer code (per transport)

- [ ] **Generator pinned and current.** `tools/require-xrcg.ps1`
      points at the xrcg version required. The release was tested
      against that exact version.
- [ ] **Producer regenerated from the manifest.** Re-ran
      `generate_producer.ps1` after the last contract change. **No
      hand-edits** to `*_producer/` directories.
- [ ] **All targeted transports regenerated.** Kafka, MQTT, AMQP
      producers are all up to date — not just the one you touched. A
      contract change touches all of them.
- [ ] **Generated code parses + imports.** Smoke test:
      `python -c "from <source>_<transport>_producer.<...> import *"`.

## 3. Runtime bridge (per transport)

- [ ] **Reference data emitted first** at startup and refreshed
      periodically (interval documented). Telemetry never publishes
      before the catalog the consumer needs to interpret it.
- [ ] **Subject / key placeholders passed explicitly** to the
      generated producer — no ad-hoc key mappers, no hidden coupling
      to upstream payload field names.
- [ ] **State, dedupe, reconnect** implemented where the source
      requires it. ETag / If-Modified-Since on REST; offset / cursor
      on streams; lock renewal on session-aware brokers.
- [ ] **Config surface mirrors the canonical env-var conventions.**
      Kafka uses `CONNECTION_STRING` + `KAFKA_*` + `SASL_*`; MQTT
      uses `MQTT_*` + auth-mode + Entra plumbing; AMQP uses `AMQP_*`
      + auth-mode (`password` / `entra` / `sas`) + matching Entra /
      SAS plumbing. Deviation requires justification.
- [ ] **All auth modes wired and validated up front.** For AMQP that
      means SASL PLAIN, Entra CBS, and SAS-token CBS are all
      reachable and mutually exclusive at `__init__`. For MQTT that
      means password + Entra OAUTH2-JWT. For Kafka that means SASL
      PLAIN with optional `CONNECTION_STRING` shortcut.

## 4. Tests

> **Delegate first:** launch **code-review** via `task` against the
> changed test files for spec-compliance and hidden workarounds.

- [ ] **Source-local unit tests pass.** `pytest <source>/tests/`.
- [ ] **Docker E2E exists for every transport.** Kafka via the shared
      `tests/docker_e2e/test_docker_kafka_flow.py`; MQTT via its own
      test class; AMQP via the Artemis test **and** the Service Bus
      emulator test (post xrcg 0.10.5). Missing a transport's E2E
      class is a blocker.
- [ ] **Every Docker E2E passes locally.** Run before requesting
      review. Cached image runs are typically 1–3 min each.
- [ ] **E2E asserts the spec-compliant wire format.** No "accept both
      `ce-` and `cloudEvents:` prefixes" workarounds. No "decode body
      twice" workarounds. If a generator bug forces a workaround,
      file the upstream issue, tag it `WORKAROUND(<issue>):`, and
      note it in the PR (per repo policy "Real Bugs Are Blockers").
- [ ] **E2E validates BOTH reference and telemetry event types**
      against the checked-in JsonStructure schemas. A green E2E that
      never saw a reference event is not actually green.

## 5. Container packaging (per transport)

- [ ] **`Dockerfile.<transport>` exists** with OCI labels: `source`,
      `title`, `description`, `documentation`, `license`. The
      `documentation` label points at the source `CONTAINER.md`.
- [ ] **Base image `python:3.10-slim`** unless documented otherwise.
- [ ] **Entry point** invokes the right module: `python -m
      <source>_<transport> feed`. Configuration is via env vars only
      — no command-line-only args in the published image.
- [ ] **Image builds clean.** No untracked editable installs, no
      broken `path = ...` references in pyproject.

## 6. Azure deployment templates (per realistic target)

> **Delegate first:** launch **code-review** via `task` against every
> `azure-template-*.json` for missing UAMI / role assignments, broken
> resource refs, and missing state share. If `kql/` or `fabric/`
> assets ship, also launch **KQL Optimizer** and **Fabric Deployer**
> in parallel.

Every realistic Azure target must have an `azure-template-*.json` ARM
template **and** a working "Deploy to Azure" button. The realistic
targets per transport are:

| Transport | Realistic Azure targets |
|---|---|
| Kafka | (a) bring-your-own Event Hubs / Fabric connection string → `azure-template.json`; (b) provision new Event Hubs namespace → `azure-template-with-eventhub.json` |
| MQTT | (c) bring-your-own MQTT 5 broker → `azure-template-mqtt.json`; (d) provision new Event Grid MQTT broker → `azure-template-with-eventgrid-mqtt.json` |
| AMQP | (e) provision new Azure Service Bus namespace → `azure-template-with-servicebus.json` |

For each in-scope target the following items are **BLOCKING REVIEW
CRITERIA**. A PR that fails any of them must not merge, even if all
other checks have signed off. The reviewer must run the verification
script (`tools/verify-arm-template.ps1`) and the validator
(`tools/validate-arm-templates.ps1`) against the changed templates
and paste the PASS lines into the PR body.

- [ ] **ARM template exists and is NON-EMPTY** at the canonical
      filename above. An `azure-template-*.json` whose `resources`
      array is empty (`"resources": []`) is a release blocker — it
      will create an empty resource group on deploy and is the most
      common silent regression in this repo. Reviewers MUST verify
      `(Get-Content <tpl> -Raw | ConvertFrom-Json).resources.Count -gt 0`
      for every template touched by the PR.
- [ ] **Every required feeder env var is exposed as an ARM
      parameter** with `type` (`string` or `securestring`), a
      sensible `defaultValue` (omit only for required secrets), and a
      `metadata.description` derived from CONTAINER.md / the runtime
      argparse help text — not a generic "X configuration value"
      placeholder. The parameter must be wired into the container
      `environmentVariables` array using `value` (non-secret) or
      `secureValue` (secret). Run
      `pwsh tools/validate-arm-templates.ps1 -FeederSlug <slug>` and
      paste the report into the PR body. Missing required-secret
      parameter is an `error` and blocks merge; missing non-secret
      parameter is a `warning` and blocks merge unless the env var
      is explicitly justified as not user-tunable in the PR body.
- [ ] **Image suffix matches transport family.** kafka + eventhub →
      base image (no suffix), servicebus + amqp → `-amqp:latest`,
      mqtt + eventgrid-mqtt → `-mqtt:latest`. Mismatches cause the
      wrong container variant to run and silently break the
      deployment.
- [ ] **Template provisions identity + role assignment** where Entra
      ID is the auth path (UAMI + the right
      `Microsoft.Authorization/roleAssignments` per resource).
- [ ] **Storage account + file share** mounted for persistent dedupe
      state on kafka / eventhub / servicebus variants. MQTT variants
      do not require a state share — follow the aisstream reference
      shape.
- [ ] **Template validated end-to-end against a live Azure
      subscription** within the last 30 days via
      `pwsh tools/verify-arm-template.ps1 -FeederSlug <slug>
      -Variant <variant>`. This script creates a real resource
      group, deploys the template, observes data flow on the
      provisioned broker (eventhub / servicebus / eventgrid-mqtt) or
      validates container-group shape (amqp / mqtt BYO variants),
      and tears the RG down in a `finally` block. Paste the script's
      `PASS` line into the PR body. A PR that has not been live-
      verified against Azure is not mergeable.

## 7. ghpages portal (`catalog.json` + `app.js`)

- [ ] **Source entry exists in `catalog.json`** with all in-scope
      transport flags set (`mqtt: true`, `amqp: true`, etc.).
- [ ] **`notebook: true` is set** in BOTH `catalog.json` (main) AND
      `app.js` SOURCES (ghpages branch) whenever
      `feeders/<slug>/notebook/<slug>-feed.ipynb` exists. A missing
      flag hides the "Deploy to Fabric Notebook" button even though
      the notebook is ready to deploy. Verify by running
      `pwsh tools/validate-fabric-deployment.ps1` — exit 0 with zero
      blockers means catalog ↔ notebook opt-in is consistent across
      the fleet.
- [ ] **Deploy button(s) render** on the live portal for every
      shipped transport. Check by inspecting the rendered card after
      the `update-ghpages-catalog` workflow runs on `main`.
- [ ] **`app.js` button plumbing exists** for every shipped transport
      (the catalog flag is necessary but not sufficient). Look for
      `btn-container-<transport>` containers and the matching hash
      route handlers.

## 7a. Fabric notebook deployment correctness — BLOCKING

> Notebook feeders are a separate hosting model from ACI: the
> deploy script (`tools/deploy-fabric/deploy-feeder-notebook.ps1`)
> uploads the `.ipynb` to a Fabric workspace, binds a per-source
> Environment + KQL DB + Eventstream, and schedules it. A broken
> notebook fails silently on the Fabric scheduler — there is no
> portal-visible stderr — so static checks before merge are
> non-negotiable for any source where
> `feeders/<slug>/notebook/<slug>-feed.ipynb` exists.

Run `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <slug>` and
confirm **zero blockers** before requesting review. The validator
enforces, per source:

- [ ] **No `asyncio.run(` in any code cell.** The Fabric kernel owns
      the event loop; `asyncio.run` deadlocks scheduled runs. Run
      `feeder.main()` on a worker thread instead.
- [ ] **No `%pip install` / `!pip install` / `%conda install` magic
      in any code cell.** Wheels must come from the per-source Fabric
      Environment built by `deploy-feeder-notebook.ps1`. Magic
      installs make scheduled runs depend on PyPI availability and
      break the version pin contract.
- [ ] **OneLake state-file logging present** —
      `/lakehouse/default/Files/feeder-state/<source>/` is the only
      diagnostic channel for scheduled runs since Fabric REST does
      not expose cell stderr.
- [ ] **`notebookutils.notebook.exit(` is called on the failure
      path** — without it, exceptions surface as a generic "notebook
      failed" with no message.
- [ ] **`CONNECTION_STRING` is NOT a notebook parameter** — the
      notebook resolves the Event Stream connection string at
      runtime via the public Topology API. Bake-in parameters expose
      the secret to anyone with workspace read access and break
      rotation.
- [ ] **`feeders/<slug>/fabric/post-deploy.ps1`** (when present)
      parses cleanly via the PowerShell AST, declares
      `[hashtable] $Context` as its first param, references at least
      one of the well-known `$Context` keys (`WorkspaceId`,
      `EventhouseId`, `DatabaseId`, `EventstreamId`), and every sibling
      file it `Join-Path $PSScriptRoot`s exists on disk.
- [ ] **Live deploy + scheduled run + tear-down** succeeded **in a
      real Fabric workspace** within the last 30 days for any
      notebook touched by this PR. Capture the workspace name + run
      ID and paste into the PR body.

A PR that introduces or modifies a notebook MUST include the
validator's `PASS` line and the live-deploy evidence in the PR body.

## 8. Documentation

> **Delegate first:** launch **code-review** via `task` to critique
> whether README.md's first 200 words convey business value to a
> non-domain reader, and to flag stale snippets, missing transports,
> missing buttons, and missing env-var rows across README +
> CONTAINER.md + EVENTS.md.

### `README.md`

- [ ] **Business value framed up front.** Open with **who consumes
      this feed in production** and **what decisions they drive** —
      flood early warning, shipping operations, energy dispatch,
      compliance, insurance, research, etc. Not just "this is a
      bridge that polls X". A reader who does not work in the source
      domain must finish the first 200 words knowing why they should
      care.
- [ ] **All shipped transports listed** in the variant table with
      image, transport stack, and default delivery shape.
- [ ] **Quick-start Docker snippet for every transport.**
- [ ] **All in-scope deploy buttons present** (same set as section 6
      above). Do not list only the Kafka buttons.
- [ ] **Repository layout** reflects current directory structure
      (every `*_producer/`, every `Dockerfile.*`, every feeder
      package).
- [ ] **Configuration reference** either fully enumerated here or
      explicitly delegated to `CONTAINER.md` with a one-line pointer
      — do not half-document.

### `CONTAINER.md`

- [ ] **Title names every shipped transport.** Not "Kafka & MQTT" if
      AMQP is also shipped.
- [ ] **Business-value paragraph** mirrors the README (it is fine to
      condense, but a pure technical document is not acceptable for a
      consumer-facing container manifest).
- [ ] **`docker pull`** commands for every image.
- [ ] **`docker run`** examples for every realistic auth mode of
      every transport. For AMQP that means: generic broker + SASL
      PLAIN, Service Bus + Entra, Service Bus emulator + SAS. For
      MQTT: generic broker + password, Event Grid + Entra
      OAUTH2-JWT. For Kafka: bootstrap servers + SASL, Event Hubs
      connection string.
- [ ] **Environment variable tables** complete for every transport.
      Every env var the feeder reads is listed with description,
      default (if any), and which auth mode it applies to. Adding a
      new env var without updating this table is a blocker.
- [ ] **All in-scope deploy buttons present** with a one-paragraph
      description of what each template provisions and what role
      assignments / identities it creates.

### `EVENTS.md`

- [ ] **Regenerated from the current `xreg/<source>.xreg.json`** —
      never edited by hand. Refresh after any contract change.
- [ ] **Covers both reference and telemetry event types** with the
      full schema, subject template, and Kafka key template.

### Root `README.md`

- [ ] **Source listed** in the appropriate topic category section. A
      new source that does not appear in the root catalog is
      invisible to discovery.

## 9. Pre-merge gate

- [ ] **Branch rebased on `main`.** No merge commits introduced by
      the rebase.
- [ ] **All checks above ticked** in the PR description with the
      observable artifact (test exit code, file path, deployed URL,
      etc.). Items declared N/A include a one-line justification.
- [ ] **Co-authored-by trailer** present on the merge commit (see
      `<git_commit_trailer>` in repo conventions).
- [ ] **Upstream issues filed** for any generator / spec bug that
      forced a workaround. The PR cross-references them and the
      workaround is tagged `WORKAROUND(<issue>):` in code.

## Outputs

When using this skill, produce a PR-ready checklist comment
containing exactly the bullets above with ✅ / ❌ / N/A status and the
observable artifact for each one. Do not paraphrase the bullets —
copy them verbatim so the gate stays auditable across releases.

## See Also

- `bootstrap-real-time-source` — start-of-source checklist.
- `xreg-source-contract` — contract authoring.
- `stream-bridge-implementation` — runtime bridge patterns.
- `container-and-delivery` — packaging baseline.
- `mqtt-uns-feeder` — MQTT delta over Kafka baseline.
- `amqp-feeder` — AMQP delta over Kafka baseline.
- `.github/instructions/xregistry-keying.instructions.md` — subject /
  key alignment rules.
