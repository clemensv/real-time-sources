import pytest
import copy
import json
from types import SimpleNamespace

from confluent_kafka import KafkaError, KafkaException

import helpers


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


def _make_fixture():
    fixture = helpers.KafkaFixture()
    fixture._kafka = SimpleNamespace(get_bootstrap_server=lambda: 'localhost:9092')
    return fixture


def test_create_topic_ignores_existing_topics(monkeypatch):
    existing_error = KafkaException(KafkaError(KafkaError.TOPIC_ALREADY_EXISTS, 'topic exists'))
    monkeypatch.setattr(helpers, 'AdminClient', lambda *args, **kwargs: _FakeAdminClient({'test-topic': _FakeFuture(existing_error)}))
    monkeypatch.setattr(helpers.time, 'sleep', lambda _seconds: None)

    _make_fixture().create_topic('test-topic')


def test_create_topic_reraises_non_existing_topic_errors(monkeypatch):
    unexpected_error = KafkaException(KafkaError(KafkaError.UNKNOWN_TOPIC_OR_PART, 'bad request'))
    monkeypatch.setattr(helpers, 'AdminClient', lambda *args, **kwargs: _FakeAdminClient({'test-topic': _FakeFuture(unexpected_error)}))
    monkeypatch.setattr(helpers.time, 'sleep', lambda _seconds: None)

    with pytest.raises(KafkaException):
        _make_fixture().create_topic('test-topic')


def test_current_and_legacy_inheritance_deep_merge_without_mutation():
    document = {'messagegroups': {'example': {'messages': {
        'base': {'envelope': 'CloudEvents/1.0', 'envelopemetadata': {
            'subject': {'type': 'uritemplate', 'value': '{id}'},
            'datacontenttype': {'type': 'string', 'value': 'application/json'},
        }},
        'mqtt': {'basemessageuri': '/messagegroups/example/messages/base',
                 'protocoloptions': {'topic_name': 'example/{id}', 'retain': True}},
        'binary': {'basemessage': '/messagegroups/example/messages/mqtt',
                   'envelopemetadata': {'datacontenttype': {'value': 'application/vnd.apache.org.avro+avro'}}},
    }}}}
    original = copy.deepcopy(document)
    resolved = helpers._resolve_message_inheritance(document, document['messagegroups']['example']['messages']['binary'])
    assert resolved['envelopemetadata']['subject']['value'] == '{id}'
    assert resolved['envelopemetadata']['datacontenttype'] == {'type': 'string', 'value': 'application/vnd.apache.org.avro+avro'}
    assert resolved['protocoloptions']['retain'] is True
    assert document == original
    document['messagegroups']['example']['messages']['base']['basemessage'] = '/messagegroups/example/messages/binary'
    with pytest.raises(AssertionError, match='Cyclic'):
        helpers._resolve_message_inheritance(document, document['messagegroups']['example']['messages']['binary'])


def test_json_flow_selects_json_structure_contract_among_avro_variants(tmp_path, monkeypatch):
    schema_uri = '#/schemagroups/example/schemas/Observation'
    base = {'dataschemaformat': 'JsonStructure/draft-02', 'dataschemauri': schema_uri,
            'envelopemetadata': {'type': {'value': 'example.Observation'}, 'subject': {'value': '{id}'}}}
    document = {
        'messagegroups': {
            'json': {'messages': {'Observation': base}},
            'avro': {'messages': {'Observation': {
                'basemessage': '/messagegroups/json/messages/Observation',
                'dataschemaformat': 'Avro/1.11.3', 'dataschemauri': '#/absent/avro',
            }}},
        },
        'endpoints': {'Kafka': {'protocol': 'KAFKA', 'messagegroups': ['#/messagegroups/json', '#/messagegroups/avro'],
                                'protocoloptions': {'options': {'key': '{id}'}}}},
        'schemagroups': {'example': {'schemas': {'Observation': {
            'defaultversionid': '1', 'versions': {'1': {'schema': {'type': 'object'}}},
        }}}},
    }
    manifest_path = tmp_path / 'example.xreg.json'
    manifest_path.write_text(json.dumps(document), encoding='utf-8')
    monkeypatch.setattr(helpers, '_find_xreg_file', lambda _project: str(manifest_path))
    monkeypatch.setattr(helpers, '_SCHEMA_VALIDATOR', SimpleNamespace(validate=lambda _schema: []))
    monkeypatch.setattr(helpers, 'InstanceValidator', lambda *args, **kwargs: object())
    helpers._load_project_contract.cache_clear()
    try:
        contracts = helpers._load_project_contract(str(tmp_path))
        assert list(contracts) == ['example.Observation']
        assert contracts['example.Observation']['dataschema_uri'] == schema_uri
    finally:
        helpers._load_project_contract.cache_clear()


@pytest.mark.parametrize('extra', [
    {'datacontenttype': 'application/vnd.apache.org.avro+avro'},
    {'data_base64': 'e30='},
])
def test_json_flow_rejects_mislabeled_or_binary_payloads(monkeypatch, extra):
    monkeypatch.setattr(helpers, '_load_project_contract', lambda _project: {})
    record = helpers.ConsumedKafkaMessage(key=b'id', value=b'{}', partition=0, offset=0)
    event = {'type': 'example.Observation', 'data': {'id': 'id'}, **extra}
    with pytest.raises(AssertionError, match='JSON flow'):
        helpers.assert_kafka_contract('example', [record], [event])
