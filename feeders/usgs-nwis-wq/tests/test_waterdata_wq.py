"""Frozen WQ projection, scope checks and broker durability."""

import asyncio
import base64
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from usgs_nwis_wq.waterdata import WaterDataFeed, api_mode
from usgs_nwis_wq.usgs_nwis_wq import USGSWaterQualityPoller
from usgs_nwis_wq.transport import PublisherAdapter
from usgs_waterdata_core.compat import CompatibilityError
from tests.synthetic_data import observations, waterml as synthetic_waterml

ROOT = Path(__file__).parents[1]


class MqttBroker:
    def __init__(self, *, connack=0, puback=0, acknowledged=True, publish_rc=0, **kwargs):
        self.identity = kwargs
        self.connack = connack
        self.puback = puback
        self.acknowledged = acknowledged
        self.publish_rc = publish_rc
        self.events = []
        self.confirmed = []
        self.connects = self.starts = self.stops = self.disconnects = 0

    def username_pw_set(self, *args):
        pass

    def tls_set(self):
        pass

    def connect(self, *args, **kwargs):
        self.connects += 1

    def loop_start(self):
        self.starts += 1
        if self.connack == "disconnect":
            self.on_disconnect(self, None, None, 128)
        else:
            self.on_connect(self, None, None, self.connack)

    def disconnect(self):
        self.disconnects += 1

    def loop_stop(self):
        self.stops += 1

    def publish(self, topic, payload, **kwargs):
        self.events.append((topic, json.loads(payload), kwargs))
        mid = len(self.events)
        if self.acknowledged and self.publish_rc == 0:
            self.on_publish(self, None, mid, self.puback)
        return SimpleNamespace(
            rc=self.publish_rc, mid=mid,
            wait_for_publish=lambda timeout: self.confirmed.append(mid),
            is_published=lambda: self.acknowledged,
        )


def test_mqtt_default_really_polls_legacy_waterml(monkeypatch, tmp_path):
    import usgs_nwis_wq.usgs_nwis_wq as runtime
    import usgs_nwis_wq_mqtt.app as app

    waterml = synthetic_waterml()
    requests = []
    events = []

    class Response:
        status = 200

        def raise_for_status(self):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def json(self, **kwargs):
            return waterml

    class Session(Response):
        def __init__(self, **kwargs):
            pass

        def get(self, url):
            requests.append(url)
            return Response()

    class Client:
        def __init__(self, **kwargs):
            pass

        async def connect(self, *args):
            pass

        async def disconnect(self):
            pass

        def __getattr__(self, name):
            async def publish(**kwargs):
                events.append((name, kwargs))
            return publish

    monkeypatch.delenv("USGS_API_MODE", raising=False)
    monkeypatch.delenv("USGS_ENROLLMENT_FILE", raising=False)
    monkeypatch.delenv("USGS_WQ_SITES", raising=False)
    monkeypatch.setenv("USGS_WQ_STATES", "MD")
    monkeypatch.setenv("USGS_WQ_PARAMETER_CODES", "00010")
    monkeypatch.setenv("USGS_WQ_LAST_POLLED_FILE", str(tmp_path / "legacy.json"))
    monkeypatch.setattr(runtime.aiohttp, "ClientSession", Session)
    monkeypatch.setattr(app.mqtt, "Client", MqttBroker)
    monkeypatch.setattr(app, "USGSWaterQualitySitesMqttMqttClient", Client)
    monkeypatch.setattr(app, "USGSWaterQualityReadingsMqttMqttClient", Client)
    asyncio.run(app.feed("localhost", 1883, once=True))
    assert requests and all(url.startswith("https://waterservices.usgs.gov/nwis/iv/") for url in requests)
    assert all("stateCd=MD" in url for url in requests)
    assert all("parameterCd=00010" in url for url in requests)
    assert len({name for name, _ in events}) == 2
    assert len(events) == 18
    assert all(args["data"].site_number == "99000001" for _, args in events)


