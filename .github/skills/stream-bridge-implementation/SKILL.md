---
name: stream-bridge-implementation
description: "Use when implementing the runtime bridge for a source in this repo. Covers pollers, websocket or MQTT clients, raw TCP decoders, family-aware normalization, generated producer wiring, state and dedupe logic, and source-local testing."
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

## Non-Negotiables

- The runtime is not allowed to paper over a sloppy contract.
- If generated producer methods or upstream subtype signals imply more event families than the bridge emits, stop and fix the contract first.
- Do not normalize semantically different upstream shapes into one generic dict or class just because the transport loop is shared.
- Preserve the family-specific fields and discriminators that justified the contract split in the first place.
- Do not patch, rewrite, or vendor modified copies of `xrcg`-generated producer or data-class code to make the runtime work; import and use the generated packages as emitted.
- The bridge must emit Kafka keys, CloudEvent subjects, and payload shapes that satisfy the checked-in xreg contract, including nullability behavior.
- Runtime work for a new source is not complete until the relevant repo-level Docker E2E test passes when the source is meant to participate in the shared container test suite.
- If Docker E2E reports key, subject, or JsonStructure schema failures, treat that as contract or runtime drift and fix the source instead of weakening the test.
- When Docker E2E evidence is needed for manual verification or debugging, the harness must support an explicit opt-in parameter that writes consumed Kafka messages and container logs to disk.

## Procedure

1. Choose the runtime pattern that matches the source: poller, websocket, MQTT, or raw TCP.
2. Structure the bridge using the runtime patterns in [runtime checklist](references/runtime-checklist.md).
3. Parse source configuration and Kafka configuration from CLI args and environment variables.
4. Normalize upstream payloads into the correct generated data classes per family and pass subject or key placeholders explicitly, matching the xreg-declared shape and nullability rules, while consuming the generated producer packages unchanged.
5. Add state, dedupe, reconnect, and emit-order behavior where the source requires it without erasing family-specific meaning.
6. Add unit and integration tests, and keep Docker compatibility in mind if the source should join the repo-wide container tests.
7. Run the relevant Docker E2E test and treat failures there as unfinished implementation work, not optional follow-up.

## Outputs

- a runtime bridge aligned with the xreg contract
- consistent producer calls with explicit placeholder values
- source-local tests that cover parsing, state, and emission behavior
- a passing repo-level Docker E2E test when the source participates in the shared container suite

## References

- [Runtime checklist](references/runtime-checklist.md)