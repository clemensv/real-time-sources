# Oman Directorate General of Meteorology - Weather Bulletins (Arabic)

- **Country/Region**: Sultanate of Oman
- **Endpoint**: `https://met.caa.gov.om` (main weather page)
- **Protocol**: HTML web scraping
- **Auth**: None
- **Format**: HTML (Arabic text)
- **Freshness**: Updated multiple times daily (bulletins timestamped)
- **Docs**: None (website only)
- **Score**: 6/18

## Overview

The **Directorate General of Meteorology and Air Navigation (DGMET)**, part of Oman's Public Authority for Civil Aviation (PACA), publishes daily weather forecasts, marine forecasts, and severe weather warnings on their public website at met.caa.gov.om. The site is primarily in **Arabic** and provides:
- **Current weather summary** (الطقس اليوم) — general conditions across Oman's governorates
- **Wind forecast** (الرياح) — wind direction and speed by region
- **Sea state** (حالة البحر) — wave heights for Gulf of Oman and Arabian Sea coasts
- **Warnings** (تحذيرات) — dust storms, fog, rough seas
- **Horizontal visibility** (الرؤية الأفقية)
- **Tomorrow's forecast** (توقعات الغد)
- **Multi-day outlook**

DGMET also issues **tropical cyclone warnings** for the Arabian Sea during cyclone season (May-June, October-November). Cyclones Shaheen (2021), Mekunu (2018), and Hikaa (2019) all prompted emergency bulletins from DGMET with evacuation orders for coastal governorates.

## Endpoint Analysis

**Website accessible, no API** — the met.caa.gov.om site loads successfully and displays Arabic-language weather bulletins in HTML format. The page structure is:
- Homepage: Current weather summary with update timestamp (e.g., "مُحدَّث: 22/05/2026, 17:25")
- Bulletin archive page: `/النشرات-الإخبارية/` (news bulletins)
- No JSON/XML API endpoints found
- No CAP (Common Alerting Protocol) feeds found

Sample bulletin (tested 2026-05-23):
```
الطقس اليوم:
صحو بوجه عام على معظم المحافظات مع فرص تدفق السحب المتفرقة على سواحل محافظة ظفار.
احتمال تصاعد الغبار والأتربة على المناطق الصحراوية والمكشوفة لمحافظات البريمي والظاهرة
 وظفار والوسطى وجنوب الشرقية خلال فترتي الظهيرة والمساء.
فرص تشكل السحب المنخفضة أو الضباب آخر الليل والصباح الباكر على أجزاء من محافظتي 
جنوب الشرقية والوسطى.

الرياح:
تهب على سواحل بحر عمان رياح شمالية شرقية خفيفة إلى معتدلة وتكون نشطة احيانا.
...

حالة البحر:
متوسط الموج على المناطق الساحلية الممتدة من رأس الحد الى مسقط وغرب مسندم ويصل أقصى 
ارتفاع للموج مترين...

تحذيرات:
- تصاعد الغبار والأتربة على المناطق الصحراوية والمكشوفة.
- متوسط الموج على المناطق الساحلية...

مُحدَّث: 22/05/2026, 17:25
```

Translation summary:
- **Weather today**: Clear across most governorates, scattered clouds on Dhofar coast, chance of dust/sand in desert areas (Al Buraimi, Al Dhahirah, Dhofar, Al Wusta, South Ash Sharqiyah) during afternoon/evening, fog possible in South Ash Sharqiyah and Al Wusta overnight/early morning
- **Winds**: NE light-to-moderate on Gulf of Oman coast, NW light-to-moderate in Al Buraimi/Al Dhahirah, S-SE elsewhere
- **Sea state**: Moderate waves (up to 2m) from Ras Al Hadd to Muscat and western Musandam, calm-to-moderate elsewhere (up to 1.5m)
- **Warnings**: Blowing dust in desert areas, moderate waves on specified coasts, fog in expected areas
- **Updated**: 22 May 2026, 17:25

