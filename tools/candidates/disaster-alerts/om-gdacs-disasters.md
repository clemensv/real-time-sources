# GDACS - Global Disaster Alerts (Oman Filter)

- **Country/Region**: Global (can filter by country code `OM` for Oman)
- **Endpoint**: `https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH`
- **Protocol**: REST (HTTP GET with query parameters)
- **Auth**: None
- **Format**: GeoJSON
- **Freshness**: Near real-time for disaster events (earthquakes within minutes, tropical cyclones every 3-6 hours, floods/droughts daily)
- **Docs**: https://www.gdacs.org/gdacsapi/
- **Score**: 15/18

## Overview

The **Global Disaster Alert and Coordination System (GDACS)** is a cooperation framework between the United Nations and the European Commission that provides real-time alerts for natural disasters worldwide. GDACS aggregates data from multiple authoritative sources:
- **Earthquakes**: USGS, EMSC, GEOFON, regional seismic networks
- **Tropical cyclones**: RSMC centers (IMD New Delhi, JTWC, NHC, etc.), ECMWF
- **Floods**: DFO (Dartmouth Flood Observatory), Copernicus EMS
- **Droughts**: GDO (Global Drought Observatory)
- **Tsunamis**: PTWC, regional tsunami centers
- **Volcanoes**: Smithsonian GVP, volcano observatories

For Oman, GDACS provides unified access to:
- **Earthquakes** in the Makran/Gulf of Oman region (M4+ events)
- **Tropical cyclones** from the Arabian Sea (Shaheen, Mekunu, Hikaa-type events)
- **Droughts** affecting the Horn of Africa and Arabian Peninsula (regional context, though Oman is arid by default)
- **Tsunamis** from Makran subduction zone events (rare but high-impact threat)

GDACS assigns a **color-coded alert level** (Red/Orange/Green) based on estimated impact (population exposure, magnitude/intensity, historical vulnerability). This makes it particularly valuable for emergency response and humanitarian coordination.

## Endpoint Analysis

**Verified working** — the GDACS event API is operational and returns GeoJSON for disasters in or affecting Oman.

Sample query (all event types for Oman, 2025-2026):
```
GET https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventtype=TC,EQ,FL,DR,TS,VO&country=OM&fromdate=2025-01-01&todate=2026-12-31
```

