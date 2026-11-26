import pytest
import json
from types import SimpleNamespace
from unittest.mock import Mock

from confluent_kafka import KafkaError, KafkaException

import helpers
from . import test_docker_kafka_flow as kafka_flow
from . import test_docker_mqtt_flow as mqtt_flow
from . import test_docker_amqp_flow as amqp_flow
from json_structure import InstanceValidator


class _FakeFuture:
    def __init__(self, exc=None):
        self._exc = exc

    def result(self, timeout=None):
        if self._exc is not None:
            raise self._exc


class _FakeAdminClient:
    def __init__(self, futures):
        self._futures = futures

    def create_topics(self, topics):
        return dict(self._futures)


def _make_fixture(monkeypatch):
    monkeypatch.setattr(helpers.docker, 'from_env', lambda: Mock())
    fixture = helpers.KafkaFixture()
    fixture._kafka = SimpleNamespace(get_bootstrap_server=lambda: 'localhost:9092')
    return fixture


def test_create_topic_ignores_existing_topics(monkeypatch):
    existing_error = KafkaException(KafkaError(KafkaError.TOPIC_ALREADY_EXISTS, 'topic exists'))
    monkeypatch.setattr(helpers, 'AdminClient', lambda *args, **kwargs: _FakeAdminClient({'test-topic': _FakeFuture(existing_error)}))
    monkeypatch.setattr(helpers.time, 'sleep', lambda _seconds: None)

    _make_fixture(monkeypatch).create_topic('test-topic')


def test_create_topic_reraises_non_existing_topic_errors(monkeypatch):
    unexpected_error = KafkaException(KafkaError(KafkaError.UNKNOWN_TOPIC_OR_PART, 'bad request'))
    monkeypatch.setattr(helpers, 'AdminClient', lambda *args, **kwargs: _FakeAdminClient({'test-topic': _FakeFuture(unexpected_error)}))
    monkeypatch.setattr(helpers.time, 'sleep', lambda _seconds: None)

    with pytest.raises(KafkaException):
        _make_fixture(monkeypatch).create_topic('test-topic')


def test_usgs_enrollment_is_staged_only_in_external_test_context(tmp_path, monkeypatch):
    checkout = tmp_path / 'checkout'
    checkout.mkdir()
    context = tmp_path / 'context'
    context.mkdir()
    enrollment = tmp_path / 'reviewed.json'
    enrollment.write_text('{"version": 1}', encoding='utf-8')
    monkeypatch.setattr(helpers, 'REPO_ROOT', str(checkout))
    monkeypatch.setenv('USGS_E2E_ENROLLMENT_FILE', str(enrollment))

    helpers._stage_usgs_test_enrollment('usgs-iv', str(context))

    assert (context / 'enrollment' / '01646500.json').read_text() == '{"version": 1}'
    assert not (checkout / 'enrollment').exists()


def test_usgs_enrollment_rejects_a_checked_in_or_missing_record(tmp_path, monkeypatch):
    monkeypatch.setattr(helpers, 'REPO_ROOT', str(tmp_path))
    record = tmp_path / 'reviewed.json'
    record.write_text('{}', encoding='utf-8')
    monkeypatch.setenv('USGS_E2E_ENROLLMENT_FILE', str(record))
    with pytest.raises(ValueError, match='outside the repository'):
        helpers._stage_usgs_test_enrollment('usgs-nwis-wq', str(tmp_path / 'context'))

    monkeypatch.setattr(helpers, 'REPO_ROOT', str(tmp_path / 'checkout'))
    monkeypatch.setenv('USGS_E2E_ENROLLMENT_FILE', str(tmp_path / 'missing.json'))
    with pytest.raises(FileNotFoundError, match='existing reviewed enrollment'):
        helpers._stage_usgs_test_enrollment('usgs-iv', str(tmp_path / 'context'))


