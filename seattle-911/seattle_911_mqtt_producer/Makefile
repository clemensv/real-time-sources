.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./seattle_911_mqtt_producer_data ./seattle_911_mqtt_producer_mqtt_client

install: build
	cd seattle_911_mqtt_producer_data && poetry install
	cd seattle_911_mqtt_producer_mqtt_client && poetry install
	pip install ./seattle_911_mqtt_producer_data ./seattle_911_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./seattle_911_mqtt_producer_mqtt_client/tests ./seattle_911_mqtt_producer_data/tests