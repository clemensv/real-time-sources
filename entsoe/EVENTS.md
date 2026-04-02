# ENTSO-E Transparency Platform Bridge Events

This document describes the events that are emitted by the ENTSO-E Transparency Platform Bridge.

- [eu.entsoe.transparency](#message-group-euentsoetransparency)
  - [eu.entsoe.transparency.ActualGenerationPerType](#message-euentsoetransparencyactualgenerationpertype)
  - [eu.entsoe.transparency.DayAheadPrices](#message-euentsoetransparencydayaheadprices)
  - [eu.entsoe.transparency.ActualTotalLoad](#message-euentsoetransparencyactualtotalload)
  - [eu.entsoe.transparency.WindSolarForecast](#message-euentsoetransparencywindsolarforecast)
  - [eu.entsoe.transparency.LoadForecastMargin](#message-euentsoetransparencyloadforecastmargin)
  - [eu.entsoe.transparency.GenerationForecast](#message-euentsoetransparencygenerationforecast)
  - [eu.entsoe.transparency.ReservoirFillingInformation](#message-euentsoetransparencyreservoirfillinginformation)
  - [eu.entsoe.transparency.ActualGeneration](#message-euentsoetransparencyactualgeneration)
  - [eu.entsoe.transparency.WindSolarGeneration](#message-euentsoetransparencywindsolargeneration)
  - [eu.entsoe.transparency.InstalledGenerationCapacityPerType](#message-euentsoetransparencyinstalledgenerationcapacitypertype)
  - [eu.entsoe.transparency.CrossBorderPhysicalFlows](#message-euentsoetransparencycrossborderphysicalflows)

---

## Message Group: eu.entsoe.transparency

---

### Message: eu.entsoe.transparency.ActualGenerationPerType

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ActualGenerationPerType` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: ActualGenerationPerType

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `psrType` | *string* | Production type code (B01=Biomass, B02=Lignite, ...) |
| `quantity` | *double* | Generated power in MW |
| `resolution` | *string* | ISO 8601 duration (PT15M, PT60M) |
| `businessType` | *string* | Business type code |
| `documentType` | *string* | ENTSO-E document type code (A75) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.DayAheadPrices

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.DayAheadPrices` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: DayAheadPrices

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `price` | *double* | Day-ahead price |
| `currency` | *string* | Currency code (EUR) |
| `unitName` | *string* | Price unit (MWH) |
| `resolution` | *string* | ISO 8601 duration |
| `documentType` | *string* | ENTSO-E document type code (A44) |
---

### Message: eu.entsoe.transparency.ActualTotalLoad

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ActualTotalLoad` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: ActualTotalLoad

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `quantity` | *double* | Total load in MW |
| `resolution` | *string* | ISO 8601 duration |
| `outDomain` | *string* (optional) | EIC code of the out domain, if applicable |
| `documentType` | *string* | ENTSO-E document type code (A65) |
---

### Message: eu.entsoe.transparency.WindSolarForecast

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.WindSolarForecast` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: WindSolarForecast

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `psrType` | *string* | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) |
| `quantity` | *double* | Forecast power in MW |
| `resolution` | *string* | ISO 8601 duration (PT15M, PT60M) |
| `businessType` | *string* | Business type code |
| `documentType` | *string* | ENTSO-E document type code (A69) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.LoadForecastMargin

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.LoadForecastMargin` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: LoadForecastMargin

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `quantity` | *double* | Forecast margin in MW |
| `resolution` | *string* | ISO 8601 duration |
| `documentType` | *string* | ENTSO-E document type code (A70) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.GenerationForecast

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.GenerationForecast` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: GenerationForecast

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `quantity` | *double* | Forecast total generation in MW |
| `resolution` | *string* | ISO 8601 duration |
| `documentType` | *string* | ENTSO-E document type code (A71) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.ReservoirFillingInformation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ReservoirFillingInformation` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: ReservoirFillingInformation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `quantity` | *double* | Stored energy in MWh |
| `resolution` | *string* | ISO 8601 duration |
| `documentType` | *string* | ENTSO-E document type code (A72) |
| `unitName` | *string* | Unit of measurement |
---

### Message: eu.entsoe.transparency.ActualGeneration

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ActualGeneration` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: ActualGeneration

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `quantity` | *double* | Total actual generation in MW |
| `resolution` | *string* | ISO 8601 duration |
| `documentType` | *string* | ENTSO-E document type code (A73) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.WindSolarGeneration

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.WindSolarGeneration` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: WindSolarGeneration

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `psrType` | *string* | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) |
| `quantity` | *double* | Actual wind/solar generation in MW |
| `resolution` | *string* | ISO 8601 duration |
| `businessType` | *string* | Business type code |
| `documentType` | *string* | ENTSO-E document type code (A74) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.InstalledGenerationCapacityPerType

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.InstalledGenerationCapacityPerType` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: InstalledGenerationCapacityPerType

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the bidding zone |
| `psrType` | *string* | Production type code (B01=Biomass, B02=Lignite, ...) |
| `quantity` | *double* | Installed capacity in MW |
| `resolution` | *string* | ISO 8601 duration |
| `businessType` | *string* | Business type code |
| `documentType` | *string* | ENTSO-E document type code (A68) |
| `unitName` | *string* | Unit of measurement (MAW) |
---

### Message: eu.entsoe.transparency.CrossBorderPhysicalFlows

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.CrossBorderPhysicalFlows` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |

#### Schema:

##### Record: CrossBorderPhysicalFlows

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `inDomain` | *string* | EIC code of the importing bidding zone |
| `outDomain` | *string* | EIC code of the exporting bidding zone |
| `quantity` | *double* | Physical flow in MW |
| `resolution` | *string* | ISO 8601 duration |
| `documentType` | *string* | ENTSO-E document type code (A11) |
| `unitName` | *string* | Unit of measurement (MAW) |
