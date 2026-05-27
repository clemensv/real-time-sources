"""TCP socket reader for Kystverket AIS NMEA stream with auto-reconnect."""

import logging
import re
import socket
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Tag block: \s:stationid,c:unixtimestamp*checksum\
_TAG_BLOCK_RE = re.compile(r'^\\s:(\d+),c:(\d+)\*[0-9A-Fa-f]+\\(.+)$')


@dataclass
class RawNMEASentence:
    """A single NMEA sentence with parsed tag block metadata."""
    station_id: str
    receive_time: datetime
    nmea: str  # The NMEA sentence starting with '!'


def parse_tag_block(line: str) -> Optional[RawNMEASentence]:
    """Parse a Kystverket-tagged NMEA line into station_id, timestamp, and NMEA payload."""
    m = _TAG_BLOCK_RE.match(line)
    if not m:
        return None
    station_id = m.group(1)
    unix_ts = int(m.group(2))
    nmea = m.group(3).strip()
    if not nmea.startswith('!'):
        return None
    return RawNMEASentence(
        station_id=station_id,
        receive_time=datetime.fromtimestamp(unix_ts, tz=timezone.utc),
        nmea=nmea,
    )


class TCPSource:
    """Reads NMEA sentences from a TCP socket with auto-reconnect and backoff."""

    def __init__(self, host: str, port: int,
                 timeout: int = 30,
                 max_retry_delay: int = 60):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.max_retry_delay = max_retry_delay
        self._sock: Optional[socket.socket] = None

    def _connect(self) -> socket.socket:
        """Create and connect a TCP socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect((self.host, self.port))
        return sock

    def stream(self, callback: Callable[[RawNMEASentence], None]) -> None:
        """Connect and stream parsed NMEA sentences to the callback.

        Reconnects with exponential backoff on failure. Runs forever until
        interrupted.
        """
        retry_delay = 1

        while True:
            try:
                logger.info("Connecting to %s:%d ...", self.host, self.port)
                self._sock = self._connect()
                logger.info("Connected to Kystverket AIS stream at %s:%d", self.host, self.port)
                retry_delay = 1  # Reset on successful connection

                buf = b''
                while True:
                    data = self._sock.recv(8192)
                    if not data:
                        raise ConnectionError("Connection closed by remote")
                    buf += data
                    while b'\n' in buf:
                        line_bytes, buf = buf.split(b'\n', 1)
                        line = line_bytes.decode('ascii', errors='replace').strip()
                        if not line:
                            continue
                        sentence = parse_tag_block(line)
                        if sentence:
                            callback(sentence)

            except KeyboardInterrupt:
                logger.info("Interrupted — closing connection.")
                break
            except Exception as e:
                logger.warning("Connection error: %s. Reconnecting in %ds...", e, retry_delay)
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self.max_retry_delay)
            finally:
                if self._sock:
                    try:
                        self._sock.close()
                    except Exception:
                        pass
                    self._sock = None
