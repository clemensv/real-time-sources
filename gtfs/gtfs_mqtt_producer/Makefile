.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gtfs_mqtt_producer_data ./gtfs_mqtt_producer_mqtt_client

install: build
	cd gtfs_mqtt_producer_data && poetry install
	cd gtfs_mqtt_producer_mqtt_client && poetry install
	pip install ./gtfs_mqtt_producer_data ./gtfs_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gtfs_mqtt_producer_mqtt_client/tests ./gtfs_mqtt_producer_data/tests