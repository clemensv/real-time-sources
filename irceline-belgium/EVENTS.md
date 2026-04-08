# IRCELINE Belgium events

Topic: `irceline-belgium`

## Endpoint and key model

| Endpoint | Message group | Event types | Kafka key / CloudEvents subject |
|---|---|---|---|
| `be.irceline.Stations.Kafka` | `be.irceline.Stations` | `be.irceline.Station` | `{station_id}` |
| `be.irceline.Timeseries.Kafka` | `be.irceline.Timeseries` | `be.irceline.Timeseries`, `be.irceline.Observation` | `{timeseries_id}` |

## Event: `be.irceline.Station`

Reference data for one monitoring station from `GET /stations`.

| Field | Type | Required | Description |
|---|---|---|---|
| `station_id` | string | yes | Numeric station identifier from `properties.id`, emitted as a string because it is the Kafka key and subject value. |
| `label` | string | yes | Station label such as `40AL02 - Beveren`. |
| `latitude` | double | yes | Station latitude in decimal degrees north from GeoJSON coordinates[1]. |
| `longitude` | double | yes | Station longitude in decimal degrees east from GeoJSON coordinates[0]. |

Example:

```json
{
  "specversion": "1.0",
  "type": "be.irceline.Station",
  "source": "https://geo.irceline.be/sos/api/v1/stations",
  "subject": "1031",
  "datacontenttype": "application/json",
  "data": {
    "station_id": "1031",
    "label": "40AL02 - Beveren",
    "latitude": 51.30452079034417,
    "longitude": 4.234832753144062
  }
}
```

## Event: `be.irceline.Timeseries`

Reference data for one station-timeseries combination from `GET /timeseries?expanded=true`.

| Field | Type | Required | Description |
|---|---|---|---|
| `timeseries_id` | string | yes | Stable numeric timeseries identifier. |
| `label` | string | yes | Descriptive upstream label. |
| `uom` | string | yes | Published unit of measurement such as `µg/m³`. |
| `station_id` | string | yes | Linked station identifier. |
| `station_label` | string | yes | Linked station label. |
| `latitude` | double or null | no | Linked station latitude when present. |
| `longitude` | double or null | no | Linked station longitude when present. |
| `phenomenon_id` | string or null | no | Measured phenomenon identifier. |
| `phenomenon_label` | string or null | no | Human-readable phenomenon label. |
| `category_id` | string or null | no | Category identifier. |
| `category_label` | string or null | no | Category label. |
| `status_intervals` | array or null | no | Ordered threshold bands with `lower`, `upper`, `name`, and `color`. |

Example:

```json
{
  "specversion": "1.0",
  "type": "be.irceline.Timeseries",
  "source": "https://geo.irceline.be/sos/api/v1/timeseries",
  "subject": "6152",
  "datacontenttype": "application/json",
  "data": {
    "timeseries_id": "6152",
    "label": "Particulate Matter < 10 µm 6152 - DAILY CORRECTION TEOM - procedure, 40AL01 - Linkeroever",
    "uom": "µg/m³",
    "station_id": "1030",
    "station_label": "40AL01 - Linkeroever",
    "latitude": 51.23619419990238,
    "longitude": 4.385223684454721,
    "phenomenon_id": "5",
    "phenomenon_label": "Particulate Matter < 10 µm",
    "category_id": "5",
    "category_label": "Particulate Matter < 10 µm",
    "status_intervals": [
      {
        "lower": "50.0",
        "upper": "60.0",
        "name": "51 - 60 PM10",
        "color": "#FFBB00"
      }
    ]
  }
}
```

## Event: `be.irceline.Observation`

Telemetry event for one value from `GET /timeseries/{id}/getData`.

| Field | Type | Required | Description |
|---|---|---|---|
| `timeseries_id` | string | yes | Timeseries identifier, identical to the Kafka key and subject. |
| `timestamp` | string | yes | ISO 8601 UTC timestamp derived from the upstream Unix millisecond timestamp. |
| `value` | double or null | no | Measurement value. Null is allowed when IRCELINE publishes a timestamp without a numeric value. |
| `uom` | string | yes | Unit of measurement copied from the parent timeseries. |

Example:

```json
{
  "specversion": "1.0",
  "type": "be.irceline.Observation",
  "source": "https://geo.irceline.be/sos/api/v1/timeseries",
  "subject": "6152",
  "datacontenttype": "application/json",
  "data": {
    "timeseries_id": "6152",
    "timestamp": "2025-04-06T23:00:00Z",
    "value": 17.3,
    "uom": "µg/m³"
  }
}
```
