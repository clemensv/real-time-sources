.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./australia_wildfires_mqtt_producer_data ./australia_wildfires_mqtt_producer_mqtt_client

install: build
	cd australia_wildfires_mqtt_producer_data && poetry install
	cd australia_wildfires_mqtt_producer_mqtt_client && poetry install
	pip install ./australia_wildfires_mqtt_producer_data ./australia_wildfires_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./australia_wildfires_mqtt_producer_mqtt_client/tests ./australia_wildfires_mqtt_producer_data/tests