from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Dict, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt

from digitraffic_maritime.bridge import DigitraficBridge, DigitrafficPortCallPoller
from digitraffic_maritime.mqtt_source import MQTTSource
from digitraffic_maritime_mqtt_producer_data import PortCall, PortLocation, VesselDetails, VesselLocation, VesselMetadata
from digitraffic_maritime_mqtt_producer_mqtt_client.client import (
    FiDigitrafficMarineAisMqttMqttClient,
    FiDigitrafficMarinePortcallMqttMqttClient,
    FiDigitrafficMarinePortcallPortlocationMqttMqttClient,
    FiDigitrafficMarinePortcallVesseldetailsMqttMqttClient,
)

import json

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
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

logger = logging.getLogger(__name__)

class _NoopFlush:
    def flush(self) -> None:
        return

class _AisAdapter:
    def __init__(self, client: FiDigitrafficMarineAisMqttMqttClient):
        self._client = client

    def send_fi_digitraffic_marine_ais_vessel_location(self, *, _mmsi: str, data: VesselLocation, flush_producer: bool = False):
        asyncio.run(self._client.publish_fi_digitraffic_marine_ais_mqtt_location(mmsi=_mmsi, data=data))

    def send_fi_digitraffic_marine_ais_vessel_metadata(self, *, _mmsi: str, data: VesselMetadata, flush_producer: bool = False):
        asyncio.run(self._client.publish_fi_digitraffic_marine_ais_mqtt_metadata(mmsi=_mmsi, data=data))

class _PortCallAdapter:
    def __init__(
        self,
        port_call_client: FiDigitrafficMarinePortcallMqttMqttClient,
        vessel_details_client: FiDigitrafficMarinePortcallVesseldetailsMqttMqttClient,
        port_location_client: FiDigitrafficMarinePortcallPortlocationMqttMqttClient,
    ):
        self._port_call_client = port_call_client
        self._vessel_details_client = vessel_details_client
        self._port_location_client = port_location_client

    def send_fi_digitraffic_marine_portcall_port_call(self, *, _port_call_id: str, data: PortCall, flush_producer: bool = False):
        asyncio.run(
            self._port_call_client.publish_fi_digitraffic_marine_portcall_mqtt_port_call(
                port_call_id=_port_call_id,
                data=data,
            )
        )

    def send_fi_digitraffic_marine_portcall_vessel_details(self, *, _vessel_id: str, data: VesselDetails, flush_producer: bool = False):
        asyncio.run(
            self._vessel_details_client.publish_fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details(
                vessel_id=_vessel_id,
                data=data,
            )
        )

    def send_fi_digitraffic_marine_portcall_port_location(self, *, _locode: str, data: PortLocation, flush_producer: bool = False):
        asyncio.run(
            self._port_location_client.publish_fi_digitraffic_marine_portcall_portlocation_mqtt_port_location(
                locode=_locode,
                data=data,
            )
        )

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if '://' in url else f'mqtt://{url}')
    scheme = (parsed.scheme or 'mqtt').lower()
    tls = scheme in ('mqtts', 'ssl', 'tls')
    host = parsed.hostname or 'localhost'
    port = parsed.port or (8883 if tls else 1883)
    return host, port, tls

def _build_clients(args: argparse.Namespace):
    host, port, tls_from_url = _parse_broker_url(args.broker_url)
    tls = tls_from_url if args.enable_tls is None else args.enable_tls

    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=args.username,
        password=args.password or '',
        client_id=args.client_id or '',
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        protocol=mqtt.MQTTv5,
        )
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set(ca_certs=args.ca_file or None)

    import threading as _threading
    _connected = _threading.Event()
    def _on_connack(client, userdata, flags, reason_code, props=None):
        if (reason_code if isinstance(reason_code, int) else reason_code.value) == 0:
            _connected.set()
    paho_client.on_connect = _on_connack
    paho_client.connect(host, port, keepalive=60, properties=_entra_props)
    paho_client.loop_start()
    if not _connected.wait(30):
        raise RuntimeError('MQTT CONNACK timeout after 30s')

    ais_client = FiDigitrafficMarineAisMqttMqttClient(paho_client, content_mode=args.content_mode)
    port_call_client = FiDigitrafficMarinePortcallMqttMqttClient(paho_client, content_mode=args.content_mode)
    vessel_details_client = FiDigitrafficMarinePortcallVesseldetailsMqttMqttClient(paho_client, content_mode=args.content_mode)
    port_location_client = FiDigitrafficMarinePortcallPortlocationMqttMqttClient(paho_client, content_mode=args.content_mode)
    return paho_client, _AisAdapter(ais_client), _PortCallAdapter(port_call_client, vessel_details_client, port_location_client)

