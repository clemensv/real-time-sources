
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-vehicleposition.avsc --message-type VehiclePosition --namespace GeneralTransitFeed.VehiclePosition
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-tripupdate.avsc --message-type TripUpdate --namespace GeneralTransitFeed.TripUpdate
avrotize p2a xreg\gtfs-rt.proto --out xreg\gtfs-rt-alert.avsc --message-type Alert --namespace GeneralTransitFeed.Alert
del .\xreg\gtfs.xreg.json
xregistry manifest init xreg\gtfs.xreg.json

xregistry manifest schemaversion add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.VehiclePosition" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-rt-vehicleposition.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.VehiclePosition" --schemaformat Avro --schemagroup "GeneralTransitFeed.RealTime" --schemaid "GeneralTransitFeed.RealTime.VehiclePosition" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.VehiclePosition" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.VehiclePosition" --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json

xregistry manifest schemaversion add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.TripUpdate" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-rt-tripupdate.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.TripUpdate" --schemaformat Avro --schemagroup "GeneralTransitFeed.RealTime" --schemaid "GeneralTransitFeed.RealTime.TripUpdate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.TripUpdate" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.TripUpdate" --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json

xregistry manifest schemaversion add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.Alert" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-rt-alert.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.Alert" --schemaformat Avro --schemagroup "GeneralTransitFeed.RealTime" --schemaid "GeneralTransitFeed.RealTime.Alert" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.Alert" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeed.RealTime" --id "GeneralTransitFeed.RealTime.Alert" --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json


function CloudEventsSourceSubject ($messageid) {
    xregistry manifest cloudevent metadata edit --groupid "GeneralTransitFeed.Static" --id $messageid --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\gtfs.xreg.json
    xregistry manifest cloudevent metadata add --groupid "GeneralTransitFeed.Static" --id $messageid --attribute subject --description "Provider name" --value "{agencyid}" --type "uritemplate" xreg\gtfs.xreg.json
}

# Agency
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Agency" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Agency.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Agency" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Agency" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Agency"

# Areas
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Areas" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Areas.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Areas" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Areas" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Areas"

# Attributions
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Attributions" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Attributions.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Attributions" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Attributions" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Attributions"

# BookingRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.BookingRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\BookingRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.BookingRules" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.BookingRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.BookingRules"


# FareAttributes
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareAttributes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareAttributes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareAttributes" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FareAttributes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FareAttributes"

# FareLegRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareLegRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareLegRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareLegRules" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FareLegRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FareLegRules"

# FareMedia
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareMedia" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareMedia.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareMedia" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FareMedia" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FareMedia"

# FareProducts
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareProducts" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareProducts.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareProducts" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FareProducts" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FareProducts"

# FareRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareRules" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FareRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FareRules"

# FareTransferRules
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareTransferRules" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FareTransferRules.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FareTransferRules" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FareTransferRules" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FareTransferRules"

# FeedInfo
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FeedInfo" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\FeedInfo.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.FeedInfo" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.FeedInfo" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.FeedInfo"

# Frequencies
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Frequencies" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Frequencies.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Frequencies" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Frequencies" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Frequencies"

# Levels
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Levels" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Levels.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Levels" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Levels" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Levels"

# LocationGeoJson
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.LocationGeoJson" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\LocationGeoJson.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.LocationGeoJson" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.LocationGeoJson" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.LocationGeoJson"

# LocationGroups
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.LocationGroups" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\LocationGroups.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.LocationGroups" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.LocationGroups" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.LocationGroups"

# LocationGroupStores
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.LocationGroupStores" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\LocationGroupStores.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.LocationGroupStores" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.LocationGroupStores" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.LocationGroupStores"

# Networks
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Networks" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Networks.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Networks" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Networks" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Networks"

# Pathways
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Pathways" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Pathways.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Pathways" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Pathways" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Pathways"

# RouteNetworks
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.RouteNetworks" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\RouteNetworks.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.RouteNetworks" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.RouteNetworks" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.RouteNetworks"

# Routes
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Routes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Routes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Routes" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Routes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Routes"

# Shapes
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Shapes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Shapes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Shapes" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Shapes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Shapes"

# StopAreas
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.StopAreas" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\StopAreas.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.StopAreas" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.StopAreas" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.StopAreas"

# Stops
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Stops" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Stops.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Stops" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Stops" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Stops"

# StopTimes
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.StopTimes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\StopTimes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.StopTimes" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.StopTimes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.StopTimes"

# Timeframes
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Timeframes" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Timeframes.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Timeframes" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Timeframes" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Timeframes"

# Transfers
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Transfers" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Transfers.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Transfers" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Transfers" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Transfers"

# Translations
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Translations" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Translations.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Translations" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Translations" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Translations"

# Trips
xregistry manifest schemaversion add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Trips" --versionid "1" --format "Avro" --schemaimport xreg\gtfs-static\Trips.avsc xreg\gtfs.xreg.json
xregistry manifest cloudevent add --groupid "GeneralTransitFeed.Static" --id "GeneralTransitFeed.Static.Trips" --schemaformat Avro --schemagroup "GeneralTransitFeed.Static" --schemaid "GeneralTransitFeed.Static.Trips" xreg\gtfs.xreg.json
CloudEventsSourceSubject "GeneralTransitFeed.Static.Trips"


xregistry generate --style kafkaproducer --language py --definitions xreg\gtfs.xreg.json --projectname gtfs_rt_producer --output gtfs_rt_producer