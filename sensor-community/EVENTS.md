# Sensor.Community Events

## `io.sensor.community.SensorInfo`

Reference data for a Sensor.Community sensor node. The bridge emits this event when it first sees a sensor in the polled feeds and whenever the metadata for that sensor changes.

Fields:

- `sensor_id` — stable Sensor.Community sensor identifier.
- `sensor_type_id` — upstream numeric identifier for the sensor hardware type.
- `sensor_type_name` — upstream hardware type name such as `SDS011` or `BME280`.
- `sensor_type_manufacturer` — manufacturer name published by Sensor.Community.
- `pin` — upstream sensor pin designation.
- `location_id` — stable Sensor.Community location identifier associated with the reading.
- `latitude` — sensor latitude in decimal degrees.
- `longitude` — sensor longitude in decimal degrees.
- `altitude` — altitude in meters when the upstream supplies it.
- `country` — ISO 3166-1 alpha-2 country code from the upstream location record.
- `indoor` — whether the sensor is marked as indoor by the upstream feed.

Subject and Kafka key: `{sensor_id}`

## `io.sensor.community.SensorReading`

Telemetry reading for one sensor at one timestamp. All measurement fields are nullable because the feed shape varies by hardware type and by individual upstream record completeness.

Fields:

- `sensor_id` — stable Sensor.Community sensor identifier.
- `timestamp` — upstream UTC timestamp formatted as `YYYY-MM-DD HH:mm:ss`.
- `sensor_type_name` — upstream hardware type name for the sensor that produced the reading.
- `pm10_ug_m3` — particulate matter PM10 concentration in µg/m³ (`P1`).
- `pm2_5_ug_m3` — particulate matter PM2.5 concentration in µg/m³ (`P2`).
- `pm1_0_ug_m3` — particulate matter PM1.0 concentration in µg/m³ (`P0`).
- `pm4_0_ug_m3` — particulate matter PM4.0 concentration in µg/m³ (`P4`).
- `temperature_celsius` — air temperature in °C.
- `humidity_percent` — relative humidity in percent.
- `pressure_pa` — atmospheric pressure in pascals.
- `pressure_sealevel_pa` — sea-level pressure in pascals.
- `noise_laeq_db` — equivalent continuous sound level in dB(A).
- `noise_la_min_db` — minimum sound level in dB(A).
- `noise_la_max_db` — maximum sound level in dB(A).

Subject and Kafka key: `{sensor_id}`
