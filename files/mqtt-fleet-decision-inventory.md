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

## Ready-to-ship remaining

- `gdacs` — ready candidate; target `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert`. Skipped in batch 8 to keep quality high after four source PRs and repeated full main CI waits.
- `meteoalarm` — ready candidate; target `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning`. Skipped in batch 8 to keep quality high after four source PRs and repeated full main CI waits.

## Notes

- The source inventory file was not present on disk at the start of batch 8, so this file records the shipped state established by PRs #385-#388.
- Mandatory xRegistry and UNS specialist reviews were completed before each source PR.
