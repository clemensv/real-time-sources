.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./sensor_community_mqtt_producer_data ./sensor_community_mqtt_producer_mqtt_client

install: build
	cd sensor_community_mqtt_producer_data && poetry install
	cd sensor_community_mqtt_producer_mqtt_client && poetry install
	pip install ./sensor_community_mqtt_producer_data ./sensor_community_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./sensor_community_mqtt_producer_mqtt_client/tests ./sensor_community_mqtt_producer_data/tests