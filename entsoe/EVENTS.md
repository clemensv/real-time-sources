# ENTSO-E Transparency Platform Bridge Events

The **ENTSO-E Transparency Platform Bridge** polls the [ENTSO-E Transparency Platform REST API](https://transparency.entsoe.eu/) for European electricity market data and emits it as [CloudEvents](https://cloudevents.io/) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 3 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `eu.entsoe.transparency.ByDomain.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`eu.entsoe.transparency.ByDomain`](#messagegroup-euentsoetransparencybydomain) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `entsoe-transparency` |
| Kafka key | `{inDomain}` |
| Deployed | False |

### Endpoint `eu.entsoe.transparency.ByDomainPsrType.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`eu.entsoe.transparency.ByDomainPsrType`](#messagegroup-euentsoetransparencybydomainpsrtype) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `entsoe-transparency` |
| Kafka key | `{inDomain}/{psrType}` |
| Deployed | False |

### Endpoint `eu.entsoe.transparency.CrossBorder.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`eu.entsoe.transparency.CrossBorder`](#messagegroup-euentsoetransparencycrossborder) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `entsoe-transparency` |
| Kafka key | `{inDomain}/{outDomain}` |
| Deployed | False |

## Messagegroups

### Messagegroup `eu.entsoe.transparency.ByDomain`
<a id="messagegroup-euentsoetransparencybydomain"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `eu.entsoe.transparency.ByDomain.Kafka` (KAFKA) |
| Messages | 6 |

#### Message `eu.entsoe.transparency.DayAheadPrices`
<a id="message-euentsoetransparencydayaheadprices"></a>

| Field | Value |
| --- | --- |
| Name | DayAheadPrices |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.DayAheadPrices`](#schema-euentsoetransparencydayaheadprices) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.DayAheadPrices` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomain.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}` |

#### Message `eu.entsoe.transparency.ActualTotalLoad`
<a id="message-euentsoetransparencyactualtotalload"></a>

| Field | Value |
| --- | --- |
| Name | ActualTotalLoad |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.ActualTotalLoad`](#schema-euentsoetransparencyactualtotalload) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.ActualTotalLoad` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomain.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}` |

#### Message `eu.entsoe.transparency.LoadForecastMargin`
<a id="message-euentsoetransparencyloadforecastmargin"></a>

| Field | Value |
| --- | --- |
| Name | LoadForecastMargin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.LoadForecastMargin`](#schema-euentsoetransparencyloadforecastmargin) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.LoadForecastMargin` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomain.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}` |

#### Message `eu.entsoe.transparency.GenerationForecast`
<a id="message-euentsoetransparencygenerationforecast"></a>

| Field | Value |
| --- | --- |
| Name | GenerationForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.GenerationForecast`](#schema-euentsoetransparencygenerationforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.GenerationForecast` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomain.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}` |

#### Message `eu.entsoe.transparency.ReservoirFillingInformation`
<a id="message-euentsoetransparencyreservoirfillinginformation"></a>

| Field | Value |
| --- | --- |
| Name | ReservoirFillingInformation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.ReservoirFillingInformation`](#schema-euentsoetransparencyreservoirfillinginformation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.ReservoirFillingInformation` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomain.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}` |

#### Message `eu.entsoe.transparency.ActualGeneration`
<a id="message-euentsoetransparencyactualgeneration"></a>

| Field | Value |
| --- | --- |
| Name | ActualGeneration |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.ActualGeneration`](#schema-euentsoetransparencyactualgeneration) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.ActualGeneration` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomain.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}` |

### Messagegroup `eu.entsoe.transparency.ByDomainPsrType`
<a id="messagegroup-euentsoetransparencybydomainpsrtype"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `eu.entsoe.transparency.ByDomainPsrType.Kafka` (KAFKA) |
| Messages | 4 |

#### Message `eu.entsoe.transparency.ActualGenerationPerType`
<a id="message-euentsoetransparencyactualgenerationpertype"></a>

| Field | Value |
| --- | --- |
| Name | ActualGenerationPerType |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.ActualGenerationPerType`](#schema-euentsoetransparencyactualgenerationpertype) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.ActualGenerationPerType` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomainPsrType.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}/{psrType}` |

#### Message `eu.entsoe.transparency.WindSolarForecast`
<a id="message-euentsoetransparencywindsolarforecast"></a>

| Field | Value |
| --- | --- |
| Name | WindSolarForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.WindSolarForecast`](#schema-euentsoetransparencywindsolarforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.WindSolarForecast` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomainPsrType.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}/{psrType}` |

#### Message `eu.entsoe.transparency.WindSolarGeneration`
<a id="message-euentsoetransparencywindsolargeneration"></a>

| Field | Value |
| --- | --- |
| Name | WindSolarGeneration |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.WindSolarGeneration`](#schema-euentsoetransparencywindsolargeneration) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.WindSolarGeneration` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomainPsrType.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}/{psrType}` |

#### Message `eu.entsoe.transparency.InstalledGenerationCapacityPerType`
<a id="message-euentsoetransparencyinstalledgenerationcapacitypertype"></a>

| Field | Value |
| --- | --- |
| Name | InstalledGenerationCapacityPerType |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.InstalledGenerationCapacityPerType`](#schema-euentsoetransparencyinstalledgenerationcapacitypertype) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.InstalledGenerationCapacityPerType` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.ByDomainPsrType.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}/{psrType}` |

### Messagegroup `eu.entsoe.transparency.CrossBorder`
<a id="messagegroup-euentsoetransparencycrossborder"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `eu.entsoe.transparency.CrossBorder.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `eu.entsoe.transparency.CrossBorderPhysicalFlows`
<a id="message-euentsoetransparencycrossborderphysicalflows"></a>

| Field | Value |
| --- | --- |
| Name | CrossBorderPhysicalFlows |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/eu.entsoe.transparency.jstruct/schemas/eu.entsoe.transparency.CrossBorderPhysicalFlows`](#schema-euentsoetransparencycrossborderphysicalflows) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `eu.entsoe.transparency.CrossBorderPhysicalFlows` |
| `source` |  | `string` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{outDomain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `eu.entsoe.transparency.CrossBorder.Kafka` | `KAFKA` | topic `entsoe-transparency`; key `{inDomain}/{outDomain}` |

## Schemagroups

### Schemagroup `eu.entsoe.transparency.jstruct`
<a id="schemagroup-euentsoetransparencyjstruct"></a>

#### Schema `eu.entsoe.transparency.ActualGenerationPerType`
<a id="schema-euentsoetransparencyactualgenerationpertype"></a>

| Field | Value |
| --- | --- |
| Name | ActualGenerationPerType |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/ActualGenerationPerType` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/ActualGenerationPerType` |
| Type | `object` |

###### Object `ActualGenerationPerType`
<a id="schema-node-actualgenerationpertype"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `psrType` | `string` | `True` | Production type code (B01=Biomass, B02=Lignite, ...) | - | - | - |
| `quantity` | `double` | `True` | Generated power in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration (PT15M, PT60M) | - | - | - |
| `businessType` | `string` | `True` | Business type code | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A75) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.DayAheadPrices`
<a id="schema-euentsoetransparencydayaheadprices"></a>

| Field | Value |
| --- | --- |
| Name | DayAheadPrices |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/DayAheadPrices` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/DayAheadPrices` |
| Type | `object` |

###### Object `DayAheadPrices`
<a id="schema-node-dayaheadprices"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `price` | `double` | `True` | Day-ahead price | - | - | - |
| `currency` | `string` | `True` | Currency code (EUR) | - | - | - |
| `unitName` | `string` | `True` | Price unit (MWH) | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A44) | - | - | - |

#### Schema `eu.entsoe.transparency.ActualTotalLoad`
<a id="schema-euentsoetransparencyactualtotalload"></a>

| Field | Value |
| --- | --- |
| Name | ActualTotalLoad |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/ActualTotalLoad` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/ActualTotalLoad` |
| Type | `object` |

###### Object `ActualTotalLoad`
<a id="schema-node-actualtotalload"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `quantity` | `double` | `True` | Total load in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `outDomain` | `string` | `False` | EIC code of the out domain, if applicable | - | default=`-` | default=`-` |
| `documentType` | `string` | `True` | ENTSO-E document type code (A65) | - | - | - |

#### Schema `eu.entsoe.transparency.WindSolarForecast`
<a id="schema-euentsoetransparencywindsolarforecast"></a>

| Field | Value |
| --- | --- |
| Name | WindSolarForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/WindSolarForecast` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/WindSolarForecast` |
| Type | `object` |

###### Object `WindSolarForecast`
<a id="schema-node-windsolarforecast"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `psrType` | `string` | `True` | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) | - | - | - |
| `quantity` | `double` | `True` | Forecast power in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration (PT15M, PT60M) | - | - | - |
| `businessType` | `string` | `True` | Business type code | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A69) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.LoadForecastMargin`
<a id="schema-euentsoetransparencyloadforecastmargin"></a>

| Field | Value |
| --- | --- |
| Name | LoadForecastMargin |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/LoadForecastMargin` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/LoadForecastMargin` |
| Type | `object` |

###### Object `LoadForecastMargin`
<a id="schema-node-loadforecastmargin"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `quantity` | `double` | `True` | Forecast margin in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A70) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.GenerationForecast`
<a id="schema-euentsoetransparencygenerationforecast"></a>

| Field | Value |
| --- | --- |
| Name | GenerationForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/GenerationForecast` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/GenerationForecast` |
| Type | `object` |

###### Object `GenerationForecast`
<a id="schema-node-generationforecast"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `quantity` | `double` | `True` | Forecast total generation in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A71) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.ReservoirFillingInformation`
<a id="schema-euentsoetransparencyreservoirfillinginformation"></a>

