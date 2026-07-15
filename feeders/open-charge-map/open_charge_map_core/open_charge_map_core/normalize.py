"""Normalization of raw Open Charge Map v3 objects into typed records.

The upstream ``/v3/poi/`` feed carries the stable identity, an expanded nested
``AddressInfo`` object, denormalized operator/usage/status/submission labels,
editorial and freshness timestamps and an expanded ``Connections[]`` array on
each point of interest. This module cracks that representation into a single
:class:`ParsedLocation` (with a flattened address and a list of
:class:`ParsedConnection`) using native Python types, so every transport variant
can build its generated ``ChargingLocation`` / ``Connection`` data classes
without repeating field extraction.

The ``/v3/referencedata/`` document carries nine lookup tables the feeder emits
as reference events; :func:`parse_reference_data` flattens each record into a
:class:`ParsedReference` whose ``fields`` dict is spread straight into the
matching generated reference data class.

Several upstream-shape decisions are normalized here:

* ``AddressInfo`` is flattened onto the location (``latitude`` / ``longitude`` /
  ``town`` / ``country_iso_code`` ...), so the primary coordinates are map-ready
  top-level fields.
* The expanded inline objects (``OperatorInfo.Title``, ``StatusType.Title`` and
  ``.IsOperational``, ``UsageType.Title``, ``SubmissionStatus.Title``,
  ``AddressInfo.Country.ISOCode`` / ``.Title``, and the per-connection
  ``ConnectionType`` / ``Level`` / ``CurrentType`` / ``StatusType`` objects) are
  hoisted into flat denormalized label fields.
* Timestamps (``DateCreated`` / ``DateLastStatusUpdate`` / ``DateLastVerified``
  / ``DateLastConfirmed`` / ``DatePlanned``) are UTC ISO-8601 strings with a
  trailing ``Z``; they are parsed into timezone-aware ``datetime`` values (the
  ``Z`` suffix is normalized because Python 3.10 ``fromisoformat`` rejects it).
* Empty strings are normalized to ``None``.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _clean_str(value: Any) -> Optional[str]:
    """Return a trimmed string, or ``None`` for empty/whitespace/missing values."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _to_int(value: Any) -> Optional[int]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _to_float(value: Any) -> Optional[float]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in ("true", "1", "yes"):
        return True
    if text in ("false", "0", "no"):
        return False
    return None


def parse_ocm_datetime(value: Any) -> Optional[datetime.datetime]:
    """Parse an Open Charge Map ISO-8601 timestamp into a UTC ``datetime``.

    OCM emits instants such as ``2026-07-13T10:00:00Z``. Python 3.10's
    ``datetime.fromisoformat`` does not accept the ``Z`` suffix, so it is
    rewritten to ``+00:00`` first. Naive results are assumed to be UTC. Empty or
    unparseable values yield ``None``.
    """
    text = _clean_str(value)
    if text is None:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


@dataclass
class ParsedConnection:
    """One physical charging connection (connector) on a charging location."""

    connection_id: int
    connection_type_id: Optional[int]
    connection_type_title: Optional[str]
    connection_type_formal_name: Optional[str]
    reference: Optional[str]
    status_type_id: Optional[int]
    is_operational: Optional[bool]
    level_id: Optional[int]
    level_title: Optional[str]
    is_fast_charge_capable: Optional[bool]
    amps: Optional[int]
    voltage: Optional[int]
    power_kw: Optional[float]
    current_type_id: Optional[int]
    current_type_title: Optional[str]
    quantity: Optional[int]
    comments: Optional[str]


