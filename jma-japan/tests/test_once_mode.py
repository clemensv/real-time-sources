"""Verify --once causes the poller to exit after one cycle."""

from unittest.mock import MagicMock, patch

from jma_japan.jma_japan import JMABulletinPoller


def _make_poller(tmp_path):
    poller = JMABulletinPoller.__new__(JMABulletinPoller)
    poller.kafka_topic = 'test-topic'
    poller.last_polled_file = str(tmp_path / 'state.json')
    poller.kafka_producer = MagicMock()
    poller.bulletins_producer = MagicMock()
    return poller


def test_once_mode_exits_after_one_cycle(tmp_path):
    poller = _make_poller(tmp_path)
    with patch.object(poller, 'poll_feeds', return_value=[]) as poll_feeds, \
         patch('jma_japan.jma_japan.time.sleep') as sleep_mock:
        poller.poll_and_send(once=True)
    assert poll_feeds.call_count == 1
    sleep_mock.assert_not_called()


def test_default_mode_loops(tmp_path):
    poller = _make_poller(tmp_path)
    call_count = {'n': 0}

    def fake_poll():
        call_count['n'] += 1
        return []

    def fake_sleep(_):
        if call_count['n'] >= 2:
            raise KeyboardInterrupt

    with patch.object(poller, 'poll_feeds', side_effect=fake_poll), \
         patch('jma_japan.jma_japan.time.sleep', side_effect=fake_sleep):
        try:
            poller.poll_and_send(once=False)
        except KeyboardInterrupt:
            pass
    assert call_count['n'] >= 2
