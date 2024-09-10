del .\xreg\pegelonline.xreg.json
xregistry manifest init xreg\pegelonline.xreg.json

xregistry manifest schemaversion add --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.Station" --versionid "1" --format "Avro" --schemaimport xreg\Station.avsc xreg\pegelonline.xreg.json
xregistry manifest cloudevent add --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.Station" --schemaformat Avro --schemagroup "de.wsv.pegelonline" --schemaid "de.wsv.pegelonline.Station" xreg\pegelonline.xreg.json
xregistry manifest cloudevent metadata edit --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.Station" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\pegelonline.xreg.json
xregistry manifest cloudevent metadata add --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.Station" --attribute subject --description "Station" --value "{station_id}" --type "uritemplate" xreg\pegelonline.xreg.json

xregistry manifest schemaversion add --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.CurrentMeasurement" --versionid "1" --format "Avro" --schemaimport xreg\CurrentMeasurement.avsc xreg\pegelonline.xreg.json
xregistry manifest cloudevent add --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.CurrentMeasurement" --schemaformat Avro --schemagroup "de.wsv.pegelonline" --schemaid "de.wsv.pegelonline.CurrentMeasurement" xreg\pegelonline.xreg.json
xregistry manifest cloudevent metadata edit --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.CurrentMeasurement" --attribute source --description "Source Feed URL" --value "{feedurl}" --type "uritemplate" xreg\pegelonline.xreg.json
xregistry manifest cloudevent metadata add --groupid "de.wsv.pegelonline" --id "de.wsv.pegelonline.CurrentMeasurement" --attribute subject --description "Station" --value "{station_id}" --type "uritemplate" xreg\pegelonline.xreg.json

xregistry generate --style kafkaproducer --language py --definitions xreg\pegelonline.xreg.json --projectname pegelonline_producer --output pegelonline_producer