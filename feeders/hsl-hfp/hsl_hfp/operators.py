"""The HSL HFP operator catalogue.

The HFP ``operator_id`` topic level (and the payload ``oper`` field) is a
numeric identifier of the transit operator that *owns* the vehicle. HSL
publishes the operator-id-to-name mapping in the HFP documentation rather than
in the GTFS feed (GTFS ``agency.txt`` carries only the single umbrella agency
``HSL``), so the table is embedded here and emitted as ``fi.hsl.gtfs.Operator``
reference events at start-up alongside the GTFS-derived routes and stops.

Source: digitransit.fi HFP documentation, "Operators" section
https://digitransit.fi/en/developers/apis/5-realtime-api/vehicle-positions/high-frequency-positioning/
(retrieved for this feeder; refresh if HSL revises the table).
"""

from __future__ import annotations

from typing import Dict, Iterator, Optional, Tuple

# numeric operator id -> (operator name, optional note)
_SHARED = "Multiple smaller operators operate under this shared operator id."
_OPER6 = ("Present only in the payload `oper` field; denotes the same owner as "
          "operator 18 (Oy Pohjolan Liikenne Ab).")

OPERATORS: Dict[int, Tuple[str, Optional[str]]] = {
    6: ("Oy Pohjolan Liikenne Ab", _OPER6),
    12: ("Koiviston Auto Oy", None),
    17: ("Tammelundin Liikenne Oy", None),
    18: ("Oy Pohjolan Liikenne Ab", None),
    20: ("Bus Travel Åbergin Linja Oy", None),
    21: ("Bus Travel Oy Reissu Ruoti", None),
    22: ("Nobina Finland Oy", None),
    30: ("Savonlinja Oy", None),
    36: ("Nurmijärven Linja Oy", None),
    40: ("HKL-Raitioliikenne", None),
    47: ("Taksikuljetus Oy", None),
    50: ("HKL-Metroliikenne", None),
    51: ("Korsisaari Oy", None),
    54: ("V-S Bussipalvelut Oy", None),
    58: ("Koillisen Liikennepalvelut Oy", None),
    59: ("Tilausliikenne Nikkanen Oy", None),
    60: ("Suomenlinnan Liikenne Oy", None),
    64: ("Taksikuljetus Harri Vuolle Oy", None),
    89: ("Metropolia", None),
    90: ("VR Oy", None),
    130: ("Matkahuolto", _SHARED),
    195: ("Siuntio", _SHARED),
}


def iter_operators() -> Iterator[Tuple[str, int, str, Optional[str]]]:
    """Yield ``(operator_id, operator_number, name, note)`` for every operator.

    ``operator_id`` is the 4-digit zero-padded form that appears as the
    ``operator_id`` MQTT-topic level; ``operator_number`` is the bare integer
    that appears in the payload ``oper`` field.
    """
    for num in sorted(OPERATORS):
        name, note = OPERATORS[num]
        yield f"{num:04d}", num, name, note
