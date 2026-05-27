.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./geosphere_austria_mqtt_producer_data ./geosphere_austria_mqtt_producer_mqtt_client

install: build
	cd geosphere_austria_mqtt_producer_data && poetry install
	cd geosphere_austria_mqtt_producer_mqtt_client && poetry install
	pip install ./geosphere_austria_mqtt_producer_data ./geosphere_austria_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./geosphere_austria_mqtt_producer_mqtt_client/tests ./geosphere_austria_mqtt_producer_data/tests