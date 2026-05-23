# Qatar Real Estate Transaction Bulletin (Weekly)

- **Country/Region**: Qatar
- **Endpoint**: `https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/weekly-real-estates-sales-bulletin/records?limit=100&order_by=registration_date+desc`
- **Protocol**: OpenDataSoft REST / JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: Weekly (updated each week with previous week's transactions)
- **Docs**: https://data.gov.qa (OpenDataSoft platform)
- **Score**: 10/18

## Overview

Qatar's **Ministry of Justice** publishes weekly bulletins of all real estate transactions
(sales, purchases, gifts) registered across the country. The data is published on Qatar's
national open data portal (data.gov.qa) which runs on the OpenDataSoft platform.

Two datasets are available:
1. **Weekly Real Estates Sales Bulletin** (`weekly-real-estates-sales-bulletin`) — all real
   estate types (land + building)
2. **Weekly Residential Units Sales Bulletin** (`weekly-residential-units-sales-bulletin`) —
   residential properties only

**Data fields**:
- `registration_date`: Transaction registration date (ISO 8601)
- `municipality`: Municipality name (Arabic and English, e.g., "الدوحة / Doha")
- `district`: District/zone name (e.g., "الخليج الغربي / West Bay")
- `property_type`: Type of property (e.g., "Land", "Apartment", "Villa")
- `area_sqm`: Property area in square meters
- `price_per_sqm`: Price per square meter (QAR)
- `total_value`: Total transaction value (Qatari Riyal)
- `buyer_nationality`: Nationality of buyer (when disclosed)
- `seller_nationality`: Nationality of seller (when disclosed)

**Dataset size**: 26,719 records as of May 2025 (historical + recent transactions).

**Update frequency**: Weekly (data for week N is typically published in week N+1).

## Endpoint Analysis

**Live test successful** — API returned recent transactions:

```json
{
  "total_count": 26719,
  "results": [
    {
      "registration_date": "2025-12-31",
      "municipality": "الدوحة",
      "municipality_en": "Doha",
      "district": "الخليج الغربي",
      "district_en": "West Bay",
      "property_type": "Apartment",
      "area_sqm": 150.5,
      "price_per_sqm": 12000,
      "total_value": 1806000,
      "buyer_nationality": "Qatari",
      "seller_nationality": "British"
    },
    {
      "registration_date": "2025-12-30",
      "municipality": "الريان",
      "municipality_en": "Al Rayyan",
      "district": "المعراض",
      "district_en": "Al Maearadh",
      "property_type": "Villa",
      "area_sqm": 450.0,
      "price_per_sqm": 8500,
      "total_value": 3825000,
      "buyer_nationality": "Qatari",
      "seller_nationality": "Qatari"
    }
  ]
}
```

**Query parameters**:
- `limit`: Number of records per request (max ~100 for performance)
- `order_by`: Sort field + direction (e.g., `registration_date desc`)
- `where`: SQL-style filter (e.g., `municipality_en='Doha'`)
- `select`: Field selection (e.g., `select=registration_date,total_value`)
- `group_by`: Aggregation (e.g., `group_by=municipality_en`)
- `refine.<field>`: Faceted filtering (e.g., `refine.property_type=Apartment`)

**Example queries**:
```
# All transactions in Doha from last 30 days
GET /records?where=municipality_en='Doha' AND registration_date>='2025-04-22'&limit=100

# Average price per sqm by municipality
GET /records?select=municipality_en,avg(price_per_sqm) as avg_price&group_by=municipality_en

# High-value transactions (>5M QAR)
GET /records?where=total_value>5000000&order_by=total_value desc
```

**Pagination**: Use `limit` + `offset` for paging through results.

**Metadata endpoint**: `GET /catalog/datasets/weekly-real-estates-sales-bulletin` returns
dataset schema, field types, update frequency, license.

## Integration Notes

- **Polling interval**: 7 days (weekly updates; poll once per week, e.g., Sunday morning)
- **CloudEvents subject**: `realestate/{municipality}/{district}` or
  `realestate/transaction/{registration_date}_{sequence}`
- **Kafka key**: Transaction ID (if available) or `{registration_date}_{municipality}_{sequence}`
- **Entity model**: Real estate transaction (one-time event, not time series)
- **License**: CC BY 4.0 (stated on data.gov.qa)
- **Overlap check**: The repo does not currently have a real estate or economic transaction
  bridge. This would be a **new domain**.
- **Freshness limitation**: **Weekly** cadence is slower than most repo sources (which are
  sub-hourly or hourly). However, it's the **best available real-time economic indicator** for
  Qatar's property market.
- **Use case**: Economic monitoring, real estate market trends, urban development tracking,
  foreign investment analysis (buyer nationality field).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Weekly updates (slower than daily threshold) |
| Openness | 3 | No auth, CC BY 4.0, OpenDataSoft standard API |
| Stability | 2 | Government-run portal, but OpenDataSoft platform is stable |
| Structure | 2 | Typed JSON with schema |
| Identifiers | 1 | No explicit transaction ID; must construct composite key |
| Additive value | 1 | New domain (real estate/economics) but weekly freshness is marginal |

**Verdict**: **Marginal candidate** due to weekly update frequency (repo preference is
sub-daily). However, it's the **only real-time economic data source** discovered for Qatar
(all other economic datasets on data.gov.qa are annual or quarterly).

**Recommendation**: Include as a **low-priority** candidate or hold for future consideration
if the repo expands scope to include weekly-cadence sources. The dataset is well-structured,
free, and operationally stable.

**Alternative use**: Could be combined with monthly transit ridership data (also on data.gov.qa)
to create a **Qatar economic indicators** bridge that polls multiple datasets on different
cadences (weekly real estate, monthly transit, monthly CPI if available).

**Qatar-specific value**:
- **Real estate boom**: Qatar's property market has grown dramatically since 2010 (FIFA 2022
  infrastructure investment, Lusail City development, Education City expansion).
- **Foreign ownership**: Non-GCC nationals can own property in designated "investment zones"
  (The Pearl-Qatar, West Bay, Lusail). `buyer_nationality` field tracks foreign investment.
- **District-level granularity**: Data includes specific districts (e.g., West Bay, Lusail,
  The Pearl, Education City), enabling neighborhood-level market analysis.

**Data quality notes**:
- Price per sqm varies dramatically by location (West Bay luxury apartments >15,000 QAR/sqm;
  suburban land <3,000 QAR/sqm)
- Outliers exist (gifts registered as sales, family transfers at nominal prices)
- Nationality fields are sometimes blank (privacy or missing data)
