"""Single-writer Azure Files checkpoints over managed-identity HTTPS."""

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
import json
import logging
import os
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit
import uuid

from azure.core.exceptions import AzureError, ResourceExistsError, ResourceNotFoundError
from azure.identity import ManagedIdentityCredential
from azure.storage.fileshare import ShareClient

logger = logging.getLogger(__name__)


@contextmanager
def _share(path: Path) -> Iterator[tuple[ShareClient, str]]:
    account = os.environ["STATE_AZURE_FILES_ACCOUNT_URL"]
    share_name = os.environ["STATE_AZURE_FILES_SHARE"]
    client_id = os.environ["STATE_AZURE_FILES_CLIENT_ID"]
    root = Path(os.environ["STATE_AZURE_FILES_ROOT"])
    parsed = urlsplit(account)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment or parsed.path not in ("", "/")):
        raise ValueError("STATE_AZURE_FILES_ACCOUNT_URL must be an HTTPS account endpoint without credentials")
    if not share_name or "/" in share_name or "\\" in share_name or not client_id:
        raise ValueError("Azure Files state requires an explicit share and managed identity client ID")
    if not root.is_absolute() or not path.is_absolute():
        raise ValueError("Azure Files state paths and their preserved mount root must be absolute")
    relative = path.relative_to(root).as_posix()
    if relative in ("", ".") or ".." in PurePosixPath(relative).parts:
        raise ValueError("Azure Files checkpoint must be a file under the preserved mount root")
    with ManagedIdentityCredential(client_id=client_id) as credential:
        with ShareClient(account_url=account, share_name=share_name, credential=credential,
                         token_intent="backup", retry_total=3,
                         connection_timeout=10, read_timeout=60) as share:
            yield share, relative


def read_json(path: Path) -> Any:
    with _share(path) as (share, relative):
        try:
            data = share.get_file_client(relative).download_file().readall()
        except ResourceNotFoundError as exc:
            if getattr(exc, "error_code", None) != "ResourceNotFound":
                raise
            return None
        loaded = json.loads(data.decode("utf-8"))
        if loaded is None:
            raise ValueError("Unsupported or corrupt USGS delivery state")
        return loaded


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    encoded = (json.dumps(data, indent=2, allow_nan=False) + "\n").encode("utf-8")
    with _share(path) as (share, relative):
        parent = PurePosixPath(relative).parent
        for index in range(1, len(parent.parts) + 1):
            directory = "/".join(parent.parts[:index])
            try:
                share.get_directory_client(directory).create_directory()
            except ResourceExistsError:
                pass
        stage_name = str(parent / f".{PurePosixPath(relative).name}.{uuid.uuid4().hex}.tmp")
        stage = share.get_file_client(stage_name)
        try:
            stage.upload_file(encoded)
            stage.rename_file(relative, overwrite=True)
        except AzureError:
            try:
                stage.delete_file()
            except ResourceNotFoundError:
                pass
            except AzureError:
                logger.warning("Could not remove a failed Azure Files checkpoint stage", exc_info=True)
            raise
