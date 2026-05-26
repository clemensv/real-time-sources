# Repository Conventions for Real-Time Sources

This repository contains Python bridges that consume open real-time data
feeds and re-emit them as CloudEvents into Apache Kafka. Each source lives
in its own top-level directory.

## Source Folder Layout

```
<source>/
  README.md
  CONTAINER.md
  EVENTS.md
  Dockerfile
  pyproject.toml
  pytest.ini
  generate_producer.ps1
  xreg/<source>.xreg.json          # authoritative contract
  <source>/<source>.py              # runtime bridge (or bridge.py)
  <source_producer>/                # xrcg-generated output (never hand-edit)
  tests/
  azure-template.json               # optional
  generate-template.ps1             # optional
  kql/<source>.kql                  # MANDATORY (generated from xreg; KQL Optimizer review required)
  fabric/                           # optional
```

## Implementation Sequence

1. **Upstream study** — Read the upstream API docs or OpenAPI spec. Inspect
   representative live payloads for every endpoint. Enumerate every data
   channel (REST endpoints, MQTT topics, WebSocket channels, file feeds)
   and produce a keep/drop list before designing the contract.
2. **xRegistry contract** — Author the `xreg/<source>.xreg.json` manifest.
3. **Generate producer** — Run `generate_producer.ps1` (which calls
   `xrcg 0.10.1`). Never hand-edit the generated output.
4. **Runtime bridge** — Implement the bridge code that polls, streams, or
   decodes upstream data and emits CloudEvents via the generated producer.
5. **Tests** — Unit and integration tests under `tests/`.
6. **Docker + docs** — Dockerfile, CONTAINER.md, EVENTS.md, README.md.
7. **Docker E2E** — Add a test class in `tests/docker_e2e/test_docker_kafka_flow.py`.
8. **Root catalog** — Add the source to the root `README.md`.

## xRegistry Contract Rules

- Every CloudEvents message **must** declare a `subject` metadata entry
  with `type: "uritemplate"`.
- Every Kafka endpoint **must** declare `protocoloptions.options.key`, and
  that key template must **match the subject template exactly**.
- Choose keys from **stable domain identifiers** (station IDs, MMSI, alert
  IDs, gauge numbers). Never use mutable names or descriptive labels.
- If event families use different identity shapes, split them into separate
  `messagegroups` and Kafka endpoints.
- Multi-part identities must stay aligned between subject and key, e.g.
  `{agency_cd}/{site_no}`.
- Schemas use **JsonStructure** (JSON Structure Core plus extension specs).
  Every schema and every field must carry exhaustive descriptions grounded
  in the upstream API docs.
- Use JSON Structure extensions where they add fidelity: `unit`/`symbol`
  for measured values, `altnames` for upstream JSON keys,
  `altenums`/`descriptions` for documented labels, validation keywords for
  ranges/formats/patterns.
- Never use `anyOf`; express nullable or alternative fields with type
  unions or `choice`.
- Conditional composition extensions are not used in this repo.
- Schema `$id` values must be globally unique.

### Reference Data as Events

If the upstream provides metadata about the entities telemetry describes
(station lists, sensor catalogs, zone definitions, route tables, vessel
registries), those **must** be modeled as named event types in the same
message group as the telemetry they contextualize. Reference data and
telemetry share the same key model and Kafka topic.

Reference data differs from telemetry only in update frequency — it is not
out-of-band context. See repo analogs: `pegelonline` (stations at startup),
`usgs-iv` (sites refreshed weekly), `chmi-hydro` (stations before
observations), `noaa-ndbc` (buoy stations).

## Producer Generation

- The generator is **xrcg 0.10.1**. Install with
  `pip install --upgrade xrcg==0.10.1`.
- Each source has `generate_producer.ps1` which calls
  `tools/require-xrcg.ps1` and then runs:\
  `xrcg generate --style kafkaproducer --language py --definitions xreg/<source>.xreg.json --projectname <source>_producer --output <source>_producer`
- Generated producer code is **never hand-edited**. If it doesn't fit,
  fix the manifest and regenerate.
- Generated output includes a `_data` sub-package (data classes) and a
  `_kafka_producer` sub-package (Kafka producer wrapper).
- The runtime imports the generated packages as pip-installed dependencies
  declared in `pyproject.toml` with `path = ...` references.

## Runtime Bridge Patterns