def test_image_build_forwards_an_explicit_secure_package_mirror(monkeypatch):
    monkeypatch.delenv("DOCKER_BUILDKIT", raising=False)
    client = Mock()
    client.images.build.return_value = (Mock(), [])
    monkeypatch.setattr(helpers.docker, "from_env", lambda: client)
    monkeypatch.setattr(helpers.shutil, "copytree", Mock())
    monkeypatch.setattr(helpers.os.path, "isfile", lambda _: False)
    monkeypatch.setenv("PIP_INDEX_URL", "https://packages.example.test/simple/")
    helpers.build_image("usgs-iv")
    assert client.images.build.call_args.kwargs["buildargs"] == {
        "PIP_INDEX_URL": "https://packages.example.test/simple/"
    }


def test_image_build_uses_buildkit_with_the_staged_context(monkeypatch):
    client = Mock()
    run = Mock()
    monkeypatch.setattr(helpers.docker, "from_env", lambda: client)
    monkeypatch.setattr(helpers.shutil, "copytree", Mock())
    monkeypatch.setattr(helpers.os.path, "isfile", lambda _: False)
    monkeypatch.setattr(helpers.subprocess, "run", run)
    monkeypatch.setenv("DOCKER_BUILDKIT", "1")
    monkeypatch.setenv("PIP_INDEX_URL", "https://packages.example.test/simple/")

    image = helpers.build_image("usgs-iv", dockerfile="Dockerfile.amqp", tag="test-amqp")

    command = run.call_args.args[0]
    assert command[:-1] == [
        "docker", "build", "--quiet", "--rm", "--file", "Dockerfile.amqp",
        "--tag", "test-amqp", "--build-arg", "PIP_INDEX_URL=https://packages.example.test/simple/",
    ]
    assert "docker-build-context-" in command[-1]
    assert run.call_args.kwargs["cwd"] == command[-1]
    assert run.call_args.kwargs["check"] is True
    client.images.build.assert_not_called()
    client.images.get.assert_called_once_with("test-amqp")
    assert image is client.images.get.return_value


@pytest.mark.parametrize("index", ["http://packages.example.test/simple/", "https://user:secret@packages.example.test/simple/"])
def test_image_build_rejects_unsafe_package_mirrors(monkeypatch, index):
    monkeypatch.setenv("PIP_INDEX_URL", index)
    with pytest.raises(ValueError, match="credential-free HTTPS"):
        helpers.build_image("usgs-iv")


def test_strict_kafka_flow_fails_instead_of_skipping_an_empty_healthy_feeder(monkeypatch):
    container = Mock()
    container.logs.return_value = b"Cycle complete"
    monkeypatch.setattr(kafka_flow, "run_container_detached", lambda *args, **kwargs: container)
    monkeypatch.setattr(kafka_flow, "Consumer", lambda *_args, **_kwargs: Mock())
    with pytest.raises(AssertionError, match="Expected >=1 messages"):
        kafka_flow._run_kafka_flow_test(
            Mock(), Mock(), "empty",
            project_dir="usgs-waterdata",
            min_messages=1,
            timeout=0,
            fail_on_missing_types=True,
        )
    container.remove.assert_called_once_with(force=True)


def test_kafka_clean_exit_gate_catches_a_crash_after_publication(monkeypatch):
    container = Mock()
    container.logs.return_value = b"Failed later in the cycle"
    container.wait.return_value = {"StatusCode": 1}
    message = Mock()
    message.error.return_value = None
    message.value.return_value = b'{"type":"Fixture.Observation"}'
    consumer = Mock()
    consumer.poll.return_value = message
    monkeypatch.setattr(kafka_flow, "run_container_detached", lambda *args, **kwargs: container)
    monkeypatch.setattr(kafka_flow, "Consumer", lambda *_args, **_kwargs: consumer)
    monkeypatch.setattr(kafka_flow, "assert_kafka_contract", lambda *args: None)
    with pytest.raises(AssertionError, match="failed after publishing"):
        kafka_flow._run_kafka_flow_test(
            Mock(), Mock(), "partial",
            project_dir="usgs-waterdata", min_messages=1, require_clean_exit=True,
        )
    container.remove.assert_called_once_with(force=True)


