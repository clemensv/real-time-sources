"""Weather alerts module — polls DWD CAP alerts.

DWD publishes alerts as ZIP files containing one or more CAP XML files.
The LATEST_..._DE.zip file contains all currently active alerts in German.
We poll that file, track seen alert identifiers, and emit new ones.
"""

import io
import logging
import zipfile
from typing import Any, Dict, List

from dwd.modules.base import BaseModule
from dwd.parsers.cap_parser import parse_cap_xml
from dwd.util.http_client import DWDHttpClient

logger = logging.getLogger(__name__)

_ALERTS_PATH = "weather/alerts/cap/COMMUNEUNION_DWD_STAT/"
_LATEST_FILE = "Z_CAP_C_EDZW_LATEST_PVW_STATUS_PREMIUMDWD_COMMUNEUNION_DE.zip"


class WeatherAlertsModule(BaseModule):
    """Polls DWD CAP weather alerts via the LATEST ZIP bundle."""

    def __init__(self, http_client: DWDHttpClient):
        self._http = http_client

    @property
    def name(self) -> str:
        return "weather_alerts"

    @property
    def default_enabled(self) -> bool:
        return True

    @property
    def default_poll_interval(self) -> int:
        return 300  # 5 minutes

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Download the LATEST alert bundle, emit new alerts."""
        events: List[Dict[str, Any]] = []
        seen_ids: set = set(state.get("seen_ids", []))

        # Use ETag to skip re-downloading when the bundle hasn't changed
        if not self._http.check_modified(_ALERTS_PATH + _LATEST_FILE):
            logger.debug("weather_alerts: LATEST bundle unchanged (304)")
            return events

        data = self._http.download_bytes(_ALERTS_PATH + _LATEST_FILE)
        if data is None:
            return events

        try:
            zf = zipfile.ZipFile(io.BytesIO(data))
        except zipfile.BadZipFile:
            logger.warning("weather_alerts: bad ZIP file")
            return events

        current_ids: set = set()
        for name in zf.namelist():
            if not name.endswith(".xml"):
                continue
            try:
                xml_text = zf.read(name).decode("utf-8")
            except Exception:
                continue

            alerts = parse_cap_xml(xml_text)
            for alert in alerts:
                aid = alert.get("identifier", name)
                current_ids.add(aid)
                if aid not in seen_ids:
                    events.append({"type": "weather_alert", "data": alert})

        # Update state: remember current alert IDs (drop expired ones)
        state["seen_ids"] = list(current_ids)

        if events:
            logger.info("weather_alerts: emitted %d new alert events", len(events))

        return events
