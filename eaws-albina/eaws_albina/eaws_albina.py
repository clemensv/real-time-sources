"""
EAWS ALBINA Avalanche Bulletin Poller
Polls the ALBINA avalanche.report CAAMLv6 API for daily avalanche bulletins
and sends them to a Kafka topic as CloudEvents.
"""

import os
import json
import sys
import time
import datetime
from typing import Dict, List, Optional, Set, Tuple
import argparse
import requests
from eaws_albina_producer_data import AvalancheBulletin, MaxDangerRatingenum
from eaws_albina_producer_kafka_producer.producer import (
    OrgEAWSALBINABulletinsEventProducer,
)

DANGER_RATING_MAP = {
    "low": 1,
    "moderate": 2,
    "considerable": 3,
    "high": 4,
    "very_high": 5,
}

DANGER_RATING_ENUM_MAP = {
    "low": MaxDangerRatingenum.low,
    "moderate": MaxDangerRatingenum.moderate,
    "considerable": MaxDangerRatingenum.considerable,
    "high": MaxDangerRatingenum.high,
    "very_high": MaxDangerRatingenum.very_high,
}

DEFAULT_REGIONS = ["AT-07", "IT-32-BZ", "IT-32-TN", "AT-02"]
DEFAULT_LANG = "en"
BASE_URL = "https://avalanche.report/albina_files"
POLL_INTERVAL_SECONDS = 3600


