.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nifc_usa_wildfires_mqtt_producer_data ./nifc_usa_wildfires_mqtt_producer_mqtt_client

install: build
	cd nifc_usa_wildfires_mqtt_producer_data && poetry install
	cd nifc_usa_wildfires_mqtt_producer_mqtt_client && poetry install
	pip install ./nifc_usa_wildfires_mqtt_producer_data ./nifc_usa_wildfires_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nifc_usa_wildfires_mqtt_producer_mqtt_client/tests ./nifc_usa_wildfires_mqtt_producer_data/tests