@dataclass
class ParsedLocation:
    """One EV charging location (POI) cracked into native-typed fields."""

    poi_id: int
    uuid: str
    data_provider_id: Optional[int]
    operator_id: Optional[int]
    operator_title: Optional[str]
    usage_type_id: Optional[int]
    usage_type_title: Optional[str]
    usage_cost: Optional[str]
    status_type_id: Optional[int]
    status_title: Optional[str]
    is_operational: Optional[bool]
    submission_status_type_id: Optional[int]
    submission_status_title: Optional[str]
    data_quality_level: Optional[int]
    number_of_points: Optional[int]
    general_comments: Optional[str]
    is_recently_verified: Optional[bool]
    date_created: Optional[datetime.datetime]
    date_last_status_update: Optional[datetime.datetime]
    date_last_verified: Optional[datetime.datetime]
    date_last_confirmed: Optional[datetime.datetime]
    date_planned: Optional[datetime.datetime]
    address_id: Optional[int]
    address_title: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    town: Optional[str]
    state_or_province: Optional[str]
    postcode: Optional[str]
    country_id: Optional[int]
    country_iso_code: Optional[str]
    country_title: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    contact_telephone1: Optional[str]
    contact_telephone2: Optional[str]
    contact_email: Optional[str]
    access_comments: Optional[str]
    related_url: Optional[str]
    connections: List[ParsedConnection] = field(default_factory=list)

    def change_signature(self) -> Optional[str]:
        """Return the upstream change watermark used for dedup.

        ``DateLastStatusUpdate`` is Open Charge Map's own record-change instant;
        the ``modifiedsince`` delta is driven by it server-side. Deduping on it
        (falling back to ``DateCreated``) means a location is (re-)emitted only
        when the upstream record actually advanced, even across overlapping poll
        windows.
        """
        marker = self.date_last_status_update or self.date_created
        return marker.isoformat() if marker is not None else None

    def latest_change(self) -> Optional[datetime.datetime]:
        """The most recent editorial instant on the record (for the watermark)."""
        candidates = [
            d
            for d in (
                self.date_last_status_update,
                self.date_created,
                self.date_last_verified,
                self.date_last_confirmed,
            )
            if d is not None
        ]
        return max(candidates) if candidates else None


def _parse_connection(raw: Dict[str, Any]) -> ParsedConnection:
    conn_type: Dict[str, Any] = raw.get("ConnectionType") or {}
    level: Dict[str, Any] = raw.get("Level") or {}
    current_type: Dict[str, Any] = raw.get("CurrentType") or {}
    status_type: Dict[str, Any] = raw.get("StatusType") or {}
    return ParsedConnection(
        connection_id=_to_int(raw.get("ID")) or 0,
        connection_type_id=_to_int(raw.get("ConnectionTypeID")),
        connection_type_title=_clean_str(conn_type.get("Title")),
        connection_type_formal_name=_clean_str(conn_type.get("FormalName")),
        reference=_clean_str(raw.get("Reference")),
        status_type_id=_to_int(raw.get("StatusTypeID")),
        is_operational=_to_bool(status_type.get("IsOperational")),
        level_id=_to_int(raw.get("LevelID")),
        level_title=_clean_str(level.get("Title")),
        is_fast_charge_capable=_to_bool(level.get("IsFastChargeCapable")),
        amps=_to_int(raw.get("Amps")),
        voltage=_to_int(raw.get("Voltage")),
        power_kw=_to_float(raw.get("PowerKW")),
        current_type_id=_to_int(raw.get("CurrentTypeID")),
        current_type_title=_clean_str(current_type.get("Title")),
        quantity=_to_int(raw.get("Quantity")),
        comments=_clean_str(raw.get("Comments")),
    )


