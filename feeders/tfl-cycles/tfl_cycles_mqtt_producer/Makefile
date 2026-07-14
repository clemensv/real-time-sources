.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./tfl_cycles_mqtt_producer_data ./tfl_cycles_mqtt_producer_mqtt_client

install: build
	cd tfl_cycles_mqtt_producer_data && poetry install
	cd tfl_cycles_mqtt_producer_mqtt_client && poetry install
	pip install ./tfl_cycles_mqtt_producer_data ./tfl_cycles_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./tfl_cycles_mqtt_producer_mqtt_client/tests ./tfl_cycles_mqtt_producer_data/tests