def _mqtt_sample():
    return {
        "topic": "hydro/us/usgs/01646500/observation",
        "qos": 1,
        "retain": True,
        "payload": {"site": "01646500", "value": 1.0},
        "user_properties": {
            "specversion": "1.0",
            "type": "Fixture.Observation",
            "source": "https://example.test/",
            "subject": "01646500",
            "id": "test-id",
            "time": "2026-11-16T12:00:00Z",
            "_contenttype": "application/json",
        },
    }


def _mqtt_contracts(monkeypatch):
    validator = InstanceValidator({
        "$schema": "https://json-structure.org/meta/core/v0/#",
        "$id": "https://example.test/Observation",
        "name": "Observation",
        "type": "object",
        "properties": {"site": {"type": "string"}, "value": {"type": "double"}},
        "required": ["site", "value"],
    }, extended=True)
    contracts = {
        "Fixture.Observation": {
            "topic": "hydro/us/usgs/{site}/observation",
            "retain": True,
            "qos": 1,
            "subject_template": "{site}",
            "validator": validator,
        }
    }
    monkeypatch.setattr(mqtt_flow, "_load_mqtt_contracts", lambda _: contracts)


def test_strict_mqtt_requires_unchanged_attribute_names(monkeypatch):
    _mqtt_contracts(monkeypatch)
    sample = _mqtt_sample()
    sample["user_properties"]["ce_type"] = sample["user_properties"].pop("type")
    with pytest.raises(AssertionError, match="unchanged"):
        mqtt_flow._assert_mqtt_contract_messages("usgs-iv", [sample], strict=True)


@pytest.mark.parametrize("drift", ["null", "topic", "subject", "double-encoded"])
def test_strict_mqtt_does_not_hide_payload_or_identity_drift(monkeypatch, drift):
    _mqtt_contracts(monkeypatch)
    sample = _mqtt_sample()
    if drift == "null":
        sample["payload"]["value"] = None
    elif drift == "topic":
        sample["topic"] = "hydro/us/usgs/99999999/observation"
    elif drift == "double-encoded":
        sample["payload"] = '{"site":"01646500","value":1.0}'
    else:
        sample["user_properties"]["subject"] = "99999999"
    with pytest.raises(AssertionError):
        mqtt_flow._assert_mqtt_contract_messages("usgs-iv", [sample], strict=True)


def test_strict_mqtt_accepts_matching_retained_payload(monkeypatch):
    _mqtt_contracts(monkeypatch)
    mqtt_flow._assert_mqtt_contract_messages(
        "usgs-iv", [_mqtt_sample()], required_types={"Fixture.Observation"}, strict=True
    )


def test_strict_mqtt_requires_each_type_even_on_the_same_topic_leaf(monkeypatch):
    _mqtt_contracts(monkeypatch)
    contracts = mqtt_flow._load_mqtt_contracts("fixture")
    contracts["Fixture.OtherObservation"] = dict(contracts["Fixture.Observation"])
    with pytest.raises(AssertionError, match="OtherObservation"):
        mqtt_flow._assert_mqtt_contract_messages(
            "fixture", [_mqtt_sample()], required_types=set(contracts), strict=True
        )


@pytest.mark.parametrize("state", ["MD", "VA"])
def test_strict_mqtt_checks_out_of_band_routing_against_an_expected_value(monkeypatch, state):
    _mqtt_contracts(monkeypatch)
    mqtt_flow._load_mqtt_contracts("fixture")["Fixture.Observation"]["topic"] = (
        "hydro/us/usgs/{state}/{site}/observation"
    )
    sample = _mqtt_sample()
    sample["topic"] = "hydro/us/usgs/MD/01646500/observation"
    if state == "VA":
        with pytest.raises(AssertionError):
            mqtt_flow._assert_mqtt_contract_messages(
                "fixture", [sample], strict=True, expected_routing={"state": state}
            )
    else:
        mqtt_flow._assert_mqtt_contract_messages(
            "fixture", [sample], strict=True, expected_routing={"state": state}
        )