def parse_poi(raw: Dict[str, Any]) -> ParsedLocation:
    """Crack one raw Open Charge Map POI object into a :class:`ParsedLocation`."""
    address: Dict[str, Any] = raw.get("AddressInfo") or {}
    country: Dict[str, Any] = address.get("Country") or {}
    operator: Dict[str, Any] = raw.get("OperatorInfo") or {}
    usage_type: Dict[str, Any] = raw.get("UsageType") or {}
    status_type: Dict[str, Any] = raw.get("StatusType") or {}
    submission_status: Dict[str, Any] = raw.get("SubmissionStatus") or {}
    connections_raw = raw.get("Connections") or []

    return ParsedLocation(
        poi_id=_to_int(raw.get("ID")) or 0,
        uuid=str(raw.get("UUID") or ""),
        data_provider_id=_to_int(raw.get("DataProviderID")),
        operator_id=_to_int(raw.get("OperatorID")),
        operator_title=_clean_str(operator.get("Title")),
        usage_type_id=_to_int(raw.get("UsageTypeID")),
        usage_type_title=_clean_str(usage_type.get("Title")),
        usage_cost=_clean_str(raw.get("UsageCost")),
        status_type_id=_to_int(raw.get("StatusTypeID")),
        status_title=_clean_str(status_type.get("Title")),
        is_operational=_to_bool(status_type.get("IsOperational")),
        submission_status_type_id=_to_int(raw.get("SubmissionStatusTypeID")),
        submission_status_title=_clean_str(submission_status.get("Title")),
        data_quality_level=_to_int(raw.get("DataQualityLevel")),
        number_of_points=_to_int(raw.get("NumberOfPoints")),
        general_comments=_clean_str(raw.get("GeneralComments")),
        is_recently_verified=_to_bool(raw.get("IsRecentlyVerified")),
        date_created=parse_ocm_datetime(raw.get("DateCreated")),
        date_last_status_update=parse_ocm_datetime(raw.get("DateLastStatusUpdate")),
        date_last_verified=parse_ocm_datetime(raw.get("DateLastVerified")),
        date_last_confirmed=parse_ocm_datetime(raw.get("DateLastConfirmed")),
        date_planned=parse_ocm_datetime(raw.get("DatePlanned")),
        address_id=_to_int(address.get("ID")),
        address_title=_clean_str(address.get("Title")),
        address_line1=_clean_str(address.get("AddressLine1")),
        address_line2=_clean_str(address.get("AddressLine2")),
        town=_clean_str(address.get("Town")),
        state_or_province=_clean_str(address.get("StateOrProvince")),
        postcode=_clean_str(address.get("Postcode")),
        country_id=_to_int(address.get("CountryID")),
        country_iso_code=_clean_str(country.get("ISOCode")),
        country_title=_clean_str(country.get("Title")),
        latitude=_to_float(address.get("Latitude")),
        longitude=_to_float(address.get("Longitude")),
        contact_telephone1=_clean_str(address.get("ContactTelephone1")),
        contact_telephone2=_clean_str(address.get("ContactTelephone2")),
        contact_email=_clean_str(address.get("ContactEmail")),
        access_comments=_clean_str(address.get("AccessComments")),
        related_url=_clean_str(address.get("RelatedURL")),
        connections=[_parse_connection(c) for c in connections_raw if isinstance(c, dict)],
    )


@dataclass
class ParsedReference:
    """One reference-data record ready to spread into a generated data class.

    ``fields`` is a keyword-argument dict whose keys match the generated
    reference data class exactly (``reference_type`` and ``reference_id`` among
    them), so a transport app can do ``ReferenceClass(**parsed.fields)`` and pick
    the send method by ``reference_type``.
    """

    reference_type: str
    reference_id: int
    fields: Dict[str, Any]

    def signature(self) -> Dict[str, Any]:
        """JSON-safe fingerprint used to re-emit a record only when it changes."""
        return self.fields


def _base_fields(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "reference_type": reference_type,
        "reference_id": _to_int(raw.get("ID")) or 0,
        "title": str(raw.get("Title") or ""),
    }


