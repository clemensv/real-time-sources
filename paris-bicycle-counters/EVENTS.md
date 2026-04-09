# Events

This document describes the CloudEvents produced by the Paris Bicycle Counters bridge.

## Event Types

### FR.Paris.OpenData.Velo.Counter

Reference data describing a permanent bicycle counting station in Paris.

- **Type**: `FR.Paris.OpenData.Velo.Counter`
- **Source**: `https://opendata.paris.fr/explore/dataset/comptage-velo-compteurs`
- **Subject**: `{counter_id}`
- **Data Content Type**: `application/json`

#### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `counter_id` | string | Yes | Unique counter channel identifier (from `id_compteur`) |
| `counter_name` | string | Yes | Human-readable counter name (from `nom_compteur`) |
| `channel_name` | string | No | Directional channel label (e.g., "SE-NO") |
| `installation_date` | string | No | Installation date (YYYY-MM-DD) |
| `longitude` | double | No | Longitude in decimal degrees (WGS 84) |
| `latitude` | double | No | Latitude in decimal degrees (WGS 84) |

### FR.Paris.OpenData.Velo.BicycleCount

Hourly bicycle count observation from a permanent counting station.

- **Type**: `FR.Paris.OpenData.Velo.BicycleCount`
- **Source**: `https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs`
- **Subject**: `{counter_id}`
- **Data Content Type**: `application/json`

#### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `counter_id` | string | Yes | Unique counter channel identifier (from `id_compteur`) |
| `counter_name` | string | Yes | Human-readable counter name (from `nom_compteur`) |
| `count` | integer | No | Bicycle count for the hour (from `sum_counts`) |
| `date` | datetime | Yes | Start of the counting window (ISO 8601) |
| `longitude` | double | No | Longitude in decimal degrees (WGS 84) |
| `latitude` | double | No | Latitude in decimal degrees (WGS 84) |

## Kafka Topic

Default topic: `paris-bicycle-counters`

Kafka key: `{counter_id}`

## Envelope

All events use the CloudEvents 1.0 structured content mode with `application/cloudevents+json` format.
