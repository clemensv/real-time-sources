# JMA Japan Weather Bulletins Bridge Events

This document describes the events emitted by the JMA Japan Weather Bulletins Bridge.

- [jp.go.jma.WeatherBulletins](#message-group-jpgojmaweatherbulletins)
  - [jp.go.jma.WeatherBulletin](#message-jpgojmaweatherbulletin)

---

## Message Group: jp.go.jma.WeatherBulletins

---

### Message: jp.go.jma.WeatherBulletin

Weather bulletin entry from the JMA Atom XML feed. Each entry represents a
forecast, warning, advisory, or risk notification published by the Japan
Meteorological Agency or one of its regional observatories.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `jp.go.jma.WeatherBulletin` |
| `source` | CloudEvent source | `string` | `True` | `https://www.data.jma.go.jp` |

#### Schema: WeatherBulletin

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `bulletin_id` | *string* | Stable hash-based identifier derived from the Atom entry ID |
| `title` | *string* | Bulletin title in Japanese (e.g., "気象特別警報・警報・注意報") |
| `author` | *string (nullable)* | Issuing authority name in Japanese (e.g., "気象庁", "松江地方気象台") |
| `updated` | *string (date-time)* | When the bulletin was last updated |
| `link` | *string (nullable)* | URL to the full XML document on the JMA data server |
| `content` | *string (nullable)* | Brief text summary of the bulletin content in Japanese |
| `feed_type` | *string (enum)* | Feed origin: regular, extra |