def _run_stream(args: argparse.Namespace, ais_adapter: _AisAdapter):
    subs = [s.strip() for s in args.subscribe.split(',') if s.strip()]
    mmsi_filter_set = set(int(m.strip()) for m in args.mmsi_filter.split(',') if m.strip()) if args.mmsi_filter else None
    bridge = DigitraficBridge(
        mqtt_source=MQTTSource(
            subscribe_locations='location' in subs,
            subscribe_metadata='metadata' in subs,
            mmsi_filter=mmsi_filter_set,
        ),
        kafka_producer=_NoopFlush(),
        event_producer=ais_adapter,
        mmsi_filter=mmsi_filter_set,
        flush_interval=max(1, args.flush_interval),
    )

    if not args.once:
        bridge.run()
        return

    seen = {'count': 0}

    original = bridge._on_message

    def _once_on_message(topic_type: str, mmsi: int, payload: Dict[str, Any]) -> None:
        original(topic_type, mmsi, payload)
        if bridge._total > 0:
            seen['count'] += 1
            raise KeyboardInterrupt

    bridge._on_message = _once_on_message  # type: ignore[assignment]
    try:
        bridge.run()
    except KeyboardInterrupt:
        if seen['count']:
            logger.info('ONCE_MODE enabled: exiting after first emitted AIS message')

def _run_port_calls(args: argparse.Namespace, port_call_adapter: _PortCallAdapter):
    poller = DigitrafficPortCallPoller(
        kafka_producer=_NoopFlush(),
        event_producer=port_call_adapter,
        vessel_details_event_producer=port_call_adapter,
        port_location_event_producer=port_call_adapter,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
    )
    poller.poll_and_send(once=args.once)

def main() -> None:
    parser = argparse.ArgumentParser(description='Digitraffic Maritime MQTT feeder')
    parser.add_argument('command', nargs='?', default='feed', choices=['feed'])
    parser.add_argument('--mode', choices=['stream', 'port-calls'], default=os.getenv('DIGITRAFFIC_MODE', 'stream'))
    parser.add_argument('--broker-url', default=os.getenv('MQTT_BROKER_URL', 'mqtt://localhost:1883'))
    parser.add_argument('--enable-tls', dest='enable_tls', action='store_true', default=None)
    parser.add_argument('--disable-tls', dest='enable_tls', action='store_false')
    parser.add_argument('--username', default=os.getenv('MQTT_USERNAME'))
    parser.add_argument('--password', default=os.getenv('MQTT_PASSWORD'))
    parser.add_argument('--ca-file', default=os.getenv('MQTT_CA_FILE'))
    parser.add_argument('--client-id', default=os.getenv('MQTT_CLIENT_ID'))
    parser.add_argument('--content-mode', choices=['binary', 'structured'], default=os.getenv('MQTT_CONTENT_MODE', 'binary'))
    parser.add_argument('--subscribe', default=os.getenv('DIGITRAFFIC_SUBSCRIBE', 'location,metadata'))
    parser.add_argument('--mmsi-filter', default=os.getenv('DIGITRAFFIC_FILTER_MMSI'))
    parser.add_argument('--flush-interval', type=int, default=int(os.getenv('DIGITRAFFIC_FLUSH_INTERVAL', '1000')))
    parser.add_argument('--poll-interval', type=int, default=int(os.getenv('DIGITRAFFIC_PORTCALL_POLL_INTERVAL', '300')))
    parser.add_argument('--state-file', default=os.getenv('DIGITRAFFIC_PORTCALL_STATE_FILE', os.path.expanduser('~/.digitraffic_portcalls_state.json')))
    parser.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE', 'false').lower() in ('1', 'true', 'yes'))
    args = parser.parse_args()

    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO').upper(), format='%(asctime)s %(levelname)s %(name)s: %(message)s')

    paho_client, ais_adapter, port_call_adapter = _build_clients(args)
    try:
        if args.mode == 'stream':
            _run_stream(args, ais_adapter)
        else:
            _run_port_calls(args, port_call_adapter)
    finally:
        paho_client.loop_stop()
        paho_client.disconnect()

if __name__ == '__main__':
    main()
