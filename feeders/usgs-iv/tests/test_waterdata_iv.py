"""Compatibility evidence, complete family wiring and acknowledged checkpoints."""

import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from usgs_iv.waterdata import WaterDataFeed, api_mode
from usgs_iv.usgs_iv import USGSDataPoller
from usgs_waterdata_core.compat import CompatibilityError
from tests.synthetic_data import observations

ROOT = Path(__file__).parents[1]


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
    monkeypatch.setenv("USGS_PARAMETERS", "00010,00060")
    monkeypatch.setenv("USGS_STATE_FILE", str(tmp_path / "state.json"))
    poller = USGSDataPoller(once=True)
    poller.site_producer = Producer()
    poller.timeseries_producer = Producer()
    poller.values_producer = Producer()
    return WaterDataFeed(poller)


def fixture_client():
    return SimpleNamespace(changes=lambda *args, **kwargs: observations())


def test_all_iv_families_and_original_identity(feed):
    assert asyncio.run(feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))) == 34
    assert len(feed.poller.site_producer.events) == 1
    assert len(feed.poller.timeseries_producer.events) == 2
    events = feed.poller.values_producer.events
    assert {name for name, _ in events} == {
        "send_usgs_instantaneous_values_water_temperature", "send_usgs_instantaneous_values_streamflow",
    }
    assert {args["_timeseries_cd"] for _, args in events} == {"11111", "22222"}
    assert all(args["_source_uri"] == "https://waterservices.usgs.gov/nwis/iv/" for _, args in events)
    assert all(args["data"].datetime.endswith("+00:00") for _, args in events)


def test_failed_flush_and_unknown_series_do_not_checkpoint(feed):
    feed.poller.values_producer.fail = True
    with pytest.raises(RuntimeError, match="flush"):
        asyncio.run(feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    assert not feed.state.path.exists()
    assert not feed.state.data["observations"]
    feed.poller.values_producer.fail = False
    client = fixture_client()
    features = client.changes()
    features[-1]["properties"]["time_series_id"] = "unreviewed"
    client.changes = lambda *args, **kwargs: features
    before = len(feed.poller.site_producer.events)
    with pytest.raises(CompatibilityError, match="enrolled"):
        asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    assert len(feed.poller.site_producer.events) == before
    assert not feed.state.path.exists()


@pytest.mark.parametrize("rejected_connection", [None, "sites", "values", "timeseries"])
def test_frozen_mqtt_publish_completion_requires_successful_puback(feed, monkeypatch, rejected_connection):
    import usgs_iv_mqtt.app as app
    from paho.mqtt.packettypes import PacketTypes
    from paho.mqtt.reasoncodes import ReasonCode

    brokers = []

    class Broker:
        def __init__(self, **kwargs):
            self.identity = kwargs["client_id"].rsplit("-", 1)[-1]
            self.confirmed = []
            self.messages = []
            brokers.append(self)

        def connect(self, *args, **kwargs):
            pass

        def loop_start(self):
            pass

        def loop_stop(self):
            pass

        def disconnect(self):
            pass

        def publish(self, topic, payload, **kwargs):
            mid = len(self.messages) + 1
            self.messages.append(json.loads(payload))
            reason = ReasonCode(PacketTypes.PUBACK, identifier=135 if self.identity == rejected_connection else 0)
            self.on_publish(self, None, mid, reason)
            # Paho marks a rejected PUBACK published and retains enqueue rc=0.
            return SimpleNamespace(
                rc=0, mid=mid, is_published=lambda: True,
                wait_for_publish=lambda timeout=None: self.confirmed.append(mid),
            )

    async def poll_and_send():
        await feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))

    monkeypatch.setenv("MQTT_AUTH_MODE", "anonymous")
    monkeypatch.setattr(app.mqtt, "Client", Broker)
    monkeypatch.setattr(feed.poller, "poll_and_send", poll_and_send)
    if rejected_connection:
        with pytest.raises(RuntimeError, match="PUBACK missing or rejected: 135"):
            asyncio.run(app.feed(feed.poller, "broker.invalid", 1883, client_id="synthetic"))
        assert not feed.state.path.exists()
        assert not feed.state.data["observations"]
        if rejected_connection != "values":
            assert not next(broker for broker in brokers if broker.identity == "values").messages
    else:
        asyncio.run(app.feed(feed.poller, "broker.invalid", 1883, client_id="synthetic"))
        assert feed.state.path.exists()
        assert sum(len(broker.messages) for broker in brokers) == 37
        assert all(len(broker.confirmed) == 2 * len(broker.messages) for broker in brokers)
    assert {broker.identity for broker in brokers} == {"sites", "values", "timeseries"}