class AlbinaPoller:
    """
    Polls the EAWS ALBINA CAAMLv6 API and sends avalanche bulletins to Kafka as CloudEvents.
    """

    def __init__(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        last_polled_file: str,
        regions: Optional[List[str]] = None,
        lang: str = DEFAULT_LANG,
    ):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.regions = regions or DEFAULT_REGIONS
        self.lang = lang
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = OrgEAWSALBINABulletinsEventProducer(kafka_producer, kafka_topic)
        self.kafka_producer = kafka_producer

    def load_state(self) -> Dict:
        """Load the dedup state from disk."""
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"seen_keys": []}

    def save_state(self, state: Dict):
        """Save the dedup state to disk."""
        try:
            directory = os.path.dirname(self.last_polled_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.last_polled_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    @staticmethod
    def build_url(date_str: str, region: str, lang: str) -> str:
        """Build the CAAMLv6 bulletin URL for a given date, region, and language."""
        return f"{BASE_URL}/{date_str}/{date_str}_{region}_{lang}_CAAMLv6.json"

    @staticmethod
    def fetch_bulletin(url: str, timeout: int = 30) -> Optional[dict]:
        """Fetch a single CAAMLv6 JSON bulletin. Returns None on 404 or error."""
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f"Error fetching {url}: {err}")
            return None

    @staticmethod
    def compute_max_danger(danger_ratings: List[dict]) -> Tuple[Optional[str], Optional[int]]:
        """Compute the highest danger rating from a CAAMLv6 dangerRatings array."""
        max_val = 0
        max_name = None
        for dr in danger_ratings:
            name = dr.get("mainValue", "")
            val = DANGER_RATING_MAP.get(name, 0)
            if val > max_val:
                max_val = val
                max_name = name
        if max_name is None:
            return None, None
        return max_name, max_val

    @staticmethod
    def parse_bulletins(data: dict, lang: str) -> List[AvalancheBulletin]:
        """
        Parse a CAAMLv6 JSON response into a list of AvalancheBulletin events.
        One event is emitted per region within each bulletin.
        """
        events: List[AvalancheBulletin] = []
        bulletins = data.get("bulletins", [])
        for b in bulletins:
            bulletin_id = b.get("bulletinID", "")
            pub_time_str = b.get("publicationTime", "")
            valid_time = b.get("validTime", {})
            vt_start_str = valid_time.get("startTime", "")
            vt_end_str = valid_time.get("endTime", "")

            if not pub_time_str or not vt_start_str or not vt_end_str:
                continue

            pub_time = datetime.datetime.fromisoformat(pub_time_str)
            vt_start = datetime.datetime.fromisoformat(vt_start_str)
            vt_end = datetime.datetime.fromisoformat(vt_end_str)

            danger_ratings = b.get("dangerRatings", [])
            max_name, max_val = AlbinaPoller.compute_max_danger(danger_ratings)
            max_enum = DANGER_RATING_ENUM_MAP.get(max_name) if max_name else None

            avalanche_problems = b.get("avalancheProblems", [])
            tendency_list = b.get("tendency", [])
            tendency_type = tendency_list[0].get("tendencyType") if tendency_list else None

            custom = b.get("customData", {})
            lwd = custom.get("LWD_Tyrol", {})
            patterns = lwd.get("dangerPatterns")
            patterns_json = json.dumps(patterns) if patterns else None

            activity = b.get("avalancheActivity", {})
            highlights = activity.get("highlights")
            snowpack = b.get("snowpackStructure", {})
            snowpack_comment = snowpack.get("comment")

            regions = b.get("regions", [])
            for region in regions:
                region_id = region.get("regionID", "")
                region_name = region.get("name", "")
                if not region_id:
                    continue

                event = AvalancheBulletin(
                    region_id=region_id,
                    region_name=region_name,
                    bulletin_id=bulletin_id,
                    publication_time=pub_time,
                    valid_time_start=vt_start,
                    valid_time_end=vt_end,
                    lang=lang,
                    max_danger_rating=max_enum,
                    max_danger_rating_value=max_val,
                    danger_ratings_json=json.dumps(danger_ratings),
                    avalanche_problems_json=json.dumps(avalanche_problems),
                    tendency_type=tendency_type,
                    danger_patterns_json=patterns_json,
                    avalanche_activity_highlights=highlights,
                    snowpack_structure_comment=snowpack_comment,
                )
                events.append(event)
        return events

    def fetch_and_send(self, date_str: str) -> int:
        """Fetch bulletins for all regions for a given date and send new ones to Kafka."""
        state = self.load_state()
        seen_keys: Set[str] = set(state.get("seen_keys", []))
        total_sent = 0

        for region in self.regions:
            url = self.build_url(date_str, region, self.lang)
            data = self.fetch_bulletin(url)
            if data is None:
                continue

            events = self.parse_bulletins(data, self.lang)
            for event in events:
                dedup_key = f"{event.region_id}:{event.publication_time.isoformat()}"
                if dedup_key in seen_keys:
                    continue

                self.producer.send_org_eaws_albina_avalanche_bulletin(
                    event.region_id, event, flush_producer=False
                )
                seen_keys.add(dedup_key)
                total_sent += 1

        if total_sent > 0:
            self.kafka_producer.flush()

        # Keep only the last 5000 seen keys
        seen_list = list(seen_keys)
        if len(seen_list) > 5000:
            seen_list = seen_list[-5000:]
        state["seen_keys"] = seen_list
        self.save_state(state)
        return total_sent

    def poll_and_send(self):
        """Main loop: poll today and yesterday, sleep, repeat."""
        print(f"Starting EAWS ALBINA Avalanche Bulletin poller, polling every {POLL_INTERVAL_SECONDS}s")
        print(f"  Regions: {self.regions}")
        print(f"  Language: {self.lang}")
        print(f"  Kafka topic: {self.kafka_topic}")

        while True:
            try:
                today = datetime.date.today()
                yesterday = today - datetime.timedelta(days=1)
                for d in [today, yesterday]:
                    date_str = d.isoformat()
                    count = self.fetch_and_send(date_str)
                    if count > 0:
                        print(f"Sent {count} bulletin event(s) for {date_str}")
            except Exception as e:
                print(f"Error in polling loop: {e}")

            time.sleep(POLL_INTERVAL_SECONDS)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs-style connection string and extract Kafka parameters."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1]
                    .strip('"')
                    .replace("sb://", "")
                    .replace("/", "")
                    + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def main():
    """Main function to parse arguments and start the ALBINA poller."""
    parser = argparse.ArgumentParser(description="EAWS ALBINA Avalanche Bulletin Poller")
    parser.add_argument("--last-polled-file", type=str, help="State file for deduplication")
    parser.add_argument("--kafka-bootstrap-servers", type=str, help="Kafka bootstrap servers")
    parser.add_argument("--kafka-topic", type=str, help="Kafka topic")
    parser.add_argument("--sasl-username", type=str, help="SASL PLAIN username")
    parser.add_argument("--sasl-password", type=str, help="SASL PLAIN password")
    parser.add_argument(
        "--connection-string",
        type=str,
        help="Azure Event Hubs or Fabric Event Stream connection string",
    )
    parser.add_argument(
        "--regions",
        type=str,
        help="Comma-separated region codes (default: AT-07,IT-32-BZ,IT-32-TN,AT-02)",
    )
    parser.add_argument("--lang", type=str, default="en", help="Language code (default: en)")

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv("CONNECTION_STRING")
    if not args.last_polled_file:
        args.last_polled_file = os.getenv("ALBINA_LAST_POLLED_FILE")
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser("~/.albina_last_polled.json")

    regions = None
    if args.regions:
        regions = [r.strip() for r in args.regions.split(",")]
    elif os.getenv("ALBINA_REGIONS"):
        regions = [r.strip() for r in os.getenv("ALBINA_REGIONS").split(",")]

    lang = args.lang or os.getenv("ALBINA_LANG", "en")

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic")
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: Dict[str, str] = {
        "bootstrap.servers": kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    poller = AlbinaPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        regions=regions,
        lang=lang,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
