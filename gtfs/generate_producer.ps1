
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-vehicleposition.avsc --message-type VehiclePosition --namespace GeneralTransitFeedRealTime.Vehicle
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-tripupdate.avsc --message-type TripUpdate --namespace GeneralTransitFeedRealTime.Trip
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-alert.avsc --message-type Alert --namespace GeneralTransitFeedRealTime.Alert
del .\xreg\gtfs.xreg.json
xregistry manifest init xreg\gtfs.xreg.json

xregistry manifest schemaversion add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Vehicle.VehiclePosition" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-rt-vehicleposition.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Vehicle.VehiclePosition" --dataschemaformat Avro --schemagroup "GeneralTransitFeedRealTime" --schemaid "GeneralTransitFeedRealTime.Vehicle.VehiclePosition" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Vehicle.VehiclePosition" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Vehicle.VehiclePosition" --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json

xregistry manifest schemaversion add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Trip.TripUpdate" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-rt-tripupdate.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Trip.TripUpdate" --dataschemaformat Avro --schemagroup "GeneralTransitFeedRealTime" --schemaid "GeneralTransitFeedRealTime.Trip.TripUpdate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Trip.TripUpdate" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Trip.TripUpdate" --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json

xregistry manifest schemaversion add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Alert.Alert" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-rt-alert.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Alert.Alert" --dataschemaformat Avro --schemagroup "GeneralTransitFeedRealTime" --schemaid "GeneralTransitFeedRealTime.Alert.Alert" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Alert.Alert" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeedRealTime" --id "GeneralTransitFeedRealTime.Alert.Alert" --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json


function CloudEventsSourceSubject ($messageid) {
    xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeedStatic" --id $messageid --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
    xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeedStatic" --id $messageid --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json
}

# Agency
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Agency" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Agency.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Agency" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Agency" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Agency"

# Areas
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Areas" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Areas.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Areas" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Areas" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Areas"

# Attributions
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Attributions" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Attributions.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Attributions" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Attributions" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Attributions"

# BookingRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeed.BookingRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\BookingRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeed.BookingRules" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeed.BookingRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.BookingRules"


# FareAttributes
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareAttributes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareAttributes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareAttributes" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FareAttributes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FareAttributes"

# FareLegRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareLegRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareLegRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareLegRules" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FareLegRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FareLegRules"

# FareMedia
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareMedia" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareMedia.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareMedia" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FareMedia" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FareMedia"

# FareProducts
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareProducts" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareProducts.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareProducts" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FareProducts" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FareProducts"

# FareRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareRules" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FareRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FareRules"

# FareTransferRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareTransferRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareTransferRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FareTransferRules" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FareTransferRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FareTransferRules"

# FeedInfo
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FeedInfo" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FeedInfo.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.FeedInfo" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.FeedInfo" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.FeedInfo"

# Frequencies
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Frequencies" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Frequencies.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Frequencies" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Frequencies" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Frequencies"

# Levels
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Levels" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Levels.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Levels" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Levels" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Levels"

# LocationGeoJson
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.LocationGeoJson" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\LocationGeoJson.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.LocationGeoJson" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.LocationGeoJson" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.LocationGeoJson"

# LocationGroups
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.LocationGroups" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\LocationGroups.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.LocationGroups" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.LocationGroups" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.LocationGroups"

# LocationGroupStores
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.LocationGroupStores" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\LocationGroupStores.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.LocationGroupStores" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.LocationGroupStores" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.LocationGroupStores"

# Networks
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Networks" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Networks.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Networks" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Networks" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Networks"

# Pathways
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Pathways" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Pathways.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Pathways" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Pathways" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Pathways"

# RouteNetworks
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.RouteNetworks" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\RouteNetworks.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.RouteNetworks" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.RouteNetworks" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.RouteNetworks"

# Routes
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Routes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Routes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Routes" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Routes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Routes"

# Shapes
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Shapes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Shapes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Shapes" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Shapes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Shapes"

# StopAreas
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.StopAreas" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\StopAreas.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.StopAreas" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.StopAreas" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.StopAreas"

# Stops
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Stops" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Stops.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Stops" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Stops" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Stops"

# StopTimes
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.StopTimes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\StopTimes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.StopTimes" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.StopTimes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.StopTimes"

# Timeframes
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Timeframes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Timeframes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Timeframes" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Timeframes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Timeframes"

# Transfers
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Transfers" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Transfers.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Transfers" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Transfers" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Transfers"

# Translations
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Translations" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Translations.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Translations" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Translations" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Translations"

# Trips
xregistry manifest schemaversion add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Trips" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Trips.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeedStatic" --id "GeneralTransitFeedStatic.Trips" --dataschemaformat Avro --schemagroup "GeneralTransitFeedStatic" --schemaid "GeneralTransitFeedStatic.Trips" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeedStatic.Trips"


xregistry generate --style kafkaproducer --language py --definitions xreg\gtfs.xreg.json --projectname gtfs_rt_producer --output gtfs_rt_producer