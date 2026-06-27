"""
NASA FIRMS active-fire poller.

Polls the NASA FIRMS (Fire Information for Resource Management System) Area API
for near-real-time active-fire / thermal-anomaly detections from the VIIRS and
MODIS instruments and emits them as CloudEvents to a Kafka topic. At startup and
periodically the bridge also fetches the FIRMS data-availability windows and
emits one DataAvailability reference event per source on the same topic, so
downstream consumers can interpret detection freshness without an out-of-band
lookup.

Upstream docs: https://firms.modaps.eosdis.nasa.gov/api/area/
A free MAP_KEY (NASA Earthdata account) is required; supply it via --map-key or
the FIRMS_MAP_KEY environment variable.
"""

import os
import sys
import csv
import math
import json
import hashlib
import asyncio
import logging
import argparse
from datetime import datetime, timedelta, timezone, date
from io import StringIO
from typing import Any, Dict, List, Optional

import aiohttp
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from nasa_firms_producer_data import (
    FireDetection,
    DataAvailability,
    InstrumentEnum,
    ConfidenceLevelenum,
    DaynightEnum,
)
try:
    from nasa_firms_producer_kafka_producer.producer import NASAFIRMSEventProducer
except ModuleNotFoundError:
    # The generated Kafka producer package is only installed in the Kafka
    # image. The MQTT/AMQP images reuse this module for the shared
    # build_*/fetch helpers and the generated data classes, so the Kafka
    # producer is an optional dependency there. Only the Kafka bridge
    # references it, and that class never runs in those images.
    NASAFIRMSEventProducer = None
# pylint: enable=import-error, line-too-long


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

FIRMS_BASE = "https://firms.modaps.eosdis.nasa.gov/"
API_BASE = FIRMS_BASE + "api/"
# CloudEvents `source` attribute value for every emitted event.
SOURCE_URI = API_BASE + "area/"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-nasa-firms/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

# Global near-real-time sources suited to worldwide OSINT monitoring.
DEFAULT_SOURCES = [
    "VIIRS_SNPP_NRT",
    "VIIRS_NOAA20_NRT",
    "VIIRS_NOAA21_NRT",
    "MODIS_NRT",
]

# Static per-source sensor facts: (instrument, platform name, nadir resolution m).
SOURCE_META: Dict[str, Any] = {
    "VIIRS_SNPP_NRT": ("VIIRS", "Suomi-NPP", 375.0),
    "VIIRS_SNPP_SP": ("VIIRS", "Suomi-NPP", 375.0),
    "VIIRS_NOAA20_NRT": ("VIIRS", "NOAA-20", 375.0),
    "VIIRS_NOAA21_NRT": ("VIIRS", "NOAA-21", 375.0),
    "MODIS_NRT": ("MODIS", "Terra/Aqua", 1000.0),
    "MODIS_SP": ("MODIS", "Terra/Aqua", 1000.0),
    "LANDSAT_NRT": ("Landsat", "Landsat 8/9", 30.0),
}

DEFAULT_DAY_RANGE = 1
DEFAULT_AREA = "world"
DEFAULT_POLL_MINUTES = 15


def confidence_level(instrument: str, raw: Optional[str]) -> ConfidenceLevelenum:
    """Normalise sensor-specific confidence into low/nominal/high.

    VIIRS reports a class letter (l/n/h); MODIS reports an integer percentage
    where <30 is low, 30-80 nominal, and >80 high.
    """
    del instrument  # kept for call-site clarity; mapping is value-driven
    if raw is None:
        return ConfidenceLevelenum.nominal
    value = raw.strip().lower()
    if value in ("l", "low"):
        return ConfidenceLevelenum.low
    if value in ("n", "nominal"):
        return ConfidenceLevelenum.nominal
    if value in ("h", "high"):
        return ConfidenceLevelenum.high
    try:
        pct = int(float(value))
    except (TypeError, ValueError):
        return ConfidenceLevelenum.nominal
    if pct < 30:
        return ConfidenceLevelenum.low
    if pct <= 80:
        return ConfidenceLevelenum.nominal
    return ConfidenceLevelenum.high


def geo_tile(lat: float, lon: float) -> str:
    """Coarse 10-degree tile label `lat<LL>_lon<LL>` (south-west corner)."""
    lat_floor = int(math.floor(lat / 10.0) * 10)
    lon_floor = int(math.floor(lon / 10.0) * 10)
    return f"lat{lat_floor}_lon{lon_floor}"


def _to_float(value: Any) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


