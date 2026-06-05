# siri Fabric assets

These post-deploy assets provision a Fabric Map for the **siri** feeder. The
hook auto-creates or reuses a Map item, installs helper KQL functions, and
wires three live layers against the feeder's KQL database.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Acquires Fabric + Kusto tokens, ensures the Map item exists, then runs `wire_siri_map.py`. |
| `wire_siri_map.py` | Installs helper functions (`siri_live_vehicles`, `siri_vehicle_density`, `siri_bbox`) and rewires the Map definition idempotently. |

## Layers

1. **Live vehicles** — last-10-minute vehicle markers coloured by the top 5 operators in the live snapshot.
2. **Vehicle density** — low-zoom heatmap showing current transit coverage.
3. **Route labels** — line labels at zoom 14+ using the live vehicle positions.

## Defaults

- Map name: `siri-map`
- Basemap center: `[-0.1276, 51.5074]`
- Basemap zoom: `11`
- Style / theme: `road` / `light`

Environment overrides:

- `SIRI_FABRIC_MAP_ID`
- `SIRI_FABRIC_MAP_NAME`
