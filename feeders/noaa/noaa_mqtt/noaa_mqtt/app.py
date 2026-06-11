"""NOAA Tides & Currents → MQTT/UNS bridge.

Polls the live NOAA datagetter API for every configured station and product and
publishes the results as CloudEvents into the documented Unified Namespace topic
tree. Reference station metadata is emitted first, then telemetry is polled in a
loop. Acquisition and record normalisation are shared with the Kafka and AMQP
feeders via the transport-agnostic :mod:`noaa_core` package.
"""

import argparse
import asyncio
import dataclasses
import inspect
import json
import logging
import os
import sys
import typing
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

import noaa_core
from noaa_core import NOAAClient
import noaa_mqtt_producer_data as ncd
from noaa_mqtt_producer_mqtt_client.client import *  # noqa: F401,F403  (MqttClient subclass)


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id

    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)


def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"

    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or "")

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    return resolved_client_id, resolved_username, resolved_password


def _slug(value):
    """Render a topic-safe URI-template value (NOAA region is often absent)."""
    return str(value or "unknown").replace("/", "-").replace(" ", "-").lower()


# ---------------------------------------------------------------------------
# Deterministic mock harness (MOCK_MODE).
#
# The Docker E2E MQTT flow runs the container with MOCK_MODE=true + ONCE_MODE
# to get deterministic event coverage without depending on live NOAA payloads.
# MOCK_MODE synthesises one sample of each generated publish_* type; normal
# operation polls the live NOAA API.
# ---------------------------------------------------------------------------
def _sample_value(name, annotation):
    lname = name.lower().rstrip("_")
    if lname in ("station_id", "station_number", "code_station", "station_ref", "station_reference", "site_number"):
        return "mock-station"
    if lname in ("sensor_num",):
        return 1
    if lname in ("parameter_code",):
        return "00010"
    if lname in ("state",):
        return "CA"
    if lname in ("region",):
        return "PACIFIC"
    if lname in ("basin", "river", "water_body", "water_body_name", "river_name", "libelle_cours_eau", "water_area_name"):
        return "mock-basin"
    if "time" in lname or "date" in lname:
        return datetime.now(timezone.utc).isoformat()
    if "lat" in lname:
        return 45.0
    if lname in ("longitude", "long", "lng") or "lon" in lname:
        return -75.0
    if any(x in lname for x in ("level", "value", "temperature", "speed", "pressure", "height", "depth", "salinity", "conductivity", "humidity", "visibility", "discharge", "flow", "elevation", "latitude")):
        return 1.0
    if any(x in lname for x in ("count", "code", "num", "bin", "direction", "timezonecorr")):
        return 1
    if lname.startswith("is_") or lname in ("tidal", "greatlakes", "observedst", "stormsurge", "forecast", "outlook", "nonnavigational", "en_service", "outside_sigma_band", "flat_tolerance_limit", "rate_of_change_limit", "max_min_expected_height", "max_pressure_exceeded", "min_pressure_exceeded", "rate_of_change_exceeded", "max_temp_exceeded", "min_temp_exceeded", "max_humidity_exceeded", "min_humidity_exceeded", "max_conductivity_exceeded", "min_conductivity_exceeded"):
        return False
    return "mock"


def _make_instance(cls):
    kwargs = {}
    for fld in dataclasses.fields(cls):
        if not fld.init:
            continue
        ann = fld.type
        origin = typing.get_origin(ann)
        args = typing.get_args(ann)
        if origin in (typing.Union, getattr(typing, "Optional", object)) and args:
            ann = next((a for a in args if a is not type(None)), args[0])
        try:
            if dataclasses.is_dataclass(ann):
                kwargs[fld.name] = _make_instance(ann)
                continue
        except Exception:  # noqa: BLE001
            pass
        kwargs[fld.name] = _sample_value(fld.name, ann)
    return cls(**kwargs)


def _required_call_kwargs(method):
    out = {}
    for name, param in inspect.signature(method).parameters.items():
        if name in ("self", "topic", "qos", "retain", "content_type", "flush_producer"):
            continue
        if name == "data":
            ann = param.annotation
            if isinstance(ann, str):
                ann = None
            if ann is inspect.Parameter.empty or ann is None:
                raise RuntimeError(f"No data annotation for {method}")
            out[name] = _make_instance(ann)
        else:
            key = name[1:] if name.startswith("_") else name
            out[name] = _sample_value(key, str(param.annotation))
    return out


