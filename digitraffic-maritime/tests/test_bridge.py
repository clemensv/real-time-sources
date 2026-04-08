"""Tests for the Digitraffic Maritime bridge logic."""

import json
from unittest.mock import MagicMock
import pytest

from digitraffic_maritime.bridge import (
    _emit_event, parse_connection_string,
    _MESSAGE_MAP, DigitraficBridge, DigitrafficPortCallPoller,
)


SAMPLE_PORT_CALLS_RESPONSE = {
    "dataUpdatedTime": "2026-04-08T07:31:42Z",
    "portCalls": [
        {
            "portCallId": 3352890,
            "portCallTimestamp": "2026-04-08T07:31:42Z",
            "customsReference": "0/750108",
            "portToVisit": "FIKTK",
            "prevPort": "DEHAM",
            "nextPort": "FIHEL",
            "domesticTrafficArrival": False,
            "domesticTrafficDeparture": False,
            "arrivalWithCargo": True,
            "notLoading": False,
            "discharge": 2,
            "vesselName": "Anina",
            "vesselNamePrefix": " ",
            "radioCallSign": "CQYU",
            "imoLloyds": 9354351,
            "mmsi": 235011250,
            "nationality": "PT",
            "vesselTypeCode": 50,
            "currentSecurityLevel": 1,
            "agentInfo": [
                {
                    "name": "C & C Port Agency Finland Oy Ltd, Helsinki",
                    "portCallDirection": "Arrival or whole PortCall",
                    "role": 1,
                },
                {
                    "name": "Orient Overseas Container Line Ltd.",
                    "portCallDirection": "Arrival or whole PortCall",
                    "role": 2,
                },
            ],
            "portAreaDetails": [
                {
                    "arrivalDraught": 0.0,
                    "ata": None,
                    "ataSource": None,
                    "atd": None,
                    "atdSource": None,
                    "berthCode": None,
                    "berthName": None,
                    "departureDraught": 0.0,
                    "eta": "2026-04-11T09:00:00Z",
                    "etaSource": "Agent",
                    "etd": "2026-04-12T09:00:00Z",
                    "etdSource": "Agent",
                    "portAreaCode": None,
                    "portAreaName": None,
                }
            ],
        }
    ],
}

SAMPLE_VESSEL_DETAILS_RESPONSE = [
    {
        "vesselId": 99991900,
        "mmsi": 210173000,
        "name": "Hav Sand",
        "namePrefix": "ms",
        "imoLloyds": 9505326,
        "radioCallSign": "OZ2229",
        "radioCallSignType": "REAL",
        "updateTimestamp": "2026-04-08T06:52:15Z",
        "dataSource": "Portnet",
        "vesselConstruction": {
            "vesselTypeCode": 70,
            "vesselTypeName": "Dry cargo vessel",
            "iceClassCode": "IA",
            "iceClassIssueDate": "2026-04-06T21:00:00Z",
            "iceClassIssuePlace": "Rotterdam",
            "iceClassEndDate": "2030-04-07T21:00:00Z",
            "doubleBottom": False,
            "inertGasSystem": False,
            "ballastTank": False,
        },
        "vesselDimensions": {
            "tonnageCertificateIssuer": "Hamburg",
            "dateOfIssue": "2011-01-25T22:00:00Z",
            "grossTonnage": 2415,
            "netTonnage": 1361,
            "deathWeight": 3175,
            "length": 82.42,
            "overallLength": 86.01,
            "height": 0.0,
            "breadth": 12.4,
            "draught": 5.3,
            "maxSpeed": None,
            "enginePower": "1980",
        },
        "vesselRegistration": {
            "nationality": "FO",
            "portOfRegistry": "Runavik",
        },
        "vesselSystem": {
            "shipOwner": " ",
            "shipTelephone1": " ",
            "shipEmail": " ",
            "shipVerifier": "LIVI",
        },
    }
]

SAMPLE_PORTS_RESPONSE = {
    "dataUpdatedTime": "2022-08-12T09:31:21.299259Z",
    "ssnLocations": {
        "features": [
            {
                "locode": "DEHEI",
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [8.7, 49.41667],
                },
                "properties": {
                    "locode": "DEHEI",
                    "locationName": "Heidelberg",
                    "country": "Germany",
                },
            }
        ]
    },
    "portAreas": {
        "features": [
            {
                "locode": "DEHEI",
                "type": "Feature",
                "geometry": None,
                "properties": {
                    "locode": "DEHEI",
                    "portAreaName": "Ei tiedossa",
                },
                "portAreaCode": "MUU",
            }
        ]
    },
    "berths": {
        "berths": [
            {
                "locode": "DEHEI",
                "portAreaCode": "MUU",
                "berthCode": "unknow",
                "berthName": "Ei tiedossa",
            }
        ]
    },
}


