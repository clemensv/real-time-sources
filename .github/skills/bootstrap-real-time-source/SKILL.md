---
name: bootstrap-real-time-source
description: "Use when planning or adding a new real-time source in this repo. Covers source study, repo fit, transport choice, event-family scoping, folder layout, and sequencing xreg, runtime, container, and documentation work."
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

## Procedure

1. Study the upstream source and identify the stable domain identity.
2. Choose the closest repo pattern from [bootstrap checklist](references/bootstrap-checklist.md).
3. Decide whether the source should be a poller, websocket client, MQTT consumer, or raw TCP bridge.
4. Split the source into event families and determine whether their identities can share one message group.
5. Lay out the source folder using the scaffold in [bootstrap checklist](references/bootstrap-checklist.md).
6. Use `xreg-source-contract` for contract work, `stream-bridge-implementation` for runtime work, and `container-and-delivery` for packaging and documentation.

## Outputs

- a scoped source plan
- a chosen analog source
- a project layout
- a stable identity model
- an ordered work breakdown

## References

- [Bootstrap checklist](references/bootstrap-checklist.md)