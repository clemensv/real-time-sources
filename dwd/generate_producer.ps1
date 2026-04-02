# The checked-in xreg manifest is authoritative. Regenerate the client from it.
xrcg generate --style kafkaproducer --language py --definitions xreg\dwd.xreg.json --projectname dwd_producer --output dwd_producer
