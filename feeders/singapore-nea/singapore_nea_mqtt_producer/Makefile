.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./singapore_nea_mqtt_producer_data ./singapore_nea_mqtt_producer_mqtt_client

install: build
	cd singapore_nea_mqtt_producer_data && poetry install
	cd singapore_nea_mqtt_producer_mqtt_client && poetry install
	pip install ./singapore_nea_mqtt_producer_data ./singapore_nea_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./singapore_nea_mqtt_producer_mqtt_client/tests ./singapore_nea_mqtt_producer_data/tests