# Turkey DSI — State Hydraulic Works Dam Levels

**Country/Region**: Turkey (~860 dams, 700+ operational)
**Publisher**: DSİ (Devlet Su İşleri Genel Müdürlüğü — State Hydraulic Works General Directorate)
**API Endpoint**: `https://www.dsi.gov.tr/` (web portal)
**Documentation**: https://www.dsi.gov.tr/ (Turkish, some English content)
**Protocol**: Web portal; no documented public REST API
**Auth**: None for public bulletin access
**Data Format**: HTML, PDF reports
**Update Frequency**: Daily dam storage bulletins
**License**: Turkish government data

## What It Provides

DSİ is responsible for the planning, construction, and operation of all major water infrastructure in Turkey, monitoring:

- **Dam storage levels** and **percentage capacity** for all operational dams
- **Reservoir inflow and outflow** data
- **Irrigation** water allocation and delivery
- **Hydroelectric generation** data
- **Flood control** operations

Turkey has the second-highest number of dams under construction in the world and ~860 operational dams. The massive GAP (Southeastern Anatolia Project) includes Atatürk Dam — one of the world's largest, critical for the Euphrates-Tigris water system that spans Turkey, Syria, and Iraq.

Major dam complexes: Atatürk (8,900 MW hydropower), Keban, Karakaya (Euphrates cascade), Ilısu (Tigris), and Istanbul's water supply dams (Ömerli, Terkos, Büyükçekmece).

## API Details

No documented public REST API. DSİ publishes information through:

- **Daily dam storage bulletins**: available on the DSİ website
- **Annual statistical yearbooks**: comprehensive dam-by-dam data
- **Regional offices**: 26 DSİ regional directorates manage local dam operations
- **Turkish Statistical Institute (TÜİK)**: aggregated dam statistics

The web portal is primarily in Turkish. Some English pages exist under international cooperation sections.

## Freshness Assessment

Moderate. Daily storage bulletins provide timely data by reservoir monitoring standards. The underlying telemetry is real-time for flood management, but public access is limited to daily or weekly summaries.

## Entity Model

- **Dam**: name, river basin, province, DSİ regional directorate, dam type, height, reservoir volume
- **Storage Report**: date, current volume (hm³), percentage full, inflow, outflow
- **River Basin**: name (Fırat/Euphrates, Dicle/Tigris, Kızılırmak, etc.), total dams
- **Regional Directorate**: DSİ region code, provinces covered

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily bulletins; real-time telemetry not publicly exposed |
| Openness | 1 | Public bulletins but no API; Turkish language primarily |
| Stability | 2 | Major government agency but web infrastructure varies |
| Structure | 0 | No programmatic access; PDF/HTML only |
| Identifiers | 1 | Dam names; no standardized public codes |
| Additive Value | 3 | Euphrates-Tigris geopolitics; GAP project; 2nd most dams under construction globally |
| **Total** | **9/18** | |

## Notes

- Turkey's dam infrastructure is geopolitically significant — the Euphrates-Tigris water system affects Syria and Iraq. Dam level data has diplomatic sensitivity.
- Istanbul's water supply depends on a ring of reservoirs — during droughts, Istanbul dam levels make international news.
- The lack of public API access is the major barrier. Data exists and is collected in real-time but is shared publicly only through web portal summaries.
- Academic researchers sometimes obtain DSİ data through formal requests — a path for bulk historical data.
- Turkey's hydroelectric capacity (~31 GW installed) makes it a top-10 global hydropower producer.
- For integration purposes, the daily bulletin scraping approach is the most realistic path, but fragile.
