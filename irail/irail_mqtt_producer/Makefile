.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./irail_mqtt_producer_data ./irail_mqtt_producer_mqtt_client

install: build
	cd irail_mqtt_producer_data && poetry install
	cd irail_mqtt_producer_mqtt_client && poetry install
	pip install ./irail_mqtt_producer_data ./irail_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./irail_mqtt_producer_mqtt_client/tests ./irail_mqtt_producer_data/tests