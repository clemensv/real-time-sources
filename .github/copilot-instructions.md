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
   `xrcg 0.11.0`). Never hand-edit the generated output.
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

- The generator is **xrcg 0.11.0**. Install with
  `pip install --upgrade xrcg==0.11.0`.
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
3. **Runtime proof: ≥1 real event has been observed on the wire for
   every shipped transport** (Kafka / MQTT / AMQP). A green build, a
   started container, and passing unit tests are **not** proof — the
   class-A "shipped but never ran" defects (a `Dockerfile.amqp` missing
   a companion package, an `app.py` missing a `_feedurl` positional, a
   `{time}`/`_time` placeholder collision) all passed those and emitted
   zero events. Observe the event in the Docker E2E flow test, an
   ACI/Fabric validation run, or a local `ONCE_MODE` run against a
   broker. The import-time half of this class is caught deterministically
   by `tools/ci/import_smoke.py` (CI `import-smoke.yml`); the on-the-wire
   observation covers the first-`send_*` half.
4. The agent has captured the verdicts from steps 1–3 in the PR
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

## All Issues Are Issues — "Pre-existing" Is Not a Pass

When a validation run, CI test, or E2E check surfaces a failure, it
must be fixed regardless of whether the current commit introduced it.
The distinction between "caused by this change" and "pre-existing" is
useful for triage ordering but **never** an excuse to skip the fix.
A broken Docker E2E test that has been failing silently for weeks is
still a broken test. A misconfigured CI workflow that never collected
its target test class is still a bug.

The expected behavior:

- **Fix it.** If the issue is within your capability to fix (wrong
  env var, missing test class, serialization bug, timeout from missing
  `ONCE_MODE`), fix it in the same PR or commit stream.
- **Do not label and defer.** "Pre-existing, not caused by our
  changes" is not a valid final status. It is an intermediate triage
  note while you plan the fix.
- **Do not exclude from the matrix.** If a source is in the test
  matrix but its test is broken, fix the test — do not remove the
  source from the matrix.

## Mandatory Pre-Commit Validation

**No code is committed without passing these gates.** Every agent, every
contributor, every time — no exceptions. A commit that introduces a
regression detectable by these checks is a process failure.

### Gate 1: Import smoke-test (every touched feeder)

For every feeder package modified in the changeset, verify the package
imports cleanly:

```powershell
# For each modified source (Kafka, MQTT, AMQP variants):
python -c "import <package_name>"
python -c "import <package_name_mqtt>.<package_name_mqtt>.app" 2>$null
python -c "import <package_name_amqp>.<package_name_amqp>.app" 2>$null
```

If any import raises (`ModuleNotFoundError`, `SyntaxError`,
`TypeError`, `ImportError`), **stop and fix before committing**. This
catches the entire "shipped but never ran" bug class: missing
`__main__.py`, wrong import paths, missing Dockerfile deps that would
crash on first start.

The CI-enforced equivalent of this gate is
`python tools/ci/import_smoke.py feeders/<source>` (workflow
`import-smoke.yml`, scoped by `tools/ci/discover_feeders.py` to the
feeders a PR touches, escalating to the whole fleet on a shared-tooling
change). It py_compiles the tree, editable-installs the generated
sub-packages in dependency order, then imports each transport variant's
runtime module taken from the `python -m <module>` target of every
`Dockerfile*` -- importing `<module>.app` (the MQTT/AMQP companion crash
site) when present, else the bare module, and **never `__main__`** (72
feeders call `main()` at module scope, which would hang). Use `--plan`
for a no-install, compile-only check on Windows.

### Gate 2: py_compile on generated + hand-written code

```powershell
python -m py_compile <every .py file in the changed source tree>
```

A `SyntaxError` in any file blocks the commit.

### Gate 3: Dockerfile builds (every touched Dockerfile variant)

```powershell
docker build -f feeders/<source>/Dockerfile feeders/<source> --no-cache -q
docker build -f feeders/<source>/Dockerfile.mqtt feeders/<source> --no-cache -q
docker build -f feeders/<source>/Dockerfile.amqp feeders/<source> --no-cache -q
```