class FirmsPoller:
    """Polls the NASA FIRMS Area API and emits CloudEvents."""

    def __init__(self, map_key: Optional[str] = None,
                 kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: Optional[str] = None,
                 last_polled_file: Optional[str] = None,
                 sources: Optional[List[str]] = None,
                 area: str = DEFAULT_AREA,
                 day_range: int = DEFAULT_DAY_RANGE,
                 poll_minutes: int = DEFAULT_POLL_MINUTES,
                 event_producer: Any = None):
        self.map_key = map_key
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.sources = sources or list(DEFAULT_SOURCES)
        self.area = area
        self.day_range = day_range
        self.poll_minutes = poll_minutes
        self.event_producer = event_producer
        if self.event_producer is None and kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = NASAFIRMSEventProducer(producer, kafka_topic)  # type: ignore[arg-type]

    # ----------------------------------------------------------------- fetching
    async def _fetch_text(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        safe_url = url.replace(self.map_key or "\0", "***") if self.map_key else url
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except asyncio.TimeoutError:
            logger.error("Request timed out: %s", safe_url)
            return None
        except aiohttp.ClientError as exc:
            logger.error("HTTP error for %s: %s", safe_url, exc)
            return None

    @staticmethod
    def _parse_csv(text: str) -> List[Dict[str, str]]:
        """Parse a FIRMS CSV response, tolerating plain-text error bodies."""
        if not text:
            return []
        first = text.lstrip().split("\n", 1)[0].lower()
        if "latitude" not in first or "longitude" not in first:
            # FIRMS returns plain-text errors (bad key, quota, no data) with 200.
            logger.warning("Non-CSV response from FIRMS: %s", text.strip()[:200])
            return []
        return list(csv.DictReader(StringIO(text)))

    def _area_url(self, source: str) -> str:
        return (f"{API_BASE}area/csv/{self.map_key}/{source}/{self.area}/"
                f"{self.day_range}")

    def _availability_url(self) -> str:
        return f"{API_BASE}data_availability/csv/{self.map_key}/all"

    async def fetch_detections(self, session: aiohttp.ClientSession, source: str) -> List[FireDetection]:
        text = await self._fetch_text(session, self._area_url(source))
        rows = self._parse_csv(text or "")
        detections = []
        for row in rows:
            det = self.parse_detection(source, row)
            if det is not None:
                detections.append(det)
        return detections

    async def fetch_availability(self, session: aiohttp.ClientSession) -> List[DataAvailability]:
        text = await self._fetch_text(session, self._availability_url())
        records: List[DataAvailability] = []
        if not text:
            return records
        first = text.lstrip().split("\n", 1)[0].lower()
        if "data_id" not in first:
            logger.warning("Non-CSV availability response from FIRMS: %s", text.strip()[:200])
            return records
        reader = csv.DictReader(StringIO(text))
        now_iso = datetime.now(timezone.utc).isoformat()
        wanted = set(self.sources)
        for row in reader:
            data_id = (row.get("data_id") or "").strip()
            if data_id not in wanted:
                continue
            instrument, satellite, resolution = SOURCE_META.get(
                data_id, (None, None, None))
            records.append(DataAvailability(
                source=data_id,
                record_id="coverage",
                data_id=data_id,
                min_date=date.fromisoformat((row.get("min_date") or "").strip() or None) if (row.get("min_date") or "").strip() or None else None,  # type: ignore[arg-type]
                max_date=date.fromisoformat((row.get("max_date") or "").strip() or None) if (row.get("max_date") or "").strip() or None else None,  # type: ignore[arg-type]
                instrument=InstrumentEnum(instrument) if instrument in ("VIIRS", "MODIS") else None,
                satellite=satellite,
                resolution_m=resolution,
                retrieved_at=datetime.fromisoformat(now_iso),
            ))
        return records

    # ------------------------------------------------------------------ parsing
    def parse_detection(self, source: str, row: Dict[str, str]) -> Optional[FireDetection]:
        lat = _to_float(row.get("latitude"))
        lon = _to_float(row.get("longitude"))
        if lat is None or lon is None:
            return None

        instrument_raw = (row.get("instrument") or "").strip().upper()
        if "MODIS" in instrument_raw:
            instrument = InstrumentEnum.MODIS
        elif "VIIRS" in instrument_raw:
            instrument = InstrumentEnum.VIIRS
        else:
            meta_instrument = SOURCE_META.get(source, ("VIIRS",))[0]
            instrument = InstrumentEnum(meta_instrument) if meta_instrument in ("VIIRS", "MODIS") else InstrumentEnum.VIIRS

        acq_date = (row.get("acq_date") or "").strip()
        acq_time = (row.get("acq_time") or "").strip().zfill(4)
        satellite = (row.get("satellite") or "").strip()
        acq_datetime = f"{acq_date}T{acq_time[:2]}:{acq_time[2:]}:00Z" if acq_date else ""

        identity = f"{source}|{lat}|{lon}|{acq_date}|{acq_time}|{satellite}"
        record_id = hashlib.sha1(identity.encode("utf-8")).hexdigest()[:16]

        raw_conf = (row.get("confidence") or "").strip() or None
        daynight_raw = (row.get("daynight") or "").strip().upper()
        daynight = DaynightEnum(daynight_raw) if daynight_raw in ("D", "N") else None

        return FireDetection(
            source=source,
            record_id=record_id,
            latitude=lat,
            longitude=lon,
            brightness=_to_float(row.get("brightness")),
            bright_t31=_to_float(row.get("bright_t31")),
            bright_ti4=_to_float(row.get("bright_ti4")),
            bright_ti5=_to_float(row.get("bright_ti5")),
            scan=_to_float(row.get("scan")),
            track=_to_float(row.get("track")),
            acq_date=date.fromisoformat(acq_date),
            acq_time=acq_time,
            acq_datetime=datetime.fromisoformat(acq_datetime),
            satellite=satellite,
            instrument=instrument,
            confidence=raw_conf,
            confidence_level=confidence_level(instrument.value, raw_conf),
            version=(row.get("version") or "").strip() or None,
            frp=_to_float(row.get("frp")),
            daynight=daynight,
            tile=geo_tile(lat, lon),
        )

    # -------------------------------------------------------------- seen-id state
    def load_seen_ids(self) -> Dict[str, str]:
        if self.last_polled_file and os.path.exists(self.last_polled_file):
            try:
                with open(self.last_polled_file, "r", encoding="utf-8") as handle:
                    return json.load(handle)
            except (json.JSONDecodeError, OSError):
                logger.error("Could not read last-polled file; starting fresh")
        return {}

    def save_seen_ids(self, seen: Dict[str, str]) -> None:
        if self.last_polled_file:
            try:
                with open(self.last_polled_file, "w", encoding="utf-8") as handle:
                    json.dump({
                        rid: ts.isoformat() if isinstance(ts, datetime) else ts
                        for rid, ts in seen.items()
                    }, handle)
            except OSError as exc:
                logger.error("Could not write last-polled file: %s", exc)

    # --------------------------------------------------------------------- driver
    async def poll_and_send(self, once: bool = False) -> None:
        """Emit reference data, then poll detections until stopped.

        Args:
            once: If True, run a single cycle and exit (Fabric notebook / cron).
        """
        async def flush_transport(producer):
            result = producer.producer.flush()
            if hasattr(result, "__await__"):
                await result

        seen = self.load_seen_ids()
        poll_interval = timedelta(minutes=self.poll_minutes)
        availability_sent = False

        while True:
            start = datetime.now(timezone.utc)
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120),
                headers={"User-Agent": USER_AGENT},
            ) as session:
                # Reference data first, refreshed roughly once per hour.
                if not availability_sent or start.minute < self.poll_minutes:
                    await self._send_availability(session)
                    availability_sent = True

                total_new = 0
                for source in self.sources:
                    detections = await self.fetch_detections(session, source)
                    for det in detections:
                        detection_timestamp = det.acq_datetime.isoformat()
                        if seen.get(det.record_id) == detection_timestamp:
                            continue
                        self._send_detection(det)
                        seen[det.record_id] = detection_timestamp
                        total_new += 1

            if self.event_producer is not None:
                await flush_transport(self.event_producer)
            self.save_seen_ids(seen)

            if total_new:
                logger.info("Emitted %d new fire detections", total_new)
            else:
                logger.debug("No new fire detections this cycle")

            # Prune the seen set to the configured day range plus a margin.
            cutoff = (datetime.now(timezone.utc) - timedelta(days=self.day_range + 2)).isoformat()
            seen = {rid: ts for rid, ts in seen.items() if (ts or "") >= cutoff}

            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break

            elapsed = datetime.now(timezone.utc) - start
            remaining = poll_interval - elapsed
            if remaining.total_seconds() > 0:
                await asyncio.sleep(remaining.total_seconds())

    async def _send_availability(self, session: aiohttp.ClientSession) -> None:
        records = await self.fetch_availability(session)
        for record in records:
            self.event_producer.send_nasa_firms_data_availability(
                _source_uri=SOURCE_URI,
                _source=record.source,
                _record_id=record.record_id,
                _time=record.retrieved_at,
                data=record,
                flush_producer=False,
            )
        if records:
            logger.info("Emitted %d data-availability reference records", len(records))

    def _send_detection(self, det: FireDetection) -> None:
        self.event_producer.send_nasa_firms_fire_detection(
            _source_uri=SOURCE_URI,
            _source=det.source,
            _record_id=det.record_id,
            _time=det.acq_datetime or None,
            data=det,
            flush_producer=False,
        )