## Integration Notes

- **Scraping challenges**: 
  - Text is in Arabic (requires Arabic NLP or translation for English-language consumers)
  - Unstructured prose format (not tabular or JSON)
  - No stable HTML element IDs or classes (brittle XPath/CSS selectors)
  - Update timestamps are embedded in Arabic text (parsing required)
  - No stable identifiers for forecast zones (governorate names mentioned in free text)
- **Fragility**: Website redesigns would break scraper immediately. No API versioning or SLA.
- **Alternatives**:
  - **WMO GTS distribution**: DGMET forecasts are distributed via WMO Global Telecommunication System to international meteorological centers. These are available as GRIB/BUFR files or decoded text bulletins from aggregators like OGIMET (SYNOP observations) but with delay and less detail than the local website.
  - **Aviation Weather API**: Provides structured METARs from Oman airports (OOMS, OOSA, etc.) but does not include the rich prose forecasts, marine state, or severe weather warnings from DGMET.
  - **CAP feeds**: If DGMET adopts CAP XML (Common Alerting Protocol) for warnings, this would become a viable machine-readable source. Currently no CAP endpoint found.
- **Additive value**: 
  - **Marine forecasts** for Gulf of Oman and Arabian Sea (wave heights, sea state) are not available from global sources at this level of detail. Oman's marine forecast is important for Salalah Port (major container transshipment hub) and fishing industry.
  - **Dust/sand storm warnings** for desert interior (relevant for aviation and ground transport).
  - **Cyclone warnings** issued during Arabian Sea tropical cyclone season (not available from global METAR aggregators).
- **Tropical cyclone bulletins**: During an active Arabian Sea cyclone threatening Oman (Shaheen-type event), DGMET issues special bulletins with:
  - Cyclone position (lat/lon approximate)
  - Expected landfall location and time
  - Rainfall forecast (mm)
  - Wind gusts (km/h)
  - Evacuation zones (Muscat, Al Batinah, Musandam)
  
  These are **high-value** warnings not available in structured format elsewhere (RSMC New Delhi bulletins are regional, not Oman-specific).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Multiple updates per day (morning, afternoon bulletins), hourly during cyclones |
| Openness | 3 | Public website, no auth required |
| Stability | 0 | HTML scraping, no API, no versioning, no SLA |
| Structure | 0 | Unstructured Arabic prose, no JSON/XML |
| Identifiers | 1 | Governorate names mentioned in text, but not as stable IDs; timestamps parseable |
| Additive value | 0 | Same meteorological data domain as METARs/SYNOP; prose format vs. structured obs |

**Verdict**: ❌ Skip

**Rationale**: While DGMET's marine forecasts and cyclone warnings are valuable, the **lack of a machine-readable API** makes this a fragile scraping target. The Arabic prose format requires translation and NLP to extract structured data (governorate names, wave heights, wind speeds). Website redesigns would break the scraper immediately.

**Alternative recommendations**:
1. **Request DGMET to publish CAP XML feeds** for severe weather warnings (tropical cyclones, dust storms, flash floods). CAP is a WMO-recommended standard for alert distribution. If Oman DGMET adopts CAP, revisit this as a ✅ Build.
2. **Use RSMC New Delhi tropical cyclone bulletins** (aggregated via GDACS) for Arabian Sea cyclone warnings affecting Oman. These are regional rather than Oman-specific but provide structured data.
3. **Use Aviation Weather API METARs** (OOMS, OOSA, OOSN, OOTH) for structured observations from Oman airports. These capture wind, visibility, pressure, and present weather (dust, fog, rain) in standard METAR format.
4. **Use WMO SYNOP data via OGIMET** or similar aggregators for Oman weather station observations. SYNOP is structured (albeit in coded format) and available from multiple sources.

**If DGMET publishes a JSON/XML API or CAP feeds in the future, upgrade this to ⚠️ Maybe or ✅ Build.**
