.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./blitzortung_mqtt_producer_data ./blitzortung_mqtt_producer_mqtt_client

install: build
	cd blitzortung_mqtt_producer_data && poetry install
	cd blitzortung_mqtt_producer_mqtt_client && poetry install
	pip install ./blitzortung_mqtt_producer_data ./blitzortung_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./blitzortung_mqtt_producer_mqtt_client/tests ./blitzortung_mqtt_producer_data/tests