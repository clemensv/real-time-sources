.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bom_australia_mqtt_producer_data ./bom_australia_mqtt_producer_mqtt_client

install: build
	cd bom_australia_mqtt_producer_data && poetry install
	cd bom_australia_mqtt_producer_mqtt_client && poetry install
	pip install ./bom_australia_mqtt_producer_data ./bom_australia_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bom_australia_mqtt_producer_mqtt_client/tests ./bom_australia_mqtt_producer_data/tests