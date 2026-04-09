# Events — Australian State Wildfires

This document describes the CloudEvents emitted by the Australian State
Wildfires bridge, derived from the xreg manifest at
`xreg/australia_wildfires.xreg.json`.

## Endpoint

| Property | Value |
|----------|-------|
| Protocol | Kafka |
| Topic | `australia-wildfires` |
| Envelope | CloudEvents/1.0 structured JSON |
| Key | `{state}/{incident_id}` |

## Message Group: `AU.Gov.Emergency.Wildfires`

### `AU.Gov.Emergency.Wildfires.FireIncident`

Normalized bushfire or grass fire incident record aggregated from three
Australian state emergency services.

| CloudEvents Attribute | Value |
|-----------------------|-------|
| `type` | `AU.Gov.Emergency.Wildfires.FireIncident` |
| `source` | `https://github.com/clemensv/real-time-sources/tree/main/australia-wildfires` |
| `subject` | `{state}/{incident_id}` |

#### Schema: `FireIncident`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `incident_id` | string | ✅ | Stable identifier for the fire incident |
| `state` | string | ✅ | Australian state abbreviation (NSW, VIC, QLD) |
| `title` | string | ✅ | Human-readable title or headline |
| `alert_level` | string | ✅ | Alert level (Advice, Watch and Act, Emergency Warning) |
| `status` | string \| null | | Operational status of the incident |
| `location` | string \| null | | Human-readable location description |
| `latitude` | double \| null | | Latitude of incident centroid (WGS84, °) |
| `longitude` | double \| null | | Longitude of incident centroid (WGS84, °) |
| `size_hectares` | double \| null | | Estimated fire area in hectares |
| `type` | string \| null | | Fire type classification (Bush Fire, Grass Fire, etc.) |
| `responsible_agency` | string \| null | | Responsible fire-fighting agency |
| `updated` | datetime | ✅ | Last update timestamp (ISO 8601 UTC) |
| `source_url` | string | ✅ | URL to original incident details |

## Data Sources

- **NSW Rural Fire Service**: `https://www.rfs.nsw.gov.au/feeds/majorIncidents.json`
- **VicEmergency**: `https://www.emergency.vic.gov.au/public/osom-geojson.json` (filtered for fire events)
- **Queensland Fire Department**: `https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert.json`