If a Dockerfile exists for a transport and the source was modified,
it must build. A build failure blocks the commit.

Every `Dockerfile*` carries a build-time import-smoke `RUN` just before
its final `CMD`:

```dockerfile
RUN python -c "import importlib, importlib.util as _u; _m='<module>'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"
```

A successful `docker build` therefore *proves* the runtime module and
every companion package it imports are installed and import-clean inside
the image -- the in-image equivalent of Gate 1, and the net that would
have caught the `Dockerfile.amqp`-missing-`_producer_mqtt_client` class.
Never delete that line when editing a Dockerfile.

### Gate 4: Unit tests pass

```powershell
cd feeders/<source>
python -m pytest tests/ -x --no-header -q
```

Red tests block the commit.

### Gate 5: Docker E2E (when modifying bridge logic or schemas)

If the change touches bridge runtime code, xreg schemas, or generated
producers, run the source's Docker E2E test locally before pushing:

```powershell
python -m pytest tests/docker_e2e/test_docker_kafka_flow.py::<TestClass> -x -v
```

A key, subject, or schema validation failure blocks the commit.

### Gate 6: mypy (if touching Python code)

```powershell
python -m mypy feeders --config-file mypy.ini --exclude /build/
```

Must not introduce new errors. Existing suppressed errors (`type: ignore`)
are acceptable; new un-suppressed errors are not.

### When to run which gates

| Change type | Gates required |
|---|---|
| Any `.py` file | 1, 2, 4, 6 |
| Dockerfile / Dockerfile.mqtt / Dockerfile.amqp | 3 |
| xreg schema or generated producer | 1, 2, 4, 5, 6 |
| Bridge runtime logic | 1, 2, 3, 4, 5, 6 |
| New transport variant (MQTT/AMQP app) | 1, 2, 3, 4, 5, 6 |
| Documentation only | None |

### Enforced in CI vs advisory

Several of these gates now run automatically on every pull request; the
rest remain agent-run pre-commit checks. Knowing which is which tells you
what a green PR has *already* proven and what you still owe by hand.

| Gate | CI workflow (auto) | Scope |
|---|---|---|
| 1 Import smoke | `import-smoke.yml` | feeders the PR touches (fleet on shared-tooling change) |
| 2 py_compile | folded into gates 1 and 5 | — |
| 4 Unit tests | `feeder-tests.yml` | feeders the PR touches |
| 5 Docker E2E | `test-docker-e2e.yml` (sharded via `discover_matrix.py`) | scoped / smoke set |
| 6 mypy | `mypy.yml` | whole `feeders/` tree |
| Encoding | `lint-encoding.yml` | `catalog.json` + every per-source doc |
| 3 Docker build | advisory (agent-run) + the build-time smoke `RUN` inside each image | per touched Dockerfile |

Advisory gates are still mandatory before you commit -- CI not running
them does not make them optional. Conversely, a CI-enforced gate going
red is never a "flake": fix it, per "All Issues Are Issues" below.

### Enforcement

- **Agents must run the applicable gates before every `git commit`.**
  Do not batch fixes and commit without validation. Do not assume a
  mechanical change is safe — verify it.
- **A commit that breaks CI in a way detectable by these gates is
  always the committer's fault**, not a "pre-existing issue" or a
  "CI flake." The agent must fix it immediately, not defer it.
- **Fleet-wide mechanical changes** (bulk renames, bulk schema fixes,
  bulk Dockerfile edits) are especially dangerous. After a bulk edit,
  run gates 1–3 on a representative sample (≥5 sources) before
  committing, and run the full Docker E2E suite immediately after push.
