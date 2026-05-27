.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gdacs_mqtt_producer_data ./gdacs_mqtt_producer_mqtt_client

install: build
	cd gdacs_mqtt_producer_data && poetry install
	cd gdacs_mqtt_producer_mqtt_client && poetry install
	pip install ./gdacs_mqtt_producer_data ./gdacs_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gdacs_mqtt_producer_mqtt_client/tests ./gdacs_mqtt_producer_data/tests