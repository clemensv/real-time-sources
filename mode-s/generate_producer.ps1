del .\xreg\mode_s.xreg.json
xregistry manifest init xreg\mode_s.xreg.json

xregistry manifest schemaversion add --groupid "Mode_S" --id "Mode_S.Messages" --versionid "1" --format "Avro" --schemaimport xreg\mode_s_message.avsc xreg\mode_s.xreg.json
xregistry manifest cloudevent add --groupid "Mode_S" --id "Mode_S.Messages" --dataschemaformat Avro --dataschemagroup "Mode_S" --dataschemaid "Mode_S.Messages" xreg\mode_s.xreg.json
xregistry manifest cloudevent metadata edit --groupid "Mode_S" --id "Mode_S.Messages" --attribute source --description "Station Identifier" --value "{stationid}" --type "uritemplate" xreg\mode_s.xreg.json

xregistry generate --style kafkaproducer --language py --definitions xreg\mode_s.xreg.json --projectname mode_s_producer --output mode_s_producer