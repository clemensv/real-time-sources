"""Shared helpers for Docker end-to-end tests.

These utilities build Docker images, run containers alongside a Kafka
container, and validate emitted CloudEvents against the checked-in
xRegistry Kafka key and JsonStructure schema declarations.
"""

import glob
import json
import os
import re
import time
from base64 import b64encode
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Mapping, Optional, Tuple

import docker
from docker.models.containers import Container
from docker.models.images import Image
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from json_structure import InstanceValidator, SchemaValidator
from testcontainers.kafka import KafkaContainer


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_TEMPLATE_PATTERN = re.compile(r'{([^{}]+)}')
_SCHEMA_VALIDATOR = SchemaValidator(extended=True)
_KAFKA_ARTIFACTS_DIR: Optional[str] = None


@dataclass(frozen=True)
class ConsumedKafkaMessage:
    """Kafka message details captured during Docker E2E validation."""

    key: Optional[bytes]
    value: bytes
    partition: int
    offset: int


def configure_kafka_artifacts_dir(path: Optional[str]) -> None:
    """Enable optional Docker E2E artifact output when a directory is provided."""
    global _KAFKA_ARTIFACTS_DIR
    _KAFKA_ARTIFACTS_DIR = os.path.abspath(path) if path else None


def _sanitize_artifact_name(value: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '-', value).strip('-') or 'artifact'


def _decode_message_value(raw_value: bytes) -> Any:
    try:
        return json.loads(raw_value)
    except (TypeError, ValueError):
        return {
            'encoding': 'base64',
            'data': b64encode(raw_value).decode('ascii'),
        }


def write_kafka_artifacts(
    project_dir: str,
    topic: str,
    records: List[ConsumedKafkaMessage],
    container_logs: str,
) -> None:
    """Persist consumed Kafka messages and container logs when artifact output is enabled."""
    if not _KAFKA_ARTIFACTS_DIR:
        return

    target_dir = os.path.join(_KAFKA_ARTIFACTS_DIR, _sanitize_artifact_name(project_dir))
    os.makedirs(target_dir, exist_ok=True)
    topic_name = _sanitize_artifact_name(topic)

    messages_path = os.path.join(target_dir, f'{topic_name}.messages.jsonl')
    with open(messages_path, 'w', encoding='utf-8') as handle:
        for record in records:
            line = {
                'key': _decode_kafka_key(record.key),
                'partition': record.partition,
                'offset': record.offset,
                'value': _decode_message_value(record.value),
            }
            handle.write(json.dumps(line, ensure_ascii=False, sort_keys=True))
            handle.write('\n')

    logs_path = os.path.join(target_dir, f'{topic_name}.container.log')
    with open(logs_path, 'w', encoding='utf-8') as handle:
        handle.write(container_logs)


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


def project_dir_from_image(image: Image) -> str:
    """Infer the project directory from the test image tag."""
    if not image.tags:
        raise AssertionError('Test image has no tags; cannot resolve project directory')

    tag = image.tags[0].split(':', 1)[0]
    if not tag.startswith('test-'):
        raise AssertionError(f'Unexpected test image tag: {tag}')
    return tag[len('test-'):]


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


def _decode_kafka_key(raw_key: Optional[bytes]) -> Optional[str]:
    if raw_key is None:
        return None
    return raw_key.decode('utf-8', errors='replace')


def _resolve_json_pointer(document: Dict[str, Any], pointer: str) -> Any:
    if not pointer.startswith('#/'):
        raise AssertionError(f'Unsupported local schema reference: {pointer}')

    current: Any = document
    for raw_token in pointer[2:].split('/'):
        token = raw_token.replace('~1', '/').replace('~0', '~')
        current = current[token]
    return current


def _render_template(template: str, context: Mapping[str, Any]) -> str:
    missing: List[str] = []

    def _replace(match: re.Match[str]) -> str:
        field_name = match.group(1)
        value = context.get(field_name)
        if value is None:
            missing.append(field_name)
            return match.group(0)
        if isinstance(value, (dict, list)):
            raise AssertionError(
                f'Template placeholder {field_name!r} resolved to a non-scalar value'
            )
        return str(value)

    rendered = _TEMPLATE_PATTERN.sub(_replace, template)
    if missing:
        raise AssertionError(
            f'Could not resolve template {template!r}; missing fields: {sorted(set(missing))}'
        )
    return rendered


@lru_cache(maxsize=None)
def _find_xreg_file(project_dir: str) -> str:
    pattern = os.path.join(REPO_ROOT, project_dir, 'xreg', '*.xreg.json')
    matches = sorted(glob.glob(pattern))
    if len(matches) != 1:
        raise AssertionError(
            f'Expected exactly one xreg manifest under {project_dir!r}, found {matches}'
        )
    return matches[0]


