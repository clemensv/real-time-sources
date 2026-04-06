. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-vehicleposition.avsc --message-type VehiclePosition --namespace GeneralTransitFeedRealTime.Vehicle
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-tripupdate.avsc --message-type TripUpdate --namespace GeneralTransitFeedRealTime.Trip
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-alert.avsc --message-type Alert --namespace GeneralTransitFeedRealTime.Alert

# The checked-in xreg manifest is authoritative. This script only refreshes
# the derived Avro files above and regenerates the client package from xreg.
xrcg generate --style kafkaproducer --language py --definitions xreg\gtfs.xreg.json --projectname gtfs_rt_producer --output gtfs_rt_producer