$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\gtfs.xreg.json"
$kqlFile = Join-Path $scriptDir "gtfs.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace GeneralTransitFeed

# Append the hand-authored flat tables and update policies.  Each block is
# written via Add-Content so adjacent commands are guaranteed to be separated
# by a newline; the previous Out-File-Append pattern silently glued
# consecutive @"..."@ here-strings together when the trailing newline was
# elided, producing invalid KQL.
function Append-Kql([string]$Text) {
    Add-Content -Path $kqlFile -Value "`r`n$Text`r`n"
}

Append-Kql @"
.create table ['GeneralTransitFeed.VehiclePositionsFlat'] (
    trip_id:string,
    route_id:string,
    direction_id:int,
    start_time:string,
    start_date:string,
    schedule_relationship:string,
    vehicle_id:string,
    vehicle_label:string,
    vehicle_license_plate:string,
    latitude:real,
    longitude:real,
    bearing:real,
    odometer:real,
    speed:real,
    current_stop_sequence:int,
    stop_id:string,
    current_status:string,
    timestamp:datetime,
    congestion_level:string,
    occupancy_status:string,
    ___type:string,
    ___source:string,
    ___id:string,
    ___time:datetime,
    ___subject:string
)
"@

Append-Kql @"
.alter table ['GeneralTransitFeed.VehiclePositionsFlat'] policy update
``````
[
  {
    "IsEnabled": true,
    "Source": "GeneralTransitFeed.VehiclePosition",
    "Query": "['GeneralTransitFeed.VehiclePosition'] | extend trip_id = tostring(trip.trip_id), route_id = tostring(trip.route_id), direction_id = toint(trip.direction_id), start_time = tostring(trip.start_time), start_date = tostring(trip.start_date), schedule_relationship = tostring(trip.schedule_relationship), vehicle_id = tostring(vehicle.id), vehicle_label = tostring(vehicle.label), vehicle_license_plate = tostring(vehicle.license_plate), latitude = todouble(position.latitude), longitude = todouble(position.longitude), bearing = todouble(position.bearing), odometer = todouble(position.odometer), speed = todouble(position.speed) | extend timestamp = unixtime_seconds_todatetime(timestamp) | project trip_id, route_id, direction_id, start_time, start_date, schedule_relationship, vehicle_id, vehicle_label, vehicle_license_plate, latitude, longitude, bearing, odometer, speed, current_stop_sequence, stop_id, current_status, timestamp, congestion_level, occupancy_status, ___type, ___source, ___id, ___time, ___subject",
    "IsTransactional": true,
    "PropagateIngestionProperties": true
  }
]
``````
"@

Append-Kql @"
.create-merge table ['GeneralTransitFeed.TripUpdateFlattened'] (
    trip_id: string,
    route_id: string,
    direction_id: int,
    trip_start_time: string,
    trip_start_date: string,
    trip_schedule_relationship: string,
    vehicle_id: string,
    vehicle_label: string,
    vehicle_license_plate: string,
    timestamp: long,
    delay: int,
    stop_sequence: int,
    stop_id: string,
    arrival_delay: int,
    arrival_time: datetime,
    arrival_uncertainty: int,
    departure_delay: int,
    departure_time: datetime,
    departure_uncertainty: int,
    stop_schedule_relationship: string,
    ___type: string,
    ___source: string,
    ___id: string,
    ___time: datetime,
    ___subject: string
)
"@

Append-Kql @"
.create-or-alter function with (skipvalidation = "true") TripUpdateFlattenFunction() {
    ['GeneralTransitFeed.TripUpdate']
    | where isnotempty(stop_time_update)
    | mv-expand stop_time_update
    | extend
        stop_sequence = toint(stop_time_update.stop_sequence),
        stop_id = tostring(stop_time_update.stop_id),
        arrival = stop_time_update.arrival,
        departure = stop_time_update.departure,
        stop_schedule_relationship = tostring(stop_time_update.schedule_relationship)
    | extend
        arrival_delay = toint(arrival.delay),
        arrival_time = unixtime_seconds_todatetime(toint(arrival.['time'])),
        arrival_uncertainty = toint(arrival.uncertainty),
        departure_delay = toint(departure.delay),
        departure_time = unixtime_seconds_todatetime(toint(departure.['time'])),
        departure_uncertainty = toint(departure.uncertainty)
    | extend
        trip_id = tostring(trip.trip_id),
        route_id = tostring(trip.route_id),
        direction_id = toint(trip.direction_id),
        trip_start_time = tostring(trip.start_time),
        trip_start_date = tostring(trip.start_date),
        trip_schedule_relationship = tostring(trip.schedule_relationship)
    | extend
        vehicle_id = tostring(vehicle.id),
        vehicle_label = tostring(vehicle.label),
        vehicle_license_plate = tostring(vehicle.license_plate)
    | project
        trip_id,
        route_id,
        direction_id,
        trip_start_time,
        trip_start_date,
        trip_schedule_relationship,
        vehicle_id,
        vehicle_label,
        vehicle_license_plate,
        timestamp,
        delay,
        stop_sequence,
        stop_id,
        arrival_delay,
        arrival_time,
        arrival_uncertainty,
        departure_delay,
        departure_time,
        departure_uncertainty,
        stop_schedule_relationship,
        ___type,
        ___source,
        ___id,
        ___time,
        ___subject
}
"@

Append-Kql @"
.alter table ['GeneralTransitFeed.TripUpdateFlattened'] policy update
``````
[
  {
    "IsEnabled": true,
    "Source": "GeneralTransitFeed.TripUpdate",
    "Query": "TripUpdateFlattenFunction()",
    "IsTransactional": false,
    "PropagateIngestionProperties": false
  }
]
``````
"@