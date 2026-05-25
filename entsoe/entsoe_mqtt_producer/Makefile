.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./entsoe_mqtt_producer_data ./entsoe_mqtt_producer_mqtt_client

install: build
	cd entsoe_mqtt_producer_data && poetry install
	cd entsoe_mqtt_producer_mqtt_client && poetry install
	pip install ./entsoe_mqtt_producer_data ./entsoe_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./entsoe_mqtt_producer_mqtt_client/tests ./entsoe_mqtt_producer_data/tests