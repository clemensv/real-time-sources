#!/bin/bash
# Sets up the Digitraffic Maritime Fabric Event Stream and KQL database using the Fabric REST API.
#
# Usage:
#   ./setup.sh <workspace-id> <eventhouse-id> [database-name] [eventstream-name]
#
# Prerequisites:
#   - Azure CLI (az) installed and authenticated: az login
#   - jq installed
#   - Permissions to create items in the Fabric workspace

set -euo pipefail

WORKSPACE_ID="${1:?Usage: $0 <workspace-id> <eventhouse-id> [database-name] [eventstream-name]}"
EVENTHOUSE_ID="${2:?Usage: $0 <workspace-id> <eventhouse-id> [database-name] [eventstream-name]}"
DATABASE="${3:-digitraffic-maritime}"
EVENTSTREAM="${4:-digitraffic-maritime-ingest}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FABRIC_API="https://api.fabric.microsoft.com/v1"
STREAM_NAME="${EVENTSTREAM}-stream"

fabric_api() {
    local method="$1" url="$2"
    shift 2
    local args=(rest --method "$method" --url "$url" --resource "https://api.fabric.microsoft.com")
    if [ $# -gt 0 ]; then
        args+=(--body "$1" --headers "Content-Type=application/json")
    fi
    az "${args[@]}" 2>&1
}

echo "=== Digitraffic Maritime Fabric Setup ==="

# Verify workspace
echo ""
echo "Verifying workspace..."
WORKSPACE_NAME=$(fabric_api GET "$FABRIC_API/workspaces/$WORKSPACE_ID" | jq -r '.displayName')
echo "  Workspace: $WORKSPACE_NAME"

# Verify eventhouse
echo "Verifying eventhouse..."
EH_JSON=$(fabric_api GET "$FABRIC_API/workspaces/$WORKSPACE_ID/eventhouses/$EVENTHOUSE_ID")
EH_NAME=$(echo "$EH_JSON" | jq -r '.displayName')
QUERY_URI=$(echo "$EH_JSON" | jq -r '.properties.queryServiceUri')
echo "  Eventhouse: $EH_NAME"

# ---------------------------------------------------------------------------
# 1. Create KQL Database
# ---------------------------------------------------------------------------
echo ""
echo "[1/3] Creating KQL Database '$DATABASE'..."

DB_LIST=$(fabric_api GET "$FABRIC_API/workspaces/$WORKSPACE_ID/kqlDatabases")
DATABASE_ID=$(echo "$DB_LIST" | jq -r ".value[] | select(.displayName==\"$DATABASE\") | .id")

if [ -n "$DATABASE_ID" ]; then
    echo "  Database already exists (ID: $DATABASE_ID)"
else
    BODY=$(jq -n --arg name "$DATABASE" --arg ehId "$EVENTHOUSE_ID" \
        '{displayName: $name, creationPayload: {databaseType: "ReadWrite", parentEventhouseItemId: $ehId}}')
    TMPFILE=$(mktemp)
    echo "$BODY" > "$TMPFILE"
    fabric_api POST "$FABRIC_API/workspaces/$WORKSPACE_ID/kqlDatabases" "@$TMPFILE" > /dev/null || true
    rm -f "$TMPFILE"
    sleep 5
    DB_LIST=$(fabric_api GET "$FABRIC_API/workspaces/$WORKSPACE_ID/kqlDatabases")
    DATABASE_ID=$(echo "$DB_LIST" | jq -r ".value[] | select(.displayName==\"$DATABASE\") | .id")
    echo "  Database created (ID: $DATABASE_ID)"
fi

# Apply KQL schema
echo "  Applying KQL schema..."
KQL_SCRIPT=$(grep -v '^\s*//' "$SCRIPT_DIR/kql_database.kql")
BODY=$(jq -n --arg csl ".execute database script <|
$KQL_SCRIPT" --arg db "$DATABASE" '{csl: $csl, db: $db}')
TMPFILE=$(mktemp)
echo "$BODY" > "$TMPFILE"
RESULT=$(az rest --method POST --url "$QUERY_URI/v1/rest/mgmt" --resource "$QUERY_URI" --body "@$TMPFILE" --headers "Content-Type=application/json" 2>&1)
rm -f "$TMPFILE"
COMPLETED=$(echo "$RESULT" | jq '[.Tables[0].Rows[] | select(.[3]=="Completed")] | length')
FAILED=$(echo "$RESULT" | jq '[.Tables[0].Rows[] | select(.[3]!="Completed")] | length')
echo "  Schema applied: $COMPLETED commands completed, $FAILED failed"

# ---------------------------------------------------------------------------
# 2. Create Event Stream
# ---------------------------------------------------------------------------
echo ""
echo "[2/3] Creating Event Stream '$EVENTSTREAM'..."

ES_LIST=$(fabric_api GET "$FABRIC_API/workspaces/$WORKSPACE_ID/eventstreams")
EVENTSTREAM_ID=$(echo "$ES_LIST" | jq -r ".value[] | select(.displayName==\"$EVENTSTREAM\") | .id")

if [ -n "$EVENTSTREAM_ID" ]; then
    echo "  Event Stream already exists (ID: $EVENTSTREAM_ID)"
else
    BODY=$(jq -n --arg name "$EVENTSTREAM" '{displayName: $name}')
    TMPFILE=$(mktemp)
    echo "$BODY" > "$TMPFILE"
    fabric_api POST "$FABRIC_API/workspaces/$WORKSPACE_ID/eventstreams" "@$TMPFILE" > /dev/null || true
    rm -f "$TMPFILE"
    sleep 5
    ES_LIST=$(fabric_api GET "$FABRIC_API/workspaces/$WORKSPACE_ID/eventstreams")
    EVENTSTREAM_ID=$(echo "$ES_LIST" | jq -r ".value[] | select(.displayName==\"$EVENTSTREAM\") | .id")
    echo "  Event Stream created (ID: $EVENTSTREAM_ID)"
fi

# ---------------------------------------------------------------------------
# 3. Build and apply Event Stream definition
# ---------------------------------------------------------------------------
echo ""
echo "[3/3] Configuring Event Stream topology..."

ES_DEF=$(jq -n \
    --arg wsId "$WORKSPACE_ID" \
    --arg dbId "$DATABASE_ID" \
    --arg dbName "$DATABASE" \
    --arg streamName "$STREAM_NAME" \
    '{
        sources: [{name: "ais-input", type: "CustomEndpoint", properties: {}}],
        destinations: [{
            name: "dispatch-kql",
            type: "Eventhouse",
            properties: {
                dataIngestionMode: "ProcessedIngestion",
                workspaceId: $wsId,
                itemId: $dbId,
                databaseName: $dbName,
                tableName: "_cloudevents_dispatch",
                inputSerialization: {type: "Json", properties: {encoding: "UTF8"}},
                mappingRuleName: "_cloudevents_dispatch_json"
            },
            inputNodes: [{name: $streamName}]
        }],
        streams: [{
            name: $streamName,
            type: "DefaultStream",
            properties: {},
            inputNodes: [{name: "ais-input"}]
        }],
        operators: [],
        compatibilityLevel: "1.1"
    }')

ES_BASE64=$(echo "$ES_DEF" | base64 -w 0)

UPDATE_BODY=$(jq -n --arg payload "$ES_BASE64" '{
    definition: {
        parts: [{
            path: "eventstream.json",
            payload: $payload,
            payloadType: "InlineBase64"
        }]
    }
}')

TMPFILE=$(mktemp)
echo "$UPDATE_BODY" > "$TMPFILE"
az rest --method POST \
    --url "$FABRIC_API/workspaces/$WORKSPACE_ID/eventstreams/$EVENTSTREAM_ID/updateDefinition" \
    --resource "https://api.fabric.microsoft.com" \
    --body "@$TMPFILE" \
    --headers "Content-Type=application/json" 2>&1
rm -f "$TMPFILE"

echo "  Topology configured:"
echo "    Source:      ais-input (Custom Endpoint)"
echo "    Destination: dispatch-kql -> $DATABASE._cloudevents_dispatch"
echo "    Routing:     KQL update policies -> 2 typed AIS tables"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Resources in workspace '$WORKSPACE_NAME':"
echo "  - Eventhouse:   $EH_NAME ($EVENTHOUSE_ID)"
echo "  - KQL Database: $DATABASE ($DATABASE_ID)"
echo "  - Event Stream: $EVENTSTREAM ($EVENTSTREAM_ID)"
echo ""
echo "Tables:"
echo "  - _cloudevents_dispatch  (ingestion target)"
echo "  - VesselLocation         (positions — ~35 msg/s)"
echo "  - VesselMetadata         (static/voyage data)"
echo ""
echo "Materialized views: VesselLocationLatest, VesselMetadataLatest"
echo ""
echo "Functions: VesselPositions(), AISStatistics(), VesselTrack()"
echo ""
echo "Next steps:"
echo "  1. Open the Event Stream in the Fabric portal to get the Custom Endpoint connection string"
echo "  2. Deploy: docker run -e CONNECTION_STRING='<cs>' ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest"
echo "  3. Or run locally: CONNECTION_STRING='<cs>' python -m digitraffic_maritime stream"
echo ""
