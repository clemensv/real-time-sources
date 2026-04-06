---
name: bootstrap-real-time-source
description: Use this skill when planning or adding a new real-time source in this repo. Covers source study, repo fit, choosing poller vs websocket or MQTT or raw TCP bridge, selecting stable event identities, mapping reference and telemetry event families, laying out the source folder, sequencing xreg work, code generation, runtime implementation, container packaging, Azure Container Instance setup, and final documentation.
argument-hint: Describe the upstream source, transport, auth model, cadence, stable identifiers, expected event families, and whether the source is a poller or a continuous stream.
user-invocable: true
---

This repo is schema-first and container-first. Start from the checked-in xreg manifest and the runtime contract you want to expose, then implement the bridge around that contract.

Use the closest existing source as a template instead of inventing a new project shape.

Good analogs by transport and behavior:

- Polling APIs with reference data plus observations: `pegelonline`, `rws-waterwebservices`, `waterinfo-vmm`, `chmi-hydro`, `imgw-hydro`, `hubeau-hydrometrie`
- Continuous websocket or MQTT feeds: `aisstream`, `bluesky`, `digitraffic-maritime`
- Raw TCP decode pipelines: `kystverket-ais`
- Multi-family or domain-partitioned polling sources: `dwd`, `entsoe`, `gtfs`

Work in this order:

1. Study the upstream source before writing code.
   Capture transport, auth, rate limits, refresh cadence, replay or resume support, timezone rules, stable identifiers, data volume, and whether the source emits reference entities, telemetry, alerts, or all three.

2. Decide whether the source fits the repo.
   This repo is for bridges that emit CloudEvents to Kafka-compatible endpoints and package cleanly as a Docker container. If the source does not naturally map to an event stream, narrow the scope until it does.

3. Pick the stable domain identity up front.
   Do not start with field lists. Start with the identifier that should become CloudEvents `subject` and the Kafka key. Good examples are station IDs, vessel MMSI, alert IDs, agency IDs, or time-series IDs.

4. Split the source into event families.
   Decide which records are reference data and which are telemetry. If the upstream source mixes materially different identity shapes, plan separate message groups or even separate endpoints instead of forcing one key model across all events.

5. Lay out the project folder before implementation.
   A full source usually needs:

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

6. Model the events in xreg, then generate the producer, then implement the bridge.
   Keep the checked-in `xreg/*.xreg.json` manifest as the source of truth. Do not hand-maintain generated producer code first and retrofit the manifest later.

7. Build the runtime around the generated producer contract.
   The runtime should fetch or receive upstream data, normalize it into the generated data classes, and call the generated producer methods with the subject or key placeholder values that the xreg model requires.

8. Package the source as a container and document it as a product.
   Every mergeable source should be runnable via Docker with Kafka-compatible connection settings. If the source should be deployable to Azure Container Instances, add the matching template and instructions.

9. Validate the source at the same level as the rest of the repo.
   Add source-local tests, build the Docker image, and if the container is meant to participate in the repo-wide Docker flow tests, make sure it can run against plain Kafka via `CONNECTION_STRING=BootstrapServer=...;EntityPath=...`.

Required repo conventions:

- Use `xrcg` `0.10.1` for producer regeneration.
- Make `generate_producer.ps1` call `tools/require-xrcg.ps1` and fail fast on the wrong generator version.
- Treat `EVENTS.md` as generated documentation derived from the xreg manifest.
- Keep Docker and docs aligned with the runtime behavior and environment variables.
- If the source is new, add it to the root `README.md` container list.

Definition of done:

- The upstream study is reflected in the event model and runtime design.
- Stable identifiers are modeled as both CloudEvents subject and Kafka key.
- The runtime emits reference and telemetry events in a predictable order where applicable.
- The container can be started with repo-standard Kafka configuration.
- README, CONTAINER, and EVENTS docs match the actual behavior.

Avoid these mistakes:

- Starting from ad hoc Python dataclasses instead of the xreg manifest.
- Using mutable names or descriptive labels as Kafka keys.
- Combining unrelated identity models in one message group.
- Adding a source folder without container docs or without a generator script.
- Copying a superficially similar source when the transport pattern is wrong.