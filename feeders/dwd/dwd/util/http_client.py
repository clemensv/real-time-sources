"""HTTP client for DWD open data — directory listing parser + file downloader."""

import io
import logging
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

# Apache/nginx directory listing pattern: <a href="filename">filename</a>  date  size
_DIR_ENTRY_RE = re.compile(
    r'<a\s+href="([^"]+)">[^<]+</a>\s+'
    r'(\d{2}-\w{3}-\d{4}\s+\d{2}:\d{2}:\d{2}|\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+'
    r'([\d.]+[KMG]?|-)',
    re.IGNORECASE,
)


@dataclass
class DirEntry:
    """One entry from a DWD directory listing."""
    name: str
    modified: datetime
    size_str: str


def parse_directory_listing(html: str) -> List[DirEntry]:
    """Parse an Apache-style directory listing HTML page into DirEntry objects."""
    entries: List[DirEntry] = []
    for m in _DIR_ENTRY_RE.finditer(html):
        name = m.group(1)
        if name in ("../", "/"):
            continue
        ts_str = m.group(2)
        try:
            if "-" in ts_str[:3]:
                # DD-Mon-YYYY HH:MM:SS format (nginx)
                modified = datetime.strptime(ts_str, "%d-%b-%Y %H:%M:%S").replace(tzinfo=timezone.utc)
            else:
                # YYYY-MM-DD HH:MM format (Apache)
                modified = datetime.strptime(ts_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        except ValueError:
            modified = datetime.min.replace(tzinfo=timezone.utc)
        entries.append(DirEntry(name=name, modified=modified, size_str=m.group(3)))
    return entries


class DWDHttpClient:
    """HTTP client for DWD open data server with ETag caching and retry."""

    def __init__(self, base_url: str = "https://opendata.dwd.de", timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "dwd-bridge/1.0 (https://github.com/clemensv/real-time-sources)"
        self._etags: Dict[str, str] = {}

    def list_directory(self, path: str) -> List[DirEntry]:
        """Fetch and parse a directory listing. Returns empty list on error."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            resp = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return parse_directory_listing(resp.text)
        except Exception as e:
            logger.warning("Failed to list %s: %s", url, e)
            return []

    def check_modified(self, path: str) -> bool:
        """Check if a resource has changed since we last fetched it (via ETag).
        Returns True if changed or unknown, False if 304 Not Modified."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        etag = self._etags.get(url)
        headers = {"If-None-Match": etag} if etag else {}
        try:
            resp = self._session.head(url, headers=headers, timeout=self.timeout)
            if resp.status_code == 304:
                return False
            if "ETag" in resp.headers:
                self._etags[url] = resp.headers["ETag"]
            return True
        except Exception:
            return True

    def download_bytes(self, path: str) -> Optional[bytes]:
        """Download a file and return raw bytes. Returns None on error."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            resp = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            if "ETag" in resp.headers:
                self._etags[url] = resp.headers["ETag"]
            return resp.content
        except Exception as e:
            logger.warning("Failed to download %s: %s", url, e)
            return None

    def download_text(self, path: str, encoding: str = "latin-1") -> Optional[str]:
        """Download a text file. Returns None on error."""
        data = self.download_bytes(path)
        if data is None:
            return None
        return data.decode(encoding)

    def download_zip_csv(self, path: str, encoding: str = "latin-1") -> Optional[str]:
        """Download a ZIP archive and extract its first text file. Returns the CSV text."""
        data = self.download_bytes(path)
        if data is None:
            return None
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                # ZIP contains one data file (produkt_...) and optionally a metadata file
                for name in zf.namelist():
                    if name.startswith("produkt_") or name.endswith(".txt"):
                        return zf.read(name).decode(encoding)
                # Fallback: read first file
                if zf.namelist():
                    return zf.read(zf.namelist()[0]).decode(encoding)
        except Exception as e:
            logger.warning("Failed to extract ZIP from %s: %s", path, e)
        return None
