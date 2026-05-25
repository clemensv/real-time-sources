.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nextbus_mqtt_producer_data ./nextbus_mqtt_producer_mqtt_client

install: build
	cd nextbus_mqtt_producer_data && poetry install
	cd nextbus_mqtt_producer_mqtt_client && poetry install
	pip install ./nextbus_mqtt_producer_data ./nextbus_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nextbus_mqtt_producer_mqtt_client/tests ./nextbus_mqtt_producer_data/tests