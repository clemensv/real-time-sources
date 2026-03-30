"""Shared helpers for Docker end-to-end tests.

These utilities build Docker images, run containers alongside a Kafka
container, and consume messages to verify data flow.
"""

import json
import os
import time
from typing import Dict, List, Optional, Tuple

import docker
from docker.models.containers import Container
from docker.models.images import Image
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from testcontainers.kafka import KafkaContainer


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def build_image(project_dir: str, dockerfile: str = 'Dockerfile', tag: Optional[str] = None) -> Image:
    """Build a Docker image for a project.

    Args:
        project_dir: Directory name relative to repo root (e.g. 'chmi-hydro').
        dockerfile: Dockerfile name within the project directory.
        tag: Image tag.  Defaults to ``test-<project_dir>``.

    Returns:
        The built :class:`docker.models.images.Image`.
    """
    client = docker.from_env()
    build_context = os.path.join(REPO_ROOT, project_dir)
    if tag is None:
        tag = f'test-{project_dir}'
    image, _logs = client.images.build(
        path=build_context,
        dockerfile=dockerfile,
        tag=tag,
        rm=True,
    )
    return image


class KafkaFixture:
    """Manages a Kafka test container for Docker E2E tests.

    Uses ``testcontainers.kafka.KafkaContainer`` for broker lifecycle.
    Application containers reach Kafka via the container's IP on the
    default ``bridge`` network, using the BROKER listener on port 9092
    (PLAINTEXT, no SASL).

    * :pyattr:`external_address` – for the test runner on the host.
    * :pyattr:`internal_address` – for containers on the default bridge.
    """

    def __init__(self) -> None:
        self._docker = docker.from_env()
        self._kafka: Optional[KafkaContainer] = None
        self._kafka_ip: Optional[str] = None

    def start(self) -> 'KafkaFixture':
        self._kafka = KafkaContainer()
        self._kafka.start()
        wrapped = self._kafka.get_wrapped_container()
        wrapped.reload()
        # Get IP on the default bridge network
        net_settings = wrapped.attrs['NetworkSettings']['Networks']
        bridge = net_settings.get('bridge', {})
        self._kafka_ip = bridge.get('IPAddress')
        if not self._kafka_ip:
            # Fallback: grab the first network IP
            first_net = next(iter(net_settings.values()))
            self._kafka_ip = first_net['IPAddress']
        return self

    def stop(self) -> None:
        if self._kafka:
            try:
                self._kafka.stop()
            except Exception:
                pass

    @property
    def external_address(self) -> str:
        """Bootstrap server reachable from the host."""
        return self._kafka.get_bootstrap_server()

    @property
    def internal_address(self) -> str:
        """Bootstrap server reachable from containers on the default bridge.

        Uses the Kafka container's IP on port 9092 (the BROKER listener,
        advertised with PLAINTEXT protocol).
        """
        return f'{self._kafka_ip}:9092'

    def create_topic(self, topic: str, partitions: int = 1) -> None:
        admin = AdminClient({'bootstrap.servers': self.external_address})
        fut = admin.create_topics([NewTopic(topic, num_partitions=partitions, replication_factor=1)])
        for _topic, f in fut.items():
            f.result(timeout=10)
        time.sleep(1)

    def consume_messages(
        self,
        topic: str,
        *,
        min_messages: int = 1,
        timeout: float = 60,
        group_id: str = 'test-consumer',
    ) -> List[bytes]:
        """Consume messages from a topic via the external listener."""
        consumer = Consumer({
            'bootstrap.servers': self.external_address,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe([topic])
        messages: List[bytes] = []
        deadline = time.time() + timeout
        try:
            while time.time() < deadline and len(messages) < min_messages:
                msg = consumer.poll(1.0)
                if msg and not msg.error():
                    messages.append(msg.value())
        finally:
            consumer.close()
        return messages


def run_container(
    image: Image,
    *,
    environment: Optional[Dict[str, str]] = None,
    command: Optional[str] = None,
    timeout: float = 120,
) -> Tuple[int, str]:
    """Run a container and wait for it to finish or timeout.

    Args:
        image: The Docker image to run.
        environment: Environment variables for the container.
        command: Override CMD.
        timeout: Seconds to wait before stopping the container.

    Returns:
        ``(exit_code, logs)`` tuple.  ``exit_code`` is ``-1`` when the
        container was forcefully stopped after *timeout*.
    """
    client = docker.from_env()
    container: Container = client.containers.run(
        image.id,
        command=command,
        environment=environment or {},
        detach=True,
    )
    exit_code = -1
    try:
        result = container.wait(timeout=timeout)
        exit_code = result.get('StatusCode', -1)
    except Exception:
        # Timeout or other error – stop the container
        container.stop(timeout=5)
    logs = container.logs().decode('utf-8', errors='replace')
    container.remove(force=True)
    return exit_code, logs


def run_container_detached(
    image: Image,
    *,
    environment: Optional[Dict[str, str]] = None,
    command: Optional[str] = None,
) -> Container:
    """Run a container in the background.

    Caller is responsible for stopping and removing the container.
    """
    client = docker.from_env()
    container: Container = client.containers.run(
        image.id,
        command=command,
        environment=environment or {},
        detach=True,
    )
    return container


def wait_for_container_logs(
    container: Container,
    pattern: str,
    timeout: float = 120,
) -> str:
    """Wait until *pattern* appears in the container logs or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        logs = container.logs().decode('utf-8', errors='replace')
        if pattern in logs:
            return logs
        time.sleep(2)
    return container.logs().decode('utf-8', errors='replace')


def assert_cloudevents(messages: List[bytes]) -> List[dict]:
    """Parse messages as JSON CloudEvents and assert basic structure."""
    events = []
    for raw in messages:
        event = json.loads(raw)
        assert 'specversion' in event, f'Missing specversion in {event}'
        assert event['specversion'] == '1.0', f'Unexpected specversion: {event["specversion"]}'
        assert 'type' in event, f'Missing type in {event}'
        assert 'source' in event, f'Missing source in {event}'
        events.append(event)
    return events