| Field | Value |
| --- | --- |
| Name | ReservoirFillingInformation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/ReservoirFillingInformation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/ReservoirFillingInformation` |
| Type | `object` |

###### Object `ReservoirFillingInformation`
<a id="schema-node-reservoirfillinginformation"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `quantity` | `double` | `True` | Stored energy in MWh | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A72) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement | - | - | - |

#### Schema `eu.entsoe.transparency.ActualGeneration`
<a id="schema-euentsoetransparencyactualgeneration"></a>

| Field | Value |
| --- | --- |
| Name | ActualGeneration |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/ActualGeneration` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/ActualGeneration` |
| Type | `object` |

###### Object `ActualGeneration`
<a id="schema-node-actualgeneration"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `quantity` | `double` | `True` | Total actual generation in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A73) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.WindSolarGeneration`
<a id="schema-euentsoetransparencywindsolargeneration"></a>

| Field | Value |
| --- | --- |
| Name | WindSolarGeneration |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/WindSolarGeneration` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/WindSolarGeneration` |
| Type | `object` |

###### Object `WindSolarGeneration`
<a id="schema-node-windsolargeneration"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `psrType` | `string` | `True` | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) | - | - | - |
| `quantity` | `double` | `True` | Actual wind/solar generation in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `businessType` | `string` | `True` | Business type code | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A74) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.InstalledGenerationCapacityPerType`
<a id="schema-euentsoetransparencyinstalledgenerationcapacitypertype"></a>

| Field | Value |
| --- | --- |
| Name | InstalledGenerationCapacityPerType |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/InstalledGenerationCapacityPerType` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/InstalledGenerationCapacityPerType` |
| Type | `object` |

###### Object `InstalledGenerationCapacityPerType`
<a id="schema-node-installedgenerationcapacitypertype"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the bidding zone | - | - | - |
| `psrType` | `string` | `True` | Production type code (B01=Biomass, B02=Lignite, ...) | - | - | - |
| `quantity` | `double` | `True` | Installed capacity in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `businessType` | `string` | `True` | Business type code | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A68) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

#### Schema `eu.entsoe.transparency.CrossBorderPhysicalFlows`
<a id="schema-euentsoetransparencycrossborderphysicalflows"></a>

| Field | Value |
| --- | --- |
| Name | CrossBorderPhysicalFlows |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/eu/entsoe/transparency/CrossBorderPhysicalFlows` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/eu/entsoe/transparency/CrossBorderPhysicalFlows` |
| Type | `object` |

###### Object `CrossBorderPhysicalFlows`
<a id="schema-node-crossborderphysicalflows"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `inDomain` | `string` | `True` | EIC code of the importing bidding zone | - | - | - |
| `outDomain` | `string` | `True` | EIC code of the exporting bidding zone | - | - | - |
| `quantity` | `double` | `True` | Physical flow in MW | - | - | - |
| `resolution` | `string` | `True` | ISO 8601 duration | - | - | - |
| `documentType` | `string` | `True` | ENTSO-E document type code (A11) | - | - | - |
| `unitName` | `string` | `True` | Unit of measurement (MAW) | - | - | - |

### Schemagroup `eu.entsoe.transparency.avro`
<a id="schemagroup-euentsoetransparencyavro"></a>

#### Schema `eu.entsoe.transparency.ActualGenerationPerType`
<a id="schema-euentsoetransparencyactualgenerationpertype"></a>

| Field | Value |
| --- | --- |
| Name | ActualGenerationPerType |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ActualGenerationPerType |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `psrType` | `string` | Production type code (B01=Biomass, B02=Lignite, ...) | `-` |
| `quantity` | `double` | Generated power in MW | `-` |
| `resolution` | `string` | ISO 8601 duration (PT15M, PT60M) | `-` |
| `businessType` | `string` | Business type code | `-` |
| `documentType` | `string` | ENTSO-E document type code (A75) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.DayAheadPrices`
<a id="schema-euentsoetransparencydayaheadprices"></a>

