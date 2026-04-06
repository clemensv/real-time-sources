# Reservoir / Dam Storage — Candidate Data Sources

Research candidates for real-time reservoir and dam storage monitoring APIs.

**Already covered in repo**: None directly (USGS IV covers some reservoir levels via gage height parameter)

## Candidates

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [cdec-california](cdec-california.md) | California CDEC | USA — California | **18/18** | Perfect score: clean JSON API, real-time hourly, no auth |
| [usbr-hydrodata](usbr-hydrodata.md) | US Bureau of Reclamation HydroData | USA — Western states | **15/18** | Powell, Mead, and major federal reservoirs; JSON/CSV |
| [spain-saih](spain-saih.md) | Spanish SAIH | Spain (~1,200 dams) | **14/18** | Highest dam density in Europe; real-time at basin level |
| [bom-water-storage](bom-water-storage.md) | BOM Water Storage Dashboard | Australia | **13/18** | National coverage; beautiful dashboard; API undocumented |
| [brazil-ana-sar](brazil-ana-sar.md) | Brazil ANA SAR | Brazil | **13/18** | 3rd-largest hydroelectric system globally; mostly web portal |

## Recommendation

**Top pick**: California CDEC (18/18) — verified working JSON API with real-time hourly reservoir storage data. Multi-station queries supported. No authentication. This is a model for what reservoir data APIs should look like.

**Strong second**: USBR HydroData (15/18) — covers the big federal reservoirs (Lake Powell, Lake Mead) that dominate US western water policy. Structured JSON/CSV access but no formal API spec.

**Natural pairing**: CDEC + USBR together cover essentially all major western US reservoir infrastructure with complementary scope (state vs. federal).

**International**: Spain (SAIH) has the richest dataset by station count but fragmented across basin authorities. Brazil (ANA) covers a globally significant hydroelectric system but with poor API access.
