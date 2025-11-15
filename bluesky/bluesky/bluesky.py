"""Bluesky AT Protocol firehose consumer that forwards events to Kafka."""

import argparse
import asyncio
import json
import logging
import os
import random
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal
from urllib.parse import urlparse

import aiohttp
from atproto import CAR, AtUri, firehose_models, models, parse_subscribe_repos_message
from confluent_kafka import Producer
from bluesky_producer_kafka_producer.producer import BlueskyFirehoseEventProducer
from bluesky_producer_data import Post, Like, Repost, Follow, Block, Profile

# Logging setup
if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class BlueskyFirehose:
    """Connects to Bluesky firehose and forwards events to Kafka."""

    def __init__(
        self,
        kafka_config: dict,
        kafka_topic: str,
        firehose_url: str = "wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos",
        collections: Optional[List[str]] = None,
        cursor_file: Optional[str] = None,
        sample_rate: float = 1.0,
        content_mode: Literal['structured', 'binary'] = 'structured',
        content_type: str = 'application/json',
        use_compression: bool = False,
    ):
        """
        Initialize the Bluesky firehose consumer.

        Args:
            kafka_config: Kafka producer configuration
            kafka_topic: Target Kafka topic
            firehose_url: Bluesky firehose WebSocket URL
            collections: List of AT Protocol collections to process (None = all)
            cursor_file: Path to file for storing cursor position
            sample_rate: Sampling rate for events (0.0 to 1.0)
            content_mode: CloudEvents mode - 'structured' (CloudEvent envelope) or 'binary' (data in body, CE attrs in headers)
            content_type: Content type for event data - 'application/json' or 'application/vnd.apache.avro+avro'
            use_compression: Enable gzip compression for event data
        """
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
        self.cursor: Optional[int] = None
        
        # Initialize avrotize producer
        self.avrotize_producer = BlueskyFirehoseEventProducer(
            self.producer, 
            self.kafka_topic, 
            content_mode=content_mode
        )
        
        self.load_cursor()

    def load_cursor(self) -> Optional[int]:
        """Load the last cursor position from file."""
        if self.cursor_file and os.path.exists(self.cursor_file):
            try:
                with open(self.cursor_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cursor = data.get('cursor')
                    logging.info("Loaded cursor: %s", self.cursor)
                    return self.cursor
            except Exception as e:
                logging.warning("Failed to load cursor: %s", e)
        return None

    def save_cursor(self, cursor: Optional[int] = None) -> None:
        """Save the current cursor position to file."""
        cursor_to_save = cursor if cursor is not None else self.cursor
        if self.cursor_file and cursor_to_save is not None:
            try:
                os.makedirs(os.path.dirname(self.cursor_file), exist_ok=True)
                with open(self.cursor_file, 'w', encoding='utf-8') as f:
                    json.dump({'cursor': cursor_to_save}, f)
                if cursor is not None:
                    self.cursor = cursor
            except Exception as e:
                logging.warning("Failed to save cursor: %s", e)

    def should_sample(self) -> bool:
        """Determine if current event should be sampled based on sample_rate."""
        return self.sample_rate >= 1.0 or random.random() < self.sample_rate

    @staticmethod
    def parse_connection_string(connection_string: str) -> Dict[str, str]:
        """
        Parse Event Hubs connection string.

        Args:
            connection_string: Event Hubs connection string

        Returns:
            Dict with bootstrap.servers and kafka_topic
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip(),
        }
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '') + ':9093'
                elif 'EntityPath' in part:
                    config_dict['kafka_topic'] = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict

    def send_cloudevent(self, event_type: str, source: str, subject: str, data: dict) -> None:
        """
        Send a CloudEvents-formatted message to Kafka.
        Uses avrotize producer if available, falls back to manual CloudEvents construction.

        Args:
            event_type: CloudEvents type
            source: CloudEvents source
            subject: CloudEvents subject
            data: Event data payload (dict)
        """
        if not self.should_sample():
            return

        try:
            # Use avrotize producer
            if self.avrotize_producer:
                self._send_with_avrotize(event_type, source, subject, data)
            self.producer.poll(0)
        except Exception as e:
            logging.error("Failed to send event: %s", e)

    def _send_with_avrotize(self, event_type: str, source: str, subject: str, data: dict) -> None:
        """Send event using avrotize-generated producer."""
        # Determine content type with compression suffix
        content_type = self.content_type
        if self.use_compression:
            content_type += '+gzip'
        
        # Map event types to avrotize producer methods and data classes
        if event_type == 'Bluesky.Feed.Post':
            post_data = Post(**data)
            self.avrotize_producer.send_bluesky_feed_post(
                source, subject, post_data, 
                content_type=content_type, 
                flush_producer=False
            )
        elif event_type == 'Bluesky.Feed.Like':
            like_data = Like(**data)
            self.avrotize_producer.send_bluesky_feed_like(
                source, subject, like_data,
                content_type=content_type,
                flush_producer=False
            )
        elif event_type == 'Bluesky.Feed.Repost':
            repost_data = Repost(**data)
            self.avrotize_producer.send_bluesky_feed_repost(
                source, subject, repost_data,
                content_type=content_type,
                flush_producer=False
            )
        elif event_type == 'Bluesky.Graph.Follow':
            follow_data = Follow(**data)
            self.avrotize_producer.send_bluesky_graph_follow(
                source, subject, follow_data,
                content_type=content_type,
                flush_producer=False
            )
        elif event_type == 'Bluesky.Graph.Block':
            block_data = Block(**data)
            self.avrotize_producer.send_bluesky_graph_block(
                source, subject, block_data,
                content_type=content_type,
                flush_producer=False
            )
        elif event_type == 'Bluesky.Actor.Profile':
            profile_data = Profile(**data)
            self.avrotize_producer.send_bluesky_actor_profile(
                source, subject, profile_data,
                content_type=content_type,
                flush_producer=False
            )

    def _delivery_callback(self, err, msg):
        """Kafka delivery callback."""
        if err:
            logging.error("Message delivery failed: %s", err)
        else:
            logging.debug("Message delivered to %s [%s]", msg.topic(), msg.partition())

    def should_process_collection(self, collection: str) -> bool:
        """Check if collection should be processed based on filter."""
        if self.collections is None:
            return True
        return collection in self.collections

    def process_commit(self, commit) -> None:
        """
        Process a commit message from the firehose.

        Args:
            commit: Firehose commit message
        """
        self.cursor = commit.seq

        if not commit.blocks:
            return

        try:
            car = CAR.from_bytes(commit.blocks)
        except Exception as e:
            logging.warning("Failed to parse CAR file: %s", e)
            return

        for op in commit.ops:
            uri = AtUri.from_str(f'at://{commit.repo}/{op.path}')
            collection = uri.collection

            if op.action == 'create' or op.action == 'update':
                if not self.should_process_collection(collection):
                    continue

                if not op.cid:
                    continue

                try:
                    record = car.blocks.get(op.cid)
                    if not record:
                        continue

                    # Ensure record is a dict (CAR may return dict or bytes depending on version)
                    if isinstance(record, bytes):
                        # Skip bytes records - they need proper DAG-CBOR decoding
                        logging.debug("Skipping bytes record at %s", uri)
                        continue
                    
                    if not isinstance(record, dict):
                        logging.warning("Unexpected record type %s at %s", type(record), uri)
                        continue

                    # Process different collection types
                    if collection == 'app.bsky.feed.post':
                        self.process_post(commit, uri, record, op.cid)
                    elif collection == 'app.bsky.feed.like':
                        self.process_like(commit, uri, record, op.cid)
                    elif collection == 'app.bsky.feed.repost':
                        self.process_repost(commit, uri, record, op.cid)
                    elif collection == 'app.bsky.graph.follow':
                        self.process_follow(commit, uri, record, op.cid)
                    elif collection == 'app.bsky.graph.block':
                        self.process_block(commit, uri, record, op.cid)
                    elif collection == 'app.bsky.actor.profile':
                        self.process_profile(commit, uri, record, op.cid)

                except Exception as e:
                    logging.warning("Failed to process record %s: %s", uri, e)

    def process_post(self, commit, uri: AtUri, record: dict, cid) -> None:
        """Process a post record."""
        # Extract reply information including CIDs
        reply = record.get('reply', {})
        reply_parent = reply.get('parent', {})
        reply_root = reply.get('root', {})
        
        # Extract embed information
        embed = record.get('embed', {})
        embed_type = embed.get('$type')
        embed_uri = None
        
        if embed_type == 'app.bsky.embed.external':
            embed_uri = embed.get('external', {}).get('uri')
        elif embed_type == 'app.bsky.embed.record':
            embed_uri = embed.get('record', {}).get('uri')
        elif embed_type == 'app.bsky.embed.recordWithMedia':
            # Compound embed: extract URI from the record part
            embed_uri = embed.get('record', {}).get('record', {}).get('uri')
        # For images and video, no URI field exists (uses CID/blob refs)
        
        data = {
            'uri': str(uri),
            'cid': str(cid) if cid else '',
            'did': commit.repo,
            'handle': None,  # Handle not available in firehose, would need separate DID resolution
            'text': record.get('text', ''),
            'langs': record.get('langs', []),
            'reply_parent': reply_parent.get('uri'),
            'reply_parent_cid': reply_parent.get('cid'),
            'reply_root': reply_root.get('uri'),
            'reply_root_cid': reply_root.get('cid'),
            'embed_type': embed_type,
            'embed_uri': embed_uri,
            'facets': json.dumps(record.get('facets', [])) if record.get('facets') else None,
            'labels': json.dumps(record.get('labels', {})) if record.get('labels') else None,
            'tags': record.get('tags', []),
            'created_at': record.get('createdAt', ''),
            'indexed_at': commit.time,
            'seq': commit.seq
        }
        self.send_cloudevent('Bluesky.Feed.Post', self.firehose_url, commit.repo, data)

    def process_like(self, commit, uri: AtUri, record: dict, cid) -> None:
        """Process a like record."""
        subject = record.get('subject', {})
        data = {
            'uri': str(uri),
            'cid': str(cid) if cid else '',
            'did': commit.repo,
            'handle': None,  # Handle not available in firehose, would need separate DID resolution
            'subject_uri': subject.get('uri', ''),
            'subject_cid': subject.get('cid', ''),
            'created_at': record.get('createdAt', ''),
            'indexed_at': commit.time,
            'seq': commit.seq
        }
        self.send_cloudevent('Bluesky.Feed.Like', self.firehose_url, commit.repo, data)

    def process_repost(self, commit, uri: AtUri, record: dict, cid) -> None:
        """Process a repost record."""
        subject = record.get('subject', {})
        data = {
            'uri': str(uri),
            'cid': str(cid) if cid else '',
            'did': commit.repo,
            'handle': None,  # Handle not available in firehose, would need separate DID resolution
            'subject_uri': subject.get('uri', ''),
            'subject_cid': subject.get('cid', ''),
            'created_at': record.get('createdAt', ''),
            'indexed_at': commit.time,
            'seq': commit.seq
        }
        self.send_cloudevent('Bluesky.Feed.Repost', self.firehose_url, commit.repo, data)

    def process_follow(self, commit, uri: AtUri, record: dict, cid) -> None:
        """Process a follow record."""
        data = {
            'uri': str(uri),
            'cid': str(cid) if cid else '',
            'did': commit.repo,
            'handle': None,  # Handle not available in firehose, would need separate DID resolution
            'subject': record.get('subject', ''),
            'subject_handle': None,
            'created_at': record.get('createdAt', ''),
            'indexed_at': commit.time,
            'seq': commit.seq
        }
        self.send_cloudevent('Bluesky.Graph.Follow', self.firehose_url, commit.repo, data)

    def process_block(self, commit, uri: AtUri, record: dict, cid) -> None:
        """Process a block record."""
        data = {
            'uri': str(uri),
            'cid': str(cid) if cid else '',
            'did': commit.repo,
            'handle': None,  # Handle not available in firehose, would need separate DID resolution
            'subject': record.get('subject', ''),
            'subject_handle': None,
            'created_at': record.get('createdAt', ''),
            'indexed_at': commit.time,
            'seq': commit.seq
        }
        self.send_cloudevent('Bluesky.Graph.Block', self.firehose_url, commit.repo, data)

    def process_profile(self, commit, uri: AtUri, record: dict, cid) -> None:
        """Process a profile record."""
        # Helper to safely extract nested dict values, handling bytes
        def safe_get_link(field_value):
            if not field_value or isinstance(field_value, bytes):
                return None
            if isinstance(field_value, dict):
                ref = field_value.get('ref', {})
                if isinstance(ref, dict):
                    return ref.get('$link')
            return None
        
        avatar_value = record.get('avatar')
        banner_value = record.get('banner')
        
        data = {
            'did': commit.repo,
            'handle': None,  # Handle not available in firehose, would need separate DID resolution
            'display_name': record.get('displayName'),
            'description': record.get('description'),
            'avatar': safe_get_link(avatar_value),
            'banner': safe_get_link(banner_value),
            'created_at': record.get('createdAt', ''),
            'indexed_at': commit.time,
            'seq': commit.seq
        }
        self.send_cloudevent('Bluesky.Actor.Profile', self.firehose_url, commit.repo, data)

    async def run(self) -> None:
        """Connect to the firehose and process events."""
        # Lazy import to avoid Pydantic initialization issues in some environments
        import atproto_firehose.models
        
        url = self.firehose_url
        if self.cursor:
            url += f'?cursor={self.cursor}'

        logging.info("Connecting to Bluesky firehose at %s", url)
        logging.info("Kafka topic: %s, bootstrap: %s", self.kafka_topic, self.kafka_config['bootstrap.servers'])
        if self.collections:
            logging.info("Filtering collections: %s", ', '.join(self.collections))
        if self.sample_rate < 1.0:
            logging.info("Sampling rate: %.2f%%", self.sample_rate * 100)

        retry_delay = 1
        max_retry_delay = 60

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        logging.info("Connected to firehose")
                        retry_delay = 1  # Reset on successful connection

                        async for msg in ws:
                            # Check if msg is a bytes object (direct data) or aiohttp WSMessage
                            if isinstance(msg, bytes):
                                # Direct bytes from firehose
                                try:
                                    # Convert bytes to MessageFrame
                                    frame = atproto_firehose.models.Frame.from_bytes(msg)
                                    if isinstance(frame, atproto_firehose.models.MessageFrame):
                                        message = parse_subscribe_repos_message(frame)
                                        if hasattr(message, 'commit') or (hasattr(message, 'seq') and hasattr(message, 'blocks')):
                                            self.process_commit(message)
                                            
                                            # Periodically save cursor
                                            if hasattr(message, 'seq') and message.seq % 1000 == 0:
                                                self.save_cursor()
                                                self.producer.flush()
                                            
                                except Exception as e:
                                    import traceback
                                    logging.warning("Failed to process message: %s (type: %s)", e, type(e).__name__)
                                    logging.warning("Full traceback:\n%s", traceback.format_exc())
                                    
                            elif isinstance(msg, aiohttp.WSMessage):
                                # aiohttp WSMessage object
                                if msg.type == aiohttp.WSMsgType.BINARY:
                                    try:
                                        # Convert bytes to MessageFrame
                                        frame = atproto_firehose.models.Frame.from_bytes(msg.data)
                                        if isinstance(frame, atproto_firehose.models.MessageFrame):
                                            message = parse_subscribe_repos_message(frame)
                                            if hasattr(message, 'commit') or (hasattr(message, 'seq') and hasattr(message, 'blocks')):
                                                self.process_commit(message)
                                                
                                                # Periodically save cursor
                                                if hasattr(message, 'seq') and message.seq % 1000 == 0:
                                                    self.save_cursor()
                                                    self.producer.flush()
                                                
                                    except Exception as e:
                                        import traceback
                                        logging.warning("Failed to process message: %s (type: %s)", e, type(e).__name__)
                                        logging.warning("Full traceback:\n%s", traceback.format_exc())
                                        
                                elif msg.type == aiohttp.WSMsgType.ERROR:
                                    logging.error("WebSocket error")
                                    break

            except Exception as e:
                logging.error("Connection error: %s. Retrying in %d seconds...", e, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)
                
                # Update URL with current cursor for reconnection
                if self.cursor:
                    parsed = urlparse(self.firehose_url)
                    url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?cursor={self.cursor}"

    def close(self) -> None:
        """Cleanup resources."""
        self.save_cursor()
        self.producer.flush()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Bluesky Firehose to Kafka Bridge')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Stream command
    stream_parser = subparsers.add_parser('stream', help='Stream firehose to Kafka')
    
    # Kafka configuration
    stream_parser.add_argument('--kafka-bootstrap-servers', 
                              help='Kafka bootstrap servers')
    stream_parser.add_argument('--kafka-topic', 
                              help='Kafka topic name')
    stream_parser.add_argument('--sasl-username', 
                              help='SASL username')
    stream_parser.add_argument('--sasl-password', 
                              help='SASL password')
    stream_parser.add_argument('--connection-string',
                              help='Event Hubs connection string (overrides other Kafka params)')
    
    # Firehose configuration
    stream_parser.add_argument('--firehose-url',
                              default=os.getenv('BLUESKY_FIREHOSE_URL', 
                                              'wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos'),
                              help='Bluesky firehose WebSocket URL')
    stream_parser.add_argument('--collections',
                              default=os.getenv('BLUESKY_COLLECTIONS', ''),
                              help='Comma-separated list of collections to process (empty = all)')
    stream_parser.add_argument('--cursor-file',
                              default=os.getenv('BLUESKY_CURSOR_FILE', 
                                              os.path.expanduser('~/.bluesky-kafka-bridge/cursor')),
                              help='Path to cursor persistence file')
    stream_parser.add_argument('--sample-rate',
                              type=float,
                              default=float(os.getenv('BLUESKY_SAMPLE_RATE', '1.0')),
                              help='Sampling rate (0.0 to 1.0)')
    
    # CloudEvents configuration
    stream_parser.add_argument('--content-mode',
                              choices=['structured', 'binary'],
                              default=os.getenv('CLOUDEVENTS_MODE', 'structured'),
                              help='CloudEvents mode: structured (envelope) or binary (headers)')
    stream_parser.add_argument('--content-type',
                              choices=['application/json', 'application/vnd.apache.avro+avro'],
                              default=os.getenv('CONTENT_TYPE', 'application/json'),
                              help='Content type for event data: JSON or Avro binary')
    stream_parser.add_argument('--compression',
                              action='store_true',
                              default=os.getenv('USE_COMPRESSION', '').lower() in ('true', '1', 'yes'),
                              help='Enable gzip compression for event data')
    
    args = parser.parse_args()
    
    if args.command != 'stream':
        parser.print_help()
        return 1
    
    # Build Kafka configuration
    kafka_config = {
        'bootstrap.servers': args.kafka_bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': args.sasl_username or os.getenv('SASL_USERNAME'),
        'sasl.password': args.sasl_password or os.getenv('SASL_PASSWORD'),
        'client.id': 'bluesky-firehose-producer',
    }
    
    kafka_topic = args.kafka_topic or os.getenv('KAFKA_TOPIC')
    
    # Parse connection string if provided
    connection_string = args.connection_string or os.getenv('CONNECTION_STRING')
    if connection_string:
        # Use the static method directly without creating an instance
        parsed = BlueskyFirehose.parse_connection_string(connection_string)
        # Extract kafka_topic separately - it's not a kafka config param
        kafka_topic = parsed.pop('kafka_topic', None)
        kafka_config.update(parsed)
    
    if not kafka_config.get('bootstrap.servers') or not kafka_topic:
        logging.error("Kafka configuration incomplete. Provide either --connection-string or all Kafka parameters.")
        return 1
    
    # Parse collections filter
    collections = None
    if args.collections:
        collections = [c.strip() for c in args.collections.split(',') if c.strip()]
    
    # Log configuration
    logging.info("Configuration:")
    logging.info("  Content mode: %s", args.content_mode)
    logging.info("  Content type: %s", args.content_type)
    logging.info("  Compression: %s", "enabled" if args.compression else "disabled")
    
    # Create and run firehose
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        firehose_url=args.firehose_url,
        collections=collections,
        cursor_file=args.cursor_file,
        sample_rate=args.sample_rate,
        content_mode=args.content_mode,
        content_type=args.content_type,
        use_compression=args.compression,
    )
    
    try:
        asyncio.run(firehose.run())
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        firehose.close()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
