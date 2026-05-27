.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bluesky_mqtt_producer_data ./bluesky_mqtt_producer_mqtt_client

install: build
	cd bluesky_mqtt_producer_data && poetry install
	cd bluesky_mqtt_producer_mqtt_client && poetry install
	pip install ./bluesky_mqtt_producer_data ./bluesky_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bluesky_mqtt_producer_mqtt_client/tests ./bluesky_mqtt_producer_data/tests