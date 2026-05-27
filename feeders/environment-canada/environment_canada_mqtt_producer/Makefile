.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./environment_canada_mqtt_producer_data ./environment_canada_mqtt_producer_mqtt_client

install: build
	cd environment_canada_mqtt_producer_data && poetry install
	cd environment_canada_mqtt_producer_mqtt_client && poetry install
	pip install ./environment_canada_mqtt_producer_data ./environment_canada_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./environment_canada_mqtt_producer_mqtt_client/tests ./environment_canada_mqtt_producer_data/tests