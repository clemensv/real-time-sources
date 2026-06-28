"""Bluesky AT Protocol firehose consumer that forwards events to Kafka."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import random
import sys
from typing import Optional

from confluent_kafka import Producer

from bluesky_core.bluesky import (
    DEFAULT_FIREHOSE_URL,
    USER_AGENT,
    build_block_event,
    build_follow_event,
    build_like_event,
    build_post_event,
    build_profile_event,
    build_repost_event,
    iter_commit_events,
    iter_firehose_events,
    iter_mock_firehose_events,
    load_cursor,
    save_cursor,
)
from bluesky_producer_data import Block, Follow, Like, Post, Profile, Repost
from bluesky_producer_kafka_producer.producer import BlueskyFirehoseEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class BlueskyFirehose:
    def __init__(self, kafka_config: dict, kafka_topic: str, firehose_url: str = DEFAULT_FIREHOSE_URL, collections: Optional[list[str]] = None, cursor_file: Optional[str] = None, sample_rate: float = 1.0, content_mode: str = 'structured', content_type: str = 'application/json', use_compression: bool = False):
        self.kafka_config = kafka_config
        self.kafka_topic = kafka_topic
        self.firehose_url = firehose_url
        self.collections = set(collections) if collections else None
        self.cursor_file = cursor_file
        self.sample_rate = sample_rate
        self.content_mode = content_mode
        self.content_type = content_type
        self.use_compression = use_compression
        self.producer = Producer(kafka_config)
        self.cursor = load_cursor(cursor_file)
        self.avrotize_producer = BlueskyFirehoseEventProducer(self.producer, self.kafka_topic, content_mode=content_mode)  # type: ignore[arg-type]

    def load_cursor(self) -> Optional[int]:
        self.cursor = load_cursor(self.cursor_file)
        return self.cursor

    def save_cursor(self, cursor: Optional[int] = None) -> None:
        cursor_to_save = cursor if cursor is not None else self.cursor
        save_cursor(self.cursor_file, cursor_to_save)
        if cursor is not None:
            self.cursor = cursor

    @staticmethod
    def parse_connection_string(connection_string: str) -> dict[str, str]:
        config_dict = {}
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
                elif 'EntityPath' in part:
                    config_dict['kafka_topic'] = part.split('=')[1].strip('"')
                elif 'SharedAccessKeyName' in part:
                    config_dict['sasl.username'] = '$ConnectionString'
                elif 'SharedAccessKey' in part:
                    config_dict['sasl.password'] = connection_string.strip()
                elif 'BootstrapServer' in part:
                    config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
        except IndexError as exc:
            raise ValueError('Invalid connection string format') from exc
        if 'sasl.username' in config_dict:
            config_dict['security.protocol'] = 'SASL_SSL'
            config_dict['sasl.mechanism'] = 'PLAIN'
        return config_dict

    def should_sample(self) -> bool:
        return self.sample_rate >= 1.0 or random.random() < self.sample_rate

    def _send_with_avrotize(self, event_type: str, source: str, subject: str, data: dict) -> None:
        content_type = self.content_type + ('+gzip' if self.use_compression else '')
        if event_type == 'Bluesky.Feed.Post':
            self.avrotize_producer.send_bluesky_feed_post(source, subject, Post(**data), content_type=content_type, flush_producer=False)
        elif event_type == 'Bluesky.Feed.Like':
            self.avrotize_producer.send_bluesky_feed_like(source, subject, Like(**data), content_type=content_type, flush_producer=False)
        elif event_type == 'Bluesky.Feed.Repost':
            self.avrotize_producer.send_bluesky_feed_repost(source, subject, Repost(**data), content_type=content_type, flush_producer=False)
        elif event_type == 'Bluesky.Graph.Follow':
            self.avrotize_producer.send_bluesky_graph_follow(source, subject, Follow(**data), content_type=content_type, flush_producer=False)
        elif event_type == 'Bluesky.Graph.Block':
            self.avrotize_producer.send_bluesky_graph_block(source, subject, Block(**data), content_type=content_type, flush_producer=False)
        elif event_type == 'Bluesky.Actor.Profile':
            self.avrotize_producer.send_bluesky_actor_profile(source, subject, Profile(**data), content_type=content_type, flush_producer=False)

    def send_cloudevent(self, event_type: str, source: str, subject: str, data: dict) -> None:
        if not self.should_sample():
            return
        self._send_with_avrotize(event_type, source, subject, data)
        self.producer.poll(0)

    def _send_event(self, event) -> None:
        self.cursor = event.seq
        self.send_cloudevent(event.event_type, self.firehose_url, event.did, event.payload)

    def process_commit(self, commit) -> None:
        for event in iter_commit_events(commit, self.collections):
            self._send_event(event)

    def process_post(self, commit, uri, record: dict, cid) -> None:
        self._send_event(build_post_event(commit.repo, commit.seq, commit.time, str(uri), record, cid))

    def process_like(self, commit, uri, record: dict, cid) -> None:
        self._send_event(build_like_event(commit.repo, commit.seq, commit.time, str(uri), record, cid))

    def process_repost(self, commit, uri, record: dict, cid) -> None:
        self._send_event(build_repost_event(commit.repo, commit.seq, commit.time, str(uri), record, cid))

    def process_follow(self, commit, uri, record: dict, cid) -> None:
        self._send_event(build_follow_event(commit.repo, commit.seq, commit.time, str(uri), record, cid))

    def process_block(self, commit, uri, record: dict, cid) -> None:
        self._send_event(build_block_event(commit.repo, commit.seq, commit.time, str(uri), record, cid))

    def process_profile(self, commit, uri, record: dict, cid) -> None:
        self._send_event(build_profile_event(commit.repo, commit.seq, commit.time, str(uri), record, cid))

    async def run(self) -> None:
        mock = os.environ.get('BLUESKY_MOCK', '').lower() in ('1', 'true', 'yes')
        if mock:
            source = iter_mock_firehose_events(max_events=12)
        else:
            source = iter_firehose_events(firehose_url=self.firehose_url, collections=list(self.collections) if self.collections else None, cursor_provider=lambda: self.cursor, user_agent=USER_AGENT)
        try:
            async for event in source:
                self._send_event(event)
                if event.seq % 1000 == 0:
                    self.save_cursor()
                    self.producer.flush()
        finally:
            self.save_cursor()
            self.producer.flush()

    def close(self) -> None:
        self.save_cursor()
        self.producer.flush()


def main():
    parser = argparse.ArgumentParser(description='Bluesky Firehose to Kafka Bridge')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    stream_parser = subparsers.add_parser('stream', help='Stream firehose to Kafka')
    stream_parser.add_argument('--kafka-bootstrap-servers')
    stream_parser.add_argument('--kafka-topic')
    stream_parser.add_argument('--sasl-username')
    stream_parser.add_argument('--sasl-password')
    stream_parser.add_argument('--connection-string')
    stream_parser.add_argument('--firehose-url', default=os.getenv('BLUESKY_FIREHOSE_URL', DEFAULT_FIREHOSE_URL))
    stream_parser.add_argument('--collections', default=os.getenv('BLUESKY_COLLECTIONS', ''))
    stream_parser.add_argument('--cursor-file', default=os.getenv('BLUESKY_CURSOR_FILE', os.path.expanduser('~/.bluesky-kafka-bridge/cursor')))
    stream_parser.add_argument('--sample-rate', type=float, default=float(os.getenv('BLUESKY_SAMPLE_RATE', '1.0')))
    stream_parser.add_argument('--content-mode', choices=['structured', 'binary'], default=os.getenv('CLOUDEVENTS_MODE', 'structured'))
    stream_parser.add_argument('--content-type', choices=['application/json', 'application/vnd.apache.avro+avro'], default=os.getenv('CONTENT_TYPE', 'application/json'))
    stream_parser.add_argument('--compression', action='store_true', default=os.getenv('USE_COMPRESSION', '').lower() in ('true', '1', 'yes'))
    stream_parser.add_argument('--mock', action='store_true', default=os.getenv('BLUESKY_MOCK', '').lower() in ('1', 'true', 'yes'))
    args = parser.parse_args()
    if args.command != 'stream':
        parser.print_help()
        return 1
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config = {'bootstrap.servers': args.kafka_bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS'), 'client.id': 'bluesky-firehose-producer'}
    sasl_username = args.sasl_username or os.getenv('SASL_USERNAME')
    sasl_password = args.sasl_password or os.getenv('SASL_PASSWORD')
    if sasl_username and sasl_password:
        kafka_config.update({'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT', 'sasl.mechanism': 'PLAIN', 'sasl.username': sasl_username, 'sasl.password': sasl_password})
    kafka_topic = args.kafka_topic or os.getenv('KAFKA_TOPIC')
    connection_string = args.connection_string or os.getenv('CONNECTION_STRING')
    if connection_string:
        parsed = BlueskyFirehose.parse_connection_string(connection_string)
        kafka_topic = parsed.pop('kafka_topic', None)
        kafka_config.update(parsed)
    if 'sasl.username' in kafka_config:
        kafka_config['security.protocol'] = 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT'
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'
    if not kafka_config.get('bootstrap.servers') or not kafka_topic:
        logging.error('Kafka configuration incomplete. Provide either --connection-string or all Kafka parameters.')
        return 1
    collections = [c.strip() for c in args.collections.split(',') if c.strip()] or None
    firehose = BlueskyFirehose(kafka_config=kafka_config, kafka_topic=kafka_topic, firehose_url=args.firehose_url, collections=collections, cursor_file=args.cursor_file, sample_rate=args.sample_rate, content_mode=args.content_mode, content_type=args.content_type, use_compression=args.compression)
    if args.mock:
        os.environ['BLUESKY_MOCK'] = 'true'
    try:
        asyncio.run(firehose.run())
    except KeyboardInterrupt:
        logging.info('Shutting down...')
    finally:
        firehose.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
