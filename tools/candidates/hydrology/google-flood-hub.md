# Google Flood Hub

**Country/Region**: Global (80+ countries)
**Publisher**: Google Research
**API Endpoint**: `https://sites.research.google/floods/` (web application only)
**Documentation**: https://sites.research.google/floods/about
**Protocol**: Web application (no public API)
**Auth**: N/A
**Data Format**: Web/visual only
**Update Frequency**: Real-time (river forecasts updated continuously)
**Station Count**: Coverage in 80+ countries, thousands of river reaches
**License**: Proprietary (Google Terms of Service)

## What It Provides

Google Flood Hub provides AI-powered flood forecasting:
- **7-day river flood forecasts** for 80+ countries
- **Flood inundation maps** showing predicted flood extent
- **Streamflow forecasts** at specific river locations
- **Alert levels** (no flood, advisory, watch, warning)
- Coverage includes India, Bangladesh, Brazil, and parts of Africa, SE Asia, South America, Europe

The system uses Google's machine learning models trained on historical data, weather forecasts, and satellite imagery.

## API Details

### Web application
```
GET https://sites.research.google/floods/l/{lat}/{lon}/{zoom}
```
Returns a web application with interactive flood map. The response is minimal HTML with JavaScript that loads the actual application.

### No public API
- No public REST API, data download, or machine-readable feed was discovered
- The web application loads data via internal Google APIs that are not documented or publicly accessible
- `https://floodhub.google.com/` — DNS failure (may have been migrated)
- Internal API calls use Google-proprietary authentication and protobuf formats

### Data disclaimer
The web application states: "Flood conditions are approximate and are for informational purposes only. Check official sources for more information."

## Freshness Assessment

- Web application shows real-time forecasts
- Data is updated continuously as weather models update
- Forecasts extend 7 days ahead
- Active development by Google Research team

## Entity Model

- **River reach**: geographic segment with lat/lon bounds
- **Forecast**: timestamp, predicted water level, alert level, probability
- **Inundation map**: predicted flood extent as raster overlay
- **Alert levels**: No flood, Advisory, Watch, Warning

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | No public API; web-only access |
| Data Richness | 3 | AI-powered forecasts, inundation maps, 7-day outlook |
| Freshness | 3 | Continuously updated forecasts |
| Station Coverage | 3 | 80+ countries, global scope |
| Documentation | 1 | About page only; no technical/API documentation |
| License/Access | 0 | Proprietary; no data access for integration |
| **Total** | **10/18** | |

## Notes

- Google Flood Hub is impressive in scope and capability but entirely closed for programmatic access
- The AI-based approach (trained on gauge data, satellite imagery, weather forecasts) is fundamentally different from traditional gauge-based monitoring
- Google has published research papers on the underlying models but not the data or APIs
- For integration purposes, this is a dead end — no way to access data programmatically
- May serve as a complementary visual tool rather than a data source
- The "informational purposes only" disclaimer limits official use
- Worth monitoring — Google may eventually provide API access or partner with existing platforms
