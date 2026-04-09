# Wallonia ISSeP events

Topic: `wallonia-issep`

## Endpoint and key model

| Endpoint | Message group | Event types | Kafka key / CloudEvents subject |
|---|---|---|---|
| `be.issep.airquality.Sensors.Kafka` | `be.issep.airquality.Sensors` | `be.issep.airquality.SensorConfiguration`, `be.issep.airquality.Observation` | `{configuration_id}` |

## Event: `be.issep.airquality.SensorConfiguration`

Reference data for one ISSeP sensor configuration derived from the data records. Each distinct `id_configuration` represents a deployed sensor unit.

| Field | Type | Required | Description |
|---|---|---|---|
| `configuration_id` | string | yes | Stable numeric sensor configuration identifier from `id_configuration`. Used as the Kafka key and CloudEvents subject. |

Example:

```json
{
  "specversion": "1.0",
  "type": "be.issep.airquality.SensorConfiguration",
  "source": "https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records",
  "subject": "10412",
  "datacontenttype": "application/json",
  "data": {
    "configuration_id": "10412"
  }
}
```

## Event: `be.issep.airquality.Observation`

Telemetry event for one air quality observation from a Wallonia ISSeP sensor.

| Field | Type | Required | Description |
|---|---|---|---|
| `configuration_id` | string | yes | Sensor configuration identifier. Matches the Kafka key and subject. |
| `moment` | string | yes | ISO 8601 observation timestamp from the upstream `moment` field. |
| `co` | int or null | no | Raw carbon monoxide electrochemical sensor reading. |
| `no` | int or null | no | Raw nitric oxide electrochemical sensor reading. |
| `no2` | int or null | no | Raw nitrogen dioxide sensor reading. Negative values are valid. |
| `o3no2` | int or null | no | Raw combined ozone/nitrogen dioxide reading. |
| `ppbno` | double or null | no | Calibrated NO in ppb. |
| `ppbno_statut` | int or null | no | Quality status flag for ppbno. |
| `ppbno2` | double or null | no | Calibrated NO₂ in ppb. |
| `ppbno2_statut` | int or null | no | Quality status flag for ppbno2. |
| `ppbo3` | double or null | no | Calibrated O₃ in ppb. |
| `ppbo3_statut` | int or null | no | Quality status flag for ppbo3. |
| `ugpcmno` | double or null | no | Calibrated NO in µg/m³. |
| `ugpcmno_statut` | int or null | no | Quality status flag for ugpcmno. |
| `ugpcmno2` | double or null | no | Calibrated NO₂ in µg/m³. |
| `ugpcmno2_statut` | int or null | no | Quality status flag for ugpcmno2. |
| `ugpcmo3` | double or null | no | Calibrated O₃ in µg/m³. |
| `ugpcmo3_statut` | int or null | no | Quality status flag for ugpcmo3. |
| `bme_t` | double or null | no | BME280 temperature in °C. |
| `bme_t_statut` | int or null | no | Quality status flag for bme_t. |
| `bme_pres` | int or null | no | BME280 atmospheric pressure in Pa. |
| `bme_pres_statut` | int or null | no | Quality status flag for bme_pres. |
| `bme_rh` | double or null | no | BME280 relative humidity in %. |
| `bme_rh_statut` | int or null | no | Quality status flag for bme_rh. |
| `pm1` | double or null | no | PM1 concentration in µg/m³. |
| `pm1_statut` | int or null | no | Quality status flag for pm1. |
| `pm25` | double or null | no | PM2.5 concentration in µg/m³. |
| `pm25_statut` | int or null | no | Quality status flag for pm25. |
| `pm4` | double or null | no | PM4 concentration in µg/m³. |
| `pm4_statut` | int or null | no | Quality status flag for pm4. |
| `pm10` | double or null | no | PM10 concentration in µg/m³. |
| `pm10_statut` | int or null | no | Quality status flag for pm10. |
| `vbat` | double or null | no | Battery voltage in V. |
| `vbat_statut` | int or null | no | Quality status flag for vbat. |
| `mwh_bat` | double or null | no | Battery energy in mWh. Negative = discharge. |
| `mwh_pv` | double or null | no | Photovoltaic energy generation in mWh. |
| `co_rf` | double or null | no | CO reference station comparison value. |
| `no_rf` | double or null | no | NO reference station comparison value. |
| `no2_rf` | double or null | no | NO₂ reference station comparison value. |
| `o3no2_rf` | double or null | no | O₃+NO₂ reference station comparison value. |
| `o3_rf` | double or null | no | O₃ reference station comparison value. |
| `pm10_rf` | double or null | no | PM10 reference station comparison value. |

Example:

```json
{
  "specversion": "1.0",
  "type": "be.issep.airquality.Observation",
  "source": "https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records",
  "subject": "10412",
  "datacontenttype": "application/json",
  "data": {
    "configuration_id": "10412",
    "moment": "2026-04-08T20:21:04+02:00",
    "co": 16,
    "no": 7,
    "no2": -1,
    "o3no2": -2,
    "ppbno": 2.711,
    "ppbno_statut": 100,
    "ppbno2": 0.985,
    "ppbno2_statut": 0,
    "ppbo3": 9.941,
    "ppbo3_statut": 0,
    "ugpcmno": 3.38,
    "ugpcmno_statut": 100,
    "ugpcmno2": 1.888,
    "ugpcmno2_statut": 0,
    "ugpcmo3": 19.965,
    "ugpcmo3_statut": 100,
    "bme_t": 21.3,
    "bme_t_statut": 100,
    "bme_pres": 101405,
    "bme_pres_statut": 100,
    "bme_rh": 38.97,
    "bme_rh_statut": 100,
    "pm1": 3.62,
    "pm1_statut": 100,
    "pm25": 1.957,
    "pm25_statut": 100,
    "pm4": 3.83,
    "pm4_statut": 100,
    "pm10": 5.148,
    "pm10_statut": 100,
    "vbat": 4.12,
    "vbat_statut": 100,
    "mwh_bat": -1.95,
    "mwh_pv": 1.56,
    "co_rf": 0.0,
    "no_rf": 0.0,
    "no2_rf": 0.0,
    "o3no2_rf": 0.0,
    "o3_rf": 0.0,
    "pm10_rf": 0.0
  }
}
```
