"""NOAA Tides & Currents → AMQP 1.0 bridge.

Polls the live NOAA datagetter API for every configured station and product and
publishes the results as CloudEvents over AMQP 1.0 to generic brokers and Azure
Service Bus / Event Hubs. Reference station metadata is emitted first, then
telemetry is polled in a loop. Acquisition and record normalisation are shared
with the Kafka and MQTT feeders via the transport-agnostic :mod:`noaa_core`
package.
"""

import argparse
import dataclasses
import enum
import inspect
import logging
import os
import sys
import time
import typing
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import noaa_core
from noaa_core import NOAAClient
import noaa_amqp_producer_data as ncd
from noaa_amqp_producer_amqp_producer.producer import *  # noqa: F401,F403  (AmqpProducer subclass)


def _slug(value):
    """Render a routing-safe region value (NOAA region is often absent)."""
    return str(value or "unknown").replace("/", "-").replace(" ", "-").lower()


_SEND_SUFFIX = {
    "water_level": "water_level",
    "predictions": "predictions",
    "air_temperature": "air_temperature",
    "wind": "wind",
    "air_pressure": "air_pressure",
    "water_temperature": "water_temperature",
    "conductivity": "conductivity",
    "visibility": "visibility",
    "humidity": "humidity",
    "salinity": "salinity",
    "currents": "currents",
    "currents_predictions": "current_predictions",
}


# ---------------------------------------------------------------------------
# Deterministic mock harness (MOCK_MODE).
#
# The Docker E2E AMQP flow runs the container with MOCK_MODE=true + ONCE_MODE
# and asserts that one instance of *every* event type reaches the broker. Real
# upstream polling can never satisfy that in a single pass (a tide station has
# no salinity/conductivity/currents), so MOCK_MODE synthesises one sample of
# each generated send_* type. Normal operation polls the live NOAA API.
# ---------------------------------------------------------------------------
def _unwrap_type(annotation):
    """Strip Optional/Union wrappers down to the first concrete type."""
    origin = typing.get_origin(annotation)
    if origin is None:
        return annotation
    args = [a for a in typing.get_args(annotation) if a is not type(None)]
    return args[0] if args else str


def _sample_value(name, annotation):
    """Deterministic sample value for a generated data-class field (MOCK_MODE).

    Type-driven first (enums, numbers, bools), then a small name-based fallback,
    so every synthetic instance constructs and serialises without contacting the
    live NOAA API.
    """
    typ = _unwrap_type(annotation)
    try:
        if isinstance(typ, type) and issubclass(typ, enum.Enum):
            return list(typ)[0]
    except TypeError:
        pass
    if typ is bool or "bool" in str(typ):
        return False
    if typ is int or "int" in str(typ):
        return 1
    if typ is float or "float" in str(typ) or "double" in str(typ):
        return 1.0
    lname = name.lower().rstrip("_")
    if "lat" in lname:
        return 45.0
    if "lon" in lname:
        return -75.0
    if "time" in lname or "date" in lname:
        return datetime.now(timezone.utc).isoformat()
    if lname in ("station_id", "station_number", "site_number"):
        return "mock-station"
    if lname == "region":
        return "PACIFIC"
    return "mock"





_DATA_CLASSES = {
    "predictions": ncd.Predictions,
    "air_temperature": ncd.AirTemperature,
    "wind": ncd.Wind,
    "air_pressure": ncd.AirPressure,
    "water_temperature": ncd.WaterTemperature,
    "conductivity": ncd.Conductivity,
    "visibility": ncd.Visibility,
    "humidity": ncd.Humidity,
    "salinity": ncd.Salinity,
    "currents": ncd.Currents,
    "currents_predictions": ncd.CurrentPredictions,
}


def _build_data(product, station_id, region, ts_iso, fields):
    """Build the generated data class for a product from normalised fields."""
    fields = dict(fields)
    if product == "water_level":
        preliminary = fields.pop("quality_preliminary")
        return ncd.WaterLevel(
            station_id=station_id,
            region=region,
            timestamp=ts_iso,
            quality=ncd.QualityLevel.Preliminary if preliminary else ncd.QualityLevel.Verified,
            **fields,
        )
    return _DATA_CLASSES[product](
        station_id=station_id, region=region, timestamp=ts_iso, **fields
    )


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def _build_producer(cls, host, port, address, tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return cls(host=host, address=address, port=port, content_mode=content_mode, credential=cred, entra_audience=entra_audience, use_tls=tls)
    if auth_mode == "sas":
        return cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=tls)
    return cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=tls)


def _send_station(producer, station):
    producer.send_station(
        data=station,
        _station_id=station.station_id,
        _region=_slug(getattr(station, "region", None)),
    )


def _send_telemetry(producer, product, station_id, region_slug, obj, time_iso):
    method = getattr(producer, "send_" + _SEND_SUFFIX[product])
    method(data=obj, _station_id=station_id, _region=region_slug, _time=time_iso)


def _mock_build(cls, **overrides):
    """Construct a generated data class with deterministic sample field values.

    Overrides that do not correspond to a field on ``cls`` are ignored, so the
    same override set can be passed to every event type.
    """
    try:
        hints = typing.get_type_hints(cls)
    except Exception:  # pragma: no cover - fall back to raw annotations
        hints = {}
    kwargs = {}
    for f in dataclasses.fields(cls):
        if f.name in overrides:
            kwargs[f.name] = overrides[f.name]
        else:
            kwargs[f.name] = _sample_value(f.name, hints.get(f.name, f.type))
    return cls(**kwargs)


