---
name: container-and-delivery
description: "Use when packaging or finishing a source for merge in this repo. Covers Dockerfile patterns, CONTAINER.md authoring, Azure Container Instance templates, optional Fabric or KQL assets, EVENTS.md generation, and repo-level delivery checks including Docker E2E validation."
argument-hint: "Describe the source, its runtime package, required environment variables, deployment target, and whether it needs Azure ACI, Fabric, or KQL artifacts."
---

# Container And Delivery

## When to Use

- Package a new source for Docker-based use.
- Bring a source up to repo merge quality.
- Add Azure Container Instance, Fabric, or KQL delivery assets.

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

## Procedure

1. Add or update the Dockerfile using the delivery patterns in [delivery checklist](references/delivery-checklist.md).
2. Write or update `CONTAINER.md` so the deployment contract matches the runtime behavior.
3. Add `azure-template.json`, `generate-template.ps1`, `kql/`, or `fabric/` assets when the source needs them.
4. Refresh `EVENTS.md` from the xreg manifest.
5. Update the source `README.md` and add the source to the root catalog when it is new.
6. Run the delivery validation checklist before commit or PR.
7. Run the source's Docker E2E test and do not treat the source as finished until it passes the full contract-aware checks.

## Outputs

- a containerized source with deployment docs
- updated delivery assets
- documentation and validation aligned with repo expectations
- a passing Docker E2E test for sources that belong in the shared container suite

## References

- [Delivery checklist](references/delivery-checklist.md)