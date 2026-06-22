from __future__ import annotations

import argparse
import asyncio
import logging
import os
import re
import threading
import time
from datetime import datetime, timedelta, timezone
from zipfile import ZipFile

import requests
from confluent_kafka import Producer
from gtfs_rt_producer_kafka_producer.producer import (
    GeneralTransitFeedRealTimeEventProducer,
    GeneralTransitFeedStaticEventProducer,
)

import gtfs_core.core as _core
from gtfs_core.core import *  # noqa: F401,F403
from gtfs_core.core import (
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_SCHEDULE_POLL_INTERVAL_SECONDS,
    fetch_and_publish_schedule as _core_fetch_and_publish_schedule,
    poll_and_publish_gtfs,
    poll_and_publish_realtime_feed as _core_poll_and_publish_realtime_feed,
)

_CORE_CALCULATE_FILE_HASHES = _core.calculate_file_hashes
_CORE_FETCH_SCHEDULE_FILE = _core.fetch_schedule_file
_CORE_FETCH_AND_PUBLISH_SCHEDULE = _core.fetch_and_publish_schedule
_CORE_ITER_SCHEDULE_FILE_CONTENTS = _core.iter_schedule_file_contents
_CORE_POLL_AND_PUBLISH_REALTIME_FEED = _core.poll_and_publish_realtime_feed
_CORE_READ_SCHEDULE_FILE_CONTENTS = _core.read_schedule_file_contents


def _call_core(func, *args, **kwargs):
    old_requests = _core.requests
    old_zipfile = _core.ZipFile
    _core.requests = requests
    _core.ZipFile = ZipFile
    try:
        return func(*args, **kwargs)
    finally:
        _core.requests = old_requests
        _core.ZipFile = old_zipfile


def fetch_schedule_file(gtfs_url, mdb_source_id, gtfs_headers, etag, cache_dir):
    return _call_core(_CORE_FETCH_SCHEDULE_FILE, gtfs_url, mdb_source_id, gtfs_headers, etag, cache_dir)


def calculate_file_hashes(schedule_file_path: str):
    return _call_core(_CORE_CALCULATE_FILE_HASHES, schedule_file_path)


def read_schedule_file_contents(schedule_file_path: str, file_name: str):
    return _call_core(_CORE_READ_SCHEDULE_FILE_CONTENTS, schedule_file_path, file_name)


def iter_schedule_file_contents(schedule_file_path: str, file_name: str):
    return _call_core(_CORE_ITER_SCHEDULE_FILE_CONTENTS, schedule_file_path, file_name)


class KafkaMqttLikePublisher:
    def __init__(self, producer: Producer, topic: str, cloudevents_mode: str) -> None:
        self._producer = producer
        self._realtime = GeneralTransitFeedRealTimeEventProducer(producer, topic, cloudevents_mode)
        self._static = GeneralTransitFeedStaticEventProducer(producer, topic, cloudevents_mode)

    async def flush(self) -> None:
        self._producer.flush()

    async def poll(self) -> None:
        self._producer.poll(0)

    def __getattr__(self, name: str):
        if not name.startswith("publish_") or not name.endswith("_mqtt"):
            raise AttributeError(name)
        target_name = "send_" + name[len("publish_") : -len("_mqtt")]
        if hasattr(self._realtime, target_name):
            target = getattr(self._realtime, target_name)
        elif hasattr(self._static, target_name):
            target = getattr(self._static, target_name)
        else:
            raise AttributeError(name)

        async def _publish(**kwargs):
            target(
                kwargs["feedurl"],
                kwargs["agencyid"],
                kwargs["data"],
                kwargs.get("content_type", "application/json"),
                flush_producer=False,
            )

        return _publish


