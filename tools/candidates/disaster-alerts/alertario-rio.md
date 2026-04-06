# AlertaRio — Rio de Janeiro Flood/Weather Monitoring

**Country/Region**: Brazil (Rio de Janeiro municipality)
**Publisher**: Prefeitura do Rio de Janeiro / GEO-RIO
**API Endpoint**: `https://alertario.rio.rj.gov.br/` (connection failed), `https://api.alertario.rio.rj.gov.br/` (connection failed)
**Documentation**: https://alertario.rio.rj.gov.br/
**Protocol**: REST / WebSocket (known to exist)
**Auth**: Unknown
**Data Format**: JSON (known)
**Update Frequency**: Real-time (rain gauges every 15 minutes)
**License**: Rio de Janeiro municipal government

## What It Provides

AlertaRio is Rio de Janeiro's integrated weather and flood early warning system — one of the most advanced urban disaster monitoring systems in Latin America. Rio's geography creates extreme flood and landslide risk:

- **Steep terrain**: Morros (hills) rising 500-1,000m within the city, often with favela settlements
- **Intense tropical rainfall**: Convective storms can deliver 50+ mm/hour
- **Flash floods**: Narrow valleys and streams flood rapidly
- **Landslides**: Saturated steep slopes collapse — the 2011 Região Serrana disaster killed 900+ people

System components:
- **33 rain gauge stations** distributed across the city
- **Weather radar** (Sumaré radar)
- **Lightning detection**
- **River/stream level sensors**
- **Automated sirens** in high-risk communities
- **Landslide risk assessment** models

### Alert Levels
- **Estágio 1 (Vigilância)**: Weather watch
- **Estágio 2 (Atenção)**: Weather warning
- **Estágio 3 (Alerta Máximo)**: Maximum alert; evacuations
- **Estágio 4 (Crise)**: Crisis; active emergency

## API Details

All endpoints were unreachable during testing:
```
https://alertario.rio.rj.gov.br/ → Connection failed
https://api.alertario.rio.rj.gov.br/v1/estacoes → Connection failed
https://websocket.alertario.rio.rj.gov.br/ → Connection failed
https://alertario.rio.rj.gov.br/upload/Geo/kml.json → Connection failed
```

AlertaRio is known to have:
- A REST API for station data
- WebSocket for real-time updates
- KML/GeoJSON exports for geographic data
- The `websocket.alertario.rio.rj.gov.br` subdomain confirms WebSocket push capability

## Integration Notes

- The WebSocket endpoint is particularly interesting — genuine push notifications for weather alerts
- Rio's 2016 Olympics infrastructure investment improved the monitoring system significantly
- The alert level system (Estágio 1-4) maps naturally to CloudEvents severity levels
- Flash flood warnings in favela communities are life-safety critical
- Rain accumulation data is scientifically valuable (extreme precipitation events)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 15-minute rain gauge intervals; WebSocket push |
| Openness | 1 | Known API exists but unreachable |
| Stability | 2 | Municipal government; Olympics-era investment |
| Structure | 2 | JSON + WebSocket; KML/GeoJSON exports |
| Identifiers | 2 | Station codes; alert levels are structured |
| Additive Value | 3 | Life-safety flash flood warnings; unique urban monitoring |
| **Total** | **12/18** | |

## Verdict

⚠️ **Maybe** — Known API with WebSocket push capability, but all endpoints unreachable during testing. The WebSocket endpoint makes this unusually valuable (genuine push, not polling). Rio's flash flood monitoring is life-safety critical. High-priority revisit target.