def test_refresh_dedupes_but_value_correction_reemits(feed):
    now = datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)
    client = fixture_client()
    asyncio.run(feed.cycle(client, now))
    features = client.changes()
    for feature in features:
        feature["properties"]["last_modified"] = "2026-11-16T15:26:00+00:00"
    client.changes = lambda *args, **kwargs: features
    assert asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 27, tzinfo=timezone.utc))) == 0
    features[0]["properties"]["value"] = "1521"
    assert asyncio.run(feed.cycle(client, datetime(2026, 11, 16, 15, 28, tzinfo=timezone.utc))) == 1


def test_iv_update_windows_include_old_observation_corrections(feed):
    features = fixture_client().changes()
    features[0]["properties"]["time"] = "2026-10-01T10:00:00+00:00"
    windows = []

    def changes(start, end, **kwargs):
        windows.append((start, end, kwargs))
        return features
    asyncio.run(feed.cycle(SimpleNamespace(changes=changes), datetime(2026, 11, 20, tzinfo=timezone.utc)))
    assert (windows[0][1] - windows[0][0]).total_seconds() == 7200
    assert "modified_since" not in windows[0][2]
    assert any(args["data"].datetime.startswith("2026-10-01") for _, args in feed.poller.values_producer.events)


def test_caught_up_iv_polls_wait_even_when_delivery_takes_time(feed, monkeypatch):
    from contextlib import nullcontext
    import usgs_iv.waterdata as module

    start = datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)
    clock_calls = []
    cycles = []
    delays = []

    class Clock:
        @staticmethod
        def now(tz):
            clock_calls.append(None)
            return start + timedelta(seconds=2 * len(clock_calls))

    class Finished(Exception):
        pass

    async def cycle(client, end):
        cycles.append(end)
        assert len(cycles) == 1, "Caught-up acquisition must wait between polls"
        feed.state.data["cursor"] = end.isoformat()
        return 0

    async def sleep(delay):
        delays.append(delay)
        raise Finished

    feed.poller.once = False
    monkeypatch.setattr(module, "datetime", Clock)
    monkeypatch.setattr(module, "WaterDataClient", lambda: nullcontext(object()))
    monkeypatch.setattr(feed, "cycle", cycle)
    monkeypatch.setattr(module.asyncio, "sleep", sleep)
    with pytest.raises(Finished):
        asyncio.run(feed.run())
    assert delays == [300]


def test_explicit_enrollment_and_full_selected_coverage(feed, monkeypatch):
    monkeypatch.setenv("USGS_PARAMETERS", "00010,00060,00065")
    with pytest.raises(CompatibilityError, match="00065"):
        WaterDataFeed(feed.poller)
    monkeypatch.delenv("USGS_ENROLLMENT_FILE")
    with pytest.raises(CompatibilityError, match="USGS_ENROLLMENT_FILE"):
        WaterDataFeed(feed.poller)
    monkeypatch.delenv("USGS_API_MODE")
    assert api_mode() == "legacy"


def test_site_list_uses_enrolled_snapshot(feed):
    async def collect():
        return [site async for site in feed.poller.get_sites_in_state("MD")]
    sites = asyncio.run(collect())
    assert len(sites) == 1
    assert sites[0].site_no == "99000001"
    assert sites[0].map_nm == "Synthetic grid"
    assert sites[0].dec_lat_va == 0.125


