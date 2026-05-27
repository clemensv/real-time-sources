"""Quick e2e probe of DWD modules against live data."""
from dwd.util.http_client import DWDHttpClient
from dwd.modules.station_metadata import StationMetadataModule
from dwd.modules.station_obs_10min import StationObs10MinModule
from dwd.modules.weather_alerts import WeatherAlertsModule

http = DWDHttpClient()

print("=== Station Metadata ===")
mod = StationMetadataModule(http)
state = {}
events = mod.poll(state)
print(f"Stations: {len(events)}")
for e in events[:3]:
    d = e["data"]
    print(f"  {d['station_id']:>5s} | {d['station_name']:<30s} | {d['state']:<20s} | {d['latitude']:.4f}, {d['longitude']:.4f}")
states = set(e["data"]["state"] for e in events if e["data"]["state"])
print(f"Unique states ({len(states)}): {sorted(states)[:5]}...")

print()
print("=== 10-Min Observations (air_temperature only) ===")
mod10 = StationObs10MinModule(http, categories=["air_temperature"])
state10 = {}
events10 = mod10.poll(state10)
print(f"New observations: {len(events10)}")
if events10:
    d = events10[0]["data"]
    print(f"  Sample: station={d['station_id']}, ts={d['timestamp']}, temp={d.get('air_temperature_2m')}")
    d = events10[-1]["data"]
    print(f"  Last:   station={d['station_id']}, ts={d['timestamp']}, temp={d.get('air_temperature_2m')}")

print()
print("=== Weather Alerts ===")
mod_alert = WeatherAlertsModule(http)
state_alert = {}
events_alert = mod_alert.poll(state_alert)
print(f"Alerts: {len(events_alert)}")
if events_alert:
    a = events_alert[0]["data"]
    print(f"  Sample: {a['event']} - {a['headline'][:80]}")
