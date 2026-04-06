# Africa CDC Disease Outbreak Reports

- **Country/Region**: Pan-African (all 55 African Union member states)
- **Endpoint**: `https://africacdc.org/disease-outbreak/`
- **Protocol**: HTTP (web scraping)
- **Auth**: None
- **Format**: HTML (structured tables/lists)
- **Freshness**: Weekly updates
- **Docs**: https://africacdc.org/
- **Score**: 8/18

## Overview

The Africa Centres for Disease Control and Prevention (Africa CDC) is the African
Union's public health agency, established in 2017. It coordinates disease surveillance
and outbreak response across the continent, tracking epidemics including:

- **Mpox (Monkeypox)**: Major outbreak in DRC and surrounding countries
- **Cholera**: Endemic in East Africa, seasonal outbreaks
- **Ebola**: Central/West Africa, sporadic outbreaks
- **Measles**: Widespread across multiple countries
- **Rift Valley Fever**: East Africa, linked to El Niño rains
- **Yellow Fever**: Central/West Africa
- **Meningitis**: Meningitis Belt across Sahel
- **Marburg Virus**: East Africa

## Endpoint Analysis

**Probed** — the disease outbreak page at `https://africacdc.org/disease-outbreak/`
returns HTML with headings for "Disease Outbreak", "Description", and "Date Updated"
but the actual content appears to be dynamically loaded.

The Africa CDC also publishes:
- Weekly Event-Based Surveillance (EBS) reports
- Outbreak briefs
- Situation reports (SitReps)
- The Africa CDC dashboard (https://africacdc.org/institutes/dashboard/)

No structured API was found — this is a web-first organization with PDF/HTML publications.

Related machine-readable sources:
- **WHO AFRO IDSR**: Integrated Disease Surveillance and Response — weekly reports
- **ProMED**: International Society for Infectious Diseases alerts
- **HealthMap**: Automated disease surveillance from news/social media
- **WAHIS**: OIE animal disease notifications (relevant for zoonotic diseases)

## Integration Notes

- **Scraping approach**: The disease outbreak page requires JavaScript rendering.
  Use a headless browser (Playwright/Puppeteer) to extract outbreak tables.
- **PDF parsing**: Weekly EBS reports are published as PDFs. These could be parsed
  with PDF extraction tools, but the format is inconsistent.
- **Alternative structured sources**: For machine-readable African disease data, consider:
  - WHO Global Health Observatory API (has African data)
  - OCHA ReliefWeb API (humanitarian situation reports)
  - ProMED-mail alerts (text-based but structured)
- **Event types**: Disease outbreaks, case counts, deaths, affected areas, response status.
- **High-value but low-accessibility**: Africa CDC data is critically important but
  the lack of an API makes integration expensive. Monitor for API development — the
  institution is young and growing.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Weekly reports |
| Openness | 2 | Public website, no auth |
| Stability | 2 | Young institution, growing capacity |
| Structure | 0 | No API, HTML/PDF only |
| Identifiers | 1 | No standardized outbreak IDs |
| Richness | 2 | Multi-disease continental coverage |