| Pattern | Use when | Repo analogs |
|---------|----------|--------------|
| Poller | Periodic HTTP/file fetch, delta detection | `pegelonline`, `noaa`, `chmi-hydro`, `hubeau-hydrometrie` |
| WebSocket/MQTT | Long-lived connection, reconnect loop | `aisstream`, `bluesky`, `digitraffic-maritime` |
| Raw TCP decoder | Binary protocol, sentence reassembly | `kystverket-ais` |
| Multi-family poller | Several endpoint groups | `dwd`, `entsoe`, `gtfs` |

### Bridge Implementation Rules

- Parse source and Kafka configuration from CLI args and environment
  variables.
- Emit **reference data first** at startup, then telemetry. Re-fetch
  reference data periodically.
- Normalize upstream payloads into the generated data classes.
- Pass subject/key placeholder values **explicitly** — do not hide them
  inside ad hoc key mappers.
- Kafka output must work with `CONNECTION_STRING` (plain or SASL/Event
  Hubs format).
- Handle state, dedupe, and reconnect where the source requires it.

## pyproject.toml Convention

```toml
[build-system]
requires = ["poetry-core>=1.1.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.dependencies]
python = ">=3.10,<4.0"
requests = ">=2.32.3"
confluent-kafka = ">=2.5.3"
cloudevents = ">=1.11.0,<2.0.0"
dataclasses_json = ">=0.6.7"
avro = ">=1.11.3"
<source>_producer_data = {path = "<source>_producer/<source>_producer_data"}
<source>_producer_kafka_producer = {path = "<source>_producer/<source>_producer_kafka_producer"}
```

Install the generated sub-packages **sequentially** (data first, then
kafka_producer, then the main package) when pip resolution conflicts arise.

## Dockerfile Convention

- Base image: `python:3.10-slim`
- Set OCI labels: `source`, `title`, `description`, `documentation`, `license`
- Documentation label points at the source `CONTAINER.md`
- Entry point: `CMD ["python", "-m", "<source>", "feed"]`
- Configuration is via environment variables only.

## Docker E2E Tests

The shared test suite at `tests/docker_e2e/test_docker_kafka_flow.py`:
- Builds the Docker image
- Starts the container alongside a Kafka broker
- Validates Kafka keys, CloudEvent subjects, and JsonStructure schemas
  against the checked-in xreg manifest
- Validates both **reference** and **telemetry** event types

A source is not done until its Docker E2E test passes. Key, subject, or
schema failures are contract or runtime drift — fix the source, not the
test.

Connection convention for E2E:
```
CONNECTION_STRING=BootstrapServer=host:port;EntityPath=topic
KAFKA_ENABLE_TLS=false
```

## Documentation

- `EVENTS.md` — generated from the xreg manifest. Refresh after contract
  changes.
- `CONTAINER.md` — deployment contract: upstream source description, env
  vars, docker pull/run examples, Kafka and Event Hubs usage.
- `README.md` — source overview, data model, upstream links.
- Root `README.md` — organized by topic category; add new sources to the
  appropriate section.

**Gold-standard reference docs.** The `pegelonline` source is the
canonical template for per-source documentation in this repo. When
authoring or revising a `README.md`, `CONTAINER.md`, or `EVENTS.md`
for any other source, mirror the structure, tone, headings, callout
usage, link-triangle pattern (cross-links between the three docs at
the top), Fabric-before-Azure deployment ordering, and image-contract
table from:

- `pegelonline/README.md`
- `pegelonline/CONTAINER.md`
- `pegelonline/EVENTS.md`

Deviate only when the source genuinely requires it (e.g. streaming
transports have no polling cadence to document). Do not invent a
different docs shape per source.

## Fabric Notebook Hosting (required for poll-based sources)

Every poll-based source ships a Fabric notebook feeder under
`<source>/notebook/<source>-feed.ipynb` and sets `notebook: true` in its
`catalog.json` entry. Streaming bridges (WebSocket / MQTT / raw TCP /
SSE firehose) are out of scope and skip this artifact. This is a
separate deployment option from ACI+Fabric and uses
`tools/deploy-fabric/deploy-feeder-notebook.ps1`
which builds a per-source Fabric Environment with the producer + bridge
wheels, binds Lakehouse + KQL + Environment to the notebook, looks up the
Event Stream connection string at runtime via the public Topology API, and
schedules the notebook. Three non-obvious rules apply:

