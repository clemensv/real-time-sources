# AviationWeather.gov Bridge Events

This document describes the events emitted by the AviationWeather.gov Bridge.

- [gov.noaa.aviationweather](#message-group-govnoaaaviationweather)
  - [gov.noaa.aviationweather.Station](#message-govnoaaaviationweatherstation)
  - [gov.noaa.aviationweather.Metar](#message-govnoaaaviationweathermetar)
  - [gov.noaa.aviationweather.Sigmet](#message-govnoaaaviationweathersigmet)

---

## Message Group: gov.noaa.aviationweather

---

### Message: gov.noaa.aviationweather.Station

*Reference data — sent at startup and refreshed periodically.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.noaa.aviationweather.Station` |
| `source` | CloudEvent source | `string` | `True` | `https://aviationweather.gov` |
| `subject` | CloudEvent subject | `uritemplate` | `True` | `{icao_id}` |

#### Schema: Station

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `icao_id` | *string* | — | ICAO station identifier (e.g. 'KJFK') |
| `iata_id` | *string* | — | IATA airport code (e.g. 'JFK') |
| `faa_id` | *string* | — | FAA location identifier |
| `wmo_id` | *string* | — | WMO station identifier |
| `name` | *string* | — | Human-readable station name |
| `latitude` | *number* | degrees | Station latitude |
| `longitude` | *number* | degrees | Station longitude |
| `elevation` | *number* | meters | Station elevation |
| `state` | *string* | — | State/province code |
| `country` | *string* | — | ISO 3166-1 alpha-2 country code |
| `site_type` | *string* | — | Available data products (e.g. 'METAR,TAF') |

---

### Message: gov.noaa.aviationweather.Metar

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.noaa.aviationweather.Metar` |
| `source` | CloudEvent source | `string` | `True` | `https://aviationweather.gov` |
| `subject` | CloudEvent subject | `uritemplate` | `True` | `{icao_id}` |

#### Schema: Metar

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `icao_id` | *string* | — | ICAO station identifier |
| `obs_time` | *string (date-time)* | — | Observation time (ISO 8601 UTC) |
| `report_time` | *string (date-time)* | — | Report time (ISO 8601 UTC) |
| `temp` | *number* | °C | Air temperature |
| `dewp` | *number* | °C | Dewpoint temperature |
| `wdir` | *integer* | degrees | Wind direction |
| `wspd` | *integer* | knots | Sustained wind speed |
| `wgst` | *integer* | knots | Wind gust speed |
| `visib` | *string* | statute miles | Prevailing visibility |
| `altim` | *number* | hPa | Altimeter setting |
| `slp` | *number* | hPa | Sea level pressure |
| `qc_field` | *integer* | — | Quality control flag |
| `wx_string` | *string* | — | Present weather codes |
| `metar_type` | *string* | — | Report type (METAR/SPECI) |
| `raw_ob` | *string* | — | Raw METAR text |
| `latitude` | *number* | degrees | Station latitude |
| `longitude` | *number* | degrees | Station longitude |
| `elevation` | *number* | meters | Station elevation |
| `flt_cat` | *string* | — | Flight category (VFR/MVFR/IFR/LIFR) |
| `clouds` | *string* | — | JSON-encoded cloud layers |
| `name` | *string* | — | Station name |

---

### Message: gov.noaa.aviationweather.Sigmet

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.noaa.aviationweather.Sigmet` |
| `source` | CloudEvent source | `string` | `True` | `https://aviationweather.gov` |
| `subject` | CloudEvent subject | `uritemplate` | `True` | `{icao_id}` |

#### Schema: Sigmet

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `icao_id` | *string* | — | Issuing office ICAO ID |
| `series_id` | *string* | — | SIGMET series identifier |
| `valid_time_from` | *string (date-time)* | — | Validity start (ISO 8601 UTC) |
| `valid_time_to` | *string (date-time)* | — | Validity end (ISO 8601 UTC) |
| `hazard` | *string* | — | Hazard type (CONVECTIVE, TS, TURB, ICE, VA) |
| `qualifier` | *string* | — | Hazard qualifier (EMBD, SEV, OBSC) |
| `sigmet_type` | *string* | — | Classification (SIGMET/ISIGMET) |
| `altitude_hi` | *integer* | feet | Upper altitude limit |
| `altitude_low` | *integer* | feet | Lower altitude limit |
| `movement_dir` | *string* | — | Direction of movement |
| `movement_spd` | *string* | — | Speed of movement |
| `severity` | *integer* | — | Severity level |
| `raw_sigmet` | *string* | — | Raw SIGMET text |
| `coords` | *string* | — | JSON-encoded polygon coordinates |
