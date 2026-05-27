"""Kusto access layer for querying Bluesky firehose data in Fabric/ADX.

The acquisition and cross-follow stages depend on KQL queries over firehose
tables such as follows, profiles, blocks, and likes. This module hides the
authentication and response-shaping details so higher-level pipeline code
can focus on domain queries and receive plain pandas DataFrames.
"""

from __future__ import annotations

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
import pandas as pd

from .config import Config


def _fabric_token_provider():
    """Get a Fabric notebook token provider when running inside Fabric.
    
    Returns:
        Callable | None: Zero-argument callable producing a Kusto token, or
        ``None`` when ``notebookutils`` is unavailable outside Fabric.
    """
    try:  # pragma: no cover - only available inside Fabric
        import notebookutils  # type: ignore
        # Probe once so we fail fast outside Fabric.
        _ = notebookutils.credentials.getToken("kusto")  # type: ignore[attr-defined]
        return lambda: notebookutils.credentials.getToken("kusto")  # type: ignore[attr-defined]
    except Exception:
        return None


def _client(config: Config) -> KustoClient:
    """Create an authenticated Kusto client for the configured environment.
    
    Args:
        config: Runtime configuration with the Kusto endpoint.
    
    Returns:
        KustoClient: Authenticated client ready to execute KQL.
    
    Notes:
        Fabric notebooks use notebook-scoped tokens, while local CLI usage
        falls back to ``DefaultAzureCredential``. This keeps the rest of the
        pipeline environment-agnostic.
    """
    if not config.kusto_uri:
        raise RuntimeError(
            "Config.kusto_uri is not set. Pass it explicitly, set "
            "BOTFINDER_KUSTO_URI, or use Config.from_fabric_context(...)."
        )

    token_provider = _fabric_token_provider()
    if token_provider is not None:
        kcsb = KustoConnectionStringBuilder.with_token_provider(
            config.kusto_uri, token_provider
        )
    else:
        from azure.identity import DefaultAzureCredential

        credential = DefaultAzureCredential()
        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
            config.kusto_uri, credential
        )
    return KustoClient(kcsb)


def execute_query(config: Config, query: str) -> pd.DataFrame:
    """Execute a KQL query and return the primary result as a DataFrame.
    
    Args:
        config: Runtime configuration containing the Kusto endpoint and
            database.
        query: Fully rendered KQL query string.
    
    Returns:
        pd.DataFrame: Primary query result table converted to pandas.
    
    Notes:
        This is the boundary between KQL templates and Python analysis code.
        All downstream scoring and graph steps expect tabular pandas input, so
        the helper normalizes the SDK response immediately.
    """
    if not config.kusto_database:
        raise RuntimeError(
            "Config.kusto_database is not set. Pass it explicitly or set "
            "BOTFINDER_KUSTO_DATABASE."
        )
    client = _client(config)
    response = client.execute(config.kusto_database, query)
    table = response.primary_results[0]
    columns = [col.column_name for col in table.columns]
    rows = [[row[col] for col in columns] for row in table]
    return pd.DataFrame(rows, columns=columns)
