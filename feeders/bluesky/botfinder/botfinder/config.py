"""Runtime configuration for the botfinder pipeline.

This module centralizes the knobs that shape one analysis run: which anchor
account to inspect, how far back to query the firehose, how aggressively to
use the public Bluesky API, and where to find the backing Kusto/Fabric
database. Downstream acquisition, scoring, clustering, and CLI code all
read from the same ``Config`` object.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """Parameters controlling one end-to-end anchor analysis.
    
    The object is intentionally small but high leverage: acquisition uses the
    Kusto connection and lookback window, scoring uses the thresholds and API
    budgets, and reporting uses the anchor handle and derived slug.
    
    Attributes:
        anchor_handle: Handle of the anchor account being investigated.
        kusto_uri: Kusto or Fabric query endpoint containing firehose tables.
        kusto_database: Database name holding the Bluesky firehose tables.
        lookback_days: Analysis window for recent follows into the anchor.
        max_followers: Maximum number of followers fetched from the public API
            when extending the cohort beyond KQL timing data.
        enrich_limit: Maximum number of accounts enriched with profile/feed
            detail from the public API.
        api_concurrency: Shared concurrency limit for Bluesky API calls.
        cluster_score_threshold: Minimum bot score for inclusion in the
            co-follow graph stage.
        bot_score_threshold: Threshold used when summarizing likely bots.
        cohort_batch_size: Number of DIDs per batched KQL query.
        skip_api: Whether to disable live Bluesky enrichment and rely on KQL
            data only.
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
        """Fill missing Kusto connection settings from environment variables.
        
        Returns:
            None
        """
        if not self.kusto_uri:
            self.kusto_uri = os.environ.get("BOTFINDER_KUSTO_URI")
        if not self.kusto_database:
            self.kusto_database = os.environ.get("BOTFINDER_KUSTO_DATABASE")

    @property
    def anchor_slug(self) -> str:
        """Return a filesystem-safe version of the anchor handle.
        
        Returns:
            str: Handle with characters such as ``.`` and ``/`` replaced so it can
            be used in output filenames like the dossier HTML path.
        """
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
        """Construct configuration from an attached Microsoft Fabric notebook.
        
        Args:
            anchor_handle: Handle of the anchor account to investigate.
            database_name: Preferred Fabric KQL database name when more than one
                database is attached.
            kusto_uri: Explicit Kusto endpoint override.
            kusto_database: Explicit Kusto database override.
            **overrides: Additional :class:`Config` field overrides such as API
                limits or thresholds.
        
        Returns:
            Config: Configuration with the best available Kusto connection details
            populated.
        
        Notes:
            Resolution order is explicit keyword arguments first, then the bound
            Fabric notebook context via ``notebookutils.kql.listDatabases()``, and
            finally environment-variable fallback in ``__post_init__``.
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
        """Construct configuration using environment-based Kusto discovery.
        
        Args:
            anchor_handle: Handle of the anchor account to investigate.
            **overrides: Optional field overrides applied on top of environment
                defaults.
        
        Returns:
            Config: Configuration instance populated via ``BOTFINDER_*``
            environment variables where needed.
        """
        return cls(anchor_handle=anchor_handle, **overrides)
