import json
from pathlib import Path
from unittest.mock import Mock, patch

from azure.core.credentials import AccessToken
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.storage.fileshare import ShareFileClient
import pytest
from requests import Response

from usgs_waterdata_core import azure_files
from usgs_waterdata_core.state import DeliveryState


@pytest.fixture
def share(monkeypatch, tmp_path):
    monkeypatch.setenv("STATE_BACKEND", "azure-files-rest")
    monkeypatch.setenv("STATE_AZURE_FILES_ACCOUNT_URL", "https://synthetic.file.core.windows.net")
    monkeypatch.setenv("STATE_AZURE_FILES_SHARE", "state")
    monkeypatch.setenv("STATE_AZURE_FILES_CLIENT_ID", "synthetic-client")
    monkeypatch.setenv("STATE_AZURE_FILES_ROOT", str(tmp_path))
    credential = Mock()
    credential.__enter__ = Mock(return_value=credential)
    credential.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(azure_files, "ManagedIdentityCredential", Mock(return_value=credential))
    client = Mock()
    client.__enter__ = Mock(return_value=client)
    client.__exit__ = Mock(return_value=False)
    constructor = Mock(return_value=client)
    monkeypatch.setattr(azure_files, "ShareClient", constructor)
    client.constructor = constructor
    client.state_path = tmp_path / "state.json"
    return client


def missing(error_code="ResourceNotFound"):
    error = ResourceNotFoundError("Synthetic missing checkpoint")
    error.error_code = error_code
    return error


def test_remote_checkpoint_atomic_commit_and_restart_preserve_dedupe(share):
    target, stage = Mock(), Mock()
    target.download_file.side_effect = missing()

    def file_client(name):
        return target if name == "state.json" else stage

    share.get_file_client.side_effect = file_client
    path = share.state_path
    state = DeliveryState(path)
    feature = {"properties": {"time_series_id": "series", "time": "2026-11-25T12:00:00Z", "value": "1"}}
    assert state.deliver([feature], lambda feature: None, lambda: 0) == 1
    stage.rename_file.assert_called_once_with("state.json", overwrite=True)
    persisted = json.loads(stage.upload_file.call_args.args[0])
    target.download_file.side_effect = None
    target.download_file.return_value.readall.return_value = json.dumps(persisted).encode()
    restarted = DeliveryState(path)
    assert restarted.deliver([feature], lambda feature: pytest.fail("Duplicate after restart"), lambda: 0) == 0
    assert share.constructor.call_args.kwargs["token_intent"] == "backup"


def test_checkpoint_rename_uses_sdk_overwrite_header(share, monkeypatch):
    credential = Mock(spec=["get_token"])
    credential.get_token.return_value = AccessToken("synthetic-test-token", 4102444800)
    stage = ShareFileClient(
        "https://synthetic.file.core.windows.net", "state", ".state.json.stage.tmp",
        credential=credential, token_intent="backup",
    )
    monkeypatch.setattr(stage, "upload_file", Mock())
    share.get_file_client.return_value = stage
    response = Response()
    response.status_code = 200
    response._content = b""
    response.raw = Mock()
    response.raw.stream.return_value = iter(())
    with patch("requests.sessions.Session.send", return_value=response) as send:
        azure_files.write_json(share.state_path, {"version": 1, "observations": {}})
    assert send.call_args.args[0].headers["x-ms-file-rename-replace-if-exists"] == "true"


def test_remote_write_failure_does_not_advance_acknowledged_state(share):
    target, stage = Mock(), Mock()
    target.download_file.side_effect = missing()
    share.get_file_client.side_effect = lambda name: target if name == "state.json" else stage
    stage.rename_file.side_effect = HttpResponseError("Synthetic rename rejected")
    state = DeliveryState(share.state_path)
    feature = {"properties": {"time_series_id": "series", "time": "2026-11-25T12:00:00Z", "value": "1"}}
    with pytest.raises(HttpResponseError, match="rename"):
        state.deliver([feature], lambda feature: None, lambda: 0)
    assert state.data == {"version": 1, "observations": {}}
    stage.delete_file.assert_called_once()


@pytest.mark.parametrize("error_code", ["ShareNotFound", "AuthorizationPermissionMismatch"])
def test_missing_share_and_access_errors_are_not_empty_state(share, error_code):
    share.get_file_client.return_value.download_file.side_effect = missing(error_code)
    with pytest.raises(ResourceNotFoundError):
        DeliveryState(share.state_path)


@pytest.mark.parametrize("data", [b'{"version":2}', b"null"])
def test_corrupt_remote_state_is_rejected(share, data):
    share.get_file_client.return_value.download_file.return_value.readall.return_value = data
    with pytest.raises(ValueError, match="corrupt"):
        DeliveryState(share.state_path)


def test_remote_state_cannot_escape_preserved_share_root(share):
    with pytest.raises(ValueError):
        DeliveryState(share.state_path.parent.parent / "different" / "state.json")
    share.constructor.assert_not_called()
