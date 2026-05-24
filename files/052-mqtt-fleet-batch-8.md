# 052 MQTT Fleet Batch 8

## Shipped

1. `gracedb` — PR #385, merge `00b7996a68eb3bb798c82ef2b8fa03626d47abea`
   - Topic: `seismic/intl/ligo/gracedb/{category}/{group}/{superevent_id}/superevent`
   - Review: xRegistry and UNS approved; non-blocking CloudEvents timestamp normalization follow-up noted.
2. `vatsim` — PR #386, merge `c9caad0c8e8d474a2b620e1e477ea68e9632638d`
   - Topics: pilots/controllers/facilities split, no `{role}` placeholder.
   - Review: xRegistry and UNS approved; non-blocking facility-status retain+expiry follow-up noted.
3. `entur-norway` — PR #387, merge `8c30130dfc24f4c780faa463cf90cc301c5fb974`
   - Topics: SIRI ET, VM, SX routed by raw payload fields with `unknown` fallback.
   - Review: xRegistry and UNS approved; non-blocking SX severity-axis follow-up noted.
4. `eaws-albina` — PR #388, merge `3c198ae84e743a8b0305d6848d36a962a41c8273`
   - Topic: `alerts/at/eaws/eaws-albina/{country}/{region_id}/{danger_level}/bulletin`
   - Review: xRegistry and UNS approved; no blocking findings.

## Main CI

- Main was verified green between every merge.
- Final main CI after #388: Dependency Graph, Docker E2E Tests, Publish Notebook Wheels, and Build Containers all completed successfully.

## Skipped

- `gdacs` — not started; remaining ready candidate, deferred to preserve quality and main-green cadence.
- `meteoalarm` — not started; remaining ready candidate, deferred to preserve quality and main-green cadence.
