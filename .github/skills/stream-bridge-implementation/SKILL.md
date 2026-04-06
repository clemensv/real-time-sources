---
name: stream-bridge-implementation
description: "Use when implementing the runtime bridge for a source in this repo. Covers pollers, websocket or MQTT clients, raw TCP decoders, state and dedupe logic, generated producer wiring, and source-local testing."
argument-hint: "Describe the transport, auth, polling or reconnect behavior, resume state needs, and the event families the runtime must emit."
---

# Stream Bridge Implementation

## When to Use

- Implement a new runtime bridge after the xreg contract is clear.
- Refactor a runtime to align with regenerated producer output.
- Add state, dedupe, reconnect, or emit-order logic.

## Inputs

- transport type and auth model
- poll or reconnect behavior
- state and dedupe requirements
- generated producer methods and placeholder arguments

## Procedure

1. Choose the runtime pattern that matches the source: poller, websocket, MQTT, or raw TCP.
2. Structure the bridge using the runtime patterns in [runtime checklist](references/runtime-checklist.md).
3. Parse source configuration and Kafka configuration from CLI args and environment variables.
4. Normalize upstream payloads into generated data classes and pass subject or key placeholders explicitly.
5. Add state, dedupe, reconnect, and emit-order behavior where the source requires it.
6. Add unit and integration tests, and keep Docker compatibility in mind if the source should join the repo-wide container tests.

## Outputs

- a runtime bridge aligned with the xreg contract
- consistent producer calls with explicit placeholder values
- source-local tests that cover parsing, state, and emission behavior

## References

- [Runtime checklist](references/runtime-checklist.md)