.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./open_charge_map_mqtt_producer_data ./open_charge_map_mqtt_producer_mqtt_client

install: build
	cd open_charge_map_mqtt_producer_data && poetry install
	cd open_charge_map_mqtt_producer_mqtt_client && poetry install
	pip install ./open_charge_map_mqtt_producer_data ./open_charge_map_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./open_charge_map_mqtt_producer_mqtt_client/tests ./open_charge_map_mqtt_producer_data/tests