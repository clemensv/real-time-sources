# LAQN London Air Quality Network Events

The LAQN London Air Quality Network bridge polls the public LAQN API operated by King's College London and emits structured JSON CloudEvents to Kafka. It keeps the upstream split intact: site metadata, species metadata, hourly site measurements, and Daily Air Quality Index bulletin records.

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `uk.kcl.laqn.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.kcl.laqn`](#messagegroup-ukkcllaqn) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `laqn-london` |
| Kafka key | `{site_code}` |
| Deployed | False |

### Endpoint `uk.kcl.laqn.species.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.kcl.laqn.species`](#messagegroup-ukkcllaqnspecies) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `laqn-london` |
| Kafka key | `{species_code}` |
| Deployed | False |

## Messagegroups

### Messagegroup `uk.kcl.laqn`
<a id="messagegroup-ukkcllaqn"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.kcl.laqn.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `uk.kcl.laqn.Site`
<a id="message-ukkcllaqnsite"></a>

LAQN monitoring site reference data, including stable site identity, operator information, and WGS84 coordinates.

| Field | Value |
| --- | --- |
| Name | Site |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.kcl.laqn.jstruct/schemas/uk.kcl.laqn.Site`](#schema-ukkcllaqnsite) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.kcl.laqn.Site` |
| `source` |  | `string` | `False` | `http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=All/Json` |
| `subject` |  | `uritemplate` | `False` | `{site_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.kcl.laqn.Kafka` | `KAFKA` | topic `laqn-london`; key `{site_code}` |

#### Message `uk.kcl.laqn.Measurement`
<a id="message-ukkcllaqnmeasurement"></a>

LAQN hourly pollutant measurement for a site and species at a GMT timestamp.

| Field | Value |
| --- | --- |
| Name | Measurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.kcl.laqn.jstruct/schemas/uk.kcl.laqn.Measurement`](#schema-ukkcllaqnmeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.kcl.laqn.Measurement` |
| `source` |  | `string` | `False` | `http://api.erg.ic.ac.uk/AirQuality/Data/Site` |
| `subject` |  | `uritemplate` | `False` | `{site_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.kcl.laqn.Kafka` | `KAFKA` | topic `laqn-london`; key `{site_code}` |

#### Message `uk.kcl.laqn.DailyIndex`
<a id="message-ukkcllaqndailyindex"></a>

LAQN Daily Air Quality Index (DAQI) for a site and pollutant, published as the latest London-wide bulletin.

| Field | Value |
| --- | --- |
| Name | DailyIndex |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.kcl.laqn.jstruct/schemas/uk.kcl.laqn.DailyIndex`](#schema-ukkcllaqndailyindex) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.kcl.laqn.DailyIndex` |
| `source` |  | `string` | `False` | `http://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/Latest/GroupName=London/Json` |
| `subject` |  | `uritemplate` | `False` | `{site_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.kcl.laqn.Kafka` | `KAFKA` | topic `laqn-london`; key `{site_code}` |

### Messagegroup `uk.kcl.laqn.species`
<a id="messagegroup-ukkcllaqnspecies"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.kcl.laqn.species.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `uk.kcl.laqn.Species`
<a id="message-ukkcllaqnspecies"></a>

LAQN pollutant reference data, including descriptive text and health guidance for a pollutant code.

| Field | Value |
| --- | --- |
| Name | Species |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.kcl.laqn.jstruct/schemas/uk.kcl.laqn.Species`](#schema-ukkcllaqnspecies) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.kcl.laqn.Species` |
| `source` |  | `string` | `False` | `http://api.erg.ic.ac.uk/AirQuality/Information/Species/Json` |
| `subject` |  | `uritemplate` | `False` | `{species_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.kcl.laqn.species.Kafka` | `KAFKA` | topic `laqn-london`; key `{species_code}` |

## Schemagroups

### Schemagroup `uk.kcl.laqn.jstruct`
<a id="schemagroup-ukkcllaqnjstruct"></a>

#### Schema `uk.kcl.laqn.Site`
<a id="schema-ukkcllaqnsite"></a>

| Field | Value |
| --- | --- |
| Name | Site |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/uk/kcl/laqn/Site` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/uk/kcl/laqn/Site` |
| Type | `object` |

###### Object `Site`
<a id="schema-node-site"></a>

Reference description of a London Air Quality Network monitoring site, including its stable code, operator metadata, and WGS84 coordinates.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_code` | `string` | `True` | Stable LAQN site code that identifies the monitoring site, such as BX1. | altnames=`["@SiteCode"]` | - | - |
| `site_name` | `string` | `True` | Human-readable LAQN site name published for the monitoring site. | altnames=`["@SiteName"]` | - | - |
| `site_type` | enum `['Suburban', 'Kerbside', 'Roadside', 'Urban Background', 'Industrial', 'Rural', 'other']` | `True` | Site classification published by LAQN, such as Suburban, Kerbside, Roadside, Urban Background, Industrial, Rural, or other. | altnames=`["@SiteType"]` | - | - |
| `local_authority_code` | `string` | `True` | Stable local authority code associated with the site in the LAQN reference data. | altnames=`["@LocalAuthorityCode"]` | - | - |
| `local_authority_name` | `string` | `True` | Human-readable local authority name associated with the site in the LAQN reference data. | altnames=`["@LocalAuthorityName"]` | - | - |
| `latitude` | `union` | `True` | WGS84 latitude of the monitoring site in decimal degrees. This bridge uses the decimal latitude field, not the projected WGS84 metre coordinate, or null when the upstream site record leaves the coordinate blank. | altnames=`["@Latitude"]` | - | - |
| `longitude` | `union` | `True` | WGS84 longitude of the monitoring site in decimal degrees. This bridge uses the decimal longitude field, not the projected WGS84 metre coordinate, or null when the upstream site record leaves the coordinate blank. | altnames=`["@Longitude"]` | - | - |
| `date_opened` | `string` | `True` | Date and time when the site opened, as published by LAQN in YYYY-MM-DD HH:MM:SS format. | altnames=`["@DateOpened"]` | - | - |
| `date_closed` | `union` | `True` | Date and time when the site closed in YYYY-MM-DD HH:MM:SS format, or null when the site is still active and no closure date is published. | altnames=`["@DateClosed"]` | - | - |
| `data_owner` | `string` | `True` | Organisation listed by LAQN as the owner of the site's data. | altnames=`["@DataOwner"]` | - | - |
| `data_manager` | `string` | `True` | Organisation listed by LAQN as the manager of the monitoring site data. | altnames=`["@DataManager"]` | - | - |

#### Schema `uk.kcl.laqn.Species`
<a id="schema-ukkcllaqnspecies"></a>

| Field | Value |
| --- | --- |
| Name | Species |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/uk/kcl/laqn/Species` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/uk/kcl/laqn/Species` |
| Type | `object` |

###### Object `Species`
<a id="schema-node-species"></a>

Reference description of a LAQN pollutant species, including explanatory text and health impact guidance.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `species_code` | `string` | `True` | Stable LAQN pollutant code, such as NO2, PM10, PM25, O3, SO2, or CO. | altnames=`["@SpeciesCode"]` | - | - |
| `species_name` | `string` | `True` | Human-readable pollutant name published by LAQN for the pollutant code. | altnames=`["@SpeciesName"]` | - | - |
| `description` | `string` | `True` | LAQN explanatory description of the pollutant and how it is formed or encountered. | altnames=`["@Description"]` | - | - |
| `health_effect` | `string` | `True` | LAQN health effect guidance describing the health impacts associated with exposure to the pollutant. | altnames=`["@HealthEffect"]` | - | - |
| `link` | `string` | `True` | HTTP URL to the LAQN or LondonAir guidance page with more detailed information about the pollutant. | altnames=`["@Link"]` | - | - |

#### Schema `uk.kcl.laqn.Measurement`
<a id="schema-ukkcllaqnmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | Measurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/uk/kcl/laqn/Measurement` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/uk/kcl/laqn/Measurement` |
| Type | `object` |

###### Object `Measurement`
<a id="schema-node-measurement"></a>

Hourly air quality measurement for a LAQN site and pollutant species at a GMT timestamp.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_code` | `string` | `True` | Stable LAQN site code for the monitoring site that produced the measurement. | altnames=`["@SiteCode"]` | - | - |
| `species_code` | `string` | `True` | Stable LAQN pollutant code for the measured species. | altnames=`["@SpeciesCode"]` | - | - |
| `measurement_date_gmt` | `string` | `True` | Measurement timestamp in GMT, encoded by LAQN as YYYY-MM-DD HH:MM:SS. | altnames=`["@MeasurementDateGMT"]` | - | - |
| `value` | `double` | `True` | Measured pollutant concentration as a decimal number. The bridge omits records for timestamps where the upstream API reports an empty value. | altnames=`["@Value"]` | - | - |

#### Schema `uk.kcl.laqn.DailyIndex`
<a id="schema-ukkcllaqndailyindex"></a>

| Field | Value |
| --- | --- |
| Name | DailyIndex |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/uk/kcl/laqn/DailyIndex` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/uk/kcl/laqn/DailyIndex` |
| Type | `object` |

###### Object `DailyIndex`
<a id="schema-node-dailyindex"></a>

Daily Air Quality Index bulletin record for a LAQN site and pollutant species within the latest London-wide index publication.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_code` | `string` | `True` | Stable LAQN site code for the monitoring site to which the daily index applies. | altnames=`["@SiteCode"]` | - | - |
| `bulletin_date` | `string` | `True` | Bulletin date and time published by LAQN for the daily index, encoded as YYYY-MM-DD HH:MM:SS. | altnames=`["@BulletinDate"]` | - | - |
| `species_code` | `string` | `True` | Stable LAQN pollutant code for the species to which the daily index applies. | altnames=`["@SpeciesCode"]` | - | - |
| `air_quality_index` | `integer` | `True` | LAQN Daily Air Quality Index value from 1 to 10, where 1 to 3 is Low, 4 to 6 is Moderate, 7 to 9 is High, and 10 is Very High. | altnames=`["@AirQualityIndex"]` | maximum=`10`<br>minimum=`1` | - |
| `air_quality_band` | enum `['Low', 'Moderate', 'High', 'Very High']` | `True` | Textual Daily Air Quality Index band published by LAQN: Low, Moderate, High, or Very High. | altnames=`["@AirQualityBand"]` | - | - |
| `index_source` | enum `['Measurement', 'Forecast']` | `True` | Origin of the daily index published by LAQN, typically Measurement or Forecast. | altnames=`["@IndexSource"]` | - | - |

### Schemagroup `uk.kcl.laqn.avro`
<a id="schemagroup-ukkcllaqnavro"></a>

#### Schema `uk.kcl.laqn.Site`
<a id="schema-ukkcllaqnsite"></a>

| Field | Value |
| --- | --- |
| Name | Site |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Site |
| Namespace | uk.kcl.laqn |
| Type | `record` |
| Doc | Reference description of a London Air Quality Network monitoring site, including its stable code, operator metadata, and WGS84 coordinates. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_code` | `string` | Stable LAQN site code that identifies the monitoring site, such as BX1. | `-` |
| `site_name` | `string` | Human-readable LAQN site name published for the monitoring site. | `-` |
| `site_type` | `string` | Site classification published by LAQN, such as Suburban, Kerbside, Roadside, Urban Background, Industrial, Rural, or other. | `-` |
| `local_authority_code` | `string` | Stable local authority code associated with the site in the LAQN reference data. | `-` |
| `local_authority_name` | `string` | Human-readable local authority name associated with the site in the LAQN reference data. | `-` |
| `latitude` | `null` \| `double` | WGS84 latitude of the monitoring site in decimal degrees, or null when the upstream site record leaves the coordinate blank. | `-` |
| `longitude` | `null` \| `double` | WGS84 longitude of the monitoring site in decimal degrees, or null when the upstream site record leaves the coordinate blank. | `-` |
| `date_opened` | `string` | Date and time when the site opened, as published by LAQN in YYYY-MM-DD HH:MM:SS format. | `-` |
| `date_closed` | `null` \| `string` | Date and time when the site closed in YYYY-MM-DD HH:MM:SS format, or null when the site is still active and no closure date is published. | `-` |
| `data_owner` | `string` | Organisation listed by LAQN as the owner of the site's data. | `-` |
| `data_manager` | `string` | Organisation listed by LAQN as the manager of the monitoring site data. | `-` |

#### Schema `uk.kcl.laqn.Species`
<a id="schema-ukkcllaqnspecies"></a>

| Field | Value |
| --- | --- |
| Name | Species |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Species |
| Namespace | uk.kcl.laqn |
| Type | `record` |
| Doc | Reference description of a LAQN pollutant species, including explanatory text and health impact guidance. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `species_code` | `string` | Stable LAQN pollutant code, such as NO2, PM10, PM25, O3, SO2, or CO. | `-` |
| `species_name` | `string` | Human-readable pollutant name published by LAQN for the pollutant code. | `-` |
| `description` | `string` | LAQN explanatory description of the pollutant and how it is formed or encountered. | `-` |
| `health_effect` | `string` | LAQN health effect guidance describing the health impacts associated with exposure to the pollutant. | `-` |
| `link` | `string` | HTTP URL to the LAQN or LondonAir guidance page with more detailed information about the pollutant. | `-` |

#### Schema `uk.kcl.laqn.Measurement`
<a id="schema-ukkcllaqnmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | Measurement |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Measurement |
| Namespace | uk.kcl.laqn |
| Type | `record` |
| Doc | Hourly air quality measurement for a LAQN site and pollutant species at a GMT timestamp. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_code` | `string` | Stable LAQN site code for the monitoring site that produced the measurement. | `-` |
| `species_code` | `string` | Stable LAQN pollutant code for the measured species. | `-` |
| `measurement_date_gmt` | `string` | Measurement timestamp in GMT, encoded by LAQN as YYYY-MM-DD HH:MM:SS. | `-` |
| `value` | `double` | Measured pollutant concentration as a decimal number. The bridge omits records for timestamps where the upstream API reports an empty value. | `-` |

#### Schema `uk.kcl.laqn.DailyIndex`
<a id="schema-ukkcllaqndailyindex"></a>

| Field | Value |
| --- | --- |
| Name | DailyIndex |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DailyIndex |
| Namespace | uk.kcl.laqn |
| Type | `record` |
| Doc | Daily Air Quality Index bulletin record for a LAQN site and pollutant species within the latest London-wide index publication. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_code` | `string` | Stable LAQN site code for the monitoring site to which the daily index applies. | `-` |
| `bulletin_date` | `string` | Bulletin date and time published by LAQN for the daily index, encoded as YYYY-MM-DD HH:MM:SS. | `-` |
| `species_code` | `string` | Stable LAQN pollutant code for the species to which the daily index applies. | `-` |
| `air_quality_index` | `int` | LAQN Daily Air Quality Index value from 1 to 10. | `-` |
| `air_quality_band` | `string` | Textual Daily Air Quality Index band published by LAQN: Low, Moderate, High, or Very High. | `-` |
| `index_source` | `string` | Origin of the daily index published by LAQN, typically Measurement or Forecast. | `-` |
