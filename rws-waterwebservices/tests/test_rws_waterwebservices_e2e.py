"""End-to-end tests for RWS Waterwebservices bridge against the real API."""

import time
import pytest
import requests

RWS_BASE_URL = "https://ddapi20-waterwebservices.rijkswaterstaat.nl"
CATALOG_ENDPOINT = "/METADATASERVICES/OphalenCatalogus"
LATEST_ENDPOINT = "/ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen"
HEADERS = {"Content-Type": "application/json"}


class TestRWSRealEndpoints:
    """Tests against the real Rijkswaterstaat Waterwebservices API."""

    def test_fetch_catalog(self):
        """Verify catalog endpoint returns data."""
        payload = {
            "CatalogusFilter": {
                "Compartimenten": True,
                "Grootheden": True,
            },
        }
        r = requests.post(RWS_BASE_URL + CATALOG_ENDPOINT, json=payload, headers=HEADERS, timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert data.get("Succesvol") is True

    def test_catalog_has_locations(self):
        """Verify catalog returns locations when filtered."""
        payload = {
            "CatalogusFilter": {"Compartimenten": True, "Grootheden": True},
            "LocatieMetadataFilter": {
                "Compartiment": {"Code": "OW"},
                "Grootheid": {"Code": "WATHTE"},
            },
        }
        r = requests.post(RWS_BASE_URL + CATALOG_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        data = r.json()
        assert data.get("Succesvol") is True
        locs = data.get("LocatieLijst", [])
        assert len(locs) > 100

    def test_catalog_location_has_required_fields(self):
        """Verify catalog locations have Code, Naam, Lat, Lon."""
        payload = {
            "CatalogusFilter": {"Compartimenten": True, "Grootheden": True},
            "LocatieMetadataFilter": {
                "Compartiment": {"Code": "OW"},
                "Grootheid": {"Code": "WATHTE"},
            },
        }
        r = requests.post(RWS_BASE_URL + CATALOG_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        data = r.json()
        loc = data["LocatieLijst"][0]
        assert "Code" in loc
        assert "Naam" in loc
        assert "Lat" in loc
        assert "Lon" in loc

    def test_fetch_latest_water_levels(self):
        """Verify latest observations endpoint returns water level data."""
        payload = {
            "LocatieLijst": [{"Code": "hoekvanholland"}],
            "AquoPlusWaarnemingMetadataLijst": [
                {"aquoMetadata": {"Compartiment": {"Code": "OW"}, "Grootheid": {"Code": "WATHTE"}}}
            ],
        }
        r = requests.post(RWS_BASE_URL + LATEST_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        assert r.status_code == 200
        data = r.json()
        assert data.get("Succesvol") is True
        assert len(data.get("WaarnemingenLijst", [])) > 0

    def test_observation_has_required_fields(self):
        """Verify observation entries have required fields."""
        payload = {
            "LocatieLijst": [{"Code": "hoekvanholland"}],
            "AquoPlusWaarnemingMetadataLijst": [
                {"aquoMetadata": {"Compartiment": {"Code": "OW"}, "Grootheid": {"Code": "WATHTE"}}}
            ],
        }
        r = requests.post(RWS_BASE_URL + LATEST_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        data = r.json()
        entry = data["WaarnemingenLijst"][0]
        assert "Locatie" in entry
        assert "MetingenLijst" in entry
        assert "AquoMetadata" in entry
        loc = entry["Locatie"]
        assert "Code" in loc
        assert "Naam" in loc

    def test_observation_has_measurement_data(self):
        """Verify observations include actual measurement values."""
        payload = {
            "LocatieLijst": [{"Code": "hoekvanholland"}],
            "AquoPlusWaarnemingMetadataLijst": [
                {"aquoMetadata": {"Compartiment": {"Code": "OW"}, "Grootheid": {"Code": "WATHTE"}}}
            ],
        }
        r = requests.post(RWS_BASE_URL + LATEST_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        data = r.json()
        found_value = False
        for entry in data.get("WaarnemingenLijst", []):
            for meting in entry.get("MetingenLijst", []):
                if meting.get("Meetwaarde", {}).get("Waarde_Numeriek") is not None:
                    found_value = True
                    break
            if found_value:
                break
        assert found_value, "No observation with a numeric measurement value found"

    def test_catalog_has_wathte_metadata(self):
        """Verify catalog contains WATHTE/OW in the aquo metadata."""
        payload = {
            "CatalogusFilter": {"Compartimenten": True, "Grootheden": True},
            "LocatieMetadataFilter": {
                "Compartiment": {"Code": "OW"},
                "Grootheid": {"Code": "WATHTE"},
            },
        }
        r = requests.post(RWS_BASE_URL + CATALOG_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        data = r.json()
        found = False
        for m in data.get("AquoMetadataLijst", []):
            if m.get("Grootheid", {}).get("Code") == "WATHTE" and m.get("Compartiment", {}).get("Code") == "OW":
                found = True
                break
        assert found, "WATHTE/OW not found in catalog metadata"

    def test_api_response_time(self):
        """Verify the API responds within a reasonable time."""
        payload = {
            "LocatieLijst": [{"Code": "hoekvanholland"}, {"Code": "delfzijl"}],
            "AquoPlusWaarnemingMetadataLijst": [
                {"aquoMetadata": {"Compartiment": {"Code": "OW"}, "Grootheid": {"Code": "WATHTE"}}}
            ],
        }
        start = time.time()
        r = requests.post(RWS_BASE_URL + LATEST_ENDPOINT, json=payload, headers=HEADERS, timeout=60)
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 30, f"API took {elapsed:.1f}s, expected < 30s"

    def test_bridge_class_against_live_api(self):
        """Test the bridge class methods against the real API."""
        from rws_waterwebservices.rws_waterwebservices import RWSWaterwebservicesAPI
        api = RWSWaterwebservicesAPI()
        stations = api.get_water_level_stations()
        assert len(stations) > 100
        # Verify we can build Station objects
        loc = stations[0]
        from rws_waterwebservices.rws_waterwebservices_producer.nl.rws.waterwebservices.station import Station
        station = Station(
            code=loc.get("Code", ""),
            name=loc.get("Naam", ""),
            latitude=float(loc.get("Lat", 0) or 0),
            longitude=float(loc.get("Lon", 0) or 0),
            coordinate_system=loc.get("Coordinatenstelsel", ""),
        )
        assert station.code != ""
        assert station.name != ""
