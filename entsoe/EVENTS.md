# ENTSO-E Transparency Platform Bridge Events

This document describes the events that are emitted by the ENTSO-E Transparency Platform Bridge.

- [eu.entsoe.transparency](#message-group-euentsoetransparency)
  - [eu.entsoe.transparency.ActualGenerationPerType](#message-euentsoetransparencyactualgenerationpertype)
  - [eu.entsoe.transparency.DayAheadPrices](#message-euentsoetransparencydayaheadprices)
  - [eu.entsoe.transparency.ActualTotalLoad](#message-euentsoetransparencyactualtotalload)

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
