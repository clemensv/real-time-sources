.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./vatsim_mqtt_producer_data ./vatsim_mqtt_producer_mqtt_client

install: build
	cd vatsim_mqtt_producer_data && poetry install
	cd vatsim_mqtt_producer_mqtt_client && poetry install
	pip install ./vatsim_mqtt_producer_data ./vatsim_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./vatsim_mqtt_producer_mqtt_client/tests ./vatsim_mqtt_producer_data/tests