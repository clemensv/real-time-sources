.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fienta_mqtt_producer_data ./fienta_mqtt_producer_mqtt_client

install: build
	cd fienta_mqtt_producer_data && poetry install
	cd fienta_mqtt_producer_mqtt_client && poetry install
	pip install ./fienta_mqtt_producer_data ./fienta_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fienta_mqtt_producer_mqtt_client/tests ./fienta_mqtt_producer_data/tests