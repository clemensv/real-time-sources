"""AMQP 1.0 feeder application for PegelOnline.

Wraps the upstream poller from :mod:`pegelonline_core` and the generated
:class:`DeWsvPegelonlineAmqpProducer`. Supports two deployment modes,
chosen at runtime:

* **Generic AMQP 1.0** (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid
  Dispatch, ...): SASL PLAIN with ``--username``/``--password`` against
  ``amqp://`` (port 5672) or ``amqps://`` (port 5671).
* **Azure Service Bus / Event Hubs** with Entra ID: pass
  ``--auth-mode entra`` and ``DefaultAzureCredential`` is used to acquire
  a JWT, which the generated producer presents via the AMQP CBS
  ``$cbs`` link (``put-token``). No SAS-key minting, no refresh loop in
  this process — the generated handler owns the connection lifecycle.

All events are written to a single AMQP address (queue or topic), set
via ``--address`` / ``AMQP_ADDRESS``. CloudEvent type, source, and
subject metadata are carried as AMQP message properties (binary mode) or
in the JSON body (structured mode).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from pegelonline_core import FEED_URL_ROOT, PegelOnlineAPI, load_state, save_state
from pegelonline_amqp_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement
from pegelonline_amqp_producer_data.de.wsv.pegelonline.station import Station
from pegelonline_amqp_producer_data.de.wsv.pegelonline.water import Water
from pegelonline_amqp_producer_amqp_producer.producer import DeWsvPegelonlineAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

logger = logging.getLogger(__name__)


def _build_station(raw: Dict[str, Any]) -> Station:
    water = raw.get("water") or {}
    return Station(
        station_id=raw.get("uuid"),
        number=raw.get("number"),
        shortname=raw.get("shortname"),
        longname=raw.get("longname"),
        km=raw.get("km"),
        agency=raw.get("agency"),
        longitude=raw.get("longitude") if raw.get("longitude") is not None else -1,
        latitude=raw.get("latitude") if raw.get("latitude") is not None else -1,
        water=Water(shortname=water.get("shortname"), longname=water.get("longname")),
    )


def _build_measurement(station_id: str, raw: Dict[str, Any]) -> CurrentMeasurement:
    return CurrentMeasurement(
        station_id=station_id,
        timestamp=raw["timestamp"],
        value=raw["value"],
        stateMnwMhw=raw.get("stateMnwMhw"),
        stateNswHsw=raw.get("stateNswHsw"),
        trend=raw.get("trend"),
    )


def _water_shortname(raw_station: Dict[str, Any]) -> str:
    """Pick the URL-safe water shortname carried as AMQP application property.

    Mirrors the helper in ``pegelonline_mqtt`` so SB/EH subscription filters
    and AMQP routers can route by waterway without cracking the JSON body.
    """
    water = raw_station.get("water") or {}
    raw = (water.get("shortname") or water.get("longname") or "unknown").strip().lower()
    out_chars = []
    for ch in raw:
        if ch.isalnum() or ch in ("-", "_"):
            out_chars.append(ch)
        else:
            out_chars.append("-")
    safe = "".join(out_chars).strip("-")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe or "unknown"


def _publish_stations(
    api: PegelOnlineAPI,
    producer: DeWsvPegelonlineAmqpProducer,
    stations: list,
    station_index: Dict[str, Dict[str, Any]],
) -> None:
    for station in stations:
        station_index[station["uuid"]] = station
        producer.send_station(
            data=_build_station(station),
            _feedurl=f"{FEED_URL_ROOT}/stations/{station['shortname']}",
            _station_id=station["uuid"],
            _water_shortname=_water_shortname(station),
        )


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
) -> DeWsvPegelonlineAmqpProducer:
    if auth_mode == "entra":
        # Lazy import so the package still installs when azure-identity
        # is missing in non-Azure deployments (it's a hard dep, but the
        # check helps surface a clearer error if someone trims it out).
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
        return DeWsvPegelonlineAmqpProducer(
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
        return DeWsvPegelonlineAmqpProducer(
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
    return DeWsvPegelonlineAmqpProducer(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=content_mode,  # type: ignore[arg-type]
        use_tls=use_tls,
    )


def feed(
    api: PegelOnlineAPI,
    producer: DeWsvPegelonlineAmqpProducer,
    polling_interval: int,
    *,
    state_file: str = "",
    once: bool = False,
) -> None:
    previous_readings: Dict[str, Dict[str, Any]] = load_state(state_file)
    station_index: Dict[str, Dict[str, Any]] = {}

    stations = api.list_stations()
    logger.info("Publishing %d station info events to AMQP address", len(stations))
    _publish_stations(api, producer, stations, station_index)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                count = 0
                start_time = datetime.now(timezone.utc)
                measurements = api.get_water_levels()
                for station_id, measurement in measurements.items():
                    prior = previous_readings.get(station_id)
                    if prior is not None and measurement.get("timestamp") == prior.get("timestamp"):
                        continue
                    count += 1
                    station_meta = station_index.get(station_id) or {}
                    try:
                        producer.send_current_measurement(
                            data=_build_measurement(station_id, measurement),
                            _feedurl=f"{FEED_URL_ROOT}/stations/{station_id}/W/currentmeasurement.json",
                            _station_id=station_id,
                            _water_shortname=_water_shortname(station_meta),
                        )
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error publishing measurement for %s: %s", station_id, e)
                    previous_readings[station_id] = measurement

                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s current measurements in %s seconds. Sleeping until %s.",
                    count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    import time
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                import time
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
    parser = argparse.ArgumentParser(description="PegelOnline → AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed stations and updates as CloudEvents over AMQP 1.0")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"),
                             help="AMQP broker URL (e.g. amqp://localhost:5672/queue, amqps://ns.servicebus.windows.net:5671/queue)")
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"),
                             help="AMQP broker hostname (alternative to --broker-url)")
    feed_parser.add_argument("--port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None,
                             help="AMQP broker port (default 5672, or 5671 with --tls)")
    feed_parser.add_argument("--address", type=str,
                             default=os.getenv("AMQP_ADDRESS", "pegelonline"),
                             help="AMQP address (queue or topic name). Default: pegelonline")
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
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.pegelonline_state.json")))
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

    api = PegelOnlineAPI()
    producer = _build_producer(
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
    )

    feed(
        api,
        producer,
        args.polling_interval,
        state_file=args.state_file,
        once=args.once,
    )


if __name__ == "__main__":
    main()
