# NOAA Tides and Currents API Bridge Events

This document describes the events that are emitted by the NOAA API Bridge.

- [Microsoft.OpenData.US.NOAA](#message-group-microsoftopendatausnoaa)
  - [Microsoft.OpenData.US.NOAA.WaterLevel](#message-microsoftopendatausnoaawaterlevel)
  - [Microsoft.OpenData.US.NOAA.Predictions](#message-microsoftopendatausnoaapredictions)
  - [Microsoft.OpenData.US.NOAA.AirPressure](#message-microsoftopendatausnoaaairpressure)
  - [Microsoft.OpenData.US.NOAA.AirTemperature](#message-microsoftopendatausnoaaairtemperature)
  - [Microsoft.OpenData.US.NOAA.WaterTemperature](#message-microsoftopendatausnoaawatertemperature)
  - [Microsoft.OpenData.US.NOAA.Wind](#message-microsoftopendatausnoaawind)
  - [Microsoft.OpenData.US.NOAA.Humidity](#message-microsoftopendatausnoaahumidity)
  - [Microsoft.OpenData.US.NOAA.Conductivity](#message-microsoftopendatausnoaaconductivity)
  - [Microsoft.OpenData.US.NOAA.Salinity](#message-microsoftopendatausnoaasalinity)
  - [Microsoft.OpenData.US.NOAA.Station](#message-microsoftopendatausnoaastation)
  - [Microsoft.OpenData.US.NOAA.Visibility](#message-microsoftopendatausnoaavisibility)

---

## Message Group: Microsoft.OpenData.US.NOAA

### Message: Microsoft.OpenData.US.NOAA.WaterLevel

**ID**: Microsoft.OpenData.US.NOAA.WaterLevel
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.WaterLevel`

#### Schema:

##### Record: WaterLevel

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the water level measurement"} |
| `value` | *double* | {"description": "Value of the water level"} |
| `stddev` | *double* | {"description": "Standard deviation of 1-second samples used to compute the water level height"} |
| `outside_sigma_band` | *boolean* | {"description": "Flag indicating if the water level is outside a 3-sigma band. Possible values: 'false' (not outside), 'true' (outside)."} |
| `flat_tolerance_limit` | *boolean* | {"description": "Flag indicating if the flat tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} |
| `rate_of_change_limit` | *boolean* | {"description": "Flag indicating if the rate of change tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} |
| `max_min_expected_height` | *boolean* | {"description": "Flag indicating if the max/min expected water level height is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} |
| `quality` | [Enum QualityLevel](#enum-qualitylevel) |  |

---

##### Enum: QualityLevel

*Quality Assurance/Quality Control level*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `Preliminary` | 0 |  |
| `Verified` | 1 |  |
### Message: Microsoft.OpenData.US.NOAA.Predictions

**ID**: Microsoft.OpenData.US.NOAA.Predictions
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Predictions`

#### Schema:

##### Record: Predictions

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the prediction"} |
| `value` | *double* | {"description": "Value of the prediction"} |
### Message: Microsoft.OpenData.US.NOAA.AirPressure

**ID**: Microsoft.OpenData.US.NOAA.AirPressure
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.AirPressure`

#### Schema:

##### Record: AirPressure

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the air pressure measurement"} |
| `value` | *double* | {"description": "Value of the air pressure"} |
| `max_pressure_exceeded` | *boolean* | Flag indicating if the maximum expected air pressure was exceeded |
| `min_pressure_exceeded` | *boolean* | Flag indicating if the minimum expected air pressure was exceeded |
| `rate_of_change_exceeded` | *boolean* | Flag indicating if the rate of change tolerance limit was exceeded |
### Message: Microsoft.OpenData.US.NOAA.AirTemperature

**ID**: Microsoft.OpenData.US.NOAA.AirTemperature
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.AirTemperature`

#### Schema:

##### Record: AirTemperature

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the air temperature measurement"} |
| `value` | *double* | {"description": "Value of the air temperature"} |
| `max_temp_exceeded` | *boolean* | Flag indicating if the maximum expected air temperature was exceeded |
| `min_temp_exceeded` | *boolean* | Flag indicating if the minimum expected air temperature was exceeded |
| `rate_of_change_exceeded` | *boolean* | Flag indicating if the rate of change tolerance limit was exceeded |
### Message: Microsoft.OpenData.US.NOAA.WaterTemperature

**ID**: Microsoft.OpenData.US.NOAA.WaterTemperature
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.WaterTemperature`

#### Schema:

##### Record: WaterTemperature

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the water temperature measurement"} |
| `value` | *double* | {"description": "Value of the water temperature"} |
| `max_temp_exceeded` | *boolean* | Flag indicating if the maximum expected water temperature was exceeded |
| `min_temp_exceeded` | *boolean* | Flag indicating if the minimum expected water temperature was exceeded |
| `rate_of_change_exceeded` | *boolean* | Flag indicating if the rate of change tolerance limit was exceeded |
### Message: Microsoft.OpenData.US.NOAA.Wind

**ID**: Microsoft.OpenData.US.NOAA.Wind
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Wind`

#### Schema:

##### Record: Wind

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the wind measurement"} |
| `speed` | *double* | {"description": "Wind speed"} |
| `direction_degrees` | *string* | {"description": "Wind direction"} |
| `direction_text` | *string* | {"description": "Direction - wind direction in text."} |
| `gusts` | *double* | {"description": "Wind gust speed"} |
| `max_wind_speed_exceeded` | *boolean* | Flag indicating if the maximum wind speed was exceeded |
| `rate_of_change_exceeded` | *boolean* | Flag indicating if the rate of change tolerance limit was exceeded |
### Message: Microsoft.OpenData.US.NOAA.Humidity

**ID**: Microsoft.OpenData.US.NOAA.Humidity
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Humidity`

#### Schema:

##### Record: Humidity

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the humidity measurement"} |
| `value` | *string* | {"description": "Value of the humidity"} |
| `max_humidity_exceeded` | *boolean* | Flag indicating if the maximum expected humidity was exceeded |
| `min_humidity_exceeded` | *boolean* | Flag indicating if the minimum expected humidity was exceeded |
| `rate_of_change_exceeded` | *boolean* | Flag indicating if the rate of change tolerance limit was exceeded |
### Message: Microsoft.OpenData.US.NOAA.Conductivity

**ID**: Microsoft.OpenData.US.NOAA.Conductivity
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Conductivity`

#### Schema:

##### Record: Conductivity

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the conductivity measurement"} |
| `value` | *string* | {"description": "Value of the conductivity"} |
| `max_conductivity_exceeded` | *boolean* | Flag indicating if the maximum expected conductivity was exceeded |
| `min_conductivity_exceeded` | *boolean* | Flag indicating if the minimum expected conductivity was exceeded |
| `rate_of_change_exceeded` | *boolean* | Flag indicating if the rate of change tolerance limit was exceeded |
### Message: Microsoft.OpenData.US.NOAA.Salinity

**ID**: Microsoft.OpenData.US.NOAA.Salinity
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Salinity`

#### Schema:

##### Record: Salinity

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | {"description": "7 character station ID, or a currents station ID."} |
| `timestamp` | *string* | {"description": "Timestamp of the salinity measurement"} |
| `salinity` | *double* | {"description": "Value of the salinity"} |
| `grams_per_kg` | *double* | {"description": "Grams of salt per kilogram of water"} |
### Message: Microsoft.OpenData.US.NOAA.Station

**ID**: Microsoft.OpenData.US.NOAA.Station
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Station`

#### Schema:

##### Record: Station

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `tidal` | *boolean* | {"description": "Indicates whether the station measures tidal data."} |
| `greatlakes` | *boolean* | {"description": "Indicates whether the station is located in the Great Lakes region."} |
| `shefcode` | *string* | {"description": "Standard Hydrologic Exchange Format code for the station."} |
| `details` | [Record details](#record-details) |  |
| `sensors` | [Record sensors](#record-sensors) |  |
| `floodlevels` | [Record floodlevels](#record-floodlevels) |  |
| `datums` | [Record datums](#record-datums) |  |
| `supersededdatums` | [Record supersededdatums](#record-supersededdatums) |  |
| `harmonicConstituents` | [Record harmonicConstituents](#record-harmonicconstituents) |  |
| `benchmarks` | [Record benchmarks](#record-benchmarks) |  |
| `tidePredOffsets` | [Record tidePredOffsets](#record-tidepredoffsets) |  |
| `ofsMapOffsets` | [Record ofsMapOffsets](#record-ofsmapoffsets) |  |
| `state` | *string* | {"description": "State where the station is located."} |
| `timezone` | *string* | {"description": "Timezone of the station."} |
| `timezonecorr` | *int* | {"description": "Timezone correction in minutes for the station."} |
| `observedst` | *boolean* | {"description": "Indicates whether the station observes Daylight Saving Time."} |
| `stormsurge` | *boolean* | {"description": "Indicates whether the station measures storm surge data."} |
| `nearby` | [Record nearby](#record-nearby) |  |
| `forecast` | *boolean* | {"description": "Indicates whether the station provides forecast data."} |
| `outlook` | *boolean* | {"description": "Indicates whether the station provides outlook data."} |
| `HTFhistorical` | *boolean* | {"description": "Indicates whether the station has historical High Tide Flooding data."} |
| `nonNavigational` | *boolean* | {"description": "Indicates whether the station is non-navigational."} |
| `id` | *string* | {"description": "Unique identifier for the station."} |
| `name` | *string* | {"description": "Name of the station."} |
| `lat` | *double* | {"description": "Latitude of the station."} |
| `lng` | *double* | {"description": "Longitude of the station."} |
| `affiliations` | *string* | {"description": "Affiliations of the station."} |
| `portscode` | *string* | {"description": "PORTS code for the station."} |
| `products` | [Record products](#record-products) |  |
| `disclaimers` | [Record disclaimers](#record-disclaimers) |  |
| `notices` | [Record notices](#record-notices) |  |
| `self` | *string* | {"description": "URL to the station's data."} |
| `expand` | *string* | {"description": "URL to expanded information about the station."} |
| `tideType` | *string* | {"description": "Type of tide measured by the station."} |

---

##### Record: details

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: sensors

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: floodlevels

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: datums

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: supersededdatums

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: harmonicConstituents

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: benchmarks

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: tidePredOffsets

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: ofsMapOffsets

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: nearby

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: products

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: disclaimers

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |

---

##### Record: notices

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `self` | *string* |  |
### Message: Microsoft.OpenData.US.NOAA.Visibility

**ID**: Microsoft.OpenData.US.NOAA.Visibility
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.US.NOAA.Visibility`

- **datacontenttype**: None
  - Type: *string*
  - Required: *True*
  - Value: `None`

- **subject**: None
  - Type: *string*
  - Required: *True*
  - Value: `None`

- **time**: None
  - Type: *string*
  - Required: *True*
  - Value: `None`

- **dataschema**: None
  - Type: *string*
  - Required: *True*
  - Value: `None`

#### Schema:

##### Record: Visibility

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `timestamp` | *string* | {"description": "Timestamp of the visibility measurement"} |
| `value` | *double* | {"description": "Value of the visibility"} |
| `max_visibility_exceeded` | *boolean* | A flag that indicates whether the maximum expected visibility was exceeded |
| `min_visibility_exceeded` | *boolean* | A flag that indicates whether the minimum expected visibility was exceeded |
| `rate_of_change_exceeded` | *boolean* | A flag that indicates whether the rate of change tolerance limit was exceeded |
| `station_id` | *string* |  |
