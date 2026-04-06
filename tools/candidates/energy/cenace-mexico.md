# CENACE — Centro Nacional de Control de Energía (Mexico)

**Country/Region**: Mexico
**Publisher**: CENACE (National Energy Control Center)
**API Endpoint**: `https://www.cenace.gob.mx/SIM/` (SIM portal)
**Documentation**: https://www.cenace.gob.mx/Paginas/SIM/Reportes.aspx
**Protocol**: Web portal with file downloads
**Auth**: None for public data
**Data Format**: CSV, Excel (via web portal); some SOAP/XML services
**Update Frequency**: Hourly (generation), daily (prices), real-time (portal display)
**License**: Mexican government public data

## What It Provides

CENACE operates Mexico's wholesale electricity market (MEM) and manages the National Interconnected System (SIN). Mexico has two synchronous areas: the bulk SIN covering most of the country, and the BCS (Baja California Sur) isolated system.

Available data via SIM (Sistema de Información del Mercado):

- **Generation**: By technology type (thermal, hydro, wind, solar, nuclear, geothermal, biomass)
- **Demand**: Real-time and forecasted demand by control area
- **Prices**: Locational Marginal Prices (PML) by node — Mexico uses nodal pricing similar to US ISOs
- **Interchange**: Cross-border flows with US (Texas via ERCOT DC ties, California) and Guatemala/Belize
- **Curtailment**: Renewable generation curtailment events
- **Transmission**: Congestion data and planned outages

## API Details

CENACE's data is primarily available through their SIM web portal, which serves reports as downloadable files. The portal at cenace.gob.mx uses ASP.NET WebForms:

```
GET https://www.cenace.gob.mx/SIM/VISTA/REPORTES/EnergiaGenLiq662702.aspx
→ HTML page with navigation links to documents and reports
```

No REST API was identified during testing. Data access patterns:

1. **SIM Portal**: Browse and download CSV/Excel reports
2. **SOAP Services**: Some older data feeds available via SOAP/XML (undocumented)
3. **Open Data**: Mexico's datos.gob.mx portal may have CENACE datasets
4. **API Mexico**: The government open data API (api.datos.gob.mx) may provide some energy datasets

## Freshness Assessment

The web portal displays near-real-time data, but downloadable files have delays of hours to a day. Day-ahead prices are published after market clearing. Real-time prices have ~1-hour lag. Generation data is available with variable delay.

## Entity Model

- **Control Area**: SIN (national interconnected), BCS (Baja California Sur), BCA (Baja California — connected to WECC)
- **Node**: ~2,000+ pricing nodes across Mexico
- **Technology**: Termoeléctrica, Hidroeléctrica, Eoloeléctrica, Fotovoltaica, Nucleoeléctrica, Geotermoeléctrica
- **Price**: PML in MXN/MWh (Mexican pesos per MWh)
- **Time**: Mexico City time (UTC-6/UTC-5 DST), Baja California time varies

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time on portal, hourly in downloadable files |
| Openness | 2 | Public data but no documented API; portal-based access only |
| Stability | 2 | Government entity, but web portal format changes periodically |
| Structure | 1 | ASP.NET WebForms portal, file downloads (CSV/Excel), no REST API |
| Identifiers | 2 | Standard node codes, technology type names (Spanish) |
| Additive Value | 3 | Only source for Mexico's grid — Latin America's 2nd largest economy |
| **Total** | **12/18** | |

## Notes

- Mexico's grid is interconnected with the US (ERCOT via DC ties, WECC via Baja California), making it relevant for North American grid analysis.
- Mexico has significant geothermal capacity (Cerro Prieto in Baja California is one of the world's largest geothermal plants) and rapidly growing wind/solar.
- The nuclear plant at Laguna Verde (1,400 MW) is Mexico's only nuclear facility.
- CENACE data is available in Spanish — field names and documentation are in Spanish.
- The lack of a REST API is the main barrier. A scraper for the SIM portal or the SOAP services would be needed.
- Consider Mexico's Open Data initiative (datos.gob.mx) as an alternative access path.
