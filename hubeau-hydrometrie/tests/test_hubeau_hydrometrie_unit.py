"""Unit tests for Hub'Eau Hydrométrie data poller - no external dependencies."""

import pytest
from hubeau_hydrometrie.hubeau_hydrometrie import HubEauHydrometrieAPI


@pytest.mark.unit
class TestHubEauAPIInitialization:
    def test_init_creates_session(self):
        api = HubEauHydrometrieAPI()
        assert api.session is not None

    def test_base_url_uses_https(self):
        assert HubEauHydrometrieAPI.BASE_URL.startswith("https://")

    def test_poll_interval_default(self):
        assert HubEauHydrometrieAPI.POLL_INTERVAL_SECONDS == 300

    def test_api_has_required_methods(self):
        api = HubEauHydrometrieAPI()
        assert hasattr(api, 'list_stations')
        assert hasattr(api, 'get_latest_observations')
        assert hasattr(api, 'parse_connection_string')
        assert hasattr(api, 'feed_stations')


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_parse_event_hubs_connection_string(self):
        api = HubEauHydrometrieAPI()
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123==;EntityPath=myeventhub"
        result = api.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myeventhub'
        assert result['sasl.username'] == '$ConnectionString'

    def test_parse_connection_string_extracts_endpoint(self):
        api = HubEauHydrometrieAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = api.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'

    def test_parse_connection_string_extracts_entity_path(self):
        api = HubEauHydrometrieAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=mytopic"
        result = api.parse_connection_string(cs)
        assert result['kafka_topic'] == 'mytopic'

    def test_parse_connection_string_sets_sasl(self):
        api = HubEauHydrometrieAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = api.parse_connection_string(cs)
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == cs.strip()

    def test_parse_connection_string_with_whitespace(self):
        api = HubEauHydrometrieAPI()
        cs = "  Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic  "
        result = api.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'

    def test_parse_connection_string_invalid_raises_error(self):
        api = HubEauHydrometrieAPI()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("EndpointWithoutEquals;EntityPathInvalid")


@pytest.mark.unit
class TestDataClasses:
    def test_station_creation(self):
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.station import Station
        s = Station(
            code_station="A694102004",
            libelle_station="Test Station",
            code_site="A6941020",
            longitude_station=6.18,
            latitude_station=48.71,
            libelle_cours_eau="Moselle",
            libelle_commune="PONT-A-MOUSSON",
            code_departement="54",
            en_service=True,
            date_ouverture_station="2012-11-11T00:00:00Z"
        )
        assert s.code_station == "A694102004"
        assert s.en_service is True

    def test_station_json_roundtrip(self):
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.station import Station
        s = Station(
            code_station="TEST01", libelle_station="Test", code_site="SITE01",
            longitude_station=2.0, latitude_station=48.0, libelle_cours_eau="Seine",
            libelle_commune="Paris", code_departement="75", en_service=True,
            date_ouverture_station="2020-01-01"
        )
        json_str = s.to_json()
        s2 = Station.from_data(json_str)
        assert s2.code_station == "TEST01"

    def test_observation_creation(self):
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.observation import Observation
        o = Observation(
            code_station="A694102004",
            date_obs="2024-06-15T12:00:00Z",
            resultat_obs=1203.0,
            grandeur_hydro="H",
            libelle_methode_obs="Mesurée",
            libelle_qualification_obs="Non qualifiée"
        )
        assert o.resultat_obs == 1203.0
        assert o.grandeur_hydro == "H"

    def test_observation_json_roundtrip(self):
        from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.observation import Observation
        o = Observation(
            code_station="TEST01", date_obs="2024-01-01T00:00:00Z",
            resultat_obs=500.0, grandeur_hydro="Q",
            libelle_methode_obs="Calculée", libelle_qualification_obs="Non qualifiée"
        )
        json_str = o.to_json()
        o2 = Observation.from_data(json_str)
        assert o2.resultat_obs == 500.0
