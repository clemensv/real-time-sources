"""Docker E2E test for the pegelonline AMQP 1.0 feeder.

Spins up an ActiveMQ Artemis broker as a sibling container, runs the
``pegelonline-amqp`` image against it in ``--once`` mode using SASL PLAIN,
then drains the queue with a Qpid Proton blocking receiver and validates
the emitted CloudEvents against the JsonStructure schemas declared in
``pegelonline/xreg/pegelonline.xreg.json``.

We deliberately use Artemis (not the Azure Service Bus emulator) for this
test:

* The bridge's ``password`` auth mode exercises generic AMQP 1.0 + SASL
  PLAIN, which is what Artemis, RabbitMQ AMQP 1.0, and Qpid Dispatch all
  expose. Artemis is the canonical "generic AMQP 1.0 broker" for testing.
* The Azure Service Bus emulator only advertises SASL ANONYMOUS and
  expects clients to authenticate via the AMQP CBS link with a JWT. The
  emulator does **not** accept real Entra ID tokens, so neither the
  bridge's ``password`` mode nor its ``entra`` mode can complete a
  handshake against it. Production Service Bus / Event Hubs use the
  ``entra`` mode against a real namespace.

Run with::

    pytest tests/docker_e2e/test_docker_amqp_artemis_flow.py -v -s
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import socket
import time
import urllib.parse
from proton import symbol
from contextlib import closing
from typing import Any, Dict, List

import docker
import pytest

from .helpers import REPO_ROOT, build_image

ARTEMIS_IMAGE = "apache/activemq-artemis:latest-alpine"
ARTEMIS_USER = "admin"
ARTEMIS_PASSWORD = "admin"
QUEUE_NAME = "pegelonline"


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _load_schemas() -> Dict[str, Dict[str, Any]]:
    xreg_path = os.path.join(REPO_ROOT, 'feeders', "pegelonline", "xreg", "pegelonline.xreg.json")
    with open(xreg_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    schemagroup = manifest["schemagroups"]["de.wsv.pegelonline.jstruct"]
    out: Dict[str, Dict[str, Any]] = {}
    for full_name, schema in schemagroup["schemas"].items():
        short = full_name.split(".")[-1]
        if short in ("Station", "CurrentMeasurement"):
            out[f"de.wsv.pegelonline.{short}"] = schema["versions"]["1"]["schema"]
    return out


@pytest.fixture(scope="module")
def pegelonline_amqp_image():
    return build_image("pegelonline", dockerfile="Dockerfile.amqp", tag="test-pegelonline-amqp")


@pytest.fixture()
def artemis_broker():
    client = docker.from_env()
    network = client.networks.create("pegelonline-amqp-e2e", driver="bridge")
    host_port = _find_free_port()
    container = None
    try:
        container = client.containers.run(
            ARTEMIS_IMAGE,
            name="pegelonline-amqp-e2e-broker",
            detach=True,
            remove=True,
            network=network.name,
            ports={"5672/tcp": host_port},
            environment={
                "ARTEMIS_USER": ARTEMIS_USER,
                "ARTEMIS_PASSWORD": ARTEMIS_PASSWORD,
                "ANONYMOUS_LOGIN": "false",
                # Pre-create the pegelonline address as an ANYCAST queue.
                # Without this, Artemis auto-creates the first-seen address
                # as MULTICAST (topic semantics), and messages sent before
                # any subscriber attaches are dropped.
                "EXTRA_ARGS": f"--queues {QUEUE_NAME}",
            },
        )

        # Wait for the AMQP acceptor to come up
        deadline = time.time() + 90
        ready = False
        while time.time() < deadline:
            try:
                with closing(socket.create_connection(("127.0.0.1", host_port), timeout=1)):
                    logs = container.logs().decode("utf-8", errors="replace")
                    if "Server is now live" in logs or "AMQP" in logs and "started" in logs.lower():
                        ready = True
                        break
            except OSError:
                pass
            time.sleep(2)
        if not ready:
            tail = container.logs().decode("utf-8", errors="replace")[-2000:]
            pytest.skip(f"Artemis broker not ready. Tail:\n{tail}")
        # Extra settle for acceptor init
        time.sleep(3)

        yield {
            "internal_host": "pegelonline-amqp-e2e-broker",
            "internal_port": 5672,
            "host_port": host_port,
            "network": network.name,
            "user": ARTEMIS_USER,
            "password": ARTEMIS_PASSWORD,
            "queue": QUEUE_NAME,
        }
    finally:
        if container is not None:
            try:
                container.kill()
            except docker.errors.APIError:
                pass
        try:
            network.remove()
        except docker.errors.APIError:
            pass


def _receive_messages(host: str, port: int, queue: str, user: str, password: str, expected: int, timeout: float = 60.0) -> List[Any]:
    """Drain messages from *queue* using proton blocking receiver.

    Returns when either *expected* messages are collected, *timeout* expires,
    or the broker is idle (no message for 5 seconds after at least one was
    received).
    """
    from proton.utils import BlockingConnection

    url = f"amqp://{urllib.parse.quote(user, safe='')}:{urllib.parse.quote(password, safe='')}@{host}:{port}"
    conn = BlockingConnection(url, timeout=30, allowed_mechs="PLAIN")
    receiver = conn.create_receiver(queue)
    messages: List[Any] = []
    deadline = time.time() + timeout
    idle_after = 5.0
    try:
        while len(messages) < expected and time.time() < deadline:
            try:
                msg = receiver.receive(timeout=2.0)
            except Exception:
                if messages and (time.time() - getattr(messages[-1], "_received_at", 0)) > idle_after:
                    break
                continue
            setattr(msg, "_received_at", time.time())
            messages.append(msg)
            receiver.accept()
    finally:
        try:
            conn.close()
        except Exception:  # pylint: disable=broad-except
            pass
    return messages


def _extract_ce_attrs(msg: Any) -> Dict[str, Any]:
    """Pull CloudEvents binary-mode attributes off an AMQP 1.0 Message.

    The CloudEvents AMQP 1.0 binding (binary mode) maps CE context
    attributes into application_properties, prefixed with ``cloudEvents:``
    per §3.1 of the spec. The Qpid Proton Python binding exposes
    application_properties as ``msg.properties``.
    """
    attrs: Dict[str, Any] = {}
    app_props = getattr(msg, "properties", None) or {}
    for k, v in dict(app_props).items():
        if not isinstance(k, str):
            continue
        if k.startswith("cloudEvents:"):
            attrs[k[len("cloudEvents:"):]] = v
        else:
            attrs[k] = v
    subj = getattr(msg, "subject", None)
    if subj and "subject" not in attrs:
        attrs["subject"] = subj
    ct = getattr(msg, "content_type", None)
    if ct and "datacontenttype" not in attrs:
        attrs["datacontenttype"] = ct
    return attrs


def _body_to_obj(msg: Any) -> Any:
    """Decode the AMQP message body as JSON.

    With xrcg ≥ 0.10.4 (which fixed the ``to_byte_array`` bytes/string
    regression) the body is sent as an AMQP binary section containing
    the raw UTF-8 JSON document. A single ``json.loads`` is sufficient.
    """
    body = msg.body
    if isinstance(body, memoryview):
        body = bytes(body)
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8", errors="replace")
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body
    return body


class TestPegelonlineAmqpArtemisFlow:
    """End-to-end: feeder pushes CloudEvents to Artemis over AMQP 1.0."""

    def test_emits_cloudevents_to_amqp_queue(self, artemis_broker, pegelonline_amqp_image):
        client = docker.from_env()

        feeder = client.containers.run(
            pegelonline_amqp_image.id,
            detach=True,
            remove=False,
            network=artemis_broker["network"],
            environment={
                "AMQP_HOST": artemis_broker["internal_host"],
                "AMQP_PORT": str(artemis_broker["internal_port"]),
                "AMQP_ADDRESS": artemis_broker["queue"],
                "AMQP_USERNAME": artemis_broker["user"],
                "AMQP_PASSWORD": artemis_broker["password"],
                "AMQP_AUTH_MODE": "password",
                "POLLING_INTERVAL": "60",
                "ONCE_MODE": "true",
                "PYTHONUNBUFFERED": "1",
            },
        )
        try:
            result = feeder.wait(timeout=600)
            logs = feeder.logs().decode("utf-8", errors="replace")
            assert result.get("StatusCode") == 0, (
                f"Feeder exited non-zero: {result}\n--- LOGS (last 4KB) ---\n{logs[-4000:]}"
            )
        finally:
            try:
                feeder.remove(force=True)
            except docker.errors.APIError:
                pass

        # Pre-created ANYCAST queue retains messages until consumed.
        messages = _receive_messages(
            "127.0.0.1",
            artemis_broker["host_port"],
            artemis_broker["queue"],
            artemis_broker["user"],
            artemis_broker["password"],
            expected=5000,
            timeout=60,
        )
        assert messages, "No AMQP messages received from Artemis"

        # Bucket by CloudEvent type
        types: Dict[str, List[Any]] = {}
        for m in messages:
            ce = _extract_ce_attrs(m)
            t = ce.get("type")
            if t:
                types.setdefault(t, []).append((m, ce))

        if "de.wsv.pegelonline.Station" not in types:
            # Dump first message for diagnosis
            first = messages[0]
            diag = {
                "subject": getattr(first, "subject", None),
                "content_type": getattr(first, "content_type", None),
                "properties": dict(getattr(first, "properties", {}) or {}),
                "application_properties": dict(getattr(first, "application_properties", {}) or {}),
                "applicationproperties": dict(getattr(first, "applicationproperties", {}) or {}),
                "body_head": str(getattr(first, "body", ""))[:300],
                "extracted_ce_attrs": _extract_ce_attrs(first),
            }
            raise AssertionError(
                f"No Station events. Types seen: {sorted(types.keys())}. "
                f"Got {len(messages)} messages total. First message:\n"
                f"{json.dumps(diag, default=str, indent=2)}"
            )
        assert "de.wsv.pegelonline.CurrentMeasurement" in types, (
            f"No CurrentMeasurement events. Types seen: {sorted(types.keys())}"
        )

        # Sanity-check CE envelope on first sample of each type
        for ce_type in ("de.wsv.pegelonline.Station", "de.wsv.pegelonline.CurrentMeasurement"):
            sample_msg, sample_ce = types[ce_type][0]
            for required in ("id", "source", "type", "subject", "specversion"):
                assert required in sample_ce, (
                    f"Missing CE attribute {required!r} on {ce_type}: {sample_ce}"
                )
            assert sample_ce["specversion"] == "1.0"
            assert sample_ce["type"] == ce_type

        # Validate one body against the JsonStructure schema
        schemas = _load_schemas()
        from json_structure import InstanceValidator, SchemaValidator
        validator_factory = SchemaValidator(extended=True)
        for ce_type, items in types.items():
            if ce_type not in schemas:
                continue
            sample_msg, _ = items[0]
            data = _body_to_obj(sample_msg)
            assert isinstance(data, dict), f"{ce_type} body not a JSON object: {data!r}"
            schema = schemas[ce_type]
            assert not validator_factory.validate(schema), (
                f"Invalid JsonStructure schema for {ce_type}"
            )
            errors = InstanceValidator(schema, extended=True).validate_instance(data)
            assert not errors, f"JsonStructure validation failed for {ce_type}: {errors[:3]}"


@pytest.fixture(scope="module")
def entsoe_amqp_image():
    return build_image("entsoe", dockerfile="Dockerfile.amqp", tag="test-entsoe-amqp")


class TestEntsoeAmqpDockerFlow:
    def test_emits_cloudevents_to_amqp_queue(self, artemis_broker, entsoe_amqp_image):
        client = docker.from_env()
        feeder = client.containers.run(
            entsoe_amqp_image.id, detach=True, remove=False, network=artemis_broker["network"],
            environment={
                "AMQP_HOST": artemis_broker["internal_host"],
                "AMQP_PORT": str(artemis_broker["internal_port"]),
                "AMQP_ADDRESS": artemis_broker["queue"],
                "AMQP_USERNAME": artemis_broker["user"],
                "AMQP_PASSWORD": artemis_broker["password"],
                "AMQP_AUTH_MODE": "password",
                "ENTSOE_SAMPLE_MODE": "true",
                "ONCE_MODE": "true",
                "PYTHONUNBUFFERED": "1",
            },
        )
        try:
            result = feeder.wait(timeout=300)
            logs = feeder.logs().decode("utf-8", errors="replace")
            assert result.get("StatusCode") == 0, f"Feeder exited non-zero: {result}\n--- LOGS ---\n{logs}"
        finally:
            try: feeder.remove(force=True)
            except docker.errors.APIError: pass
        messages = _receive_messages("127.0.0.1", artemis_broker["host_port"], artemis_broker["queue"], artemis_broker["user"], artemis_broker["password"], expected=11, timeout=60)
        assert len(messages) >= 11
        types = {_extract_ce_attrs(m).get("type") for m in messages}
        assert "eu.entsoe.transparency.DayAheadPrices" in types
        assert "eu.entsoe.transparency.CrossBorderPhysicalFlows" in types
        for m in messages[:3]:
            assert getattr(m, 'content_type', None) == 'application/json'
            ce = _extract_ce_attrs(m)
            for required in ("id", "source", "type", "subject", "specversion"):
                assert required in ce, ce
            data = _body_to_obj(m)
            assert isinstance(data, dict), data
            app_props = dict(getattr(m, "properties", None) or {})
            # CloudEvents AMQP binary mode stores type as "cloudEvents:type" in
            # application properties; extract the short class name from the suffix.
            assert ce.get("type", "").split(".")[-1] in {"DayAheadPrices", "CrossBorderPhysicalFlows", "ActualGenerationPerType", "ActualTotalLoad", "WindSolarForecast", "LoadForecastMargin", "GenerationForecast", "ReservoirFillingInformation", "ActualGeneration", "WindSolarGeneration", "InstalledGenerationCapacityPerType"}
            if "inDomain" in data:
                # Generated producers use either camelCase (cloudEvents: prefixed) or
                # hyphenated (non-prefixed) naming depending on the producer template.
                assert (ce.get("inDomain") or ce.get("in-domain")) == data["inDomain"]
            if "outDomain" in data and ("outDomain" in ce or "out-domain" in ce):
                assert (ce.get("outDomain") or ce.get("out-domain")) == data["outDomain"]
            if "psrType" in data and ("psrType" in ce or "psr-type" in ce):
                assert (ce.get("psrType") or ce.get("psr-type")) == data["psrType"]
            annotations = dict(getattr(m, "annotations", None) or {})
            partition_key = annotations.get(symbol("x-opt-partition-key")) or annotations.get("x-opt-partition-key")
            assert partition_key == ce["subject"]
# ---------------------------------------------------------------------------
# AMQP companion backfill feeders (mock-mode, generic Artemis broker)
# ---------------------------------------------------------------------------

HYDRO_AMQP_SOURCES = [
    ("bafu-hydro", "test-bafu-hydro-amqp", "CH.BAFU.Hydrology.Station", "CH.BAFU.Hydrology.WaterLevelObservation"),
    ("chmi-hydro", "test-chmi-hydro-amqp", "CZ.Gov.CHMI.Hydro.Station", "CZ.Gov.CHMI.Hydro.WaterLevelObservation"),
    ("german-waters", "test-german-waters-amqp", "DE.Waters.Hydrology.Station", "DE.Waters.Hydrology.WaterLevelObservation"),
    ("nve-hydro", "test-nve-hydro-amqp", "NO.NVE.Hydrology.Station", "NO.NVE.Hydrology.WaterLevelObservation"),
    ("rws-waterwebservices", "test-rws-waterwebservices-amqp", "NL.RWS.Waterwebservices.Station", "NL.RWS.Waterwebservices.WaterLevelObservation"),
    ("smhi-hydro", "test-smhi-hydro-amqp", "SE.Gov.SMHI.Hydro.Station", "SE.Gov.SMHI.Hydro.DischargeObservation"),
    ("wallonia-issep", "test-wallonia-issep-amqp", "be.issep.airquality.SensorConfiguration", "be.issep.airquality.Observation"),
    ("fdsn-seismology", "test-fdsn-seismology-amqp", "org.fdsn.event.Node", "org.fdsn.event.Earthquake"),
]


def _load_source_schemas(source_dir: str) -> Dict[str, Dict[str, Any]]:
    xreg_dir = os.path.join(REPO_ROOT, 'feeders', source_dir, "xreg")
    xreg_name = next(n for n in os.listdir(xreg_dir) if n.endswith(".xreg.json"))
    with open(os.path.join(xreg_dir, xreg_name), "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    schemagroup = next(v for k, v in manifest["schemagroups"].items() if k.endswith(".jstruct"))
    return {name: schema["versions"]["1"]["schema"] for name, schema in schemagroup["schemas"].items()}


def _run_generic_amqp_artemis_flow(source_dir: str, image_tag: str, station_type: str, telemetry_type: str) -> None:
    queue = source_dir
    client = docker.from_env()
    image = build_image(source_dir, dockerfile="Dockerfile.amqp", tag=image_tag)
    network = client.networks.create(f"{source_dir}-amqp-e2e", driver="bridge")
    host_port = _find_free_port()
    broker = None
    try:
        broker = client.containers.run(
            ARTEMIS_IMAGE,
            name=f"{source_dir}-amqp-e2e-broker",
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
        while time.time() < deadline:
            try:
                with closing(socket.create_connection(("127.0.0.1", host_port), timeout=1)):
                    logs = broker.logs().decode("utf-8", errors="replace")
                    if "Server is now live" in logs or ("AMQP" in logs and "started" in logs.lower()):
                        break
            except OSError:
                pass
            time.sleep(2)
        else:
            pytest.skip(f"Artemis broker not ready. Tail:\n{broker.logs().decode('utf-8', errors='replace')[-2000:]}")
        time.sleep(3)
        feeder = client.containers.run(
            image.id,
            detach=True,
            remove=False,
            network=network.name,
            environment={
                "AMQP_HOST": f"{source_dir}-amqp-e2e-broker",
                "AMQP_PORT": "5672",
                "AMQP_ADDRESS": queue,
                "AMQP_USERNAME": ARTEMIS_USER,
                "AMQP_PASSWORD": ARTEMIS_PASSWORD,
                "AMQP_AUTH_MODE": "password",
                "MOCK_MODE": "true",
                "NVE_API_KEY": "mock",
                "ONCE_MODE": "true",
                "PYTHONUNBUFFERED": "1",
            },
        )
        try:
            result = feeder.wait(timeout=300)
            logs = feeder.logs().decode("utf-8", errors="replace")
            assert result.get("StatusCode") == 0, f"Feeder exited non-zero: {result}\n--- LOGS ---\n{logs[-4000:]}"
        finally:
            feeder.remove(force=True)
        expected_messages = 16 if source_dir == "fdsn-seismology" else 2
        messages = _receive_messages("127.0.0.1", host_port, queue, ARTEMIS_USER, ARTEMIS_PASSWORD, expected=expected_messages, timeout=60)
        assert messages, "No AMQP messages received from Artemis"
        by_type: Dict[str, List[Any]] = {}
        for message in messages:
            ce = _extract_ce_attrs(message)
            by_type.setdefault(ce.get("type"), []).append((message, ce))
        assert station_type in by_type, sorted(by_type)
        assert telemetry_type in by_type, sorted(by_type)
        schemas = _load_source_schemas(source_dir)
        from json_structure import InstanceValidator, SchemaValidator
        validator_factory = SchemaValidator(extended=True)
        for ce_type in (station_type, telemetry_type):
            sample_msg, sample_ce = by_type[ce_type][0]
            for required in ("id", "source", "type", "subject", "specversion"):
                assert required in sample_ce, f"Missing CE attribute {required!r}: {sample_ce}"
            schema = schemas[ce_type]
            assert not validator_factory.validate(schema)
            data = _body_to_obj(sample_msg)
            assert isinstance(data, dict), data
            errors = InstanceValidator(schema, extended=True).validate_instance(data)
            assert not errors, f"JsonStructure validation failed for {ce_type}: {errors[:3]}"
    finally:
        if broker is not None:
            try:
                broker.kill()
            except docker.errors.APIError:
                pass
        try:
            network.remove()
        except docker.errors.APIError:
            pass


class TestBafuHydroAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[0])

class TestChmiHydroAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[1])

class TestGermanWatersAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[2])

class TestNveHydroAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[3])

class TestRwsWaterwebservicesAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[4])

class TestSmhiHydroAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[5])

class TestWalloniaIssepAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[6])

class TestFdsnSeismologyAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_generic_amqp_artemis_flow(*HYDRO_AMQP_SOURCES[7])


# ---------------------------------------------------------------------------
# B1 hydro/maritime AMQP companions (Artemis, mock-mode)
# ---------------------------------------------------------------------------

B1_AMQP_SOURCES = [('canada-eccc-wateroffice', 'test-canada-eccc-wateroffice-amqp', ['CA.Gov.ECCC.Hydro.Observation', 'CA.Gov.ECCC.Hydro.Station']), ('cdec-reservoirs', 'test-cdec-reservoirs-amqp', ['gov.ca.water.cdec.ReservoirReading']), ('hubeau-hydrometrie', 'test-hubeau-hydrometrie-amqp', ['FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation', 'FR.Gov.Eaufrance.HubEau.Hydrometrie.Station']), ('imgw-hydro', 'test-imgw-hydro-amqp', ['PL.Gov.IMGW.Hydro.Station', 'PL.Gov.IMGW.Hydro.WaterLevelObservation']), ('ireland-opw-waterlevel', 'test-ireland-opw-waterlevel-amqp', ['ie.gov.opw.waterlevel.Station', 'ie.gov.opw.waterlevel.WaterLevelReading']), ('nepal-bipad-hydrology', 'test-nepal-bipad-hydrology-amqp', ['np.gov.bipad.hydrology.RiverStation', 'np.gov.bipad.hydrology.WaterLevelReading']), ('noaa-ndbc', 'test-noaa-ndbc-amqp', ['Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation', 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement', 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary', 'Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement', 'Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation', 'Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation', 'Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation', 'Microsoft.OpenData.US.NOAA.NDBC.BuoyStation', 'Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement']), ('noaa', 'test-noaa-amqp', ['Microsoft.OpenData.US.NOAA.AirPressure', 'Microsoft.OpenData.US.NOAA.AirTemperature', 'Microsoft.OpenData.US.NOAA.Conductivity', 'Microsoft.OpenData.US.NOAA.CurrentPredictions', 'Microsoft.OpenData.US.NOAA.Currents', 'Microsoft.OpenData.US.NOAA.Humidity', 'Microsoft.OpenData.US.NOAA.Predictions', 'Microsoft.OpenData.US.NOAA.Salinity', 'Microsoft.OpenData.US.NOAA.Station', 'Microsoft.OpenData.US.NOAA.Visibility', 'Microsoft.OpenData.US.NOAA.WaterLevel', 'Microsoft.OpenData.US.NOAA.WaterTemperature', 'Microsoft.OpenData.US.NOAA.Wind']), ('snotel', 'test-snotel-amqp', ['gov.usda.nrcs.snotel.SnowObservation', 'gov.usda.nrcs.snotel.Station']), ('syke-hydro', 'test-syke-hydro-amqp', ['FI.SYKE.Hydrology.Station', 'FI.SYKE.Hydrology.WaterLevelObservation']), ('uk-ea-flood-monitoring', 'test-uk-ea-flood-monitoring-amqp', ['UK.Gov.Environment.EA.FloodMonitoring.Reading', 'UK.Gov.Environment.EA.FloodMonitoring.Station']), ('usgs-nwis-wq', 'test-usgs-nwis-wq-amqp', ['USGS.WaterQuality.Readings.WaterQualityReading', 'USGS.WaterQuality.Sites.MonitoringSite']), ('waterinfo-vmm', 'test-waterinfo-vmm-amqp', ['BE.Vlaanderen.Waterinfo.VMM.Station', 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'])]


def _run_b1_amqp_artemis_flow(index: int) -> None:
    source_dir, image_tag, expected_types = B1_AMQP_SOURCES[index]
    queue = source_dir
    client = docker.from_env()
    image = build_image(source_dir, dockerfile='Dockerfile.amqp', tag=image_tag)
    network = client.networks.create(f'{source_dir}-b1-amqp-e2e', driver='bridge')
    host_port = _find_free_port()
    broker = None
    try:
        broker = client.containers.run(ARTEMIS_IMAGE, name=f'{source_dir}-b1-amqp-e2e-broker', detach=True, remove=True, network=network.name, ports={'5672/tcp': host_port}, environment={'ARTEMIS_USER': ARTEMIS_USER, 'ARTEMIS_PASSWORD': ARTEMIS_PASSWORD, 'ANONYMOUS_LOGIN': 'false', 'EXTRA_ARGS': f'--queues {queue}'})
        deadline = time.time() + 90
        while time.time() < deadline:
            try:
                with closing(socket.create_connection(('127.0.0.1', host_port), timeout=1)):
                    logs = broker.logs().decode('utf-8', errors='replace')
                    if 'Server is now live' in logs or ('AMQP' in logs and 'started' in logs.lower()): break
            except OSError: pass
            time.sleep(2)
        time.sleep(3)
        feeder = client.containers.run(image.id, detach=True, remove=False, network=network.name, environment={'AMQP_HOST': f'{source_dir}-b1-amqp-e2e-broker', 'AMQP_PORT': '5672', 'AMQP_ADDRESS': queue, 'AMQP_USERNAME': ARTEMIS_USER, 'AMQP_PASSWORD': ARTEMIS_PASSWORD, 'AMQP_AUTH_MODE': 'password', 'MOCK_MODE': 'true', 'ONCE_MODE': 'true', 'PYTHONUNBUFFERED': '1'})
        try:
            result = feeder.wait(timeout=300); logs = feeder.logs().decode('utf-8', errors='replace')
            assert result.get('StatusCode') == 0, f"Feeder exited non-zero: {result}\n--- LOGS ---\n{logs[-4000:]}"
        finally:
            feeder.remove(force=True)
        messages = _receive_messages('127.0.0.1', host_port, queue, ARTEMIS_USER, ARTEMIS_PASSWORD, expected=len(expected_types), timeout=30)
        assert messages, f'No AMQP messages received for {source_dir}'
        seen = {_extract_ce_attrs(m).get('type') for m in messages}
        assert set(expected_types).issubset(seen), (source_dir, seen, expected_types)
        for m in messages[: min(3, len(messages))]:
            ce = _extract_ce_attrs(m)
            for required in ('id','source','type','subject','specversion'):
                assert required in ce, ce
            assert isinstance(_body_to_obj(m), dict)
    finally:
        if broker is not None:
            try: broker.kill()
            except docker.errors.APIError: pass
        try: network.remove()
        except docker.errors.APIError: pass

class TestCanadaEcccWaterofficeAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(0)


class TestCdecReservoirsAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(1)


class TestHubeauHydrometrieAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(2)


class TestImgwHydroAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(3)


class TestIrelandOpwWaterlevelAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(4)


class TestNepalBipadHydrologyAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(5)


class TestNoaaNdbcAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(6)


class TestNoaaAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(7)


class TestSnotelAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(8)


class TestSykeHydroAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(9)


class TestUkEaFloodMonitoringAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(10)


class TestUsgsNwisWqAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(11)


class TestWaterinfoVmmAmqpArtemisFlow:
    def test_emits_cloudevents_to_amqp_queue(self):
        _run_b1_amqp_artemis_flow(12)



# ===========================================================================
# NOAA SWPC L1 AMQP 1.0 (Artemis) ΓÇö also asserts x-opt-partition-key
# ===========================================================================
SWPC_QUEUE_NAME = "noaa-swpc-l1"
@pytest.fixture(scope="module")
def noaa_swpc_l1_amqp_image():
    return build_image("noaa-swpc-l1", dockerfile="Dockerfile.amqp", tag="test-noaa-swpc-l1-amqp")

@pytest.fixture()
def artemis_broker_swpc():
    client = docker.from_env()
    network = client.networks.create("noaa-swpc-l1-amqp-e2e", driver="bridge")
    host_port = _find_free_port()
    container = None
    try:
        container = client.containers.run(
            ARTEMIS_IMAGE,
            name="noaa-swpc-l1-amqp-e2e-broker",
            detach=True, remove=True, network=network.name,
            ports={"5672/tcp": host_port},
            environment={
                "ARTEMIS_USER": ARTEMIS_USER,
                "ARTEMIS_PASSWORD": ARTEMIS_PASSWORD,
                "ANONYMOUS_LOGIN": "false",
                "EXTRA_ARGS": f"--queues {SWPC_QUEUE_NAME}",
            },
        )
        deadline = time.time() + 90
        ready = False
        while time.time() < deadline:
            try:
                with closing(socket.create_connection(("127.0.0.1", host_port), timeout=1)):
                    logs = container.logs().decode("utf-8", errors="replace")
                    if "Server is now live" in logs or ("AMQP" in logs and "started" in logs.lower()):
                        ready = True
                        break
            except OSError:
                pass
            time.sleep(2)
        if not ready:
            tail = container.logs().decode("utf-8", errors="replace")[-2000:]
            pytest.skip(f"Artemis broker not ready. Tail:\n{tail}")
        time.sleep(3)
        yield {
            "internal_host": "noaa-swpc-l1-amqp-e2e-broker",
            "internal_port": 5672,
            "host_port": host_port,
            "network": network.name,
            "user": ARTEMIS_USER,
            "password": ARTEMIS_PASSWORD,
            "queue": SWPC_QUEUE_NAME,
        }
    finally:
        if container is not None:
            try: container.kill()
            except docker.errors.APIError: pass
        try: network.remove()
        except docker.errors.APIError: pass


class TestNoaaSwpcL1AmqpArtemisFlow:
    """End-to-end: SWPC L1 feeder pushes CloudEvents + partition annotation."""

    def test_emits_cloudevents_with_partition_key(self, artemis_broker_swpc, noaa_swpc_l1_amqp_image):
        client = docker.from_env()
        feeder = client.containers.run(
            noaa_swpc_l1_amqp_image.id,
            detach=True, remove=False,
            network=artemis_broker_swpc["network"],
            environment={
                "AMQP_HOST": artemis_broker_swpc["internal_host"],
                "AMQP_PORT": str(artemis_broker_swpc["internal_port"]),
                "AMQP_ADDRESS": artemis_broker_swpc["queue"],
                "AMQP_USERNAME": artemis_broker_swpc["user"],
                "AMQP_PASSWORD": artemis_broker_swpc["password"],
                "AMQP_AUTH_MODE": "password",
                "POLLING_INTERVAL": "60",
                "BACKFILL_MINUTES": "1440",
                "ONCE_MODE": "true",
                "PYTHONUNBUFFERED": "1",
            },
        )
        try:
            result = feeder.wait(timeout=600)
            logs = feeder.logs().decode("utf-8", errors="replace")
            assert result.get("StatusCode") == 0, (
                f"Feeder exited non-zero: {result}\n--- LOGS (last 4KB) ---\n{logs[-4000:]}"
            )
        finally:
            try: feeder.remove(force=True)
            except docker.errors.APIError: pass
        messages = _receive_messages(
            "127.0.0.1",
            artemis_broker_swpc["host_port"],
            artemis_broker_swpc["queue"],
            artemis_broker_swpc["user"],
            artemis_broker_swpc["password"],
            expected=2000,
            timeout=60,
        )
        assert messages, "No AMQP messages received from Artemis"
        # All messages should be PropagatedSolarWind
        types: Dict[str, List[Any]] = {}
        for m in messages:
            ce = _extract_ce_attrs(m)
            t = ce.get("type")
            if t:
                types.setdefault(t, []).append((m, ce))
        assert "gov.noaa.swpc.l1.PropagatedSolarWind" in types, (
            f"No PropagatedSolarWind events. Types seen: {sorted(types.keys())}"
        )
        # Subject = {spacecraft} (currently 'dscovr')
        sample_msg, sample_ce = types["gov.noaa.swpc.l1.PropagatedSolarWind"][0]
        for required in ("id", "source", "type", "subject", "specversion"):
            assert required in sample_ce, f"Missing CE attribute {required!r}: {sample_ce}"
        assert sample_ce["specversion"] == "1.0"
        assert sample_ce["subject"] in ("dscovr", "ace")

        # ----- Partition key annotation verification -----
        # The bridge wraps every send to stamp x-opt-partition-key into
        # the AMQP message annotations. This is the default partitioning
        # for all new sources (Service Bus PartitionKey / Event Hubs
        # partition selector).
        annotations = getattr(sample_msg, "annotations", None) or {}
        anno_map: Dict[str, Any] = {}
        try:
            for k, v in dict(annotations).items():
                key = k if isinstance(k, str) else (k.name if hasattr(k, "name") else str(k))
                anno_map[key] = v
        except Exception:  # pylint: disable=broad-except
            pass
        pk = anno_map.get("x-opt-partition-key")
        assert pk is not None, (
            f"x-opt-partition-key annotation missing. Annotations seen: {list(anno_map.keys())}"
        )
        if isinstance(pk, (bytes, bytearray)):
            pk = pk.decode("utf-8", errors="replace")
        assert pk == sample_ce["subject"], (
            f"x-opt-partition-key {pk!r} != CE subject {sample_ce['subject']!r}"
        )
        # Validate JsonStructure schema for the body
        xreg_path = os.path.join(REPO_ROOT, 'feeders', "noaa-swpc-l1", "xreg", "noaa_swpc_l1.xreg.json")
        with open(xreg_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
        schemagroup = manifest["schemagroups"]["gov.noaa.swpc.l1.jstruct"]
        schemas: Dict[str, Dict[str, Any]] = {}
        for full_name, schema in schemagroup["schemas"].items():
            schemas[full_name] = schema["versions"]["1"]["schema"]
        from json_structure import InstanceValidator, SchemaValidator
        validator_factory = SchemaValidator(extended=True)
        schema = schemas["gov.noaa.swpc.l1.PropagatedSolarWind"]
        assert not validator_factory.validate(schema), "Invalid JsonStructure schema"
        body = _body_to_obj(sample_msg)
        assert isinstance(body, dict), f"body not a JSON object: {body!r}"
        errors = InstanceValidator(schema, extended=True).validate_instance(body)
        assert not errors, f"JsonStructure validation failed: {errors[:3]}"