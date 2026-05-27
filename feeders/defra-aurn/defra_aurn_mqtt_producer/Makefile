.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./defra_aurn_mqtt_producer_data ./defra_aurn_mqtt_producer_mqtt_client

install: build
	cd defra_aurn_mqtt_producer_data && poetry install
	cd defra_aurn_mqtt_producer_mqtt_client && poetry install
	pip install ./defra_aurn_mqtt_producer_data ./defra_aurn_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./defra_aurn_mqtt_producer_mqtt_client/tests ./defra_aurn_mqtt_producer_data/tests