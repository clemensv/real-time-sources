$scriptPath = Split-Path -Parent $PSCommandPath
$jsonFiles = Get-ChildItem -Path "$scriptPath/../xreg/gtfs-static" -Filter "*.avsc" | Select-Object -ExpandProperty FullName
$gtfsRtFiles = Get-ChildItem -Path "$scriptPath/../xreg/" -Filter "gtfs-rt-*.avsc" | Select-Object -ExpandProperty FullName
$jsonFiles += $gtfsRtFiles
$outputFile = ".schemas.avsc"

$mergedArray = @()
foreach ($file in $jsonFiles) {
    $jsonContent = Get-Content $file -Raw | ConvertFrom-Json
    $mergedArray += $jsonContent
}
$mergedArray | ConvertTo-Json -Depth 20 | Out-File $outputFile -Encoding UTF8

avrotize a2k $outputFile --emit-cloudevents-dispatch --emit-cloudevents-columns > gtfs.kql
Remove-Item $outputFile

# append the following to gtfs.kql
@"

.create table VehiclePositionsFlat (
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
"@ | Out-File -Append -FilePath gtfs.kql

@"

.alter table VehiclePositionsFlat policy update
```
[
  {
    "IsEnabled": true,
    "Source": "VehiclePosition",
    "Query": "VehiclePosition | extend trip_id = tostring(trip.trip_id), route_id = tostring(trip.route_id), direction_id = toint(trip.direction_id), start_time = tostring(trip.start_time), start_date = tostring(trip.start_date), schedule_relationship = tostring(trip.schedule_relationship), vehicle_id = tostring(vehicle.id), vehicle_label = tostring(vehicle.label), vehicle_license_plate = tostring(vehicle.license_plate), latitude = todouble(position.latitude), longitude = todouble(position.longitude), bearing = todouble(position.bearing), odometer = todouble(position.odometer), speed = todouble(position.speed) | extend timestamp = unixtime_seconds_todatetime(timestamp) | project trip_id, route_id, direction_id, start_time, start_date, schedule_relationship, vehicle_id, vehicle_label, vehicle_license_plate, latitude, longitude, bearing, odometer, speed, current_stop_sequence, stop_id, current_status, timestamp, congestion_level, occupancy_status, ___type, ___source, ___id, ___time, ___subject",
    "IsTransactional": true,
    "PropagateIngestionProperties": true
  }
]
```
"@ | Out-File -Append -FilePath gtfs.kql

@"

.create-merge table TripUpdateFlattened (
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
);
"@ | Out-File -Append -FilePath gtfs.kql

@"

.create-or-alter function with (skipvalidation = "true") TripUpdateFlattenFunction() {
    TripUpdate
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
"@ | Out-File -Append -FilePath gtfs.kql

@"

.alter table TripUpdateFlattened policy update @'[{
    "IsEnabled": true,
    "Source": "TripUpdate",
    "Query": "TripUpdateFlattenFunction()",
    "IsTransactional": false,
    "PropagateIngestionProperties": false
}]'
"@ | Out-File -Append -FilePath gtfs.kql