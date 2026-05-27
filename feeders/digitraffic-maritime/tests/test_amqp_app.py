from argparse import Namespace

from digitraffic_maritime_amqp.app import _build_common_kwargs, _parse_broker_url


def test_parse_amqp_broker_url():
    host, port, address, username, password, tls = _parse_broker_url('amqps://user:secret@broker.example.local:5671/digitraffic')
    assert host == 'broker.example.local'
    assert port == 5671
    assert address == 'digitraffic'
    assert username == 'user'
    assert password == 'secret'
    assert tls is True


def test_build_common_kwargs_from_broker_url():
    args = Namespace(
        broker_url='amqp://broker.example.local:5672/digitraffic-maritime',
        host=None,
        port=0,
        address='',
        tls=False,
        username=None,
        password=None,
        auth_mode='password',
        entra_client_id=None,
        entra_audience='https://servicebus.azure.net/.default',
        content_mode='binary',
    )
    kwargs, address = _build_common_kwargs(args)
    assert kwargs['host'] == 'broker.example.local'
    assert kwargs['port'] == 5672
    assert kwargs['address'] == 'digitraffic-maritime'
    assert kwargs['content_mode'] == 'binary'
    assert kwargs['use_tls'] is False
    assert address == 'digitraffic-maritime'
