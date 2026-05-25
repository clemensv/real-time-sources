# NWS Forecast Zones Events

This bridge polls **NWS forecast-zone products** for Seattle/Puget Sound style use cases and emits them as CloudEvents into Kafka. It covers both:

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `Microsoft.OpenData.US.NOAA.NWS.Forecasts.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.NWS.Forecasts`](#messagegroup-microsoftopendatausnoaanwsforecasts) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `nws-forecasts` |
| Kafka key | `{zone_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Microsoft.OpenData.US.NOAA.NWS.Forecasts`
<a id="messagegroup-microsoftopendatausnoaanwsforecasts"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.NWS.Forecasts.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `Microsoft.OpenData.US.NOAA.NWS.ForecastZone`
<a id="message-microsoftopendatausnoaanwsforecastzone"></a>

| Field | Value |
| --- | --- |
| Name | ForecastZone |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.Forecasts.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.ForecastZone`](#schema-microsoftopendatausnoaanwsforecastzone) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.ForecastZone` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{zone_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Forecasts.Kafka` | `KAFKA` | topic `nws-forecasts`; key `{zone_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast`
<a id="message-microsoftopendatausnoaanwslandzoneforecast"></a>

| Field | Value |
| --- | --- |
| Name | LandZoneForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.Forecasts.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast`](#schema-microsoftopendatausnoaanwslandzoneforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{zone_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Forecasts.Kafka` | `KAFKA` | topic `nws-forecasts`; key `{zone_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast`
<a id="message-microsoftopendatausnoaanwsmarinezoneforecast"></a>

| Field | Value |
| --- | --- |
| Name | MarineZoneForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.Forecasts.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast`](#schema-microsoftopendatausnoaanwsmarinezoneforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast` |
| `source` |  | `string` | `False` | `https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/` |
| `subject` |  | `uritemplate` | `False` | `{zone_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Forecasts.Kafka` | `KAFKA` | topic `nws-forecasts`; key `{zone_id}` |

## Schemagroups

### Schemagroup `Microsoft.OpenData.US.NOAA.NWS.Forecasts.jstruct`
<a id="schemagroup-microsoftopendatausnoaanwsforecastsjstruct"></a>

#### Schema `Microsoft.OpenData.US.NOAA.NWS.ForecastZone`
<a id="schema-microsoftopendatausnoaanwsforecastzone"></a>

| Field | Value |
| --- | --- |
| Name | ForecastZone |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/nws-forecasts/schemas/Microsoft.OpenData.US.NOAA.NWS.ForecastZone.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ForecastZone`
<a id="schema-node-forecastzone"></a>

Reference data for an NWS forecast zone selected by the bridge. The api.weather.gov /zones/forecast/{zoneId} endpoint returns both public land forecast zones such as WAZ315 and marine forecast zones such as PZZ135. The bridge emits this reference event at startup and on periodic refresh so downstream consumers can correlate forecast snapshots with stable zone metadata.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/nws-forecasts/schemas/Microsoft.OpenData.US.NOAA.NWS.ForecastZone.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `zone_id` | `string` | `True` | NWS forecast zone identifier from the upstream properties.id field, such as WAZ315 for the City of Seattle public forecast zone or PZZ135 for the Puget Sound and Hood Canal marine zone. | - | pattern=`^[A-Z]{3}[0-9]{3}$` | - |
| `zone_type` | enum `['public', 'coastal', 'offshore', 'marine']` | `True` | NWS zone category from the upstream properties.type field. Forecast-zone responses use 'public' for land forecast zones and marine-oriented values such as 'coastal', 'offshore', or 'marine' for waters forecasts. | - | - | - |
| `name` | `string` | `True` | Human-readable NWS zone name from properties.name, for example 'City of Seattle' or 'Puget Sound and Hood Canal'. | - | - | - |
| `state` | `string` | `True` | Two-letter state or marine area code from properties.state. Washington forecast zones use WA for public zones and PZ for Washington coastal and inland waters marine zones. | - | pattern=`^[A-Z]{2}$` | - |
| `forecast_office_url` | `string` | `True` | Canonical api.weather.gov URL of the primary Weather Forecast Office responsible for the zone, from properties.forecastOffice. | - | - | - |
| `grid_identifier` | `union` | `False` | Grid identifier from properties.gridIdentifier. For Seattle forecast zones this is commonly the three-letter WFO grid identifier such as SEW. Marine zones can omit this field. | - | pattern=`^[A-Z]{3}$` | - |
| `awips_location_identifier` | `union` | `False` | AWIPS location identifier from properties.awipsLocationIdentifier when the zone has a matching AWIPS code. | - | - | - |
| `cwa_ids` | array of `string` | `False` | List of Weather Forecast Office county warning area identifiers from properties.cwa. The NWS publishes this as an array because a zone can be served by one or more CWAs. | - | - | - |
| `forecast_office_urls` | array of `string` | `False` | List of api.weather.gov office URLs from properties.forecastOffices. The public zone detail currently repeats the primary office here, but the endpoint models it as a list. | - | - | - |
| `time_zones` | array of `string` | `False` | Ordered list of IANA timezone names from properties.timeZone for the zone boundary. Most Puget Sound zones use a single entry of America/Los_Angeles. | - | - | - |
| `observation_station_ids` | array of `string` | `False` | Ordered list of observation station identifiers derived from the properties.observationStations URL array. The bridge strips the common URL prefix and emits only the terminal station identifier for compact reference data. | - | - | - |
| `radar_station` | `union` | `False` | Nearest NEXRAD radar station identifier from properties.radarStation, such as ATX for Seattle-area land zones, or null when the zone metadata does not declare a radar station. | - | - | - |
| `effective_date` | `datetime` | `True` | Date and time at which this zone definition became effective, from properties.effectiveDate. | - | - | - |
| `expiration_date` | `datetime` | `True` | Date and time at which this zone definition expires, from properties.expirationDate. NWS currently uses a far-future sentinel date for active zone definitions. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast`
<a id="schema-microsoftopendatausnoaanwslandzoneforecast"></a>

| Field | Value |
| --- | --- |
| Name | LandZoneForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/nws-forecasts/schemas/Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `LandZoneForecast`
<a id="schema-node-landzoneforecast"></a>

Public land-zone forecast snapshot from api.weather.gov /zones/forecast/{zoneId}/forecast. This endpoint returns narrative forecast periods for a land forecast zone such as Seattle or Tacoma. The bridge preserves the ordered forecast periods and emits the zone identifier as the Kafka key so each event represents the current forecast snapshot for one zone.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/nws-forecasts/schemas/Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `zone_id` | `string` | `True` | Forecast zone identifier for the land forecast snapshot. This matches the configured zone identifier and the upstream properties.zone URL suffix. | - | pattern=`^[A-Z]{3}[0-9]{3}$` | - |
| `updated` | `datetime` | `True` | Timestamp from properties.updated indicating when the NWS most recently updated this zone forecast. | - | - | - |
| `periods` | array of [object `LandForecastPeriod`](#schema-node-landforecastperiod) | `True` | Ordered narrative forecast periods from properties.periods. Each element represents one named daypart or day-level outlook such as Tonight, Tuesday, or Tuesday Night. | - | - | - |

###### Object `LandForecastPeriod`
<a id="schema-node-landforecastperiod"></a>

One ordered narrative period from the NWS land zone forecast payload.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `period_number` | `int32` | `True` | Ordinal period number from properties.periods[].number. NWS numbers the periods in forecast order starting at 1. | - | - | - |
| `period_name` | `string` | `True` | Human-readable forecast period label from properties.periods[].name, for example Tonight, Tuesday, or Tuesday Night. | - | - | - |
| `detailed_forecast` | `string` | `True` | Full narrative forecast text from properties.periods[].detailedForecast. This text carries the forecast content including precipitation chances, temperature ranges, and wind conditions. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast`
<a id="schema-microsoftopendatausnoaanwsmarinezoneforecast"></a>

| Field | Value |
| --- | --- |
| Name | MarineZoneForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/nws-forecasts/schemas/Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MarineZoneForecast`
<a id="schema-node-marinezoneforecast"></a>

Marine forecast bulletin snapshot parsed from the NOAA/NWS coastal waters text feed under tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/. The upstream feed is plain text rather than structured JSON, so the bridge emits the bulletin metadata plus an ordered array of named narrative periods for the selected marine zone.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/nws-forecasts/schemas/Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `zone_id` | `string` | `True` | Marine forecast zone identifier parsed from the bulletin zone header line, such as PZZ135 for Puget Sound and Hood Canal. | - | pattern=`^[A-Z]{3}[0-9]{3}$` | - |
| `zone_name` | `string` | `True` | Marine zone display name parsed from the zone header line immediately following the zone identifier in the text bulletin. | - | - | - |
| `product_title` | `union` | `False` | Bulletin title line, such as 'Coastal Waters Forecast for Washington'. | - | - | - |
| `office_name` | `union` | `False` | Issuing office line from the bulletin header, for example 'National Weather Service Seattle WA'. | - | - | - |
| `issued_at_text` | `string` | `True` | Issue time line from the zone-specific section of the marine bulletin, preserved as the original text because the feed uses local-office time abbreviations such as PDT. | - | - | - |
| `expires_text` | `union` | `False` | Raw Expires header value from the bulletin preamble, preserved as text because the feed does not provide an explicit timezone annotation in ISO form. | - | - | - |
| `wmo_header` | `union` | `False` | WMO abbreviated heading line from the marine bulletin, for example 'FZUS56 KSEW 132142'. | - | - | - |
| `bulletin_awips_id` | `union` | `False` | AWIPS product identifier line from the bulletin, for example CWFSEW. | - | - | - |
| `synopsis` | `union` | `False` | Narrative synopsis paragraph that appears before the zone-specific section and describes the broader marine area covered by the bulletin. | - | - | - |
| `periods` | array of [object `MarineForecastPeriod`](#schema-node-marineforecastperiod) | `True` | Ordered narrative forecast periods parsed from the zone-specific section. Each element preserves the named period heading and its free-text forecast text. | - | - | - |
| `bulletin_text` | `string` | `True` | Zone-specific marine bulletin body including the ordered period sections, preserved as plain text so downstream consumers can retain the original marine forecast wording. | - | - | - |

###### Object `MarineForecastPeriod`
<a id="schema-node-marineforecastperiod"></a>

One named forecast period parsed from the marine text bulletin.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `period_name` | `string` | `True` | Uppercase period label parsed from the leading token in the bulletin section, such as TONIGHT, TUE, or SAT NIGHT. | - | - | - |
| `forecast_text` | `string` | `True` | Narrative forecast text for the period, preserving the marine bulletin wording about winds, seas, waves, precipitation, and outlook conditions. | - | - | - |