| Field | Value |
| --- | --- |
| Name | DayAheadPrices |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DayAheadPrices |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `price` | `double` | Day-ahead price | `-` |
| `currency` | `string` | Currency code (EUR) | `-` |
| `unitName` | `string` | Price unit (MWH) | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `documentType` | `string` | ENTSO-E document type code (A44) | `-` |

#### Schema `eu.entsoe.transparency.ActualTotalLoad`
<a id="schema-euentsoetransparencyactualtotalload"></a>

| Field | Value |
| --- | --- |
| Name | ActualTotalLoad |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ActualTotalLoad |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `quantity` | `double` | Total load in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `outDomain` | `null` \| `string` | EIC code of the out domain, if applicable | `-` |
| `documentType` | `string` | ENTSO-E document type code (A65) | `-` |

#### Schema `eu.entsoe.transparency.WindSolarForecast`
<a id="schema-euentsoetransparencywindsolarforecast"></a>

| Field | Value |
| --- | --- |
| Name | WindSolarForecast |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WindSolarForecast |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `psrType` | `string` | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) | `-` |
| `quantity` | `double` | Forecast power in MW | `-` |
| `resolution` | `string` | ISO 8601 duration (PT15M, PT60M) | `-` |
| `businessType` | `string` | Business type code | `-` |
| `documentType` | `string` | ENTSO-E document type code (A69) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.LoadForecastMargin`
<a id="schema-euentsoetransparencyloadforecastmargin"></a>

| Field | Value |
| --- | --- |
| Name | LoadForecastMargin |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | LoadForecastMargin |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `quantity` | `double` | Forecast margin in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `documentType` | `string` | ENTSO-E document type code (A70) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.GenerationForecast`
<a id="schema-euentsoetransparencygenerationforecast"></a>