- **"It worked on my machine" is not acceptable.** The Docker build
  gate (Gate 3) catches dependency mismatches between the dev
  environment and the container. Always run it for Dockerfile changes.

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
- **"Shipped but never ran" AMQP/MQTT companion bugs** — a whole class of
  defects where a non-Kafka variant crashes on import or first send and has
  *never emitted a single event*, yet looked deployed. Observed instances:
  (a) `Dockerfile.amqp` installed only the `_producer_data` package but not
  the `_producer_mqtt_client` package the companion app imports →
  `ModuleNotFoundError` on first poll (12 feeders); (b) a hand-written AMQP
  `app.py` omitted a required `_feedurl` positional on the generated `send_*`
  methods → `TypeError` on first send (`dmi-amqp`); (c) a subject placeholder
  named `{time}` collided with the CloudEvents envelope `_time` param the
  codegen injects → `SyntaxError: duplicate argument '_time'` in the generated
  producer (`tepco-denkiyoho-amqp`). These crash-loop in ~7 s with logs that
  masquerade as auth/RBAC failures. **Mandate:** in CI and before declaring any
  source done, `py_compile` every generated producer module and **smoke-import
  the companion `app` module** of every non-Kafka variant (`<src>_amqp.app`,
  `<src>_mqtt.app`). An import that raises is a blocker, not a flake. Upstream
  codegen should also reject envelope-vs-placeholder name collisions
  (file an xregistry/codegen issue) and sanitize numeric-leading enum symbols
  (file a clemensv/avrotize issue).

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

## CI, Dependencies & PR Management

These cross-cutting facts about this repo's CI and PR machinery were learned
resolving a 116-PR dependabot pile-up and many fleet-validation runs. They are
durable and apply to any future maintenance work, not one task.

### mypy is repo-wide and stops at the first syntax error

CI runs `mypy feeders` across the **entire** `feeders/` tree. A single
in-scope file with a `SyntaxError` (e.g. a botched-indentation `WORKAROUND`
block) makes mypy abort at that file and **fails the mypy check on every open
PR**, regardless of what the PR touched. When many unrelated PRs fail mypy
identically, suspect one broken file on `main`, not the PRs. Emulate locally
with `python -m mypy feeders --config-file mypy.ini --exclude /build/` (the
`/build/` exclude avoids spurious "Duplicate module" errors from `build/lib`
artifacts; `mypy.ini` already excludes `tests/` and `*_producer/`).

### mypy strict mode with MYPYPATH for full producer type resolution

The CI workflow (`.github/workflows/mypy.yml`) sets `MYPYPATH` to all
`*_producer*/*/src` directories, which gives mypy visibility into the
generated data-class signatures. Without MYPYPATH, producer types resolve
to `Any` and arg-type errors are invisible. Key rules:

- **`mypy.ini` enables `arg-type`** — mismatched constructor arguments
  (wrong type passed to a generated data class field) are hard errors.
  This catches real bugs: wrong method calls, missing kwargs, incorrect
  attributes, passing `str` to `datetime` fields, etc.
- **Bridges must parse values to their schema type.** Pass
  `datetime.datetime.fromisoformat(x)` to datetime fields,
  `float(x)` to float fields, `EnumType.from_ordinal(x)` to enum
  fields. Never pass raw strings to typed fields.
- **Schema nullability must match upstream API reality.** If an
  upstream API returns `null` for a field, the xreg schema must
  declare it nullable (`"type": ["string", "null"]`). Otherwise the
  generated data class requires non-Optional and the bridge needs
  `# type: ignore` — which masks potential runtime issues.
- **xrcg requires non-nullable enum fields to NOT be in `required`
  for Optional generation.** If a string enum field's type is
  `["string", "null"]` but it remains in the schema's `required`
  array, xrcg still generates a non-Optional enum type. Remove it
  from `required` to get `Optional[EnumType]`.
- **`from_ordinal` ternary narrowing is a known mypy limitation.**
  The pattern `EnumType.from_ordinal(row.get("x")) if row.get("x")
  else DEFAULT` is correct at runtime but mypy can't narrow type
  across two separate `.get()` calls. Suppress with
  `# type: ignore[arg-type]`.

### Known safe `type: ignore[arg-type]` categories

These suppressions are permanent and correct:

