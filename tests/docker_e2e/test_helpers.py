import pytest
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
