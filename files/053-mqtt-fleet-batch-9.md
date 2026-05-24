# 053 MQTT Fleet Batch 9

## Shipped

1. `gdacs` — PR #390, merge `8ccb37573bd3153de8dace7ed6cc06ed13c6e4a0`
   - Topic: `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert`
   - Review: xRegistry and UNS approved after fixing MQTT endpoint shape, event/alert routing guards, and topic sanitization; no final blockers.
2. `meteoalarm` — PR #391, merge `c4ed253d6f825a2a2388540c7ffa95fb5e837143`
   - Topic: `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning`
   - Review: xRegistry and UNS approved; awareness type is normalized for MQTT routing while retaining the raw CAP parameter.
3. `ptwc-tsunami` — PR #392, merge `a15181491e9f913d8ad46ff373623feedb3c1e1c`
   - Topic: `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin`
   - Review: xRegistry and UNS approved; basin and ptwc_level routing axes are schema-backed and non-null.
4. `nina-bbk` — PR #393, merge `2db32ac5003182ce4f739aa7cd7a381d78ec57e5`
   - Topic: `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning`
   - Review: xRegistry and UNS approved; state is derived from CAP area administrative codes with sender fallback.

## Main CI

- Main was verified green between every merge.
- Final main CI after #393: Dependency Graph, Docker E2E Tests, Publish Notebook Wheels, and Build Containers all completed successfully.

## Skipped

- `jma-bosai-warning` — not started; deferred to preserve quality and main-green cadence after four alert/bulletin source PRs.
- `jma-bosai-quake` — not started; deferred to preserve quality and main-green cadence after four alert/bulletin source PRs.