@pytest.mark.parametrize("outcome", ["accepted", "missing-puback", "rejected-puback", "enqueue-failed", "rejected-connect", "disconnected"])
def test_real_mqtt_wrappers_share_owned_connection_and_confirm_delivery(feed, monkeypatch, outcome):
    import usgs_nwis_wq_mqtt.app as app

    brokers = []

    def make_broker(**kwargs):
        broker = MqttBroker(
            **kwargs,
            connack=128 if outcome == "rejected-connect" else "disconnect" if outcome == "disconnected" else 0,
            puback=128 if outcome == "rejected-puback" else 0,
            publish_rc=4 if outcome == "enqueue-failed" else 0,
            acknowledged=outcome != "missing-puback",
        )
        brokers.append(broker)
        return broker

    async def poll_and_send(once=False):
        assert once
        await feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))

    monkeypatch.setattr(app.mqtt, "Client", make_broker)
    monkeypatch.setattr(app, "USGSWaterQualityPoller", lambda **kwargs: feed.poller)
    monkeypatch.setattr(feed.poller, "poll_and_send", poll_and_send)

    async def run():
        await asyncio.wait_for(app.feed("broker.invalid", 1883, client_id="one-connection", once=True), 2)

    if outcome == "accepted":
        asyncio.run(run())
        assert feed.state.path.exists()
        assert len(brokers[0].events) == len(brokers[0].confirmed) == 18
        assert len({payload["parameter_code"] for _, payload, _ in brokers[0].events if "parameter_code" in payload}) == 1
        assert all(options["qos"] == 1 for _, _, options in brokers[0].events)
    else:
        message = ("PUBACK" if "puback" in outcome else "publish failed" if outcome == "enqueue-failed"
                   else "CONNECT" if outcome == "rejected-connect" else "CONNACK")
        with pytest.raises((RuntimeError, TimeoutError), match=message):
            asyncio.run(run())
        assert not feed.state.path.exists()
        assert not feed.state.data["observations"]
    assert len(brokers) == 1
    broker = brokers[0]
    assert broker.identity["client_id"] == "one-connection"
    assert broker.connects == broker.starts == broker.stops == broker.disconnects == 1


def test_amqp_shared_poller_keeps_transport_polling_and_state_configuration(monkeypatch):
    import usgs_nwis_wq.usgs_nwis_wq as runtime
    import usgs_nwis_wq_amqp.app as app

    calls = {}

    class Poller:
        def __init__(self, **kwargs):
            calls.update(kwargs)

        async def poll_and_send(self, once=False):
            calls["once"] = once

    monkeypatch.setenv("USGS_API_MODE", "legacy")
    monkeypatch.setenv("USGS_ENROLLMENT_FILE", "unused-during-rollback.json")
    monkeypatch.setenv("USGS_WQ_LAST_POLLED_FILE", "configured.json")
    monkeypatch.setattr(runtime, "USGSWaterQualityPoller", Poller)
    monkeypatch.setattr(app, "_build_sites_producer", lambda *args: SimpleNamespace(close=lambda: None))
    monkeypatch.setattr(app, "_build_readings_producer", lambda *args: SimpleNamespace(close=lambda: None))
    app.feed("localhost", 5672, once=True, polling_interval=17, state_file="fallback.json")
    assert calls["polling_interval"] == 17
    assert calls["last_polled_file"] == "configured.json"
    assert calls["once"] is True


class Producer:
    def __init__(self):
        self.producer = self
        self.events = []
        self.fail = False

    def __getattr__(self, name):
        if not name.startswith("send_"):
            raise AttributeError(name)
        return lambda **kwargs: self.events.append((name, kwargs))

    def flush(self, timeout=120):
        return 1 if self.fail else 0


@pytest.fixture
def feed(monkeypatch, tmp_path):
    monkeypatch.setenv("USGS_API_MODE", "waterdata")
    monkeypatch.setenv("USGS_ENROLLMENT_FILE", str(ROOT / "enrollment" / "synthetic-example.json"))
    monkeypatch.setenv("USGS_SITES", "99000001")
    monkeypatch.setenv("USGS_PARAMETERS", "00010")
    monkeypatch.setenv("USGS_STATE_FILE", str(tmp_path / "state.json"))
    poller = USGSWaterQualityPoller()
    poller.site_producer = Producer()
    poller.readings_producer = Producer()
    return WaterDataFeed(poller)


def fixture_client():
    features = [f for f in observations() if f["properties"]["parameter_code"] == "00010"]
    return SimpleNamespace(changes=lambda *args, **kwargs: deepcopy(features))


def test_original_wq_families_without_null_optional_fields(feed):
    assert asyncio.run(feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))) == 17
    assert len(feed.poller.site_producer.events) == 1
    assert len(feed.poller.readings_producer.events) == 17
    for _, args in feed.poller.site_producer.events + feed.poller.readings_producer.events:
        payload = json.loads(args["data"].to_json())
        assert payload["site_number"] == "99000001"
        assert None not in payload.values()
        assert args["_source_uri"] == "https://waterservices.usgs.gov/nwis/iv/"


def test_wq_window_excludes_old_corrections_but_iv_does_not(feed):
    client = fixture_client()
    rows = client.changes()
    rows[0]["properties"]["time"] = "2026-11-15T10:00:00+00:00"
    client.changes = lambda *args, **kwargs: rows
    assert asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))) == 16