@pytest.mark.parametrize("tls", [False, True])
def test_amqp_remote_rejection_preserves_checkpoint(feed, monkeypatch, tls):
    from proton.reactor import AtLeastOnce
    from usgs_iv_amqp import delivery
    from usgs_iv_amqp.app import _AmqpPublishFacade, _MqttProducerAdapter

    urls, options, auth = [], [], []

    class Sender:
        def close(self):
            pass

        def send(self, message):
            if message.properties["cloudEvents:type"].startswith("USGS.InstantaneousValues."):
                raise RuntimeError("Broker rejected telemetry")

    class Connection:
        def __init__(self, url, **kwargs):
            urls.append(url)
            auth.append(kwargs)

        def create_sender(self, address, **kwargs):
            options.append(kwargs.get("options"))
            return Sender()

    monkeypatch.setattr(delivery, "BlockingConnection", Connection)
    producers = [
        cls(host="broker.invalid", port=5671 if tls else 5672, address="usgs",
            username="publisher", password="example", use_tls=tls)
        for cls in (delivery.ConfirmedSitesProducer, delivery.ConfirmedTimeseriesProducer, delivery.ConfirmedValuesProducer)
    ]
    facade = _AmqpPublishFacade(producers)
    feed.poller.site_producer = _MqttProducerAdapter(facade, "usgs_sites_")
    feed.poller.timeseries_producer = feed.poller.site_producer
    feed.poller.values_producer = _MqttProducerAdapter(facade, "usgs_instantaneous_values_")
    with pytest.raises(RuntimeError):
        asyncio.run(feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc)))
    assert not feed.state.path.exists()
    assert not feed.state.data["observations"]
    assert all(url.startswith("amqps://" if tls else "amqp://") for url in urls)
    assert len(options) == 3 and all(isinstance(option, AtLeastOnce) for option in options)
    assert all(config["allowed_mechs"] == "PLAIN" and config["sasl_enabled"] for config in auth)
    assert all(config["allow_insecure_mechs"] is (not tls) for config in auth)
    assert all(config["user"] == "publisher" and config["password"] == "example" for config in auth)


@pytest.mark.parametrize("auth", ["entra", "sas"])
def test_amqp_confirmed_boundary_preserves_cbs_auth(monkeypatch, auth):
    import usgs_iv_amqp_producer_amqp_producer.producer as generated
    from usgs_iv_amqp import delivery

    initialized = []
    kwargs = {"credential": object()} if auth == "entra" else {"sas_key_name": "name", "sas_key": "ZXhhbXBsZQ=="}
    for base, cls in (
        (generated.USGSSitesAmqpProducer, delivery.ConfirmedSitesProducer),
        (generated.USGSSiteTimeseriesAmqpProducer, delivery.ConfirmedTimeseriesProducer),
        (generated.USGSInstantaneousValuesAmqpProducer, delivery.ConfirmedValuesProducer),
    ):
        monkeypatch.setattr(base, "_init_reactor", lambda self: initialized.append(self))
        producer = cls(host="broker.invalid", address="usgs", use_tls=True, **kwargs)
        assert producer._cbs_enabled and producer._use_tls
        with pytest.raises(ValueError, match="mutually exclusive"):
            cls(host="broker.invalid", address="usgs", username="publisher", password="example", **kwargs)
    assert len(initialized) == 3


@pytest.mark.parametrize("auth", ["password", "entra", "sas"])
@pytest.mark.parametrize("content_mode", ["binary", "structured"])
def test_amqp_partition_identity_for_every_generated_family(monkeypatch, auth, content_mode):
    import inspect
    from proton import Message, symbol
    import usgs_iv_amqp_producer_amqp_producer.producer as generated
    from usgs_iv_amqp import delivery

    events = []

    class Queue:
        def put(self, queued):
            message, accepted = queued
            events.append(message)
            accepted.set_result(None)

    def init_reactor(self):
        self._handler = object()
        self._send_queue = Queue()

    class Connection:
        def __init__(self, *args, **kwargs):
            pass

        def create_sender(self, *args, **kwargs):
            return SimpleNamespace(send=events.append)

    monkeypatch.setattr(delivery, "BlockingConnection", Connection)
    auth_config = {
        "password": {"username": "publisher", "password": "example"},
        "entra": {"credential": object()},
        "sas": {"sas_key_name": "name", "sas_key": "ZXhhbXBsZQ=="},
    }[auth]
    arguments = dict(
        data={}, _source_uri="https://waterservices.usgs.gov/nwis/iv/",
        _agency_cd="USGS", _site_no="99000001", _parameter_cd="00010",
        _timeseries_cd="11111", _datetime="2026-11-16T13:00:00+00:00",
    )
    expected_subjects = set()
    for base, cls in (
        (generated.USGSSitesAmqpProducer, delivery.ConfirmedSitesProducer),
        (generated.USGSSiteTimeseriesAmqpProducer, delivery.ConfirmedTimeseriesProducer),
        (generated.USGSInstantaneousValuesAmqpProducer, delivery.ConfirmedValuesProducer),
    ):
        monkeypatch.setattr(base, "_init_reactor", init_reactor)
        producer = cls(host="broker.invalid", address="usgs", content_mode=content_mode, **auth_config)
        for name in dir(base):
            if not name.startswith("send_") or name.endswith("_batch"):
                continue
            method = getattr(producer, name)
            parameters = inspect.signature(method).parameters
            method(**{key: value for key, value in arguments.items() if key in parameters})
            expected = "USGS/99000001"
            if "_parameter_cd" in parameters:
                expected += "/00010/11111"
            expected_subjects.add(expected)
            decoded = Message()
            decoded.decode(events[-1].encode())
            assert decoded.subject == expected
            assert decoded.annotations[symbol("x-opt-partition-key")] == expected
            assert isinstance(next(iter(decoded.annotations)), symbol)
    assert expected_subjects == {"USGS/99000001", "USGS/99000001/00010/11111"}
    assert len(events) == sum(
        len([name for name in dir(cls) if name.startswith("send_") and not name.endswith("_batch")])
        for cls in (generated.USGSSitesAmqpProducer, generated.USGSSiteTimeseriesAmqpProducer,
                    generated.USGSInstantaneousValuesAmqpProducer)
    )


