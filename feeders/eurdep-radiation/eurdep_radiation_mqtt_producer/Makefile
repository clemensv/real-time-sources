.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./eurdep_radiation_mqtt_producer_data ./eurdep_radiation_mqtt_producer_mqtt_client

install: build
	cd eurdep_radiation_mqtt_producer_data && poetry install
	cd eurdep_radiation_mqtt_producer_mqtt_client && poetry install
	pip install ./eurdep_radiation_mqtt_producer_data ./eurdep_radiation_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./eurdep_radiation_mqtt_producer_mqtt_client/tests ./eurdep_radiation_mqtt_producer_data/tests