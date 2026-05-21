.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./pegelonline_mqtt_producer_data ./pegelonline_mqtt_producer_mqtt_client

install: build
	cd pegelonline_mqtt_producer_data && poetry install
	cd pegelonline_mqtt_producer_mqtt_client && poetry install
	pip install ./pegelonline_mqtt_producer_data ./pegelonline_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./pegelonline_mqtt_producer_mqtt_client/tests ./pegelonline_mqtt_producer_data/tests