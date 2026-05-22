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
    xreg_path = os.path.join(REPO_ROOT, "pegelonline", "xreg", "pegelonline.xreg.json")
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
