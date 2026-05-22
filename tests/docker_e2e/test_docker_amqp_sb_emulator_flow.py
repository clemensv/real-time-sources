"""Docker E2E test for the pegelonline AMQP 1.0 feeder against the
Azure Service Bus emulator (``mcr.microsoft.com/azure-messaging/servicebus-emulator``).

**Status: currently skipped.** The Service Bus emulator authenticates
exclusively via the AMQP CBS link with a SAS-token put-token
(``type=servicebus.windows.net:sastoken``). The xrcg-generated Python AMQP
producer currently only supports JWT-bearer CBS (``type=jwt``) — see
xregistry/codegen#290. Once that ships, the ``@pytest.mark.skip`` decorator
below should be removed.

The fixture infrastructure is kept in place so the test is ready to run
the moment the upstream gap closes. It is also useful as a working
testcontainers reference for the Azure Service Bus emulator.

Topology:

* MSSQL 2022 container (``mcr.microsoft.com/mssql/server``) — required
  state store for the emulator.
* SB emulator container — connects to MSSQL by name, mounts a Config.json
  that pre-declares the ``pegelonline`` queue under namespace
  ``sbemulatorns``.
* Pegelonline AMQP feeder container — runs in ``--once`` mode against the
  emulator over plain AMQP 1.0 (no TLS).
* ``azure-servicebus`` SDK receiver on the host drains the queue and
  validates CloudEvents wire format + JsonStructure schemas.

Run with::

    pytest tests/docker_e2e/test_docker_amqp_sb_emulator_flow.py -v -s
"""

from __future__ import annotations

import json
import os
import socket
import tempfile
import time
from contextlib import closing
from typing import Any, Dict, List

import docker
import pytest

from .helpers import REPO_ROOT, build_image

MSSQL_IMAGE = "mcr.microsoft.com/mssql/server:2022-latest"
SBEMU_IMAGE = "mcr.microsoft.com/azure-messaging/servicebus-emulator:latest"
SA_PASSWORD = "P@ssw0rd!Strong"
QUEUE_NAME = "pegelonline"
NAMESPACE_NAME = "sbemulatorns"
# The emulator ships with a well-known SAS key for the
# RootManageSharedAccessKey rule; this matches the value documented in
# Microsoft's emulator README / Microsoft.ServiceBus.Emulator sample.
SAS_KEY_NAME = "RootManageSharedAccessKey"
SAS_KEY_VALUE = "SAS_KEY_VALUE"