def poll_and_submit_realtime_feed(
    agency_id: str,
    producer_client: GeneralTransitFeedRealTimeEventProducer,
    feed_url: str,
    gtfs_rt_headers,
    route: str | None,
):
    class _RealtimeAdapter:
        def __init__(self, producer):
            self._producer = producer

        async def flush(self):
            self._producer.producer.flush()

        async def publish_general_transit_feed_real_time_vehicle_vehicle_position_mqtt(self, **kwargs):
            self._producer.send_general_transit_feed_real_time_vehicle_vehicle_position(
                kwargs["feedurl"],
                kwargs["agencyid"],
                kwargs["data"],
                kwargs.get("content_type", "application/json"),
                flush_producer=False,
            )

        async def publish_general_transit_feed_real_time_trip_trip_update_mqtt(self, **kwargs):
            self._producer.send_general_transit_feed_real_time_trip_trip_update(
                kwargs["feedurl"],
                kwargs["agencyid"],
                kwargs["data"],
                kwargs.get("content_type", "application/json"),
                flush_producer=False,
            )

        async def publish_general_transit_feed_real_time_alert_alert_mqtt(self, **kwargs):
            self._producer.send_general_transit_feed_real_time_alert_alert(
                kwargs["feedurl"],
                kwargs["agencyid"],
                kwargs["data"],
                kwargs.get("content_type", "application/json"),
                flush_producer=False,
            )

    asyncio.run(_core_poll_and_publish_realtime_feed(agency_id, _RealtimeAdapter(producer_client), feed_url, gtfs_rt_headers, route))


def fetch_and_process_schedule(
    agency_id: str,
    reference_producer_client: GeneralTransitFeedStaticEventProducer,
    gtfs_urls,
    headers,
    force_refresh: bool = False,
    cache_dir: str | None = None,
):
    old_fetch = _core.fetch_schedule_file
    old_calc = _core.calculate_file_hashes
    old_read = _core.read_schedule_file_contents
    old_iter = _core.iter_schedule_file_contents
    old_read_hashes = _core.read_file_hashes
    old_write_hashes = _core.write_file_hashes
    _core.fetch_schedule_file = fetch_schedule_file
    _core.calculate_file_hashes = calculate_file_hashes
    _core.read_schedule_file_contents = read_schedule_file_contents
    _core.iter_schedule_file_contents = iter_schedule_file_contents
    _core.read_file_hashes = read_file_hashes
    _core.write_file_hashes = write_file_hashes

    class _StaticAdapter:
        def __init__(self, producer):
            self._producer = producer

        async def flush(self):
            self._producer.producer.flush()

        async def poll(self):
            self._producer.producer.poll(0)

        def __getattr__(self, name: str):
            if not name.startswith("publish_") or not name.endswith("_mqtt"):
                raise AttributeError(name)
            target_name = "send_" + name[len("publish_") : -len("_mqtt")]
            target = getattr(self._producer, target_name)

            async def _publish(**kwargs):
                target(
                    kwargs["feedurl"],
                    kwargs["agencyid"],
                    kwargs["data"],
                    kwargs.get("content_type", "application/json"),
                    flush_producer=False,
                )

            return _publish

    try:
        asyncio.run(
            _CORE_FETCH_AND_PUBLISH_SCHEDULE(
                agency_id,
                _StaticAdapter(reference_producer_client),
                gtfs_urls,
                headers,
                force_refresh=force_refresh,
                cache_dir=cache_dir,
            )
        )
    finally:
        _core.fetch_schedule_file = old_fetch
        _core.calculate_file_hashes = old_calc
        _core.read_schedule_file_contents = old_read
        _core.iter_schedule_file_contents = old_iter
        _core.read_file_hashes = old_read_hashes
        _core.write_file_hashes = old_write_hashes


