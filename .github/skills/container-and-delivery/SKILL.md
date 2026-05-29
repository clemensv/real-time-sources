---
name: container-and-delivery
description: "Use when packaging or finishing a source for merge in this repo. Covers Dockerfile patterns, CONTAINER.md authoring, Azure Container Instance templates, mandatory KQL schema script generation + KQL Optimizer review, optional Fabric assets, EVENTS.md generation, and repo-level delivery checks including Docker E2E validation."
argument-hint: "Describe the source, its runtime package, required environment variables, deployment target, and whether it needs Azure ACI, Fabric, or KQL artifacts."
---

# Container And Delivery

## When to Use

- Package a new source for Docker-based use.
- Bring a source up to repo merge quality.
- Add Azure Container Instance, Fabric, or KQL delivery assets.
- **Packaging an MQTT sibling alongside a Kafka feeder** (separate
  `Dockerfile.mqtt`, MQTT-specific pyproject, the two MQTT ARM
  templates, MQTT Docker E2E, and the `mqtt: true` portal flag) — see
  the `mqtt-uns-feeder` skill for the MQTT delta over this baseline.

## Inputs

- source name and runtime package
- required environment variables and credentials model
- target deployment path, including Docker, ACI, Event Hubs, Fabric, or KQL

## Non-Negotiables

- A containerized source is not merge-ready because the image builds, starts, or passes unit tests.
- If the source is expected to participate in the shared Docker Kafka flow suite, the work is not done until that E2E test is passing.
- The shared Docker Kafka flow suite is a contract-aware test: it consumes emitted records and validates Kafka keys, CloudEvent subjects, and payload schemas against the checked-in xreg manifest.
- A red Docker E2E result means the delivery work is incomplete.
- Do not dismiss key, subject, or schema failures there as harness noise; they usually mean contract or runtime drift that must be fixed before merge.
- Delivery work must package and install `xrcg`-generated producer artifacts as generated. Do not copy patched generated Python into the runtime package or rely on post-generation fixups as a container workaround.
- The Docker E2E harness must offer an explicit opt-in parameter for writing consumed Kafka messages and container logs to disk when delivery verification artifacts are needed.
- **`<source>/kql/<source>.kql` is mandatory, not optional.** Generated from the xreg manifest via `tools/generate-kql-from-xreg.ps1 -Qualified`, committed to the repo, referenced from `catalog.json`, and reviewed by the **KQL Optimizer** agent. Without it, the Fabric deployers log "No KQL script — database schema step will be skipped" and the deployed database has no typed tables, no update policies, and no `*Latest` materialized views — every downstream KQL consumer is broken. See the **Mandatory KQL Schema** section in [stream-bridge-implementation](../stream-bridge-implementation/SKILL.md#mandatory-kql-schema-not-optional).
- **Fabric notebook deployment correctness is a blocking review criterion.** If the source ships `feeders/<slug>/notebook/<slug>-feed.ipynb`, the PR MUST pass `pwsh tools/validate-fabric-deployment.ps1 -FeederSlug <slug>` with zero blockers AND have been deployed end-to-end to a real Fabric workspace (one scheduled run observed reaching `KQL count > 0`) within the last 30 days. The validator catches the silent failure modes — `asyncio.run` in cells, `%pip install` magic, missing OneLake state-file path, missing `notebookutils.notebook.exit` failure handler, `CONNECTION_STRING` exposed as a notebook parameter, broken post-deploy hooks, and catalog ↔ notebook opt-in drift (the single most common cause of "the button doesn't show up on the portal"). See the [`fabric-notebook-deployment`](../fabric-notebook-deployment/SKILL.md) skill for the full check list and the `notebook: true` flag handling in both `catalog.json` and the ghpages `app.js` SOURCES list.
- **ARM template correctness is a blocking review criterion, not a soft check.** Every `azure-template-*.json` the source ships must have a non-empty `resources` array, expose every required feeder env var as an ARM parameter with `metadata.description`, use the right container image suffix for the transport family, and pass a live deploy via `pwsh tools/verify-arm-template.ps1 -FeederSlug <slug> -Variant <variant>` (creates RG → deploys → observes data flow → tears down). An "empty placeholder" template (`"resources": []`) is the single most common silent regression in this repo because the deploy button "succeeds" and creates an empty resource group. Audit before merge with `pwsh tools/validate-arm-templates.ps1 -RepoRoot .` and reject any PR that introduces or leaves an empty template behind. Hand-editing per-feeder templates for fleet-wide parameter changes is also a red flag — regenerate from the aisstream canonicals via `python tools/generate-arm-templates.py` and let every feeder pick up the change uniformly.

## Procedure

1. Add or update the Dockerfile using the delivery patterns in [delivery checklist](references/delivery-checklist.md).
2. Write or update `CONTAINER.md` so the deployment contract matches the runtime behavior.
3. **Generate `<source>/kql/<source>.kql`** from the xreg manifest with `tools/generate-kql-from-xreg.ps1 -Qualified`. Commit the script and a thin `kql/create-kql-script.ps1` wrapper. Add the `kql` key to the source's `catalog.json` entry.
4. Add `azure-template.json`, `generate-template.ps1`, or `fabric/` assets when the source needs them. **Every `azure-template-*.json` MUST have a non-empty `resources` array** — never commit an empty placeholder. Generate fleet-wide via `python tools/generate-arm-templates.py` rather than hand-editing, expose every required feeder env var as an ARM parameter with `metadata.description`, and verify with `pwsh tools/verify-arm-template.ps1 -FeederSlug <slug> -Variant <variant>` before opening the PR. This is enforced as a blocking review criterion in the delivery checklist.
5. Refresh `EVENTS.md` from the xreg manifest.
6. Update the source `README.md` and add the source to the root catalog when it is new.
7. Run the delivery validation checklist before commit or PR.
8. Run the source's Docker E2E test and do not treat the source as finished until it passes the full contract-aware checks.
9. **Dispatch a KQL Optimizer review** of the generated `<source>/kql/<source>.kql` before opening the delivery PR. The reviewer must read the actual script and the xreg manifest, confirm that every event type has a typed table + update policy + JSON mappings, confirm reference event types have `*Latest` materialized views, and call out inefficient projections or missing type coercions. Treat blocking findings as merge blockers.

## Outputs

- a containerized source with deployment docs
- updated delivery assets
- documentation and validation aligned with repo expectations
- a passing Docker E2E test for sources that belong in the shared container suite

## References

- [Delivery checklist](references/delivery-checklist.md)