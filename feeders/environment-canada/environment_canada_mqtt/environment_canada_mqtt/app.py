from __future__ import annotations
import argparse, asyncio, json, logging, os
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from environment_canada_core import ECWeatherAPI, _load_state, _save_state
from environment_canada_mqtt_producer_mqtt_client.client import CAGovECCCWeatherMqttMqttClient
logger = logging.getLogger(__name__)
def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params={"api-version":"2018-02-01","resource":audience or "https://eventgrid.azure.net/"}
    if managed_identity_client_id: params["client_id"]=managed_identity_client_id
    request=Request("http://169.254.169.254/metadata/identity/oauth2/token?"+urlencode(params),headers={"Metadata":"true"})
    with urlopen(request,timeout=30) as response: payload=json.loads(response.read().decode("utf-8"))
    return str(payload.get("accessToken") or payload.get("access_token"))
def _resolve(*, username=None,password=None,client_id=None,auth_mode=None):
    cid=str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip(); mode=str(auth_mode or os.getenv("MQTT_AUTH_MODE","password")).strip().lower() or "password"
    if mode!="entra": return cid,str(username or ""),str(password or ""),None
    from paho.mqtt.properties import Properties as P; from paho.mqtt.packettypes import PacketTypes as T
    pwd=_fetch_entra_mqtt_token(os.getenv("MQTT_ENTRA_AUDIENCE","https://eventgrid.azure.net/"), os.getenv("MQTT_ENTRA_CLIENT_ID") or None); props=P(T.CONNECT); props.AuthenticationMethod="OAUTH2-JWT"; props.AuthenticationData=pwd.encode("utf-8"); return cid, str(username or cid), pwd, props
def _parse(url):
    parsed=urlparse(url if "://" in url else f"mqtt://{url}"); scheme=(parsed.scheme or "mqtt").lower(); return parsed.hostname or "localhost", parsed.port or (8883 if scheme in ("mqtts","ssl","tls") else 1883), scheme in ("mqtts","ssl","tls")
def _segment(value):
    text=(str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/","+","#","\x00"): text=text.replace(forbidden,"-")
    return "-".join(text.split()) or "unknown"
async def _run(args,mqtt_client):
    api=ECWeatherAPI(polling_interval=args.polling_interval, station_limit=args.station_limit, obs_limit=args.obs_limit); state=_load_state(args.state_file); provinces={}
    for feature in api.get_stations():
        station=api.parse_station(feature)
        if not station.msc_id: continue
        provinces[station.msc_id]=station.province or station.province_territory
        await mqtt_client.publish_ca_gov_eccc_weather_mqtt_station(msc_id=station.msc_id, province=_segment(station.province or station.province_territory or "unknown"), data=station)
    while True:
        for feature in api.get_recent_observations():
            obs=api.parse_observation(feature)
            if not obs: continue
            key=f"{obs.msc_id}:{obs.observation_time.isoformat()}"
            if key in state: continue
            await mqtt_client.publish_ca_gov_eccc_weather_mqtt_weather_observation(msc_id=obs.msc_id, province=_segment(obs.province or provinces.get(obs.msc_id) or "unknown"), data=obs, _time=obs.observation_time.isoformat())
            state[key]=obs.observation_time.isoformat()
        _save_state(args.state_file,state)
        if args.once: break
        await asyncio.sleep(args.polling_interval)
def main():
    logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p=argparse.ArgumentParser(); p.add_argument("feed", nargs="?", default="feed"); p.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL","mqtt://localhost:1883")); p.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(r"~/.environment_canada_mqtt_state.json"))); p.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL","900"))); p.add_argument("--station-limit", type=int, default=int(os.getenv("STATION_LIMIT","500"))); p.add_argument("--obs-limit", type=int, default=int(os.getenv("OBS_LIMIT","500"))); p.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE","").lower() in ("1","true","yes")); p.add_argument("--username", default=os.getenv("MQTT_USERNAME","")); p.add_argument("--password", default=os.getenv("MQTT_PASSWORD","")); p.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID","")); p.add_argument("--content-mode", choices=("binary","structured"), default=os.getenv("MQTT_CONTENT_MODE","binary")); a=p.parse_args(); host,port,tls=_parse(a.broker_url); cid,user,pwd,props=_resolve(username=a.username or None,password=a.password or None,client_id=a.client_id or None,auth_mode=os.getenv("MQTT_AUTH_MODE"))
    async def runner():
        client=mqtt.Client(client_id=cid or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if props is None and (user or pwd): client.username_pw_set(user,pwd)
        if tls or props is not None: client.tls_set()
        mqtt_client=CAGovECCCWeatherMqttMqttClient(client=client, content_mode=a.content_mode, loop=asyncio.get_running_loop())
        if props is not None: client.connect(host,port,keepalive=60,clean_start=True,properties=props); client.loop_start()
        else: await mqtt_client.connect(host,port)
        try: await _run(a,mqtt_client)
        finally: await mqtt_client.disconnect()
    asyncio.run(runner())
if __name__=='__main__': main()
