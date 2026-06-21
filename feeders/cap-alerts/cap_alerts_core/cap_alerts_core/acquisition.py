from __future__ import annotations
import json, re, os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CAP_NS = "urn:oasis:names:tc:emergency:cap:1.2"
ATOM_NS = "http://www.w3.org/2005/Atom"
MOCK_CAP_XML = '<?xml version="1.0" encoding="UTF-8"?>\n<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">\n  <identifier>mock-20260620-001</identifier>\n  <sender>mock@example.invalid</sender>\n  <sent>2026-06-20T17:00:00Z</sent>\n  <status>Actual</status>\n  <msgType>Alert</msgType>\n  <scope>Public</scope>\n  <code>profile:CAP-CP:0.4</code>\n  <info>\n    <language>en-US</language>\n    <category>Met</category>\n    <event>Flood Warning</event>\n    <responseType>Monitor</responseType>\n    <urgency>Expected</urgency>\n    <severity>Severe</severity>\n    <certainty>Likely</certainty>\n    <effective>2026-06-20T17:00:00Z</effective>\n    <onset>2026-06-20T18:00:00Z</onset>\n    <expires>2026-06-21T00:00:00Z</expires>\n    <senderName>Mock Alerting Authority</senderName>\n    <headline>Mock flood warning for coastal zones</headline>\n    <description>Rising water may affect low-lying roads.</description>\n    <instruction>Move to higher ground if instructed by local officials.</instruction>\n    <parameter><valueName>VTEC</valueName><value>/O.NEW.KMTR.FL.W.0001.260620T1800Z-260621T0000Z/</value></parameter>\n    <parameter><valueName>awareness_level</valueName><value>3; orange; Severe</value></parameter>\n    <area>\n      <areaDesc>Mock Coast County</areaDesc>\n      <geocode><valueName>UGC</valueName><value>CAZ001</value></geocode>\n      <geocode><valueName>SAME</valueName><value>006001</value></geocode>\n    </area>\n  </info>\n  <info>\n    <language>es-US</language>\n    <category>Met</category>\n    <event>Flood Warning</event>\n    <urgency>Expected</urgency>\n    <severity>Severe</severity>\n    <certainty>Likely</certainty>\n    <headline>Aviso de inundación de prueba</headline>\n    <area><areaDesc>Condado Costa de Prueba</areaDesc></area>\n  </info>\n</alert>\n'

DEFAULT_CAP_SOURCES = json.dumps([
    {"cap_source_id":"nws-us", "url":"https://api.weather.gov/alerts/active", "format":"nws-json", "zone_url":"https://api.weather.gov/zones?limit=25"},
    {"cap_source_id":"meteoalarm-belgium", "url":"https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-belgium", "format":"atom-cap"}
])

@dataclass(frozen=True)
class CapSource:
    cap_source_id: str
    url: str
    format: str = "cap-xml"
    zone_url: str | None = None
    auth_env: str | None = None


