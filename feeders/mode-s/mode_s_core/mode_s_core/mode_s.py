"""Transport-neutral dump1090 acquisition and Mode-S decoding."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
import math
from typing import Dict, Optional

logger = logging.getLogger(__name__)

DF_TO_MSG_TYPE: Dict[int, str] = {
    4: "df4-altitude",
    5: "df5-identity",
    11: "df11-acquisition",
    17: "df17-adsb",
    18: "df17-adsb",
    20: "df20-comm-b",
    21: "df21-comm-b",
}

_PUBLISH_BY_MSG_TYPE = {
    "df17-adsb": "publish_adsb",
    "df4-altitude": "publish_altitude_reply",
    "df5-identity": "publish_identity_reply",
    "df11-acquisition": "publish_acquisition_reply",
    "df20-comm-b": "publish_comm_baltitude",
    "df21-comm-b": "publish_comm_bidentity",
}


@dataclass
class ModeSRecord:
    icao24: str
    receiver_id: str
    msg_type: str
    ts: int
    df: int
    tc: Optional[int]
    bcode: Optional[str]
    alt: Optional[int]
    cs: Optional[str]
    sq: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    spd: Optional[float]
    ang: Optional[float]
    vr: Optional[float]
    rssi: Optional[float]


def _norm_segment(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")


def _hex_icao(icao_value: Optional[str]) -> str:
    if not icao_value:
        return ""
    return _norm_segment(icao_value)


def _decode_rssi(raw_msg: bytes) -> Optional[float]:
    if len(raw_msg) < 7:
        return None
    raw_rssi = raw_msg[6]
    if raw_rssi <= 0:
        return None
    signal_level = (raw_rssi / 255) ** 2
    return round(10 * math.log10(signal_level), 2)


def decode_one(msg_hex: str, ts_ms: int, receiver_id: str, ref_lat: float = 0.0, ref_lon: float = 0.0) -> Optional[ModeSRecord]:
    import pyModeS as pms

    try:
        raw_msg = bytes.fromhex(msg_hex)
    except ValueError:
        return None
    if len(raw_msg) < 7:
        return None
    try:
        df = pms.df(msg_hex)
        icao = pms.icao(msg_hex)
    except Exception:
        return None
    if icao is None or df not in DF_TO_MSG_TYPE:
        return None
    rec = ModeSRecord(
        icao24=_hex_icao(icao),
        receiver_id=_norm_segment(receiver_id),
        msg_type=DF_TO_MSG_TYPE[df],
        ts=int(ts_ms),
        df=int(df),
        tc=None,
        bcode=None,
        alt=None,
        cs=None,
        sq=None,
        lat=None,
        lon=None,
        spd=None,
        ang=None,
        vr=None,
        rssi=_decode_rssi(raw_msg),
    )
    try:
        if df in (17, 18):
            tc = pms.typecode(msg_hex)
            rec.tc = tc
            if tc is None:
                pass
            elif 1 <= tc <= 4:
                rec.cs = pms.adsb.callsign(msg_hex)
            elif 5 <= tc <= 8:
                rec.lat, rec.lon = pms.adsb.surface_position_with_ref(msg_hex, ref_lat, ref_lon)
            elif 9 <= tc <= 18:
                rec.alt = pms.adsb.altitude(msg_hex)
                rec.lat, rec.lon = pms.adsb.airborne_position_with_ref(msg_hex, ref_lat, ref_lon)
            elif tc == 19:
                rec.spd, rec.ang, rec.vr, _ = pms.adsb.velocity(msg_hex)
            elif 20 <= tc <= 22:
                rec.alt = pms.adsb.altitude(msg_hex)
                rec.lat, rec.lon = pms.adsb.airborne_position_with_ref(msg_hex, ref_lat, ref_lon)
        elif df == 20:
            try:
                rec.alt = pms.common.altcode(msg_hex)
            except Exception:
                pass
            try:
                rec.bcode = pms.bds.infer(msg_hex, mrar=True) or None
            except Exception:
                pass
        elif df == 21:
            try:
                rec.sq = str(pms.common.idcode(msg_hex))
            except Exception:
                pass
            try:
                rec.bcode = pms.bds.infer(msg_hex, mrar=True) or None
            except Exception:
                pass
    except Exception as exc:
        logger.debug("decode partial-failure for %s: %s", msg_hex, exc)
    return rec


class ModeSBridge:
    def __init__(self, client, *, feedurl: str, receiver_id: str, ref_lat: float = 0.0, ref_lon: float = 0.0) -> None:
        self.client = client
        self.feedurl = feedurl
        self.receiver_id = receiver_id
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self._count = 0

    async def publish_record(self, rec: ModeSRecord) -> None:
        publish_name = _PUBLISH_BY_MSG_TYPE.get(rec.msg_type)
        if publish_name is None:
            return
        publish_fn = getattr(self.client, publish_name)
        await publish_fn(feedurl=self.feedurl, icao24=rec.icao24, receiver_id=rec.receiver_id, data=rec)
        self._count += 1

    async def run_from_dump1090(self, host: str, port: int, rawtype: str = "beast", max_events: Optional[int] = None) -> None:
        from pyModeS.extra.tcpclient import TcpClient

        loop = asyncio.get_running_loop()
        bridge_self = self

        class _PumpClient(TcpClient):
            def __init__(self):
                super().__init__(host, port, rawtype)

            def handle_messages(self, messages):
                for msg_hex, ts in messages:
                    rec = decode_one(msg_hex, int(ts * 1000), bridge_self.receiver_id, bridge_self.ref_lat, bridge_self.ref_lon)
                    if rec is None:
                        continue
                    fut = asyncio.run_coroutine_threadsafe(bridge_self.publish_record(rec), loop)
                    try:
                        fut.result(timeout=10)
                    except Exception as exc:  # pragma: no cover
                        logger.warning("publish failed: %s", exc)
                    if max_events and bridge_self._count >= max_events:
                        self.stop_flag = True
                        return

        pump = _PumpClient()
        await loop.run_in_executor(None, pump.run)
