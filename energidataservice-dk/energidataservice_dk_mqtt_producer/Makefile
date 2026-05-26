.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./energidataservice_dk_mqtt_producer_data ./energidataservice_dk_mqtt_producer_mqtt_client

install: build
	cd energidataservice_dk_mqtt_producer_data && poetry install
	cd energidataservice_dk_mqtt_producer_mqtt_client && poetry install
	pip install ./energidataservice_dk_mqtt_producer_data ./energidataservice_dk_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./energidataservice_dk_mqtt_producer_mqtt_client/tests ./energidataservice_dk_mqtt_producer_data/tests