def _dt(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        result = datetime.fromisoformat(text)
    except ValueError:
        return None
    return result if result.tzinfo else result.replace(tzinfo=timezone.utc)


def _text(parent: ET.Element, name: str) -> str | None:
    child = parent.find(f"{{{CAP_NS}}}{name}")
    return child.text.strip() if child is not None and child.text else None


def _texts(parent: ET.Element, name: str) -> list[str]:
    return [c.text.strip() for c in parent.findall(f"{{{CAP_NS}}}{name}") if c.text and c.text.strip()]


def _pairs(parent: ET.Element, name: str) -> list[dict[str, str]]:
    out=[]
    for node in parent.findall(f"{{{CAP_NS}}}{name}"):
        value_name=_text(node,"valueName") or name
        value=_text(node,"value") or ""
        out.append({"value_name": value_name, "value": value})
    return out


def _event_type(value: str | None) -> str | None:
    if not value:
        return None
    token = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return token or None


def _first(values: list[str]) -> str | None:
    return values[0] if values else None


def _info(node: ET.Element) -> dict[str, Any]:
    areas=[]
    same=[]; ugc=[]
    for area in node.findall(f"{{{CAP_NS}}}area"):
        geos=_pairs(area,"geocode")
        for g in geos:
            n=g["value_name"].upper(); v=g["value"]
            if n == "SAME": same.append(v)
            if n in {"UGC", "FIPS6"}: ugc.append(v)
        areas.append({"area_desc":_text(area,"areaDesc"),"polygon":_texts(area,"polygon"),"circle":_texts(area,"circle"),"geocode":geos,"altitude":float(_text(area,"altitude")) if _text(area,"altitude") else None,"ceiling":float(_text(area,"ceiling")) if _text(area,"ceiling") else None})
    params=_pairs(node,"parameter")
    resources=[]
    for res in node.findall(f"{{{CAP_NS}}}resource"):
        sz=_text(res,"size")
        resources.append({"resource_desc":_text(res,"resourceDesc"),"mime_type":_text(res,"mimeType"),"size":int(sz) if sz and sz.isdigit() else None,"uri":_text(res,"uri"),"deref_uri":_text(res,"derefUri"),"digest":_text(res,"digest")})
    return {"language":_text(node,"language"),"category":_texts(node,"category"),"event":_text(node,"event"),"response_type":_texts(node,"responseType"),"urgency":_text(node,"urgency"),"severity":_text(node,"severity"),"certainty":_text(node,"certainty"),"audience":_text(node,"audience"),"event_code":_pairs(node,"eventCode"),"effective":_dt(_text(node,"effective")),"onset":_dt(_text(node,"onset")),"expires":_dt(_text(node,"expires")),"ends":None,"sender_name":_text(node,"senderName"),"headline":_text(node,"headline"),"description":_text(node,"description"),"instruction":_text(node,"instruction"),"web":_text(node,"web"),"contact":_text(node,"contact"),"parameter":params,"resource":resources,"area":areas}


def parse_cap_xml(xml_text: str, cap_source_id: str, provider_url: str) -> dict[str, Any]:
    root = ET.fromstring(xml_text.encode("utf-8"))
    infos=[_info(i) for i in root.findall(f"{{{CAP_NS}}}info")]
    all_params=[p for i in infos for p in i.get("parameter", [])]
    def pval(*names):
        wanted={n.lower() for n in names}
        for p in all_params:
            if p["value_name"].lower() in wanted:
                return p["value"]
        return None
    first_area = next((a for i in infos for a in i.get("area", []) if a.get("area_desc")), None)
    same=[g["value"] for i in infos for a in i.get("area", []) for g in a.get("geocode", []) if g["value_name"].upper()=="SAME"]
    ugc=[g["value"] for i in infos for a in i.get("area", []) for g in a.get("geocode", []) if g["value_name"].upper() in {"UGC","FIPS6"}]
    vtec=[p["value"] for p in all_params if p["value_name"].upper()=="VTEC"]
    event = next((i.get("event") for i in infos if i.get("event")), None)
    sent = _dt(_text(root,"sent")) or datetime.now(timezone.utc)
    return {"cap_source_id":cap_source_id,"identifier":_text(root,"identifier") or f"missing-{hash(xml_text)}","sender":_text(root,"sender") or cap_source_id,"sent":sent,"status":_text(root,"status") or "Actual","msg_type":_text(root,"msgType") or "Alert","source":_text(root,"source"),"scope":_text(root,"scope") or "Public","restriction":_text(root,"restriction"),"addresses":(_text(root,"addresses") or "").split() if _text(root,"addresses") else [],"code":[{"value_name":"code","value":v} for v in _texts(root,"code")],"note":_text(root,"note"),"references":(_text(root,"references") or "").split() if _text(root,"references") else [],"incidents":(_text(root,"incidents") or "").split() if _text(root,"incidents") else [],"affected_zones":[],"raw_source_json":None,"info":infos,"provider_url":provider_url,"raw_cap_xml":xml_text,"area_desc": first_area.get("area_desc") if first_area else None,"same_codes":same,"ugc_codes":ugc,"vtec":vtec,"awareness_level":pval("awareness_level"),"awareness_type":pval("awareness_type"),"event_type":_event_type(event),"state":None}


def parse_nws_alerts_json(payload: dict[str, Any], cap_source_id: str, provider_url: str) -> list[dict[str, Any]]:
    alerts=[]
    for feature in payload.get("features", []):
        p=feature.get("properties", {})
        geocode=p.get("geocode") or {}
        same=list(geocode.get("SAME") or [])
        ugc=list(geocode.get("UGC") or [])
        params=[]
        for name, vals in (p.get("parameters") or {}).items():
            for val in vals if isinstance(vals, list) else [vals]:
                params.append({"value_name":name,"value":str(val)})
        area={"area_desc":p.get("areaDesc"),"polygon":[],"circle":[],"geocode":[{"value_name":"SAME","value":v} for v in same]+[{"value_name":"UGC","value":v} for v in ugc],"altitude":None,"ceiling":None}
        info={"language":None,"category":[p.get("category") or "Met"],"event":p.get("event"),"response_type":[],"urgency":p.get("urgency") or "Unknown","severity":p.get("severity") or "Unknown","certainty":p.get("certainty") or "Unknown","audience":None,"event_code":[],"effective":_dt(p.get("effective")),"onset":_dt(p.get("onset")),"expires":_dt(p.get("expires")),"ends":_dt(p.get("ends")),"sender_name":p.get("senderName"),"headline":p.get("headline"),"description":p.get("description"),"instruction":p.get("instruction"),"web":p.get("uri") or p.get("@id"),"contact":None,"parameter":params,"resource":[],"area":[area]}
        alerts.append({"cap_source_id":cap_source_id,"identifier":p.get("id") or feature.get("id") or p.get("@id"),"sender":p.get("sender") or "NWS","sent":_dt(p.get("sent")) or datetime.now(timezone.utc),"status":p.get("status") or "Actual","msg_type":p.get("messageType") or "Alert","source":None,"scope":p.get("scope") or "Public","restriction":None,"addresses":[],"code":[],"note":None,"references":p.get("references",[]),"incidents":[],"affected_zones":p.get("affectedZones") or [],"raw_source_json":json.dumps(feature, separators=(",",":"), sort_keys=True),"info":[info],"provider_url":provider_url,"raw_cap_xml":None,"area_desc":p.get("areaDesc"),"same_codes":same,"ugc_codes":ugc,"vtec":[x["value"] for x in params if x["value_name"].upper()=="VTEC"],"awareness_level":None,"awareness_type":None,"event_type":_event_type(p.get("event")),"state":_first(ugc)[:2] if ugc else None})
    return [a for a in alerts if a.get("identifier")]


def load_sources(config_text: str | None) -> list[CapSource]:
    raw = json.loads(config_text or os.getenv("CAP_SOURCES") or DEFAULT_CAP_SOURCES)
    return [CapSource(cap_source_id=str(x["cap_source_id"]), url=str(x["url"]), format=str(x.get("format","cap-xml")), zone_url=x.get("zone_url"), auth_env=x.get("auth_env")) for x in raw]

class CapClient:
    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=(429,500,502,503,504), allowed_methods=("GET",))
        self.session.mount("http://", HTTPAdapter(max_retries=retry)); self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.headers.update({"User-Agent":"real-time-sources-cap-alerts/0.1"})
    def fetch_alerts(self, source: CapSource) -> list[dict[str, Any]]:
        headers={}
        if source.auth_env and os.getenv(source.auth_env): headers["Authorization"] = os.getenv(source.auth_env, "")
        r=self.session.get(source.url, timeout=30, headers=headers); r.raise_for_status()
        if source.format == "nws-json": return parse_nws_alerts_json(r.json(), source.cap_source_id, source.url)
        text=r.text
        if source.format in {"cap-directory", "dwd-directory"}:
            alerts=[]
            for href in re.findall(r'href=["\\\']([^"\\\']+\\.xml)["\\\']', text, flags=re.IGNORECASE)[:50]:
                try:
                    rr=self.session.get(urljoin(source.url, href), timeout=30, headers=headers); rr.raise_for_status(); alerts.append(parse_cap_xml(rr.text, source.cap_source_id, rr.url))
                except Exception:
                    continue
            return alerts
        if "<feed" in text[:2000]:
            root=ET.fromstring(text.encode("utf-8")); alerts=[]
            for entry in root.findall(f"{{{ATOM_NS}}}entry")[:25]:
                link=entry.find(f"{{{ATOM_NS}}}link")
                href=link.get("href") if link is not None else None
                if href:
                    try:
                        rr=self.session.get(urljoin(source.url, href), timeout=30); rr.raise_for_status(); alerts.append(parse_cap_xml(rr.text, source.cap_source_id, rr.url))
                    except Exception:
                        continue
            return alerts
        return [parse_cap_xml(text, source.cap_source_id, source.url)]
    def fetch_zones(self, source: CapSource) -> list[dict[str, Any]]:
        if not source.zone_url:
            return []
        r=self.session.get(source.zone_url, timeout=30); r.raise_for_status(); payload=r.json(); zones=[]
        for f in payload.get("features", []):
            p=f.get("properties", {})
            zid=p.get("id") or p.get("@id") or f.get("id")
            if not zid: continue
            zones.append({"cap_source_id":source.cap_source_id,"zone_id":str(zid).split("/")[-1],"name":p.get("name"),"zone_type":p.get("type"),"state":p.get("state"),"forecast_office":p.get("forecastOffice"),"time_zones":p.get("timeZone") or [],"geometry":json.dumps(f.get("geometry"), separators=(",",":")) if f.get("geometry") else None,"provider_url":source.zone_url})
        return zones


def mock_client_and_sources() -> tuple[CapClient, list[CapSource]]:
    class MockSession(requests.Session):
        def get(self, url, *args, **kwargs):
            class Resp:
                def __init__(self, text, url): self.text=text; self.url=url; self.status_code=200
                def raise_for_status(self): pass
                def json(self): return json.loads(self.text)
            fixture=Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "sample-cap.xml"
            if "zones" in url:
                return Resp(json.dumps({"features":[{"id":"https://api.weather.gov/zones/forecast/CAZ001","properties":{"id":"CAZ001","name":"Mock Coast","type":"forecast","state":"CA","forecastOffice":"https://api.weather.gov/offices/MTR","timeZone":["America/Los_Angeles"]},"geometry":None}]}), url)
            return Resp(fixture.read_text(encoding="utf-8") if fixture.exists() else MOCK_CAP_XML, url)
    return CapClient(MockSession()), [CapSource("mock-cap", "https://example.invalid/sample-cap.xml", "cap-xml", "https://example.invalid/zones")]
