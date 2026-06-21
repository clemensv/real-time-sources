from datex2_core import load_endpoints, mock_batch


def test_mock_batch_covers_reference_telemetry_and_situation():
    batch = mock_batch()
    assert batch.measurement_sites and batch.traffic_measurements and batch.situation_records
    assert batch.measurement_sites[0]["supplier_id"] == "sample"


def test_endpoint_loader_accepts_registry_json():
    endpoints = load_endpoints('[{"id":"ndw","url":"https://example.invalid/feed.xml.gz","publication":"MeasuredDataPublication","country":"nl","operator":"ndw"}]')
    assert endpoints[0].id == "ndw"
    assert endpoints[0].country == "nl"