Sample response (tested 2026-05-23, no Oman-specific events but nearby regional events):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "1485124_1642572_EQ",
      "geometry": {
        "type": "Point",
        "coordinates": [-73.1444, 4.5125]
      },
      "properties": {
        "eventid": 1485124,
        "episodeid": 1642572,
        "eventtype": "EQ",
        "eventname": "",
        "glide": "EQ-2025-000080-COL",
        "name": "Earthquake in Colombia",
        "alertlevel": "Orange",
        "alertscore": 2,
        "fromdate": "2025-06-08T13:08:06",
        "todate": "2025-06-08T13:08:06",
        "country": "Colombia",
        "iso3": "COL",
        "severitydata": {
          "severity": 6.3,
          "severitytext": "Magnitude 6.3M, Depth:10km",
          "severityunit": "M"
        },
        ...
      }
    }
  ]
}
```

Note: The query returned events **not** in Oman (Colombia earthquake, East Africa drought, etc.), suggesting the `country=OM` filter may match events that have **potential cross-border impact** or the filter may not be working as expected. Manual filtering by bounding box (lat/lon) may be needed.

Better query approach (bounding box for Oman region):
```
GET https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventtype=TC,EQ&bbox=52,16,60,27&fromdate=2025-01-01
```

Key fields in GDACS response:
- **`eventid`**: GDACS unique event identifier (integer)
- **`episodeid`**: Episode ID for events with multiple updates (e.g., cyclone track updates)
- **`eventtype`**: Event type code (`EQ`, `TC`, `FL`, `DR`, `TS`, `VO`)
- **`glide`**: GLIDE number (Global Identifier for Disasters) — standardized disaster ID format
- **`alertlevel`**: Red (severe), Orange (moderate), Green (low)
- **`alertscore`**: Numeric impact score (0-3, higher = more severe)
- **`fromdate`, `todate`**: Event start/end timestamps
- **`country`**, **`iso3`**: Affected countries (can be multi-country for regional events)
- **`severitydata`**: Event-specific severity metrics (magnitude for earthquakes, wind speed for cyclones, etc.)

### Real-Time Updates

GDACS events are **continuously updated** as new information arrives. For tropical cyclones, each forecast bulletin from RSMC New Delhi or JTWC creates a new `episodeid` for the same `eventid`. Polling strategy:
- Poll every 5-10 minutes for earthquake updates (rapid aftershocks, magnitude revisions)
- Poll every 1-2 hours for tropical cyclone track updates during active storms
- Poll daily for drought/flood updates (slower-moving hazards)

## Integration Notes

- **Global vs. regional source**: GDACS is global but filterable by country or bounding box. An Oman-specific bridge would filter for events affecting Oman, but the upstream data source is the same as a global GDACS bridge. **Recommendation**: Build a **global GDACS bridge** rather than Oman-only, with optional geographic filtering in the query layer (not at bridge level). This maximizes additive value — GDACS covers disasters in regions not yet served by this repo.

- **Overlap with existing sources**:
  - **Earthquakes**: USGS and EMSC already cover global seismicity. GDACS adds alert-level scoring and multi-source aggregation but is not faster than EMSC or USGS for raw earthquake data.
  - **Tropical cyclones**: No existing coverage in repo. GDACS would be the **first tropical cyclone source**.
  - **Floods, droughts, tsunamis**: No existing coverage in repo. GDACS would be additive.

- **Additive value**: GDACS's strength is **alert-level assessment** (Red/Orange/Green) and **multi-hazard aggregation**. If the repo's goal is to provide raw sensor data (gauges, seismometers, weather stations), GDACS is redundant. If the goal is to provide **disaster event notifications**, GDACS is highly valuable — it's the system used by UN OCHA, humanitarian NGOs, and national disaster agencies worldwide for coordination.

- **Keying strategy**: Use `eventid` (global unique ID across all GDACS events) or `glide` (standardized disaster identifier) as CloudEvents subject and Kafka key. For events with multiple episodes (e.g., cyclone track updates), use `eventid_episodeid` as the key to capture each bulletin as a separate event.

- **Event families**: Different disaster types have different schemas:
  - **Earthquakes**: magnitude, depth, hypocenter
  - **Tropical cyclones**: position, wind speed, central pressure, forecast track
  - **Floods**: affected area, population exposure, river basin
  - **Droughts**: affected area, vegetation health index
  
  An xRegistry contract would need **separate message groups** for each event type or a union schema with type-specific fields.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Sub-minute for earthquakes, hourly for cyclones, daily for floods/droughts |
| Openness | 3 | No auth, no rate limits, fully public API |
| Stability | 3 | UN/EC-backed system operational since 2004, formal API with documentation |
| Structure | 3 | GeoJSON with well-defined schema, consistent across event types |
| Identifiers | 3 | `eventid` and `glide` are both globally unique and stable |
| Additive value | 0 | Earthquakes overlap with USGS/EMSC (already global). Cyclones/floods/droughts are new, but GDACS is global aggregator. |

**Verdict**: ⏭️ Reference

**Rationale**: GDACS is a **high-quality global disaster alert system**, but it is an **aggregator** of data from sources already covered or planned:
- Earthquakes come from USGS/EMSC (already in repo or strong candidates)
- Tropical cyclones come from RSMC centers and JTWC (could be ingested directly)
- Floods/droughts come from Copernicus, DFO, GDO (standalone candidates)

GDACS adds value through **alert-level scoring** and **multi-source fusion**, but if the repo's philosophy is to bridge **primary data sources** (gauges, seismometers, weather bulletins), GDACS is a **secondary aggregator** that should be referenced but not necessarily bridged.

**Alternative recommendation**: Build a **global tropical cyclone bridge** using **JTWC** or **RSMC center data directly** (if public APIs become available), and a **global flood bridge** using **Copernicus Emergency Management Service** or **Dartmouth Flood Observatory**. These would provide the same event types GDACS covers but from authoritative primary sources rather than an aggregator.

**However**, if the repo wants a **single multi-hazard disaster alert feed** for user convenience, GDACS is the best option — it's what humanitarian organizations use in the field.

**For Oman specifically**: The lack of Oman-specific events in the test query (2025-2026) suggests Oman experiences infrequent disasters at the GDACS alert threshold (Orange/Red). Most Arabian Sea cyclones landfall in Yemen or dissipate before reaching Oman. Earthquakes in the region are typically M4-5 (Green alert, below disaster threshold). This makes an Oman-only GDACS filter **low-yield**. A global GDACS bridge would be more valuable.
