# EPIAS/EXIST Transparency Platform (Turkey)

**Country/Region**: Turkey
**Publisher**: EPİAŞ (Energy Exchange Istanbul / Enerji Piyasaları İşletme A.Ş.)
**API Endpoint**: `https://seffaflik.epias.com.tr/electricity-service/v1/`
**Documentation**: https://seffaflik.epias.com.tr (Turkish; SPA-based portal)
**Protocol**: REST
**Auth**: None for public data (some endpoints may require registration)
**Data Format**: JSON
**Update Frequency**: Hourly (market data), 15 minutes (generation)
**License**: Publicly accessible (Turkish energy market transparency obligation)

## What It Provides

EPIAS (formerly EXIST — Energy Exchange Istanbul) operates Turkey's organized electricity and gas markets. The Transparency Platform (Şeffaflık Platformu) publishes market and generation data as required by Turkish energy market regulations.

Data categories:

- **Day-ahead market**: Market Clearing Price (MCP), volumes, bid/ask data
- **Intraday market**: Continuous trading data
- **Balancing market**: System Marginal Price (SMP), up/down regulation
- **Generation**: Real-time generation by fuel type (thermal, hydro, wind, solar, geothermal)
- **Consumption**: System load data
- **Cross-border**: Import/export with neighboring countries (Greece, Bulgaria, Georgia, Iran, Iraq, Syria)

Turkey's grid is interesting: it's synchronously interconnected with continental Europe (since 2010) and has rapidly growing renewable capacity — especially solar and wind.

## API Details

The transparency platform is built as a React SPA that calls backend REST services. The exact API endpoint structure proved difficult to verify during testing — multiple URL patterns returned 404:

```
GET https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/real-time-generation → 404
GET https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/day-ahead-mcp → 404
GET https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/mcp → 404
```

The platform is protected by an F5 BIG-IP web application firewall (identified from page source JavaScript), which may be blocking programmatic access or requiring specific headers/cookies.

An alternative path: Turkey is listed as a country in the energy-charts.info API (country=tr), though it returned 400 during testing — possibly limited data availability.

## Freshness Assessment

Market data (day-ahead prices) updates daily after market clearing. Real-time generation data updates at 15-minute intervals when accessible via the web portal. The SPA dashboard shows live data, but programmatic API access is the challenge.

## Entity Model

- **Market**: DAM (Day-Ahead Market), IDM (Intraday Market), BPM (Balancing Power Market)
- **Fuel Type**: Thermal, Hydro, Wind, Solar, Geothermal, Other
- **Price**: MCP (Market Clearing Price) in TRY/MWh
- **Time**: Turkish local time (UTC+3)
- **Region**: Single price zone (Turkey is one bidding zone)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time on dashboard, but API access unverified |
| Openness | 1 | API endpoints returned 404/blocked; WAF may prevent programmatic access |
| Stability | 2 | Government-mandated transparency platform, but SPA-based with changing API |
| Structure | 2 | Likely clean JSON behind the SPA (standard pattern), but unverified |
| Identifiers | 2 | Standard market and fuel type codes (Turkish market terminology) |
| Additive Value | 2 | Turkey is a significant and interesting grid, but partially covered by energy-charts.info |
| **Total** | **11/18** | |

## Notes

- The EPIAS platform underwent a major redesign (the current React SPA replaced an older system). The API endpoints may be fully documented in Turkish developer documentation not found during this investigation.
- The F5 WAF protection suggests the platform is serious about controlling access — may need to investigate if an API key or registration process exists.
- Turkey's grid is fascinating: it bridges Europe and Asia, has significant geothermal capacity (unique in the region), and is experiencing explosive solar growth.
- For a basic Turkey generation mix, energy-charts.info may work (country=tr) once data availability improves.
- Alternative: ENTSO-E Transparency Platform covers Turkey's data for the European-interconnected portion.
