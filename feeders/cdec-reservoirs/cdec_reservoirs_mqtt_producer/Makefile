.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./cdec_reservoirs_mqtt_producer_data ./cdec_reservoirs_mqtt_producer_mqtt_client

install: build
	cd cdec_reservoirs_mqtt_producer_data && poetry install
	cd cdec_reservoirs_mqtt_producer_mqtt_client && poetry install
	pip install ./cdec_reservoirs_mqtt_producer_data ./cdec_reservoirs_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./cdec_reservoirs_mqtt_producer_mqtt_client/tests ./cdec_reservoirs_mqtt_producer_data/tests