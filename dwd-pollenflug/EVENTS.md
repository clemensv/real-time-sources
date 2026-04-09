# DWD Pollenflug (German Pollen Forecast) Bridge Events

This document describes the events emitted by the DWD Pollenflug Bridge.

- [DE.DWD.Pollenflug](#message-group-dedwdpollenflug)
  - [DE.DWD.Pollenflug.Region](#message-dedwdpollenflugregion)
  - [DE.DWD.Pollenflug.PollenForecast](#message-dedwdpollenflugpollenforecast)

---

## Message Group: DE.DWD.Pollenflug

---

### Message: DE.DWD.Pollenflug.Region

*Reference data — sent once at startup before the telemetry polling loop begins.*

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | CloudEvent type | `string` | `True` | `DE.DWD.Pollenflug.Region` |
| `source` | CloudEvent source | `string` | `True` | `https://opendata.dwd.de/climate_environment/health/alerts/` |
| `subject` | Region identifier | `uritemplate` | `True` | `{region_id}` |

#### Schema: Region

| **Field Name** | **Type** | **Description** |
|---|---|---|
| `region_id` | *integer* | Unique numeric identifier for the forecast area |
| `region_name` | *string* | Name of the main geographic region |
| `partregion_id` | *integer (nullable)* | Sub-region identifier (-1 means no sub-region; emitted as null) |
| `partregion_name` | *string (nullable)* | Sub-region name (empty string means no sub-region; emitted as null) |

#### Example CloudEvent:

```json
{
  "specversion": "1.0",
  "type": "DE.DWD.Pollenflug.Region",
  "source": "https://opendata.dwd.de/climate_environment/health/alerts/",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "subject": "11",
  "datacontenttype": "application/json",
  "data": {
    "region_id": 11,
    "region_name": "Schleswig-Holstein und Hamburg",
    "partregion_id": 11,
    "partregion_name": "Inseln und Marschen"
  }
}
```

---

### Message: DE.DWD.Pollenflug.PollenForecast

*Telemetry data — emitted for each region whenever a new forecast is published.*

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | CloudEvent type | `string` | `True` | `DE.DWD.Pollenflug.PollenForecast` |
| `source` | CloudEvent source | `string` | `True` | `https://opendata.dwd.de/climate_environment/health/alerts/` |
| `subject` | Region identifier | `uritemplate` | `True` | `{region_id}` |

#### Schema: PollenForecast

| **Field Name** | **Type** | **Description** |
|---|---|---|
| `region_id` | *integer* | Unique numeric identifier for the forecast area |
| `region_name` | *string* | Display name of the forecast area |
| `last_update` | *string* | Timestamp of the last forecast update (e.g. "2025-04-08 11:00 Uhr") |
| `next_update` | *string* | Timestamp of the next expected update |
| `sender` | *string (nullable)* | Issuing organization |
| `hazel_today` | *string (nullable)* | Hazel (Hasel) pollen intensity today |
| `hazel_tomorrow` | *string (nullable)* | Hazel pollen intensity tomorrow |
| `hazel_dayafter_to` | *string (nullable)* | Hazel pollen intensity day after tomorrow |
| `alder_today` | *string (nullable)* | Alder (Erle) pollen intensity today |
| `alder_tomorrow` | *string (nullable)* | Alder pollen intensity tomorrow |
| `alder_dayafter_to` | *string (nullable)* | Alder pollen intensity day after tomorrow |
| `birch_today` | *string (nullable)* | Birch (Birke) pollen intensity today |
| `birch_tomorrow` | *string (nullable)* | Birch pollen intensity tomorrow |
| `birch_dayafter_to` | *string (nullable)* | Birch pollen intensity day after tomorrow |
| `ash_today` | *string (nullable)* | Ash (Esche) pollen intensity today |
| `ash_tomorrow` | *string (nullable)* | Ash pollen intensity tomorrow |
| `ash_dayafter_to` | *string (nullable)* | Ash pollen intensity day after tomorrow |
| `grasses_today` | *string (nullable)* | Grasses (Gräser) pollen intensity today |
| `grasses_tomorrow` | *string (nullable)* | Grasses pollen intensity tomorrow |
| `grasses_dayafter_to` | *string (nullable)* | Grasses pollen intensity day after tomorrow |
| `rye_today` | *string (nullable)* | Rye (Roggen) pollen intensity today |
| `rye_tomorrow` | *string (nullable)* | Rye pollen intensity tomorrow |
| `rye_dayafter_to` | *string (nullable)* | Rye pollen intensity day after tomorrow |
| `mugwort_today` | *string (nullable)* | Mugwort (Beifuß) pollen intensity today |
| `mugwort_tomorrow` | *string (nullable)* | Mugwort pollen intensity tomorrow |
| `mugwort_dayafter_to` | *string (nullable)* | Mugwort pollen intensity day after tomorrow |
| `ragweed_today` | *string (nullable)* | Ragweed (Ambrosia) pollen intensity today |
| `ragweed_tomorrow` | *string (nullable)* | Ragweed pollen intensity tomorrow |
| `ragweed_dayafter_to` | *string (nullable)* | Ragweed pollen intensity day after tomorrow |

#### Pollen Intensity Scale

| **Value** | **Description (German)** | **Description (English)** |
|---|---|---|
| `0` | keine Belastung | No load |
| `0-1` | keine bis geringe Belastung | None to low load |
| `1` | geringe Belastung | Low load |
| `1-2` | geringe bis mittlere Belastung | Low to medium load |
| `2` | mittlere Belastung | Medium load |
| `2-3` | mittlere bis hohe Belastung | Medium to high load |
| `3` | hohe Belastung | High load |

#### Example CloudEvent:

```json
{
  "specversion": "1.0",
  "type": "DE.DWD.Pollenflug.PollenForecast",
  "source": "https://opendata.dwd.de/climate_environment/health/alerts/",
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "subject": "11",
  "datacontenttype": "application/json",
  "data": {
    "region_id": 11,
    "region_name": "Inseln und Marschen",
    "last_update": "2025-04-08 11:00 Uhr",
    "next_update": "2025-04-09 11:00 Uhr",
    "sender": "Deutscher Wetterdienst - Medizin-Meteorologie",
    "hazel_today": "0",
    "hazel_tomorrow": "0",
    "hazel_dayafter_to": "0",
    "alder_today": "0-1",
    "alder_tomorrow": "0-1",
    "alder_dayafter_to": "0-1",
    "birch_today": "2-3",
    "birch_tomorrow": "2-3",
    "birch_dayafter_to": "2",
    "ash_today": "1-2",
    "ash_tomorrow": "1-2",
    "ash_dayafter_to": "1",
    "grasses_today": "0",
    "grasses_tomorrow": "0",
    "grasses_dayafter_to": "0",
    "rye_today": "0",
    "rye_tomorrow": "0",
    "rye_dayafter_to": "0",
    "mugwort_today": "0",
    "mugwort_tomorrow": "0",
    "mugwort_dayafter_to": "0",
    "ragweed_today": "0",
    "ragweed_tomorrow": "0",
    "ragweed_dayafter_to": "0"
  }
}
```
