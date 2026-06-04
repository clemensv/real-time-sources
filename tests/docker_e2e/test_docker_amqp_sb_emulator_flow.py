"""Docker E2E test for the pegelonline AMQP 1.0 feeder against the
Azure Service Bus emulator (``mcr.microsoft.com/azure-messaging/servicebus-emulator``).

The Service Bus emulator authenticates exclusively via the AMQP CBS link
with a SAS-token put-token (``type=servicebus.windows.net:sastoken``).
xrcg 0.10.5 added that path to the generated Python AMQP producer
(xregistry/codegen#291), and the pegelonline AMQP feeder exposes it via
``--auth-mode=sas`` / ``AMQP_SAS_KEY_NAME`` + ``AMQP_SAS_KEY``.

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

        deadline = time.time() + 180
        ready = False
        while time.time() < deadline:
            try:
                emu_logs = emu_container.logs().decode("utf-8", errors="replace")
                if "Emulator Service is Successfully Up" in emu_logs:
                    ready = True
                    break
            except docker.errors.APIError:
                pass
            time.sleep(2)
        if not ready:
            tail = emu_container.logs().decode("utf-8", errors="replace")[-2000:]
            pytest.skip(f"SB emulator not ready. Tail:\n{tail}")
        # Even after "Successfully Up", the AMQP listener may need a moment
        # before it accepts the first connection cleanly.
        time.sleep(5)

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


@pytest.mark.docker_e2e
class TestPegelonlineAmqpSbEmulatorFlow:
    """End-to-end: feeder pushes CloudEvents to Service Bus emulator over AMQP 1.0."""

    def test_emits_cloudevents_to_sb_emulator_queue(self, sb_emulator, pegelonline_amqp_image):
        client = docker.from_env()

        # Feeder wired for SAS CBS auth — uses xrcg 0.10.5+ which adds
        # the type=servicebus.windows.net:sastoken CBS path required by
        # the Service Bus emulator.
        feeder = client.containers.run(
            pegelonline_amqp_image.id,
            detach=True,
            remove=False,
            network=sb_emulator["network"],
            environment={
                "AMQP_HOST": sb_emulator["internal_host"],
                "AMQP_PORT": str(sb_emulator["internal_port"]),
                "AMQP_ADDRESS": sb_emulator["queue"],
                "AMQP_AUTH_MODE": "sas",
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


# ---------------------------------------------------------------------------
# AMQP companion backfill feeders (mock-mode, Service Bus emulator)
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


def _load_source_schemas_sb(source_dir: str) -> Dict[str, Dict[str, Any]]:
    xreg_dir = os.path.join(REPO_ROOT, 'feeders', source_dir, "xreg")
    xreg_name = next(n for n in os.listdir(xreg_dir) if n.endswith(".xreg.json"))
    with open(os.path.join(xreg_dir, xreg_name), "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    schemagroup = next(v for k, v in manifest["schemagroups"].items() if k.endswith(".jstruct"))
    return {name: schema["versions"]["1"]["schema"] for name, schema in schemagroup["schemas"].items()}


def _run_generic_amqp_sb_flow(source_dir: str, image_tag: str, station_type: str, telemetry_type: str) -> None:
    queue = source_dir
    client = docker.from_env()
    image = build_image(source_dir, dockerfile="Dockerfile.amqp", tag=image_tag)
    network = client.networks.create(f"{source_dir}-sbemu-e2e", driver="bridge")
    host_port = _find_free_port()
    mssql_container = None
    emu_container = None
    config_dir = tempfile.mkdtemp(prefix=f"{source_dir}-sbemu-config-")
    config_path = os.path.join(config_dir, "Config.json")
    config = {"UserConfig": {"Namespaces": [{"Name": NAMESPACE_NAME, "Queues": [{"Name": queue, "Properties": {"DeadLetteringOnMessageExpiration": False, "DefaultMessageTimeToLive": "PT1H", "DuplicateDetectionHistoryTimeWindow": "PT20S", "EnableBatchedOperations": True, "EnableExpress": False, "EnablePartitioning": False, "ForwardDeadLetteredMessagesTo": "", "ForwardTo": "", "LockDuration": "PT1M", "MaxDeliveryCount": 10, "MaxMessageSizeInKilobytes": 256, "MaxSizeInMegabytes": 1024, "RequiresDuplicateDetection": False, "RequiresSession": False}}], "Topics": []}], "Logging": {"Type": "File"}}}
    with open(config_path, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)
    try:
        mssql_container = client.containers.run(
            MSSQL_IMAGE,
            name=f"{source_dir}-sbemu-e2e-mssql",
            detach=True,
            remove=True,
            network=network.name,
            environment={"ACCEPT_EULA": "Y", "MSSQL_SA_PASSWORD": SA_PASSWORD},
        )
        deadline = time.time() + 120
        while time.time() < deadline:
            if "SQL Server is now ready for client connections" in mssql_container.logs().decode("utf-8", errors="replace"):
                break
            time.sleep(2)
        else:
            pytest.skip("MSSQL container did not become ready in 120s")
        emu_container = client.containers.run(
            SBEMU_IMAGE,
            name=f"{source_dir}-sbemu-e2e-emu",
            detach=True,
            remove=True,
            network=network.name,
            ports={"5672/tcp": host_port},
            environment={"ACCEPT_EULA": "Y", "SQL_SERVER": f"{source_dir}-sbemu-e2e-mssql", "MSSQL_SA_PASSWORD": SA_PASSWORD},
            volumes={config_path: {"bind": "/ServiceBus_Emulator/ConfigFiles/Config.json", "mode": "ro"}},
        )
        deadline = time.time() + 180
        while time.time() < deadline:
            if "Emulator Service is Successfully Up" in emu_container.logs().decode("utf-8", errors="replace"):
                break
            time.sleep(2)
        else:
            pytest.skip(f"SB emulator not ready. Tail:\n{emu_container.logs().decode('utf-8', errors='replace')[-2000:]}")
        time.sleep(5)
        feeder = client.containers.run(
            image.id,
            detach=True,
            remove=False,
            network=network.name,
            environment={
                "AMQP_HOST": f"{source_dir}-sbemu-e2e-emu",
                "AMQP_PORT": "5672",
                "AMQP_ADDRESS": queue,
                "AMQP_AUTH_MODE": "sas",
                "AMQP_SAS_KEY_NAME": SAS_KEY_NAME,
                "AMQP_SAS_KEY": SAS_KEY_VALUE,
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
        messages = _receive_via_sdk(host_port, queue, SAS_KEY_NAME, SAS_KEY_VALUE, expected=expected_messages, timeout=60)
        assert messages, "No AMQP messages received from SB emulator"
        by_type: Dict[str, List[Any]] = {}
        for message in messages:
            app_props = dict(message.application_properties or {})
            event_type = app_props.get(b"cloudEvents:type") or app_props.get("cloudEvents:type")
            if isinstance(event_type, bytes):
                event_type = event_type.decode("utf-8", errors="replace")
            by_type.setdefault(event_type, []).append(message)
        assert station_type in by_type, sorted(by_type)
        assert telemetry_type in by_type, sorted(by_type)
        schemas = _load_source_schemas_sb(source_dir)
        from json_structure import InstanceValidator, SchemaValidator
        validator_factory = SchemaValidator(extended=True)
        for ce_type in (station_type, telemetry_type):
            sample_msg = by_type[ce_type][0]
            body_bytes = b"".join(sample_msg.body) if hasattr(sample_msg.body, "__iter__") else sample_msg.body
            data = json.loads(body_bytes.decode("utf-8") if isinstance(body_bytes, (bytes, bytearray)) else body_bytes)
            schema = schemas[ce_type]
            assert not validator_factory.validate(schema)
            errors = InstanceValidator(schema, extended=True).validate_instance(data)
            assert not errors, f"JsonStructure validation failed for {ce_type}: {errors[:3]}"
    finally:
        for container in (emu_container, mssql_container):
            if container is not None:
                try:
                    container.kill()
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


@pytest.mark.docker_e2e
class TestBafuHydroAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[0])

@pytest.mark.docker_e2e
class TestChmiHydroAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[1])

@pytest.mark.docker_e2e
class TestGermanWatersAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[2])

@pytest.mark.docker_e2e
class TestNveHydroAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[3])

@pytest.mark.docker_e2e
class TestRwsWaterwebservicesAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[4])

@pytest.mark.docker_e2e
class TestSmhiHydroAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[5])

@pytest.mark.docker_e2e
class TestWalloniaIssepAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[6])

@pytest.mark.docker_e2e
class TestFdsnSeismologyAmqpSbEmulatorFlow:
    def test_emits_cloudevents_to_sb_emulator_queue(self):
        _run_generic_amqp_sb_flow(*HYDRO_AMQP_SOURCES[7])