def feed_realtime_messages(
    agency_id: str,
    kafka_bootstrap_servers: str,
    kafka_topic: str,
    sasl_username: str | None,
    sasl_password: str | None,
    gtfs_rt_urls,
    gtfs_rt_headers,
    gtfs_urls,
    gtfs_headers,
    mdb_source_id: str | None,
    route: str | None,
    poll_interval: int,
    schedule_poll_interval: int,
    cloudevents_mode: str,
    cache_dir: str | None,
    force_schedule_refresh: bool,
):
    if not gtfs_rt_urls and mdb_source_id:
        gtfs_rt_urls = [get_gtfs_rt_url(mdb_source_id, cache_dir)]
    if not gtfs_urls and mdb_source_id:
        gtfs_urls = [get_gtfs_url(mdb_source_id, cache_dir)]

    publisher = _build_kafka_publisher(
        kafka_bootstrap_servers,
        kafka_topic,
        sasl_username,
        sasl_password,
        cloudevents_mode,
    )
    producer = publisher._producer
    gtfs_rt_producer = publisher._realtime
    last_schedule_completed: datetime | None = None
    schedule_lock = threading.Lock()
    schedule_thread: threading.Thread | None = None

    def _run_schedule(force_refresh: bool):
        nonlocal last_schedule_completed
        try:
            bg_static_producer = GeneralTransitFeedStaticEventProducer(producer, kafka_topic, cloudevents_mode)
            fetch_and_process_schedule(
                agency_id,
                bg_static_producer,
                gtfs_urls,
                gtfs_headers,
                force_refresh=force_refresh,
                cache_dir=cache_dir,
            )
            with schedule_lock:
                last_schedule_completed = datetime.now()
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Background: failed to fetch and process schedule: %s", exc)

    try:
        while True:
            start_time = datetime.now(timezone.utc)
            if gtfs_urls:
                with schedule_lock:
                    thread_alive = schedule_thread is not None and schedule_thread.is_alive()
                    needs_run = force_schedule_refresh or (
                        last_schedule_completed is None
                        or datetime.now() - last_schedule_completed > timedelta(seconds=schedule_poll_interval)
                    )
                if needs_run and not thread_alive:
                    schedule_thread = threading.Thread(
                        target=_run_schedule,
                        args=(force_schedule_refresh,),
                        daemon=True,
                        name="gtfs-schedule",
                    )
                    schedule_thread.start()
                    force_schedule_refresh = False

            if gtfs_rt_urls:
                for gtfs_feed_url in gtfs_rt_urls:
                    poll_and_submit_realtime_feed(agency_id, gtfs_rt_producer, gtfs_feed_url, gtfs_rt_headers, route)

            elapsed_time = datetime.now(timezone.utc) - start_time
            if elapsed_time.total_seconds() < poll_interval:
                time.sleep(poll_interval - elapsed_time.total_seconds())
    except KeyboardInterrupt:
        logger.info("Loop interrupted by user")

    if schedule_thread is not None and schedule_thread.is_alive():
        schedule_thread.join(timeout=30)
    producer.flush()


def _build_kafka_publisher(
    kafka_bootstrap_servers: str,
    kafka_topic: str,
    sasl_username: str | None,
    sasl_password: str | None,
    cloudevents_mode: str,
) -> KafkaMqttLikePublisher:
    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = {
        "bootstrap.servers": kafka_bootstrap_servers,
        "acks": "all",
        "linger.ms": 100,
        "retries": 5,
        "retry.backoff.ms": 1000,
        "batch.size": (1024 * 1024) - 512,
    }
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"
    producer = Producer(kafka_config, logger=logger)
    return KafkaMqttLikePublisher(producer, kafka_topic, cloudevents_mode)


async def run_feed(args):
    if args.log_level:
        logger.setLevel(getattr(logging, args.log_level))
    if not args.agency:
        raise ValueError("No agency specified")
    if not args.gtfs_urls and not args.gtfs_rt_urls and not args.mdb_source_id:
        raise ValueError("No GTFS URL or Mobility Database source ID specified")
    gtfs_rt_headers = [v.split("=", 1) for v in args.gtfs_rt_headers] if args.gtfs_rt_headers else None
    gtfs_headers = [v.split("=", 1) for v in args.gtfs_headers] if args.gtfs_headers else None

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic")
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        raise ValueError("No Kafka bootstrap servers specified")
    if not kafka_topic:
        raise ValueError("No Kafka topic specified")

    publisher = _build_kafka_publisher(
        kafka_bootstrap_servers,
        kafka_topic,
        sasl_username,
        sasl_password,
        args.cloudevents_mode,
    )
    await poll_and_publish_gtfs(
        agency_id=args.agency,
        publisher=publisher,
        gtfs_rt_urls=args.gtfs_rt_urls,
        gtfs_rt_headers=gtfs_rt_headers,
        gtfs_urls=args.gtfs_urls,
        gtfs_headers=gtfs_headers,
        mdb_source_id=args.mdb_source_id,
        route=args.route,
        poll_interval=args.poll_interval,
        schedule_poll_interval=args.schedule_poll_interval,
        cache_dir=args.cache_dir,
        force_schedule_refresh=args.force_schedule_refresh,
        once=False,
    )


