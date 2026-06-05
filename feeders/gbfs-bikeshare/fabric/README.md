# gbfs-bikeshare Fabric assets

These post-deploy assets provision a Fabric Map for the **gbfs-bikeshare** feeder.
The hook auto-creates or reuses a Map item, installs helper KQL functions, and
wires three live layers against the feeder's KQL database.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Acquires Fabric + Kusto tokens, ensures the Map item exists, then runs `wire_gbfs_bikeshare_map.py`. |
| `wire_gbfs_bikeshare_map.py` | Installs helper functions (`gbfs_station_availability`, `gbfs_free_bikes`, `gbfs_bbox`) and rewires the Map definition idempotently. |

## Layers

1. **Station availability** — bubble layer at `StationInformationLatest` locations, coloured by bikes / capacity fill ratio and refreshed every 60 seconds.
2. **Free bikes** — green dockless-bike points from `FreeBikeStatusLatest`, refreshed every 60 seconds.
3. **Station labels** — station-name labels at zoom 13+ for close-in inspection.

## Defaults

- Map name: `gbfs-bikeshare-map`
- Basemap center: `[0, 30]`
- Basemap zoom: `2`
- Style / theme: `road` / `light`

Environment overrides:

- `GBFS_BIKESHARE_FABRIC_MAP_ID`
- `GBFS_BIKESHARE_FABRIC_MAP_NAME`
