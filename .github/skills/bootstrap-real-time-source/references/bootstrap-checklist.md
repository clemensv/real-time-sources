# Bootstrap Checklist

## Repo Patterns

- Polling APIs with reference data plus observations: `pegelonline`, `rws-waterwebservices`, `waterinfo-vmm`, `chmi-hydro`, `imgw-hydro`, `hubeau-hydrometrie`
- Continuous websocket or MQTT feeds with REST reference data: `aisstream`, `bluesky`, `digitraffic-maritime`
- Raw TCP decode pipelines: `kystverket-ais`
- Multi-family or domain-partitioned polling sources: `dwd`, `entsoe`, `gtfs`

## Standard Source Layout

- `README.md`
- `CONTAINER.md`
- `EVENTS.md`
- `Dockerfile`
- `pyproject.toml`
- `pytest.ini`
- `generate_producer.ps1`
- `xreg/<source>.xreg.json`
- runtime package like `<source>/<source>.py` or `bridge.py`
- generated producer output like `<source>_producer/` or `<source>_producer_tmp/`
- `tests/`
- optional `azure-template.json`, `generate-template.ps1`, `kql/`, or `fabric/`

## Repo Conventions

- Use `xrcg` `0.10.1` for producer regeneration.
- Make `generate_producer.ps1` call `tools/require-xrcg.ps1` and fail fast on the wrong generator version.
- Treat `EVENTS.md` as generated documentation derived from the xreg manifest.
- Keep Docker and docs aligned with the runtime behavior and environment variables.
- If the source is new, add it to the root `README.md` container list.

## Definition Of Done

- **The upstream data channel enumeration is complete.** Every MQTT topic tree, REST collection endpoint, WebSocket channel, and file feed has been reviewed and a keep/drop decision documented.
- The upstream study is reflected in the event model and runtime design.
- Stable identifiers are modeled as both CloudEvents subject and Kafka key.
- **Reference data is modeled and emitted for every source that has metadata endpoints.** If the upstream provides station lists, sensor catalogs, zone definitions, route tables, or entity registries, those are modeled as named reference event types in the xreg manifest and emitted by the bridge at startup and periodically thereafter. Reference events share the same key model and Kafka topic as the telemetry they contextualize.
- The runtime emits reference and telemetry events in a predictable order where applicable.
- The container can be started with repo-standard Kafka configuration.
- README, CONTAINER, and EVENTS docs match the actual behavior.
- The Docker E2E test validates both reference and telemetry event types where applicable.

## Common Mistakes

- **Stopping the upstream audit after the first two obvious data families.** Walk every API doc subsection, every MQTT topic tree, and every REST collection endpoint. Produce the full hit list before proceeding.
- **Omitting reference data.** If the upstream has station lists, sensor catalogs, zone definitions, or entity metadata, those MUST be modeled as events and emitted by the bridge. Telemetry without reference data forces consumers to fetch context out-of-band, breaking temporal consistency.
- Starting from ad hoc Python dataclasses instead of the xreg manifest.
- Using mutable names or descriptive labels as Kafka keys.
- Combining unrelated identity models in one message group.
- **Forgetting that multiple message groups produce multiple generated producer classes.** If the contract splits the source into several message groups, plan for the runtime to import and instantiate all corresponding `*EventProducer` classes. Do not assume one generated producer wrapper owns every `send_*` method.
- Adding a source folder without container docs or without a generator script.
- Copying a superficially similar source when the transport pattern is wrong.
