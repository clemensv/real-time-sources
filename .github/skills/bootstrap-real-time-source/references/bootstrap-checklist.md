# Bootstrap Checklist

## Repo Patterns

- Polling APIs with reference data plus observations: `pegelonline`, `rws-waterwebservices`, `waterinfo-vmm`, `chmi-hydro`, `imgw-hydro`, `hubeau-hydrometrie`
- Continuous websocket or MQTT feeds: `aisstream`, `bluesky`, `digitraffic-maritime`
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

- The upstream study is reflected in the event model and runtime design.
- Stable identifiers are modeled as both CloudEvents subject and Kafka key.
- The runtime emits reference and telemetry events in a predictable order where applicable.
- The container can be started with repo-standard Kafka configuration.
- README, CONTAINER, and EVENTS docs match the actual behavior.

## Common Mistakes

- Starting from ad hoc Python dataclasses instead of the xreg manifest.
- Using mutable names or descriptive labels as Kafka keys.
- Combining unrelated identity models in one message group.
- Adding a source folder without container docs or without a generator script.
- Copying a superficially similar source when the transport pattern is wrong.