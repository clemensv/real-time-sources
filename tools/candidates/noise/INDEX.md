# Noise Monitoring — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [nyc-311-noise](nyc-311-noise.md) | NYC 311 Noise Complaints | New York City | REST/JSON (Socrata) | None | 18/18 |
| [dublin-noise](dublin-noise.md) | Dublin City Noise (Sonitus) | Ireland | REST/JSON | API Key | 14/18 |
| [bruitparif](bruitparif.md) | Bruitparif RUMEUR Network | Paris/Île-de-France | Web SPA | None | 13/18 |
| [schiphol-noise](schiphol-noise.md) | Schiphol Airport Noise (NOMOS) | Netherlands | Web/CSV | None | 12/18 |

## Summary
Four candidates covering urban noise complaints (NYC 311), environmental sensor monitoring (Dublin/Sonitus, Paris/Bruitparif), and airport noise (Schiphol/NOMOS). NYC 311 is a breakthrough addition scoring a perfect 18/18 — a production-grade Socrata API delivering near real-time noise complaint data with full geolocation, status tracking, and 15+ years of history across all five boroughs. Bruitparif operates one of the world's densest urban noise monitoring networks (~170 stations) but locks data behind a JavaScript SPA. The noise domain shows a clear split: complaint data (NYC) has excellent API access, while sensor data (Bruitparif, Schiphol) remains trapped in web portals.
