from unittest.mock import Mock

import pytest

from usgs_waterdata_core.delivery import AcknowledgedKafkaProducer


@pytest.mark.parametrize("error,callback,remaining", [("rejected", True, 0), (None, False, 0), (None, True, 1)])
def test_failed_or_missing_kafka_delivery_is_visible(error, callback, remaining):
    raw = Mock()
    producer = AcknowledgedKafkaProducer(raw)
    producer.produce("topic", value=b"data")
    if callback:
        raw.produce.call_args.kwargs["on_delivery"](error, object())
    raw.flush.return_value = remaining
    with pytest.raises(RuntimeError, match="Kafka delivery failed"):
        producer.flush()


def test_success_requires_callback_and_empty_flush():
    raw = Mock()
    producer = AcknowledgedKafkaProducer(raw)
    producer.produce("topic", value=b"data")
    raw.produce.call_args.kwargs["on_delivery"](None, object())
    raw.flush.return_value = 0
    assert producer.flush() == 0
