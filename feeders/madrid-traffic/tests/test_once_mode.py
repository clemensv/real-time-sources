"""
Verify that the --once flag causes main() to perform a single polling cycle
and return, instead of looping forever. This is required for Fabric notebook
scheduled execution (single-cycle exits).
"""

import sys
from unittest.mock import patch, MagicMock

from madrid_traffic.madrid_traffic import main


def test_once_flag_runs_single_cycle(monkeypatch):
    monkeypatch.setenv('CONNECTION_STRING',
                       'Endpoint=sb://fake/;SharedAccessKeyName=k;'
                       'SharedAccessKey=v;EntityPath=madrid')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')

    poller_instance = MagicMock()
    poller_instance.fetch_xml.return_value = None
    with patch('madrid_traffic.madrid_traffic.MadridTrafficPoller',
               return_value=poller_instance) as poller_cls, \
         patch('madrid_traffic.madrid_traffic.Producer'), \
         patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer'), \
         patch('madrid_traffic.madrid_traffic.time.sleep') as sleep_mock, \
         patch.object(sys, 'argv', ['madrid-traffic', '--once']):
        main()

    poller_cls.assert_called_once()
    poller_instance.fetch_xml.assert_called_once()
    sleep_mock.assert_not_called()


def test_once_mode_env_var_runs_single_cycle(monkeypatch):
    monkeypatch.setenv('CONNECTION_STRING',
                       'Endpoint=sb://fake/;SharedAccessKeyName=k;'
                       'SharedAccessKey=v;EntityPath=madrid')
    monkeypatch.setenv('KAFKA_ENABLE_TLS', 'false')
    monkeypatch.setenv('ONCE_MODE', 'true')

    poller_instance = MagicMock()
    poller_instance.fetch_xml.return_value = None
    with patch('madrid_traffic.madrid_traffic.MadridTrafficPoller',
               return_value=poller_instance), \
         patch('madrid_traffic.madrid_traffic.Producer'), \
         patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer'), \
         patch('madrid_traffic.madrid_traffic.time.sleep') as sleep_mock, \
         patch.object(sys, 'argv', ['madrid-traffic']):
        main()

    poller_instance.fetch_xml.assert_called_once()
    sleep_mock.assert_not_called()