def _build_operator(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(
        website_url=_clean_str(raw.get("WebsiteURL")),
        comments=_clean_str(raw.get("Comments")),
        phone_primary_contact=_clean_str(raw.get("PhonePrimaryContact")),
        phone_secondary_contact=_clean_str(raw.get("PhoneSecondaryContact")),
        contact_email=_clean_str(raw.get("ContactEmail")),
        booking_url=_clean_str(raw.get("BookingURL")),
        fault_report_email=_clean_str(raw.get("FaultReportEmail")),
        is_private_individual=_to_bool(raw.get("IsPrivateIndividual")),
    )
    return fields


def _build_connection_type(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(
        formal_name=_clean_str(raw.get("FormalName")),
        is_discontinued=_to_bool(raw.get("IsDiscontinued")),
        is_obsolete=_to_bool(raw.get("IsObsolete")),
    )
    return fields


def _build_current_type(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(description=_clean_str(raw.get("Description")))
    return fields


def _build_charger_type(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(
        comments=_clean_str(raw.get("Comments")),
        is_fast_charge_capable=_to_bool(raw.get("IsFastChargeCapable")),
    )
    return fields


def _build_country(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(
        iso_code=_clean_str(raw.get("ISOCode")),
        continent_code=_clean_str(raw.get("ContinentCode")),
    )
    return fields


def _build_data_provider(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    status: Dict[str, Any] = raw.get("DataProviderStatusType") or {}
    fields = _base_fields(reference_type, raw)
    fields.update(
        website_url=_clean_str(raw.get("WebsiteURL")),
        comments=_clean_str(raw.get("Comments")),
        license=_clean_str(raw.get("License")),
        is_open_data_licensed=_to_bool(raw.get("IsOpenDataLicensed")),
        is_restricted_edit=_to_bool(raw.get("IsRestrictedEdit")),
        is_approved_import=_to_bool(raw.get("IsApprovedImport")),
        status_title=_clean_str(status.get("Title")),
        is_provider_enabled=_to_bool(status.get("IsProviderEnabled")),
    )
    return fields


def _build_status_type(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(
        is_operational=_to_bool(raw.get("IsOperational")),
        is_user_selectable=_to_bool(raw.get("IsUserSelectable")),
    )
    return fields


def _build_usage_type(reference_type: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(
        is_pay_at_location=_to_bool(raw.get("IsPayAtLocation")),
        is_membership_required=_to_bool(raw.get("IsMembershipRequired")),
        is_access_key_required=_to_bool(raw.get("IsAccessKeyRequired")),
    )
    return fields


def _build_submission_status_type(
    reference_type: str, raw: Dict[str, Any]
) -> Dict[str, Any]:
    fields = _base_fields(reference_type, raw)
    fields.update(is_live=_to_bool(raw.get("IsLive")))
    return fields


# (reference_type discriminator, OCM referencedata table key, field builder).
# The discriminator is snake_case so it doubles as the send-method suffix:
# ``send_io_open_charge_map_<reference_type>`` on Kafka/AMQP and
# ``publish_io_open_charge_map_mqtt_<reference_type>`` on MQTT.
REFERENCE_SPECS = [
    ("operator", "Operators", _build_operator),
    ("connection_type", "ConnectionTypes", _build_connection_type),
    ("current_type", "CurrentTypes", _build_current_type),
    ("charger_type", "ChargerTypes", _build_charger_type),
    ("country", "Countries", _build_country),
    ("data_provider", "DataProviders", _build_data_provider),
    ("status_type", "StatusTypes", _build_status_type),
    ("usage_type", "UsageTypes", _build_usage_type),
    ("submission_status_type", "SubmissionStatusTypes", _build_submission_status_type),
]


def parse_reference_data(refdata: Dict[str, Any]) -> List[ParsedReference]:
    """Flatten the OCM reference-data document into :class:`ParsedReference` records.

    Only the nine emitted lookup tables are processed; the discriminator/id pair
    keys each record for its reference Kafka topic and CloudEvent subject.
    """
    parsed: List[ParsedReference] = []
    for reference_type, table_key, builder in REFERENCE_SPECS:
        for raw in refdata.get(table_key) or []:
            if not isinstance(raw, dict):
                continue
            reference_id = _to_int(raw.get("ID"))
            if reference_id is None:
                continue
            parsed.append(
                ParsedReference(
                    reference_type=reference_type,
                    reference_id=reference_id,
                    fields=builder(reference_type, raw),
                )
            )
    return parsed
