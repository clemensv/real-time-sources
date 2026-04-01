# The checked-in xreg manifest is authoritative. Regenerate the client from it.
xrcg generate --style kafkaproducer --language py --definitions xreg\german_waters.xreg.json --projectname german_waters_producer --output german_waters_producer
