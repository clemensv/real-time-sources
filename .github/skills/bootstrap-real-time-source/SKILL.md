---
name: bootstrap-real-time-source
description: "Use when planning or adding a new real-time source in this repo. Covers mandatory upstream docs and field review, required JSON Structure Core and extension-spec study for schema work, repo fit, transport choice, event-family scoping, folder layout, and sequencing xreg, runtime, container, and documentation work."
argument-hint: "Describe the upstream source, transport, auth model, cadence, stable identifiers, and expected event families."
---

# Bootstrap Real-Time Source

## When to Use

- Add a brand-new source folder to this repo.
- Turn a rough source idea into an ordered implementation plan.
- Choose the right repo analog before writing xreg or runtime code.

## Inputs

- Upstream source name and endpoint
- transport, auth, refresh cadence, replay behavior, and expected volume
- stable identifiers and expected reference, telemetry, or alert families

## Non-Negotiables

- Do not infer the contract from one convenient list payload and call it done.
- Read the upstream docs or OpenAPI and inspect representative live payloads before you name event families or schemas.
- **Enumerate every available data channel exhaustively.** List every MQTT topic tree, every REST collection endpoint, every WebSocket channel, and every file feed the upstream exposes. Do not stop at the first two obvious families. Walk the full upstream API index page, topic namespace, or OpenAPI tag list and confirm each channel was reviewed. If the upstream docs have a "Data" or "MQTT" section, read every subsection, not just the ones that sound familiar. Probe topics you are unsure about with live requests. Produce an explicit hit list of every data family the source offers, then justify keeping or dropping each one before proceeding to contract authoring.
- If the source will require JsonStructure schema work, read JSON Structure Core and the relevant extension specs during planning; they are part of the required curriculum for this workflow.
- Collect the upstream field descriptions, units, aliases, enums, and validation rules before you hand off schema work; payload shape alone is not enough.
- If the source exposes detail endpoints, subtype enums, or `display_type`-style discriminators, review them before deciding anything about family boundaries.
- Flattening semantically different upstream entities into one generic catch-all item is a modeling error, not an acceptable simplification.
- **Every source that exposes reference data must emit it as events.** Reference data (station metadata, sensor catalogs, route definitions, zone lists, vessel registries, task type catalogs) is not fundamentally different from telemetry; it differs only in update frequency. Treating reference data as out-of-band context that consumers must fetch themselves breaks temporal consistency in downstream analytics. Model reference data as named event types in the xreg manifest, fetch it via REST at bridge startup (and periodically thereafter), and emit it as CloudEvents into the same Kafka topic(s) as the telemetry it contextualizes. The reference article for this pattern is: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events
- Plan to consume `xrcg` output as generated. Do not design a source around post-generation Python edits, vendored rewrites, or import-fixup scripts as a normal integration step.
- If the upstream review is not strong enough to support exhaustive field descriptions in the eventual schemas, the source is not ready for contract authoring.
- A new source is not done when the manifest generates or the unit tests pass; it is done when the source's repo-level Docker E2E test is passing if the source is expected to ship as a containerized bridge.
- **Poll-based sources must ship a Fabric notebook alongside the container.** If the bridge is a poller (HTTP/file fetch on a fixed cadence, not a long-lived stream), the source's deliverables include `<source>/notebook/<source>-feed.ipynb` and a `notebook: true` flag in `catalog.json`, so the gh-pages portal exposes the Fabric Notebook deploy button. Streaming bridges (WebSocket / MQTT / raw TCP / SSE firehose) do not qualify and must skip the notebook artifact. See the Fabric Notebook Hosting section of [`stream-bridge-implementation`](../stream-bridge-implementation/SKILL.md) for the canonical pegelonline pattern; new sources follow the same shape from day one rather than being retrofitted later.
- **Every new source ships all three transport feeders by default: Kafka, MQTT, and AMQP 1.0.** Unless the user (or an upstream constraint such as a binary-protocol decoder with no realistic MQTT/AMQP consumer story) explicitly tells you to skip one, plan the source from day one as a multi-transport feeder with the pegelonline layout: a shared `<source>_core/` acquisition package plus three sibling apps `<source>_kafka/`, `<source>_mqtt/`, `<source>_amqp/`, each with its own generated producer tree, `pyproject.toml`, `Dockerfile.kafka` / `Dockerfile.mqtt` / `Dockerfile.amqp`, and matching xRegistry messagegroup + endpoint. The xreg manifest declares all three protocol bindings in the same file; the bridges share data acquisition but never publish to more than one transport per process. Document any decision to ship fewer than three variants in the source's `README.md` with the reason. See [`mqtt-uns-feeder`](../mqtt-uns-feeder/SKILL.md) and [`amqp-feeder`](../amqp-feeder/SKILL.md) for the per-transport mechanics, and [`feeder-release-checklist`](../feeder-release-checklist/SKILL.md) for the documentation, deploy-button, and schema-quality gates that all three variants must pass before merge.
- **Generalize the feeder, don't fork it.** Before scaffolding a new source, check whether its upstream speaks a *standardized* protocol family the repo already serves with a **generalized, config-driven** feeder. The repo's generalized feeders are: `gtfs` / `siri` (GTFS-RT & SIRI transit, multi-agency), `gbfs-bikeshare` (GBFS micromobility, `GBFS_FEEDS` URL list), `fdsn-seismology` (federated FDSN seismic node list), and `rss` (multi-feed). If the new source fits one of these, it is **not a new source** — it is a config entry (a feed URL / FDSN node / agency added to the existing feeder's list). Do not create a new folder. Conversely, if several candidate sources share one standardized protocol with no generalized feeder yet (e.g. DATEX II road traffic, CAP alerts, OpenAQ air quality, ERDDAP ocean grids, ArcGIS FeatureServer), build **one** config-driven feeder for the family — a shared core that takes a list of endpoints/instances — rather than N near-identical bespoke feeders. A bespoke feeder that duplicates a generalized one (the way `tokyo-docomo-bikeshare` duplicates `gbfs-bikeshare`, or `entur-norway` / `uk-bods-siri` duplicate `siri`) is technical debt to fold back in, not a pattern to copy. The candidate backlog at `tools/candidates/IMPLEMENTATION-RANKING.md` ("Generalization strategy" section) tracks which families are already generalized and which clusters are worth generalizing.

## Procedure

1. Study the authoritative upstream docs, read JSON Structure Core and the relevant extension specs if the source will need schema work, and inspect representative live list and detail payloads, then identify the stable domain identity and extract the field descriptions, units, aliases, enums, and validation rules the schema will need.
2. **Enumerate all available data channels.** Walk the full upstream API index, MQTT topic namespace, WebSocket message types, or OpenAPI tag list. For each channel, probe a live payload to confirm its shape and volume. Produce an explicit table of every data family with columns: family name, transport (MQTT topic / REST endpoint / WS channel), identity shape, update cadence, and keep/drop decision with justification. This table is a gate: do not proceed to contract authoring until it is complete.
3. **Identify reference data.** For every telemetry family, determine whether the upstream provides metadata about the entities that telemetry describes (stations, sensors, vehicles, zones, routes, task types). If so, plan a reference data event type that will be fetched via REST at startup and periodically refreshed. Reference data and telemetry share the same key model and go to the same Kafka topic so consumers can build temporally consistent views. If the upstream provides no useful metadata endpoint, document that explicitly.
4. Choose the closest repo pattern from [bootstrap checklist](references/bootstrap-checklist.md). **First check whether the source is merely a config of a generalized feeder** (`gtfs`/`siri`, `gbfs-bikeshare`, `fdsn-seismology`, `rss`) — if so, add the feed/node to that feeder's list instead of scaffolding a new source. If multiple candidates share one standardized protocol with no generalized feeder yet, generalize one config-driven feeder for the family rather than forking N bespoke builds.
5. Decide whether the source should be a poller, websocket client, MQTT consumer, or raw TCP bridge.
6. **Plan all three transport feeders by default — Kafka, MQTT, and AMQP 1.0 — unless the user explicitly says otherwise or the source's nature makes a variant nonsensical.** Use the pegelonline shape: shared `<source>_core/` acquisition module + three sibling apps `<source>_kafka/`, `<source>_mqtt/`, `<source>_amqp/`. The xreg manifest declares Kafka, MQTT, and AMQP messagegroups/endpoints in a single file (see `pegelonline/xreg/pegelonline.xreg.json`). Each variant gets its own `Dockerfile.<transport>` and its own generator invocation in `generate_producer.ps1`. Streaming sources (WebSocket / raw TCP) still get all three publish-side variants — only the upstream acquisition is shared. If you intend to ship fewer variants, record the rationale in `README.md` before starting contract work.
7. Split the source into event families (including reference types) and determine whether their identities can share one message group, preserving meaningful upstream schema and subtype distinctions unless you can prove they are semantically identical.
8. Lay out the source folder using the scaffold in [bootstrap checklist](references/bootstrap-checklist.md).
9. Use `xreg-source-contract` for contract work, `stream-bridge-implementation` for runtime work, [`mqtt-uns-feeder`](../mqtt-uns-feeder/SKILL.md) and [`amqp-feeder`](../amqp-feeder/SKILL.md) for the non-Kafka transports, and `container-and-delivery` for packaging and documentation.
10. **If the source is a poller, add a Fabric notebook hosting option.** Copy `pegelonline/notebook/pegelonline-feed.ipynb` verbatim, perform the substitutions in `.github/skills/stream-bridge-implementation/references/notebook-substitution-table.md`, place the result at `<source>/notebook/<source>-feed.ipynb`, and set `notebook: true` in the source's `catalog.json` entry. Ensure the bridge supports `--once` (single-cycle execution) — this is mandatory for the notebook flow because Fabric runs the notebook on a schedule, not as a daemon. Skip this step for streaming bridges.
11. Treat the source as incomplete until its expected repo-level Docker E2E coverage is passing **for every shipped transport variant** (Kafka, MQTT Mosquitto, AMQP Artemis, AMQP SB-emulator) **and the mandatory expert review (xRegistry, JSON Structure, Avro Schema) defined in [`stream-bridge-implementation`](../stream-bridge-implementation/SKILL.md) has signed off and [`feeder-release-checklist`](../feeder-release-checklist/SKILL.md) passes for every variant.**

## Outputs

- a scoped source plan
- a chosen analog source
- a project layout
- a stable identity model
- an ordered work breakdown

## References

- [Bootstrap checklist](references/bootstrap-checklist.md)
- [`xreg-source-contract`](../xreg-source-contract/SKILL.md) — contract authoring
- [`stream-bridge-implementation`](../stream-bridge-implementation/SKILL.md) — runtime
- [`container-and-delivery`](../container-and-delivery/SKILL.md) — packaging
- [`notebook substitution table`](../stream-bridge-implementation/references/notebook-substitution-table.md) — Fabric notebook hosting pattern (folded into stream-bridge-implementation)
- [`fabric-notebook-deployment`](../fabric-notebook-deployment/SKILL.md) — how the notebook gets deployed
- JSON Structure Core: https://json-structure.github.io/core/draft-vasters-json-structure-core.html
- JSON Structure Alternate Names and Descriptions: https://json-structure.github.io/alternate-names/draft-vasters-json-structure-alternate-names.html
- JSON Structure Symbols, Scientific Units, and Currencies: https://json-structure.github.io/units/draft-vasters-json-structure-units.html
- JSON Structure Validation Extensions: https://json-structure.github.io/validation/draft-vasters-json-structure-validation.html
- JSON Structure Conditional Composition: https://json-structure.github.io/conditional-composition/draft-vasters-json-structure-cond-composition.html
- JSON Structure Import: https://json-structure.github.io/import/draft-vasters-json-structure-import.html