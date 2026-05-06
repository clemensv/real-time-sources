"""Kusto client wrapping ``azure-kusto-data`` with parameterised
cluster + database settings."""

from __future__ import annotations

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
import pandas as pd

from .config import Config


def _fabric_token_provider():
    """Return a callable that yields a Kusto access token via
    ``notebookutils.credentials.getToken``. Returns ``None`` outside Fabric.
    """
    try:  # pragma: no cover - only available inside Fabric
        import notebookutils  # type: ignore
        # Probe once so we fail fast outside Fabric.
        _ = notebookutils.credentials.getToken("kusto")  # type: ignore[attr-defined]
        return lambda: notebookutils.credentials.getToken("kusto")  # type: ignore[attr-defined]
    except Exception:
        return None


def _client(config: Config) -> KustoClient:
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
    """Execute a KQL query against the configured database and
    return a DataFrame."""
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
