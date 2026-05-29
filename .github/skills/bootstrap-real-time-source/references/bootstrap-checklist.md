# Bootstrap Checklist

## Repo Patterns

- Polling APIs with reference data plus observations: `pegelonline`, `rws-waterwebservices`, `waterinfo-vmm`, `chmi-hydro`, `imgw-hydro`, `hubeau-hydrometrie`
- Continuous websocket or MQTT feeds with REST reference data: `aisstream`, `bluesky`, `digitraffic-maritime`
- Raw TCP decode pipelines: `kystverket-ais`
- Multi-family or domain-partitioned polling sources: `dwd`, `entsoe`, `gtfs`

## Standard Source Layout

The default layout is a **multi-transport feeder** matching `pegelonline` — shared acquisition core plus one app per transport (Kafka, MQTT, AMQP). Single-transport layouts are only acceptable when the user explicitly says so or the source's nature makes one transport unworkable; document the reason in `README.md`.

- `README.md`
- `CONTAINER.md`
- `EVENTS.md`
- `Dockerfile.kafka`, `Dockerfile.mqtt`, `Dockerfile.amqp` — one per shipped transport variant. (Single-transport sources may use a plain `Dockerfile`.)
- `pytest.ini`
- `generate_producer.ps1` — invokes `xrcg` once per transport variant (Kafka + MQTT + AMQP).
- `xreg/<source>.xreg.json` — single manifest declaring **all three** protocol messagegroups + endpoints (see `pegelonline/xreg/pegelonline.xreg.json`).
- `<source>_core/` — shared upstream-acquisition package (HTTP client, parsers, state, dedupe). No transport code.
- `<source>_kafka/` — Kafka bridge app with its own `pyproject.toml` and `app.py`.
- `<source>_mqtt/` — MQTT bridge app with its own `pyproject.toml` and `app.py`.
- `<source>_amqp/` — AMQP 1.0 bridge app with its own `pyproject.toml` and `app.py`.
- `<source>_producer/`, `<source>_mqtt_producer/`, `<source>_amqp_producer/` — generated producer trees (never hand-edited).
- `tests/` — unit + integration tests covering all variants.
- `notebook/<source>-feed.ipynb` — **required for poll-based sources**; copied from `pegelonline/notebook/pegelonline-feed.ipynb` with the substitutions from the Fabric Notebook Hosting section of [`stream-bridge-implementation`](../../stream-bridge-implementation/SKILL.md). Skipped for streaming bridges (WebSocket / MQTT / raw TCP / SSE).
- `kql/<source>.kql` — **required for every source**, generated from the xreg via `tools/generate-kql-from-xreg.ps1 -Qualified`. Reviewed by the KQL Optimizer agent before merge. See the *Mandatory KQL Schema* section in [`stream-bridge-implementation`](../../stream-bridge-implementation/SKILL.md#mandatory-kql-schema-not-optional).
- `kql/create-kql-script.ps1` — thin wrapper that re-runs the generator.
- `azure-template.json` (Kafka → Event Hubs), `azure-template-with-servicebus.json` (AMQP → Service Bus), `azure-template-mqtt.json` (MQTT → Event Grid) where applicable.

In addition:

- `catalog.json` at the repo root must list the new source. For poll-based sources, set `"notebook": true` after the `kql` field so the gh-pages portal exposes the Fabric Notebook deploy button.
- The bridge module must support `--once` (preferred) or `ONCE_MODE=true` so the notebook can run a single polling cycle on a Fabric schedule.

## Repo Conventions

- Use `xrcg` `0.10.7` for producer regeneration.
- Make `generate_producer.ps1` call `tools/require-xrcg.ps1` and fail fast on the wrong generator version.
- Treat `EVENTS.md` as generated documentation derived from the xreg manifest.
- Keep Docker and docs aligned with the runtime behavior and environment variables.
- If the source is new, add it to the root `README.md` container list.

## Definition Of Done

- **The upstream data channel enumeration is complete.** Every MQTT topic tree, REST collection endpoint, WebSocket channel, and file feed has been reviewed and a keep/drop decision documented.
- The upstream study is reflected in the event model and runtime design.
- Stable identifiers are modeled as both CloudEvents subject and Kafka key (and MQTT topic placeholders, and AMQP `application_properties`).
- **All three transport feeders ship by default — Kafka, MQTT, AMQP 1.0** — unless the user explicitly opted out or the source nature (e.g. raw binary decoder with no realistic MQTT/AMQP consumer story) makes a variant unworkable. Any single-transport decision is recorded in `README.md` with rationale.
- **Reference data is modeled and emitted for every source that has metadata endpoints.** If the upstream provides station lists, sensor catalogs, zone definitions, route tables, or entity registries, those are modeled as named reference event types in the xreg manifest and emitted by the bridge at startup and periodically thereafter. Reference events share the same key model and Kafka topic as the telemetry they contextualize.
- The runtime emits reference and telemetry events in a predictable order where applicable.
- Each transport container can be started with its repo-standard configuration (Kafka `CONNECTION_STRING`, MQTT broker URL + creds, AMQP broker URL + SASL or Azure CBS).
- README, CONTAINER, and EVENTS docs match the actual behavior **and include deploy buttons for every shipped variant** (Kafka → Event Hubs, MQTT → Event Grid, AMQP → Service Bus where applicable).
- The Docker E2E test validates both reference and telemetry event types **for every shipped transport** (`test_docker_kafka_flow.py`, `test_docker_mqtt_flow.py`, `test_docker_amqp_artemis_flow.py`, `test_docker_amqp_sb_emulator_flow.py`).
- [`feeder-release-checklist`](../../feeder-release-checklist/SKILL.md) passes for every variant before merge.
- **For poll-based sources:** `<source>/notebook/<source>-feed.ipynb` exists, declares the five required placeholders (`EVENTSTREAM_NAME`, `STATE_FILE`, `POLLING_INTERVAL`, `ONCE_MODE`, `WORKSPACE_ID`), contains no forbidden patterns (`asyncio.run(`, `%pip install`, hardcoded `CONNECTION_STRING=`), and `catalog.json` has `"notebook": true` for the source. The bridge accepts `--once` and exits after one cycle.

## Common Mistakes

- **Stopping the upstream audit after the first two obvious data families.** Walk every API doc subsection, every MQTT topic tree, and every REST collection endpoint. Produce the full hit list before proceeding.
- **Omitting reference data.** If the upstream has station lists, sensor catalogs, zone definitions, or entity metadata, those MUST be modeled as events and emitted by the bridge. Telemetry without reference data forces consumers to fetch context out-of-band, breaking temporal consistency.
- Starting from ad hoc Python dataclasses instead of the xreg manifest.
- Using mutable names or descriptive labels as Kafka keys.
- Combining unrelated identity models in one message group.
- **Forgetting that multiple message groups produce multiple generated producer classes.** If the contract splits the source into several message groups, plan for the runtime to import and instantiate all corresponding `*EventProducer` classes. Do not assume one generated producer wrapper owns every `send_*` method.
- Adding a source folder without container docs or without a generator script.
- Copying a superficially similar source when the transport pattern is wrong.
- **Shipping only a Kafka feeder when the user didn't opt out of MQTT/AMQP.** The default is all three transports (Kafka + MQTT + AMQP) with the pegelonline shared-core layout. Single-transport shortcuts must be justified in `README.md`.
- **Shipping a poll-based source without the notebook artifact and `catalog.json` `notebook: true` flag.** The Fabric Notebook hosting path is a first-class deployment option in this repo; new poll-based sources must expose it from day one rather than being retrofitted later. Forgetting `--once` support in the bridge is the same mistake — the notebook flow requires single-cycle execution.
