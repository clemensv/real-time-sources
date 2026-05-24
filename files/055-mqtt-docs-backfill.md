# 055 MQTT Docs Backfill

## Shipped

1. Simple firehoses/docs gaps — PR #399, merge `06c55472`
   - Sources: `rss`, `cbp-border-wait`, `inpe-deter-brazil`, `irail`, `pegelonline` EVENTS.
   - Touched source docs plus root README and portal MQTT flags.
2. USGS, EPA, and civic — PR #400, merge `5a150394`
   - Sources: `epa-uv`, `seattle-911`, `usgs-geomag`, `usgs-iv`, `usgs-earthquakes`.
   - Touched source docs plus root README and portal MQTT flags.
3. Alerts, aviation, rail, science — PR #401, merge `63b7391a`
   - Sources: `eaws-albina`, `gdacs`, `meteoalarm`, `ptwc-tsunami`, `nina-bbk`, `gracedb`, `vatsim`, `entur-norway`.
   - Touched source docs plus root README and portal MQTT flags.

## Verification

- Survey over all 18 shipped sources found no README/CONTAINER/EVENTS MQTT gaps.
- Root `README.md` has the MQTT image link and both MQTT Azure deploy badges for all 18 sources.
- `app.js` and `catalog.json` have `mqtt: true` for all 18 sources.

## Main CI

- Main was admin-merged for #399, #400, and #401 after checks started with no observed failures.
- Final main CI status was checked after the backfill sequence.
