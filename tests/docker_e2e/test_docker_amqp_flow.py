"""Docker E2E coverage for AMQP companion feeders added after PegelOnline."""

from __future__ import annotations

import socket
import time
import urllib.parse
from contextlib import closing
from typing import Any, Dict, List

import docker
import pytest

from .helpers import REPO_ROOT, build_image

ARTEMIS_IMAGE = "apache/activemq-artemis:latest-alpine"
ARTEMIS_USER = "admin"
ARTEMIS_PASSWORD = "admin"


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _receive_messages(host: str, port: int, queue: str, expected: int, timeout: float = 60.0) -> List[Any]:
    from proton.utils import BlockingConnection

    url = f"amqp://{urllib.parse.quote(ARTEMIS_USER)}:{urllib.parse.quote(ARTEMIS_PASSWORD)}@{host}:{port}"
    conn = BlockingConnection(url, timeout=30, allowed_mechs="PLAIN")
    receiver = conn.create_receiver(queue)
    messages: List[Any] = []
    deadline = time.time() + timeout
    try:
        while len(messages) < expected and time.time() < deadline:
            try:
                msg = receiver.receive(timeout=2.0)
            except Exception:
                if messages:
                    break
                continue
            messages.append(msg)
            receiver.accept()
    finally:
        conn.close()
    return messages


def _extract_ce_attrs(msg: Any) -> Dict[str, Any]:
    attrs: Dict[str, Any] = {}
    for k, v in dict(getattr(msg, "properties", None) or {}).items():
        if isinstance(k, str) and k.startswith("cloudEvents:"):
            attrs[k[len("cloudEvents:"):]] = v
        elif isinstance(k, str):
            attrs[k] = v
    if getattr(msg, "subject", None) and "subject" not in attrs:
        attrs["subject"] = msg.subject
    return attrs


@pytest.mark.docker_e2e
class AmqpDockerFlowBase:
    source_dir = ""
    image = ""
    env: Dict[str, str] = {}
    expected_types: set[str] = set()
    expected_count = 3

    def test_emits_cloudevents_to_amqp_queue(self):
        client = docker.from_env()
        queue = self.source_dir
        image = build_image(self.source_dir, dockerfile="Dockerfile.amqp", tag=f"test-{self.image}")
        network = client.networks.create(f"{self.image}-e2e", driver="bridge")
        host_port = _find_free_port()
        broker = None
        feeder = None
        try:
            broker = client.containers.run(
                ARTEMIS_IMAGE,
                name=f"{self.image}-broker",
                detach=True,
                remove=True,
                network=network.name,
                ports={"5672/tcp": host_port},
                environment={
                    "ARTEMIS_USER": ARTEMIS_USER,
                    "ARTEMIS_PASSWORD": ARTEMIS_PASSWORD,
                    "ANONYMOUS_LOGIN": "false",
                    "EXTRA_ARGS": f"--queues {queue}",
                },
            )
            deadline = time.time() + 90
            ready = False
            while time.time() < deadline:
                try:
                    with closing(socket.create_connection(("127.0.0.1", host_port), timeout=1)):
                        logs = broker.logs().decode("utf-8", errors="replace")
                        if "Server is now live" in logs or ("AMQP" in logs and "started" in logs.lower()):
                            ready = True
                            break
                except OSError:
                    pass
                time.sleep(2)
            if not ready:
                tail = broker.logs().decode("utf-8", errors="replace")[-2000:]
                pytest.skip(f"Artemis broker did not become ready. Tail:\n{tail}")
            time.sleep(8)

            env = {
                "AMQP_HOST": f"{self.image}-broker",
                "AMQP_PORT": "5672",
                "AMQP_ADDRESS": queue,
                "AMQP_USERNAME": ARTEMIS_USER,
                "AMQP_PASSWORD": ARTEMIS_PASSWORD,
                "AMQP_AUTH_MODE": "password",
                "PYTHONUNBUFFERED": "1",
                **self.env,
            }
            feeder = client.containers.run(image.id, detach=True, remove=False, network=network.name, environment=env)
            result = feeder.wait(timeout=600)
            logs = feeder.logs().decode("utf-8", errors="replace")
            assert result.get("StatusCode") == 0, f"Feeder failed: {result}\n{logs[-4000:]}"
            messages = _receive_messages("127.0.0.1", host_port, queue, expected=self.expected_count, timeout=60)
            assert messages, "No AMQP messages received"
            seen = {str(_extract_ce_attrs(m).get("type")) for m in messages}
            assert self.expected_types <= seen, f"Missing event types. Seen: {sorted(seen)}"
            for msg in messages:
                ce = _extract_ce_attrs(msg)
                for required in ("id", "source", "type", "subject", "specversion"):
                    assert required in ce, f"Missing CE {required}: {ce}"
        finally:
            if feeder is not None:
                try:
                    feeder.remove(force=True)
                except docker.errors.APIError:
                    pass
            if broker is not None:
                try:
                    broker.kill()
                except docker.errors.APIError:
                    pass
            try:
                network.remove()
            except docker.errors.APIError:
                pass


class TestKystverketAisAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "kystverket-ais"
    image = "kystverket-ais-amqp"
    env = {"KYSTVERKET_AIS_MOCK": "true"}
    expected_types = {"NO.Kystverket.AIS.PositionReport", "NO.Kystverket.AIS.ShipStatic", "NO.Kystverket.AIS.AidToNavigation"}


class TestKingCountyMarineAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "king-county-marine"
    image = "king-county-marine-amqp"
    env = {"KING_COUNTY_MARINE_SAMPLE_MODE": "true", "ONCE_MODE": "true"}
    expected_types = {"US.WA.KingCounty.Marine.Station", "US.WA.KingCounty.Marine.WaterQualityReading"}
    expected_count = 2


class TestVatsimAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "vatsim"
    image = "vatsim-amqp"
    env = {"VATSIM_SAMPLE_MODE": "true"}
    expected_types = {"net.vatsim.PilotPosition", "net.vatsim.ControllerPosition", "net.vatsim.NetworkStatus"}


class TestModeSAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "mode-s"
    image = "mode-s-amqp"
    env = {"MODE_S_MOCK": "true"}
    expected_types = {"Mode_S.ADSB", "Mode_S.AltitudeReply", "Mode_S.IdentityReply", "Mode_S.AcquisitionReply", "Mode_S.CommBAltitude", "Mode_S.CommBIdentity"}
    expected_count = 6


class TestAisstreamAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "aisstream"
    image = "aisstream-amqp"
    env = {"AISSTREAM_MOCK": "true"}
    expected_types = {"IO.AISstream.mqtt.PositionReport", "IO.AISstream.mqtt.ShipStatic", "IO.AISstream.mqtt.AidToNavigation"}

class TestAustraliaWildfiresAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "australia-wildfires"
    image = "australia-wildfires-amqp"
    env = {"AUSTRALIA_WILDFIRES_SAMPLE_MODE": "true", "ONCE_MODE": "true"}
    expected_types = {"AU.Gov.Emergency.Wildfires.FireIncident"}
    expected_count = 1


class TestCarbonIntensityAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "carbon-intensity"
    image = "carbon-intensity-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {"uk.org.carbonintensity.Intensity", "uk.org.carbonintensity.GenerationMix", "uk.org.carbonintensity.RegionalIntensity"}
    expected_count = 3


class TestRssAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "rss"
    image = "rss-amqp"
    env = {"RSS_SAMPLE_MODE": "true"}
    expected_types = {"Microsoft.OpenData.RssFeeds.FeedItem"}
    expected_count = 1


class TestWikimediaEventstreamsAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "wikimedia-eventstreams"
    image = "wikimedia-eventstreams-amqp"
    env = {"WIKIMEDIA_EVENTSTREAMS_MOCK": "true"}
    expected_types = {"Wikimedia.EventStreams.RecentChange"}
    expected_count = 4


class TestWikimediaOsmDiffsAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "wikimedia-osm-diffs"
    image = "wikimedia-osm-diffs-amqp"
    env = {"OSM_DIFFS_MOCK": "true"}
    expected_types = {"Org.OpenStreetMap.Diffs.MapChange", "Org.OpenStreetMap.Diffs.ReplicationState"}
    expected_count = 4


class TestBlueskyAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "bluesky"
    image = "bluesky-amqp"
    env = {"BLUESKY_MOCK": "true"}
    expected_types = {"Bluesky.Feed.Post", "Bluesky.Feed.Like", "Bluesky.Feed.Repost", "Bluesky.Graph.Follow", "Bluesky.Graph.Block", "Bluesky.Actor.Profile"}
    expected_count = 6


class TestEpaUvAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "epa-uv"
    image = "epa-uv-amqp"
    env = {"EPA_UV_MOCK": "true", "ONCE_MODE": "true"}
    expected_types = {"US.EPA.UVIndex.HourlyForecast", "US.EPA.UVIndex.DailyForecast"}
    expected_count = 2


class TestHongkongEpdAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "hongkong-epd"
    image = "hongkong-epd-amqp"
    env = {"HONGKONG_EPD_MOCK": "true", "ONCE_MODE": "true"}
    expected_types = {"HK.Gov.EPD.AQHI.Station", "HK.Gov.EPD.AQHI.AQHIReading"}
    expected_count = 2


class TestMeteoalarmAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "meteoalarm"
    image = "meteoalarm-amqp"
    env = {"METEOALARM_MOCK": "true", "ONCE_MODE": "true"}
    expected_types = {"Meteoalarm.WeatherWarning"}
    expected_count = 1


# B6 traffic/transit AMQP companion feeders

class TestAutobahnAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "autobahn"
    image = "autobahn-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'DE.Autobahn.ParkingLorryResolved', 'DE.Autobahn.EntryExitClosureResolved', 'DE.Autobahn.ClosureAppeared', 'DE.Autobahn.ElectricChargingStationAppeared', 'DE.Autobahn.ShortTermRoadworkAppeared', 'DE.Autobahn.ShortTermRoadworkUpdated', 'DE.Autobahn.ElectricChargingStationResolved', 'DE.Autobahn.WarningResolved', 'DE.Autobahn.WeightLimit35RestrictionUpdated', 'DE.Autobahn.StrongElectricChargingStationAppeared', 'DE.Autobahn.StrongElectricChargingStationResolved', 'DE.Autobahn.EntryExitClosureAppeared', 'DE.Autobahn.StrongElectricChargingStationUpdated', 'DE.Autobahn.ClosureUpdated', 'DE.Autobahn.WeightLimit35RestrictionAppeared', 'DE.Autobahn.RoadworkUpdated', 'DE.Autobahn.ElectricChargingStationUpdated', 'DE.Autobahn.ParkingLorryUpdated', 'DE.Autobahn.WarningUpdated', 'DE.Autobahn.WebcamUpdated', 'DE.Autobahn.WebcamAppeared', 'DE.Autobahn.ClosureResolved', 'DE.Autobahn.RoadworkAppeared', 'DE.Autobahn.ShortTermRoadworkResolved', 'DE.Autobahn.WeightLimit35RestrictionResolved', 'DE.Autobahn.WebcamResolved', 'DE.Autobahn.WarningAppeared', 'DE.Autobahn.EntryExitClosureUpdated', 'DE.Autobahn.ParkingLorryAppeared', 'DE.Autobahn.RoadworkResolved'}
    expected_count = 30

class TestFrenchRoadTrafficAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "french-road-traffic"
    image = "french-road-traffic-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'fr.gouv.transport.bison_fute.RoadEvent', 'fr.gouv.transport.bison_fute.TrafficFlowMeasurement'}
    expected_count = 2

class TestGTFSAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "gtfs"
    image = "gtfs-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'GeneralTransitFeedStatic.Transfers', 'GeneralTransitFeedStatic.FeedInfo', 'GeneralTransitFeedStatic.FareAttributes', 'GeneralTransitFeedStatic.StopAreas', 'GeneralTransitFeedStatic.LocationGroups', 'GeneralTransitFeedStatic.Pathways', 'GeneralTransitFeedStatic.Trips', 'GeneralTransitFeedRealTime.Trip.TripUpdate', 'GeneralTransitFeedStatic.Areas', 'GeneralTransitFeedStatic.LocationGeoJson', 'GeneralTransitFeedStatic.Networks', 'GeneralTransitFeedStatic.Routes', 'GeneralTransitFeedStatic.FareProducts', 'GeneralTransitFeedStatic.StopTimes', 'GeneralTransitFeedStatic.FareTransferRules', 'GeneralTransitFeedStatic.Frequencies', 'GeneralTransitFeedStatic.RouteNetworks', 'GeneralTransitFeedRealTime.Alert.Alert', 'GeneralTransitFeed.BookingRules', 'GeneralTransitFeedStatic.Levels', 'GeneralTransitFeedStatic.Stops', 'GeneralTransitFeedStatic.Timeframes', 'GeneralTransitFeedStatic.Shapes', 'GeneralTransitFeedStatic.LocationGroupStores', 'GeneralTransitFeedStatic.Attributions', 'GeneralTransitFeedStatic.FareRules', 'GeneralTransitFeedStatic.FareMedia', 'GeneralTransitFeedStatic.Agency', 'GeneralTransitFeedRealTime.Vehicle.VehiclePosition', 'GeneralTransitFeedStatic.Translations', 'GeneralTransitFeedStatic.FareLegRules'}
    expected_count = 31

class TestMadridTrafficAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "madrid-traffic"
    image = "madrid-traffic-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'es.madrid.informo.TrafficReading', 'es.madrid.informo.MeasurementPoint'}
    expected_count = 2

class TestNDLNetherlandsAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "ndl-netherlands"
    image = "ndl-netherlands-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'NL.NDW.Traffic.TrafficSpeed', 'NL.NDW.Traffic.TrafficSituation', 'NL.NDW.Traffic.TravelTime'}
    expected_count = 3

class TestNDWRoadTrafficAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "ndw-road-traffic"
    image = "ndw-road-traffic-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'NL.NDW.DRIP.DripDisplayState', 'NL.NDW.AVG.TrafficObservation', 'NL.NDW.Situations.TemporarySpeedLimit', 'NL.NDW.MSI.MsiDisplayState', 'NL.NDW.Situations.BridgeOpening', 'NL.NDW.Situations.TemporaryClosure', 'NL.NDW.DRIP.DripSign', 'NL.NDW.Situations.SafetyRelatedMessage', 'NL.NDW.Situations.Roadwork', 'NL.NDW.AVG.RouteMeasurementSite', 'NL.NDW.MSI.MsiSign', 'NL.NDW.AVG.TravelTimeObservation', 'NL.NDW.AVG.PointMeasurementSite'}
    expected_count = 13

class TestNextbusAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "nextbus"
    image = "nextbus-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'nextbus.Message', 'nextbus.VehiclePosition', 'nextbus.RouteConfig', 'nextbus.Schedule'}
    expected_count = 4

class TestParisBicycleCountersAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "paris-bicycle-counters"
    image = "paris-bicycle-counters-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'FR.Paris.OpenData.Velo.Counter', 'FR.Paris.OpenData.Velo.BicycleCount'}
    expected_count = 2

class TestSeattleStreetClosuresAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "seattle-street-closures"
    image = "seattle-street-closures-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'US.WA.Seattle.StreetClosures.StreetClosure'}
    expected_count = 1

class TestTFLRoadTrafficAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "tfl-road-traffic"
    image = "tfl-road-traffic-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'uk.gov.tfl.road.RoadStatus', 'uk.gov.tfl.road.RoadCorridor', 'uk.gov.tfl.road.RoadDisruption'}
    expected_count = 8

class TestTokyoDocomoBikeshareAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "tokyo-docomo-bikeshare"
    image = "tokyo-docomo-bikeshare-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'JP.ODPT.DocomoBikeshare.BikeshareSystem', 'JP.ODPT.DocomoBikeshare.BikeshareStation', 'JP.ODPT.DocomoBikeshare.BikeshareStationStatus'}
    expected_count = 3

class TestWSDOTAmqpDockerFlow(AmqpDockerFlowBase):
    source_dir = "wsdot"
    image = "wsdot-amqp"
    env = {"ONCE_MODE": "true"}
    expected_types = {'us.wa.wsdot.weather.WeatherStation', 'us.wa.wsdot.traffic.TrafficFlowStation', 'us.wa.wsdot.tolls.TollRate', 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction', 'us.wa.wsdot.ferries.VesselLocation', 'us.wa.wsdot.traveltimes.TravelTimeRoute', 'us.wa.wsdot.traffic.TrafficFlowReading', 'us.wa.wsdot.border.BorderCrossing', 'us.wa.wsdot.mountainpass.MountainPassCondition', 'us.wa.wsdot.weather.WeatherReading'}
    expected_count = 10