- **No `asyncio.run()` in cells.** The Fabric kernel owns the loop; run
  `feeder.main()` in a worker thread.
- **No `%pip install` in cells.** Wheels live in the per-source Environment;
  the deploy script builds and uploads them.
- **OneLake is the only diagnostic channel** for scheduled runs. The notebook
  must log to `/lakehouse/default/Files/feeder-state/<source>/last-run.log`
  and call `notebookutils.notebook.exit("FAIL: …")` on error — Fabric REST
  does not expose cell output.

Full playbook: `.github/skills/fabric-notebook-deployment/SKILL.md`.
Reference implementation: `pegelonline/notebook/pegelonline-feed.ipynb`.

### Retrofitting existing pollers (fleet operation)

To add notebook hosting to an **already-shipped** poll-based source,
use the retrofit workflow folded into
`.github/skills/stream-bridge-implementation/SKILL.md` (the "Fabric
Notebook Hosting → Retrofit Workflow" section). It is designed to be
dispatched in parallel — one agent per source — by an orchestrator.
The agent copies the canonical `pegelonline` notebook, performs an
exact substitution table, flips `catalog.json` `notebook: true`,
validates locally, and opens a PR. It does **not** deploy to Fabric.

To discover the eligible-source set:

```powershell
pwsh .github/skills/stream-bridge-implementation/references/notebook-eligibility-discovery.ps1 -Format Lines
```

Sources in `skip:streaming` (websocket/MQTT) or `skip:not-a-poller`
(no polling loop) are out of scope for notebook hosting.

### Mandatory expert review

Every feeder PR that adds a new source or changes a contract must be
reviewed by all three of the following expert agents before it merges:
**xRegistry Expert** (manifest layout, CloudEvents modeling, key /
subject alignment), **JSON Structure Expert** (schema correctness,
native primitives, descriptions, validation extensions), and **Avro
Schema Expert** (Avro shape round-trip stability, nullability mirror,
identifier validity). The full review contract — what each agent
checks, when re-runs are required, and how to dispatch them — lives in
`.github/skills/stream-bridge-implementation/SKILL.md` under "Mandatory
Expert Review". Record each reviewer's verdict in the PR body.

### Mandatory container-and-delivery check (new-source PRs)

Every PR that adds a **new source** must additionally pass a final
review against the `container-and-delivery` skill
(`.github/skills/container-and-delivery/SKILL.md`) before it merges.
The skill is the single source of truth for the packaging-and-delivery
contract: Dockerfile shape and labels, `CONTAINER.md` authoring,
Azure Container Instance ARM templates, the mandatory KQL schema
script and its KQL Optimizer review, optional Fabric assets,
`EVENTS.md` generation, the root catalog entry, and the Docker E2E
validation. Walk the skill end-to-end against the PR and record the
check verdict in the PR body alongside the three expert reviews. A
new-source PR that has not been checked against this skill must not
be merged, even if the three expert reviews have signed off.

### Agent definition of done for new-source tasks

When the coding agent is tasked with creating a new source, the task
is **not done** — and must not be reported as done to the user — until
the agent has itself walked, end-to-end, the full pre-merge checklist
against its own work:

1. The three mandatory expert reviews (xRegistry Expert,
   JSON Structure Expert, Avro Schema Expert) have been dispatched
   against the final state of the manifest and generated artifacts,
   and every blocker raised has been addressed (or explicitly
   justified) and re-reviewed.
2. The `container-and-delivery` skill has been walked end-to-end
   against the source as it stands on the branch. Every checklist
   item the skill defines (Dockerfile, CONTAINER.md, ARM templates,
   KQL + KQL Optimizer review, optional Fabric assets, EVENTS.md,
   root catalog entry, Docker E2E) must be satisfied or have a
   recorded justification.
3. The agent has captured the verdicts from steps 1 and 2 in the PR
   body before handing back to the user.

**The agent must attempt to correct every issue raised by the reviews
autonomously, not just record them.** When any reviewer (xRegistry
Expert, JSON Structure Expert, Avro Schema Expert, or the
`container-and-delivery` skill walkthrough) flags a blocker or an
important finding, the agent's default behavior is to fix it in place
— edit the xreg manifest, regenerate producers, rebuild the
container, refresh the docs, re-run the Docker E2E — and then re-run
the affected review against the corrected state. The PR body should
report the *resolved* verdict and the fix that landed, not the original
finding plus an unaddressed TODO.

The agent should only escalate an issue back to the user (instead of
fixing it) when one of the following is true:

- The fix would change scope or contract semantics in a way the user
  has not authorized (e.g. dropping or renaming an event type,
  switching the keying scheme, removing a transport).
- The fix requires an external resource the agent cannot obtain (a
  paid API key, a vendor decision, a credential).
- Two competing reviewer recommendations cannot both be satisfied and
  the trade-off is a user-level judgement call.
- The same fix has been attempted and failed verification twice in a
  row, indicating the agent is stuck and needs human direction.

In every other case — schema description gaps, missing units,
malformed enums, missing reference data, broken codegen output,
missing ARM template, missing KQL update policy, failing Docker E2E,
missing portal catalog entry — the expected agent behavior is *fix,
regenerate, re-review, re-report*, not *log and defer*.

Reporting a new-source task as done while any of these reviews are
outstanding, deferred, or known to be failing is a process violation.
If the agent genuinely cannot complete or correct a review item, it
must surface that explicitly as an open item with the reason it could
not be fixed autonomously — never silently mark the task done.

## Things That Are Not Allowed

- Hand-editing generated producer code.
- Using `anyOf` or conditional composition in JsonStructure schemas.
- Using mutable names or labels as Kafka keys.
- Collapsing semantically different upstream entities into one generic
  catch-all schema without proof they are the same entity.
- Omitting reference data when the upstream provides metadata endpoints.
- Stopping the upstream API audit after the first two obvious endpoints.
- Shipping a source without CONTAINER.md, EVENTS.md, or a generator script.
- Bypassing `tools/require-xrcg.ps1` version enforcement.
- Calling `asyncio.run()` inside a Fabric notebook cell.
- Adding a `CONNECTION_STRING` parameter to a Fabric notebook (look it up
  at runtime via the Topology API instead).
- Using the legacy MWC token chain for Event Stream connection strings.
- Bundling multiple sources into one notebook-retrofit PR. The notebook
  retrofit workflow must produce one PR per source.
- Deploying notebook-retrofit PRs to Fabric from the retrofit agent
  itself. End-to-end Fabric verification is a separate, serial step.
- Merging a new-source or contract-changing PR without the three
  mandatory expert reviews (xRegistry, JSON Structure, Avro Schema)
  having signed off.
- Merging a new-source PR without a completed check against the
  `container-and-delivery` skill recorded in the PR body.
- Reporting a new-source task as done before the agent has itself
  completed the three mandatory expert reviews **and** the
  `container-and-delivery` skill walkthrough against its own work,
  with the verdicts recorded in the PR body.

## Real Bugs Are Blockers — Never Gloss Over Them

If during E2E work you discover a bug in a generated artifact, an
upstream tool (xrcg, avrotize, xregistry), a producer/consumer template,
or a spec-compliance issue (e.g. CloudEvents bindings, AMQP/MQTT/Kafka
protocol details), **stop and surface it**. Do not paper over it with a
test-only workaround and move on.

Examples of real bugs that must be raised, not worked around silently:

- Generated AMQP/MQTT/Kafka producer emits the wrong CloudEvents prefix
  (CE spec: `cloudEvents:` on AMQP, `ce-` on HTTP, `ce_` on Kafka).
- Generated dataclass `to_byte_array("application/json")` returns a
  `str` instead of `bytes`, causing the AMQP/MQTT binary body to be
  JSON-double-encoded on the wire.
- avrotize fails to generate dataclasses for schemas that use `$root`.
- xrcg filter / template bugs that produce empty or malformed output.
- Any spec-noncompliant header, key, subject, or content-type emission.

The required workflow when you hit one:

1. Capture the smallest reproducer (failing test, on-wire dump, or
   diff against the spec section it violates).
2. File or update an issue in the upstream repo (xregistry/codegen,
   clemensv/avrotize, etc.) with the reproducer.
3. If a temporary workaround is unavoidable to keep CI moving (e.g. a
   double `json.loads` in a test), mark it clearly in the code with a
   `# WORKAROUND(<upstream-issue>):` comment and link the issue.
4. Tell the user in the same response — do not bury the finding in a
   summary or treat it as "fixed" when only the symptom is masked.
5. Add a follow-up to the session plan so the workaround is removed
   once the upstream fix lands.

A passing test that hides a generator or spec-compliance bug is worse
than a failing test, because every future consumer of the generated
code will hit the same bug in production.
