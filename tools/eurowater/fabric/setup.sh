#!/bin/bash
# Sets up the Eurowater Fabric Event Stream and KQL database.
#
# Usage:
#   ./setup.sh <workspace-name> [eventhouse-name] [database-name] [eventstream-name]
#
# Prerequisites:
#   - Microsoft Fabric CLI (fab) installed
#   - Authenticated: fab login

set -euo pipefail

WORKSPACE="${1:?Usage: $0 <workspace-name> [eventhouse-name] [database-name] [eventstream-name]}"
EVENTHOUSE="${2:-eurowater}"
DATABASE="${3:-eurowater}"
EVENTSTREAM="${4:-eurowater-ingest}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Eurowater Fabric Setup ==="

# ---------------------------------------------------------------------------
# 1. KQL Eventhouse and Database
# ---------------------------------------------------------------------------
echo "[1/5] Creating KQL Eventhouse '$EVENTHOUSE'..."
fab eventhouse create --workspace "$WORKSPACE" --name "$EVENTHOUSE" 2>/dev/null || \
    echo "  Eventhouse may already exist, continuing..."

echo "[2/5] Creating KQL Database '$DATABASE'..."
fab kqldatabase create --workspace "$WORKSPACE" --eventhouse "$EVENTHOUSE" --name "$DATABASE" 2>/dev/null || \
    echo "  Database may already exist, continuing..."

echo "  Applying KQL schema..."
KQL_SCRIPT=$(cat "$SCRIPT_DIR/kql_database.kql")
fab kqldatabase execute \
    --workspace "$WORKSPACE" \
    --eventhouse "$EVENTHOUSE" \
    --database "$DATABASE" \
    --script "$KQL_SCRIPT"

# ---------------------------------------------------------------------------
# 2. Event Stream
# ---------------------------------------------------------------------------
echo "[3/5] Creating Event Stream '$EVENTSTREAM'..."
fab eventstream create --workspace "$WORKSPACE" --name "$EVENTSTREAM" 2>/dev/null || \
    echo "  Event Stream may already exist, continuing..."

# ---------------------------------------------------------------------------
# 3. Custom Input
# ---------------------------------------------------------------------------
echo "[4/5] Adding custom input endpoint..."
INPUT_RESULT=$(fab eventstream add-source \
    --workspace "$WORKSPACE" \
    --eventstream "$EVENTSTREAM" \
    --source-type "custom-endpoint" \
    --name "eurowater-input" \
    --format "json")

CONNECTION_STRING=$(echo "$INPUT_RESULT" | jq -r '.connectionString // empty')
if [ -n "$CONNECTION_STRING" ]; then
    echo "  Connection String: $CONNECTION_STRING"
else
    echo "  Custom input created. Retrieve the connection string from the Fabric portal."
fi

# ---------------------------------------------------------------------------
# 4. SQL Operator
# ---------------------------------------------------------------------------
echo "[5/5] Adding SQL normalization operator..."

STATIONS_SQL=$(cat "$SCRIPT_DIR/normalize_stations.sql")
MEASUREMENTS_SQL=$(cat "$SCRIPT_DIR/normalize_measurements.sql")

COMBINED_SQL="$STATIONS_SQL

$MEASUREMENTS_SQL"

fab eventstream add-operator \
    --workspace "$WORKSPACE" \
    --eventstream "$EVENTSTREAM" \
    --operator-type "sql" \
    --name "normalize" \
    --input "eurowater-input" \
    --query "$COMBINED_SQL"

# ---------------------------------------------------------------------------
# 5. KQL Database destinations
# ---------------------------------------------------------------------------
echo "  Adding Stations KQL destination..."
fab eventstream add-destination \
    --workspace "$WORKSPACE" \
    --eventstream "$EVENTSTREAM" \
    --destination-type "kql-database" \
    --name "stations-kql" \
    --input "normalize" \
    --output-name "StationOutput" \
    --eventhouse "$EVENTHOUSE" \
    --database "$DATABASE" \
    --table "Stations" \
    --mapping "StationsMapping" \
    --format "json"

echo "  Adding Measurements KQL destination..."
fab eventstream add-destination \
    --workspace "$WORKSPACE" \
    --eventstream "$EVENTSTREAM" \
    --destination-type "kql-database" \
    --name "measurements-kql" \
    --input "normalize" \
    --output-name "MeasurementOutput" \
    --eventhouse "$EVENTHOUSE" \
    --database "$DATABASE" \
    --table "Measurements" \
    --mapping "MeasurementsMapping" \
    --format "json"

# ---------------------------------------------------------------------------
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Resources in workspace '$WORKSPACE':"
echo "  Eventhouse:   $EVENTHOUSE"
echo "  KQL Database: $DATABASE (tables: Stations, Measurements)"
echo "  Event Stream: $EVENTSTREAM"
echo ""
echo "Next: deploy the container group with the connection string above."
