# MQTT Fleet Decision Inventory

## Already-shipped

- `gracedb` — PR #385, merge `00b7996a68eb3bb798c82ef2b8fa03626d47abea`; topic `seismic/intl/ligo/gracedb/{category}/{group}/{superevent_id}/superevent`.
- `vatsim` — PR #386, merge `c9caad0c8e8d474a2b620e1e477ea68e9632638d`; topics:
  - `aviation-network/intl/vatsim/vatsim/pilots/{callsign}/pilot-position`
  - `aviation-network/intl/vatsim/vatsim/controllers/{callsign}/controller-position`
  - `aviation-network/intl/vatsim/vatsim/facilities/{facility}/facility-status`
- `entur-norway` — PR #387, merge `8c30130dfc24f4c780faa463cf90cc301c5fb974`; topics:
  - `transit/no/entur/entur-norway/et/{operator_ref}/{line_ref}/{service_journey_id}/estimated-vehicle-journey`
  - `transit/no/entur/entur-norway/vm/{operator_ref}/{line_ref}/{service_journey_id}/monitored-vehicle-journey`
  - `transit/no/entur/entur-norway/sx/{severity}/{situation_number}/situation`
- `eaws-albina` — PR #388, merge `3c198ae84e743a8b0305d6848d36a962a41c8273`; topic `alerts/at/eaws/eaws-albina/{country}/{region_id}/{danger_level}/bulletin`.
- `gdacs` — PR #390, merge `8ccb37573bd3153de8dace7ed6cc06ed13c6e4a0`; topic `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert`.
- `meteoalarm` — PR #391, merge `c4ed253d6f825a2a2388540c7ffa95fb5e837143`; topic `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning`.
- `ptwc-tsunami` — PR #392, merge `a15181491e9f913d8ad46ff373623feedb3c1e1c`; topic `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin`.
- `nina-bbk` — PR #393, merge `2db32ac5003182ce4f739aa7cd7a381d78ec57e5`; topic `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning`.

## Ready-to-ship remaining

- `jma-bosai-warning` — ready candidate; target `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}`. Deferred in batch 9 to preserve quality after four source PRs and repeated full main CI waits.
- `jma-bosai-quake` — ready candidate; target `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report`. Deferred in batch 9 to preserve quality after four source PRs and repeated full main CI waits.

## Notes

- The source inventory file was not present on disk at the start of batch 8, so this file records the shipped state established by PRs #385-#388.
- Mandatory xRegistry and UNS specialist reviews were completed before each source PR.
