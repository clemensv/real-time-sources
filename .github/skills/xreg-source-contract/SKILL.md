---
name: xreg-source-contract
description: "Use when designing or changing event contracts for this repo. Covers CloudEvents modeling, xreg message groups, stable subject and Kafka key selection, regeneration with xrcg 0.10.1, and EVENTS.md refresh."
argument-hint: "Describe the source, event families, stable identifier shape, and whether multiple families share one identity or need separate message groups."
---

# Xreg Source Contract

## When to Use

- Add a new xreg manifest for a source.
- Change CloudEvents subject or Kafka key modeling.
- Split one source into multiple message groups or endpoints.
- Refresh generated producers after contract changes.

## Inputs

- source name and upstream system
- event families and their stable identifiers
- desired CloudEvents types, source values, and schema formats

## Procedure

1. Identify the real entity or time-series identity for each event family.
2. Decide whether the families can share one endpoint or need separate key models.
3. Update the checked-in manifest under `xreg/` and model `type`, `source`, and `subject` deliberately.
4. Apply the repo keying rules and validation points in [contract checklist](references/contract-checklist.md).
5. Regenerate producer output with the source-local `generate_producer.ps1` script.
6. Sync any runtime wrappers that call the generated producer so subject and key behavior stay aligned.
7. Refresh `EVENTS.md` from the manifest.

## Outputs

- an updated xreg manifest
- regenerated producer artifacts
- refreshed runtime wiring and event documentation

## References

- [Contract checklist](references/contract-checklist.md)