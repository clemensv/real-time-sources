# USGS Instantaneous Values API Bridge Events

This document describes the events that are emitted by the USGS Instantaneous Values API Bridge.

- [USGS.Sites](#message-group-usgssites)
  - [USGS.Sites.Site](#message-usgssitessite)
  - [USGS.Sites.SiteTimeseries](#message-usgssitessitetimeseries)
- [USGS.InstantaneousValues](#message-group-usgsinstantaneousvalues)
  - [USGS.InstantaneousValues.OtherParameter](#message-usgsinstantaneousvaluesotherparameter)
  - [USGS.InstantaneousValues.Precipitation](#message-usgsinstantaneousvaluesprecipitation)
  - [USGS.InstantaneousValues.Streamflow](#message-usgsinstantaneousvaluesstreamflow)
  - [USGS.InstantaneousValues.GageHeight](#message-usgsinstantaneousvaluesgageheight)
  - [USGS.InstantaneousValues.WaterTemperature](#message-usgsinstantaneousvalueswatertemperature)
  - [USGS.InstantaneousValues.DissolvedOxygen](#message-usgsinstantaneousvaluesdissolvedoxygen)
  - [USGS.InstantaneousValues.pH](#message-usgsinstantaneousvaluesph)
  - [USGS.InstantaneousValues.SpecificConductance](#message-usgsinstantaneousvaluesspecificconductance)
  - [USGS.InstantaneousValues.Turbidity](#message-usgsinstantaneousvaluesturbidity)
  - [USGS.InstantaneousValues.AirTemperature](#message-usgsinstantaneousvaluesairtemperature)
  - [USGS.InstantaneousValues.WindSpeed](#message-usgsinstantaneousvalueswindspeed)
  - [USGS.InstantaneousValues.WindDirection](#message-usgsinstantaneousvalueswinddirection)
  - [USGS.InstantaneousValues.RelativeHumidity](#message-usgsinstantaneousvaluesrelativehumidity)
  - [USGS.InstantaneousValues.BarometricPressure](#message-usgsinstantaneousvaluesbarometricpressure)
  - [USGS.InstantaneousValues.TurbidityFNU](#message-usgsinstantaneousvaluesturbidityfnu)
  - [USGS.InstantaneousValues.fDOM](#message-usgsinstantaneousvaluesfdom)
  - [USGS.InstantaneousValues.ReservoirStorage](#message-usgsinstantaneousvaluesreservoirstorage)
  - [USGS.InstantaneousValues.LakeElevationNGVD29](#message-usgsinstantaneousvalueslakeelevationngvd29)
  - [USGS.InstantaneousValues.WaterDepth](#message-usgsinstantaneousvalueswaterdepth)
  - [USGS.InstantaneousValues.EquipmentStatus](#message-usgsinstantaneousvaluesequipmentstatus)
  - [USGS.InstantaneousValues.TidallyFilteredDischarge](#message-usgsinstantaneousvaluestidallyfiltereddischarge)
  - [USGS.InstantaneousValues.WaterVelocity](#message-usgsinstantaneousvalueswatervelocity)
  - [USGS.InstantaneousValues.EstuaryElevationNGVD29](#message-usgsinstantaneousvaluesestuaryelevationngvd29)
  - [USGS.InstantaneousValues.LakeElevationNAVD88](#message-usgsinstantaneousvalueslakeelevationnavd88)
  - [USGS.InstantaneousValues.Salinity](#message-usgsinstantaneousvaluessalinity)
  - [USGS.InstantaneousValues.GateOpening](#message-usgsinstantaneousvaluesgateopening)

---

## Message Group: USGS.Sites

---

### Message: USGS.Sites.Site

*USGS site metadata.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.Sites.Site` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |

#### Schema:

##### Record: Site

*USGS site metadata.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `agency_cd` | *string* | Agency code. |
| `site_no` | *string* | USGS site number. |
| `station_nm` | *string* | Station name. |
| `site_tp_cd` | *string* | Site type code. |
| `dec_lat_va` | *float* (optional) | Decimal latitude. |
| `dec_long_va` | *float* (optional) | Decimal longitude. |
| `coord_acy_cd` | *string* | Coordinate accuracy code. |
| `dec_coord_datum_cd` | *string* | Decimal coordinate datum code. |
| `alt_va` | *float* (optional) | Altitude. |
| `alt_acy_va` | *float* (optional) | Altitude accuracy. |
| `alt_datum_cd` | *string* | Altitude datum code. |
---

### Message: USGS.Sites.SiteTimeseries

*USGS site timeseries metadata.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.Sites.SiteTimeseries` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Schema:

##### Record: SiteTimeseries

*USGS site timeseries metadata.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `agency_cd` | *string* | Agency code. |
| `site_no` | *string* | USGS site number. |
| `parameter_cd` | *string* | Parameter code. |
| `timeseries_cd` | *string* | Timeseries code. |
| `description` | *string* | Description. |
## Message Group: USGS.InstantaneousValues

---

### Message: USGS.InstantaneousValues.OtherParameter

*USGS other parameter data.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.OtherParameter` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: OtherParameter

*USGS other parameter data.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.Precipitation

*USGS precipitation data. Parameter code 00045.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.Precipitation` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: Precipitation

*USGS precipitation data. Parameter code 00045.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Precipitation value, inches."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.Streamflow

*USGS streamflow data. Parameter code 00060.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.Streamflow` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: Streamflow

*USGS streamflow data. Parameter code 00060.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Discharge value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.GageHeight

*USGS gage height data. Parameter code 00065.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.GageHeight` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: GageHeight

*USGS gage height data. Parameter code 00065.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Gage height value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.WaterTemperature

*USGS water temperature data. Parameter code 00010.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.WaterTemperature` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: WaterTemperature

*USGS water temperature data. Parameter code 00010.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Water temperature value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.DissolvedOxygen

*USGS dissolved oxygen data. Parameter code 00300.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.DissolvedOxygen` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: DissolvedOxygen

*USGS dissolved oxygen data. Parameter code 00300.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Dissolved oxygen value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.pH

*USGS pH data. Parameter code 00400.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.pH` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: pH

*USGS pH data. Parameter code 00400.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "pH value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.SpecificConductance

*USGS specific conductance data. Parameter code 00095.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.SpecificConductance` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: SpecificConductance

*USGS specific conductance data. Parameter code 00095.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Specific conductance value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.Turbidity

*USGS turbidity data. Parameter code 00076.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.Turbidity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: Turbidity

*USGS turbidity data. Parameter code 00076.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Turbidity value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.AirTemperature

*USGS air temperature data. Parameter code 00020.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.AirTemperature` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: AirTemperature

*USGS air temperature data. Parameter code 00020.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Air temperature value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.WindSpeed

*USGS wind speed data. Parameter code 00035.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.WindSpeed` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: WindSpeed

*USGS wind speed data. Parameter code 00035.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Wind speed value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.WindDirection

*USGS wind direction data. Parameter codes 00036 and 163695.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.WindDirection` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: WindDirection

*USGS wind direction data. Parameter codes 00036 and 163695.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Wind direction value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.RelativeHumidity

*USGS relative humidity data. Parameter code 00052.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.RelativeHumidity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: RelativeHumidity

*USGS relative humidity data. Parameter code 00052.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Relative humidity value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.BarometricPressure

*USGS barometric pressure data. Parameter codes 62605 and 75969.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.BarometricPressure` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: BarometricPressure

*USGS barometric pressure data. Parameter codes 62605 and 75969.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Barometric pressure value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.TurbidityFNU

*USGS turbidity data (FNU). Parameter code 63680.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.TurbidityFNU` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: TurbidityFNU

*USGS turbidity data (FNU). Parameter code 63680.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Turbidity value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.fDOM

*USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.fDOM` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: fDOM

*USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Dissolved organic matter fluorescence value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.ReservoirStorage

*USGS reservoir storage data. Parameter code 00054.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.ReservoirStorage` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: ReservoirStorage

*USGS reservoir storage data. Parameter code 00054.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Reservoir storage value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.LakeElevationNGVD29

*USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.LakeElevationNGVD29` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: LakeElevationNGVD29

*USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Lake elevation above NGVD 1929."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.WaterDepth

*USGS water depth data. Parameter code 72199.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.WaterDepth` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: WaterDepth

*USGS water depth data. Parameter code 72199.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Water depth value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.EquipmentStatus

*USGS equipment alarm status data. Parameter code 99235.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.EquipmentStatus` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: EquipmentStatus

*USGS equipment alarm status data. Parameter code 99235.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `status` | *string* (optional) | {"description": "Status of equipment alarm as codes."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.TidallyFilteredDischarge

*USGS tidally filtered discharge data. Parameter code 72137.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.TidallyFilteredDischarge` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: TidallyFilteredDischarge

*USGS tidally filtered discharge data. Parameter code 72137.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Tidally filtered discharge value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.WaterVelocity

*USGS water velocity data. Parameter code 72254.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.WaterVelocity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: WaterVelocity

*USGS water velocity data. Parameter code 72254.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Water velocity value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.EstuaryElevationNGVD29

*USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.EstuaryElevationNGVD29` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: EstuaryElevationNGVD29

*USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Estuary or ocean water surface elevation above NGVD 1929."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.LakeElevationNAVD88

*USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.LakeElevationNAVD88` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: LakeElevationNAVD88

*USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Lake elevation above NAVD 1988."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.Salinity

*USGS salinity data. Parameter code 00480.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.Salinity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: Salinity

*USGS salinity data. Parameter code 00480.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Salinity value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
---

### Message: USGS.InstantaneousValues.GateOpening

*USGS gate opening data. Parameter code 45592.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `USGS.InstantaneousValues.GateOpening` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

#### Schema:

##### Record: GateOpening

*USGS gate opening data. Parameter code 45592.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_no` | *string* | {"description": "USGS site number."} |
| `datetime` | *string* | {"description": "Date and time of the measurement in ISO-8601 format."} |
| `value` | *double* (optional) | {"description": "Gate opening value."} |
| `exception` | *string* (optional) | {"description": "Exception code when the value is unavailable."} |
| `qualifiers` | *array* | {"description": "Qualifiers for the measurement."} |
| `parameter_cd` | *string* | {"description": "Parameter code."} |
| `timeseries_cd` | *string* | {"description": "Timeseries code."} |
