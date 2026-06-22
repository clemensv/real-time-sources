"""EAWS ALBINA avalanche bulletins - transport-neutral acquisition."""
from __future__ import annotations
import datetime, json, os
from typing import Dict, List, Optional, Tuple
import requests
from eaws_albina_producer_data import AvalancheBulletin, AvalancheRegion, MaxDangerRatingenum
DANGER_RATING_MAP = {"low":1,"moderate":2,"considerable":3,"high":4,"very_high":5}
DANGER_RATING_ENUM_MAP = {"low":MaxDangerRatingenum.low,"moderate":MaxDangerRatingenum.moderate,"considerable":MaxDangerRatingenum.considerable,"high":MaxDangerRatingenum.high,"very_high":MaxDangerRatingenum.very_high}
def topic_segment(value: Optional[str]) -> str:
    value = (value or '').strip().lower(); return 'unknown' if (not value or any(ch in value for ch in ('/','+','#','\x00'))) else value
USER_AGENT = os.environ.get("USER_AGENT") or ("real-time-sources-eaws-albina/0.1.0 " "(+https://github.com/clemensv/real-time-sources; " + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")")
DEFAULT_REGIONS = ["AT-07", "IT-32-BZ", "IT-32-TN", "AT-02"]
DEFAULT_LANG = "en"
BASE_URL = "https://avalanche.report/albina_files"
POLL_INTERVAL_SECONDS = 3600
__all__ = ["DANGER_RATING_MAP","DANGER_RATING_ENUM_MAP","topic_segment","USER_AGENT","DEFAULT_REGIONS","DEFAULT_LANG","BASE_URL","POLL_INTERVAL_SECONDS","AlbinaPoller"]
class AlbinaPoller:
    def __init__(self, last_polled_file: str = '', regions: Optional[List[str]] = None, lang: str = DEFAULT_LANG):
        self.last_polled_file = last_polled_file; self.regions = regions or DEFAULT_REGIONS; self.lang = lang
    def load_state(self) -> Dict:
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f: return json.load(f)
        except Exception: pass
        return {'seen_keys': []}
    def save_state(self, state: Dict):
        try:
            directory = os.path.dirname(self.last_polled_file)
            if directory: os.makedirs(directory, exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f: json.dump(state, f, indent=2)
        except Exception as e: print(f'Error saving state: {e}')
    @staticmethod
    def build_url(date_str: str, region: str, lang: str) -> str: return f"{BASE_URL}/{date_str}/{date_str}_{region}_{lang}_CAAMLv6.json"
    @staticmethod
    def fetch_bulletin(url: str, timeout: int = 30) -> Optional[dict]:
        try:
            response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=timeout)
            if response.status_code == 404: return None
            response.raise_for_status(); return response.json()
        except Exception as err:
            print(f'Error fetching {url}: {err}'); return None
    @staticmethod
    def compute_max_danger(danger_ratings: List[dict]) -> Tuple[Optional[str], Optional[int]]:
        max_val = 0; max_name = None
        for dr in danger_ratings:
            name = dr.get('mainValue', ''); val = DANGER_RATING_MAP.get(name, 0)
            if val > max_val: max_val = val; max_name = name
        return (None, None) if max_name is None else (max_name, max_val)
    @staticmethod
    def parse_bulletins(data: dict, lang: str) -> List[AvalancheBulletin]:
        events: List[AvalancheBulletin] = []
        for b in data.get('bulletins', []):
            bulletin_id = b.get('bulletinID', ''); pub_time_str = b.get('publicationTime', ''); valid_time = b.get('validTime', {}); vt_start_str = valid_time.get('startTime', ''); vt_end_str = valid_time.get('endTime', '')
            if not pub_time_str or not vt_start_str or not vt_end_str: continue
            pub_time = datetime.datetime.fromisoformat(pub_time_str); vt_start = datetime.datetime.fromisoformat(vt_start_str); vt_end = datetime.datetime.fromisoformat(vt_end_str); danger_ratings = b.get('dangerRatings', []); max_name, max_val = AlbinaPoller.compute_max_danger(danger_ratings); max_enum = DANGER_RATING_ENUM_MAP.get(max_name) if max_name else None; avalanche_problems = b.get('avalancheProblems', []); tendency_list = b.get('tendency', []); tendency_type = tendency_list[0].get('tendencyType') if tendency_list else None; custom = b.get('customData', {}); lwd = custom.get('LWD_Tyrol', {}); patterns = lwd.get('dangerPatterns'); patterns_json = json.dumps(patterns) if patterns else None; activity = b.get('avalancheActivity', {}); highlights = activity.get('highlights'); snowpack = b.get('snowpackStructure', {}); snowpack_comment = snowpack.get('comment')
            for region in b.get('regions', []):
                region_id = region.get('regionID', ''); region_name = region.get('name', '')
                if not region_id: continue
                events.append(AvalancheBulletin(region_id=region_id, country=topic_segment(region_id.split('-', 1)[0] if region_id else None), region_name=region_name, bulletin_id=bulletin_id, publication_time=pub_time, valid_time_start=vt_start, valid_time_end=vt_end, lang=lang, max_danger_rating=max_enum, danger_level=topic_segment(max_name), max_danger_rating_value=max_val, danger_ratings_json=json.dumps(danger_ratings), avalanche_problems_json=json.dumps(avalanche_problems), tendency_type=tendency_type, danger_patterns_json=patterns_json, avalanche_activity_highlights=highlights, snowpack_structure_comment=snowpack_comment))
        return events
    def fetch_for_date(self, date_str: str):
        state = self.load_state(); seen_keys = set(state.get('seen_keys', [])); new_bulletins = []
        for region in self.regions:
            url = self.build_url(date_str, region, self.lang); data = self.fetch_bulletin(url)
            if data is None: continue
            for event in self.parse_bulletins(data, self.lang):
                dedup_key = f"{event.region_id}:{event.publication_time.isoformat()}"
                if dedup_key in seen_keys: continue
                new_bulletins.append(event); seen_keys.add(dedup_key)
        seen_list = list(seen_keys)
        if len(seen_list) > 5000: seen_list = seen_list[-5000:]
        state['seen_keys'] = seen_list; self.save_state(state); return new_bulletins
    def get_region_catalog(self):
        now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0); regions = []
        for region in self.regions: regions.append(AvalancheRegion(region_id=region, lang=self.lang, configured_at=now, bulletin_base_url=BASE_URL))
        return regions
