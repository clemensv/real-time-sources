# German State Environment Agencies — Water Quality Monitoring (LANUV, LfU, etc.)

**Country/Region**: Germany (federated — each state operates independently)
**Publisher**: Various Landesumweltämter (State Environment Agencies), coordinated by UBA (Federal Environment Agency)
**API Endpoint**: Various per state (see details below)
**Documentation**: Varies by state; https://www.umweltbundesamt.de/ (federal UBA)
**Protocol**: Web portals; some provide WMS/WFS OGC services
**Auth**: Generally none for public data
**Data Format**: HTML, CSV, XML; some GeoJSON via WFS
**Update Frequency**: Mix of real-time continuous monitoring and periodic discrete sampling
**License**: German open data laws (varies by state; generally open)

## What It Provides

Germany's water quality monitoring is a federated system where each of the 16 states (Bundesländer) operates its own monitoring network. The federal UBA coordinates reporting to the EU under the Water Framework Directive.

Key state agencies and portals:
- **NRW (North Rhine-Westphalia)**: LANUV — `https://www.elwasweb.nrw.de/` — comprehensive water data portal
- **Bavaria**: LfU Bayern — `https://www.gkd.bayern.de/` — real-time continuous monitoring
- **Baden-Württemberg**: LUBW — `https://udo.lubw.baden-wuerttemberg.de/` — environmental data portal
- **Lower Saxony**: NLWKN — `https://www.wasserdaten.niedersachsen.de/`
- **Hesse**: HLNUG — `https://www.hlnug.de/`
- **Saxony**: LfULG — various portals

Parameters monitored:
- Continuous: temperature, pH, dissolved oxygen, conductivity, turbidity, nitrate (at select stations)
- Discrete: full chemical analysis (nutrients, metals, pesticides, industrial chemicals, pharmaceuticals)
- Biological: macroinvertebrates, fish, macrophytes, diatoms (WFD assessments)

Bavaria's GKD (Gewässerkundlicher Dienst) system is notable for providing real-time continuous water quality data alongside flow and level data.

## API Details

**Bavaria GKD** (most promising):
- `https://www.gkd.bayern.de/de/fluesse/wasserqualitaet/` — real-time water quality
- Provides Kisters WISKI-based data services
- Real-time graphs and data for temperature, DO, conductivity, pH at continuous monitoring stations

**NRW ELWAS-WEB**:
- `https://www.elwasweb.nrw.de/elwas-web/` — map-based portal
- WFS/WMS services for geospatial data
- Monitoring data accessible through the portal

**Federal (UBA)**:
- Water quality reporting data aggregated from all states
- Available through UBA's data portal and feeds into EEA Waterbase

No standardized national API exists — each state operates independently.

## Freshness Assessment

Good to excellent for the real-time continuous monitoring stations (Bavaria GKD in particular). These provide 15-minute interval data for temperature, DO, conductivity, pH, and turbidity. Discrete sampling data has the usual lab analysis delay.

## Entity Model

- **State Agency**: name, state, web portal
- **Monitoring Station**: state code, name, water body, coordinates (ETRS89)
- **Measurement**: timestamp, parameter, value, unit, QC flag
- **WFD Water Body**: EU water body code, type, river basin district, ecological/chemical status

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time at some stations (Bavaria); mixed for discrete sampling |
| Openness | 2 | Generally open; fragmented access across 16 states |
| Stability | 3 | Government agencies with legal mandates |
| Structure | 1 | Fragmented across states; no unified API; some Kisters WISKI backends |
| Identifiers | 2 | State-specific station codes; WFD water body codes for cross-referencing |
| Additive Value | 2 | German rivers (Rhine, Elbe, Danube) are major European waterways |
| **Total** | **12/18** | |

## Notes

- The federated structure of German environmental monitoring makes this one of the harder targets to integrate. Each of 16 states has its own system, nomenclature, and access methods.
- Bavaria (GKD) is the most promising starting point — it has the most developed online data infrastructure with real-time continuous water quality.
- The Rhine and Elbe rivers have international monitoring programs (ICPR, ICPE) that may provide better-structured cross-border data.
- Many German state agencies use Kisters WISKI as their backend — if you can identify the WISKI API endpoints, you get standardized access across states.
- UBA's national reporting feeds into EEA Waterbase, so the pan-European route may be more practical for German data than trying to integrate 16 state systems.
- Pharmaceutical and microplastic monitoring is increasingly prominent in German water quality programs — a unique data dimension.
