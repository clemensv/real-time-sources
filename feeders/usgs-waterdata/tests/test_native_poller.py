import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from usgs_waterdata.poller import NativePoller, series_resource
from usgs_waterdata_core.state import DeliveryState

NOW = datetime(2040, 2, 3, 12, tzinfo=timezone.utc)


class Sink:
    def __init__(self):
        self.sent = []
        self.flushes = 0
        self.fail = False

    async def send(self, family, series_id, payload):
        self.sent.append((family, series_id, payload))

    async def flush(self):
        self.flushes += 1
        if self.fail:
            raise RuntimeError("unacknowledged")


def setup(tmp_path, sites=None):
    evidence = json.loads((Path(__file__).parent / "fixtures/synthetic-features.json").read_text(encoding="utf-8"))
    data = evidence["collections"]
    client = Mock()
    series = next(
        row for row in data["time-series-metadata"]["features"]
        if row["properties"]["computation_identifier"] == "Instantaneous"
    )
    location = data["monitoring-locations"]["features"][0]
    parameter = data["parameter-codes"]["features"][0]
    observation = deepcopy(data["continuous"]["features"][0])
    observation["properties"]["time_series_id"] = series["properties"]["id"]
    client.features.side_effect = lambda *a, **k: iter([series])
    client.item.side_effect = lambda collection, key: location if collection == "monitoring-locations" else parameter
    client.observations.return_value = [observation]
    client.changes.return_value = []
    sink, state = Sink(), DeliveryState(tmp_path / "state.json")
    poller = NativePoller(client, sink, state, sites=sites or ["USGS-99000001"], reference_interval=1)
    return poller, client, sink, state, observation, evidence


def test_reference_order_dedupe_and_old_correction(tmp_path):
    poller, client, sink, state, observation, _ = setup(tmp_path)
    assert asyncio.run(poller.cycle(NOW)) == 1
    assert [row[0] for row in sink.sent] == ["MonitoringLocation", "Parameter", "TimeSeries", "ContinuousObservation"]
    assert asyncio.run(poller.cycle(NOW + timedelta(seconds=2))) == 0
    corrected = deepcopy(observation)
    corrected["properties"]["value"] = "999.000"
    client.observations.return_value = []
    client.changes.return_value = [corrected]
    assert asyncio.run(poller.cycle(NOW + timedelta(seconds=4))) == 1
    assert sink.sent[-1][2]["value"] == "999.000"
    assert client.changes.call_args.kwargs.get("start") is None
    assert "modified_until" in state.data


def test_flush_failure_leaves_checkpoint_and_records_retryable(tmp_path):
    poller, _, sink, state, _, _ = setup(tmp_path)
    asyncio.run(poller._references("USGS-99000001", NOW))
    before = deepcopy(state.data)
    sink.fail = True
    with pytest.raises(RuntimeError, match="poll failed"):
        asyncio.run(poller.cycle(NOW))
    assert state.data == before
    assert not state.path.exists()
    sink.fail = False
    assert asyncio.run(poller.cycle(NOW)) == 1


def test_reference_outage_preserves_cache(tmp_path):
    poller, client, _, _, _, _ = setup(tmp_path)
    asyncio.run(poller.cycle(NOW))
    catalog = poller.catalog
    client.item.side_effect = TimeoutError("metadata unavailable")
    assert asyncio.run(poller.cycle(NOW + timedelta(seconds=2))) == 0
    assert poller.catalog is catalog
    assert poller.catalog["USGS-99000001"]


def test_site_failure_does_not_discard_successful_site(tmp_path):
    poller, client, sink, state, _, _ = setup(tmp_path, ["USGS-broken", "USGS-99000001"])
    get_item = client.item.side_effect

    def item(collection, identifier):
        if identifier == "USGS-broken":
            raise TimeoutError("one unavailable site")
        return get_item(collection, identifier)

    client.item.side_effect = item
    with pytest.raises(RuntimeError, match="USGS-broken"):
        asyncio.run(poller.cycle(NOW))
    assert sink.sent[-1][0] == "ContinuousObservation"
    assert set(state.data["modified_until"]) == {"USGS-99000001"}


def test_reference_chunking_and_synthetic_thresholds(tmp_path):
    poller, client, sink, _, _, evidence = setup(tmp_path)
    sample = evidence["collections"]["time-series-metadata"]["features"][0]
    normalized = series_resource(sample)
    assert normalized["thresholds"][0]["periods"][0]["end_time"] == "9999-12-31T23:59:59.9999999+00:00"
    rows = []
    for i in range(80):
        row = deepcopy(sample)
        row["properties"]["id"] = f"series-{i}"
        rows.append(row)
    client.features.side_effect = lambda *a, **k: iter(rows)
    asyncio.run(poller._references("USGS-99000001", NOW))
    assert len(sink.sent) == 240
    assert sink.flushes == 3
