# Contributing

Thanks for your interest in `real-time-sources`. This repo collects
~100 small, independently deployable feeders that pull from real-time
public data sources and forward to a message broker (Kafka, Event Hubs,
Service Bus AMQP, MQTT, or Fabric Event Streams).

## Ways to contribute

- **Add a new source** — propose a public real-time API that isn't
  covered yet and submit a feeder for it.
- **Improve an existing feeder** — bug fixes, missing event types,
  better schemas, better documentation.
- **Improve shared tooling** — the deploy scripts in `tools/`, the CI
  in `.github/workflows/`, the catalog generator, the ghpages portal.
- **Improve docs** — feeder READMEs, root README, the proposals in
  `docs/proposals/`.

## Getting set up

```powershell
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources
# Per-feeder development: each feeder is self-contained
cd feeders/<source>
python -m venv .venv
.venv/Scripts/Activate.ps1   # or `source .venv/bin/activate` on Linux/macOS
pip install -e .[dev]
pytest
```

Most feeders can also be exercised standalone:

```powershell
python -m <source_package> feed --once
```

with the appropriate `CONNECTION_STRING` env var set.

## Repository layout

- `feeders/<source>/` — per-source code, Docker, ARM templates, xreg
  manifest, EVENTS docs, optional Fabric notebook, optional MQTT
  topology.
- `tools/deploy-fabric/` — PowerShell scripts that provision Fabric
  resources and deploy a feeder either as an Azure Container Instance
  or as a Fabric notebook.
- `tools/docs/` — documentation generators (root README catalog,
  per-source hero, per-source deploy section).
- `tests/docker_e2e/` — Docker-based end-to-end test harness.
- `.github/workflows/` — CI for builds, tests, container publishing,
  doc regeneration.
- `.github/skills/` — agent-readable runbooks for repeated tasks
  (release checklist, xreg authoring, MQTT topology, etc.).
- `app.js` + `catalog.json` — the static ghpages portal at
  https://clemensv.github.io/real-time-sources/

## Conventions

- Feeders use the **xRegistry** message catalog under
  `feeders/<source>/xreg/` and generate producers via the local
  `generate_producer.ps1` script. Do **not** hand-edit generated files.
- Schemas use **JSON Structure** (`.struct.json`). Read the JSON
  Structure spec before authoring a new schema; we enforce nullability
  parity, English field names, and exhaustive descriptions.
- Bridges read configuration from environment variables. The standard
  set is `CONNECTION_STRING`, `KAFKA_TOPIC` (where applicable),
  `POLLING_INTERVAL`, `ONCE_MODE`, `STATE_FILE`.
- New feeders must include a README, a CONTAINER.md (for the published
  image), an `azure-template.json` (and `azure-template-with-eventhub.json`),
  an `EVENTS.md` generated from the xreg manifest, and unit tests.
  The release checklist at
  `.github/skills/feeder-release-checklist/SKILL.md` is the
  authoritative reference.

## Commit messages

We use conventional-commit prefixes (`fix:`, `feat:`, `docs:`,
`refactor:`, `chore:`, `ci:`). Keep the subject under ~72 chars and use
the body to explain *why*, not *what*.

## Pull requests

- Keep PRs focused. One feeder per PR for new sources.
- CI must be green. Don't merge red.
- Update docs alongside code changes.
- We squash-merge. The PR title becomes the squash commit subject.

## Code of conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating you agree to abide by it.

## License

By contributing you agree your contribution will be licensed under the
[MIT License](LICENSE.md) that covers this project.
