# Ministry of Environment Iraq - Air Quality Monitoring

- **Country/Region**: Iraq
- **Endpoint**: `http://www.moen.gov.iq` (unreachable), `https://www.moen.gov.iq` (unreachable)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: None accessible
- **Score**: 0/18

## Overview

Iraq faces severe air quality crises from multiple sources:
- **Dust storms** — Iraq is one of the world's worst-hit countries for dust/sandstorms, causing respiratory hospitalizations and airport closures
- **Agricultural burning** — wheat stubble burning in May-June produces dense smoke plumes over Baghdad and other cities
- **Oil field emissions** — gas flaring and refinery pollution in Basra region
- **Vehicle emissions** — traffic in Baghdad, Basra, Erbil
- **Industrial pollution** — cement plants, brick kilns, petrochemical facilities
- **Transboundary pollution** — dust from Syria and Saudi Arabia

The Ministry of Environment (MOE) is nominally responsible for air quality monitoring, but the extent of its operational monitoring network is unclear.

**Air quality data would be high-value public health information** for Iraq, especially during dust storm and agricultural burning seasons.

## Endpoint Analysis

**Website unreachable/timeout** — the ministry's website has been inaccessible:

```
curl http://www.moen.gov.iq
# Result: Timeout

curl https://www.moen.gov.iq
# Result: Timeout
```

No evidence of any API, real-time air quality dashboard, or AQI station network.

## Search Attempts (Arabic)

Searched for:
- "وزارة البيئة العراق جودة الهواء الوقت الحقيقي"
- "مؤشر جودة الهواء بغداد الوقت الحقيقي"
- "moen.gov.iq محطات رصد تلوث الهواء"
- "PM2.5 العراق API"

No structured real-time air quality data found from MOE.

## Known Context

Iraq's air quality monitoring infrastructure is minimal:
- **No known nationwide AQI network** — unlike many countries, Iraq does not appear to operate a public air quality monitoring station network publishing PM2.5/PM10/O3/NO2 in real-time.
- **Baghdad monitoring** — there may be a few stations in Baghdad (possibly at the U.S. Embassy or other foreign missions), but data is not published publicly.
- **Research stations** — academic institutions (University of Baghdad, others) may have air quality sensors, but no public API.
- **Oil field monitoring** — international oil companies (IOCs) operating in Basra may monitor air quality at their facilities, but this data is proprietary.

## Alternative Coverage

Since MOE does not publish air quality data, alternatives:

1. **OpenAQ** — global air quality aggregator. Checked for Iraq:
   ```
   curl -s "https://api.openaq.org/v2/locations?country=IQ" | jq
   # Result: 0 stations in Iraq
   ```
   OpenAQ has **no Iraq coverage** as of 2025.

2. **PurpleAir** — crowdsourced PM2.5 sensors. No PurpleAir sensors registered in Iraq visible on public map.

3. **U.S. Embassy air quality** — many U.S. embassies publish real-time PM2.5 readings via AirNow.gov. Checked for Baghdad:
   - Not listed on https://www.airnow.gov/international/
   - U.S. Embassy Baghdad may measure air quality internally but does not publish

4. **Satellite-derived products** — NASA/ESA satellites measure AOD (aerosol optical depth) and can estimate ground-level PM2.5, but these are gridded products with days of latency, not real-time station obs.

**No accessible real-time air quality data exists for Iraq.**

## Significance

This is a **critical public health data gap**. Iraq's dust storms and agricultural burning create hazardous air quality conditions that hospitalize thousands. Real-time AQI data would be comparable to weather data in utility. But no accessible source exists.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data accessible |
| Openness | 0 | No endpoint |
| Stability | 0 | Website offline |
| Structure | 0 | N/A |
| Identifiers | 0 | N/A |
| Richness | 0 | N/A |

**Verdict**: ❌ **Skip** — **High-value missing data**. Iraq's air quality crises (dust storms, agricultural burning, oil field emissions) make real-time PM2.5/PM10 monitoring as critical as weather data. But no accessible endpoint exists. Ministry of Environment does not publish real-time air quality. No crowdsourced sensors (PurpleAir, Sensor.Community) are registered in Iraq. No U.S. Embassy AQI feed. This is a complete data gap. If MOE or international agencies ever publish real-time AQI for Iraq, it should be added immediately.
