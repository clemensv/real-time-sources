# NOAA SWPC Space Weather Poller Events

**NOAA SWPC Space Weather Poller** polls the NOAA Space Weather Prediction Center (SWPC) API endpoints for space weather data and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen data timestamps to avoid sending duplicates.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 5 |
| Messagegroups | 5 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `Microsoft.OpenData.US.NOAA.SWPC.Alerts.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.SWPC.Alerts`](#messagegroup-microsoftopendatausnoaaswpcalerts) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-goes` |
| Kafka key | `{product_id}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.US.NOAA.SWPC.Observations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.SWPC.Observations`](#messagegroup-microsoftopendatausnoaaswpcobservations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-goes` |
| Kafka key | `{observation_time}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux`](#messagegroup-microsoftopendatausnoaaswpcgoesparticleflux) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-goes` |
| Kafka key | `{satellite}/{energy}/{time_tag}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.US.NOAA.SWPC.GOESMagnetometer.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.SWPC.GOESMagnetometer`](#messagegroup-microsoftopendatausnoaaswpcgoesmagnetometer) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-goes` |
| Kafka key | `{satellite}/{time_tag}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.US.NOAA.SWPC.SolarFlares.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.SWPC.SolarFlares`](#messagegroup-microsoftopendatausnoaaswpcsolarflares) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-goes` |
| Kafka key | `{satellite}/{begin_time}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Microsoft.OpenData.US.NOAA.SWPC.Alerts`
<a id="messagegroup-microsoftopendatausnoaaswpcalerts"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.SWPC.Alerts.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert`
<a id="message-microsoftopendatausnoaaswpcspaceweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | SpaceWeatherAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert`](#schema-microsoftopendatausnoaaswpcspaceweatheralert) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{product_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.Alerts.Kafka` | `KAFKA` | topic `noaa-goes`; key `{product_id}` |

### Messagegroup `Microsoft.OpenData.US.NOAA.SWPC.Observations`
<a id="messagegroup-microsoftopendatausnoaaswpcobservations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.SWPC.Observations.Kafka` (KAFKA) |
| Messages | 4 |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex`
<a id="message-microsoftopendatausnoaaswpcplanetarykindex"></a>

| Field | Value |
| --- | --- |
| Name | PlanetaryKIndex |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex`](#schema-microsoftopendatausnoaaswpcplanetarykindex) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{observation_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.Observations.Kafka` | `KAFKA` | topic `noaa-goes`; key `{observation_time}` |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary`
<a id="message-microsoftopendatausnoaaswpcsolarwindsummary"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindSummary |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary`](#schema-microsoftopendatausnoaaswpcsolarwindsummary) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{observation_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.Observations.Kafka` | `KAFKA` | topic `noaa-goes`; key `{observation_time}` |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma`
<a id="message-microsoftopendatausnoaaswpcsolarwindplasma"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindPlasma |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma`](#schema-microsoftopendatausnoaaswpcsolarwindplasma) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{observation_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.Observations.Kafka` | `KAFKA` | topic `noaa-goes`; key `{observation_time}` |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField`
<a id="message-microsoftopendatausnoaaswpcsolarwindmagfield"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindMagField |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField`](#schema-microsoftopendatausnoaaswpcsolarwindmagfield) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{observation_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.Observations.Kafka` | `KAFKA` | topic `noaa-goes`; key `{observation_time}` |

### Messagegroup `Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux`
<a id="messagegroup-microsoftopendatausnoaaswpcgoesparticleflux"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux`
<a id="message-microsoftopendatausnoaaswpcgoesxrayflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesXrayFlux |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux`](#schema-microsoftopendatausnoaaswpcgoesxrayflux) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{satellite}/{energy}/{time_tag}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux.Kafka` | `KAFKA` | topic `noaa-goes`; key `{satellite}/{energy}/{time_tag}` |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux`
<a id="message-microsoftopendatausnoaaswpcgoesprotonflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesProtonFlux |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux`](#schema-microsoftopendatausnoaaswpcgoesprotonflux) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{satellite}/{energy}/{time_tag}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux.Kafka` | `KAFKA` | topic `noaa-goes`; key `{satellite}/{energy}/{time_tag}` |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux`
<a id="message-microsoftopendatausnoaaswpcgoeselectronflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesElectronFlux |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux`](#schema-microsoftopendatausnoaaswpcgoeselectronflux) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{satellite}/{energy}/{time_tag}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.GOESParticleFlux.Kafka` | `KAFKA` | topic `noaa-goes`; key `{satellite}/{energy}/{time_tag}` |

### Messagegroup `Microsoft.OpenData.US.NOAA.SWPC.GOESMagnetometer`
<a id="messagegroup-microsoftopendatausnoaaswpcgoesmagnetometer"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.SWPC.GOESMagnetometer.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer`
<a id="message-microsoftopendatausnoaaswpcgoesmagnetometer"></a>

| Field | Value |
| --- | --- |
| Name | GoesMagnetometer |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer`](#schema-microsoftopendatausnoaaswpcgoesmagnetometer) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{satellite}/{time_tag}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.GOESMagnetometer.Kafka` | `KAFKA` | topic `noaa-goes`; key `{satellite}/{time_tag}` |

### Messagegroup `Microsoft.OpenData.US.NOAA.SWPC.SolarFlares`
<a id="messagegroup-microsoftopendatausnoaaswpcsolarflares"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.SWPC.SolarFlares.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Microsoft.OpenData.US.NOAA.SWPC.XrayFlare`
<a id="message-microsoftopendatausnoaaswpcxrayflare"></a>

| Field | Value |
| --- | --- |
| Name | XrayFlare |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.SWPC.jstruct/schemas/Microsoft.OpenData.US.NOAA.SWPC.XrayFlare`](#schema-microsoftopendatausnoaaswpcxrayflare) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.SWPC.XrayFlare` |
| `source` |  | `string` | `False` | `https://services.swpc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{satellite}/{begin_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.SWPC.SolarFlares.Kafka` | `KAFKA` | topic `noaa-goes`; key `{satellite}/{begin_time}` |

## Schemagroups

### Schemagroup `Microsoft.OpenData.US.NOAA.SWPC.jstruct`
<a id="schemagroup-microsoftopendatausnoaaswpcjstruct"></a>

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert`
<a id="schema-microsoftopendatausnoaaswpcspaceweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | SpaceWeatherAlert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SpaceWeatherAlert` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SpaceWeatherAlert`
<a id="schema-node-spaceweatheralert"></a>

NOAA Space Weather Prediction Center alert, watch, or warning bulletin. Alerts are issued for observed or expected space weather conditions that may affect technology systems on Earth or in space, including geomagnetic storms (ALTK/WARK), solar radiation storms (ALTPC/WARPC), and radio blackouts (ALTXR/SUM).

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SpaceWeatherAlert` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `product_id` | `string` | `True` | Unique SWPC product identifier for this alert bulletin, combining the alert type code and serial number or date (e.g., 'ALTK04-20240101'). Used as the Kafka message key. | - | - | - |
| `issue_datetime` | `string` | `True` | Date and time the alert was issued by SWPC, formatted as 'YYYY Mon DD HHMM UTC' (e.g., '2024 Jan 01 0030 UTC'). | - | - | - |
| `message` | `string` | `True` | Full text body of the SWPC alert bulletin, including the message code, serial number, issue time, IP code, validity period, and detailed description of the observed or expected space weather condition with numerical thresholds. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex`
<a id="schema-microsoftopendatausnoaaswpcplanetarykindex"></a>

| Field | Value |
| --- | --- |
| Name | PlanetaryKIndex |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/PlanetaryKIndex` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PlanetaryKIndex`
<a id="schema-node-planetarykindex"></a>

Planetary K-index (Kp) observation from the NOAA Space Weather Prediction Center. The Kp index quantifies disturbances in the horizontal component of Earth's magnetic field on a 0-9 quasi-logarithmic scale, derived from 3-hour standardized K values at a global network of ground magnetometer stations. Values of Kp >= 5 indicate geomagnetic storm conditions (G1-G5 on the NOAA scale).

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/PlanetaryKIndex` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `observation_time` | `string` | `True` | UTC date-time marking the start of the 3-hour Kp observation period, in 'YYYY-MM-DD HH:MM:SS.fff' format from the SWPC noaa-planetary-k-index endpoint. | altnames=`["time_tag"]` | - | - |
| `kp` | `double` | `True` | Planetary K-index value for this 3-hour period, ranging from 0.00 (quiet) to 9.00 (extreme storm). Each unit increase corresponds to roughly a doubling of geomagnetic disturbance amplitude. Storm thresholds: G1 (Kp=5), G2 (Kp=6), G3 (Kp=7), G4 (Kp=8), G5 (Kp=9). | - | maximum=`9`<br>minimum=`0` | - |
| `a_running` | `double` | `True` | Running daily planetary A-index (Ap), a linear measure of geomagnetic activity derived from the eight 3-hour Kp values via a standard conversion table. Ap is measured in units of 2 nT. | unit=`nT` symbol=`nT` | - | - |
| `station_count` | `integer` | `True` | Number of ground magnetometer stations contributing data to this Kp determination. Typical station count is 8-13; fewer stations may reduce measurement confidence. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary`
<a id="schema-microsoftopendatausnoaaswpcsolarwindsummary"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindSummary |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SolarWindSummary` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SolarWindSummary`
<a id="schema-node-solarwindsummary"></a>

Latest solar wind conditions summary from the DSCOVR satellite at the L1 Lagrange point (~1.5 million km sunward of Earth), combining proton bulk speed from the summary/solar-wind-speed endpoint and interplanetary magnetic field from the summary/solar-wind-mag-field endpoint. Provides a single snapshot of current conditions, updated approximately every minute.

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SolarWindSummary` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `observation_time` | `string` | `True` | UTC date-time of the solar wind measurement from DSCOVR, in ISO 8601 format. | altnames=`["time_tag", "TimeStamp"]` | - | - |
| `wind_speed` | `double` | `True` | Solar wind proton bulk speed measured by DSCOVR at L1. Typical slow-wind values are 300-400 km/s; fast streams and CME passages can reach 500-1000+ km/s. | unit=`km/s` symbol=`km/s` | - | - |
| `bt` | `double` | `True` | Interplanetary magnetic field total magnitude (Bt) measured by the DSCOVR magnetometer at L1. Quiet-time values are typically 3-6 nT; values above 20 nT indicate strong solar wind driving. | unit=`nT` symbol=`nT` | - | - |
| `bz` | `double` | `True` | Interplanetary magnetic field north-south component in Geocentric Solar Magnetospheric (GSM) coordinates (Bz GSM). Sustained negative (southward) Bz is the primary driver of geomagnetic storms via magnetic reconnection at Earth's magnetopause. | unit=`nT` symbol=`nT` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma`
<a id="schema-microsoftopendatausnoaaswpcsolarwindplasma"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindPlasma |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SolarWindPlasma` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SolarWindPlasma`
<a id="schema-node-solarwindplasma"></a>

One-minute resolution solar wind plasma measurement from the DSCOVR satellite Faraday Cup instrument at the L1 Lagrange point, as reported by the SWPC solar-wind/plasma-7-day endpoint. Includes proton density, bulk speed, and ion temperature. DSCOVR provides approximately 15-45 minutes of advance warning before solar wind structures reach Earth's magnetosphere.

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SolarWindPlasma` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `observation_time` | `string` | `True` | UTC date-time of the plasma measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format. | altnames=`["time_tag"]` | - | - |
| `density` | `union` | `False` | Solar wind proton number density measured by the DSCOVR Faraday Cup. Typical quiet-time values are 3-10 n/cm³; values above 20 n/cm³ may indicate a coronal mass ejection passage or a compressed solar wind region. | unit=`n/cm³` symbol=`n/cm³` | - | - |
| `speed` | `union` | `False` | Solar wind proton bulk speed measured by DSCOVR. Typical quiet-time values are 300-400 km/s (slow wind); high-speed streams reach 500-800 km/s and CME-driven shocks can exceed 1000 km/s. | unit=`km/s` symbol=`km/s` | - | - |
| `temperature` | `union` | `False` | Solar wind ion temperature measured by DSCOVR. Typical values are 10,000-200,000 K; elevated temperatures often accompany high-speed streams and interplanetary shock passages. | unit=`K` symbol=`K` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField`
<a id="schema-microsoftopendatausnoaaswpcsolarwindmagfield"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindMagField |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SolarWindMagField` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SolarWindMagField`
<a id="schema-node-solarwindmagfield"></a>

One-minute resolution interplanetary magnetic field (IMF) vector measurement from the DSCOVR satellite magnetometer at the L1 Lagrange point, as reported by the SWPC solar-wind/mag-7-day endpoint. Provides the full magnetic field vector in Geocentric Solar Magnetospheric (GSM) coordinates plus total magnitude. The Bz GSM component is the primary indicator of geomagnetic storm potential.

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/SolarWindMagField` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `observation_time` | `string` | `True` | UTC date-time of the magnetic field measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format. | altnames=`["time_tag"]` | - | - |
| `bx_gsm` | `union` | `False` | IMF X-component in GSM coordinates, directed from Earth toward the Sun along the Earth-Sun line. | unit=`nT` symbol=`nT` | - | - |
| `by_gsm` | `union` | `False` | IMF Y-component in GSM coordinates, perpendicular to the Earth-Sun line in the magnetic equatorial plane. Influences the dawn-dusk electric field in the magnetosphere. | unit=`nT` symbol=`nT` | - | - |
| `bz_gsm` | `union` | `False` | IMF Z-component in GSM coordinates (north-south). Sustained negative (southward) Bz is the primary driver of geomagnetic storms through magnetic reconnection at the dayside magnetopause. Values below -10 nT can produce G2+ storms. | unit=`nT` symbol=`nT` | - | - |
| `lon_gsm` | `union` | `False` | IMF longitude angle in GSM coordinates, measured in the GSM X-Y plane from the Earth-Sun line. | unit=`degrees` symbol=`°` | - | - |
| `lat_gsm` | `union` | `False` | IMF latitude angle in GSM coordinates, measured from the GSM X-Y plane toward the Z-axis. | unit=`degrees` symbol=`°` | - | - |
| `bt` | `union` | `False` | Total interplanetary magnetic field magnitude, computed as the vector sum sqrt(Bx² + By² + Bz²). Typical quiet-time values are 3-6 nT; values above 20 nT indicate strong solar wind magnetic driving. | unit=`nT` symbol=`nT` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux`
<a id="schema-microsoftopendatausnoaaswpcgoesxrayflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesXrayFlux |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesXrayFlux` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GoesXrayFlux`
<a id="schema-node-goesxrayflux"></a>

One-minute resolution full-disk solar X-ray flux measurement from the GOES primary satellite XRS (X-Ray Sensor) instrument, as reported by the SWPC goes/primary/xrays-7-day endpoint. Two energy bands are reported: 0.05-0.4 nm (short, harder X-rays) and 0.1-0.8 nm (long, softer X-rays). The 0.1-0.8 nm band is used for the official solar flare classification scale (A < B < C < M < X).

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesXrayFlux` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `time_tag` | `string` | `True` | UTC date-time of the X-ray flux measurement from the GOES XRS instrument, in ISO 8601 format (e.g., '2024-01-01T00:00:00Z'). | - | - | - |
| `satellite` | `integer` | `True` | GOES satellite number providing the measurement (e.g., 18 for GOES-18, 19 for GOES-19). The primary operational GOES satellite changes when new spacecraft are commissioned. | - | - | - |
| `flux` | `double` | `True` | Solar X-ray irradiance in the specified energy band. Flare classification thresholds for the 0.1-0.8 nm band: A (< 1e-7), B (1e-7 to 1e-6), C (1e-6 to 1e-5), M (1e-5 to 1e-4), X (>= 1e-4). Background is typically A1-B1 level during solar minimum. | unit=`W/m²` symbol=`W/m²` | - | - |
| `energy` | `string` | `True` | X-ray energy band identifier: '0.05-0.4nm' (short wavelength, harder X-rays) or '0.1-0.8nm' (long wavelength, softer X-rays used for flare classification). | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux`
<a id="schema-microsoftopendatausnoaaswpcgoesprotonflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesProtonFlux |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesProtonFlux` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GoesProtonFlux`
<a id="schema-node-goesprotonflux"></a>

Five-minute resolution integral proton flux measurement from the GOES primary satellite SEISS/SGPS (Space Environment In-Situ Suite / Solar and Galactic Proton Sensor) instrument, as reported by the SWPC goes/primary/integral-protons-7-day endpoint. Four energy thresholds are reported. The >= 10 MeV channel is used for the official NOAA S-scale solar radiation storm classification (S1-S5).

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesProtonFlux` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `time_tag` | `string` | `True` | UTC date-time of the proton flux measurement in ISO 8601 format. | - | - | - |
| `satellite` | `integer` | `True` | GOES satellite number providing the measurement (e.g., 19 for GOES-19). | - | - | - |
| `flux` | `double` | `True` | Integral proton flux above the specified energy threshold, in particle flux units (pfu = protons/cm²/sr/s). An S1 minor radiation storm is declared when >= 10 MeV flux exceeds 10 pfu. S5 extreme: >= 100,000 pfu. | unit=`pfu` symbol=`pfu` | - | - |
| `energy` | `string` | `True` | Proton energy threshold identifier: '>=10 MeV' (NOAA S-scale metric), '>=50 MeV', '>=100 MeV', or '>=500 MeV'. Higher thresholds indicate more energetic and penetrating radiation. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux`
<a id="schema-microsoftopendatausnoaaswpcgoeselectronflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesElectronFlux |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesElectronFlux` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GoesElectronFlux`
<a id="schema-node-goeselectronflux"></a>

Five-minute resolution integral electron flux measurement from the GOES primary satellite SEISS/SGPS instrument, as reported by the SWPC goes/primary/integral-electrons-3-day endpoint. The >= 2 MeV channel is monitored for deep dielectric charging risk to geosynchronous spacecraft. Elevated fluxes (> 1000 e/cm²/sr/s) sustained for several days can cause internal charging failures in satellite electronics.

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesElectronFlux` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `time_tag` | `string` | `True` | UTC date-time of the electron flux measurement in ISO 8601 format. | - | - | - |
| `satellite` | `integer` | `True` | GOES satellite number providing the measurement (e.g., 19 for GOES-19). | - | - | - |
| `flux` | `double` | `True` | Integral electron flux above the specified energy threshold, in electrons per cm² per steradian per second. Values above 1000 indicate elevated deep dielectric charging risk for geosynchronous satellites. | unit=`e/(cm²·sr·s)` symbol=`e/(cm²·sr·s)` | - | - |
| `energy` | `string` | `True` | Electron energy threshold identifier, currently '>=2 MeV'. This channel is monitored for spacecraft internal charging hazard assessment. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer`
<a id="schema-microsoftopendatausnoaaswpcgoesmagnetometer"></a>

| Field | Value |
| --- | --- |
| Name | GoesMagnetometer |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesMagnetometer` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GoesMagnetometer`
<a id="schema-node-goesmagnetometer"></a>

One-minute resolution magnetic field measurement from the GOES primary satellite magnetometer at geostationary orbit (~6.6 Earth radii), as reported by the SWPC goes/primary/magnetometers-7-day endpoint. The field is measured in the spacecraft-centered HEN coordinate system where Hp is parallel to Earth's rotation axis, He is perpendicular in the east-west direction, and Hn is radially earthward. During geomagnetic storms, Hp can drop dramatically or even become negative, indicating magnetopause compression.

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/GoesMagnetometer` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `time_tag` | `string` | `True` | UTC date-time of the magnetic field measurement in ISO 8601 format. | - | - | - |
| `satellite` | `integer` | `True` | GOES satellite number providing the measurement (e.g., 19 for GOES-19). | - | - | - |
| `he` | `union` | `False` | Magnetic field He component: perpendicular to the satellite-Earth direction and the dipole axis, positive eastward. Measures the east-west distortion of the geomagnetic field at geostationary orbit. | unit=`nT` symbol=`nT`<br>altnames=`["He"]` | - | - |
| `hp` | `union` | `False` | Magnetic field Hp component: parallel to Earth's dipole axis, positive northward. During quiet times Hp is typically 80-120 nT; during intense geomagnetic storms (G4-G5) it can drop below zero, indicating the magnetopause has been compressed inside geostationary orbit. | unit=`nT` symbol=`nT`<br>altnames=`["Hp"]` | - | - |
| `hn` | `union` | `False` | Magnetic field Hn component: along the satellite-Earth direction, positive radially earthward. | unit=`nT` symbol=`nT`<br>altnames=`["Hn"]` | - | - |
| `total` | `union` | `False` | Total magnetic field magnitude at geostationary orbit, computed as sqrt(He² + Hp² + Hn²). Typical quiet-time values are 100-120 nT. | unit=`nT` symbol=`nT` | - | - |
| `arcjet_flag` | `union` | `False` | When true, the satellite's electric propulsion (arcjet) thrusters are firing, which causes magnetic field contamination. Magnetometer readings during arcjet events should be treated with caution as they may not reflect the ambient geomagnetic field. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.XrayFlare`
<a id="schema-microsoftopendatausnoaaswpcxrayflare"></a>

| Field | Value |
| --- | --- |
| Name | XrayFlare |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/XrayFlare` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `XrayFlare`
<a id="schema-node-xrayflare"></a>

Individual solar X-ray flare event detected by the GOES primary satellite XRS instrument, as reported by the SWPC goes/primary/xray-flares-7-day endpoint. Each record represents a discrete flare event with onset, peak, and end times plus X-ray classifications on the standard A/B/C/M/X logarithmic scale. The flare classification is based on peak 0.1-0.8 nm X-ray flux: C-class (1e-6 W/m²), M-class (1e-5), X-class (1e-4).

| Field | Value |
| --- | --- |
| $id | `https://services.swpc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/SWPC/XrayFlare` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `time_tag` | `string` | `True` | UTC date-time when this flare record was reported/filed by SWPC, in ISO 8601 format. | - | - | - |
| `begin_time` | `string` | `True` | UTC date-time of the flare onset (start of the X-ray flux rise above background), in ISO 8601 format. Used as part of the Kafka key to uniquely identify each flare event. | - | - | - |
| `begin_class` | `union` | `False` | X-ray classification at flare onset, e.g., 'B6.9' or 'C1.0'. Format is a letter (A/B/C/M/X) followed by a decimal multiplier within that decade of flux. | - | - | - |
| `max_time` | `union` | `False` | UTC date-time of the peak X-ray flux during the flare, in ISO 8601 format. | - | - | - |
| `max_class` | `union` | `False` | X-ray classification at flare peak, e.g., 'C1.2', 'M5.3', 'X1.0'. This is the official flare magnitude used in space weather bulletins. | - | - | - |
| `max_xrlong` | `union` | `False` | Peak X-ray flux in the 0.1-0.8 nm (long wavelength) band at the time of maximum. | unit=`W/m²` symbol=`W/m²` | - | - |
| `max_ratio` | `union` | `False` | Ratio of 0.05-0.4 nm (short) to 0.1-0.8 nm (long) X-ray flux at flare maximum. Higher ratios indicate a spectrally harder (more energetic) flare, which correlates with stronger ionospheric effects. | - | - | - |
| `max_ratio_time` | `union` | `False` | UTC date-time of the maximum short/long flux ratio, in ISO 8601 format. May differ from max_time. | - | - | - |
| `current_int_xrlong` | `union` | `False` | Current time-integrated X-ray flux in the 0.1-0.8 nm band since flare onset, representing total X-ray energy delivered. | unit=`J/m²` symbol=`J/m²` | - | - |
| `end_time` | `union` | `False` | UTC date-time when the flare X-ray flux returned to half the peak value above background, in ISO 8601 format. Null if the flare is still in progress. | - | - | - |
| `end_class` | `union` | `False` | X-ray classification at the declared end of the flare event. | - | - | - |
| `satellite` | `integer` | `True` | GOES satellite number that detected this flare event (e.g., 18 for GOES-18, 19 for GOES-19). | - | - | - |

### Schemagroup `Microsoft.OpenData.US.NOAA.SWPC.avro`
<a id="schemagroup-microsoftopendatausnoaaswpcavro"></a>

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert`
<a id="schema-microsoftopendatausnoaaswpcspaceweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | SpaceWeatherAlert |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SpaceWeatherAlert |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | NOAA SWPC space weather alert, watch, or warning bulletin. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `product_id` | `string` |  | `-` |
| `issue_datetime` | `string` |  | `-` |
| `message` | `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex`
<a id="schema-microsoftopendatausnoaaswpcplanetarykindex"></a>

| Field | Value |
| --- | --- |
| Name | PlanetaryKIndex |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | PlanetaryKIndex |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | Planetary K-index observation with Kp, running Ap, and station count. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `observation_time` | `string` |  | `-` |
| `kp` | `double` |  | `-` |
| `a_running` | `double` |  | `-` |
| `station_count` | `int` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary`
<a id="schema-microsoftopendatausnoaaswpcsolarwindsummary"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindSummary |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SolarWindSummary |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | Latest solar wind speed and interplanetary magnetic field summary from DSCOVR at L1. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `observation_time` | `string` |  | `-` |
| `wind_speed` | `double` |  | `-` |
| `bt` | `double` |  | `-` |
| `bz` | `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SolarWindPlasma`
<a id="schema-microsoftopendatausnoaaswpcsolarwindplasma"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindPlasma |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SolarWindPlasma |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | One-minute DSCOVR solar wind plasma measurement: density, speed, temperature. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `observation_time` | `string` |  | `-` |
| `density` | `null` \| `double` |  | `-` |
| `speed` | `null` \| `double` |  | `-` |
| `temperature` | `null` \| `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.SolarWindMagField`
<a id="schema-microsoftopendatausnoaaswpcsolarwindmagfield"></a>

| Field | Value |
| --- | --- |
| Name | SolarWindMagField |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SolarWindMagField |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | One-minute DSCOVR interplanetary magnetic field vector in GSM coordinates. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `observation_time` | `string` |  | `-` |
| `bx_gsm` | `null` \| `double` |  | `-` |
| `by_gsm` | `null` \| `double` |  | `-` |
| `bz_gsm` | `null` \| `double` |  | `-` |
| `lon_gsm` | `null` \| `double` |  | `-` |
| `lat_gsm` | `null` \| `double` |  | `-` |
| `bt` | `null` \| `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux`
<a id="schema-microsoftopendatausnoaaswpcgoesxrayflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesXrayFlux |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GoesXrayFlux |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | One-minute GOES XRS solar X-ray flux measurement in two energy bands. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `time_tag` | `string` |  | `-` |
| `satellite` | `int` |  | `-` |
| `flux` | `double` |  | `-` |
| `energy` | `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux`
<a id="schema-microsoftopendatausnoaaswpcgoesprotonflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesProtonFlux |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GoesProtonFlux |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | Five-minute GOES SEISS/SGPS integral proton flux at multiple energy thresholds. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `time_tag` | `string` |  | `-` |
| `satellite` | `int` |  | `-` |
| `flux` | `double` |  | `-` |
| `energy` | `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux`
<a id="schema-microsoftopendatausnoaaswpcgoeselectronflux"></a>

| Field | Value |
| --- | --- |
| Name | GoesElectronFlux |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GoesElectronFlux |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | Five-minute GOES SEISS/SGPS integral electron flux for deep dielectric charging assessment. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `time_tag` | `string` |  | `-` |
| `satellite` | `int` |  | `-` |
| `flux` | `double` |  | `-` |
| `energy` | `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer`
<a id="schema-microsoftopendatausnoaaswpcgoesmagnetometer"></a>

| Field | Value |
| --- | --- |
| Name | GoesMagnetometer |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GoesMagnetometer |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | One-minute GOES magnetometer field measurement at geostationary orbit in HEN coordinates. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `time_tag` | `string` |  | `-` |
| `satellite` | `int` |  | `-` |
| `he` | `null` \| `double` |  | `-` |
| `hp` | `null` \| `double` |  | `-` |
| `hn` | `null` \| `double` |  | `-` |
| `total` | `null` \| `double` |  | `-` |
| `arcjet_flag` | `null` \| `boolean` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.SWPC.XrayFlare`
<a id="schema-microsoftopendatausnoaaswpcxrayflare"></a>

| Field | Value |
| --- | --- |
| Name | XrayFlare |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | XrayFlare |
| Namespace | Microsoft.OpenData.US.NOAA.SWPC |
| Type | `record` |
| Doc | Individual solar X-ray flare event with onset, peak, and end classifications. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `time_tag` | `string` |  | `-` |
| `begin_time` | `string` |  | `-` |
| `begin_class` | `null` \| `string` |  | `-` |
| `max_time` | `null` \| `string` |  | `-` |
| `max_class` | `null` \| `string` |  | `-` |
| `max_xrlong` | `null` \| `double` |  | `-` |
| `max_ratio` | `null` \| `double` |  | `-` |
| `max_ratio_time` | `null` \| `string` |  | `-` |
| `current_int_xrlong` | `null` \| `double` |  | `-` |
| `end_time` | `null` \| `string` |  | `-` |
| `end_class` | `null` \| `string` |  | `-` |
| `satellite` | `int` |  | `-` |
