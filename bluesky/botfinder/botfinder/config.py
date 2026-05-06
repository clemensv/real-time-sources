"""Configuration for the botfinder pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """Pipeline configuration.

    The Kusto cluster URI and database can be supplied directly,
    discovered from a Fabric notebook context (via
    ``Config.from_fabric_context``), or read from the environment
    variables ``BOTFINDER_KUSTO_URI`` and ``BOTFINDER_KUSTO_DATABASE``.
    """

    anchor_handle: str
    kusto_uri: Optional[str] = None
    kusto_database: Optional[str] = None
    lookback_days: int = 90
    max_followers: int = 5000
    enrich_limit: int = 400
    api_concurrency: int = 10
    cluster_score_threshold: float = 0.45
    bot_score_threshold: float = 0.5
    cohort_batch_size: int = 200
    skip_api: bool = False

    def __post_init__(self) -> None:
        if not self.kusto_uri:
            self.kusto_uri = os.environ.get("BOTFINDER_KUSTO_URI")
        if not self.kusto_database:
            self.kusto_database = os.environ.get("BOTFINDER_KUSTO_DATABASE")

    @property
    def anchor_slug(self) -> str:
        """Filesystem-safe representation of the anchor handle."""
        return self.anchor_handle.replace(".", "_").replace("/", "_")

    @classmethod
    def from_fabric_context(
        cls,
        anchor_handle: str,
        database_name: Optional[str] = None,
        *,
        kusto_uri: Optional[str] = None,
        kusto_database: Optional[str] = None,
        **overrides,
    ) -> "Config":
        """Build a Config using the bound Fabric notebook KQL database.

        Resolution order for ``kusto_uri`` / ``kusto_database``:

        1. Explicit keyword arguments (e.g. from a notebook parameters cell).
        2. ``notebookutils.kql.listDatabases()`` when running inside Fabric.
        3. Environment variables ``BOTFINDER_KUSTO_URI`` /
           ``BOTFINDER_KUSTO_DATABASE`` (handled in :py:meth:`__post_init__`).
        """
        kusto_database = kusto_database or database_name

        if not kusto_uri or not kusto_database:
            try:  # pragma: no cover — only available inside Fabric
                import notebookutils  # type: ignore

                dbs = notebookutils.kql.listDatabases()  # type: ignore[attr-defined]
                chosen = None
                if database_name:
                    chosen = next(
                        (d for d in dbs if d.get("databaseName") == database_name),
                        None,
                    )
                if chosen is None and dbs:
                    chosen = dbs[0]
                if chosen is not None:
                    kusto_uri = kusto_uri or chosen.get("queryServiceUri")
                    kusto_database = kusto_database or chosen.get("databaseName")
            except Exception:
                pass

        return cls(
            anchor_handle=anchor_handle,
            kusto_uri=kusto_uri,
            kusto_database=kusto_database,
            **overrides,
        )

    @classmethod
    def from_env(cls, anchor_handle: str, **overrides) -> "Config":
        return cls(anchor_handle=anchor_handle, **overrides)
