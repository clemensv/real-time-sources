"""NDW Netherlands Road Traffic bridge.

Downloads gzip-compressed DATEX II XML files from the Dutch NDW open data
platform and emits CloudEvents for traffic speed, travel time, and traffic
situations onto Kafka topics.
"""

from __future__ import annotations

import argparse
import gzip
import json
import logging
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from io import BytesIO
from typing import Any, Dict, List, Optional, Set, Tuple

from confluent_kafka import Producer

from ndl_netherlands_producer_data import TrafficSpeed, TravelTime, TrafficSituation
from ndl_netherlands_producer_kafka_producer.producer import (
    NLNDWTrafficMeasurementsEventProducer,
    NLNDWTrafficSituationsEventProducer,
)

BASE_URL = "https://opendata.ndw.nu"
SPEED_FILE = "trafficspeed.xml.gz"
TRAVELTIME_FILE = "traveltime.xml.gz"
SITUATION_FILE = "actueel_beeld.xml.gz"

DEFAULT_MEASUREMENTS_TOPIC = "ndl-traffic"
DEFAULT_SITUATIONS_TOPIC = "ndl-traffic-situations"
DEFAULT_POLL_INTERVAL_SECONDS = 60
DEFAULT_STATE_FILE = os.path.expanduser("~/.ndl_netherlands_state.json")

# DATEX II v2 namespace (trafficspeed, traveltime)
DATEX2_NS = "http://datex2.eu/schema/2/2_0"
SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"

# DATEX II v3 namespaces (actueel_beeld situations)
D3_SIT = "http://datex2.eu/schema/3/situation"
D3_COM = "http://datex2.eu/schema/3/common"
D3_MC = "http://datex2.eu/schema/3/messageContainer"

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Connection string / Kafka helpers
# ---------------------------------------------------------------------------

def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs-style connection string into confluent-kafka config."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["entity_path"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = part.split("=", 1)[1].strip('"')
    except (IndexError, ValueError) as exc:
        raise ValueError("Invalid connection string format") from exc
    return config_dict


def _build_kafka_config(connection_string: str, enable_tls: bool = True) -> Tuple[Dict[str, str], Optional[str]]:
    """Build Kafka producer config and extract topic from connection string."""
    topic: Optional[str] = None

    if "BootstrapServer=" in connection_string:
        parts = {}
        for part in connection_string.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                parts[k.strip()] = v.strip().strip('"')
        config: Dict[str, str] = {"bootstrap.servers": parts.get("BootstrapServer", "")}
        topic = parts.get("EntityPath")
    else:
        parsed = parse_connection_string(connection_string)
        config = {
            "bootstrap.servers": parsed.get("bootstrap.servers", ""),
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": "$ConnectionString",
            "sasl.password": connection_string.strip(),
        }
        topic = parsed.get("entity_path")

    if not enable_tls and "security.protocol" not in config:
        config["security.protocol"] = "PLAINTEXT"

    return config, topic


# ---------------------------------------------------------------------------
# XML download + decompress
# ---------------------------------------------------------------------------

