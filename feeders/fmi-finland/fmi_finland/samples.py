"""Offline sample corpus for deterministic ``--mock`` runs.

The bridge normally polls the live FMI WFS endpoint, which makes the Docker
E2E flow test dependent on the upstream service being reachable and on it
actually publishing fresh observations during the test window.  To make the
test deterministic, ``--mock`` swaps the upstream HTTP layer for the recorded
WFS-XML fixtures below while still emitting through the real Kafka/MQTT/AMQP
producer.

The XML mirrors the shape FMI returns for the
``fmi::ef::stations`` (station registry) and
``urban::observations::airquality::PT1H::simple`` (hourly air quality)
stored queries.  Each observation element embeds its station ``fmisid`` in the
``gml:id`` so ``_resolve_fmisid`` resolves it without relying on a coordinate
lookup.  Three stations at two hourly timestamps yield three ``Station``
reference events and six ``Observation`` telemetry events (nine messages),
comfortably above the E2E ``min_messages`` floor.
"""

from __future__ import annotations

# Three real Helsinki-region air quality stations.
MOCK_STATIONS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<wfs:FeatureCollection
  xmlns:wfs="http://www.opengis.net/wfs/2.0"
  xmlns:gml="http://www.opengis.net/gml/3.2"
  xmlns:ef="http://inspire.ec.europa.eu/schemas/ef/4.0"
  xmlns:ins_base="http://inspire.ec.europa.eu/schemas/base/3.3">
  <wfs:member>
    <ef:EnvironmentalMonitoringFacility gml:id="station-100662">
      <gml:identifier codeSpace="http://xml.fmi.fi/namespace/stationcode/fmisid">100662</gml:identifier>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/locationcode/name">Helsinki Kallio 2</gml:name>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/location/region">Helsinki</gml:name>
      <ef:name>Helsinki Kallio 2</ef:name>
      <ef:representativePoint>
        <gml:Point gml:id="point-100662">
          <gml:pos>60.187390 24.950600</gml:pos>
        </gml:Point>
      </ef:representativePoint>
    </ef:EnvironmentalMonitoringFacility>
  </wfs:member>
  <wfs:member>
    <ef:EnvironmentalMonitoringFacility gml:id="station-100742">
      <gml:identifier codeSpace="http://xml.fmi.fi/namespace/stationcode/fmisid">100742</gml:identifier>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/locationcode/name">Espoo Leppavaara Lansituuli</gml:name>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/location/region">Espoo</gml:name>
      <ef:name>Espoo Leppavaara Lansituuli</ef:name>
      <ef:representativePoint>
        <gml:Point gml:id="point-100742">
          <gml:pos>60.219180 24.813900</gml:pos>
        </gml:Point>
      </ef:representativePoint>
    </ef:EnvironmentalMonitoringFacility>
  </wfs:member>
  <wfs:member>
    <ef:EnvironmentalMonitoringFacility gml:id="station-100803">
      <gml:identifier codeSpace="http://xml.fmi.fi/namespace/stationcode/fmisid">100803</gml:identifier>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/locationcode/name">Tampere Linja-autoasema</gml:name>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/location/region">Tampere</gml:name>
      <ef:name>Tampere Linja-autoasema</ef:name>
      <ef:representativePoint>
        <gml:Point gml:id="point-100803">
          <gml:pos>61.495300 23.775200</gml:pos>
        </gml:Point>
      </ef:representativePoint>
    </ef:EnvironmentalMonitoringFacility>
  </wfs:member>
</wfs:FeatureCollection>
"""


def _observation_member(gml_id: str, lat: str, lon: str, time: str, param: str, value: str) -> str:
    return (
        '  <wfs:member>\n'
        f'    <BsWfs:BsWfsElement gml:id="{gml_id}">\n'
        f'      <BsWfs:Location><gml:Point gml:id="p-{gml_id}"><gml:pos>{lat} {lon}</gml:pos></gml:Point></BsWfs:Location>\n'
        f'      <BsWfs:Time>{time}</BsWfs:Time>\n'
        f'      <BsWfs:ParameterName>{param}</BsWfs:ParameterName>\n'
        f'      <BsWfs:ParameterValue>{value}</BsWfs:ParameterValue>\n'
        '    </BsWfs:BsWfsElement>\n'
        '  </wfs:member>'
    )


_STATION_COORDS = {
    "100662": ("60.18739", "24.95060"),
    "100742": ("60.21918", "24.81390"),
    "100803": ("61.49530", "23.77520"),
}

# Two hourly windows so each station yields two aggregated observation events.
_OBSERVATION_TIMES = ("2024-01-15T13:00:00Z", "2024-01-15T14:00:00Z")

# Per (station, hour) parameter readings.  AQINDEX plus a couple of pollutants
# per record exercises the full Observation schema; an explicit ``NaN`` checks
# the null-coalescing path in ``_measurement_arg``.
_OBSERVATION_READINGS = {
    "100662": [("AQINDEX_PT1H_avg", "1.0"), ("PM10_PT1H_avg", "12.5"), ("PM25_PT1H_avg", "6.3")],
    "100742": [("AQINDEX_PT1H_avg", "2.0"), ("NO2_PT1H_avg", "18.4"), ("O3_PT1H_avg", "NaN")],
    "100803": [("AQINDEX_PT1H_avg", "3.0"), ("PM10_PT1H_avg", "21.7"), ("SO2_PT1H_avg", "4.1")],
}


def _build_observations_xml() -> str:
    members = []
    for fmisid, (lat, lon) in _STATION_COORDS.items():
        for time in _OBSERVATION_TIMES:
            for index, (param, value) in enumerate(_OBSERVATION_READINGS[fmisid], start=1):
                gml_id = f"BsWfsElement.{fmisid}.{param}.{index}"
                members.append(_observation_member(gml_id, lat, lon, time, param, value))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<wfs:FeatureCollection\n'
        '  xmlns:wfs="http://www.opengis.net/wfs/2.0"\n'
        '  xmlns:gml="http://www.opengis.net/gml/3.2"\n'
        '  xmlns:BsWfs="http://xml.fmi.fi/schema/wfs/2.0">\n'
        + "\n".join(members)
        + '\n</wfs:FeatureCollection>\n'
    )


MOCK_OBSERVATIONS_XML = _build_observations_xml()


def build_offline_api():
    """Return an :class:`FMIAirQualityAPI` that serves the offline corpus.

    The upstream HTTP seam (``get_station_metadata_xml`` /
    ``get_observations_xml``) is overridden to return the recorded fixtures so
    the bridge runs end to end without contacting the live FMI WFS service.
    """

    from fmi_finland.fmi_finland import FMIAirQualityAPI

    class _OfflineFMIAirQualityAPI(FMIAirQualityAPI):
        def get_station_metadata_xml(self) -> str:
            return MOCK_STATIONS_XML

        def get_observations_xml(self, start_time: str, end_time: str) -> str:
            return MOCK_OBSERVATIONS_XML

    return _OfflineFMIAirQualityAPI()
