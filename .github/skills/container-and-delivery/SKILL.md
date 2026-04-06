---
name: container-and-delivery
description: "Use when packaging or finishing a source for merge in this repo. Covers Dockerfile patterns, CONTAINER.md authoring, Azure Container Instance templates, optional Fabric or KQL assets, EVENTS.md generation, and repo-level delivery checks."
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

## Procedure

1. Add or update the Dockerfile using the delivery patterns in [delivery checklist](references/delivery-checklist.md).
2. Write or update `CONTAINER.md` so the deployment contract matches the runtime behavior.
3. Add `azure-template.json`, `generate-template.ps1`, `kql/`, or `fabric/` assets when the source needs them.
4. Refresh `EVENTS.md` from the xreg manifest.
5. Update the source `README.md` and add the source to the root catalog when it is new.
6. Run the delivery validation checklist before commit or PR.

## Outputs

- a containerized source with deployment docs
- updated delivery assets
- documentation and validation aligned with repo expectations

## References

- [Delivery checklist](references/delivery-checklist.md)