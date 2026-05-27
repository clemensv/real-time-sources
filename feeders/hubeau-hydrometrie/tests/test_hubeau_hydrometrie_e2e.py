"""End-to-end tests for Hub'Eau Hydrométrie against real API."""

import pytest
from hubeau_hydrometrie.hubeau_hydrometrie import HubEauHydrometrieAPI


@pytest.mark.e2e
class TestHubEauRealEndpoints:
    def test_fetch_real_stations_list(self):
        api = HubEauHydrometrieAPI()
        # Fetch just first page
        import requests
        response = requests.get(
            api.STATIONS_URL,
            params={"format": "json", "size": 10, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        stations = data.get("data", [])
        assert len(stations) > 0
        assert data.get("count", 0) > 1000

    def test_station_has_required_fields(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.STATIONS_URL,
            params={"format": "json", "size": 5, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        stations = response.json().get("data", [])
        for s in stations:
            assert "code_station" in s
            assert "libelle_station" in s

    def test_station_coordinates(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.STATIONS_URL,
            params={"format": "json", "size": 20, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        stations = response.json().get("data", [])
        with_coords = [s for s in stations if s.get("longitude_station") and s.get("latitude_station")]
        assert len(with_coords) > 0

    def test_fetch_observations(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.OBSERVATIONS_URL,
            params={"format": "json", "size": 10},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        observations = data.get("data", [])
        assert len(observations) > 0

    def test_observation_has_required_fields(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.OBSERVATIONS_URL,
            params={"format": "json", "size": 5},
            timeout=30
        )
        response.raise_for_status()
        observations = response.json().get("data", [])
        for o in observations:
            assert "code_station" in o
            assert "date_obs" in o
            assert "resultat_obs" in o
            assert "grandeur_hydro" in o

    def test_observation_grandeur_values(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.OBSERVATIONS_URL,
            params={"format": "json", "size": 50},
            timeout=30
        )
        response.raise_for_status()
        observations = response.json().get("data", [])
        grandeurs = set(o.get("grandeur_hydro") for o in observations)
        # Should have at least H (height) or Q (discharge)
        assert len(grandeurs.intersection({"H", "Q"})) > 0

    def test_station_river_info(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.STATIONS_URL,
            params={"format": "json", "size": 50, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        stations = response.json().get("data", [])
        with_river = [s for s in stations if s.get("libelle_cours_eau")]
        assert len(with_river) > 0

    def test_api_response_time(self):
        import time
        api = HubEauHydrometrieAPI()
        import requests
        start = time.time()
        response = requests.get(
            api.STATIONS_URL,
            params={"format": "json", "size": 10, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        elapsed = time.time() - start
        assert elapsed < 15.0

    def test_pagination_has_count(self):
        api = HubEauHydrometrieAPI()
        import requests
        response = requests.get(
            api.STATIONS_URL,
            params={"format": "json", "size": 2, "page": 1},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        assert "count" in data
        assert data["count"] > 0
        assert "next" in data
