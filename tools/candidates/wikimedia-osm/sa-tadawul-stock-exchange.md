# Saudi Stock Exchange (Tadawul) - Real-Time Market Data

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: `https://www.saudiexchange.sa` (exchange website)
- **Protocol**: WebSocket / REST (for commercial data feeds)
- **Auth**: Required (commercial license for real-time)
- **Format**: JSON, FIX protocol (Financial Information eXchange)
- **Freshness**: Real-time (millisecond latency for trades)
- **Docs**: https://www.saudiexchange.sa/wps/portal/saudiexchange/trading/market-data
- **Score**: 8/18

## Overview

**Tadawul** (تداول), formally the **Saudi Exchange** (السوق المالية السعودية), is the only stock exchange in Saudi Arabia and the largest in the Middle East by market capitalization (~$3 trillion as of 2024). Key facts:

- **Listed companies**: ~230 (including Saudi Aramco, SABIC, Al Rajhi Bank, STC)
- **Indices**: TASI (Tadawul All Share Index), Nomu-Parallel Market
- **Trading hours**: Sunday-Thursday, 10:00-15:00 AST (UTC+3)
- **Ownership**: Owned by the Saudi Exchange Group (public company)
- **MSCI classification**: Emerging market (upgraded from standalone in 2019)

**Saudi Aramco IPO** (2019): The world's largest IPO at $25.6 billion. Aramco is the most valuable listed company globally (~$2 trillion market cap).

**Tadawul operates**:
- **Equities trading** (stocks)
- **Derivatives** (futures, options — launched 2020)
- **Sukuk** (Islamic bonds)
- **ETFs** (exchange-traded funds)

## Market Data Tiers

Stock exchanges globally offer **multiple data tiers**:

1. **Real-time (Level 1)** — Last price, bid/ask, volume (millisecond latency)
   - **Commercial**: Requires paid subscription (monthly fees, per-user licenses)
   - **Free delayed**: 15-minute delay (common for retail investors)

2. **Depth-of-book (Level 2)** — Full order book (all bids/asks)
   - **Commercial only**: Expensive, used by algorithmic traders

3. **Historical data** — End-of-day prices, historical time series
   - **Often free**: Available on exchange websites or via APIs

4. **Derived data** — Indices, market statistics, sector aggregates
   - **Often free**: Calculated from trades, not raw order flow

## Tadawul Data Products

**Commercial real-time** (requires license):
- **TaFeed** (Tadawul Feed) — Real-time market data feed for professional traders
  - Protocol: FIX, proprietary binary
  - Latency: Sub-100ms
  - Pricing: Not public (contact Tadawul Market Information Services)

**Free delayed data**:
- **Tadawul website** — 15-minute delayed quotes
- **Yahoo Finance**, **Google Finance** — Delayed Tadawul data
- **TradingView** — Delayed TASI index

**Free real-time** (limited):
- Some brokers offer real-time quotes to their **clients only** (login required)
- No open real-time API exists

**Comparison with other exchanges**:

| Exchange | Country | Free real-time? | API? |
|----------|---------|-----------------|------|
| **Tadawul** | Saudi Arabia | ❌ Delayed only | ✅ Commercial (paid) |
| IEX | USA | ✅ Yes (IEX Cloud) | ✅ Free tier + paid |
| Alpha Vantage | Global aggregator | ✅ Limited free | ✅ Free key |
| Polygon.io | USA | ✅ Limited free | ✅ Free tier + paid |
| TSE | Japan | ❌ Delayed | ✅ Commercial |
| LSE | UK | ❌ Delayed | ✅ Commercial |

**IEX (Investors Exchange)** is the only major exchange with a **free real-time API** (via IEX Cloud). Most exchanges (including Tadawul) require paid licenses for real-time data.

## Endpoint Analysis

**Tadawul website**: `https://www.saudiexchange.sa`

The website provides:
- **Delayed quotes** (15-minute delay)
- **Market statistics** (daily volume, market cap, index levels)
- **Company profiles** (financials, announcements)

**No free real-time API**: Tadawul does not offer a free developer API for real-time prices. Real-time data requires a **TaFeed commercial license**.

**Possible free endpoints** (delayed data, hypothetical):
```
https://www.saudiexchange.sa/api/v1/index/tasi
https://www.saudiexchange.sa/api/v1/stock/2222 (Saudi Aramco)
```

These endpoints are speculative and may not exist or may be WAF-protected.

## Integration Notes

- **No free real-time data**: Tadawul requires a commercial license for real-time market data. This violates the "open" criterion for this repo.
- **Delayed data is low-value**: 15-minute delayed stock prices are not "real-time" by this repo's standards (sub-minute / streaming target).
- **Alternative: IEX Cloud** — For **US stocks**, IEX offers a free real-time API. This is already available globally and would be a better target than Tadawul delayed data.
- **Indices may be free**: Tadawul may publish **TASI index values** in real-time for free (indices are less sensitive than individual stock prices). However, this was not confirmed.

**Unique value if free real-time existed**:
- **Saudi Aramco** — World's most valuable company, oil price proxy
- **Petrochemical sector** — SABIC and others (global petrochemical markets)
- **Islamic finance** — Tadawul is a major market for Sharia-compliant equities and sukuk

However, **free real-time data is extremely unlikely** for any major exchange (universal commercial practice).

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time trades are sub-second (if accessible) |
| Openness | 0 | Real-time data requires paid commercial license |
| Stability | 3 | Tadawul is a formal exchange, highly reliable infrastructure |
| Structure | 2 | FIX protocol or JSON (commercial feeds) |
| Identifiers | 3 | Stock tickers (e.g., 2222 for Aramco) are globally stable |
| Additive value | 1 | Delayed data is low-value; real-time is commercially gated |

**Total: 12/18** (if free real-time existed)  
**Actual: 8/18** (penalized for commercial barrier)

**Verdict**: ❌ **Skip** — Tadawul real-time market data requires a **paid commercial license** (TaFeed), which violates this repo's "open" requirement. Delayed data (15-minute) is **not real-time** and adds minimal value.

**Alternative approaches**:
- **IEX Cloud** (USA) — Free real-time US stock data (already available globally, better target than Tadawul delayed)
- **Alpha Vantage** — Free tier for global stock APIs (includes Saudi stocks via delayed data)
- **TASI index** — If Tadawul publishes the **index value** (single number) in real-time for free, this might be worth a lightweight scraper. However, this is far lower value than individual stock data.

Do not build a Tadawul bridge unless:
1. Tadawul launches a **free real-time API** (extremely unlikely)
2. Or, Tadawul publishes **TASI index values** in real-time for free (plausible, but still low-value)

For **financial market data**, focus on **IEX Cloud** (USA) or **cryptocurrency exchanges** (Binance, Coinbase have free WebSocket APIs) instead of commercial stock exchanges.
