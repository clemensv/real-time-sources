"""AMQP 1.0 feeder application for TfL Santander Cycles (BikePoint).

Wraps the upstream BikePoint poller from :mod:`tfl_cycles_core` and the
generated :class:`UKGovTfLCyclesAmqpStationsProducer`. Supports three
deployment modes, chosen at runtime:

* **Generic AMQP 1.0** (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid
  Dispatch, ...): SASL PLAIN with ``--username``/``--password`` against
  ``amqp://`` (port 5672) or ``amqps://`` (port 5671).
* **Azure Service Bus / Event Hubs** with Entra ID: pass ``--auth-mode entra``
  and ``DefaultAzureCredential`` is used to acquire a JWT presented via the AMQP
  CBS ``$cbs`` link (``put-token``).
* **SAS** (``--auth-mode sas``) for SAS-only namespaces or the Service Bus
  emulator.

All events are written to a single AMQP address (queue or topic), set via
``--address`` / ``AMQP_ADDRESS``. CloudEvent type, source, and subject metadata
are carried as AMQP message properties (binary mode) or in the JSON body
(structured mode).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from tfl_cycles_core import (
    FEED_URL_ROOT,
    ParsedStation,
    TfLCyclesAPI,
    load_state,
    parse_bikepoint,
    save_state,
)
from tfl_cycles_amqp_producer_data import StationInformation, StationStatus
from tfl_cycles_amqp_producer_amqp_producer.producer import UKGovTfLCyclesAmqpStationsProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

logger = logging.getLogger(__name__)


def _build_info(p: ParsedStation) -> StationInformation:
    return StationInformation(
        station_id=p.station_id,
        name=p.name,
        lat=float(p.lat) if p.lat is not None else 0.0,
        lon=float(p.lon) if p.lon is not None else 0.0,
        terminal_name=p.terminal_name,
        capacity=p.capacity,
        temporary=p.temporary,
        install_date=p.install_date,
        removal_date=p.removal_date,
    )


def _build_status(p: ParsedStation) -> StationStatus:
    return StationStatus(
        station_id=p.station_id,
        num_bikes_available=p.num_bikes_available if p.num_bikes_available is not None else 0,
        num_standard_bikes_available=p.num_standard_bikes_available,
        num_ebikes_available=p.num_ebikes_available,
        num_empty_docks=p.num_empty_docks if p.num_empty_docks is not None else 0,
        num_docks=p.num_docks,
        is_installed=p.is_installed if p.is_installed is not None else False,
        is_locked=p.is_locked if p.is_locked is not None else False,
        modified=p.modified,
    )


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:  # pylint: disable=broad-except
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                            attempt + 1, max_attempts, e, delay)
            time.sleep(delay)


def _build_producer(
    *,
    host: str,
    port: int,
    address: str,
    use_tls: bool,
    content_mode: str,
    auth_mode: str,
    username: Optional[str],
    password: Optional[str],
    entra_audience: str,
    entra_client_id: Optional[str],
    sas_key_name: Optional[str],
    sas_key: Optional[str],
) -> UKGovTfLCyclesAmqpStationsProducer:
    if auth_mode == "entra":
        try:
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "auth-mode=entra requires azure-identity. Reinstall the package."
            ) from exc

        if entra_client_id:
            credential = ManagedIdentityCredential(client_id=entra_client_id)
        else:
            credential = DefaultAzureCredential()

        logger.info(
            "Using Entra ID auth via CBS (host=%s, address=%s, audience=%s)",
            host, address, entra_audience,
        )
        return UKGovTfLCyclesAmqpStationsProducer(
            host=host,
            address=address,
            port=port,
            content_mode=content_mode,  # type: ignore[arg-type]
            credential=credential,
            entra_audience=entra_audience,
            use_tls=use_tls,
        )

    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError(
                "auth-mode=sas requires --sas-key-name and --sas-key "
                "(or AMQP_SAS_KEY_NAME / AMQP_SAS_KEY env vars)."
            )
        logger.info(
            "Using SAS auth via CBS (host=%s, address=%s, tls=%s, key_name=%s)",
            host, address, use_tls, sas_key_name,
        )
        return UKGovTfLCyclesAmqpStationsProducer(
            host=host,
            address=address,
            port=port,
            content_mode=content_mode,  # type: ignore[arg-type]
            sas_key_name=sas_key_name,
            sas_key=sas_key,
            use_tls=use_tls,
        )

    logger.info(
        "Using SASL PLAIN auth (host=%s:%s, address=%s, tls=%s, user=%s)",
        host, port, address, use_tls, username or "<anonymous>",
    )
    return UKGovTfLCyclesAmqpStationsProducer(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=content_mode,  # type: ignore[arg-type]
        use_tls=use_tls,
    )


def feed(
    api: TfLCyclesAPI,
    producer: UKGovTfLCyclesAmqpStationsProducer,
    polling_interval: int,
    *,
    state_file: str = "",
    once: bool = False,
    reference_refresh_interval: int = 3600,
) -> None:
    previous_status: Dict[str, Any] = load_state(state_file)
    previous_info: Dict[str, Any] = {}
    last_ref_emit = 0.0

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                bikepoints = api.list_bikepoints()
                parsed = [parse_bikepoint(bp) for bp in bikepoints]
                now_ts = time.time()
                reference_due = (now_ts - last_ref_emit) >= reference_refresh_interval

                info_count = 0
                for p in parsed:
                    signature = p.info_signature()
                    if reference_due or previous_info.get(p.station_id) != signature:
                        try:
                            producer.send_station_information(
                                data=_build_info(p),
                                _feedurl=f"{FEED_URL_ROOT}/BikePoint/{p.station_id}",
                                _station_id=p.station_id,
                            )
                            info_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing station info for %s: %s", p.station_id, e)
                        previous_info[p.station_id] = signature
                if reference_due:
                    last_ref_emit = now_ts

                status_count = 0
                for p in parsed:
                    signature = p.status_signature()
                    if previous_status.get(p.station_id) != signature:
                        try:
                            producer.send_station_status(
                                data=_build_status(p),
                                _feedurl=f"{FEED_URL_ROOT}/BikePoint/{p.station_id}",
                                _station_id=p.station_id,
                            )
                            status_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing station status for %s: %s", p.station_id, e)
                        previous_status[p.station_id] = signature

                save_state(state_file, previous_status)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s station info + %s status events in %.1fs. Sleeping until %s.",
                    info_count,
                    status_count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                time.sleep(polling_interval)
    finally:
        try:
            producer.close()
        except Exception:  # pylint: disable=broad-except
            pass


def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TfL Santander Cycles -> AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed BikePoint reference and availability CloudEvents over AMQP 1.0")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"),
                             help="AMQP broker URL (e.g. amqp://localhost:5672/queue, amqps://ns.servicebus.windows.net:5671/queue)")
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"),
                             help="AMQP broker hostname (alternative to --broker-url)")
    feed_parser.add_argument("--port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None,
                             help="AMQP broker port (default 5672, or 5671 with --tls)")
    feed_parser.add_argument("--address", type=str,
                             default=os.getenv("AMQP_ADDRESS", "tfl-cycles"),
                             help="AMQP address (queue or topic name). Default: tfl-cycles")
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--content-mode", type=str,
                             default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"],
                             help="CloudEvents content mode (default: binary)")
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=polling_interval_default,
                             help="Polling interval in seconds")
    feed_parser.add_argument("--reference-refresh-interval", type=int,
                             default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")),
                             help="Seconds between full re-emissions of station reference data")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.tfl_cycles_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle.")
    feed_parser.add_argument("--auth-mode", type=str,
                             default=os.getenv("AMQP_AUTH_MODE", "password"),
                             choices=["password", "entra", "sas"],
                             help="Authentication mode: 'password' (default, SASL PLAIN), "
                                  "'entra' (AMQP CBS with Azure Entra ID via DefaultAzureCredential, "
                                  "targets Azure Service Bus / Event Hubs), or 'sas' (AMQP CBS with "
                                  "a Shared Access Signature, for SAS-only namespaces or the Service "
                                  "Bus emulator).")
    feed_parser.add_argument("--entra-audience", type=str,
                             default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
                             help=f"Entra token audience. Default: {DEFAULT_ENTRA_AUDIENCE_SERVICEBUS} "
                                  f"(Service Bus). Use {DEFAULT_ENTRA_AUDIENCE_EVENTHUBS} for Event Hubs.")
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"),
                             help="Optional user-assigned managed identity client id; "
                                  "defaults to DefaultAzureCredential resolution.")
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"),
                             help="SAS policy / key name (e.g. RootManageSharedAccessKey). "
                                  "Required with --auth-mode=sas.")
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"),
                             help="SAS key value (base64) used to sign tokens. "
                                  "Required with --auth-mode=sas.")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password

    if not address:
        parser.error("--address is required (or include it in --broker-url path)")

    api = TfLCyclesAPI()
    producer = _retry_producer_init(lambda: _build_producer(
        host=host,
        port=port,
        address=address,
        use_tls=tls,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        username=username,
        password=password,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
    ))

    feed(
        api,
        producer,
        args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        reference_refresh_interval=args.reference_refresh_interval,
    )


if __name__ == "__main__":
    main()