@lru_cache(maxsize=None)
def _load_project_contract(project_dir: str) -> Dict[str, Dict[str, Any]]:
    xreg_path = _find_xreg_file(project_dir)
    with open(xreg_path, 'r', encoding='utf-8') as handle:
        document = json.load(handle)

    messagegroups = document.get('messagegroups', {})
    validators: Dict[str, InstanceValidator] = {}
    contracts: Dict[str, Dict[str, Any]] = {}

    for endpoint_name, endpoint in document.get('endpoints', {}).items():
        if endpoint.get('protocol') != 'KAFKA':
            continue

        key_template = endpoint.get('protocoloptions', {}).get('options', {}).get('key')
        for group_ref in endpoint.get('messagegroups', []):
            group_name = group_ref.rsplit('/', 1)[-1]
            group = messagegroups.get(group_name)
            if group is None:
                raise AssertionError(
                    f'Endpoint {endpoint_name!r} references missing message group {group_name!r}'
                )

            for event_type, message in group.get('messages', {}).items():
                dataschema_uri = message.get('dataschemauri')
                if not dataschema_uri:
                    raise AssertionError(f'Message {event_type!r} is missing dataschemauri')

                schema_record = _resolve_json_pointer(document, dataschema_uri)
                default_version = schema_record.get('defaultversionid')
                if not default_version:
                    raise AssertionError(
                        f'Schema {dataschema_uri!r} in {xreg_path} has no defaultversionid'
                    )

                schema = schema_record['versions'][default_version]['schema']
                if dataschema_uri not in validators:
                    schema_errors = _SCHEMA_VALIDATOR.validate(schema)
                    if schema_errors:
                        formatted_errors = '; '.join(str(error) for error in schema_errors)
                        raise AssertionError(
                            f'Invalid JsonStructure schema {dataschema_uri!r} in {xreg_path}: '
                            f'{formatted_errors}'
                        )
                    validators[dataschema_uri] = InstanceValidator(schema, extended=True)

                subject_template = message.get('envelopemetadata', {}).get('subject', {}).get('value')
                existing = contracts.get(event_type)
                if existing is not None:
                    if (
                        existing['key_template'] != key_template
                        or existing['subject_template'] != subject_template
                        or existing['dataschema_uri'] != dataschema_uri
                    ):
                        raise AssertionError(
                            f'Conflicting Kafka contract declarations for {event_type!r} in {xreg_path}'
                        )
                    continue

                contracts[event_type] = {
                    'key_template': key_template,
                    'subject_template': subject_template,
                    'dataschema_uri': dataschema_uri,
                    'validator': validators[dataschema_uri],
                }

    if not contracts:
        raise AssertionError(f'No Kafka message contracts found in {xreg_path}')
    return contracts


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


def assert_kafka_contract(
    project_dir: str,
    records: List[ConsumedKafkaMessage],
    events: Optional[List[dict]] = None,
) -> List[dict]:
    """Validate Kafka keys and CloudEvent payloads against the project's xreg contract."""
    if events is None:
        events = assert_cloudevents([record.value for record in records])

    assert len(events) == len(records), 'Kafka record count does not match parsed CloudEvent count'
    contracts = _load_project_contract(project_dir)
    partitions_by_key: Dict[str, int] = {}

    for record, event in zip(records, events):
        event_type = event.get('type')
        contract = contracts.get(event_type)
        assert contract is not None, (
            f'No xreg contract found for event type {event_type!r} in project {project_dir!r}'
        )

        data = event.get('data')
        assert isinstance(data, dict), (
            f'CloudEvent {event_type!r} is missing an object data payload: {event}'
        )

        context = dict(event)
        context.update(data)

        actual_key = _decode_kafka_key(record.key)
        key_template = contract['key_template']
        if key_template is not None:
            expected_key = _render_template(key_template, context)
            assert actual_key == expected_key, (
                f'Kafka key mismatch for {event_type!r} at partition {record.partition}, '
                f'offset {record.offset}: expected {expected_key!r}, got {actual_key!r}'
            )

        if actual_key is not None:
            previous_partition = partitions_by_key.setdefault(actual_key, record.partition)
            assert previous_partition == record.partition, (
                f'Kafka key {actual_key!r} moved partitions during the test: '
                f'{previous_partition} -> {record.partition}'
            )

        subject_template = contract['subject_template']
        if subject_template is not None:
            expected_subject = _render_template(subject_template, context)
            assert event.get('subject') == expected_subject, (
                f'CloudEvent subject mismatch for {event_type!r} at partition {record.partition}, '
                f'offset {record.offset}: expected {expected_subject!r}, '
                f'got {event.get("subject")!r}'
            )

        schema_errors = contract['validator'].validate_instance(data)
        assert not schema_errors, (
            f'JsonStructure validation failed for {event_type!r} at partition {record.partition}, '
            f'offset {record.offset}: '
            f'{"; ".join(str(error) for error in schema_errors[:5])}\n'
            f'Data: {json.dumps(data, ensure_ascii=True, sort_keys=True)[:2000]}'
        )

    return events