| Field | Value |
| --- | --- |
| Name | GenerationForecast |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GenerationForecast |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `quantity` | `double` | Forecast total generation in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `documentType` | `string` | ENTSO-E document type code (A71) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.ReservoirFillingInformation`
<a id="schema-euentsoetransparencyreservoirfillinginformation"></a>

| Field | Value |
| --- | --- |
| Name | ReservoirFillingInformation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ReservoirFillingInformation |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `quantity` | `double` | Stored energy in MWh | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `documentType` | `string` | ENTSO-E document type code (A72) | `-` |
| `unitName` | `string` | Unit of measurement | `-` |

#### Schema `eu.entsoe.transparency.ActualGeneration`
<a id="schema-euentsoetransparencyactualgeneration"></a>

| Field | Value |
| --- | --- |
| Name | ActualGeneration |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ActualGeneration |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `quantity` | `double` | Total actual generation in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `documentType` | `string` | ENTSO-E document type code (A73) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.WindSolarGeneration`
<a id="schema-euentsoetransparencywindsolargeneration"></a>

| Field | Value |
| --- | --- |
| Name | WindSolarGeneration |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WindSolarGeneration |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `psrType` | `string` | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) | `-` |
| `quantity` | `double` | Actual wind/solar generation in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `businessType` | `string` | Business type code | `-` |
| `documentType` | `string` | ENTSO-E document type code (A74) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.InstalledGenerationCapacityPerType`
<a id="schema-euentsoetransparencyinstalledgenerationcapacitypertype"></a>

| Field | Value |
| --- | --- |
| Name | InstalledGenerationCapacityPerType |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | InstalledGenerationCapacityPerType |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the bidding zone | `-` |
| `psrType` | `string` | Production type code (B01=Biomass, B02=Lignite, ...) | `-` |
| `quantity` | `double` | Installed capacity in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `businessType` | `string` | Business type code | `-` |
| `documentType` | `string` | ENTSO-E document type code (A68) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |

#### Schema `eu.entsoe.transparency.CrossBorderPhysicalFlows`
<a id="schema-euentsoetransparencycrossborderphysicalflows"></a>

| Field | Value |
| --- | --- |
| Name | CrossBorderPhysicalFlows |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | CrossBorderPhysicalFlows |
| Namespace | eu.entsoe.transparency |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `inDomain` | `string` | EIC code of the importing bidding zone | `-` |
| `outDomain` | `string` | EIC code of the exporting bidding zone | `-` |
| `quantity` | `double` | Physical flow in MW | `-` |
| `resolution` | `string` | ISO 8601 duration | `-` |
| `documentType` | `string` | ENTSO-E document type code (A11) | `-` |
| `unitName` | `string` | Unit of measurement (MAW) | `-` |
