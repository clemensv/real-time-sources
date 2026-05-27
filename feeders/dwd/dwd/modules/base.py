"""Abstract base class for DWD data source modules."""

import abc
from typing import Any, Dict, List


class BaseModule(abc.ABC):
    """Each module polls one DWD data category and returns events to emit."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Module identifier used in config and state keys."""
        ...

    @property
    @abc.abstractmethod
    def default_enabled(self) -> bool:
        """Whether this module is on by default."""
        ...

    @property
    @abc.abstractmethod
    def default_poll_interval(self) -> int:
        """Default polling interval in seconds."""
        ...

    @abc.abstractmethod
    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Poll for new data. Returns a list of event dicts.

        Each event dict has:
          - 'type': the event type string (e.g. 'air_temperature_10min')
          - 'data': the payload dict matching the schema
        The module reads from and writes to the state dict for checkpointing.
        """
        ...