| Category | Cause | Count |
|----------|-------|-------|
| Cross-package identity | AMQP/MQTT bridges pass Kafka `_producer_data` classes to AMQP/MQTT producers that expect their own structurally-identical types | ~6 |
| `content_mode` Literal | xrcg generates `str` parameter, bridges pass string literals that mypy types as `str` not `Literal['structured','binary']` | ~8 |
| `from_ordinal` ternary | mypy can't narrow `Any\|None` from `.get()` across ternary branches | ~29 |
| `float(x)` with fallback | `float(raw.get("x") if raw.get("x") is not None else -1)` — mypy sees `Any\|int\|None` | ~6 |

### Feeder test workflows must install local packages explicitly

The consolidated `feeder-tests.yml` matrix workflow runs each touched
feeder's `pytest` using the pip pattern (not `poetry install`). Local
sub-packages (`*_core`, `*_producer_data`, `*_producer_kafka_producer`,
etc.) are NOT on PyPI — they are installed with `pip install -e ./<path>`
in dependency order (via `tools/ci/import_smoke.py --install-only`) before
the feeder's `.[dev]` extra. See `feeder-tests.yml` for reference. Failing
to install producer packages first produces
`ERROR: No matching distribution found for <package>` at install time.
(The six hand-maintained `test-<source>.yml` workflows were retired in
favour of this one.)

### Branch protection is OFF → the dependabot auto-merge workflow can't work

`gh api repos/:owner/:repo/branches/main/protection` returns **404** — there is
no branch protection or merge queue on `main`. `.github/workflows/
dependabot-auto-merge.yml` runs `gh pr merge --auto`, which **requires** branch
protection to have something to wait on; without it the command errors on every
dependabot PR and nothing ever merges. Fixing this is a user decision: either
(a) add required-status-check branch protection, or (b) change the workflow to
a direct `gh pr merge --squash` gated on the substantive checks. Do not change
it unilaterally.

### Stale dependabot branches — use the update-branch API, not bulk rebase

When dependabot branches are many commits behind `main`, their CI fails on the
**stale tree**, not on the dependency bump. Dependabot **ignores bulk
`@dependabot rebase` comments** at scale. Instead, merge current `main` into
each branch non-destructively via the REST API:
`gh api --method PUT repos/:owner/:repo/pulls/<n>/update-branch`. Then
**squash-merge** — a squash applies only the dependency diff onto current
`main`, so the merged result is correct regardless of how stale the branch was.
A genuine file conflict (e.g. a `requirements.txt` that collides with a
generated-producer rewrite already on `main`) must be applied directly to
`main` and the PR closed as superseded.

### gh / az / PowerShell gotchas that silently corrupt automation

- `gh pr list --json statusCheckRollup` **504s** on large PR sets. Use per-PR
  `gh pr checks <n> --json name,bucket` instead (buckets: `pass`/`fail`/
  `pending`/`skipping`/`cancel`).
- **`2>&1` merges gh/az stderr into stdout** and breaks a downstream
  `ConvertFrom-Json`. Keep stderr separate when you intend to parse stdout.
- Firing many CI runs at once **saturates the Actions runner queue** (jobs sit
  `queued`, they are not failing). Merging a PR **cancels** that branch's queued
  runs — a useful lever to reclaim the queue.
- Each `powershell` call is a **fresh process** — env vars, working directory,
  and `az`/virtualenv state do not persist between calls.
- `&&` only chains **native** commands in PowerShell; use `;` before any
  language keyword (`if`, `foreach`, `$x =`).
- A `foreach {}` block can't be piped straight into `Sort-Object` — collect into
  a variable first.
- Prefer `git commit -F <file>` over `-m` for multi-line or backslash-bearing
  commit messages.
- **Regex-disabling flags silently match nothing.** `Select-String -SimpleMatch`
  (and `findstr` without `/r`) treat the pattern as a literal, so a regex
  alternation like `fix|refactor` matches zero lines instead of erroring —
  yielding a confidently-wrong "no hits" result. When mining history or
  classifying commits, confirm the matcher honours regex before trusting a
  zero count.

### Test secrets live outside the repo

