# NWS CAP Weather Alerts Events

## Topics and Keys

| Topic | Key template | Message group | Event types |
|---|---|---|---|
| `nws-alerts` | `{alert_id}` | `NWS.Alerts` | `WeatherAlert` |

## Event Metadata

- `source`: `https://api.weather.gov`
- `time`: CAP `sent` timestamp

## Event Types

### NWS.WeatherAlert

Weather or non-weather alert from the US National Weather Service via IPAWS.

- `alert_id` — URN-based CAP identifier (key)
- `area_desc` — affected area names
- `same_codes`, `ugc_codes` — SAME and UGC zone geocodes
- `sent`, `effective`, `onset`, `expires`, `ends` — temporal fields
- `status` — Actual, Test, etc.
- `message_type` — Alert, Update, Cancel
- `category`, `severity`, `urgency`, `certainty` — CAP fields
- `event` — event type (e.g., "Tornado Warning")
- `sender`, `sender_name` — issuing office
- `headline`, `description`, `instruction` — human-readable text
- `response`, `scope`, `code` — CAP metadata
- `nws_headline`, `vtec` — NWS-specific parameters
- `web` — URL to full alert

## Data Source

NWS alerts API: `https://api.weather.gov/alerts/active`