def test_amqp_partition_boundary_preserves_annotations_and_rejects_identity_loss():
    from proton import Message, symbol
    from usgs_iv_amqp.delivery import subject_partitioned

    delivered = []
    publish = subject_partitioned(delivered.append)
    message = Message(subject="USGS/99000001", annotations={symbol("existing"): "retained"})
    publish(message)
    assert message.annotations == {
        symbol("existing"): "retained", symbol("x-opt-partition-key"): "USGS/99000001",
    }
    for subject in (None, "", "x" * 129):
        with pytest.raises(ValueError, match="partition identity"):
            publish(Message(subject=subject))
    assert delivered == [message]


@pytest.mark.parametrize("transport", ["kafka", "mqtt", "amqp"])
def test_generated_methods_cover_all_selected_families(feed, transport):
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
            from usgs_iv_producer_kafka_producer.producer import (
                USGSSitesEventProducer, USGSSiteTimeseriesEventProducer, USGSInstantaneousValuesEventProducer,
            )
            from usgs_waterdata_core.delivery import AcknowledgedKafkaProducer
            broker = AcknowledgedKafkaProducer(Broker())
            feed.poller.site_producer = USGSSitesEventProducer(broker, "contract")
            feed.poller.timeseries_producer = USGSSiteTimeseriesEventProducer(broker, "contract")
            feed.poller.values_producer = USGSInstantaneousValuesEventProducer(broker, "contract")
        elif transport == "mqtt":
            from usgs_iv_mqtt.app import _MqttProducerAdapter
            from usgs_iv_mqtt_producer_mqtt_client.client import (
                USGSSitesMqttMqttClient, USGSSiteTimeseriesMqttMqttClient, USGSInstantaneousValuesMqttMqttClient,
            )
            for name, cls, prefix in (
                ("site_producer", USGSSitesMqttMqttClient, "usgs_sites_"),
                ("timeseries_producer", USGSSiteTimeseriesMqttMqttClient, "usgs_sites_"),
                ("values_producer", USGSInstantaneousValuesMqttMqttClient, "usgs_instantaneous_values_"),
            ):
                client = cls(client=Broker(), content_mode="structured", loop=asyncio.get_running_loop())
                setattr(feed.poller, name, _MqttProducerAdapter(client, prefix))
        else:
            from usgs_iv_amqp.app import _AmqpPublishFacade, _MqttProducerAdapter
            from usgs_iv_amqp_producer_amqp_producer.producer import (
                USGSSitesAmqpProducer, USGSSiteTimeseriesAmqpProducer, USGSInstantaneousValuesAmqpProducer,
            )
            producers = []
            for cls in (USGSSitesAmqpProducer, USGSSiteTimeseriesAmqpProducer, USGSInstantaneousValuesAmqpProducer):
                producer = object.__new__(cls)
                producer.content_mode = "binary"
                producer._sender = SimpleNamespace(send=events.append)
                producer._send_via_blocking_sender = lambda message: events.append(message)
                producers.append(producer)
            facade = _AmqpPublishFacade(producers)
            feed.poller.site_producer = _MqttProducerAdapter(facade, "usgs_sites_")
            feed.poller.timeseries_producer = feed.poller.site_producer
            feed.poller.values_producer = _MqttProducerAdapter(facade, "usgs_instantaneous_values_")
        await feed.cycle(fixture_client(), datetime(2026, 11, 16, 15, 25, tzinfo=timezone.utc))
    asyncio.run(run())
    assert len(events) == 37
    expected = {
        "USGS.Sites.Site", "USGS.Sites.SiteTimeseries",
        "USGS.InstantaneousValues.WaterTemperature", "USGS.InstantaneousValues.Streamflow",
    }
    if transport != "amqp":
        assert {event["type"] for event in events} == expected
    else:
        assert {event.properties["cloudEvents:type"] for event in events} == expected
