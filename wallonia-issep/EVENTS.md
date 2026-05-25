# Wallonia ISSeP Events

MQTT/5.0 transport variants of the ISSeP Wallonia air quality CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under aq/be/wallonia/wallonia-issep/{configuration_id}/... The bridge publishes sensor configuration info and observations per configuration_id.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `be.issep.airquality.Sensors.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`be.issep.airquality.Sensors`](#messagegroup-beissepairqualitysensors) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wallonia-issep` |
| Kafka key | `{configuration_id}` |
| Deployed | False |

### Endpoint `be.issep.airquality.Sensors.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`be.issep.airquality.Sensors.mqtt`](#messagegroup-beissepairqualitysensorsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `be.issep.airquality.Sensors`
<a id="messagegroup-beissepairqualitysensors"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `be.issep.airquality.Sensors.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `be.issep.airquality.SensorConfiguration`
<a id="message-beissepairqualitysensorconfiguration"></a>

| Field | Value |
| --- | --- |
| Name | SensorConfiguration |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.issep.airquality.jstruct/schemas/be.issep.airquality.SensorConfiguration`](#schema-beissepairqualitysensorconfiguration) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.issep.airquality.SensorConfiguration` |
| `source` |  | `string` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.issep.airquality.Sensors.Kafka` | `KAFKA` | topic `wallonia-issep`; key `{configuration_id}` |

#### Message `be.issep.airquality.Observation`
<a id="message-beissepairqualityobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.issep.airquality.jstruct/schemas/be.issep.airquality.Observation`](#schema-beissepairqualityobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.issep.airquality.Observation` |
| `source` |  | `string` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.issep.airquality.Sensors.Kafka` | `KAFKA` | topic `wallonia-issep`; key `{configuration_id}` |

### Messagegroup `be.issep.airquality.Sensors.mqtt`
<a id="messagegroup-beissepairqualitysensorsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the ISSeP Wallonia air quality CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under aq/be/wallonia/wallonia-issep/{configuration_id}/... The bridge publishes sensor configuration info and observations per configuration_id. |
| Transport bindings | `be.issep.airquality.Sensors.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `be.issep.airquality.Sensors.mqtt.SensorConfiguration`
<a id="message-beissepairqualitysensorsmqttsensorconfiguration"></a>

| Field | Value |
| --- | --- |
| Name | SensorConfiguration |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.issep.airquality.jstruct/schemas/be.issep.airquality.SensorConfiguration`](#schema-beissepairqualitysensorconfiguration) |
| Base message chain | `/messagegroups/be.issep.airquality.Sensors/messages/be.issep.airquality.SensorConfiguration` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.issep.airquality.SensorConfiguration` |
| `source` |  | `string` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.issep.airquality.Sensors.Mqtt` | `MQTT/5.0` | topic `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `be.issep.airquality.Sensors.mqtt.Observation`
<a id="message-beissepairqualitysensorsmqttobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.issep.airquality.jstruct/schemas/be.issep.airquality.Observation`](#schema-beissepairqualityobservation) |
| Base message chain | `/messagegroups/be.issep.airquality.Sensors/messages/be.issep.airquality.Observation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.issep.airquality.Observation` |
| `source` |  | `string` | `False` | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records` |
| `subject` |  | `uritemplate` | `False` | `{configuration_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.issep.airquality.Sensors.Mqtt` | `MQTT/5.0` | topic `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/observation` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `be.issep.airquality.jstruct`
<a id="schemagroup-beissepairqualityjstruct"></a>

#### Schema `be.issep.airquality.SensorConfiguration`
<a id="schema-beissepairqualitysensorconfiguration"></a>

| Field | Value |
| --- | --- |
| Name | SensorConfiguration |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Reference event for an ISSeP Wallonia air quality sensor configuration derived from the last-data records. Each distinct id_configuration represents a deployed sensor unit. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.odwb.be/schemas/be/issep/airquality/SensorConfiguration` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `SensorConfiguration`
<a id="schema-node-sensorconfiguration"></a>

Reference data for one ISSeP Wallonia air quality sensor configuration. Each id_configuration identifies a deployed sensor unit. The bridge emits this event at startup for each distinct configuration seen in the data records.

| Field | Value |
| --- | --- |
| $id | `https://www.odwb.be/schemas/be/issep/airquality/SensorConfiguration` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `configuration_id` | `string` | `True` | Stable numeric identifier of the sensor configuration from the upstream id_configuration field. Converted to string because it serves as the CloudEvents subject and Kafka key. | altnames=`{"issep": "id_configuration"}` | pattern=`^[0-9]+$` | - |
| `province` | `string` | `True` | Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis. | - | - | - |

#### Schema `be.issep.airquality.Observation`
<a id="schema-beissepairqualityobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Telemetry event for one air quality observation from a Wallonia ISSeP sensor. Contains pollutant concentrations, particulate matter levels, environmental readings, and quality status flags. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.odwb.be/schemas/be/issep/airquality/Observation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Air quality observation from one ISSeP Wallonia sensor at a specific moment in time. Includes raw electrochemical gas readings, calibrated ppb and µg/m³ values, particulate matter concentrations, environmental parameters, reference station comparisons, and quality status flags. Negative raw values (e.g. no2=-4) are valid sensor readings and must not be filtered.

| Field | Value |
| --- | --- |
| $id | `https://www.odwb.be/schemas/be/issep/airquality/Observation` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `configuration_id` | `string` | `True` | Stable numeric sensor configuration identifier from id_configuration. Matches the CloudEvents subject and Kafka key. | altnames=`{"issep": "id_configuration"}` | pattern=`^[0-9]+$` | - |
| `province` | `string` | `True` | Slug of the Walloon province where the sensor is located (e.g. brabant-wallon, hainaut, liege, luxembourg, namur, or "unknown" sentinel if location is not yet mapped). Matches the {province} MQTT topic axis. | - | - | - |
| `moment` | `string` | `True` | ISO 8601 observation timestamp from the upstream moment field, e.g. '2026-04-08T09:09:13+02:00'. Preserved as-is from the API response. | altnames=`{"issep": "moment"}` | - | - |
| `co` | `union` | `False` | Raw carbon monoxide electrochemical sensor reading in internal units. | altnames=`{"issep": "co"}` | - | - |
| `no` | `union` | `False` | Raw nitric oxide electrochemical sensor reading in internal units. | altnames=`{"issep": "no"}` | - | - |
| `no2` | `union` | `False` | Raw nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid. | altnames=`{"issep": "no2"}` | - | - |
| `o3no2` | `union` | `False` | Raw combined ozone and nitrogen dioxide electrochemical sensor reading in internal units. Negative values are valid. | altnames=`{"issep": "o3no2"}` | - | - |
| `ppbno` | `union` | `False` | Calibrated nitric oxide concentration in parts per billion (ppb). | unit=`ppb`<br>altnames=`{"issep": "ppbno"}` | - | - |
| `ppbno_statut` | `union` | `False` | Quality status flag for ppbno. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "ppbno_statut"}` | - | - |
| `ppbno2` | `union` | `False` | Calibrated nitrogen dioxide concentration in parts per billion (ppb). | unit=`ppb`<br>altnames=`{"issep": "ppbno2"}` | - | - |
| `ppbno2_statut` | `union` | `False` | Quality status flag for ppbno2. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "ppbno2_statut"}` | - | - |
| `ppbo3` | `union` | `False` | Calibrated ozone concentration in parts per billion (ppb). | unit=`ppb`<br>altnames=`{"issep": "ppbo3"}` | - | - |
| `ppbo3_statut` | `union` | `False` | Quality status flag for ppbo3. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "ppbo3_statut"}` | - | - |
| `ugpcmno` | `union` | `False` | Calibrated nitric oxide concentration in micrograms per cubic meter (µg/m³). | unit=`µg/m³`<br>altnames=`{"issep": "ugpcmno"}` | - | - |
| `ugpcmno_statut` | `union` | `False` | Quality status flag for ugpcmno. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "ugpcmno_statut"}` | - | - |
| `ugpcmno2` | `union` | `False` | Calibrated nitrogen dioxide concentration in micrograms per cubic meter (µg/m³). | unit=`µg/m³`<br>altnames=`{"issep": "ugpcmno2"}` | - | - |
| `ugpcmno2_statut` | `union` | `False` | Quality status flag for ugpcmno2. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "ugpcmno2_statut"}` | - | - |
| `ugpcmo3` | `union` | `False` | Calibrated ozone concentration in micrograms per cubic meter (µg/m³). | unit=`µg/m³`<br>altnames=`{"issep": "ugpcmo3"}` | - | - |
| `ugpcmo3_statut` | `union` | `False` | Quality status flag for ugpcmo3. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "ugpcmo3_statut"}` | - | - |
| `bme_t` | `union` | `False` | Temperature reading from the BME280 environmental sensor in degrees Celsius. | unit=`°C`<br>altnames=`{"issep": "bme_t"}` | - | - |
| `bme_t_statut` | `union` | `False` | Quality status flag for bme_t. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "bme_t_statut"}` | - | - |
| `bme_pres` | `union` | `False` | Atmospheric pressure reading from the BME280 sensor in Pascals. | unit=`Pa`<br>altnames=`{"issep": "bme_pres"}` | - | - |
| `bme_pres_statut` | `union` | `False` | Quality status flag for bme_pres. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "bme_pres_statut"}` | - | - |
| `bme_rh` | `union` | `False` | Relative humidity reading from the BME280 sensor as a percentage. | unit=`%`<br>altnames=`{"issep": "bme_rh"}` | - | - |
| `bme_rh_statut` | `union` | `False` | Quality status flag for bme_rh. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "bme_rh_statut"}` | - | - |
| `pm1` | `union` | `False` | Particulate matter concentration for particles under 1 micrometer in µg/m³. | unit=`µg/m³`<br>altnames=`{"issep": "pm1"}` | - | - |
| `pm1_statut` | `union` | `False` | Quality status flag for pm1. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "pm1_statut"}` | - | - |
| `pm25` | `union` | `False` | Particulate matter concentration for particles under 2.5 micrometers in µg/m³. | unit=`µg/m³`<br>altnames=`{"issep": "pm25"}` | - | - |
| `pm25_statut` | `union` | `False` | Quality status flag for pm25. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "pm25_statut"}` | - | - |
| `pm4` | `union` | `False` | Particulate matter concentration for particles under 4 micrometers in µg/m³. | unit=`µg/m³`<br>altnames=`{"issep": "pm4"}` | - | - |
| `pm4_statut` | `union` | `False` | Quality status flag for pm4. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "pm4_statut"}` | - | - |
| `pm10` | `union` | `False` | Particulate matter concentration for particles under 10 micrometers in µg/m³. | unit=`µg/m³`<br>altnames=`{"issep": "pm10"}` | - | - |
| `pm10_statut` | `union` | `False` | Quality status flag for pm10. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "pm10_statut"}` | - | - |
| `vbat` | `union` | `False` | Battery voltage of the sensor unit in Volts. | unit=`V`<br>altnames=`{"issep": "vbat"}` | - | - |
| `vbat_statut` | `union` | `False` | Quality status flag for vbat. 100 indicates valid, 0 indicates invalid or unavailable. | altnames=`{"issep": "vbat_statut"}` | - | - |
| `mwh_bat` | `union` | `False` | Battery energy level in milliwatt-hours. Negative values indicate discharge. | unit=`mWh`<br>altnames=`{"issep": "mwh_bat"}` | - | - |
| `mwh_pv` | `union` | `False` | Photovoltaic energy generation in milliwatt-hours. | unit=`mWh`<br>altnames=`{"issep": "mwh_pv"}` | - | - |
| `co_rf` | `union` | `False` | Carbon monoxide reference station comparison value. | altnames=`{"issep": "co_rf"}` | - | - |
| `no_rf` | `union` | `False` | Nitric oxide reference station comparison value. | altnames=`{"issep": "no_rf"}` | - | - |
| `no2_rf` | `union` | `False` | Nitrogen dioxide reference station comparison value. | altnames=`{"issep": "no2_rf"}` | - | - |
| `o3no2_rf` | `union` | `False` | Combined ozone and nitrogen dioxide reference station comparison value. | altnames=`{"issep": "o3no2_rf"}` | - | - |
| `o3_rf` | `union` | `False` | Ozone reference station comparison value. | altnames=`{"issep": "o3_rf"}` | - | - |
| `pm10_rf` | `union` | `False` | PM10 reference station comparison value. | altnames=`{"issep": "pm10_rf"}` | - | - |