API keys and tokens for E2E/validation runs are stored in
`c:\rts-creds\test-creds.json` (outside the repo, git-ignored by virtue of
location). Never commit secrets, never echo them into logs, and read them from
that file (or the session-local gitignored runner) rather than hardcoding.

### Dependency / codegen version-bump checklist (highest-blast-radius routine action)

Bumping a **shared dependency major** (cloudevents, confluent-kafka, paho,
qpid-proton) or the **codegen tool** (xrcg / avrotize) is the repo's
highest-blast-radius routine change — it touches every feeder at once. The two
fleet-wide regen chores and the cloudevents `<2.0.0` flip-flop (revert
`4d00aea4a` → re-cap `bf584c928`, 92 pyprojects) all started as a one-line bump.
Before bumping, run this ritual:

1. **Grep for relocated/removed submodules.** Search the generated producers
   **and** the bridges for every import path the new major removes or moves
   (the `cloudevents.http` → `cloudevents.core.bindings.http` lesson). If any
   feeder still imports the old path, the bump breaks it at import time.
2. **Smoke a representative sample.** Run `tools/ci/import_smoke.py` across ≥5
   feeders spanning Kafka/MQTT/AMQP with the new version resolved — do not
   trust that "it installed."
3. **Pin, don't float.** Land the new constraint as an explicit cap in *every*
   pyproject (and confirm the producer sub-packages already carry it), so a
   transitive resolve can't silently pull the breaking major in CI.
4. **One bump, one PR.** Never combine a version bump with unrelated feeder
   changes — the blast radius makes bisecting a regression impossible.

### cloudevents must be pinned `<2.0.0` — 2.x removed `cloudevents.http`

cloudevents **2.x** (PyPI latest 2.2.0) is a breaking rewrite that **removed
the `cloudevents.http` module** (relocated to `cloudevents.core.bindings.http`).
Every generated producer and every bridge imports `from cloudevents.http import
CloudEvent` (the 1.x API), so any environment that resolves cloudevents 2.x
fails at import with `ModuleNotFoundError: No module named 'cloudevents.http'`.
**Every feeder pyproject must pin `cloudevents>=1.12.1,<2.0.0`** — the same cap
the generated `*_producer/*` packages already use. A looser `<3.0.0` (or a bare
`"cloudevents"`) lets `pip install -e .[dev]` pull 2.x and turns the per-feeder
Bridge Tests red. **Production containers are NOT affected**: every `Dockerfile*`
installs the producer packages (pinned `<2.0.0`) **before** `pip install .`, so
the runtime resolves cloudevents 1.x regardless of the main package's
constraint — the breakage is **CI-only** (dev-installs of the main package
alone). Do not "fix" this by switching to the 2.x import path unless you rewrite
every `cloudevents.http` import across the whole repo. Incident: 92 pyprojects
re-capped in `bf584c928` after GTFS / USGS-IV / RSS / Bluesky went red
~2026-06-19.

### Feeder test workflows use pip + explicit producer installs — never poetry

Feeder pyprojects are PEP 621 / setuptools-scm (`[project]` with
`dynamic = ["version"]`). `poetry install` **rejects a dynamic version in
package mode** ("Either [project.version] or [tool.poetry.version] is required"),
so a `poetry`-based test workflow fails at the install step before any test
runs. The consolidated `feeder-tests.yml` matrix workflow uses the pip
pattern (see `feeder-tests.yml`): set up Python with
`cache: 'pip'`, **install the generated producer packages first**
(`pip install -e ./<src>_producer/<src>_producer_data` then
`..._kafka_producer`, plus any mqtt/amqp producer the tests import), then
`python -m pip install -e '.[dev]'`, then run `pytest` directly (no `poetry run`
prefix). The producer packages must be installed explicitly because the
setuptools-scm migration drops the old poetry `path = ...` deps — so
`pip install -e '.[dev]'` alone does not pull them and tests fail with
`ModuleNotFoundError: No module named '<src>_producer_data'`. Incident:
`test-usgs-iv.yml` + `test-rss.yml` migrated off poetry in `b69774da9`
(those per-source workflows were later consolidated into `feeder-tests.yml`).
