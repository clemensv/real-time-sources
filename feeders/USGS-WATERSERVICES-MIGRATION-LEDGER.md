# USGS WaterServices migration work ledger

Updated: 2026-11-23. Repository baseline: `41a32d93d9080c9b125d641e89ce328f0cda39ce`.

Draft migration PR: [#1762](https://github.com/clemensv/real-time-sources/pull/1762).
The branch contains only the USGS migration on current `origin/main`; unrelated
inherited work remains on its original branches. Local validation and all
review corrections passed. Cloud release gates remain blocked in
[#1761](https://github.com/clemensv/real-time-sources/issues/1761); no merge,
image publication or production cutover has occurred.

## Decision and current status

Implement two tracks:

1. A new [usgs-waterdata](usgs-waterdata/) feeder with native OGC identities and
   separate event types/topics. The user selected continuous observations plus
   monitoring-location, time-series and parameter reference data. Other OGC
   products are outside this task.
2. Transitional OGC acquisition in [usgs-iv](usgs-iv/) and
   [usgs-nwis-wq](usgs-nwis-wq/), with their existing contracts, generated
   producers, source identifiers and key semantics unchanged. Only explicitly
   enrolled legacy identities are eligible; previously unknown series belong
   in the native feed until their legacy identity is established.

Worktree: `C:\git\rts-usgs-waterdata`.
Branch: `feature/usgs-waterdata-migration`.
The original working tree and its unrelated changes are not part of this work.

**Implementation and local transport acceptance passed; cloud release is blocked.** The
native feeder has four event families, generated Kafka/MQTT/AMQP producers,
three container variants, six ARM templates, a notebook, KQL and documentation.
Both existing feeders have opt-in OGC acquisition on all three transports.
Their legacy acquisition remains the default; no production cutover occurred.

### Accepted upstream constraints (November 23)

Proceed using the information supplied by USGS on November 17 and 18.
Further upstream answers are not a prerequisite for the scoped sample
implementation. This decision does not authorize fabricated legacy identities,
reduced metadata fidelity, a contract change or a production cutover.

- **Identity:** no direct legacy TS_ID crosswalk exists. Use native IDs for
  the new feeder. Keep transitional output limited to verified enrollment.
  Mike's suggested `sublocation_id` and `web_description` comparison with
  legacy `timeSeries.values.method.methodDescription` is additional evidence,
  not proof of identity. His linked endpoint uses v0. The November 23
  re-audit confirms v1 exposes nullable `sublocation_identifier` and
  `web_description`; both were populated in live examples. Use those actual
  v1 field names if this comparison is added to capture tooling.
  New or ambiguous series use the native feed, not invented numeric IDs.
- **Metadata:** the [migration guide][migration] explicitly discontinues the
  legacy fields listed below. Historical supplements remain historical; do
  not claim they provide current values or coverage for new sites. Keep
  transformed geometry and its coordinate reference system distinct from
  the original datum.
- **Qualifiers:** approval status is separate from value qualifiers. The full
  qualifier reference is not yet published. Preserve native values; legacy
  projection accepts only reviewed translations and rejects unknown values.
  Examples such as `Revised` and `Ice` are not a complete mapping table.
- **Thresholds:** USGS confirmed the intended representation is a JSON array
  when present and the schema mismatch is in its backlog. Retain the current
  array-based contract; no schema relaxation is needed.
- **Corrections and withdrawals:** complete `last_modified` coverage and
  deletion notification remain unconfirmed. Retain the implemented overlapping
  reads and correction-aware dedupe, but do not claim complete synchronization.
  An observation absent from a query is not evidence of withdrawal. No
  withdrawal event or automatic downstream deletion is introduced.

The feeders are sample code provided as-is, not a supported production
service. Scoped sample acceptance and production completeness remain separate.
The Azure policy and Fabric hosting/authentication gates below are unchanged.
Their resolution is tracked in [#1761](https://github.com/clemensv/real-time-sources/issues/1761).

### November 23 PR review corrections

### November 24 CI remediation

The IV resilience fixture now mocks all three producer groups with confirmed
flush results and uses a bounded once-mode cycle. Tests no longer catch every
exception or depend on the seven-day refresh boundary's timing. The vendor
freshness check accepts Git-converted CRLF manifest text without changing the
wheel bytes. A focused regression covers that checkout case.

The WQ Service Bus emulator failure was a 300-second container-wait timeout.
The harness now reports feeder logs before cleanup on that failure; its
deadline and required wire assertions are unchanged. The same strict WQ
emulator case passed locally without retries after this diagnostic change.

Local checks: 66 IV offline tests using CI import/selection options, all three
installed IV runtime imports, complete IV compilation, 51 shared regressions
and producer-aware mypy over 1,332 files passed. The vendored core wheel remains
byte-identical. Remote CI must verify the pushed remediation before green
status is claimed.

### November 23 validation detail

The final code reviewer closed all four findings after corrections:

- IV MQTT now rejects unsuccessful PUBACKs on all three connections. The
  actual-Paho rejection reproduction no longer advances the checkpoint.
- Short legacy IV cycles confirm series references before dependent telemetry
  and drain reference delivery before saving state.
- Native and legacy fixtures/enrollment examples are newly constructed
  synthetic scenarios. Original recordings and reviewed operator enrollment
  remain outside Git.
- Native deployment links now select the implemented Event Hubs, Service Bus
  and Fabric ACI routes.

Current local results are native 63, IV 65 and WQ 80 offline tests; 51 shared
regressions; producer-aware fleet mypy over 1,332 files; compilation of all 138
changed/new Python files; 18 clean ARM audits and 33 clean notebook checks.
Nine no-cache images built, with an additional three-image IV no-cache build
after the acknowledgement corrections. Native ARM regeneration ran twice in
an external verification tree; all six templates matched checkout byte-for-byte.

Live transitional tests require reviewed external enrollment through
`USGS_E2E_ENROLLMENT_FILE`. CI materializes the encrypted
`USGS_E2E_ENROLLMENT_JSON` repository secret in `RUNNER_TEMP`; normal image
build contexts and Git do not contain the operator record. The test builder injects it only
into its temporary context. Missing CI configuration fails explicitly.

The final consolidated command passed all 13 selected real-data wire cases
in 1,427.22 seconds:

```powershell
python -m pytest tests\docker_e2e\test_docker_kafka_flow.py `
  tests\docker_e2e\test_docker_mqtt_flow.py `
  tests\docker_e2e\test_docker_amqp_flow.py `
  tests\docker_e2e\test_docker_amqp_sb_emulator_flow.py `
  tests\docker_e2e\test_docker_amqp_artemis_flow.py `
  -k 'USGSWaterData or USGSIV or UsgsNwisWq' -v `
  --kafka-artifacts-dir=<external-artifact-directory>
```

The earlier run without the external enrollment record failed after fixture
sanitization; the final configured run passed without skips or retry masking.
Generated producer/KQL whitespace is retained to preserve exact generator
output. The staged whitespace check is clean for handwritten files.

Real broker tests have passed for Kafka, MQTT and AMQP on all three feeders.
All three AMQP implementations passed both Artemis and the Service Bus
emulator; the WQ Artemis compatibility entry point passed as well. These
13 distinct cases passed across focused runs, not a single all-green matrix
invocation. Required reference and telemetry families, schemas and transport
identities were checked without mocks or skipped acceptance. This is local
acceptance, not image publication, production deployment or cutover. The
November 23 PR review and validation results above supersede the earlier counts.

Cloud release has two explicit blockers: the existing Azure policy prohibits
the shared-key storage used by the stateful ACI templates, and the shared
Fabric deployer's kernel/Environment and authentication paths require an
approved replacement. Six native ARM-engine validations were attempted in
an isolated empty resource group; all were blocked by policy. That resource
group was deleted and its absence verified.

The [USGS shutdown notice][shutdown] confirms permanent shutdown on
**2027-02-22**. USGS correspondence reviewed for this investigation specifies
slowdowns from **2026-11-16** and intentional outages from **2027-01-27**.
The linked [public degradation schedule][schedule] returned HTTP 403 here;
its detailed timetable was not independently retrieved.

Recommended planning target, not a deployment commitment: resolve identity and
metadata questions during the week of November 16, then complete comparison and
cutover during December 2026, before the January outage period. Start preserving
legacy metadata and identity evidence now, while the old services still answer.

## Native API scope

The complete collection index was enumerated before the user selected the
continuous-only scope. This table records the disposition of every collection.
Exclusion here follows that explicit scope decision, not a claim that the
excluded products lack useful or regularly updated data.

| Collections | Decision | Reason |
|---|---|---|
| `continuous` | Keep | Continuous observations with native series/location/parameter identifiers, observation time, precision-preserving value strings and approval/qualifier metadata. |
| `latest-continuous` | Duplicate presentation | Latest values for the same continuous series; bounded `continuous` reads also support overlap and corrections. Do not emit duplicate event families. |
| `monitoring-locations` | Keep | Location reference events, including all documented properties and geometry. |
| `time-series-metadata` | Keep | Reference events for the instantaneous series represented by continuous observations, including structured thresholds and sublocation/computation metadata. |
| `parameter-codes` | Keep | Parameter reference events and documented names/units. |
| `latest-daily`, `daily`, `edr/daily` | Exclude | Daily products, outside the selected continuous-observation scope. |
| `latest-field-measurements`, `field-measurements`, `channel-measurements`, `field-measurements-metadata` | Exclude | Field-visit and channel-measurement products, outside the selected scope. |
| `peaks` | Exclude | Peak-flow product, outside the selected scope. |
| `combined-metadata` | Exclude | Cross-product metadata presentation; use the selected location/series reference collections directly. |
| `time-series-revisions`, `time-series-methods` | Exclude standalone events | Additional revision/method histories were not included in the selected reference scope. Preserve the method category supplied on continuous observations; do not claim a complete method-history feed. |
| `agency-codes`, `altitude-datums`, `aquifer-codes`, `aquifer-types`, `coordinate-accuracy-codes`, `coordinate-datum-codes`, `coordinate-method-codes` | Exclude standalone events | Additional lookup catalogs outside the selected three reference families; preserve supplied codes and labels on location events. |
| `counties`, `countries`, `hydrologic-unit-codes`, `national-aquifer-codes`, `site-types`, `states`, `topographic-codes`, `time-zone-codes` | Exclude standalone events | Geographic/site lookup catalogs outside the selected reference scope. `states` remains usable for validated abbreviation-to-code acquisition configuration. |
| `medium-codes`, `methods`, `method-categories`, `method-citations`, `citations`, `combined-method-citations`, `reliability-codes`, `statistic-codes` | Exclude standalone events | Additional classification/method/citation catalogs outside the selected reference scope. Preserve applicable upstream identifiers on the selected events. |

Resolved schema/documentation discrepancy: `time-series-metadata/schema`
describes `thresholds` as a string, while live responses use an array.
The native contract models the threshold objects from non-empty live examples;
USGS confirmed the array representation on November 18. The November 23 API re-audit reconfirmed all 39 collections and
coverage of the four retained resources.

## Affected APIs and repository surfaces

| Existing API | Actual use | Replacement | Disposition |
|---|---|---|---|
| `waterservices.usgs.gov/nwis/iv/`, RDB | [IV runtime](usgs-iv/usgs_iv/usgs_iv.py): per-state `stateCd`, `modifiedSince=PT2H`; column names supply numeric `TS_ID` and parameter code | [`continuous/items`][continuous], joined to [`time-series-metadata`][series] | Migrate acquisition and parsing; preserve all existing parameter families, including `OtherParameter` |
| `waterservices.usgs.gov/nwis/site/`, expanded RDB | IV site inventory, startup/refresh, and site-list CLI commands | [`monitoring-locations`][locations] plus an explicitly managed legacy metadata supplement if required | Migrate all callers, not just telemetry; resolve missing fields before cutover |
| `waterservices.usgs.gov/nwis/iv/`, JSON | [WQ Kafka runtime](usgs-nwis-wq/usgs_nwis_wq/usgs_nwis_wq.py): per-state or explicit sites, parameter selection, two-hour observation window | `continuous/items` plus monitoring-location and parameter/time-series metadata | Migrate continuous sensor readings; this is not a discrete-sample feed |
| Same IV JSON endpoint | [WQ AMQP runtime](usgs-nwis-wq/usgs_nwis_wq_amqp/usgs_nwis_wq_amqp/app.py): independent fetch/parser and defaults | Same OGC acquisition adapter | Must replace its separate legacy path too |
| `/nwis/dv/` and `/nwis/stat/` | Services advertised on the retiring WaterServices site; no runtime call found in the repository search | [`daily`][daily] and [Water Data Statistics API][statistics] | Affected upstream services, but no feeder migration identified here |
| Water Quality Portal / Samples API | Not the source used by `usgs-nwis-wq` | No substitution proposed | Do not replace continuous readings with discrete laboratory samples |
| Earthquake and geomagnetic APIs | [Earthquake runtime](usgs-earthquakes/usgs_earthquakes/usgs_earthquakes.py) uses `earthquake.usgs.gov`; [geomagnetic runtime](usgs-geomag/usgs_geomag/usgs_geomag.py) uses `geomag.usgs.gov` | None for this notice | Outside this WaterServices migration |

Repository search covered legacy water-service host/path references in Python,
JSON, Markdown, TOML and notebooks, plus PowerShell, YAML and shell scripts.
Only the two water feeders were identified as runtime consumers. This is a
repository inventory, not an inventory of deployed resources or external clients.

Deployment coverage:

- IV Kafka, MQTT and AMQP now share the transitional acquisition path.
  The distinct series-reference producer is wired as well as site/value
  producers. Live acceptance tests disable mocks and require all configured
  reference and telemetry families.
- WQ Kafka, MQTT and AMQP now share OGC normalization when opted in.
  Legacy defaults and each transport's routing/configuration remain intact.
- [WQ MQTT](usgs-nwis-wq/usgs_nwis_wq_mqtt/usgs_nwis_wq_mqtt/app.py) now
  defaults to real legacy polling instead of unconditional mocks. Its OGC
  flow now passes strict real-broker validation, including acknowledged delivery.
- Both feeders have [IV notebook](usgs-iv/notebook/usgs-iv-feed.ipynb) /
  [WQ notebook](usgs-nwis-wq/notebook/usgs-nwis-wq-feed.ipynb) deployment surfaces.
  Rebuild their wheel bundles and test scheduled runs after runtime migration.
- Updated source/API descriptions in both feeders' README and CONTAINER documents,
  the native root catalog entry and [upstream links](../tools/docs/upstream_links.json).
  Classify URL occurrences: historical CloudEvent source identifiers must not be
  mechanically replaced with HTTP acquisition URLs.

## Evidence gathered on November 16

These are bounded probes, not national coverage or transport validation.

| Probe | Result and migration consequence |
|---|---|
| Legacy IV RDB | Numeric legacy series identity is part of the current event key. |
| New continuous data without a time filter | The first page can contain historical observations. Never assume a first page means latest data. |
| New continuous data, `datetime=PT2H` | HTTP 400: `InvalidParameterValue`, `Unknown string format: PT2H`, despite the long-form guide's duration example. |
| New continuous data, `time=PT2H` | Accepted. A matching value without a matching instant does not prove an identity crosswalk. |
| Legacy WQ JSON | Active and discontinued methods can coexist. Approval and qualifier codes need explicit translation. |
| Paired continuous WQ queries | Comparable temperature observations were found; that does not establish coverage of every WQ parameter or a permanent identity mapping. |
| New state query, `state_code=10` | Accepted and paginated. CLI `DE` must translate to ANSI/FIPS `10`. |
| New location lookup with `monitoring_location_id=...` on collection items | HTTP 400. Location collection uses `id`, unlike continuous/series collections. Exact `/items/USGS-01646500?f=json` succeeded. |
| Expanded legacy site and new location | New location omits several legacy fields; altitude accuracy can differ. Coordinates and their datum metadata also require semantic checks. |
| New time-series metadata | HTTP 200. Unfiltered first page included a daily mean series; restrict discovery to the required computation families. Instantaneous sample has `computation_period_identifier=Points`, `computation_identifier=Instantaneous`, `statistic_id=00011`. |
| Current [OpenAPI][openapi] and collection queryables | Read successfully. Continuous has `time_series_id`, `time`, `last_modified`, state and parameter filters. Default page size is 10, maximum 50,000; live responses supply cursor-based `rel=next` links. |
| Fixed-window paired capture | Expanded sites, legacy JSON/RDB, OGC observations and instantaneous metadata were captured outside Git. Candidate temperature/discharge correspondences require explicit review; none were automatically enrolled. |
| Same fixed observation window, `limit=10` | Actual continuation links were followed to completion. An accepted empty `last_modified` query does not establish changed-record coverage. The separate `changes` method omits an observation-time filter so older corrections are not excluded. |

Reproducible public examples:

- [Legacy IV RDB sample](https://waterservices.usgs.gov/nwis/iv/?format=rdb&sites=01646500&parameterCd=00060&period=PT1H)
- [Legacy expanded site sample](https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=01646500&siteOutput=expanded)
- [Legacy WQ JSON sample](https://waterservices.usgs.gov/nwis/iv/?format=json&sites=01646500&parameterCd=00010&period=PT2H)
- [New continuous streamflow sample](https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/items?f=json&limit=1&monitoring_location_id=USGS-01646500&parameter_code=00060&time=PT2H)
- [New continuous temperature sample](https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/items?f=json&limit=1&monitoring_location_id=USGS-01646500&parameter_code=00010&time=PT2H)
- [New location sample](https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/items/USGS-01646500?f=json)
- [New instantaneous series sample](https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/items/66a4e3fb8abe42fcb0942b5c0fe98f68?f=json)

Relative-window URLs return changing results. Implementation work must capture
public, fixed-window fixtures with retrieval timestamps before asserting parity.

## Compatibility boundary

Freeze these authoritative manifests, including their transport bindings:

| Contract | Baseline SHA-256 of file bytes |
|---|---|
| [IV xRegistry](usgs-iv/xreg/usgs-iv.xreg.json) | `78ee87c65010d5763928fd4ff199555cf449ebd1fcee6c599225aa5d74016197` |
| [WQ xRegistry](usgs-nwis-wq/xreg/usgs_nwis_wq.xreg.json) | `d96b56e93494811527e850e3c85159541dbe5aeff14febd53a5b8e84d4fa3f62` |

Do not regenerate producers, edit generated classes, change schema IDs/versions,
rename types, add fields, relax nullability, change numeric types, or change
KQL table/mapping shapes for this acquisition-only migration.

Preserve:

| Event family | CloudEvent type / identity |
|---|---|
| IV site | `USGS.Sites.Site`; subject and Kafka key `{agency_cd}/{site_no}` |
| IV series reference | `USGS.Sites.SiteTimeseries`; subject and key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| IV measurements | All 26 existing `USGS.InstantaneousValues.*` types; same four-part subject/key as series reference |
| WQ site | `USGS.WaterQuality.Sites.MonitoringSite`; subject/key `{site_number}` |
| WQ measurement | `USGS.WaterQuality.Readings.WaterQualityReading`; subject/key `{site_number}/{parameter_code}` |

Keep the current topics (`usgs-iv`, `usgs-nwis-wq`, or operator overrides),
MQTT topic templates/QoS/retain settings, AMQP routing properties/partition
identity, content modes, serialization, and each family's current time policy.
IV measurement time represents observation time; do not introduce a new envelope
time policy for WQ as part of this migration.

The runtime currently supplies `https://waterservices.usgs.gov/nwis/iv/` as
CloudEvent `source`. **Keep that value as a historical logical source identifier**
while configuring a separate OGC acquisition base URL. A CloudEvent source URI
need not be a working fetch endpoint. Changing it would split downstream
source-based identities and materialized latest views.

### Measurement translation

| Existing output | OGC input / compatibility rule |
|---|---|
| `agency_cd`, `site_no`, WQ `agency_code`, `site_number` | Join monitoring location; retain string IDs and leading zeros. `USGS-01646500` must not become the outward site number. Validate agency and number rather than coercing IDs to integers. |
| IV `parameter_cd`, WQ `parameter_code` | Preserve five-digit `parameter_code` and current event-family dispatch. Preserve unknown-parameter handling and distinguish datum/unit-specific families. |
| IV `timeseries_cd` | Resolve from a persistent, validated new-series-to-legacy-TS_ID crosswalk. Do not copy the new opaque ID into this field without an approved identity change. |
| IV `datetime`, WQ `date_time` | Parse offset-aware `time`. Preserve observation instant and existing per-feeder formatting policy; IV currently formats site-local offsets, WQ Kafka uses UTC. Test DST, Arizona, Alaska and territories. |
| IV/WQ numeric `value` | Parse the upstream string into the existing generated numeric type. Match legacy no-data and nonnumeric handling; do not emit sentinel values as genuine measurements or replace missing values with zero. |
| IV `exception`, `EquipmentStatus.status` | Preserve documented special-value/status meaning; do not cast all observations through a numeric-only adapter. Confirm new API encodings with USGS. |
| IV `qualifiers`, WQ `qualifier` | Translate `approval_status` separately from `qualifier`. Validate `Provisional -> P`, `Approved -> A`, estimated/ice/other codes, ordering and per-transport string/list representation against legacy fixtures. A null OGC qualifier does not mean legacy qualifier `P` vanished. |
| WQ `site_name`, `site_type`, geographical fields | Join monitoring-location metadata; preserve name/description decoding and existing field conventions. |
| WQ `parameter_name`, `unit`; IV implicit parameter units | Use a reviewed per-parameter compatibility map backed by parameter-code/series metadata. Observed `degC` versus legacy `deg C`; do not copy labels blindly or assume a unit-label difference implies a value conversion. |
| WQ `state_code`, `county_code`, `state`, `huc_code` | Preserve legacy conventions per field/transport. Old JSON sample has state `24`, county `24031`; new location has county `031`. Keep routing state abbreviations distinct from numeric state codes. |

### Hard blocker: time-series identity

Old RDB exposes numeric TS_IDs such as `69928`; new continuous data uses opaque
IDs such as `66a4e3fb8abe42fcb0942b5c0fe98f68`. The reviewed new metadata fields
do not expose the legacy numeric TS_ID. Legacy WaterML method IDs are another
candidate crosswalk input, not a proven universal identity guarantee.

USGS confirmed that no direct crosswalk exists. Build and validate scoped
enrollment during overlap using site, agency, parameter, units, computation, sublocation/method,
and matching observation windows. Site+parameter alone is insufficient:
multiple sensor/method series can coexist. Persist provenance and ambiguity
status with every mapping; keep these adapter records outside the event payload.

Cutover requires 100% mapping of the active series in the configured deployment
scope, with zero ambiguous mappings. Also settle how genuinely new series receive
compatible identifiers after shutdown. Do not fabricate numeric IDs, hash opaque
IDs, silently drop unmapped series, or call opaque-ID substitution schema stability.
The accepted policy sends genuinely new or ambiguous series through the native
feeder. Unchanged legacy key semantics are supported only for verified enrolled
series; full legacy coverage is not promised.

### Hard blocker: expanded site semantics

Direct or candidate renamed fields from the new location endpoint:

| Legacy fields | New properties |
|---|---|
| `station_nm`, `site_tp_cd` | `monitoring_location_name`, `site_type_code` |
| `district_cd`, `state_cd`, `county_cd`, `country_cd` | `district_code`, `state_code`, `county_code`, `country_code` |
| `coord_meth_cd`, `coord_acy_cd`, `coord_datum_cd` | `horizontal_position_method_code`, `horizontal_positional_accuracy_code`, `original_horizontal_datum` |
| `alt_va`, `alt_meth_cd`, `alt_acy_va`, `alt_datum_cd` | `altitude`, `altitude_method_code`, `altitude_accuracy`, `vertical_datum`; verify units and changed values |
| `huc_cd`, `basin_cd` | `hydrologic_unit_code`, `basin_code`; preserve code width and null/empty conventions |
| `drain_area_va`, `contrib_drain_area_va` | `drainage_area`, `contributing_drainage_area`; verify units |
| `tz_cd`, `local_time_fg` | `time_zone_abbreviation`, `uses_daylight_savings`; explicitly translate flag values |
| `construction_dt` | `construction_date`; verify legacy date string representation |
| `nat_aqfr_cd`, `aqfr_cd`, `aqfr_type_cd` | `national_aquifer_code`, `aquifer_code`, `aquifer_type_code` |
| `well_depth_va`, `hole_depth_va`, `depth_src_cd` | `well_constructed_depth`, `hole_constructed_depth`, `depth_source_code` |

The reviewed location endpoint does not expose direct equivalents for `lat_va`,
`long_va`, `land_net_ds`, `map_nm`, `map_scale_fc`, `topo_cd`, `instruments_cd`,
`inventory_dt`, `reliability_cd`, `gw_file_cd`, or `project_no`.
GeoJSON geometry can supply decimal coordinates, but `dec_lat_va`,
`dec_long_va` and `dec_coord_datum_cd` must stay mutually consistent.
The new API documents transformed WGS84 geometry and the *original* horizontal
datum separately. Do not label transformed coordinates with the original datum
or manufacture original DMS coordinates by reformatting transformed geometry.

The migration guide marks these missing fields as no longer provided; USGS
referred to that disposition in both replies. Capture an expanded legacy
snapshot while available, keyed by agency/site, if a supplement is needed. A snapshot only
preserves historical values: specify refresh, age reporting, treatment of new
sites and conflict resolution. Required strings cannot silently become empty
just to pass validation; unknown booleans cannot silently become false.
Document any accepted reduction in metadata fidelity as a maintainer decision.

## Acquisition and state design

1. Keep generated transport producers as they are. Add/reuse a small handwritten
   OGC fetch/normalization boundary per feeder; route WQ Kafka/AMQP/MQTT through
   the same acquisition semantics without merging their outward contracts.
2. Discover locations and instantaneous series; cache location, parameter and
   legacy-ID metadata. Emit existing reference events before measurements.
   Do not add new reference event types in this migration.
3. Translate `stateCd=DE` to `state_code=10`, `sites=01646500` to
   `monitoring_location_id=USGS-01646500`, and `parameterCd` to `parameter_code`.
   Current OpenAPI supports comma-separated site, parameter and series filters.
   Preserve existing CLI/env names and explicit-site precedence.
4. WQ `period=PT2H` is an observation-time window. IV `modifiedSince=PT2H`
   is an update-time filter: evaluate `last_modified`, not just `time`.
   Establish fixed UTC query bounds and overlap at cycle start, test late
   arrivals/corrections, and never rely on duration parsing in `datetime`.
   `time=PT2H` was verified; other combinations still need fixtures/probes.
5. Follow the returned `links[rel=next].href` until exhausted. Check expected
   HTTPS host/path before forwarding credentials. Do not construct cursor
   tokens, assume one page is complete, or infer sorting from response order.
   Choose bounded state/site/time slices and measure full-cycle duration.
6. Reuse an HTTP session, bound concurrency and retries, honor 429/Retry-After,
   and isolate failures by slice. Retain the last valid metadata snapshot after
   refresh failure. Reject malformed records explicitly with actionable logs.
7. Support an optional API key via a proposed `USGS_API_KEY` environment variable
   and `X-Api-Key` header, never URL/log output. Existing anonymous probes worked;
   nationwide request volume must be measured against the actual response
   rate-limit headers. [API key guidance][keys] does not guarantee a single
   universal rate quota.
8. Track observation identity internally by upstream series ID + observation
   instant, not the feature UUID: USGS documents that UUID as unstable on refresh.
   Separate poll watermarks from measurement timestamps; define whether corrected
   measurements at an existing time are re-emitted without changing payload shape.
   Hash normalized content if needed to distinguish a correction from a database
   refresh that only changed `last_modified`.
9. Preserve existing state files via an explicit, versioned migration and backup.
   IV currently keys watermarks by parameter-name/site, WQ Kafka by site/parameter,
   WQ AMQP by site/parameter/time. They cannot be blindly treated as equivalent to
   per-series state. Commit state only after successful transport delivery.
10. Resolve multiple WQ series for the same site/parameter without adding a field
    or selecting an arbitrary first result. Baseline the actual legacy behavior,
    retain all intended observations internally, and obtain a decision if the
    existing payload cannot distinguish required series.

## Work ledger

Owners below are proposed roles, not assignments already accepted.
`Done` means the listed evidence exists; it does not mean the migration shipped.
`Blocked` identifies an unresolved cutover gate; investigation can continue.

| ID | Status | Proposed owner | Depends on | Work and completion evidence |
|---|---|---|---|---|
| USGS-01 | Done | Implementer | None | Repository API inventory, transport-path inspection, manifest field/key inventory and initial live probes recorded above. |
| USGS-02 | Pending | Operator + implementer | USGS-01 | Inventory actual ACI/notebook deployments, images, transport modes, configured states/sites/parameters, state paths and downstream source/key dependencies. Output an explicit rollout scope. |
| USGS-03 | In progress | Implementer | USGS-01 | Capture CLI implemented and exercised live for site 01646500, parameters 00010/00060; captures expanded sites, IV JSON/RDB, OGC continuous data and series metadata. Remaining: every configured family, multi-method ambiguity, groundwater, no-data/status and DST/territory coverage. |
| USGS-04 | Scoped policy accepted; production coverage pending | Implementer + operator | USGS-02, USGS-03 | USGS confirms no direct crosswalk. Verified enrollment only; new/ambiguous series use native output. Archive legacy evidence before shutdown. Production legacy scope still requires complete, unambiguous enrollment; no further USGS mapping service is assumed. |
| USGS-05 | Scoped policy accepted; production fidelity pending | Implementer + operator; maintainer for fidelity decisions | USGS-03 | Discontinued fields use explicitly historical supplements for enrolled sites; unknown qualifiers fail legacy projection. Do not invent current metadata or accept fidelity loss implicitly. Coordinate and field parity remain per-enrollment checks. |
| USGS-06 | Done | Implementer | USGS-03 | Shared core and installed legacy integration implemented: retries, fixed windows, safe pagination, cached references, state-code resolution, slice isolation, atomic snapshots and post-delivery checkpoints. Focused failure/correction tests pass. |
| USGS-07 | Done for enrolled scope | Implementer | USGS-04, USGS-05, USGS-06 | IV OGC poller/site commands and separate series-reference producer wired. Strict Kafka/MQTT/Artemis/Service Bus tests received site, series, streamflow and temperature events. AMQP partition identity equals subject for every family. Broader production enrollment remains blocked by USGS-04/05. |
| USGS-08 | Done for enrolled scope | Implementer | USGS-05, USGS-06 | WQ OGC normalization on all transports; real legacy polling is the MQTT default. Strict Kafka, MQTT, Artemis and Service Bus tests passed for site and reading events; the Artemis compatibility entry point also passed. |
| USGS-09 | Done | Implementer | USGS-07, USGS-08 | Delivery-acknowledged state, versioned state preservation, replay/correction and rejection tests implemented. Failed sends/flushes do not advance checkpoints. Broker acceptance still requires USGS-10. |
| USGS-10 | Local checks done; cloud blocked | Implementer | USGS-09 | 271 frozen artifacts unchanged; 201 offline source tests, 49 shared regressions, nine final image builds and 1,331-file fleet mypy passed. All 13 distinct strict transport cases passed across focused runs, without mocks/skips/xfails. USGS-17/18 block cloud acceptance. |
| USGS-11 | Pending | Operator + implementer | USGS-02, USGS-10 | Run legacy/new shadow comparison with isolated topics/state, over 24 hours and a reference refresh; compare matched observation sets and report all differences by field/reason. No unexplained omissions, identity changes or numeric/unit changes. |
| USGS-12 | Done | Implementer | USGS-10 | Native and transitional deployment/API docs, root catalog/portal entry, upstream links, matrix and notebook wheel publication integration updated. Historical CE source and frozen legacy EVENTS/contracts retained. |
| USGS-13 | Pending | Operator + maintainer | USGS-11, USGS-12 | Rebuild/publish images and notebook wheels; canary one scoped deployment per hosting/transport surface, then roll out serially. Capture deployed versions, observed records, lag and rollback checkpoint per deployment. |
| USGS-14 | Pending | Operator | USGS-13 | Verify scheduled notebook diagnostics and typed KQL tables, then monitor freshness/delivery/429s for 48 hours. Confirm no production acquisition traffic to legacy WaterServices and retain the compatibility crosswalk/supplement. |
| USGS-15 | Local acceptance done; release blocked | Implementer | USGS-01 | Native continuous-only implementation, generated contracts/producers, packaging and independent specialist reviews complete. Final Kafka/MQTT/Artemis/Service Bus run passed all four cases. USGS-17/18 block release. |
| USGS-16 | Done for reviewed sample | Implementer | USGS-03 | Verified enrollment for site 01646500 and parameters 00010/00060, captured expanded-site metadata, explicit units/qualifiers, guarded projection and deterministic vendored-core wheels integrated. Broader enrollment remains an operator coverage gate, not inferred from this sample. |
| USGS-17 | Blocked | Maintainer + implementer | USGS-10, USGS-15 | Choose and implement policy-compatible persistent state hosting for ACI. All six native ARM-engine validations hit the existing deny-shared-key policy. Do not waive policy or discard state; rerun live deployment acceptance after approval. |
| USGS-18 | Blocked | Maintainer + implementer | USGS-10, USGS-15 | Resolve Environment-backed Spark hosting and supported publishing identity for Fabric; obtain approval before any access-key fallback. Then verify fresh notebook output, typed KQL history and a scheduled run. |
| USGS-19 | Pending upstream fixes | Upstream maintainers + implementer | USGS-06, USGS-15 | Track the four linked generator defects. Retire handwritten boundaries only after fixed generation and strict on-wire/schema regression tests; preserve the legacy contract freeze. |

### Implemented compatibility boundary

The [capture CLI](usgs-waterdata/usgs_waterdata_core/usgs_waterdata_core/capture.py)
does not guess numeric IDs from opaque native IDs. It records numeric RDB
identities separately from WaterML method candidates. It requires at least
three matching observation instants and no mismatched shared instants to report
a candidate. Candidates remain unverified even when only one matches.

The [compatibility projection](usgs-waterdata/usgs_waterdata_core/usgs_waterdata_core/compat.py)
requires explicit verification attribution/time and a captured RDB identity.
It rejects conflicting identities, unreviewed units, unknown qualifiers,
missing historical metadata and unrepresentable WQ values. Unit aliases are
reviewed label changes, not implicit numeric conversions. Snapshot capture time
is logged when historical site metadata is used. This does not yet establish
complete field parity or policy for all exceptional values.

The [delivery checkpoint](usgs-waterdata/usgs_waterdata_core/usgs_waterdata_core/state.py)
commits only after the send/flush callbacks succeed and Kafka reports no
remaining messages. A later-page failure leaves the checkpoint unchanged.
Re-emission after a failed partial delivery is intentional at-least-once
behavior. Broker acknowledgements still require transport-specific callbacks;
this module alone is not delivery proof.

The core is distributed as a deterministic, digest-verified wheel in each
legacy source's vendor directory. All six legacy Docker contexts remain
self-contained; no unpublished PyPI dependency or copied client implementation
is required. CI import installation, local notebook wheel builds and the wheel
publication workflow include and verify that wheel. Clean wheel installs were
tested. Rebuild vendor wheels after changing the shared core.

Developer capture example from the worktree root (choose a new output file;
existing evidence files are not overwritten):

```powershell
$env:PYTHONPATH = "$PWD\feeders\usgs-waterdata\usgs_waterdata_core"
python -m usgs_waterdata_core.capture `
  --sites 01646500 --parameter-codes 00010,00060 `
  --start 2026-11-16T13:25:42Z --end 2026-11-16T15:25:42Z `
  --output C:\rts-evidence\usgs-01646500.json
```

`USGS_API_KEY`, when provided, is sent only in the OGC request header.
Legacy evidence requests explicitly remove that header. The capture contains
public upstream records, query bounds and capture time, not credentials.
The successful capture from this session is retained outside the repository in
the session's persistent `files` directory as `usgs-01646500-capture.json`.

Questions were sent November 17; USGS support replied November 17 and Mike
replied November 18. The accepted constraints above replace waiting for a
crosswalk or replacement fields. Complete qualifier mappings, original-coordinate
availability and correction/withdrawal synchronization remain unconfirmed.
They are documented limitations, not guarantees inferred from the replies.

## Reviews and tracked generator defects

The final native contract received GO verdicts from the UNS Catalog Architect,
xRegistry Expert, JSON Structure Expert, independent Avro reviewer, upstream
API re-auditor and KQL Optimizer. No named Avro agent profile was available,
so a separate general-purpose agent performed that specialist role after the
earlier combined JSON Structure/Avro review. Its Apache Avro 1.12.1 probes
passed four rooted contracts, 118-field required/nullability/description
parity, eight binary round trips and 24 generated-model JSON round trips.
The reviewed native manifest SHA-256 is
`4b93e092d5663c2d12df2e1df1bba809b19495ea4b771754f089af99cc9ef9d3`.

The KQL review covers all four typed tables, dispatch projections/mappings,
update policies and three reference Latest views. Duration text remains a
string, not a Kusto timespan. The reviewed script SHA-256 is
`DB30DF02765F858BA06E434538B0377807D6154387D59C4FB19D088B468F8349`.

Four upstream defects remain open. Generated artifacts were not patched:

| Issue | Defect | Handwritten boundary treatment |
|---|---|---|
| [xregistry/codegen#698](https://github.com/xregistry/codegen/issues/698) | Optional absent nonnullable fields serialize as null. | Typed serialization boundaries omit absent optional fields; strict schema validation remains enabled. |
| [xregistry/codegen#699](https://github.com/xregistry/codegen/issues/699) | Generic AMQP password mode uses pre-settled delivery and ignores TLS selection. | Acknowledged sender boundary selects at-least-once settlement and the requested TLS scheme; rejection retains checkpoints. Explicit SASL PLAIN configuration and plugin packaging correct generic-broker negotiation. |
| [clemensv/avrotize#572](https://github.com/clemensv/avrotize/issues/572) | Generated duration fields lack an ISO 8601 JSON encoder. | A shallow serialization copy retains original duration text; the typed model keeps its parsed duration. |
| [xregistry/codegen#700](https://github.com/xregistry/codegen/issues/700) | Generated MQTT callback ownership and acknowledgement handling break connection/PUBACK tracking. | Handwritten WQ boundary restores callbacks and requires successful PUBACK; enqueue errors, rejected acknowledgements and missing acknowledgements retain checkpoints. |

Follow-up: remove each boundary only after the corresponding upstream fix is
released, producers are regenerated in an authorized contract-preserving
change, and strict schema/on-wire tests pass again. An issue being closed is
not evidence that the generator installed here contains its fix.

The final IV AMQP boundary supplies a symbolic `x-opt-partition-key` equal to
the CloudEvent subject on both password and CBS paths. Missing or overlength
identities fail rather than being truncated. Historical generated behavior
is documented in [xregistry/codegen#294](https://github.com/xregistry/codegen/issues/294).
The native CBS failure was a separate local configuration bug: the boundary
had not forwarded `AMQP_USE_TLS`. That override now works; Entra mode still
rejects TLS disablement. No generated CBS defect is claimed for this failure.

Native JSON preserves RFC 3339 spelling, including seven fractional digits,
offsets and boundary years. Parser input is normalized only where Python 3.10
requires it; emitted text is retained. The Avro datetime representation is
string-backed with custom logical type `rfc3339-timestamp-millis`, not a
standard long-backed timestamp. All shipped transport paths emit JSON.

## Validation and release gates

Last completed local results:

| Gate | Result |
|---|---|
| Native unit suite | 63 passed |
| IV offline unit/integration suite | 58 passed; eight live legacy-API tests tracked separately |
| WQ offline unit/integration suite | 80 passed; two live legacy-API tests tracked separately |
| Live legacy-API checks | Initial all-tests runs had one HTTP timeout each: IV 58/59 passed, WQ 81/82 passed. Both unchanged failing tests passed on their first separate live retry. No mocks, skips or timeout-as-success changes were added. |
| Shared strict harness/matrix/schema-compatibility tests | 49 passed |
| Producer-aware fleet mypy | Passed, 1,331 source files |
| Docker builds and in-image imports | All nine final variants built; all three native builds used `--no-cache` |
| Legacy contract freeze | 271 manifest/generated/KQL artifacts byte-identical to baseline |
| ARM static validation | Native 6, IV 7, WQ 5 templates; zero blockers/warnings |
| Notebook static validation | 11 checks passed per source; zero blockers/warnings |
| Publication integration | YAML parses; both legacy bundles include the verified core wheel |
| Real Kafka flows | Native, IV and WQ passed with required reference and telemetry families |
| Real MQTT flows | Native, IV and WQ passed with required reference and telemetry families |
| Real AMQP flows | Native, IV and WQ passed Artemis and Service Bus emulator; WQ Artemis compatibility entry point passed |
| Installed import smoke | IV and WQ each passed all three runtime imports in an isolated validation environment |
| Compile/import plans | All three sources passed; generated and handwritten Python compiled |
| Cloud preflight | Approved Fabric workspace accessible with assigned capacity; no existing USGS items. No feeder deployed. |
| Azure ARM-engine validation | All six native templates blocked by the existing deny-shared-key policy; temporary validation resource group removed |

Final transport coverage:

| Feeder | Kafka | MQTT | AMQP/Artemis | AMQP/Service Bus emulator |
|---|---|---|---|---|
| Native Water Data | Pass | Pass | Pass | Pass |
| Transitional IV | Pass | Pass | Pass | Pass |
| Transitional WQ | Pass | Pass | Pass, including compatibility entry point | Pass |

The first 13-case run passed all six Kafka/MQTT cases and exposed AMQP
schema-resolver and native TLS-override failures. A five-case legacy AMQP
retry passed all three WQ cases and exposed missing IV partition identity.
After those corrections, the final native four-case run and IV two-case run
passed. The failed attempts remain recorded; they are not reported as passing
suite invocations. Pytest also reports an existing unregistered `docker_e2e`
marker warning; no warnings or errors were used as delivery proof.

Cloud acceptance is not waived. The shared notebook deployer forces the Python
kernel and removes Environment binding; the Environment-backed hosting path
requires Spark bindings. Its legacy connection-string path also needs an
explicitly approved access-key fallback if workspace-identity publishing is
unavailable. The current static validator passing does not settle either
runtime question. No access keys were retrieved and no shared Fabric items
were modified. Resolve the hosting/authentication path before running cloud
acceptance; do not silently change a shared deployment or enable key auth.

Azure returned `RequestDisallowedByPolicy` for all six native templates.
The policy, "Deny storage accounts that allow Shared Key", requires
`allowSharedKeyAccess=false`; the templates use account-key-backed Azure Files
for persistent state. Merely adding that property does not establish a working,
policy-compatible mount. Do not request an exemption, bypass the policy,
remove dedupe persistence or silently switch authentication. Release requires
an approved state-storage/hosting design and then successful live acceptance.

All commands below run from the migration worktree. The package mirror uses
verified HTTPS without credentials; no TLS verification was disabled.
`DOCKER_BUILDKIT=1` explicitly selects the Docker CLI builder with the same
staged context. It avoids this machine's observed legacy SDK-builder
containerd lease/content-store failures without restarting or pruning the
shared Docker daemon.

```powershell
$env:PIP_INDEX_URL = 'https://packagefeedproxy.microsoft.io/pypi/simple/'
$env:DOCKER_BUILDKIT = '1'
# Import-smoke: full install/import gate on a supported environment.
python tools\ci\import_smoke.py feeders\usgs-iv
python tools\ci\import_smoke.py feeders\usgs-nwis-wq
# Windows compile-only diagnostic; not a substitute for in-image import proof.
python tools\ci\import_smoke.py feeders\usgs-iv --plan
python tools\ci\import_smoke.py feeders\usgs-nwis-wq --plan

Push-Location feeders\usgs-iv
python -m pytest tests\ -m "not e2e" -x --no-header -q
python -m pytest tests\ -m e2e -x --no-header -q
Pop-Location
Push-Location feeders\usgs-nwis-wq
python -m pytest tests\ -m "not e2e" -x --no-header -q
python -m pytest tests\ -m e2e -x --no-header -q
Pop-Location

# Run with CI-equivalent producer MYPYPATH.
python -m mypy feeders --config-file mypy.ini --exclude /build/

docker build -f feeders\usgs-iv\Dockerfile feeders\usgs-iv --no-cache -q
docker build -f feeders\usgs-iv\Dockerfile.mqtt feeders\usgs-iv --no-cache -q
docker build -f feeders\usgs-iv\Dockerfile.amqp feeders\usgs-iv --no-cache -q
docker build -f feeders\usgs-nwis-wq\Dockerfile feeders\usgs-nwis-wq --no-cache -q
docker build -f feeders\usgs-nwis-wq\Dockerfile.mqtt feeders\usgs-nwis-wq --no-cache -q
docker build -f feeders\usgs-nwis-wq\Dockerfile.amqp feeders\usgs-nwis-wq --no-cache -q

python -m pytest tests\docker_e2e\test_docker_kafka_flow.py::TestUSGSIVDockerFlow tests\docker_e2e\test_docker_kafka_flow.py::TestUSGSNWISWQDockerFlow -x -v
```

Final executed check commands and results (`python` denotes the isolated
validation interpreter; broker captures remain outside the repository):

| Command | Result |
|---|---|
| `python -m pytest tests -m "not e2e" -q --no-header`, separately in each source directory | Native 63 passed; IV 58 passed; WQ 80 passed. |
| `python -m pytest tests\docker_e2e\test_helpers.py tests\docker_e2e\test_discover_matrix.py tests\docker_e2e\test_jsonstructure_compat.py -q` | 49 passed. |
| `python -m mypy feeders --config-file mypy.ini --exclude /build/`, with producer-aware `MYPYPATH` | Passed: 1,331 source files. Clear this mypy-only variable before running environment-mocking tests on Windows; restoring an inherited value longer than 32,767 characters fails in `os.environ`. |
| `python tools\ci\import_smoke.py feeders\usgs-iv` and `python tools\ci\import_smoke.py feeders\usgs-nwis-wq` | Passed: three installed runtime imports per feeder. |
| `python tools\ci\import_smoke.py feeders\<source> --plan`, for all three sources | Passed: complete source trees compiled; install/import deliberately skipped by this diagnostic flag. Final images additionally passed in-image imports. |
| `python -m pytest tests\docker_e2e\test_docker_kafka_flow.py tests\docker_e2e\test_docker_mqtt_flow.py tests\docker_e2e\test_docker_amqp_flow.py tests\docker_e2e\test_docker_amqp_sb_emulator_flow.py -k USGSWaterData -v --kafka-artifacts-dir=<external-capture-directory>` | Final native run: four passed in 383.56 seconds. |
| `python -m pytest tests\docker_e2e\test_docker_amqp_flow.py tests\docker_e2e\test_docker_amqp_sb_emulator_flow.py -k USGSIV -v` | Final IV AMQP run: two passed in 394.95 seconds. |
| `python -m pytest tests\docker_e2e\test_docker_amqp_flow.py tests\docker_e2e\test_docker_amqp_sb_emulator_flow.py tests\docker_e2e\test_docker_amqp_artemis_flow.py -k "(USGSIV or UsgsNwisWq) and not WaterData" -v` | Three WQ cases passed; two IV cases failed before the partition fix and passed in the final IV command above. |
| `pwsh -NoProfile -File tools\validate-arm-templates.ps1 -FeederSlug <source>`, separately for all three sources | 18 templates passed; zero blockers/warnings. |
| `pwsh -NoProfile -File tools\validate-fabric-deployment.ps1 -FeederSlug <source>`, separately for all three sources | 33 checks passed; zero blockers/warnings. This is static validation, not cloud acceptance. |

Also compile every Python file in each changed source tree, including generated
files, before committing. Keep Docker build-time import-smoke instructions intact.
Update focused tests for the new parser rather than only changing old URL
assertions. A skipped/xfailed/live-empty test is not a passing migration gate.

Required tests/evidence beyond these commands:

- Byte-identical xRegistry manifests and generated producer/schema artifacts;
  unchanged KQL contracts. Validate serialized events against the frozen manifests.
- Fixed-window parity for all configured parameters, reference records, keys,
  source/type/subject, values, exception/status fields, qualifiers, units and
  observation instants. Account for metadata precision and textual timestamp
  differences explicitly; do not silently allow arbitrary differences.
- Pagination across multiple pages, unsorted rows, late arrivals, repeated rows,
  corrections, unknown/multiple series, no-data, missing metadata, 429/5xx/timeouts,
  cached-catalog survival and partial-slice failure.
- Delivery failure must leave pending observations eligible after restart;
  failed metadata refresh must not replace a good cache. Bound reference batches
  and flush timeouts according to the runtime checklist.
- Real upstream site/reference and telemetry events on **Kafka, MQTT and AMQP for
  each feeder**. Inspect consumed messages, not just container logs. Add WQ MQTT
  live-flow coverage; remove mock/xfail-based success from the acceptance path.
  IV must additionally emit `USGS.Sites.SiteTimeseries`.
- Notebook wheel installation/import and one scheduled run per feeder, with
  OneLake logs, preserved state, fresh Eventstream output and typed KQL rows.
- Record exact commands, results, deployment IDs and observation timestamps in
  the eventual PR/release evidence. Store deployment identities, endpoints,
  captures and receipts outside the repository.

Production inventory, coverage enrollment, the 24-hour shadow comparison,
canaries and 48-hour rollout monitoring remain separate operator work. None
of these is implied by a local unit test or by the reviewed sample enrollment.

Contract/expert-review trigger: an acquisition-only implementation with unchanged
contracts does not need schema regeneration. If a blocker demands a contract
change, stop the schema-stable track, obtain authorization, then run the
repository's xRegistry, JSON Structure, Avro and KQL reviews as applicable.
Do not disguise that change as an adapter refactor.

Rollback: retain the previous image/wheels and a state-file backup; isolate the
canary from production topics. Before shutdown, rollback to the old API is only
a temporary option subject to its degradation/outages. After shutdown, rollback
must use a known-good OGC implementation; the legacy URL is not a recovery plan.

## Executed preparation checks

Run in `C:\git\rts-usgs-waterdata`:

| Command/check | Result |
|---|---|
| `python -m pytest feeders\usgs-waterdata\tests -q` | Passed: 32 tests. |
| `python -m mypy feeders\usgs-waterdata\usgs_waterdata_core\usgs_waterdata_core --follow-imports=silent` | Passed: five source files. This is a focused check, not the fleet-wide CI gate. |
| `python -m mypy feeders --config-file mypy.ini --exclude /build/`, with generated producer `src` directories on `MYPYPATH` | Passed: 1,309 source files. |
| `python -m compileall -q feeders\usgs-waterdata` | Passed. |
| Import `usgs_waterdata_core`, `capture`, `compat`, `state` with the core directory on `PYTHONPATH` | Passed; imports do not start a polling loop. |
| `python -m pip wheel --no-deps .\feeders\usgs-waterdata\usgs_waterdata_core --wheel-dir <session-files>\usgs-wheels` | Passed; built `usgs_waterdata_core-1.9.1.post3-py3-none-any.whl`. Wheel and build dependency isolation are not a container test. |
| Install that wheel using `PIP_USER=false` and `python -m pip install --no-deps --target <session-files>\usgs-wheel-check <wheel>`; import all four modules and run `python -m usgs_waterdata_core.capture --help` | Passed from the isolated install, without a global package install. Verified the wheel contains five Python modules and no interpreter caches. |
| Live capture command above, with the recorded UTC bounds and a session-local output path | Passed: one site, 34 observations, two unverified candidates; no mappings auto-approved. |

## Current result

Implemented in the isolated worktree: native continuous-data contracts and
three transport apps, shared acquisition/capture/compatibility core, opt-in
transitional acquisition in both legacy feeders, packaging, notebook assets,
KQL, documentation and catalog integration. Legacy runtimes changed; their
271 contract/generated/KQL artifacts did not. Native specialist reviews
returned GO, including the independent Avro review recorded above.

Kafka, MQTT and AMQP delivery are verified for all three feeders. National identity/metadata coverage, deployed
cloud acceptance, production shadow comparison and cutover are not established
by the reviewed sample. Azure policy and Fabric hosting/authentication block
release. No migration commit, PR, image release or production deployment has
been made.

[shutdown]: https://waterservices.usgs.gov/
[schedule]: https://waterdata.usgs.gov/blog/wdfn-waterservices-degradation/
[continuous]: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous
[series]: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata
[locations]: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations
[daily]: https://api.waterdata.usgs.gov/ogcapi/v1/collections/daily
[statistics]: https://api.waterdata.usgs.gov/statistics/v0/docs
[openapi]: https://api.waterdata.usgs.gov/ogcapi/v1/openapi?f=json
[keys]: https://api.waterdata.usgs.gov/docs/ogcapi/keys/
[migration]: https://api.waterdata.usgs.gov/docs/ogcapi/migration/
