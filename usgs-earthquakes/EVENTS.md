# USGS Earthquake Hazards Program Events

This document describes the events emitted by the USGS Earthquake Hazards Program bridge.

- [USGS.Earthquakes](#message-group-usgsearthquakes)
  - [USGS.Earthquakes.Event](#message-usgsearthquakesevent)

---

## Message Group: USGS.Earthquakes

---

### Message: USGS.Earthquakes.Event

*USGS earthquake event data from the Earthquake Hazards Program.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `USGS.Earthquakes.Event` |
| `source` | Source URI | `uritemplate` | `True` | `{source_uri}` |
| `subject` | Network and event code | `uritemplate` | `True` | `{net}/{code}` |
| `time` | Event time | `uritemplate` | `True` | `{event_time}` |

#### Schema: USGS.Earthquakes.Event (Avro)

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `id` | `string` | Unique identifier for the earthquake event. |
| `magnitude` | `double?` | Magnitude of the earthquake. |
| `mag_type` | `string?` | Method or algorithm used to calculate the magnitude (e.g. ml, md, mb, mww). |
| `place` | `string?` | Textual description of the named geographic region near the event. |
| `event_time` | `string` (timestamp-millis) | Time of the earthquake event in ISO-8601 format. |
| `updated` | `string` (timestamp-millis) | Time when the event was most recently updated in ISO-8601 format. |
| `url` | `string?` | Link to USGS Event Page for this event. |
| `detail_url` | `string?` | Link to GeoJSON detail feed for this event. |
| `felt` | `int?` | Number of felt reports submitted to the DYFI system. |
| `cdi` | `double?` | Maximum reported community determined intensity (DYFI). |
| `mmi` | `double?` | Maximum estimated instrumental intensity (ShakeMap). |
| `alert` | `string?` | PAGER alert level (green, yellow, orange, red). |
| `status` | `string` | Review status of the event (automatic, reviewed, deleted). |
| `tsunami` | `int` | Flag indicating whether the event has a tsunami advisory (1=yes, 0=no). |
| `sig` | `int?` | Significance of the event, a number describing how significant the event is (0-1000). |
| `net` | `string` | ID of the data contributor network. |
| `code` | `string` | Identifying code assigned by the corresponding source for the event. |
| `sources` | `string?` | Comma-separated list of network contributors. |
| `nst` | `int?` | Number of seismic stations used to determine earthquake location. |
| `dmin` | `double?` | Horizontal distance from the epicenter to the nearest station (degrees). |
| `rms` | `double?` | Root-mean-square travel time residual (seconds). |
| `gap` | `double?` | Largest azimuthal gap between azimuthally adjacent stations (degrees). |
| `event_type` | `string?` | Type of seismic event (earthquake, quarry blast, etc.). |
| `latitude` | `double` | Latitude of the earthquake epicenter in decimal degrees. |
| `longitude` | `double` | Longitude of the earthquake epicenter in decimal degrees. |
| `depth` | `double?` | Depth of the earthquake in kilometers. |