@pytest.mark.parametrize("protocol", ["AMQP", "amqp", "AMQP/1.0"])
@pytest.mark.parametrize("base_attribute", ["basemessageuri", "basemessage"])
@pytest.mark.parametrize("schema_ref", [
    "#/schemagroups/structures/schemas/payload",
    "#/schemagroups/structures/schemas/payload/versions/1",
])
def test_amqp_schemas_resolve_inherited_message_references_without_group_format(tmp_path, monkeypatch, protocol, base_attribute, schema_ref):
    schema = {
        "$schema": "https://json-structure.org/meta/core/v0/#",
        "$id": "https://example.test/Observation",
        "name": "Observation",
        "type": "object",
        "properties": {"value": {"type": "double"}},
        "required": ["value"],
    }
    manifest = {
        "endpoints": {"amqp": {"protocol": protocol, "messagegroups": ["/messagegroups/amqp"]}},
        "messagegroups": {
            "base": {"messages": {"observation": {
                "dataschemauri": schema_ref,
                "envelopemetadata": {"type": {"value": "Fixture.Observation"}},
            }}},
            "amqp": {"messages": {"inherited": {
                base_attribute: "/messagegroups/base/messages/observation",
            }}},
        },
        "schemagroups": {"structures": {"schemas": {"payload": {
            "defaultversionid": "1",
            "versions": {"1": {"format": "JsonStructure", "schema": schema}},
        }}}},
    }
    path = tmp_path / "fixture.xreg.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(amqp_flow, "_find_xreg_file", lambda _: str(path))

    validators = amqp_flow._load_jstruct_validators("fixture")

    assert not validators["Fixture.Observation"].validate_instance({"value": 1.0})
    assert validators["Fixture.Observation"].validate_instance({"value": None})


@pytest.mark.parametrize("format_location", ["group", "resource", "version"])
@pytest.mark.parametrize("version_reference", [False, True])
def test_amqp_validators_use_selected_schema_format_and_version(tmp_path, format_location, version_reference):
    schema = {
        "$schema": "https://json-structure.org/meta/core/v0/#",
        "$id": "https://example.test/schemas/Observation/v2",
        "name": "Observation",
        "type": "object",
        "properties": {"count": {"type": "int32"}},
        "required": ["count"],
    }
    previous = {**schema, "$id": "https://example.test/schemas/Observation/v1",
                "properties": {"count": {"type": "string"}}}
    version = {"schema": schema}
    resource = {"defaultversionid": "2", "versions": {
        "1": {"schema": previous}, "2": version,
    }}
    group = {"schemas": {"example.Observation": resource}}
    {"group": group, "resource": resource, "version": version}[format_location]["format"] = "JsonStructure/draft-02"
    schema_ref = "#/schemagroups/example.jstruct/schemas/example.Observation"
    if version_reference:
        resource["defaultversionid"] = "1"
        schema_ref += "/versions/2"
    manifest = {
        "endpoints": {"amqp": {"protocol": "AMQP", "messagegroups": ["/messagegroups/amqp"]}},
        "messagegroups": {
            "base": {"messages": {"observation": {
                "dataschemauri": schema_ref,
                "envelopemetadata": {"type": {"value": "Fixture.Observation"}},
            }}},
            "amqp": {"messages": {
                "json": {"basemessageuri": "/messagegroups/base/messages/observation"},
                "avro": {
                    "basemessageuri": "/messagegroups/base/messages/observation",
                    "dataschemauri": "#/schemagroups/example.avro/schemas/example.AvroObservation",
                },
            }},
        },
        "schemagroups": {
            "example.jstruct": group,
            "example.avro": {"format": "Avro/1.11.3", "schemas": {
                "example.AvroObservation": {"schema": {
                    "type": "record", "name": "AvroObservation", "fields": [],
                }},
            }},
        },
    }
    xreg_dir = tmp_path / "xreg"
    xreg_dir.mkdir()
    (xreg_dir / "test.xreg.json").write_text(json.dumps(manifest), encoding="utf-8")

    validators = amqp_flow._load_jstruct_validators(str(tmp_path))

    assert set(validators) == {"Fixture.Observation"}
    validator = validators["Fixture.Observation"]
    assert validator.validate({"count": 71}) == []
    assert validator.validate({"count": 71.5})
