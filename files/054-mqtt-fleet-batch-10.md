# 054 MQTT Fleet Batch 10

## Shipped

1. `jma-bosai-warning` — PR #395, merge `097c67d06b8fc9cdfac7c6fb25f3a62ebe7fc87f`
   - Topics:
     - `alerts/jp/jma/jma-bosai-warning/{prefecture}/REFERENCE/{office_code}/{area_code}/office` (retained QoS 1 office reference records)
     - `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/warning` (non-retained QoS 1 weather warning records)
   - Review: xRegistry and UNS approved. Follow-up severity-axis note was addressed by using `REFERENCE`; final reviews were CLEAN.
2. `jma-bosai-quake` — PR #396, merge `e997cd3df711b4546e7948e309d0b83b59039b7c`
   - Topic: `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report`
   - Review: xRegistry and UNS approved. UNS advisory about arbitrary prefecture fallback was addressed by using the closed-vocabulary `unknown` sentinel; final reviews were CLEAN.

## Main CI

- Main was verified green between the two source merges.
- Final main CI after #396: Dependency Graph, Docker E2E Tests, Publish Notebook Wheels, and Build Containers all completed successfully.

## Skipped

- `jma-bosai-volcano` — not started; deferred to preserve source quality and main-green cadence after two JMA source PRs and repeated full main CI waits.
- `jma-bosai-amedas` — not started; deferred for the same reason.
- `jma-japan` — not started; deferred for the same reason.
- `environment-canada` — not started; deferred for the same reason.
- Alternates (`fmi-finland`, `hko-hong-kong`, `canada-aqhi`) — not needed because no prioritized source was blocked; deferred.
