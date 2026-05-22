# DMI Open Data Bridge Events

This document describes the events emitted by the DMI Open Data observation triad bridge (metObs + oceanObs + lightning).

- [dk.dmi.metObs](#message-group-dkdmimetobs)
  - [dk.dmi.metObs.MetObsStation](#message-dkdmimetobsmetobsstation)
  - [dk.dmi.metObs.MetObsObservation](#message-dkdmimetobsmetobsobservation)
- [dk.dmi.oceanObs](#message-group-dkdmioceanobs)
  - [dk.dmi.oceanObs.OceanStation](#message-dkdmioceanobsoceanstation)
  - [dk.dmi.oceanObs.TidewaterStation](#message-dkdmioceanobstidewaterstation)
  - [dk.dmi.oceanObs.OceanObservation](#message-dkdmioceanobsoceanobservation)
  - [dk.dmi.oceanObs.TidewaterPrediction](#message-dkdmioceanobstidewaterprediction)
- [dk.dmi.lightning](#message-group-dkdmilightning)
  - [dk.dmi.lightning.LightningSensor](#message-dkdmilightninglightningsensor)
  - [dk.dmi.lightning.LightningStrike](#message-dkdmilightninglightningstrike)
- [dk.dmi.metObs.kafka](#message-group-dkdmimetobskafka)
  - [dk.dmi.metObs.kafka.Station](#message-dkdmimetobskafkastation)
  - [dk.dmi.metObs.kafka.Observation](#message-dkdmimetobskafkaobservation)
- [dk.dmi.oceanObs.kafka](#message-group-dkdmioceanobskafka)
  - [dk.dmi.oceanObs.kafka.Station](#message-dkdmioceanobskafkastation)
  - [dk.dmi.oceanObs.kafka.TidewaterStation](#message-dkdmioceanobskafkatidewaterstation)
  - [dk.dmi.oceanObs.kafka.Observation](#message-dkdmioceanobskafkaobservation)
  - [dk.dmi.oceanObs.kafka.TidewaterPrediction](#message-dkdmioceanobskafkatidewaterprediction)
- [dk.dmi.lightning.kafka](#message-group-dkdmilightningkafka)
  - [dk.dmi.lightning.kafka.Sensor](#message-dkdmilightningkafkasensor)
  - [dk.dmi.lightning.kafka.Strike](#message-dkdmilightningkafkastrike)
- [dk.dmi.metObs.mqtt](#message-group-dkdmimetobsmqtt)
  - [dk.dmi.metObs.mqtt.Station](#message-dkdmimetobsmqttstation)
  - [dk.dmi.metObs.mqtt.Observation](#message-dkdmimetobsmqttobservation)
- [dk.dmi.oceanObs.mqtt](#message-group-dkdmioceanobsmqtt)
  - [dk.dmi.oceanObs.mqtt.Station](#message-dkdmioceanobsmqttstation)
  - [dk.dmi.oceanObs.mqtt.TidewaterStation](#message-dkdmioceanobsmqtttidewaterstation)
  - [dk.dmi.oceanObs.mqtt.Observation](#message-dkdmioceanobsmqttobservation)
  - [dk.dmi.oceanObs.mqtt.TidewaterPrediction](#message-dkdmioceanobsmqtttidewaterprediction)

---

## Message Group: dk.dmi.metObs
---
### Message: dk.dmi.metObs.MetObsStation
*Reference data for a DMI meteorological observation station. Emitted at feeder startup and refreshed daily. Stations cover Denmark, Greenland (DNK/GRL) and the Faroe Islands (FRO).*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.metObs.MetObsStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: MetObsStation
*A meteorological observation station owned and operated by (or on behalf of) DMI. See https://opendatadocs.dmi.govcloud.dk/en/Data/Meteorological_Observation_Data for the canonical field list. Identity is stable per stationId; metadata is slowly-changing via validFrom/validTo.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Stable DMI station identifier (e.g. '06030', '04202' for Pituffik in Greenland). Used as the Kafka partition key and CloudEvent subject. |
| `wmo_station_id` | *string* (optional) | - | `False` | World Meteorological Organization (WMO) station identifier when registered with WMO. |
| `wmo_country_code` | *string* (optional) | - | `False` | WMO country code as an integer string (e.g. '06' for Denmark). |
| `name` | *string* | - | `True` | Human-readable station name. |
| `country` | *string* | - | `True` | ISO 3166-1 alpha-3 country code: 'DNK' (Denmark), 'GRL' (Greenland), 'FRO' (Faroe Islands). |
| `owner` | *string* (optional) | - | `False` | Organisation that owns/operates the station (typically 'DMI'). |
| `region_id` | *string* (optional) | - | `False` | DMI region identifier within the country. |
| `type` | *string* (optional) | - | `False` | Station type as classified by DMI (e.g. 'Synop', 'PluvioSync'). |
| `status` | *string* (optional) | - | `False` | Operational status (e.g. 'Active', 'Inactive'). |
| `parameter_id` | *unknown* | - | `False` | List of DMI parameterId values this station reports (e.g. ['temp_dry','wind_speed','humidity']). |
| `latitude` | *double* | deg | `True` | Station latitude in decimal degrees (WGS84). Derived from GeoJSON geometry.coordinates[1]. |
| `longitude` | *double* | deg | `True` | Station longitude in decimal degrees (WGS84). Derived from GeoJSON geometry.coordinates[0]. |
| `station_height` | *double* (optional) | m | `False` | Height of the station above mean sea level. |
| `barometer_height` | *double* (optional) | m | `False` | Height of the barometer above mean sea level. |
| `anemometer_height` | *double* (optional) | m | `False` | Height of the anemometer above ground level. |
| `valid_from` | *string* (optional) | - | `False` | Timestamp from which this station-metadata version is valid. |
| `valid_to` | *string* (optional) | - | `False` | Timestamp after which this station-metadata version is no longer valid; null while current. |
| `operation_from` | *string* (optional) | - | `False` | Timestamp from which the station began operating. |
| `operation_to` | *string* (optional) | - | `False` | Timestamp at which the station stopped operating; null while operational. |
| `created` | *string* (optional) | - | `False` | Timestamp when this metadata row was created by DMI. |
| `updated` | *string* (optional) | - | `False` | Timestamp when this metadata row was last updated by DMI. |
---
### Message: dk.dmi.metObs.MetObsObservation
*A single meteorological observation value reported by a station for one parameter at a specific observed time. Cadence depends on parameter (10-minute or hourly).*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.metObs.MetObsObservation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{parameter_id}` |

#### Schema:
##### Object: MetObsObservation
*A single meteorological observation: one parameter, one station, one timestamp. Units are SI: degC, hPa, m/s, %, m, mm, degrees. wind_dir=0 means calm (not north).*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `observation_id` | *string* (optional) | - | `False` | DMI-assigned per-row identifier. Not stable across re-ingestions; use (station_id, parameter_id, observed) for idempotency. |
| `station_id` | *string* | - | `True` | Reporting station identifier (foreign key to Station). |
| `parameter_id` | *string* | - | `True` | DMI parameter identifier (e.g. 'temp_dry', 'wind_speed', 'humidity', 'pressure_at_sea'). |
| `observed` | *string* | - | `True` | Timestamp at which the value was observed (UTC, ISO 8601). |
| `value` | *double* | - | `True` | Numeric measurement value. Units depend on parameter_id (see DMI documentation). |
| `latitude` | *double* (optional) | deg | `False` | Station latitude (decimal degrees, WGS84) at observation time. |
| `longitude` | *double* (optional) | deg | `False` | Station longitude (decimal degrees, WGS84) at observation time. |
## Message Group: dk.dmi.oceanObs
---
### Message: dk.dmi.oceanObs.OceanStation
*Reference data for an oceanographic observation station (tide gauge or other coastal sensor). Owners include DMI and Kystdirektoratet (Danish Coastal Authority).*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.oceanObs.OceanStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: OceanStation
*An oceanographic observation station (typically a tide gauge). Owners include DMI and Kystdirektoratet (Danish Coastal Authority). See https://opendatadocs.dmi.govcloud.dk/en/Data/Oceanographic_Observation_Data.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Stable DMI ocean station identifier. |
| `name` | *string* | - | `True` | Human-readable station name. |
| `country` | *string* (optional) | - | `False` | ISO 3166-1 alpha-3 country code (DNK, GRL, FRO). |
| `owner` | *string* (optional) | - | `False` | Operating agency (e.g. 'DMI', 'Kystdirektoratet'). |
| `type` | *string* (optional) | - | `False` | Station type (e.g. 'Tide-gauge-primary'). |
| `status` | *string* (optional) | - | `False` | Operational status. |
| `parameter_id` | *unknown* | - | `False` | Parameter IDs supported by this station (subset of {sealev_dvr, sealev_ln, sea_reg, tw}). |
| `latitude` | *double* | deg | `True` | Station latitude (decimal degrees, WGS84). |
| `longitude` | *double* | deg | `True` | Station longitude (decimal degrees, WGS84). |
| `valid_from` | *string* (optional) | - | `False` | Metadata-validity start. |
| `valid_to` | *string* (optional) | - | `False` | Metadata-validity end. |
| `operation_from` | *string* (optional) | - | `False` |  |
| `operation_to` | *string* (optional) | - | `False` |  |
| `created` | *string* (optional) | - | `False` |  |
| `updated` | *string* (optional) | - | `False` |  |
---
### Message: dk.dmi.oceanObs.TidewaterStation
*Reference data for a station/grid-point at which DMI publishes tidewater (sea-level) predictions. The set partially overlaps physical tide gauges but also includes prediction-only grid points (e.g. Faroes).*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.oceanObs.TidewaterStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: TidewaterStation
*A station or virtual grid point at which DMI publishes tidewater (sea-level) predictions. The catalog includes both physical tide gauges and prediction-only points.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Stable identifier of the tidewater prediction station/grid-point. |
| `name` | *string* (optional) | - | `False` | Human-readable station name where available. |
| `country` | *string* (optional) | - | `False` | ISO 3166-1 alpha-3 country code. |
| `owner` | *string* (optional) | - | `False` | Operating agency. |
| `latitude` | *double* | deg | `True` | Prediction-point latitude (decimal degrees, WGS84). |
| `longitude` | *double* | deg | `True` | Prediction-point longitude (decimal degrees, WGS84). |
| `valid_from` | *string* (optional) | - | `False` |  |
| `valid_to` | *string* (optional) | - | `False` |  |
---
### Message: dk.dmi.oceanObs.OceanObservation
*A single oceanographic observation. Parameters are sealev_dvr (sea level vs DVR90 datum, cm), sealev_ln (sea level vs local zero, cm), sea_reg (registered sea level by Kystdirektoratet, cm), and tw (water temperature, deg C). 10-minute cadence.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.oceanObs.OceanObservation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{parameter_id}` |

#### Schema:
##### Object: OceanObservation
*A single oceanographic measurement. parameter_id is one of: sealev_dvr (sea level vs DVR90 datum, cm; preferred since 1997), sealev_ln (sea level vs local zero, cm; preferred before 1997), sea_reg (sea-level registration by Kystdirektoratet, cm), tw (water temperature, deg C; indicative).*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `observation_id` | *string* (optional) | - | `False` | DMI-assigned row identifier (not stable across re-ingestions). |
| `station_id` | *string* | - | `True` |  |
| `parameter_id` | *string* | - | `True` | One of sealev_dvr, sealev_ln, sea_reg, tw. |
| `observed` | *string* | - | `True` |  |
| `value` | *double* | - | `True` | Numeric value. cm for sealev_*/sea_reg, deg C for tw. |
| `latitude` | *double* (optional) | deg | `False` |  |
| `longitude` | *double* (optional) | deg | `False` |  |
---
### Message: dk.dmi.oceanObs.TidewaterPrediction
*A deterministic tidewater (sea-level) prediction for one station and one forecast horizon. predictionType is typically '10minutes'; predictions are issued forward ~30 days.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.oceanObs.TidewaterPrediction` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: TidewaterPrediction
*A deterministic tidewater (sea-level) prediction for one station and one forecast horizon. Predictions are issued every model cycle and span ~30 days at 10-minute granularity.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `prediction_id` | *string* (optional) | - | `False` | DMI-assigned row identifier. |
| `station_id` | *string* | - | `True` |  |
| `prediction_type` | *string* (optional) | - | `False` | Granularity of the prediction series (typically '10minutes'). |
| `prediction_time` | *string* | - | `True` | Target time for which the value is predicted. |
| `value` | *double* | - | `True` | Predicted sea level (cm vs DVR90 unless otherwise noted). |
| `latitude` | *double* (optional) | deg | `False` |  |
| `longitude` | *double* (optional) | deg | `False` |  |
## Message Group: dk.dmi.lightning
---
### Message: dk.dmi.lightning.LightningSensor
*Reference data for one of DMI's lightning detection sensors. Six DMI-owned sensors cover Denmark; third-party sensor IDs that appear in observation.sensors are not catalogued here.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.lightning.LightningSensor` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{sensor_id}` |

#### Schema:
##### Object: LightningSensor
*A DMI lightning detection sensor site. Six DMI-owned sensors cover Denmark; third-party sensors that contribute to triangulation are not catalogued here but their IDs appear in Strike.sensors.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `sensor_id` | *string* | - | `True` | Stable sensor identifier (1..6 for DMI-owned sensors). |
| `name` | *string* (optional) | - | `False` | Human-readable sensor site name. |
| `owner` | *string* (optional) | - | `False` | Operating agency (typically 'DMI'). |
| `country` | *string* (optional) | - | `False` | ISO 3166-1 alpha-3 country code (typically 'DNK'). |
| `latitude` | *double* | deg | `True` |  |
| `longitude` | *double* | deg | `True` |  |
| `active_from` | *string* (optional) | - | `False` |  |
| `active_to` | *string* (optional) | - | `False` |  |
---
### Message: dk.dmi.lightning.LightningStrike
*A single triangulated lightning strike. Type 0 = cloud-to-ground negative, 1 = cloud-to-ground positive, 2 = cloud-to-cloud. amp is signed peak current in kA. observed timestamps have microsecond precision.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `dk.dmi.lightning.LightningStrike` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{strike_id}` |

#### Schema:
##### Object: LightningStrike
*A single triangulated lightning strike. See https://opendatadocs.dmi.govcloud.dk/en/Data/Lightning_Data. observed timestamps have microsecond precision; location accuracy is approximately +/- 500-2000 m.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `strike_id` | *string* | - | `True` | Stable DMI-assigned strike identifier (e.g. 'u1xrxj10262553824830001-03'). |
| `observed` | *string* | - | `True` | Strike timestamp (UTC, microsecond precision). |
| `created` | *string* (optional) | - | `False` | Timestamp when DMI ingested the strike. |
| `type` | *integer* | - | `True` | Strike type code. |
| `amp` | *double* (optional) | kA | `False` | Signed peak current. |
| `strokes` | *integer* (optional) | - | `False` | Number of return strokes. |
| `sensors` | *string* (optional) | - | `False` | Comma-separated list of sensor IDs that contributed to triangulation (may include third-party sensors not in the Sensor catalog). |
| `latitude` | *double* | deg | `True` | Strike latitude (decimal degrees, WGS84). |
| `longitude` | *double* | deg | `True` | Strike longitude (decimal degrees, WGS84). |
## Message Group: dk.dmi.metObs.kafka
---
### Message: dk.dmi.metObs.kafka.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.metObs.kafka.Observation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
## Message Group: dk.dmi.oceanObs.kafka
---
### Message: dk.dmi.oceanObs.kafka.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.oceanObs.kafka.TidewaterStation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.oceanObs.kafka.Observation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.oceanObs.kafka.TidewaterPrediction
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
## Message Group: dk.dmi.lightning.kafka
---
### Message: dk.dmi.lightning.kafka.Sensor
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.lightning.kafka.Strike
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
## Message Group: dk.dmi.metObs.mqtt
---
### Message: dk.dmi.metObs.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.metObs.mqtt.Observation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
## Message Group: dk.dmi.oceanObs.mqtt
---
### Message: dk.dmi.oceanObs.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.oceanObs.mqtt.TidewaterStation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.oceanObs.mqtt.Observation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
---
### Message: dk.dmi.oceanObs.mqtt.TidewaterPrediction
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema inherited from `basemessageurl`.
