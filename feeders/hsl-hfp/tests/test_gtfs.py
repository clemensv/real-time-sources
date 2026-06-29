"""Tests for the HSL GTFS-static reference fetch/parse.

HSL ships ``routes.txt``/``stops.txt`` as windows-1252 text with empty optional
columns padded to a single space. The parser must decode the Latin text
correctly, coerce the documented integer/float columns, and normalize the
whitespace padding to ``None`` so empty values never leak onto the wire.
"""

from __future__ import annotations

import io
import zipfile

from hsl_hfp.hfp_gtfs import GtfsStatic


_ROUTES = (
    "route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url\r\n"
    "1059,HSL,59,Kamppi - Sornainen, ,3, \r\n"
)
# 'Sornainen' uses the o-with-diaeresis below to exercise windows-1252 decode.
_STOPS = (
    "stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,"
    "location_type,parent_station,platform_code,wheelchair_boarding,vehicle_type,digistop_id\r\n"
    "1284,H1234,S\u00f6rn\u00e4inen, ,60.19,24.94,A, ,0, , ,1,3, \r\n"
)


def _zip_bytes() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as archive:
        archive.writestr("routes.txt", _ROUTES.encode("windows-1252"))
        archive.writestr("stops.txt", _STOPS.encode("windows-1252"))
    return buf.getvalue()


def _gtfs(monkeypatch) -> GtfsStatic:
    data = _zip_bytes()
    gtfs = GtfsStatic("http://example.invalid/hsl.zip")
    monkeypatch.setattr(gtfs, "_download", lambda: zipfile.ZipFile(io.BytesIO(data)))
    return gtfs


class TestGtfsParse:
    def test_route_row_parsed(self, monkeypatch):
        snapshot = _gtfs(monkeypatch).fetch()
        assert len(snapshot.routes) == 1
        route = snapshot.routes[0]
        assert route["route_id"] == "1059"
        assert route["route_type"] == 3  # int coercion
        assert route["route_desc"] is None  # ' ' -> None
        assert route["route_url"] is None

    def test_stop_row_windows1252_decoded(self, monkeypatch):
        snapshot = _gtfs(monkeypatch).fetch()
        stop = snapshot.stops[0]
        assert stop["stop_name"] == "S\u00f6rn\u00e4inen"

    def test_stop_numeric_coercion(self, monkeypatch):
        snapshot = _gtfs(monkeypatch).fetch()
        stop = snapshot.stops[0]
        assert stop["stop_lat"] == 60.19
        assert stop["stop_lon"] == 24.94
        assert stop["location_type"] == 0
        assert stop["wheelchair_boarding"] == 1
        assert stop["vehicle_type"] == 3

    def test_stop_whitespace_padding_normalized(self, monkeypatch):
        snapshot = _gtfs(monkeypatch).fetch()
        stop = snapshot.stops[0]
        assert stop["stop_desc"] is None
        assert stop["parent_station"] is None
        assert stop["platform_code"] is None
