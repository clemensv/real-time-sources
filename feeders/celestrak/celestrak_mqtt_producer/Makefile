.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./celestrak_mqtt_producer_data ./celestrak_mqtt_producer_mqtt_client

install: build
	cd celestrak_mqtt_producer_data && poetry install
	cd celestrak_mqtt_producer_mqtt_client && poetry install
	pip install ./celestrak_mqtt_producer_data ./celestrak_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./celestrak_mqtt_producer_mqtt_client/tests ./celestrak_mqtt_producer_data/tests