async def main():
    parser = argparse.ArgumentParser(description="Real-time transit data bridge for the Mobility Database and GTFS")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    split_pattern = r'''(?:(?<!\\)"[^"]*"|'[^']*'|[^\s"']+)+'''

    feed_parser = subparsers.add_parser(
        "feed",
        help="poll real-time feeds and submit to a Kafka endpoint, Event Hub, or Fabric Event Stream custom endpoint",
    )
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.environ.get("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str, default=os.environ.get("KAFKA_TOPIC"))
    feed_parser.add_argument("--sasl-username", type=str, default=os.environ.get("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.environ.get("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", dest="connection_string", type=str, default=os.environ.get("CONNECTION_STRING"))
    feed_parser.add_argument("-r", "--route", default="*" if not os.environ.get("ROUTE") else os.environ.get("ROUTE"))
    feed_parser.add_argument("--gtfs-rt-urls", nargs="+", default=os.environ.get("GTFS_RT_URLS").split(",") if os.environ.get("GTFS_RT_URLS") else None)
    feed_parser.add_argument("--gtfs-urls", nargs="+", default=os.environ.get("GTFS_URLS").split(",") if os.environ.get("GTFS_URLS") else None)
    feed_parser.add_argument("-m", "--mdb-source-id", default=os.environ.get("MDB_SOURCE_ID"))
    feed_parser.add_argument("-a", "--agency", default=os.environ.get("AGENCY"))
    feed_parser.add_argument("--gtfs-rt-headers", action="append", nargs="*", default=re.findall(split_pattern, os.environ.get("GTFS_RT_HEADERS")) if os.environ.get("GTFS_RT_HEADERS") else None)
    feed_parser.add_argument("--gtfs-headers", action="append", nargs="*", default=re.findall(split_pattern, os.environ.get("GTFS_HEADERS")) if os.environ.get("GTFS_HEADERS") else None)
    feed_parser.add_argument("--poll-interval", type=float, default=float(os.environ.get("POLL_INTERVAL")) if os.environ.get("POLL_INTERVAL") else DEFAULT_POLL_INTERVAL_SECONDS)
    feed_parser.add_argument("--schedule-poll-interval", type=float, default=float(os.environ.get("SCHEDULE_POLL_INTERVAL")) if os.environ.get("SCHEDULE_POLL_INTERVAL") else DEFAULT_SCHEDULE_POLL_INTERVAL_SECONDS)
    feed_parser.add_argument("--cloudevents-mode", choices=["structured", "binary"], default="structured")
    feed_parser.add_argument("--cache-dir", type=str, default=os.environ.get("CACHE_DIR"))
    feed_parser.add_argument("--log-level", type=str, default=os.environ.get("LOG_LEVEL"), choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    feed_parser.add_argument("--force-schedule-refresh", action="store_true", default=False)
    feed_parser.set_defaults(func=run_feed)

    printfeed_parser = subparsers.add_parser("printfeed", help="Print the feed data for a route for a single request")
    printfeed_parser.add_argument("--gtfs-rt-url", required=False)
    printfeed_parser.add_argument("-m", "--mdb-source-id", required=False, default=None)
    printfeed_parser.add_argument("--header", action="append", nargs=2)
    printfeed_parser.add_argument("--cache-dir", type=str, default=os.environ.get("CACHE_DIR"))

    async def cmd_print_feed_items(args):
        if not args.gtfs_rt_url and not args.mdb_source_id:
            raise ValueError("No GTFS URL or Mobility Database source ID specified")
        headers = {k: v for k, v in args.header} if args.header else {}
        await print_feed_items(args.gtfs_rt_url, args.mdb_source_id, headers, args.cache_dir)

    printfeed_parser.set_defaults(func=cmd_print_feed_items)

    agencies_parser = subparsers.add_parser("agencies", help="get the list of transit agencies")
    agencies_parser.add_argument("--cache-dir", type=str, default=os.environ.get("CACHE_DIR"))
    agencies_parser.set_defaults(func=run_print_agencies)

    route_parser = subparsers.add_parser("routes", help="get the list of routes for an agency")
    route_parser.add_argument("gtfs_url")
    route_parser.add_argument("-m", "--mdb-source-id", required=False, default=None)
    route_parser.add_argument("--header", action="append", nargs=2)
    route_parser.add_argument("--cache-dir", type=str, default=os.environ.get("CACHE_DIR"))
    route_parser.set_defaults(func=run_print_routes)

    stops_parser = subparsers.add_parser("stops", help="get the list of stops for a route")
    stops_parser.add_argument("-r", "--route", required=False)
    stops_parser.add_argument("gtfs_url")
    stops_parser.add_argument("-m", "--mdb-source-id", required=False, default=None)
    stops_parser.add_argument("--header", action="append", nargs=2)
    stops_parser.add_argument("--cache-dir", type=str, default=os.environ.get("CACHE_DIR"))
    stops_parser.set_defaults(func=run_print_stops)

    args = parser.parse_args()
    if hasattr(args, "func") and callable(args.func):
        await args.func(args)
    else:
        parser.print_help()


def cli():
    asyncio.run(main())


if __name__ == "__main__":
    cli()
