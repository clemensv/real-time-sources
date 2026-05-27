.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gios_poland_mqtt_producer_data ./gios_poland_mqtt_producer_mqtt_client

install: build
	cd gios_poland_mqtt_producer_data && poetry install
	cd gios_poland_mqtt_producer_mqtt_client && poetry install
	pip install ./gios_poland_mqtt_producer_data ./gios_poland_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gios_poland_mqtt_producer_mqtt_client/tests ./gios_poland_mqtt_producer_data/tests