def download_gzip_xml(url: str, timeout: int = 120) -> bytes:
    """Download a gzip-compressed file and return the decompressed bytes."""
    req = urllib.request.Request(url, headers={"Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        compressed = resp.read()
    return gzip.decompress(compressed)


# ---------------------------------------------------------------------------
# DATEX II v2 parsers (trafficspeed + traveltime)
# ---------------------------------------------------------------------------

def _find_text(elem: ET.Element, path: str, ns: str = DATEX2_NS) -> Optional[str]:
    """Find text of a child element by local-name path within DATEX II v2 namespace."""
    node = elem.find(path, {"d": ns})
    return node.text.strip() if node is not None and node.text else None


def parse_traffic_speed_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    """Parse trafficspeed DATEX II v2 XML into list of per-site dicts."""
    root = ET.fromstring(xml_bytes)
    ns = {"d": DATEX2_NS, "xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    results: List[Dict[str, Any]] = []

    for sm in root.iter(f"{{{DATEX2_NS}}}siteMeasurements"):
        ref = sm.find(f"{{{DATEX2_NS}}}measurementSiteReference")
        if ref is None:
            continue
        site_id = ref.get("id", "")
        time_elem = sm.find(f"{{{DATEX2_NS}}}measurementTimeDefault")
        mtime = time_elem.text.strip() if time_elem is not None and time_elem.text else ""

        speeds: List[float] = []
        flows: List[int] = []

        for mv in sm.findall(f"{{{DATEX2_NS}}}measuredValue"):
            inner = mv.find(f"{{{DATEX2_NS}}}measuredValue")
            if inner is None:
                continue
            bd = inner.find(f"{{{DATEX2_NS}}}basicData")
            if bd is None:
                continue

            xsi_type = bd.get(f"{{{ns['xsi']}}}type", "")
            if xsi_type == "TrafficSpeed":
                avg_elem = bd.find(f"{{{DATEX2_NS}}}averageVehicleSpeed")
                if avg_elem is not None:
                    spd_elem = avg_elem.find(f"{{{DATEX2_NS}}}speed")
                    if spd_elem is not None and spd_elem.text:
                        val = float(spd_elem.text)
                        if val > 0:
                            speeds.append(val)
            elif xsi_type == "TrafficFlow":
                vf_elem = bd.find(f"{{{DATEX2_NS}}}vehicleFlow")
                if vf_elem is not None:
                    rate_elem = vf_elem.find(f"{{{DATEX2_NS}}}vehicleFlowRate")
                    if rate_elem is not None and rate_elem.text:
                        flows.append(int(rate_elem.text))

        lanes = max(len(speeds), len(flows))
        avg_speed: Optional[float] = round(sum(speeds) / len(speeds), 2) if speeds else None
        total_flow: Optional[int] = sum(flows) if flows else None

        results.append({
            "site_id": site_id,
            "measurement_time": mtime,
            "average_speed": avg_speed,
            "vehicle_flow_rate": total_flow,
            "number_of_lanes_with_data": lanes,
        })

    return results


def parse_travel_time_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    """Parse traveltime DATEX II v2 XML into list of per-site dicts."""
    root = ET.fromstring(xml_bytes)
    ns = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    results: List[Dict[str, Any]] = []

    for sm in root.iter(f"{{{DATEX2_NS}}}siteMeasurements"):
        ref = sm.find(f"{{{DATEX2_NS}}}measurementSiteReference")
        if ref is None:
            continue
        site_id = ref.get("id", "")
        time_elem = sm.find(f"{{{DATEX2_NS}}}measurementTimeDefault")
        mtime = time_elem.text.strip() if time_elem is not None and time_elem.text else ""

        duration: Optional[float] = None
        ref_duration: Optional[float] = None
        accuracy: Optional[float] = None
        data_quality: Optional[float] = None
        n_input: Optional[int] = None

        for mv in sm.findall(f"{{{DATEX2_NS}}}measuredValue"):
            inner = mv.find(f"{{{DATEX2_NS}}}measuredValue")
            if inner is None:
                continue
            bd = inner.find(f"{{{DATEX2_NS}}}basicData")
            if bd is None:
                continue
            xsi_type = bd.get(f"{{{ns['xsi']}}}type", "")
            if xsi_type != "TravelTimeData":
                continue

            tt_elem = bd.find(f"{{{DATEX2_NS}}}travelTime")
            if tt_elem is not None:
                dur_elem = tt_elem.find(f"{{{DATEX2_NS}}}duration")
                if dur_elem is not None and dur_elem.text:
                    val = float(dur_elem.text)
                    duration = val if val >= 0 else None

                acc_val = tt_elem.get("accuracy")
                if acc_val is not None:
                    accuracy = float(acc_val)

                niv = tt_elem.get("numberOfInputValuesUsed")
                if niv is not None:
                    n_input = int(niv)

                dq_val = tt_elem.get("supplierCalculatedDataQuality")
                if dq_val is not None:
                    data_quality = float(dq_val)

            # Reference duration from extension
            ext = inner.find(f"{{{DATEX2_NS}}}measuredValueExtension")
            if ext is not None:
                ext2 = ext.find(f"{{{DATEX2_NS}}}measuredValueExtended")
                if ext2 is not None:
                    brv = ext2.find(f"{{{DATEX2_NS}}}basicDataReferenceValue")
                    if brv is not None:
                        ttd = brv.find(f"{{{DATEX2_NS}}}travelTimeData")
                        if ttd is not None:
                            rtt = ttd.find(f"{{{DATEX2_NS}}}travelTime")
                            if rtt is not None:
                                rd = rtt.find(f"{{{DATEX2_NS}}}duration")
                                if rd is not None and rd.text:
                                    rdv = float(rd.text)
                                    ref_duration = rdv if rdv >= 0 else None

        results.append({
            "site_id": site_id,
            "measurement_time": mtime,
            "duration": duration,
            "reference_duration": ref_duration,
            "accuracy": accuracy,
            "data_quality": data_quality,
            "number_of_input_values": n_input,
        })

    return results


# ---------------------------------------------------------------------------
# DATEX II v3 parser (actueel_beeld situations)
# ---------------------------------------------------------------------------

def parse_situation_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    """Parse actueel_beeld DATEX II v3 XML into list of situation dicts."""
    root = ET.fromstring(xml_bytes)
    results: List[Dict[str, Any]] = []

    for sit in root.iter(f"{{{D3_SIT}}}situation"):
        situation_id = sit.get("id", "")

        vt_elem = sit.find(f"{{{D3_SIT}}}situationVersionTime")
        version_time = vt_elem.text.strip() if vt_elem is not None and vt_elem.text else ""

        sev_elem = sit.find(f"{{{D3_SIT}}}overallSeverity")
        severity = sev_elem.text.strip() if sev_elem is not None and sev_elem.text else None

        header = sit.find(f"{{{D3_SIT}}}headerInformation")
        info_status = "real"
        if header is not None:
            is_elem = header.find(f"{{{D3_COM}}}informationStatus")
            if is_elem is not None and is_elem.text:
                info_status = is_elem.text.strip()

        # Extract first situation record's type and cause
        record_type: Optional[str] = None
        cause_type: Optional[str] = None
        start_time: Optional[str] = None
        end_time: Optional[str] = None

        sr = sit.find(f"{{{D3_SIT}}}situationRecord")
        if sr is not None:
            xsi_type = sr.get(f"{{http://www.w3.org/2001/XMLSchema-instance}}type", "")
            if xsi_type.startswith("sit:"):
                record_type = xsi_type[4:]
            elif xsi_type:
                record_type = xsi_type

            cause_elem = sr.find(f"{{{D3_SIT}}}cause")
            if cause_elem is not None:
                ct_elem = cause_elem.find(f"{{{D3_SIT}}}causeType")
                if ct_elem is not None and ct_elem.text:
                    cause_type = ct_elem.text.strip()

            validity = sr.find(f"{{{D3_SIT}}}validity")
            if validity is not None:
                vts = validity.find(f"{{{D3_COM}}}validityTimeSpecification")
                if vts is not None:
                    st_elem = vts.find(f"{{{D3_COM}}}overallStartTime")
                    if st_elem is not None and st_elem.text:
                        start_time = st_elem.text.strip()
                    et_elem = vts.find(f"{{{D3_COM}}}overallEndTime")
                    if et_elem is not None and et_elem.text:
                        end_time = et_elem.text.strip()

        results.append({
            "situation_id": situation_id,
            "version_time": version_time,
            "severity": severity,
            "record_type": record_type,
            "cause_type": cause_type,
            "start_time": start_time,
            "end_time": end_time,
            "information_status": info_status,
        })

    return results


# ---------------------------------------------------------------------------
# State management for dedup
# ---------------------------------------------------------------------------

class StateManager:
    """Persists last-seen timestamps per site/situation for deduplication."""

    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state: Dict[str, Dict[str, str]] = {"speed": {}, "traveltime": {}, "situation": {}}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            except (json.JSONDecodeError, OSError):
                logger.warning("Could not load state file, starting fresh")

    def save(self) -> None:
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f)
        except OSError:
            logger.warning("Could not save state file")

    def is_new_speed(self, site_id: str, mtime: str) -> bool:
        bucket = self.state.setdefault("speed", {})
        if bucket.get(site_id) == mtime:
            return False
        bucket[site_id] = mtime
        return True

    def is_new_traveltime(self, site_id: str, mtime: str) -> bool:
        bucket = self.state.setdefault("traveltime", {})
        if bucket.get(site_id) == mtime:
            return False
        bucket[site_id] = mtime
        return True

    def is_new_situation(self, situation_id: str, version_time: str) -> bool:
        bucket = self.state.setdefault("situation", {})
        if bucket.get(situation_id) == version_time:
            return False
        bucket[situation_id] = version_time
        return True


# ---------------------------------------------------------------------------
# Poller
# ---------------------------------------------------------------------------

class NdwPoller:
    """Polls NDW open data feeds and emits CloudEvents."""

    def __init__(
        self,
        measurements_producer: NLNDWTrafficMeasurementsEventProducer,
        situations_producer: NLNDWTrafficSituationsEventProducer,
        state: StateManager,
        poll_interval: int = DEFAULT_POLL_INTERVAL_SECONDS,
        base_url: str = BASE_URL,
    ):
        self.measurements_producer = measurements_producer
        self.situations_producer = situations_producer
        self.state = state
        self.poll_interval = poll_interval
        self.base_url = base_url
        self._last_situation_poll: float = 0

    def poll_and_send(self) -> Tuple[int, int, int]:
        """Run one poll cycle. Returns (speed_count, tt_count, sit_count)."""
        speed_count = self._poll_speed()
        tt_count = self._poll_traveltime()
        sit_count = 0

        # Situations update every ~15 min, poll every 10 min
        if time.time() - self._last_situation_poll >= 600:
            sit_count = self._poll_situations()
            self._last_situation_poll = time.time()

        self.state.save()
        return speed_count, tt_count, sit_count

    def _poll_speed(self) -> int:
        url = f"{self.base_url}/{SPEED_FILE}"
        logger.info("Downloading %s", url)
        try:
            xml_bytes = download_gzip_xml(url)
        except Exception:
            logger.exception("Failed to download traffic speed data")
            return 0

        records = parse_traffic_speed_xml(xml_bytes)
        count = 0
        for rec in records:
            if not self.state.is_new_speed(rec["site_id"], rec["measurement_time"]):
                continue
            data = TrafficSpeed(
                site_id=rec["site_id"],
                measurement_time=rec["measurement_time"],
                average_speed=rec["average_speed"],
                vehicle_flow_rate=rec["vehicle_flow_rate"],
                number_of_lanes_with_data=rec["number_of_lanes_with_data"],
            )
            self.measurements_producer.send_nl_ndw_traffic_traffic_speed(
                rec["site_id"], data, flush_producer=False
            )
            count += 1

        if count:
            self.measurements_producer.producer.flush()
        logger.info("Emitted %d traffic speed events (of %d sites)", count, len(records))
        return count

    def _poll_traveltime(self) -> int:
        url = f"{self.base_url}/{TRAVELTIME_FILE}"
        logger.info("Downloading %s", url)
        try:
            xml_bytes = download_gzip_xml(url)
        except Exception:
            logger.exception("Failed to download travel time data")
            return 0

        records = parse_travel_time_xml(xml_bytes)
        count = 0
        for rec in records:
            if not self.state.is_new_traveltime(rec["site_id"], rec["measurement_time"]):
                continue
            data = TravelTime(
                site_id=rec["site_id"],
                measurement_time=rec["measurement_time"],
                duration=rec["duration"],
                reference_duration=rec["reference_duration"],
                accuracy=rec["accuracy"],
                data_quality=rec["data_quality"],
                number_of_input_values=rec["number_of_input_values"],
            )
            self.measurements_producer.send_nl_ndw_traffic_travel_time(
                rec["site_id"], data, flush_producer=False
            )
            count += 1

        if count:
            self.measurements_producer.producer.flush()
        logger.info("Emitted %d travel time events (of %d sites)", count, len(records))
        return count

    def _poll_situations(self) -> int:
        url = f"{self.base_url}/{SITUATION_FILE}"
        logger.info("Downloading %s", url)
        try:
            xml_bytes = download_gzip_xml(url)
        except Exception:
            logger.exception("Failed to download situation data")
            return 0

        records = parse_situation_xml(xml_bytes)
        count = 0
        for rec in records:
            if not self.state.is_new_situation(rec["situation_id"], rec["version_time"]):
                continue
            data = TrafficSituation(
                situation_id=rec["situation_id"],
                version_time=rec["version_time"],
                severity=rec["severity"],
                record_type=rec["record_type"],
                cause_type=rec["cause_type"],
                start_time=rec["start_time"],
                end_time=rec["end_time"],
                information_status=rec["information_status"],
            )
            self.situations_producer.send_nl_ndw_traffic_traffic_situation(
                rec["situation_id"], data, flush_producer=False
            )
            count += 1

        if count:
            self.situations_producer.producer.flush()
        logger.info("Emitted %d situation events (of %d situations)", count, len(records))
        return count

    def run_forever(self) -> None:
        """Main polling loop."""
        logger.info("Starting NDW Netherlands traffic poller (interval=%ds)", self.poll_interval)
        # Force first situation poll
        self._last_situation_poll = 0
        while True:
            try:
                s, t, sit = self.poll_and_send()
                logger.info("Poll cycle complete: speed=%d, traveltime=%d, situation=%d", s, t, sit)
            except Exception:
                logger.exception("Error during poll cycle")
            time.sleep(self.poll_interval)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="NDW Netherlands Road Traffic bridge")
    parser.add_argument("--measurements-topic", default=None, help="Kafka topic for speed/traveltime")
    parser.add_argument("--situations-topic", default=None, help="Kafka topic for situations")
    parser.add_argument("--poll-interval", type=int, default=None, help="Poll interval in seconds")
    parser.add_argument("--state-file", default=None, help="Path to state file for dedup")
    args = parser.parse_args()

    connection_string = os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logger.error("CONNECTION_STRING environment variable is required")
        sys.exit(1)

    enable_tls = os.environ.get("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config, conn_topic = _build_kafka_config(connection_string, enable_tls)

    measurements_topic = (
        args.measurements_topic
        or os.environ.get("KAFKA_TOPIC", "")
        or os.environ.get("MEASUREMENTS_TOPIC", "")
        or conn_topic
        or DEFAULT_MEASUREMENTS_TOPIC
    )
    situations_topic = (
        args.situations_topic
        or os.environ.get("SITUATIONS_TOPIC", "")
        or DEFAULT_SITUATIONS_TOPIC
    )

    poll_interval = args.poll_interval or int(os.environ.get("POLLING_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS))
    state_file = args.state_file or os.environ.get("STATE_FILE", DEFAULT_STATE_FILE)

    producer = Producer(kafka_config)

    measurements_prod = NLNDWTrafficMeasurementsEventProducer(producer, measurements_topic)
    situations_prod = NLNDWTrafficSituationsEventProducer(producer, situations_topic)

    state = StateManager(state_file)
    poller = NdwPoller(measurements_prod, situations_prod, state, poll_interval)
    poller.run_forever()


if __name__ == "__main__":
    main()