def test_failed_delivery_does_not_advance_and_retry_sends_all(feed):
    feed.poller.readings_producer.fail = True
    now = datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)
    with pytest.raises(RuntimeError, match="flush"):
        asyncio.run(feed.cycle(fixture_client(), now))
    assert not feed.state.path.exists()
    assert not feed.state.data["observations"]
    feed.poller.readings_producer.fail = False
    assert asyncio.run(feed.cycle(fixture_client(), now)) == 17


def test_wq_metadata_refresh_dedupes_but_in_window_correction_emits(feed):
    client = fixture_client()
    asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    features = client.changes()
    for feature in features:
        feature["properties"]["last_modified"] = "2026-11-16T15:26:00+00:00"
    client.changes = lambda *args, **kwargs: features
    assert asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 27, tzinfo=timezone.utc))) == 0
    features[0]["properties"]["value"] = "10.1"
    assert asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 28, tzinfo=timezone.utc))) == 1


def test_unknown_series_never_silently_disappears_even_outside_window(feed):
    client = fixture_client()
    rows = client.changes()
    rows[0]["properties"].update(time_series_id="unknown", time="2026-11-15T10:00:00+00:00")
    client.changes = lambda *args, **kwargs: rows
    with pytest.raises(CompatibilityError, match="Unenrolled"):
        asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    assert not feed.poller.site_producer.events