async def run_recent_detections(map_key: str, sources: List[str], area: str, day_range: int) -> None:
    poller = FirmsPoller(map_key=map_key, sources=sources, area=area, day_range=day_range)
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=120),
        headers={"User-Agent": USER_AGENT},
    ) as session:
        for source in poller.sources:
            detections = await poller.fetch_detections(session, source)
            print(f"{source}: {len(detections)} detections")
            for det in detections[:10]:
                frp = f"{det.frp:.1f}MW" if det.frp is not None else "FRP?"
                print(f"  {det.acq_datetime} {det.latitude:.3f},{det.longitude:.3f} "
                      f"{det.confidence_level.value} {frp} [{det.record_id}]")


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config['bootstrap.servers'] = part.split('=', 1)[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config['kafka_topic'] = part.split('=', 1)[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if 'sasl.username' in config:
        config['security.protocol'] = 'SASL_SSL'
        config['sasl.mechanism'] = 'PLAIN'
    return config


def main() -> None:
    parser = argparse.ArgumentParser(description="NASA FIRMS active-fire poller")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    feed_parser = subparsers.add_parser('feed', help="Poll FIRMS and feed Kafka")
    feed_parser.add_argument('--map-key', type=str, help="NASA FIRMS MAP_KEY (or FIRMS_MAP_KEY env)")
    feed_parser.add_argument('--last-polled-file', type=str, help="File to persist seen detection IDs")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str)
    feed_parser.add_argument('--kafka-topic', type=str)
    feed_parser.add_argument('--sasl-username', type=str)
    feed_parser.add_argument('--sasl-password', type=str)
    feed_parser.add_argument('--connection-string', type=str,
                             help='Event Hubs / Fabric Event Stream connection string')
    feed_parser.add_argument('--sources', type=str,
                             help=f'Comma-separated FIRMS sources (default: {",".join(DEFAULT_SOURCES)})')
    feed_parser.add_argument('--area', type=str, default=DEFAULT_AREA,
                             help='`world` or `west,south,east,north` bounding box')
    feed_parser.add_argument('--day-range', type=int,
                             default=int(os.getenv('FIRMS_DAY_RANGE', DEFAULT_DAY_RANGE)),
                             help='Number of days back to request (1-10; also FIRMS_DAY_RANGE env)')
    feed_parser.add_argument('--poll-minutes', type=int, default=DEFAULT_POLL_MINUTES)
    feed_parser.add_argument('--log-level', type=str, default='INFO')
    feed_parser.add_argument('--once', action='store_true',
                             default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'),
                             help='Exit after one polling cycle (also ONCE_MODE env). For Fabric notebooks.')

    det_parser = subparsers.add_parser('detections', help="List recent detections")
    det_parser.add_argument('--map-key', type=str)
    det_parser.add_argument('--sources', type=str)
    det_parser.add_argument('--area', type=str, default=DEFAULT_AREA)
    det_parser.add_argument('--day-range', type=int, default=DEFAULT_DAY_RANGE)

    subparsers.add_parser('sources', help="List configured FIRMS sources")

    args = parser.parse_args()

    if args.subcommand == 'sources':
        for src, (instrument, satellite, res) in SOURCE_META.items():
            print(f"{src}: {instrument} {satellite} {res:.0f}m")
        return
    if args.subcommand == 'detections':
        map_key = args.map_key or os.getenv('FIRMS_MAP_KEY')
        if not map_key:
            print("Error: a FIRMS MAP_KEY is required (--map-key or FIRMS_MAP_KEY).")
            sys.exit(1)
        sources = args.sources.split(',') if args.sources else list(DEFAULT_SOURCES)
        asyncio.run(run_recent_detections(map_key, sources, args.area, args.day_range))
        return
    if args.subcommand != 'feed':
        parser.print_help()
        return

    if os.getenv('LOG_LEVEL'):
        args.log_level = os.getenv('LOG_LEVEL')
    logger.setLevel(args.log_level)

    map_key = args.map_key or os.getenv('FIRMS_MAP_KEY')
    if not map_key:
        print("Error: a FIRMS MAP_KEY is required (--map-key or FIRMS_MAP_KEY).")
        sys.exit(1)

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('FIRMS_LAST_POLLED_FILE',
                                          os.path.expanduser('~/.nasa_firms_last_polled.json'))

    sources = args.sources or os.getenv('FIRMS_SOURCES')
    sources = sources.split(',') if sources else list(DEFAULT_SOURCES)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided via CLI or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided via CLI or connection string.")
        sys.exit(1)

    kafka_config = {'bootstrap.servers': kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
            # Event Hubs / Fabric Event Streams reject the idempotent producer
            # (UNSUPPORTED_FOR_MESSAGE_FORMAT); disable it on the SASL path.
            'enable.idempotence': False,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = FirmsPoller(
        map_key=map_key,
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        sources=sources,
        area=args.area,
        day_range=args.day_range,
        poll_minutes=args.poll_minutes,
    )
    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
