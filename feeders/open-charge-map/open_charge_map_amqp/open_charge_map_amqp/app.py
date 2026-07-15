"""AMQP 1.0 feeder application for Open Charge Map.

Wraps the Open Charge Map reference and POI pollers from
:mod:`open_charge_map_core` and the generated
:class:`IOOpenChargeMapLocationsAmqpProducer` /
:class:`IOOpenChargeMapReferenceAmqpProducer`. Supports three deployment modes,
chosen at runtime:

* **Generic AMQP 1.0** (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid
  Dispatch, ...): SASL PLAIN with ``--username``/``--password`` against
  ``amqp://`` (port 5672) or ``amqps://`` (port 5671).
* **Azure Service Bus / Event Hubs** with Entra ID: pass ``--auth-mode entra``
  and ``DefaultAzureCredential`` is used to acquire a JWT presented via the AMQP
  CBS ``$cbs`` link (``put-token``).
* **SAS** (``--auth-mode sas``) for SAS-only namespaces or the Service Bus
  emulator.

Both producer classes write to the same AMQP address (``--address`` /
``AMQP_ADDRESS``). CloudEvent type, source, and subject metadata are carried as
AMQP message properties (binary mode) or in the JSON body (structured mode).
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

from open_charge_map_core import (
    POI_URL,
    REFERENCE_URL,
    FeedConfig,
    OpenChargeMapAPI,
    ParsedLocation,
    ParsedReference,
    load_state,
    parse_ocm_datetime,
    parse_poi,
    parse_reference_data,
    save_state,
)
from open_charge_map_amqp_producer_data import (
    ChargerType,
    ChargingLocation,
    Connection,
    ConnectionType,
    Country,
    CurrentType,
    DataProvider,
    Operator,
    StatusType,
    SubmissionStatusType,
    UsageType,
)
from open_charge_map_amqp_producer_amqp_producer.producer import (
    IOOpenChargeMapLocationsAmqpProducer,
    IOOpenChargeMapReferenceAmqpProducer,
)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

logger = logging.getLogger(__name__)

REF_CLASSES = {
    "operator": Operator,
    "connection_type": ConnectionType,
    "current_type": CurrentType,
    "charger_type": ChargerType,
    "country": Country,
    "data_provider": DataProvider,
    "status_type": StatusType,
    "usage_type": UsageType,
    "submission_status_type": SubmissionStatusType,
}


def _build_location(p: ParsedLocation) -> ChargingLocation:
    data = dataclasses.asdict(p)
    connections = data.pop("connections")
    if data.get("latitude") is None:
        data["latitude"] = 0.0
    if data.get("longitude") is None:
        data["longitude"] = 0.0
    return ChargingLocation(
        **data,
        connections=[Connection(**c) for c in connections],
    )


def _build_reference(r: ParsedReference):
    return REF_CLASSES[r.reference_type](**r.fields)


def _initial_watermark(state: Dict[str, Any], modified_since_days: int) -> datetime:
    marker = state.get("watermark")
    parsed = parse_ocm_datetime(marker) if marker else None
    if parsed is not None:
        return parsed
    return datetime.now(timezone.utc) - timedelta(days=modified_since_days)


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:  # pylint: disable=broad-except
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning(
                "Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                attempt + 1, max_attempts, e, delay,
            )
            time.sleep(delay)


def _build_producers(
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
) -> Tuple[IOOpenChargeMapLocationsAmqpProducer, IOOpenChargeMapReferenceAmqpProducer]:
    credential = None
    kwargs: Dict[str, Any] = {
        "host": host,
        "address": address,
        "port": port,
        "content_mode": content_mode,
        "use_tls": use_tls,
    }
    if auth_mode == "entra":
        try:
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "auth-mode=entra requires azure-identity. Reinstall the package."
            ) from exc
        credential = (
            ManagedIdentityCredential(client_id=entra_client_id)
            if entra_client_id
            else DefaultAzureCredential()
        )
        logger.info(
            "Using Entra ID auth via CBS (host=%s, address=%s, audience=%s)",
            host, address, entra_audience,
        )
        kwargs.update(credential=credential, entra_audience=entra_audience)
    elif auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError(
                "auth-mode=sas requires --sas-key-name and --sas-key "
                "(or AMQP_SAS_KEY_NAME / AMQP_SAS_KEY env vars)."
            )
        logger.info(
            "Using SAS auth via CBS (host=%s, address=%s, tls=%s, key_name=%s)",
            host, address, use_tls, sas_key_name,
        )
        kwargs.update(sas_key_name=sas_key_name, sas_key=sas_key)
    else:
        logger.info(
            "Using SASL PLAIN auth (host=%s:%s, address=%s, tls=%s, user=%s)",
            host, port, address, use_tls, username or "<anonymous>",
        )
        kwargs.update(username=username, password=password)

    loc = IOOpenChargeMapLocationsAmqpProducer(**kwargs)  # type: ignore[arg-type]
    ref = IOOpenChargeMapReferenceAmqpProducer(**kwargs)  # type: ignore[arg-type]
    return loc, ref


def feed(
    api: OpenChargeMapAPI,
    loc_producer: IOOpenChargeMapLocationsAmqpProducer,
    ref_producer: IOOpenChargeMapReferenceAmqpProducer,
    cfg: FeedConfig,
) -> None:
    state: Dict[str, Any] = load_state(cfg.state_file)
    poi_sigs: Dict[str, Any] = state.get("pois", {})
    watermark = _initial_watermark(state, cfg.modified_since_days)
    last_ref_emit = 0.0

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                now_ts = time.time()
                reference_due = (now_ts - last_ref_emit) >= cfg.reference_refresh_interval

                ref_count = 0
                if reference_due:
                    references = parse_reference_data(api.list_reference_data())
                    for r in references:
                        try:
                            method = getattr(ref_producer, f"send_{r.reference_type}")
                            method(
                                data=_build_reference(r),
                                _feedurl=f"{REFERENCE_URL}#{r.reference_type}/{r.reference_id}",
                                _reference_type=r.reference_type,
                                _reference_id=str(r.reference_id),
                            )
                            ref_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error(
                                "Error publishing reference %s/%s: %s",
                                r.reference_type, r.reference_id, e,
                            )
                    last_ref_emit = now_ts

                pois = api.list_pois(
                    modified_since=watermark,
                    country_code=cfg.country_code,
                    max_results=cfg.max_results,
                    opendata=cfg.opendata,
                )
                loc_count = 0
                max_change = watermark
                for raw in pois:
                    p = parse_poi(raw)
                    if p.poi_id == 0:
                        continue
                    signature = p.change_signature()
                    key = str(p.poi_id)
                    if poi_sigs.get(key) != signature:
                        try:
                            loc_producer.send_charging_location(
                                data=_build_location(p),
                                _feedurl=f"{POI_URL}#{p.poi_id}",
                                _poi_id=key,
                            )
                            loc_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing location %s: %s", p.poi_id, e)
                        poi_sigs[key] = signature
                    latest = p.latest_change()
                    if latest is not None and latest > max_change:
                        max_change = latest

                watermark = max_change
                save_state(cfg.state_file, {"watermark": watermark.isoformat(), "pois": poi_sigs})
                end_time = datetime.now(timezone.utc)
                effective = max(
                    0, cfg.polling_interval - (end_time - start_time).total_seconds()
                )
                logger.info(
                    "Published %s reference + %s location events in %.1fs (watermark=%s). "
                    "Sleeping until %s.",
                    ref_count,
                    loc_count,
                    (end_time - start_time).total_seconds(),
                    watermark.isoformat(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                if cfg.once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                time.sleep(cfg.polling_interval)
    finally:
        for producer in (loc_producer, ref_producer):
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
    parser = argparse.ArgumentParser(description="Open Charge Map -> AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed", help="Feed Open Charge Map reference and location CloudEvents over AMQP 1.0"
    )
    feed_parser.add_argument(
        "--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"),
        help="AMQP broker URL (e.g. amqp://localhost:5672/queue, "
        "amqps://ns.servicebus.windows.net:5671/queue)",
    )
    feed_parser.add_argument(
        "--host", type=str, default=os.getenv("AMQP_HOST"),
        help="AMQP broker hostname (alternative to --broker-url)",
    )
    feed_parser.add_argument(
        "--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None,
        help="AMQP broker port (default 5672, or 5671 with --tls)",
    )
    feed_parser.add_argument(
        "--address", type=str, default=os.getenv("AMQP_ADDRESS", "open-charge-map"),
        help="AMQP address (queue or topic name). Default: open-charge-map",
    )
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument(
        "--tls", action="store_true",
        default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"),
    )
    feed_parser.add_argument(
        "--content-mode", type=str, default=os.getenv("AMQP_CONTENT_MODE", "binary"),
        choices=["binary", "structured"],
        help="CloudEvents content mode (default: binary)",
    )
    feed_parser.add_argument(
        "-i", "--polling-interval", type=int,
        default=int(os.getenv("POLLING_INTERVAL", "600")),
        help="Delta polling interval in seconds",
    )
    feed_parser.add_argument(
        "--reference-refresh-interval", type=int,
        default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "86400")),
        help="Seconds between full re-emissions of reference data",
    )
    feed_parser.add_argument(
        "--country-code", type=str, default=os.getenv("OCM_COUNTRYCODE"),
        help="Optional ISO country code to scope the POI query (default: global)",
    )
    feed_parser.add_argument(
        "--modified-since-days", type=int,
        default=int(os.getenv("OCM_MODIFIED_SINCE_DAYS", "1")),
        help="Initial look-back window in days for the first delta poll",
    )
    feed_parser.add_argument(
        "--max-results", type=int, default=int(os.getenv("OCM_MAX_RESULTS", "5000")),
        help="Maximum POI records requested per poll",
    )
    feed_parser.add_argument(
        "--state-file", type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.open_charge_map_state.json")),
    )
    feed_parser.add_argument(
        "--once", action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle.",
    )
    feed_parser.add_argument(
        "--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"),
        choices=["password", "entra", "sas"],
        help="Authentication mode: 'password' (default, SASL PLAIN), "
        "'entra' (AMQP CBS with Azure Entra ID via DefaultAzureCredential, "
        "targets Azure Service Bus / Event Hubs), or 'sas' (AMQP CBS with "
        "a Shared Access Signature, for SAS-only namespaces or the Service "
        "Bus emulator).",
    )
    feed_parser.add_argument(
        "--entra-audience", type=str,
        default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        help=f"Entra token audience. Default: {DEFAULT_ENTRA_AUDIENCE_SERVICEBUS} "
        f"(Service Bus). Use {DEFAULT_ENTRA_AUDIENCE_EVENTHUBS} for Event Hubs.",
    )
    feed_parser.add_argument(
        "--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        help="Optional user-assigned managed identity client id; "
        "defaults to DefaultAzureCredential resolution.",
    )
    feed_parser.add_argument(
        "--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"),
        help="SAS policy / key name (e.g. RootManageSharedAccessKey). "
        "Required with --auth-mode=sas.",
    )
    feed_parser.add_argument(
        "--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"),
        help="SAS key value (base64) used to sign tokens. Required with --auth-mode=sas.",
    )
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

    cfg = FeedConfig.from_env(
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        reference_refresh_interval=args.reference_refresh_interval,
        country_code=args.country_code,
        modified_since_days=args.modified_since_days,
        max_results=args.max_results,
    )
    api = OpenChargeMapAPI()
    loc_producer, ref_producer = _retry_producer_init(
        lambda: _build_producers(
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
    )

    feed(api, loc_producer, ref_producer, cfg)


if __name__ == "__main__":
    main()
