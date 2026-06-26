"""Docker E2E smoke test for MQTT over TLS.

Generates a self-signed CA and server certificate, starts Mosquitto with
TLS on port 8883, runs the pegelonline-mqtt feeder with MQTT_TLS=true,
and verifies that retained MQTT 5 publishes arrive over the encrypted
connection.

This validates the TLS code path that is otherwise untested by the
plain-text ``test_docker_mqtt_flow.py`` suite.
"""

from __future__ import annotations

import datetime
import ipaddress
import json
import os
import socket
import ssl
import time
from contextlib import closing
from typing import Any, Dict, List

import docker
import paho.mqtt.client as mqtt
import pytest
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from .helpers import REPO_ROOT, build_image

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def _generate_certs(tmpdir: str) -> Dict[str, str]:
    """Generate a self-signed CA and server cert using the cryptography library."""
    if not HAS_CRYPTOGRAPHY:
        pytest.skip('cryptography package not installed; cannot generate TLS certs')

    ca_key_path = os.path.join(tmpdir, 'ca.key')
    ca_crt_path = os.path.join(tmpdir, 'ca.crt')
    srv_key_path = os.path.join(tmpdir, 'server.key')
    srv_crt_path = os.path.join(tmpdir, 'server.crt')

    # Generate CA key and self-signed cert
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'TestCA')])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )

    # Generate server key and cert signed by CA
    srv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    srv_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')])
    srv_cert = (
        x509.CertificateBuilder()
        .subject_name(srv_name)
        .issuer_name(ca_name)
        .public_key(srv_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=1))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName('localhost'),
                x509.DNSName('mqtt-tls-broker'),
                x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
            ]),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    # Write PEM files
    with open(ca_key_path, 'wb') as f:
        f.write(ca_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
    with open(ca_crt_path, 'wb') as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
    with open(srv_key_path, 'wb') as f:
        f.write(srv_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
    with open(srv_crt_path, 'wb') as f:
        f.write(srv_cert.public_bytes(serialization.Encoding.PEM))

    return {
        'ca_crt': ca_crt_path,
        'srv_key': srv_key_path,
        'srv_crt': srv_crt_path,
    }


@pytest.fixture(scope='module')
def pegelonline_mqtt_image():
    return build_image('pegelonline', dockerfile='Dockerfile.mqtt', tag='test-pegelonline-mqtt-tls')


@pytest.fixture()
def mosquitto_tls_container(tmp_path_factory):
    """Start Mosquitto 2.x with TLS on the default bridge network."""
    tmpdir = str(tmp_path_factory.mktemp('mqtt_tls_certs'))

    try:
        certs = _generate_certs(tmpdir)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        pytest.skip(f'openssl not available or cert generation failed: {e}')

    client = docker.from_env()
    host_port = _find_free_port()

    # Mosquitto TLS config
    mosquitto_conf = (
        'listener 8883\n'
        'allow_anonymous true\n'
        'cafile /certs/ca.crt\n'
        'certfile /certs/server.crt\n'
        'keyfile /certs/server.key\n'
    )
    conf_path = os.path.join(tmpdir, 'mosquitto.conf')
    with open(conf_path, 'w') as f:
        f.write(mosquitto_conf)

    container = client.containers.run(
        'eclipse-mosquitto:2',
        detach=True,
        remove=True,
        name='mqtt-tls-broker',
        ports={'8883/tcp': host_port},
        volumes={
            certs['ca_crt']: {'bind': '/certs/ca.crt', 'mode': 'ro'},
            certs['srv_crt']: {'bind': '/certs/server.crt', 'mode': 'ro'},
            certs['srv_key']: {'bind': '/certs/server.key', 'mode': 'ro'},
            conf_path: {'bind': '/mosquitto/config/mosquitto.conf', 'mode': 'ro'},
        },
    )
    container.reload()

    # Wait for TLS listener
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            ctx = ssl.create_default_context(cafile=certs['ca_crt'])
            with closing(socket.create_connection(('127.0.0.1', host_port), timeout=2)) as sock:
                with ctx.wrap_socket(sock, server_hostname='localhost'):
                    break
        except (OSError, ssl.SSLError):
            time.sleep(0.5)
    else:
        logs = container.logs().decode('utf-8', errors='replace')
        try:
            container.kill()
        except Exception:
            pass
        pytest.skip(f'Mosquitto TLS broker did not start.\nLogs: {logs}')

    try:
        yield {
            'host_port': host_port,
            'internal_host': '127.0.0.1',
            'internal_port': host_port,
            'ca_crt': certs['ca_crt'],
        }
    finally:
        try:
            container.kill()
        except docker.errors.APIError:
            pass
        pass


def _collect_tls_messages(host: str, port: int, ca_crt: str, timeout: float = 25.0) -> List[Dict[str, Any]]:
    """Subscribe over TLS and collect retained messages."""
    collected: List[Dict[str, Any]] = []
    last_msg_time = [time.time()]
    connected = [False]

    def on_connect(client, userdata, flags, rc, properties=None):
        connected[0] = True
        client.subscribe('hydro/de/wsv/pegelonline/#', qos=1)

    def on_message(_client, _userdata, msg):
        last_msg_time[0] = time.time()
        props = {}
        if msg.properties is not None:
            for k, v in getattr(msg.properties, 'UserProperty', []) or []:
                props[k] = v
            ct = getattr(msg.properties, 'ContentType', None)
            if ct:
                props['_contenttype'] = ct
        try:
            payload = json.loads(msg.payload)
        except (TypeError, ValueError):
            payload = None
        collected.append({
            'topic': msg.topic,
            'retain': bool(msg.retain),
            'qos': msg.qos,
            'user_properties': props,
            'payload': payload,
        })

    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    client.tls_set(ca_certs=ca_crt)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, 30)
    client.loop_start()
    try:
        deadline = time.time() + timeout
        idle_threshold = 3.0
        while time.time() < deadline:
            time.sleep(0.5)
            if collected and time.time() - last_msg_time[0] > idle_threshold:
                break
    finally:
        client.loop_stop()
        client.disconnect()
    return collected


class TestMqttTlsFlow:
    """Verify the pegelonline-mqtt feeder works over TLS."""

    def test_publishes_over_tls(self, mosquitto_tls_container, pegelonline_mqtt_image):
        """Feeder connects via mqtts:// and publishes retained messages over TLS."""
        docker_client = docker.from_env()
        broker_url = f"mqtts://{mosquitto_tls_container['internal_host']}:{mosquitto_tls_container['internal_port']}"

        # Build a combined CA bundle: system certs + our self-signed CA
        # so the feeder can reach both the upstream HTTPS API and our broker
        ca_crt_path = mosquitto_tls_container['ca_crt']
        combined_ca_path = os.path.join(os.path.dirname(ca_crt_path), 'combined-ca.crt')
        import certifi
        with open(certifi.where(), 'r') as sys_ca, open(ca_crt_path, 'r') as our_ca:
            combined = sys_ca.read() + '\n' + our_ca.read()
        with open(combined_ca_path, 'w') as f:
            f.write(combined)

        # Mount the combined CA and run the feeder
        feeder = docker_client.containers.run(
            pegelonline_mqtt_image.id,
            detach=True,
            remove=False,
            network_mode='host',
            environment={
                'MQTT_BROKER_URL': broker_url,
                'MQTT_TLS': 'true',
                'POLLING_INTERVAL': '60',
                'ONCE_MODE': 'true',
                'PYTHONUNBUFFERED': '1',
                'SSL_CERT_FILE': '/certs/combined-ca.crt',
                'REQUESTS_CA_BUNDLE': '/certs/combined-ca.crt',
            },
            volumes={
                combined_ca_path: {'bind': '/certs/combined-ca.crt', 'mode': 'ro'},
            },
        )
        try:
            result = feeder.wait(timeout=300)
            logs = feeder.logs().decode('utf-8', errors='replace')
            assert result.get('StatusCode') == 0, (
                f"Feeder exited non-zero over TLS: {result}\n--- LOGS ---\n{logs}"
            )
        finally:
            try:
                feeder.remove(force=True)
            except docker.errors.APIError:
                pass

        # Collect retained messages over TLS from the subscriber side
        # (messages are retained so they persist after the feeder exits)
        messages = _collect_tls_messages(
            '127.0.0.1',
            mosquitto_tls_container['host_port'],
            mosquitto_tls_container['ca_crt'],
            timeout=15.0,
        )
        assert messages, 'No retained messages received over TLS connection'

        info_msgs = [m for m in messages if m['topic'].endswith('/info')]
        level_msgs = [m for m in messages if m['topic'].endswith('/water-level')]
        assert info_msgs, 'No /info reference events published over TLS'
        assert level_msgs, 'No /water-level telemetry events published over TLS'

        # Verify CloudEvents user properties are present
        for sample in (info_msgs[0], level_msgs[0]):
            up = sample['user_properties']
            for required in ('id', 'source', 'type', 'subject', 'time', 'specversion'):
                assert required in up, f"missing CE attribute {required} on {sample['topic']}: {up}"
            assert sample['user_properties'].get('_contenttype') == 'application/json'
            assert sample['retain'] is True
            assert sample['qos'] == 1
