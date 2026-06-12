from __future__ import annotations
import argparse, asyncio, os
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from noaa_goes_mqtt_producer_data import GoesXrayFlux, GoesProtonFlux, GoesElectronFlux, GoesMagnetometer, SpaceWeatherAlert, XrayFlare
from noaa_goes_mqtt_producer_mqtt_client.client import MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient

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

def _parse(url):
    p=urlparse(url if '://' in url else 'mqtt://'+url); return p.hostname or 'localhost', p.port or 1883
async def _mock(c):
    ts='2026-04-07T10:00:00Z'; sat='goes-18'
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt(satellite=sat, energy='0.1-0.8nm', time_tag=ts, event='xrs', data=GoesXrayFlux(time_tag=ts, satellite=18, flux=1.2e-6, energy='0.1-0.8nm'))
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt(satellite=sat, energy='>=10MeV', time_tag=ts, event='sgps', data=GoesProtonFlux(time_tag=ts, satellite=18, flux=3.0, energy='>=10MeV'))
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt(satellite=sat, energy='>=2MeV', time_tag=ts, event='exis', data=GoesElectronFlux(time_tag=ts, satellite=18, flux=900.0, energy='>=2MeV'))
    await c.publish_microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt(satellite=sat, time_tag=ts, event='magnetometer', data=GoesMagnetometer(time_tag=ts, satellite=18, he=1.0, hp=2.0, hn=3.0, total=3.7, arcjet_flag=False))
    await c.publish_microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt(product_id='ALTXMF-20260407', data=SpaceWeatherAlert(product_id='ALTXMF-20260407', issue_datetime='2026 Apr 07 1000 UTC', message='Synthetic SWPC alert.'))
    await c.publish_microsoft_open_data_us_noaa_swpc_xray_flare_mqtt(satellite=sat, begin_time='2026-04-07T09:58:00Z', flare_class='M1', data=XrayFlare(time_tag=ts, begin_time='2026-04-07T09:58:00Z', begin_class='C9.0', max_time=ts, max_class='M1.0', max_xrlong=1e-5, max_ratio=0.2, max_ratio_time=ts, current_int_xrlong=1e-3, end_time='2026-04-07T10:10:00Z', end_class='C2.0', satellite=18))

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883'))
    a=ap.parse_args(argv)
    if a.command!='feed': ap.print_help(); return
    async def run():
        resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
            auth_mode=os.getenv("MQTT_AUTH_MODE"),
        )
        host,port=_parse(a.mqtt_broker_url); p=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if _entra_props is None and (resolved_username or resolved_password): p.username_pw_set(resolved_username, resolved_password)
        if _entra_props is not None or a.mqtt_broker_url.startswith(('mqtts://', 'ssl://')): p.tls_set()
        c=MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop())
        # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
        if _entra_props is not None:
            import threading as _threading
            _connected = _threading.Event()
            def _on_connack(client, userdata, flags, reason_code, props=None):
                if reason_code == 0:
                    _connected.set()
            p.on_connect = _on_connack
            p.connect(host, port, keepalive=60, clean_start=True, properties=_entra_props)
            p.loop_start()
            if not await asyncio.get_running_loop().run_in_executor(None, lambda: _connected.wait(30)):
                raise RuntimeError('MQTT CONNACK timeout after 30s')
        else:
            await c.connect(host,port)
        await _mock(c); await asyncio.sleep(1); await c.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()