@pytest.mark.parametrize("transport", ["mqtt", "amqp"])
def test_each_transport_emits_both_families_with_reviewed_routing(feed, transport):
    events = []
    class Client:
        def __getattr__(self, name):
            if transport == "mqtt":
                async def publish(**kwargs):
                    events.append((name, kwargs))
                return publish
            return lambda **kwargs: events.append((name, kwargs))
    feed.poller.site_producer = PublisherAdapter(Client(), transport)
    feed.poller.readings_producer = PublisherAdapter(Client(), transport)
    asyncio.run(feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    assert len(events) == 18
    assert len({name for name, _ in events}) == 2
    state_key = "state" if transport == "mqtt" else "_state"
    assert all(args[state_key] == "MD" for _, args in events)


def test_missing_enrollment_fails_and_legacy_remains_default(feed, monkeypatch):
    monkeypatch.delenv("USGS_ENROLLMENT_FILE")
    with pytest.raises(CompatibilityError, match="USGS_ENROLLMENT_FILE"):
        WaterDataFeed(feed.poller)
    monkeypatch.delenv("USGS_API_MODE")
    assert api_mode() == "legacy"


@pytest.mark.parametrize("tls", [False, True])
def test_amqp_remote_rejection_preserves_checkpoint(feed, monkeypatch, tls):
    from proton.reactor import AtLeastOnce
    from usgs_nwis_wq_amqp import delivery

    urls, options, auth = [], [], []

    class Sender:
        def send(self, message, **kwargs):
            if message.properties["cloudEvents:type"].endswith("WaterQualityReading"):
                raise RuntimeError("Broker rejected telemetry")

    class Connection:
        def __init__(self, url, **kwargs):
            urls.append(url)
            auth.append(kwargs)

        def create_sender(self, address, **kwargs):
            options.append(kwargs.get("options"))
            return Sender()

    monkeypatch.setattr(delivery, "BlockingConnection", Connection)
    for name, cls in (
        ("site_producer", delivery.ConfirmedSitesProducer),
        ("readings_producer", delivery.ConfirmedReadingsProducer),
    ):
        producer = cls(host="broker.invalid", port=5671 if tls else 5672, address="usgs",
                       username="publisher", password="example", use_tls=tls, content_mode="binary")
        assert producer._blocking_sender_is_presettled is False
        setattr(feed.poller, name, PublisherAdapter(producer, "amqp"))
    with pytest.raises(RuntimeError, match="rejected"):
        asyncio.run(feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    assert not feed.state.path.exists()
    assert not feed.state.data["observations"]
    assert all(url.startswith("amqps://" if tls else "amqp://") for url in urls)
    assert all(isinstance(option, AtLeastOnce) for option in options)
    assert all(config["allowed_mechs"] == "PLAIN" and config["sasl_enabled"] for config in auth)
    assert all(config["allow_insecure_mechs"] is (not tls) for config in auth)
    assert all(config["user"] == "publisher" and config["password"] == "example" for config in auth)


@pytest.mark.parametrize("auth", ["entra", "sas"])
def test_amqp_confirmed_boundary_preserves_cbs_auth(monkeypatch, auth):
    import usgs_nwis_wq_amqp_producer_amqp_producer.producer as generated
    from usgs_nwis_wq_amqp import delivery

    initialized = []
    kwargs = {"credential": object()} if auth == "entra" else {"sas_key_name": "name", "sas_key": "ZXhhbXBsZQ=="}
    for base, cls in (
        (generated.USGSWaterQualitySitesAmqpProducer, delivery.ConfirmedSitesProducer),
        (generated.USGSWaterQualityReadingsAmqpProducer, delivery.ConfirmedReadingsProducer),
    ):
        monkeypatch.setattr(base, "_init_reactor", lambda self: initialized.append(self))
        producer = cls(host="broker.invalid", address="usgs", use_tls=True, **kwargs)
        assert producer._cbs_enabled and producer._use_tls
        with pytest.raises(ValueError, match="mutually exclusive"):
            cls(host="broker.invalid", address="usgs", username="publisher", password="example", **kwargs)
    assert len(initialized) == 2


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
def test_generated_wq_producers_accept_frozen_payloads(feed, transport):
    events = []

    class Broker:
        def produce(self, topic, **kwargs):
            events.append(json.loads(kwargs["value"]))
            kwargs["on_delivery"](None, None)

        def flush(self, timeout=120):
            return 0

        def poll(self, timeout):
            pass

        def publish(self, topic, payload, **kwargs):
            events.append(json.loads(payload))
            return SimpleNamespace(rc=0, wait_for_publish=lambda: None)

    async def run():
        if transport == "kafka":
            from usgs_nwis_wq_producer_kafka_producer.producer import (
                USGSWaterQualitySitesEventProducer, USGSWaterQualityReadingsEventProducer,
            )
            from usgs_waterdata_core.delivery import AcknowledgedKafkaProducer
            broker = AcknowledgedKafkaProducer(Broker())
            feed.poller.site_producer = USGSWaterQualitySitesEventProducer(broker, "contract")
            feed.poller.readings_producer = USGSWaterQualityReadingsEventProducer(broker, "contract")
        elif transport == "mqtt":
            from usgs_nwis_wq_mqtt_producer_mqtt_client.client import (
                USGSWaterQualitySitesMqttMqttClient, USGSWaterQualityReadingsMqttMqttClient,
            )
            for name, cls in (
                ("site_producer", USGSWaterQualitySitesMqttMqttClient),
                ("readings_producer", USGSWaterQualityReadingsMqttMqttClient),
            ):
                client = cls(client=Broker(), content_mode="structured", loop=asyncio.get_running_loop())
                setattr(feed.poller, name, PublisherAdapter(client, "mqtt"))
        else:
            from usgs_nwis_wq_amqp_producer_amqp_producer.producer import (
                USGSWaterQualitySitesAmqpProducer, USGSWaterQualityReadingsAmqpProducer,
            )
            for name, cls in (
                ("site_producer", USGSWaterQualitySitesAmqpProducer),
                ("readings_producer", USGSWaterQualityReadingsAmqpProducer),
            ):
                producer = object.__new__(cls)
                producer.content_mode = "binary"
                producer._send_via_blocking_sender = lambda message: events.append(message)
                setattr(feed.poller, name, PublisherAdapter(producer, "amqp"))
        await feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))
    asyncio.run(run())
    assert len(events) == 18
    if transport != "amqp":
        assert {event["type"] for event in events} == {
            "USGS.WaterQuality.Sites.MonitoringSite", "USGS.WaterQuality.Readings.WaterQualityReading",
        }
        payloads = [
            event["data"] if "data" in event else json.loads(base64.b64decode(event["data_base64"]))
            for event in events
        ]
        assert all(None not in payload.values() for payload in payloads)
    else:
        assert all(None not in json.loads(event.body).values() for event in events)
        payloads = [json.loads(event.body) for event in events]
    from json_structure import InstanceValidator
    manifest = json.loads((ROOT / "xreg" / "usgs_nwis_wq.xreg.json").read_text())
    schemas = {
        name: schema["versions"][schema["defaultversionid"]]["schema"]
        for group in manifest["schemagroups"].values()
        for name, schema in group["schemas"].items()
    }
    event_types = [
        event["type"] if transport != "amqp" else event.properties["cloudEvents:type"]
        for event in events
    ]
    for event_type, payload in zip(event_types, payloads):
        assert not list(InstanceValidator(schemas[event_type], extended=True).validate_instance(payload))
    invalid_site = dict(payloads[0], county_code=None)
    assert list(InstanceValidator(schemas[event_types[0]], extended=True).validate_instance(invalid_site))
