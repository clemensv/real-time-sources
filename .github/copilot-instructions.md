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
  kql/                              # optional
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
