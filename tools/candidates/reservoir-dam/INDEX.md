# Reservoir / Dam Storage — Candidate Data Sources

Research candidates for real-time reservoir and dam storage monitoring APIs.

**Already covered in repo**: None directly (USGS IV covers some reservoir levels via gage height parameter)

## Candidates

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [cdec-california](cdec-california.md) | California CDEC | USA — California | **18/18** | Perfect score: clean JSON API, real-time hourly, no auth |
| [usbr-hydrodata](usbr-hydrodata.md) | US Bureau of Reclamation HydroData | USA — Western states | **15/18** | Powell, Mead, and major federal reservoirs; JSON/CSV |
| [spain-saih](spain-saih.md) | Spanish SAIH | Spain (~1,200 dams) | **14/18** | Highest dam density in Europe; real-time at basin level |
| [japan-mlit-dams](japan-mlit-dams.md) | Japan MLIT River Bureau | Japan (~550 major dams) | **13/18** | 10-min real-time telemetry; flood ops; no public REST API |
| [bom-water-storage](bom-water-storage.md) | BOM Water Storage Dashboard | Australia | **13/18** | National coverage; beautiful dashboard; API undocumented |
| [brazil-ana-sar](brazil-ana-sar.md) | Brazil ANA SAR | Brazil | **13/18** | 3rd-largest hydroelectric system globally; mostly web portal |
| [portugal-snirh](portugal-snirh.md) | Portugal SNIRH | Portugal (~60 major dams) | **11/18** | Alqueva (largest EU artificial lake); complements Spain SAIH |
| [india-cwc](india-cwc.md) | India CWC Reservoir Bulletin | India (130+ reservoirs) | **10/18** | 3rd largest dam inventory globally; monsoon-critical |
| [south-africa-dws](south-africa-dws.md) | South Africa DWS Dam Levels | South Africa (~250 dams) | **10/18** | Water-scarce nation; "Day Zero" context; critical indicator |
| [turkey-dsi](turkey-dsi.md) | Turkey DSI State Hydraulic Works | Turkey (~860 dams) | **9/18** | Euphrates-Tigris geopolitics; GAP project; no API |

## Recommendation

**Top pick**: California CDEC (18/18) — verified working JSON API with real-time hourly reservoir storage data. Multi-station queries supported. No authentication. This is a model for what reservoir data APIs should look like.

**Strong second**: USBR HydroData (15/18) — covers the big federal reservoirs (Lake Powell, Lake Mead) that dominate US western water policy. Structured JSON/CSV access but no formal API spec.

**Natural pairing**: CDEC + USBR together cover essentially all major western US reservoir infrastructure with complementary scope (state vs. federal).

**International — API accessible**: Spain (SAIH, 14/18) has the richest dataset by station count but fragmented across basin authorities. Portugal (SNIRH, 11/18) complements SAIH for complete Iberian coverage, and the Albufeira Convention requires transboundary monitoring.

**International — data-rich but API-poor**: Japan (13/18) has world-class 10-minute telemetry but no public API. India (10/18), South Africa (10/18), and Turkey (9/18) all monitor critical infrastructure but expose data only through web portals and bulletins. These represent the biggest gap between data importance and data accessibility in the reservoir domain.

**Geopolitical significance**: Turkey's DSI data is diplomatically sensitive — Euphrates-Tigris dam operations directly affect Syria and Iraq. India's CWC bulletin moves agricultural markets during monsoon season. South Africa's dam levels made global headlines during Cape Town's "Day Zero" crisis.
