"""Docker E2E test for the pegelonline AMQP feeder against Azure Service Bus emulator.

Spins up the official Azure Service Bus emulator (which requires an Azure SQL
Edge sidecar) and runs the ``pegelonline-amqp`` image against it in
``--once`` mode, then drains the queue with a Qpid Proton blocking receiver
and validates emitted CloudEvents against the checked-in JsonStructure
schemas.

This test is **opt-in**: it is skipped unless ``AMQP_SB_EMULATOR_E2E=1`` is
set, because:

* The SB emulator image is large (~1 GB total with sql-edge) and slow to pull.
* SQL Edge is Linux-only, so this test will not run on Windows runners.
* The emulator EULA must be accepted (``ACCEPT_EULA=Y``).

Run locally with::

    AMQP_SB_EMULATOR_E2E=1 pytest tests/docker_e2e/test_docker_amqp_servicebus_flow.py -v
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

SB_EMULATOR_IMAGE = "mcr.microsoft.com/azure-messaging/servicebus-emulator:latest"
SQL_EDGE_IMAGE = "mcr.microsoft.com/azure-sql-edge:latest"
EMULATOR_KEY = "SAS_KEY_VALUE"
EMULATOR_KEY_NAME = "RootManageSharedAccessKey"
QUEUE_NAME = "pegelonline"

CONFIG_JSON = {
    "UserConfig": {
        "Namespaces": [
            {
                "Name": "sbemulatorns",
                "Queues": [
                    {
                        "Name": QUEUE_NAME,
                        "Properties": {
                            "DeadLetteringOnMessageExpiration": False,
                            "DefaultMessageTimeToLive": "PT1H",
                            "DuplicateDetectionHistoryTimeWindow": "PT20S",
                            "ForwardDeadLetteredMessagesTo": "",
                            "ForwardTo": "",
                            "LockDuration": "PT1M",
                            "MaxDeliveryCount": 10,
                            "RequiresDuplicateDetection": False,
                            "RequiresSession": False,
                        },
                    }
                ],
                "Topics": [],
            }
        ],
        "Logging": {"Type": "File"},
    }
}


pytestmark = pytest.mark.skipif(
    os.getenv("AMQP_SB_EMULATOR_E2E") not in ("1", "true", "yes"),
    reason="set AMQP_SB_EMULATOR_E2E=1 to run the Service Bus emulator E2E test",
)


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _generate_sas_token(uri: str, key: str, key_name: str, ttl: int = 3600) -> str:
    encoded_uri = urllib.parse.quote_plus(uri)
    expiry = int(time.time() + ttl)
    string_to_sign = f"{encoded_uri}\n{expiry}"
    signed = hmac.new(
        key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    signature = urllib.parse.quote_plus(base64.b64encode(signed))
    return (
        f"SharedAccessSignature sr={encoded_uri}&sig={signature}"
        f"&se={expiry}&skn={key_name}"
    )


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
def sb_emulator():
    """Start sql-edge + servicebus-emulator on a private docker network."""
    client = docker.from_env()
    network = client.networks.create("pegelonline-amqp-sb-e2e", driver="bridge")
    sa_password = "Strong!Passw0rd"
    sql = None
    sb = None
    amqp_host_port = _find_free_port()

    # Write Config.json to a tmp file mounted into the emulator container
    config_dir = os.path.join(REPO_ROOT, "tests", "docker_e2e", ".sb-emulator-tmp")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "Config.json")
    with open(config_path, "w", encoding="utf-8") as fh:
        json.dump(CONFIG_JSON, fh, indent=2)

    try:
        sql = client.containers.run(
            SQL_EDGE_IMAGE,
            name="pegelonline-amqp-sb-e2e-sql",
            detach=True,
            remove=True,
            network=network.name,
            environment={
                "ACCEPT_EULA": "Y",
                "MSSQL_SA_PASSWORD": sa_password,
            },
        )
        # Wait for SQL Edge to be ready
        deadline = time.time() + 90
        while time.time() < deadline:
            logs = sql.logs().decode("utf-8", errors="replace")
            if "Recovery is complete" in logs or "SQL Server is now ready" in logs:
                break
            time.sleep(2)

        sb = client.containers.run(
            SB_EMULATOR_IMAGE,
            name="pegelonline-amqp-sb-e2e-broker",
            detach=True,
            remove=True,
            network=network.name,
            ports={"5672/tcp": amqp_host_port},
            environment={
                "ACCEPT_EULA": "Y",
                "SQL_SERVER": "pegelonline-amqp-sb-e2e-sql",
                "MSSQL_SA_PASSWORD": sa_password,
            },
            volumes={config_path: {"bind": "/ServiceBus_Emulator/ConfigFiles/Config.json", "mode": "ro"}},
        )

        # Wait for AMQP listener
        deadline = time.time() + 60
        while time.time() < deadline:
            try:
                with closing(socket.create_connection(("127.0.0.1", amqp_host_port), timeout=1)):
                    break
            except OSError:
                time.sleep(1)
        else:
            pytest.skip("Service Bus emulator did not start listening on 5672")

        # Wait extra for emulator to fully load Config.json
        time.sleep(8)

        yield {
            "internal_host": "pegelonline-amqp-sb-e2e-broker",
            "internal_port": 5672,
            "host_port": amqp_host_port,
            "network": network.name,
            "key": EMULATOR_KEY,
            "key_name": EMULATOR_KEY_NAME,
            "queue": QUEUE_NAME,
        }
    finally:
        for c in (sb, sql):
            if c is None:
                continue
            try:
                c.kill()
            except docker.errors.APIError:
                pass
        try:
            network.remove()
        except docker.errors.APIError:
            pass


def _receive_messages(host: str, port: int, queue: str, sas_token: str, expected: int, timeout: float = 60.0) -> List[Any]:
    """Drain *expected* messages from *queue* using proton blocking receiver."""
    from proton import Url
    from proton.utils import BlockingConnection

    url = Url(f"amqp://{urllib.parse.quote(EMULATOR_KEY_NAME, safe='')}:{urllib.parse.quote(sas_token, safe='')}@{host}:{port}")
    conn = BlockingConnection(str(url), allowed_mechs="PLAIN")
    receiver = conn.create_receiver(queue)
    messages = []
    deadline = time.time() + timeout
    try:
        while len(messages) < expected and time.time() < deadline:
            remaining = max(1.0, deadline - time.time())
            try:
                msg = receiver.receive(timeout=min(remaining, 5.0))
            except Exception:
                break
            messages.append(msg)
            receiver.accept()
    finally:
        try:
            conn.close()
        except Exception:  # pylint: disable=broad-except
            pass
    return messages


class TestPegelonlineAmqpSbEmulatorFlow:
    """Verify the pegelonline-amqp container delivers CloudEvents to Service Bus."""

    def test_emits_cloudevents_to_servicebus_queue(self, sb_emulator, pegelonline_amqp_image):
        client = docker.from_env()
        sas_internal = _generate_sas_token(
            f"sb://{sb_emulator['internal_host']}/{sb_emulator['queue']}",
            sb_emulator["key"],
            sb_emulator["key_name"],
        )
        broker_url = (
            f"amqp://{urllib.parse.quote(sb_emulator['key_name'], safe='')}:"
            f"{urllib.parse.quote(sas_internal, safe='')}@"
            f"{sb_emulator['internal_host']}:{sb_emulator['internal_port']}/{sb_emulator['queue']}"
        )

        feeder = client.containers.run(
            pegelonline_amqp_image.id,
            detach=True,
            remove=False,
            network=sb_emulator["network"],
            environment={
                "AMQP_BROKER_URL": broker_url,
                "AMQP_ADDRESS": sb_emulator["queue"],
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
                f"Feeder exited non-zero: {result}\n--- LOGS ---\n{logs}"
            )
        finally:
            try:
                feeder.remove(force=True)
            except docker.errors.APIError:
                pass

        sas_external = _generate_sas_token(
            f"sb://localhost/{sb_emulator['queue']}",
            sb_emulator["key"],
            sb_emulator["key_name"],
        )
        messages = _receive_messages(
            "127.0.0.1",
            sb_emulator["host_port"],
            sb_emulator["queue"],
            sas_external,
            expected=2,
            timeout=60,
        )
        assert messages, "No AMQP messages received from emulator queue"

        # Parse CloudEvents — bridge runs in binary mode by default, so CE
        # attributes ride as message properties / application_properties.
        types_seen = set()
        for msg in messages:
            props = dict(getattr(msg, "properties", {}) or {})
            app_props = dict(getattr(msg, "application_properties", {}) or {})
            merged = {**app_props, **props}
            ce_type = merged.get("type") or merged.get("ce-type") or merged.get("cloudEvents:type")
            if ce_type:
                types_seen.add(ce_type)

        assert "de.wsv.pegelonline.Station" in types_seen, (
            f"Expected Station events, saw types: {types_seen}"
        )