def _emit_mock(producer):
    """MOCK_MODE: emit one synthetic instance of every event type, no polling.

    The Docker E2E AMQP flow runs the container with MOCK_MODE=true + ONCE_MODE
    and asserts the Station reference type (plus best-effort telemetry types)
    reach the broker. Live polling cannot satisfy that in a single pass, so we
    synthesise one sample of each generated send_* type instead.
    """
    region = "PACIFIC"
    region_slug = _slug(region)
    ts_iso = datetime.now(timezone.utc).isoformat()
    station = _mock_build(ncd.Station, station_id="mock-station", region=region)
    _send_station(producer, station)
    logging.info("MOCK_MODE: emitted station mock-station")
    classes = {"water_level": ncd.WaterLevel, **_DATA_CLASSES}
    for product, cls in classes.items():
        try:
            obj = _mock_build(cls, station_id="mock-station", region=region, timestamp=ts_iso)
            _send_telemetry(producer, product, "mock-station", region_slug, obj, ts_iso)
            logging.info("MOCK_MODE: emitted %s", product)
        except Exception as exc:  # best-effort telemetry; Station above is required
            logging.warning("MOCK_MODE: skipped %s: %s", product, exc)


def feed(
    host,
    port,
    address="noaa",
    *,
    username=None,
    password=None,
    tls=False,
    content_mode="binary",
    auth_mode="password",
    entra_audience="https://servicebus.azure.net/.default",
    entra_client_id=None,
    sas_key_name=None,
    sas_key=None,
    station=None,
    state_file=None,
    polling_interval=300,
    once=False,
    mock=False,
):
    cls = next(obj for obj in globals().values() if isinstance(obj, type) and obj.__name__.endswith("AmqpProducer"))
    producer = _retry_producer_init(lambda: _build_producer(cls, host, port, address, tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key))
    api = NOAAClient()
    try:
        if mock:
            _emit_mock(producer)
            return
        raw_stations = api.fetch_stations_raw()
        stations = ncd.Station.schema().load(raw_stations, many=True)  # pylint: disable=no-member
        stations = noaa_core.select_stations(stations, station)
        if station and not stations:
            sys.exit(1)

        # Reference data first.
        for st in stations:
            _send_station(producer, st)

        last_polled = noaa_core.load_last_polled_times(state_file)
        while True:
            for st in stations:
                station_id = st.station_id
                # `region` is a required string in the telemetry schemas; many
                # NOAA stations have no region, so default to a stable
                # placeholder rather than emitting null.
                region = getattr(st, "region", None) or "unknown"
                region_slug = _slug(region)
                datum = NOAAClient.datum_for_tide_type(getattr(st, "tideType", None))
                for product in noaa_core.PRODUCT_ORDER:
                    last_time = last_polled.get(product, {}).get(
                        station_id, datetime.now(timezone.utc) - timedelta(hours=24)
                    )
                    records = api.poll_product(product, station_id, datum, last_time)
                    print(f"Polling {product} for station {station_id}: {len(records)} new records since {last_time}")
                    max_ts = last_time
                    for record in records:
                        ts = noaa_core.record_timestamp(product, record)
                        fields = noaa_core.extract_fields(product, record)
                        obj = _build_data(product, station_id, region, ts.isoformat(), fields)
                        _send_telemetry(producer, product, station_id, region_slug, obj, ts.isoformat())
                        if ts > max_ts:
                            max_ts = ts
                    if records:
                        last_polled.setdefault(product, {})[station_id] = max_ts
                        noaa_core.save_last_polled_times(state_file, last_polled)
            if once:
                break
            time.sleep(polling_interval)
    finally:
        close = getattr(producer, "close", None)
        if close:
            close()


def _parse_broker_url(url):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    tls = (parsed.scheme or "amqp").lower() in ("amqps", "ssl", "tls")
    return (
        parsed.hostname or "localhost",
        parsed.port or (5671 if tls else 5672),
        tls,
        parsed.username,
        parsed.password,
        (parsed.path or "").lstrip("/") or None,
    )


def main(argv=None):
    logging.basicConfig(level=logging.INFO)
    p = argparse.ArgumentParser(description="noaa AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")
    f = sub.add_parser("feed")
    f.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    f.add_argument("--broker-host", default=os.getenv("AMQP_HOST"))
    f.add_argument("--broker-port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    f.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "noaa"))
    f.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    f.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    f.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    f.add_argument("--content-mode", default=os.getenv("AMQP_CONTENT_MODE", "binary"), choices=["binary", "structured"])
    f.add_argument("--auth-mode", default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra", "sas"])
    f.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", "https://servicebus.azure.net/.default"))
    f.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    f.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    f.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    f.add_argument(
        "--station",
        default=os.getenv("NOAA_STATIONS") or os.getenv("NOAA_STATION"),
        help="Comma-separated list of station IDs to poll. If omitted, all stations are polled.",
    )
    f.add_argument("--state-file", default=noaa_core.default_last_polled_file(), help="File storing last-polled timestamps per station/product.")
    f.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("NOAA_POLLING_INTERVAL", "300")), help="Seconds between poll cycles.")
    f.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    f.add_argument("--mock", action="store_true", default=os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"), help="Emit one synthetic instance of every event type instead of polling NOAA (used by Docker E2E).")
    args = p.parse_args(argv)
    if args.command != "feed":
        p.print_help()
        return
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        port = args.broker_port or port
        tls = tls or args.tls
        address = path or args.address
    else:
        tls = args.tls or args.auth_mode in ("entra", "sas")
        host = args.broker_host or "localhost"
        port = args.broker_port or (5671 if tls else 5672)
        username = args.username
        password = args.password
        address = args.address
    feed(
        host,
        port,
        address=address,
        username=username,
        password=password,
        tls=tls,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
        station=args.station,
        state_file=args.state_file,
        polling_interval=args.polling_interval,
        once=args.once,
        mock=args.mock,
    )
