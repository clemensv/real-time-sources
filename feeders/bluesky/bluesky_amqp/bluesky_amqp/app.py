"""Bluesky firehose -> AMQP 1.0 bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from bluesky_amqp_producer_amqp_producer.producer import BlueskyFirehoseAmqpProducer
from bluesky_amqp_producer_data import Block, Follow, Like, Post, Profile, Repost
from bluesky_core.bluesky import DEFAULT_FIREHOSE_URL, USER_AGENT, iter_firehose_events, iter_mock_firehose_events, normalize_segment

logger = logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _build_data(event):
    if event.event_type == 'Bluesky.Feed.Post':
        return Post(**event.payload)
    if event.event_type == 'Bluesky.Feed.Like':
        return Like(**event.payload)
    if event.event_type == 'Bluesky.Feed.Repost':
        return Repost(**event.payload)
    if event.event_type == 'Bluesky.Graph.Follow':
        return Follow(**event.payload)
    if event.event_type == 'Bluesky.Graph.Block':
        return Block(**event.payload)
    return Profile(**event.payload)


class _AmqpClient:
    def __init__(self, producer):
        self.producer = producer

    def __getattr__(self, name: str):
        if not name.startswith('publish_'):
            raise AttributeError(name)
        method = getattr(self.producer, 'send_' + name[len('publish_'):])

        async def _publish(**kwargs):
            data = kwargs.pop('data')
            kwargs.pop('qos', None)
            kwargs.pop('retain', None)
            params = set(method.__code__.co_varnames[: method.__code__.co_argcount])
            call_kwargs = {f'_{k}': v for k, v in kwargs.items() if v is not None and f'_{k}' in params}
            method(data=data, **call_kwargs)

        return _publish


class BlueskyAmqpBridge:
    def __init__(self, client: _AmqpClient, *, firehose_url: str = DEFAULT_FIREHOSE_URL, collections: Optional[list[str]] = None) -> None:
        self.client = client
        self.firehose_url = firehose_url
        self.collections = collections
        self._count = 0

    async def run(self, max_events: Optional[int] = None, mock: bool = False) -> None:
        if mock:
            source = iter_mock_firehose_events(max_events=max_events or 12)
        else:
            source = iter_firehose_events(firehose_url=self.firehose_url, collections=self.collections, user_agent=USER_AGENT)
        async for event in source:
            data = _build_data(event)
            method = getattr(self.client, 'publish_' + event.event_type.rsplit('.', 1)[-1].lower())
            await method(firehoseurl=self.firehose_url, did=normalize_segment(event.did), collection=normalize_segment(event.collection), lang=normalize_segment(event.lang), data=data, qos=0, retain=False)
            self._count += 1
            if max_events and self._count >= max_events:
                return


def _parse_amqp_broker_url(url: str):
    parsed = urlparse(url if '://' in url else f'amqp://{url}')
    scheme = (parsed.scheme or 'amqp').lower()
    tls = scheme in ('amqps', 'ssl', 'tls')
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or 'localhost', port, tls, parsed.username or None, parsed.password or None, (parsed.path or '').lstrip('/') or None


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL'))
    parser.add_argument('--host', default=os.getenv('AMQP_HOST'))
    parser.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None)
    parser.add_argument('--address', default=os.getenv('AMQP_ADDRESS', default_address))
    parser.add_argument('--username', default=os.getenv('AMQP_USERNAME'))
    parser.add_argument('--password', default=os.getenv('AMQP_PASSWORD'))
    parser.add_argument('--tls', action='store_true', default=os.getenv('AMQP_TLS', '').lower() in ('1', 'true', 'yes'))
    parser.add_argument('--content-mode', choices=('binary', 'structured'), default=os.getenv('AMQP_CONTENT_MODE', 'binary'))
    parser.add_argument('--auth-mode', choices=('password', 'entra', 'sas'), default=os.getenv('AMQP_AUTH_MODE', 'password'))
    parser.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID'))
    parser.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME'))
    parser.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY'))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or 'localhost'
        tls = bool(args.tls) or args.auth_mode in ('entra', 'sas')
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if args.auth_mode == 'entra':
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, credential=credential, entra_audience=args.entra_audience, use_tls=tls)
    if args.auth_mode == 'sas':
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError('AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY')
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key, use_tls=tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=args.content_mode, use_tls=tls)


async def _run(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, BlueskyFirehoseAmqpProducer)
    client = _AmqpClient(producer)
    collections = [c.strip() for c in args.collections.split(',') if c.strip()] if args.collections else None
    mock = os.environ.get('BLUESKY_MOCK', '').lower() in ('1', 'true', 'yes')
    try:
        await BlueskyAmqpBridge(client, firehose_url=args.firehose_url, collections=collections).run(max_events=args.max_events, mock=mock)
    finally:
        producer.close()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    p = argparse.ArgumentParser(description='Bluesky firehose -> AMQP 1.0 bridge')
    sub = p.add_subparsers(dest='command')
    feed = sub.add_parser('feed', help='Stream firehose to AMQP')
    add_amqp_arguments(feed, 'bluesky')
    feed.add_argument('--firehose-url', default=os.getenv('BLUESKY_FIREHOSE_URL', DEFAULT_FIREHOSE_URL))
    feed.add_argument('--collections', default=os.getenv('BLUESKY_COLLECTIONS', ''))
    feed.add_argument('--max-events', type=int, default=int(os.getenv('BLUESKY_MAX_EVENTS', '0')) or None)
    args = p.parse_args()
    if args.command != 'feed':
        p.print_help()
        sys.exit(1)
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info('Shutting down')


if __name__ == '__main__':
    main()
