# Ministry of Electricity Iraq - Grid Load and Outages

- **Country/Region**: Iraq
- **Endpoint**: `http://www.moelc.gov.iq` (unreachable), `https://www.moelc.gov.iq` (unreachable)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: None accessible
- **Score**: 0/18

## Overview

Iraq has experienced **chronic power shortages** for two decades. The electricity crisis is a major political and quality-of-life issue:
- Summer temperatures regularly exceed 50°C, making air conditioning essential for survival
- Grid capacity is ~24,000 MW but peak summer demand is ~32,000+ MW
- Rolling blackouts are routine (many areas get only 4-12 hours of electricity per day)
- Riots and protests over electricity shortages have toppled ministers
- Most businesses and wealthier households rely on diesel generators
- Rural areas often have no grid connection

The Ministry of Electricity (MOE) is responsible for generation, transmission, and distribution. Key infrastructure:
- Gas turbine power plants (many damaged, aging, or under construction)
- Transmission network (often sabotaged)
- Regional distribution companies
- Imported electricity from Iran (1,200-1,400 MW) and Turkey

**Real-time grid load, outage maps, and restoration estimates would be extremely high-value public data** for Iraq — comparable to weather data for quality of life impact.

## Endpoint Analysis

**Website unreachable** — the ministry's website has been offline or blocking automated access:

```
curl http://www.moelc.gov.iq
# Result: Connection timeout or HTTP 403

curl https://www.moelc.gov.iq
# Result: Connection timeout or HTTP 403
```

No evidence of any API, outage dashboard, or real-time load publication.

## Search Attempts (Arabic)

Searched for:
- "وزارة الكهرباء العراق انقطاع التيار الوقت الحقيقي"
- "moelc.gov.iq API بيانات الشبكة"
- "تقنين الكهرباء بغداد الوقت الحقيقي"
- "خريطة الانقطاعات الكهرباء العراق"

No real-time outage data or grid load feeds found from MOE.

## Known Context

Iraq's electricity sector is characterized by:
- **No public transparency** on grid load or outages (data is not published)
- **Political sensitivity** — electricity shortages are a major source of public anger, government is reluctant to publicize the scale
- **Informal tracking** — citizens share outage information via social media and WhatsApp groups, but no structured data
- **International monitoring** — U.S. EIA publishes Iraq electricity statistics, but these are monthly/annual, not real-time

## Alternative Coverage

Since MOE does not publish real-time data, alternatives:

1. **Crowdsourced outage reporting** — a social media scraping approach could aggregate citizen reports of outages, but this is not structured data.
2. **Kurdistan Region grid** — KRG operates a separate electricity system from federal Iraq and may have better data publication (see `iq-krg-electricity.md`), but no accessible endpoint found yet.
3. **Iraq Stock Exchange** — if the exchange lists electricity distribution companies, stock price movements might correlate with grid performance, but this is indirect.

**No real-time grid or outage data exists in accessible form.**

## Significance

This is a **critical missing data source**. Electricity outages are Iraq's #1 quality-of-life issue alongside water scarcity. Real-time outage maps would have massive public utility. But the government does not publish the data, likely for political reasons.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data accessible |
| Openness | 0 | No endpoint |
| Stability | 0 | Website offline |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — **Extremely high-value missing data**. Iraq's electricity crisis makes real-time grid load and outage data as critical as weather or earthquake monitoring. But no accessible endpoint exists. The Ministry of Electricity does not publish real-time data. This is a frontier gap driven by political sensitivity (government reluctance to expose the severity of shortages). If MOE ever launches a public outage dashboard or grid status API, it should be added immediately. For now, no implementation is possible.