class TestParseConnectionString:
    def test_event_hubs_style(self):
        cs = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=mytopic"
        cfg = parse_connection_string(cs)
        assert cfg["bootstrap.servers"] == "myhub.servicebus.windows.net:9093"
        assert cfg["kafka_topic"] == "mytopic"
        assert cfg["sasl.username"] == "$ConnectionString"
        assert cfg["security.protocol"] == "SASL_SSL"

    def test_bootstrap_server_override(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test"
        cfg = parse_connection_string(cs)
        assert cfg["bootstrap.servers"] == "localhost:9092"
        assert cfg["kafka_topic"] == "test"


class TestMessageMap:
    def test_has_location_and_metadata(self):
        assert "location" in _MESSAGE_MAP
        assert "metadata" in _MESSAGE_MAP
        assert len(_MESSAGE_MAP) == 2

    def test_location_maps_to_vessel_location(self):
        data_class, method = _MESSAGE_MAP["location"]
        assert data_class.__name__ == "VesselLocation"
        assert method == "send_fi_digitraffic_marine_ais_vessel_location"

    def test_metadata_maps_to_vessel_metadata(self):
        data_class, method = _MESSAGE_MAP["metadata"]
        assert data_class.__name__ == "VesselMetadata"
        assert method == "send_fi_digitraffic_marine_ais_vessel_metadata"


class TestEmitEvent:
    def test_location_event(self):
        producer = MagicMock()
        payload = {
            "time": 1775137137,
            "sog": 10.7,
            "cog": 326.6,
            "navStat": 0,
            "rot": 0,
            "posAcc": True,
            "raim": False,
            "heading": 325,
            "lon": 20.345818,
            "lat": 60.03802,
        }
        result = _emit_event(producer, "location", 230629000, payload)
        assert result is True
        producer.send_fi_digitraffic_marine_ais_vessel_location.assert_called_once()

    def test_location_event_passes_mmsi_placeholder(self):
        producer = MagicMock()
        payload = {
            "time": 1775137137,
            "sog": 10.7,
            "cog": 326.6,
            "navStat": 0,
            "rot": 0,
            "posAcc": True,
            "raim": False,
            "heading": 325,
            "lon": 20.345818,
            "lat": 60.03802,
        }

        _emit_event(producer, "location", 230629000, payload)

        call = producer.send_fi_digitraffic_marine_ais_vessel_location.call_args
        assert call.kwargs["_mmsi"] == "230629000"
        assert call.kwargs["flush_producer"] is False
        assert "key_mapper" not in call.kwargs

    def test_metadata_event(self):
        producer = MagicMock()
        payload = {
            "timestamp": 1668075026035,
            "destination": "UST LUGA",
            "name": "ARUNA CIHAN",
            "draught": 68,
            "eta": 733376,
            "posType": 15,
            "refA": 160,
            "refB": 33,
            "refC": 20,
            "refD": 12,
            "callSign": "V7WW7",
            "imo": 9543756,
            "type": 70,
        }
        result = _emit_event(producer, "metadata", 538007963, payload)
        assert result is True
        producer.send_fi_digitraffic_marine_ais_vessel_metadata.assert_called_once()

    def test_unknown_type_returns_false(self):
        producer = MagicMock()
        result = _emit_event(producer, "status", 0, {})
        assert result is False

    def test_mmsi_injected_into_payload(self):
        """Verify MMSI from topic is injected into the data class."""
        producer = MagicMock()
        payload = {
            "time": 1775137137, "sog": 0, "cog": 0, "navStat": 0,
            "rot": 0, "posAcc": False, "raim": False, "heading": 0,
            "lon": 0, "lat": 0,
        }
        _emit_event(producer, "location", 230629000, payload)
        call_args = producer.send_fi_digitraffic_marine_ais_vessel_location.call_args
        data = call_args.kwargs.get("data") or call_args[1].get("data")
        assert data.mmsi == 230629000


class TestBridgeFiltering:
    def test_mmsi_filter_blocks(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = DigitraficBridge(
            mqtt_source=mqtt,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter={230629000},
        )

        bridge._on_message("location", 999999999, {
            "time": 0, "sog": 0, "cog": 0, "navStat": 0,
            "rot": 0, "posAcc": False, "raim": False, "heading": 0,
            "lon": 0, "lat": 0,
        })
        assert event_prod.send_fi_digitraffic_marine_ais_vessel_location.call_count == 0

    def test_mmsi_filter_allows(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = DigitraficBridge(
            mqtt_source=mqtt,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter={230629000},
        )

        bridge._on_message("location", 230629000, {
            "time": 1775137137, "sog": 10.7, "cog": 326.6, "navStat": 0,
            "rot": 0, "posAcc": True, "raim": False, "heading": 325,
            "lon": 20.345818, "lat": 60.03802,
        })
        event_prod.send_fi_digitraffic_marine_ais_vessel_location.assert_called_once()

    def test_no_filter_allows_all(self):
        mqtt = MagicMock()
        kafka = MagicMock()
        event_prod = MagicMock()

        bridge = DigitraficBridge(
            mqtt_source=mqtt,
            kafka_producer=kafka,
            event_producer=event_prod,
            mmsi_filter=None,
        )

        bridge._on_message("location", 999999999, {
            "time": 0, "sog": 0, "cog": 0, "navStat": 0,
            "rot": 0, "posAcc": False, "raim": False, "heading": 0,
            "lon": 0, "lat": 0,
        })
        event_prod.send_fi_digitraffic_marine_ais_vessel_location.assert_called_once()


class TestPortCallPoller:
    @pytest.fixture
    def state_file(self, tmp_path):
        return str(tmp_path / "portcalls-state.json")

    def test_parse_port_call(self):
        port_call = DigitrafficPortCallPoller.parse_port_call(SAMPLE_PORT_CALLS_RESPONSE["portCalls"][0])

        assert port_call is not None
        assert port_call.port_call_id == 3352890
        assert port_call.updated_at == "2026-04-08T07:31:42Z"
        assert port_call.port_to_visit == "FIKTK"
        assert port_call.previous_port == "DEHAM"
        assert port_call.next_port == "FIHEL"
        assert port_call.vessel_name == "Anina"
        assert port_call.vessel_name_prefix is None
        assert port_call.mmsi == 235011250
        assert len(port_call.agents) == 2
        assert port_call.agents[0].name == "C & C Port Agency Finland Oy Ltd, Helsinki"
        assert port_call.port_areas[0].eta == "2026-04-11T09:00:00Z"
        assert port_call.port_areas[0].arrival_draught == 0.0

    def test_parse_vessel_details(self):
        vessel_detail = DigitrafficPortCallPoller.parse_vessel_details(SAMPLE_VESSEL_DETAILS_RESPONSE[0])

        assert vessel_detail is not None
        assert vessel_detail.vessel_id == 99991900
        assert vessel_detail.updated_at == "2026-04-08T06:52:15Z"
        assert vessel_detail.mmsi == 210173000
        assert vessel_detail.name == "Hav Sand"
        assert vessel_detail.name_prefix == "ms"
        assert vessel_detail.vessel_construction["vessel_type_code"] == 70
        assert vessel_detail.vessel_dimensions["dead_weight"] == 3175
        assert vessel_detail.vessel_registration["nationality"] == "FO"
        assert vessel_detail.vessel_system["ship_owner"] is None
        assert vessel_detail.vessel_system["ship_verifier"] == "LIVI"

    def test_poll_port_locations_success(self, state_file):
        session = MagicMock()
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = SAMPLE_PORTS_RESPONSE
        session.get.return_value = response

        poller = DigitrafficPortCallPoller(
            kafka_producer=MagicMock(),
            event_producer=MagicMock(),
            vessel_details_event_producer=MagicMock(),
            port_location_event_producer=MagicMock(),
            state_file=state_file,
            session=session,
        )

        port_locations = poller.poll_port_locations()

        assert len(port_locations) == 1
        assert port_locations[0].locode == "DEHEI"
        assert port_locations[0].location_name == "Heidelberg"
        assert port_locations[0].country == "Germany"
        assert port_locations[0].longitude == 8.7
        assert port_locations[0].latitude == 49.41667
        assert len(port_locations[0].port_areas) == 1
        assert port_locations[0].port_areas[0].port_area_code == "MUU"
        assert len(port_locations[0].berths) == 1
        assert port_locations[0].berths[0].berth_code == "unknow"
        session.get.assert_called_once_with("https://meri.digitraffic.fi/api/port-call/v1/ports", timeout=60)

    def test_poll_port_calls_success(self, state_file):
        session = MagicMock()
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = SAMPLE_PORT_CALLS_RESPONSE
        session.get.return_value = response

        poller = DigitrafficPortCallPoller(
            kafka_producer=MagicMock(),
            event_producer=MagicMock(),
            vessel_details_event_producer=MagicMock(),
            port_location_event_producer=MagicMock(),
            state_file=state_file,
            session=session,
        )

        port_calls = poller.poll_port_calls()

        assert len(port_calls) == 1
        assert port_calls[0].port_call_id == 3352890
        session.get.assert_called_once_with("https://meri.digitraffic.fi/api/port-call/v1/port-calls", timeout=60)

    def test_poll_and_send_emits_reference_and_port_call_events(self, state_file):
        kafka = MagicMock()
        event_producer = MagicMock()
        vessel_details_event_producer = MagicMock()
        port_location_event_producer = MagicMock()
        poller = DigitrafficPortCallPoller(
            kafka_producer=kafka,
            event_producer=event_producer,
            vessel_details_event_producer=vessel_details_event_producer,
            port_location_event_producer=port_location_event_producer,
            state_file=state_file,
            session=MagicMock(),
        )

        port_call = DigitrafficPortCallPoller.parse_port_call(SAMPLE_PORT_CALLS_RESPONSE["portCalls"][0])
        vessel_detail = DigitrafficPortCallPoller.parse_vessel_details(SAMPLE_VESSEL_DETAILS_RESPONSE[0])
        port_location = DigitrafficPortCallPoller.parse_port_location(
            SAMPLE_PORTS_RESPONSE["ssnLocations"]["features"][0],
            SAMPLE_PORTS_RESPONSE["dataUpdatedTime"],
            SAMPLE_PORTS_RESPONSE["portAreas"]["features"],
            SAMPLE_PORTS_RESPONSE["berths"]["berths"],
        )
        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(poller, "poll_port_calls", lambda: [port_call])
            monkeypatch.setattr(poller, "poll_vessel_details", lambda: [vessel_detail])
            monkeypatch.setattr(poller, "poll_port_locations", lambda: [port_location])
            poller.poll_and_send(once=True)

        event_producer.send_fi_digitraffic_marine_portcall_port_call.assert_called_once()
        assert event_producer.send_fi_digitraffic_marine_portcall_port_call.call_args.kwargs["_port_call_id"] == "3352890"
        assert "key_mapper" not in event_producer.send_fi_digitraffic_marine_portcall_port_call.call_args.kwargs
        vessel_details_event_producer.send_fi_digitraffic_marine_portcall_vessel_details.assert_called_once_with(
            _vessel_id="99991900",
            data=vessel_detail,
            flush_producer=False,
        )
        port_location_event_producer.send_fi_digitraffic_marine_portcall_port_location.assert_called_once_with(
            _locode="DEHEI",
            data=port_location,
            flush_producer=False,
        )
        kafka.flush.assert_called_once()

        with open(state_file, "r", encoding="utf-8") as file_handle:
            state = json.load(file_handle)
        assert state["port_calls"]["3352890"] == "2026-04-08T07:31:42Z"
        assert state["vessel_details"]["99991900"] == "2026-04-08T06:52:15Z"
        assert state["port_locations"]["DEHEI"] == "2022-08-12T09:31:21.299259Z"

    def test_poll_and_send_skips_duplicate_port_call(self, state_file):
        with open(state_file, "w", encoding="utf-8") as file_handle:
            json.dump({
                "port_calls": {"3352890": "2026-04-08T07:31:42Z"},
                "vessel_details": {"99991900": "2026-04-08T06:52:15Z"},
                "port_locations": {"DEHEI": "2022-08-12T09:31:21.299259Z"},
            }, file_handle)

        kafka = MagicMock()
        event_producer = MagicMock()
        vessel_details_event_producer = MagicMock()
        port_location_event_producer = MagicMock()
        poller = DigitrafficPortCallPoller(
            kafka_producer=kafka,
            event_producer=event_producer,
            vessel_details_event_producer=vessel_details_event_producer,
            port_location_event_producer=port_location_event_producer,
            state_file=state_file,
            session=MagicMock(),
        )

        port_call = DigitrafficPortCallPoller.parse_port_call(SAMPLE_PORT_CALLS_RESPONSE["portCalls"][0])
        vessel_detail = DigitrafficPortCallPoller.parse_vessel_details(SAMPLE_VESSEL_DETAILS_RESPONSE[0])
        port_location = DigitrafficPortCallPoller.parse_port_location(
            SAMPLE_PORTS_RESPONSE["ssnLocations"]["features"][0],
            SAMPLE_PORTS_RESPONSE["dataUpdatedTime"],
            SAMPLE_PORTS_RESPONSE["portAreas"]["features"],
            SAMPLE_PORTS_RESPONSE["berths"]["berths"],
        )
        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(poller, "poll_port_calls", lambda: [port_call])
            monkeypatch.setattr(poller, "poll_vessel_details", lambda: [vessel_detail])
            monkeypatch.setattr(poller, "poll_port_locations", lambda: [port_location])
            poller.poll_and_send(once=True)

        event_producer.send_fi_digitraffic_marine_portcall_port_call.assert_not_called()
        vessel_details_event_producer.send_fi_digitraffic_marine_portcall_vessel_details.assert_not_called()
        port_location_event_producer.send_fi_digitraffic_marine_portcall_port_location.assert_not_called()
        kafka.flush.assert_not_called()
