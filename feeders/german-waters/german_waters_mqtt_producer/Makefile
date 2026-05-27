.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./german_waters_mqtt_producer_data ./german_waters_mqtt_producer_mqtt_client

install: build
	cd german_waters_mqtt_producer_data && poetry install
	cd german_waters_mqtt_producer_mqtt_client && poetry install
	pip install ./german_waters_mqtt_producer_data ./german_waters_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./german_waters_mqtt_producer_mqtt_client/tests ./german_waters_mqtt_producer_data/tests