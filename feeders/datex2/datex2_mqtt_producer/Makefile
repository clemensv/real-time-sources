.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./datex2_mqtt_producer_data ./datex2_mqtt_producer_mqtt_client

install: build
	cd datex2_mqtt_producer_data && poetry install
	cd datex2_mqtt_producer_mqtt_client && poetry install
	pip install ./datex2_mqtt_producer_data ./datex2_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./datex2_mqtt_producer_mqtt_client/tests ./datex2_mqtt_producer_data/tests