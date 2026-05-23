# Wallonia ISSEP Air Quality Bridge Events

Events emitted by the Wallonia ISSEP bridge.

- [be.issep.airquality.Sensors](#message-group-beissepairqualitysensors)
  - [be.issep.airquality.SensorConfiguration](#message-beissepairqualitysensorconfiguration)
  - [be.issep.airquality.Observation](#message-beissepairqualityobservation)
- [be.issep.airquality.Sensors.mqtt](#message-group-beissepairqualitysensorsmqtt)
  - [be.issep.airquality.Sensors.mqtt.SensorConfiguration](#message-beissepairqualitysensorsmqttsensorconfiguration)
  - [be.issep.airquality.Sensors.mqtt.Observation](#message-beissepairqualitysensorsmqttobservation)

---

## Message Group: be.issep.airquality.Sensors
---
### Message: be.issep.airquality.SensorConfiguration
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `be.issep.airquality.SensorConfiguration` |
| `source` |  | `` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

#### Schema:
##### Object: SensorConfiguration
*Reference data for one ISSeP Wallonia air quality sensor configuration. Each id_configuration identifies a deployed sensor unit. The bridge emits this event at startup for each distinct configuration seen in the data records.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `configuration_id` | *string* | - | `True` | Stable numeric identifier of the sensor configuration from the upstream id_configuration field. Converted to string because it serves as the CloudEvents subject and Kafka key. |
| `province` | *string* | - | `True` | Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis. |
---
### Message: be.issep.airquality.Observation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `be.issep.airquality.Observation` |
| `source` |  | `` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

#### Schema:
##### Object: Observation
*Air quality observation from one ISSeP Wallonia sensor at a specific moment in time. Includes raw electrochemical gas readings, calibrated ppb and µg/m³ values, particulate matter concentrations, environmental parameters, reference station comparisons, and quality status flags. Negative raw values (e.g. no2=-4) are valid sensor readings and must not be filtered.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `configuration_id` | *string* | - | `True` | Stable numeric sensor configuration identifier from id_configuration. Matches the CloudEvents subject and Kafka key. |
| `province` | *string* | - | `True` | Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis. |
| `moment` | *string* | - | `True` | ISO 8601 observation timestamp from the upstream moment field, e.g. '2026-04-08T09:09:13+02:00'. Preserved as-is from the API response. |
| `co` | *int32* (optional) | - | `False` | Raw carbon monoxide electrochemical sensor reading in internal units. |
| `no` | *int32* (optional) | - | `False` | Raw nitric oxide electrochemical sensor reading in internal units. |
| `no2` | *int32* (optional) | - | `False` | Raw nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid. |
| `o3no2` | *int32* (optional) | - | `False` | Raw combined ozone and nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid. |
| `ppbno` | *double* (optional) | ppb | `False` | Calibrated nitric oxide concentration in parts per billion (ppb). |
| `ppbno_statut` | *int32* (optional) | - | `False` | Quality status flag for ppbno. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ppbno2` | *double* (optional) | ppb | `False` | Calibrated nitrogen dioxide concentration in parts per billion (ppb). |
| `ppbno2_statut` | *int32* (optional) | - | `False` | Quality status flag for ppbno2. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ppbo3` | *double* (optional) | ppb | `False` | Calibrated ozone concentration in parts per billion (ppb). |
| `ppbo3_statut` | *int32* (optional) | - | `False` | Quality status flag for ppbo3. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ugpcmno` | *double* (optional) | µg/m³ | `False` | Calibrated nitric oxide concentration in micrograms per cubic meter (µg/m³). |
| `ugpcmno_statut` | *int32* (optional) | - | `False` | Quality status flag for ugpcmno. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ugpcmno2` | *double* (optional) | µg/m³ | `False` | Calibrated nitrogen dioxide concentration in micrograms per cubic meter (µg/m³). |
| `ugpcmno2_statut` | *int32* (optional) | - | `False` | Quality status flag for ugpcmno2. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ugpcmo3` | *double* (optional) | µg/m³ | `False` | Calibrated ozone concentration in micrograms per cubic meter (µg/m³). |
| `ugpcmo3_statut` | *int32* (optional) | - | `False` | Quality status flag for ugpcmo3. 100 indicates valid, 0 indicates invalid or unavailable. |
| `bme_t` | *double* (optional) | °C | `False` | Temperature reading from the BME280 environmental sensor in degrees Celsius. |
| `bme_t_statut` | *int32* (optional) | - | `False` | Quality status flag for bme_t. 100 indicates valid, 0 indicates invalid or unavailable. |
| `bme_pres` | *int32* (optional) | Pa | `False` | Atmospheric pressure reading from the BME280 sensor in Pascals. |
| `bme_pres_statut` | *int32* (optional) | - | `False` | Quality status flag for bme_pres. 100 indicates valid, 0 indicates invalid or unavailable. |
| `bme_rh` | *double* (optional) | % | `False` | Relative humidity reading from the BME280 sensor as a percentage. |
| `bme_rh_statut` | *int32* (optional) | - | `False` | Quality status flag for bme_rh. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm1` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 1 micrometer in µg/m³. |
| `pm1_statut` | *int32* (optional) | - | `False` | Quality status flag for pm1. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm25` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 2.5 micrometers in µg/m³. |
| `pm25_statut` | *int32* (optional) | - | `False` | Quality status flag for pm25. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm4` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 4 micrometers in µg/m³. |
| `pm4_statut` | *int32* (optional) | - | `False` | Quality status flag for pm4. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm10` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 10 micrometers in µg/m³. |
| `pm10_statut` | *int32* (optional) | - | `False` | Quality status flag for pm10. 100 indicates valid, 0 indicates invalid or unavailable. |
| `vbat` | *double* (optional) | V | `False` | Battery voltage of the sensor unit in Volts. |
| `vbat_statut` | *int32* (optional) | - | `False` | Quality status flag for vbat. 100 indicates valid, 0 indicates invalid or unavailable. |
| `mwh_bat` | *double* (optional) | mWh | `False` | Battery energy level in milliwatt-hours. Negative values indicate discharge. |
| `mwh_pv` | *double* (optional) | mWh | `False` | Photovoltaic energy generation in milliwatt-hours. |
| `co_rf` | *double* (optional) | - | `False` | Carbon monoxide reference station comparison value. |
| `no_rf` | *double* (optional) | - | `False` | Nitric oxide reference station comparison value. |
| `no2_rf` | *double* (optional) | - | `False` | Nitrogen dioxide reference station comparison value. |
| `o3no2_rf` | *double* (optional) | - | `False` | Combined ozone and nitrogen dioxide reference station comparison value. |
| `o3_rf` | *double* (optional) | - | `False` | Ozone reference station comparison value. |
| `pm10_rf` | *double* (optional) | - | `False` | PM10 reference station comparison value. |
## Message Group: be.issep.airquality.Sensors.mqtt
---
### Message: be.issep.airquality.Sensors.mqtt.SensorConfiguration
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `be.issep.airquality.SensorConfiguration` |
| `source` |  | `` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

#### Schema:
##### Object: SensorConfiguration
*Reference data for one ISSeP Wallonia air quality sensor configuration. Each id_configuration identifies a deployed sensor unit. The bridge emits this event at startup for each distinct configuration seen in the data records.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `configuration_id` | *string* | - | `True` | Stable numeric identifier of the sensor configuration from the upstream id_configuration field. Converted to string because it serves as the CloudEvents subject and Kafka key. |
| `province` | *string* | - | `True` | Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis. |
---
### Message: be.issep.airquality.Sensors.mqtt.Observation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `be.issep.airquality.Observation` |
| `source` |  | `` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

#### Schema:
##### Object: Observation
*Air quality observation from one ISSeP Wallonia sensor at a specific moment in time. Includes raw electrochemical gas readings, calibrated ppb and µg/m³ values, particulate matter concentrations, environmental parameters, reference station comparisons, and quality status flags. Negative raw values (e.g. no2=-4) are valid sensor readings and must not be filtered.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `configuration_id` | *string* | - | `True` | Stable numeric sensor configuration identifier from id_configuration. Matches the CloudEvents subject and Kafka key. |
| `province` | *string* | - | `True` | Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis. |
| `moment` | *string* | - | `True` | ISO 8601 observation timestamp from the upstream moment field, e.g. '2026-04-08T09:09:13+02:00'. Preserved as-is from the API response. |
| `co` | *int32* (optional) | - | `False` | Raw carbon monoxide electrochemical sensor reading in internal units. |
| `no` | *int32* (optional) | - | `False` | Raw nitric oxide electrochemical sensor reading in internal units. |
| `no2` | *int32* (optional) | - | `False` | Raw nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid. |
| `o3no2` | *int32* (optional) | - | `False` | Raw combined ozone and nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid. |
| `ppbno` | *double* (optional) | ppb | `False` | Calibrated nitric oxide concentration in parts per billion (ppb). |
| `ppbno_statut` | *int32* (optional) | - | `False` | Quality status flag for ppbno. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ppbno2` | *double* (optional) | ppb | `False` | Calibrated nitrogen dioxide concentration in parts per billion (ppb). |
| `ppbno2_statut` | *int32* (optional) | - | `False` | Quality status flag for ppbno2. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ppbo3` | *double* (optional) | ppb | `False` | Calibrated ozone concentration in parts per billion (ppb). |
| `ppbo3_statut` | *int32* (optional) | - | `False` | Quality status flag for ppbo3. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ugpcmno` | *double* (optional) | µg/m³ | `False` | Calibrated nitric oxide concentration in micrograms per cubic meter (µg/m³). |
| `ugpcmno_statut` | *int32* (optional) | - | `False` | Quality status flag for ugpcmno. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ugpcmno2` | *double* (optional) | µg/m³ | `False` | Calibrated nitrogen dioxide concentration in micrograms per cubic meter (µg/m³). |
| `ugpcmno2_statut` | *int32* (optional) | - | `False` | Quality status flag for ugpcmno2. 100 indicates valid, 0 indicates invalid or unavailable. |
| `ugpcmo3` | *double* (optional) | µg/m³ | `False` | Calibrated ozone concentration in micrograms per cubic meter (µg/m³). |
| `ugpcmo3_statut` | *int32* (optional) | - | `False` | Quality status flag for ugpcmo3. 100 indicates valid, 0 indicates invalid or unavailable. |
| `bme_t` | *double* (optional) | °C | `False` | Temperature reading from the BME280 environmental sensor in degrees Celsius. |
| `bme_t_statut` | *int32* (optional) | - | `False` | Quality status flag for bme_t. 100 indicates valid, 0 indicates invalid or unavailable. |
| `bme_pres` | *int32* (optional) | Pa | `False` | Atmospheric pressure reading from the BME280 sensor in Pascals. |
| `bme_pres_statut` | *int32* (optional) | - | `False` | Quality status flag for bme_pres. 100 indicates valid, 0 indicates invalid or unavailable. |
| `bme_rh` | *double* (optional) | % | `False` | Relative humidity reading from the BME280 sensor as a percentage. |
| `bme_rh_statut` | *int32* (optional) | - | `False` | Quality status flag for bme_rh. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm1` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 1 micrometer in µg/m³. |
| `pm1_statut` | *int32* (optional) | - | `False` | Quality status flag for pm1. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm25` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 2.5 micrometers in µg/m³. |
| `pm25_statut` | *int32* (optional) | - | `False` | Quality status flag for pm25. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm4` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 4 micrometers in µg/m³. |
| `pm4_statut` | *int32* (optional) | - | `False` | Quality status flag for pm4. 100 indicates valid, 0 indicates invalid or unavailable. |
| `pm10` | *double* (optional) | µg/m³ | `False` | Particulate matter concentration for particles under 10 micrometers in µg/m³. |
| `pm10_statut` | *int32* (optional) | - | `False` | Quality status flag for pm10. 100 indicates valid, 0 indicates invalid or unavailable. |
| `vbat` | *double* (optional) | V | `False` | Battery voltage of the sensor unit in Volts. |
| `vbat_statut` | *int32* (optional) | - | `False` | Quality status flag for vbat. 100 indicates valid, 0 indicates invalid or unavailable. |
| `mwh_bat` | *double* (optional) | mWh | `False` | Battery energy level in milliwatt-hours. Negative values indicate discharge. |
| `mwh_pv` | *double* (optional) | mWh | `False` | Photovoltaic energy generation in milliwatt-hours. |
| `co_rf` | *double* (optional) | - | `False` | Carbon monoxide reference station comparison value. |
| `no_rf` | *double* (optional) | - | `False` | Nitric oxide reference station comparison value. |
| `no2_rf` | *double* (optional) | - | `False` | Nitrogen dioxide reference station comparison value. |
| `o3no2_rf` | *double* (optional) | - | `False` | Combined ozone and nitrogen dioxide reference station comparison value. |
| `o3_rf` | *double* (optional) | - | `False` | Ozone reference station comparison value. |
| `pm10_rf` | *double* (optional) | - | `False` | PM10 reference station comparison value. |
