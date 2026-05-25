"""Docker E2E coverage for AMQP companion feeders added after PegelOnline."""

from __future__ import annotations

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
