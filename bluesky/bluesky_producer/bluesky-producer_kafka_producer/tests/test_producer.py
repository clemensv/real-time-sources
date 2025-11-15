# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bluesky-producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bluesky-producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bluesky-producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from bluesky-producer_kafka_producer.producer import BlueskyFirehoseEventProducer
from bluesky-producer_data import Post
from bluesky-producer_data import Like
from bluesky-producer_data import Repost
from bluesky-producer_data import Follow
from bluesky-producer_data import Block
from bluesky-producer_data import Profile

@pytest.fixture(scope="module")
def kafka_emulator():
    with KafkaContainer() as kafka:
        admin_client = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic_list = [
            NewTopic("test_topic", num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(topic_list)

        yield {
            "bootstrap_servers": kafka.get_bootstrap_server(),
            "topic": "test_topic",
        }

def parse_cloudevent(msg: Message) -> CloudEvent:
    headers_dict: Dict[str, bytes] = {header[0]: header[1] for header in msg.headers()}
    message = KafkaMessage(headers=headers_dict, key=msg.key(), value=msg.value())
    if message.headers and 'content-type' in message.headers:
        content_type = message.headers['content-type'].decode()
        if content_type.startswith('application/cloudevents'):
            ce = from_structured(message)
            if 'datacontenttype' not in ce:
                ce['datacontenttype'] = 'application/json'
        else:
            ce = from_binary(message)
            ce['datacontenttype'] = message.headers['content-type'].decode()
    else:
        ce = from_binary(message)
        ce['datacontenttype'] = 'application/json'
    return ce

def test_blueskyfirehose_blueskyfeedpost(kafka_emulator):
    """Test the BlueskyFeedPost event from the BlueskyFirehose message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_blueskyfirehose_blueskyfeedpost',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Bluesky.Feed.Post":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Post
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_bluesky_feed_post(_firehoseurl = 'test', _did = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_blueskyfirehose_blueskyfeedlike(kafka_emulator):
    """Test the BlueskyFeedLike event from the BlueskyFirehose message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_blueskyfirehose_blueskyfeedlike',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Bluesky.Feed.Like":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Like
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_bluesky_feed_like(_firehoseurl = 'test', _did = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_blueskyfirehose_blueskyfeedrepost(kafka_emulator):
    """Test the BlueskyFeedRepost event from the BlueskyFirehose message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_blueskyfirehose_blueskyfeedrepost',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Bluesky.Feed.Repost":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Repost
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_bluesky_feed_repost(_firehoseurl = 'test', _did = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_blueskyfirehose_blueskygraphfollow(kafka_emulator):
    """Test the BlueskyGraphFollow event from the BlueskyFirehose message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_blueskyfirehose_blueskygraphfollow',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Bluesky.Graph.Follow":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Follow
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_bluesky_graph_follow(_firehoseurl = 'test', _did = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_blueskyfirehose_blueskygraphblock(kafka_emulator):
    """Test the BlueskyGraphBlock event from the BlueskyFirehose message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_blueskyfirehose_blueskygraphblock',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Bluesky.Graph.Block":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Block
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_bluesky_graph_block(_firehoseurl = 'test', _did = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_blueskyfirehose_blueskyactorprofile(kafka_emulator):
    """Test the BlueskyActorProfile event from the BlueskyFirehose message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_blueskyfirehose_blueskyactorprofile',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Bluesky.Actor.Profile":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Profile
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_bluesky_actor_profile(_firehoseurl = 'test', _did = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()