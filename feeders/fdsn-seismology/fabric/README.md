# fdsn-seismology Fabric assets

These post-deploy assets provision a Fabric Map for the **fdsn-seismology**
feeder. The hook auto-creates or reuses a Map item, installs helper KQL
functions, and wires three live layers against the feeder's KQL database.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Acquires Fabric + Kusto tokens, ensures the Map item exists, then runs `wire_fdsn_seismology_map.py`. |
| `wire_fdsn_seismology_map.py` | Installs helper functions (`fdsn_recent_events`, `fdsn_significant_events`, `fdsn_density_points`, `fdsn_bbox`) and rewires the Map definition idempotently. |

## Layers

1. **Recent earthquakes** — 24-hour bubble layer coloured by earthquake depth.
2. **Seismic density heatmap** — 7-day low-zoom heatmap for global seismic activity.
3. **Significant events** — labelled M4.5+ bubbles with a magnitude-derived alert bucket.

## Defaults

- Map name: `fdsn-seismology-map`
- Basemap center: `[0, 20]`
- Basemap zoom: `2`
- Style / theme: `grayscale_dark` / `dark`
- Background color: `#1E293B`

Environment overrides:

- `FDSN_SEISMOLOGY_FABRIC_MAP_ID`
- `FDSN_SEISMOLOGY_FABRIC_MAP_NAME`