EMULATOR_CONFIG = {
    "UserConfig": {
        "Namespaces": [
            {
                "Name": NAMESPACE_NAME,
                "Queues": [
                    {
                        "Name": QUEUE_NAME,
                        "Properties": {
                            "DeadLetteringOnMessageExpiration": False,
                            "DefaultMessageTimeToLive": "PT1H",
                            "DuplicateDetectionHistoryTimeWindow": "PT20S",
                            "EnableBatchedOperations": True,
                            "EnableExpress": False,
                            "EnablePartitioning": False,
                            "ForwardDeadLetteredMessagesTo": "",
                            "ForwardTo": "",
                            "LockDuration": "PT1M",
                            "MaxDeliveryCount": 10,
                            "MaxMessageSizeInKilobytes": 256,
                            "MaxSizeInMegabytes": 1024,
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
def sb_emulator():
    """Spin up MSSQL + SB emulator on a shared bridge network."""
    client = docker.from_env()
    network = client.networks.create("pegelonline-sbemu-e2e", driver="bridge")
    host_port = _find_free_port()
    mssql_container = None
    emu_container = None
    config_dir = tempfile.mkdtemp(prefix="sbemu-config-")
    config_path = os.path.join(config_dir, "Config.json")
    with open(config_path, "w", encoding="utf-8") as fh:
        json.dump(EMULATOR_CONFIG, fh, indent=2)
    try:
        mssql_container = client.containers.run(
            MSSQL_IMAGE,
            name="pegelonline-sbemu-e2e-mssql",
            detach=True,
            remove=True,
            network=network.name,
            environment={
                "ACCEPT_EULA": "Y",
                "MSSQL_SA_PASSWORD": SA_PASSWORD,
            },
        )
        # Wait for SQL Server to come up before launching the emulator
        deadline = time.time() + 120
        ready = False
        while time.time() < deadline:
            logs = mssql_container.logs().decode("utf-8", errors="replace")
            if "SQL Server is now ready for client connections" in logs:
                ready = True
                break
            time.sleep(2)
        if not ready:
            pytest.skip("MSSQL container did not become ready in 120s")

        emu_container = client.containers.run(
            SBEMU_IMAGE,
            name="pegelonline-sbemu-e2e-emu",
            detach=True,
            remove=True,
            network=network.name,
            ports={"5672/tcp": host_port},
            environment={
                "ACCEPT_EULA": "Y",
                "SQL_SERVER": "pegelonline-sbemu-e2e-mssql",
                "MSSQL_SA_PASSWORD": SA_PASSWORD,
            },
            volumes={
                config_path: {
                    "bind": "/ServiceBus_Emulator/ConfigFiles/Config.json",
                    "mode": "ro",
                }
            },
        )

        deadline = time.time() + 120
        ready = False
        while time.time() < deadline:
            try:
                with closing(socket.create_connection(("127.0.0.1", host_port), timeout=1)):
                    ready = True
                    break
            except OSError:
                pass
            time.sleep(2)
        if not ready:
            tail = emu_container.logs().decode("utf-8", errors="replace")[-2000:]
            pytest.skip(f"SB emulator not ready. Tail:\n{tail}")
        time.sleep(3)

        yield {
            "internal_host": "pegelonline-sbemu-e2e-emu",
            "internal_port": 5672,
            "host_port": host_port,
            "network": network.name,
            "namespace": NAMESPACE_NAME,
            "queue": QUEUE_NAME,
            "sas_key_name": SAS_KEY_NAME,
            "sas_key_value": SAS_KEY_VALUE,
        }
    finally:
        for c in (emu_container, mssql_container):
            if c is not None:
                try:
                    c.kill()
                except docker.errors.APIError:
                    pass
        try:
            network.remove()
        except docker.errors.APIError:
            pass
        try:
            os.remove(config_path)
            os.rmdir(config_dir)
        except OSError:
            pass


def _receive_via_sdk(host_port: int, queue: str, sas_key_name: str, sas_key_value: str,
                     expected: int, timeout: float = 60.0) -> List[Any]:
    """Drain *queue* using the azure-servicebus SDK (which speaks AMQP+SAS
    natively against the emulator)."""
    from azure.servicebus import ServiceBusClient

    conn_str = (
        f"Endpoint=sb://localhost:{host_port};"
        f"SharedAccessKeyName={sas_key_name};"
        f"SharedAccessKey={sas_key_value};"
        "UseDevelopmentEmulator=true"
    )
    received: List[Any] = []
    deadline = time.time() + timeout
    with ServiceBusClient.from_connection_string(conn_str) as client:
        with client.get_queue_receiver(queue) as receiver:
            while len(received) < expected and time.time() < deadline:
                batch = receiver.receive_messages(max_message_count=200, max_wait_time=5)
                if not batch:
                    if received:
                        break
                    continue
                for msg in batch:
                    received.append(msg)
                    receiver.complete_message(msg)
    return received


@pytest.mark.skip(
    reason=(
        "Blocked on xregistry/codegen#290: generated AMQP producer's CBS "
        "handshake only supports type=jwt, but Service Bus emulator requires "
        "type=servicebus.windows.net:sastoken. Remove this skip once xrcg "
        "ships SAS-token CBS support."
    )
)
class TestPegelonlineAmqpSbEmulatorFlow:
    """End-to-end: feeder pushes CloudEvents to Service Bus emulator over AMQP 1.0."""

    def test_emits_cloudevents_to_sb_emulator_queue(self, sb_emulator, pegelonline_amqp_image):
        client = docker.from_env()

        # Once xrcg #290 lands, the feeder will accept a SAS connection
        # string via AMQP_CONNECTION_STRING or equivalent. The exact env
        # shape depends on the xrcg template surface chosen — placeholder
        # values below mirror the SDK conn-string format for the emulator.
        feeder = client.containers.run(
            pegelonline_amqp_image.id,
            detach=True,
            remove=False,
            network=sb_emulator["network"],
            environment={
                "AMQP_HOST": sb_emulator["internal_host"],
                "AMQP_PORT": str(sb_emulator["internal_port"]),
                "AMQP_ADDRESS": sb_emulator["queue"],
                "AMQP_AUTH_MODE": "sas",  # NEW: post-#290 template surface
                "AMQP_SAS_KEY_NAME": sb_emulator["sas_key_name"],
                "AMQP_SAS_KEY": sb_emulator["sas_key_value"],
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

        messages = _receive_via_sdk(
            sb_emulator["host_port"],
            sb_emulator["queue"],
            sb_emulator["sas_key_name"],
            sb_emulator["sas_key_value"],
            expected=5000,
            timeout=60,
        )
        assert messages, "No AMQP messages received from SB emulator"

        # The azure-servicebus SDK exposes CE binary-mode attributes via
        # ``application_properties`` (already-decoded dict). Bucket by type.
        types: Dict[str, List[Any]] = {}
        for m in messages:
            app_props = dict(m.application_properties or {})
            t = app_props.get(b"cloudEvents:type") or app_props.get("cloudEvents:type")
            if isinstance(t, bytes):
                t = t.decode("utf-8", errors="replace")
            if t:
                types.setdefault(t, []).append((m, app_props))

        assert "de.wsv.pegelonline.Station" in types, (
            f"No Station events. Types seen: {sorted(types.keys())}"
        )
        assert "de.wsv.pegelonline.CurrentMeasurement" in types, (
            f"No CurrentMeasurement events. Types seen: {sorted(types.keys())}"
        )

        schemas = _load_schemas()
        from json_structure import InstanceValidator, SchemaValidator
        validator_factory = SchemaValidator(extended=True)
        for ce_type, items in types.items():
            if ce_type not in schemas:
                continue
            sample_msg, _ = items[0]
            body_bytes = b"".join(sample_msg.body) if hasattr(sample_msg.body, "__iter__") else sample_msg.body
            if isinstance(body_bytes, (bytes, bytearray)):
                data = json.loads(body_bytes.decode("utf-8"))
            else:
                data = json.loads(body_bytes)
            schema = schemas[ce_type]
            assert not validator_factory.validate(schema), (
                f"Invalid JsonStructure schema for {ce_type}"
            )
            errors = InstanceValidator(schema, extended=True).validate_instance(data)
            assert not errors, f"JsonStructure validation failed for {ce_type}: {errors[:3]}"
