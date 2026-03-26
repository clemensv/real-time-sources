# Hub'Eau Hydrométrie API Bridge Events

This document describes the events emitted by the Hub'Eau Hydrométrie API Bridge.

- [FR.Gov.Eaufrance.HubEau.Hydrometrie](#message-group-frgoveaufrancehubieauhydrometrie)
  - [FR.Gov.Eaufrance.HubEau.Hydrometrie.Station](#message-frgoveaufrancehubieauhydrometriestation)
  - [FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation](#message-frgoveaufrancehubieauhydrometrieobservation)

---

## Message Group: FR.Gov.Eaufrance.HubEau.Hydrometrie

---

### Message: FR.Gov.Eaufrance.HubEau.Hydrometrie.Station

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `FR.Gov.Eaufrance.HubEau.Hydrometrie.Station` |
| `source` | Source Feed URL | `string` | `True` | `https://hubeau.eaufrance.fr/api/v2/hydrometrie` |

#### Schema: Station

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `code_station` | *string* | Unique station code (10 characters) |
| `libelle_station` | *string* | Station name/label |
| `code_site` | *string* | Parent site code (8 characters) |
| `longitude_station` | *number* | Longitude in WGS84 |
| `latitude_station` | *number* | Latitude in WGS84 |
| `libelle_cours_eau` | *string* | River/waterway name |
| `libelle_commune` | *string* | Municipality name |
| `code_departement` | *string* | Department code |
| `en_service` | *boolean* | Whether the station is currently active |
| `date_ouverture_station` | *string* | Station opening date in ISO 8601 |

---

### Message: FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `FR.Gov.Eaufrance.HubEau.Hydrometrie.Observation` |
| `source` | Source Feed URL | `string` | `True` | `https://hubeau.eaufrance.fr/api/v2/hydrometrie` |

#### Schema: Observation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `code_station` | *string* | Station code for this observation |
| `date_obs` | *string* | Observation timestamp in ISO 8601 |
| `resultat_obs` | *number* | Observation value (mm for H, L/s for Q) |
| `grandeur_hydro` | *string* | Hydrometric quantity: H (height) or Q (discharge) |
| `libelle_methode_obs` | *string* | Observation method label |
| `libelle_qualification_obs` | *string* | Quality qualification label |
