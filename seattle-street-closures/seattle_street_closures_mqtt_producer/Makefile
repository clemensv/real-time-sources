.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./seattle_street_closures_mqtt_producer_data ./seattle_street_closures_mqtt_producer_mqtt_client

install: build
	cd seattle_street_closures_mqtt_producer_data && poetry install
	cd seattle_street_closures_mqtt_producer_mqtt_client && poetry install
	pip install ./seattle_street_closures_mqtt_producer_data ./seattle_street_closures_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./seattle_street_closures_mqtt_producer_mqtt_client/tests ./seattle_street_closures_mqtt_producer_data/tests