async def _publish_mock(client):
    """Publish one synthetic instance of every generated publish_* type."""
    for method in [getattr(client, n) for n in dir(client) if n.startswith("publish_")]:
        await method(**_required_call_kwargs(method))



# Map a NOAA product key onto the MQTT client publish-method suffix. Note the
# product `currents_predictions` maps onto the `current_predictions` method.
_METHOD_SUFFIX = {
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

# Telemetry data classes keyed by product (water_level handled separately
# because it carries the QualityLevel enum).
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


async def _publish_station(client, station):
    await client.publish_microsoft_open_data_us_noaa_mqtt_station(
        station.station_id, _slug(getattr(station, "region", None)), station
    )


async def _publish_telemetry(client, product, station_id, region_slug, obj):
    method = getattr(client, "publish_microsoft_open_data_us_noaa_mqtt_" + _METHOD_SUFFIX[product])
    if product == "visibility":
        await method(noaa_core.VISIBILITY_DATACONTENTTYPE, station_id, region_slug, obj)
    else:
        await method(station_id, region_slug, obj)


async def feed(
    host,
    port,
    *,
    username=None,
    password=None,
    tls=False,
    client_id=None,
    content_mode="binary",
    station=None,
    state_file=None,
    polling_interval=300,
    once=False,
    mock=False,
):
    resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(
        client_id=resolved_client_id or "",
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if resolved_username or resolved_password:
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls:
        paho_client.tls_set()
    client_cls = next(obj for obj in globals().values() if isinstance(obj, type) and obj.__name__.endswith("MqttClient"))
    client = client_cls(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await client.connect(host, port)

    if mock:
        try:
            await _publish_mock(client)
        finally:
            await client.disconnect()
        return

    api = NOAAClient()
    try:
        raw_stations = api.fetch_stations_raw()
        stations = ncd.Station.schema().load(raw_stations, many=True)  # pylint: disable=no-member
        stations = noaa_core.select_stations(stations, station)
        if station and not stations:
            sys.exit(1)

        # Reference data first.
        for st in stations:
            await _publish_station(client, st)

        last_polled = noaa_core.load_last_polled_times(state_file)
        while True:
            for st in stations:
                station_id = st.station_id
                region = getattr(st, "region", None)
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
                        await _publish_telemetry(client, product, station_id, region_slug, obj)
                        if ts > max_ts:
                            max_ts = ts
                    if records:
                        last_polled.setdefault(product, {})[station_id] = max_ts
                        noaa_core.save_last_polled_times(state_file, last_polled)
            if once:
                break
            await asyncio.sleep(polling_interval)
    finally:
        await client.disconnect()


def _parse_broker_url(url):
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    tls = (parsed.scheme or "mqtt").lower() in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls, parsed.username, parsed.password


def main(argv=None):
    logging.basicConfig(level=logging.INFO)
    p = argparse.ArgumentParser(description="noaa MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")
    f = sub.add_parser("feed")
    f.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL"))
    f.add_argument("--broker-host", default=os.getenv("MQTT_HOST"))
    f.add_argument("--broker-port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None)
    f.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    f.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    f.add_argument("--tls", action="store_true", default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    f.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID"))
    f.add_argument("--content-mode", default=os.getenv("MQTT_CONTENT_MODE", "binary"), choices=["binary", "structured"])
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
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        port = args.broker_port or port
        tls = tls or args.tls
    else:
        tls = args.tls
        host = args.broker_host or "localhost"
        port = args.broker_port or (8883 if tls else 1883)
        username = args.username
        password = args.password
    asyncio.run(
        feed(
            host,
            port,
            username=username,
            password=password,
            tls=tls,
            client_id=args.client_id,
            content_mode=args.content_mode,
            station=args.station,
            state_file=args.state_file,
            polling_interval=args.polling_interval,
            once=args.once,
            mock=args.mock,
        )
    )
