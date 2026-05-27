.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./madrid_traffic_mqtt_producer_data ./madrid_traffic_mqtt_producer_mqtt_client

install: build
	cd madrid_traffic_mqtt_producer_data && poetry install
	cd madrid_traffic_mqtt_producer_mqtt_client && poetry install
	pip install ./madrid_traffic_mqtt_producer_data ./madrid_traffic_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./madrid_traffic_mqtt_producer_mqtt_client/tests ./madrid_traffic_mqtt_producer_data/tests