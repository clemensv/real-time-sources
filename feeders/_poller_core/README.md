# Shared poller core

`feeders/_poller_core` is the first shared cross-feeder Python package in this repository. It is **not** a feeder/source: it has no xRegistry contract, generated producer, transport app, container, or Events document. Bespoke feeders import it for reusable fetch plumbing and still define their own event contracts and mapping code.

Future feeders wire it as a path dependency:

```toml
[tool.poetry.dependencies]
poller_core = { path = "../_poller_core" }
```

## ArcGIS FeatureServer usage

```python
from poller_core import ArcGisFeatureServerPoller, DeltaDetector, JsonFileStateStore

poller = ArcGisFeatureServerPoller(
    "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer",
    layer_id=0,
    unique_field="IrwinID",
    order_by_fields="OBJECTID ASC",
    headers={"User-Agent": USER_AGENT},
)
state_store = JsonFileStateStore(last_polled_file)
state = state_store.load_namespace("wildfire-delta")
delta = DeltaDetector(timestamp_field="ModifiedOnDateTime")

for feature in delta.changed_features(poller.fetch().features, state):
    attrs = feature["attributes"]
    geometry = feature["geometry"]
    incident = WildfireIncident(
        irwin_id=feature["id"],
        incident_name=attrs.get("IncidentName", ""),
        # map the rest of this feeder's schema here
    )
    producer.send_wildfire_incident(incident, _subject_id=feature["id"])

state_store.save_namespace("wildfire-delta", state)
```

The ArcGIS poller normalizes service-root, layer, and `/query` URLs; discovers `objectIdField` and `maxRecordCount` from layer metadata; requests `f=geojson` first; falls back to `f=json`; and pages with `resultOffset`/`resultRecordCount` until all features are fetched.

## GeoJSON FeatureCollection usage

```python
from poller_core import DeltaDetector, GeoJsonFeatureCollectionPoller, OffsetLimitPagination

poller = GeoJsonFeatureCollectionPoller(
    "https://api.weather.gc.ca/collections/swob-stations/items",
    params={"f": "json"},
    id_path="properties.id",
    pagination=OffsetLimitPagination(limit=500),
    headers={"User-Agent": USER_AGENT},
)
delta = DeltaDetector()  # falls back to a stable attributes+geometry hash
state = state_store.load_namespace("stations")

for feature in delta.changed_features(poller.fetch().features, state):
    props = feature["attributes"]
    station = Station(
        station_id=feature["id"],
        name=props.get("name", ""),
        # map the rest of this feeder's schema here
    )
    producer.send_station(station, _subject_id=feature["id"])
```

The GeoJSON poller handles gzip payloads, conditional GET with ETag/Last-Modified, offset/limit pagination, and RFC 5988 `Link: rel="next"` pagination. It returns normalized `{id, attributes, geometry}` dictionaries so each feeder remains responsible for its own schema-specific parsing.

## Generalized existing patterns

This package extracts the shared fetch skeleton already present in bespoke feeders:

- `nifc-usa-wildfires`: ArcGIS FeatureServer `f=geojson`, `resultOffset`, `resultRecordCount`, and `exceededTransferLimit` paging.
- `german-waters`: ArcGIS/MapServer query parameters, `outFields`, `outSR`, and attribute/geometry parsing.
- `australia-wildfires`: GeoJSON FeatureCollection polling from multiple emergency feeds and per-feature id extraction.
- `environment-canada`: OGC API FeatureCollection offset/limit paging.
- `eurdep-radiation` and `inpe-deter-brazil`: FeatureCollection/WFS-style page loops and stable feature extraction.
- `noaa-nws`: FeatureCollection pagination using a next-page URL.
- `bfs-odl`, `ireland-opw-waterlevel`, and `usgs-geomag`: simple GeoJSON fetch-then-map patterns and file-backed state/dedupe analogs.

Current feeders do not import this package yet. It lands ahead of consumers so future ArcGIS and GeoJSON sources can depend on one reviewed polling implementation.
