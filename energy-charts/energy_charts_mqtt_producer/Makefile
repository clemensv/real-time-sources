.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./energy_charts_mqtt_producer_data ./energy_charts_mqtt_producer_mqtt_client

install: build
	cd energy_charts_mqtt_producer_data && poetry install
	cd energy_charts_mqtt_producer_mqtt_client && poetry install
	pip install ./energy_charts_mqtt_producer_data ./energy_charts_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./energy_charts_mqtt_producer_mqtt_client/tests ./energy_charts_mqtt_producer_data/tests