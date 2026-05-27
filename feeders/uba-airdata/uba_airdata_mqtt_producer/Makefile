.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./uba_airdata_mqtt_producer_data ./uba_airdata_mqtt_producer_mqtt_client

install: build
	cd uba_airdata_mqtt_producer_data && poetry install
	cd uba_airdata_mqtt_producer_mqtt_client && poetry install
	pip install ./uba_airdata_mqtt_producer_data ./uba_airdata_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./uba_airdata_mqtt_producer_mqtt_client/tests ./uba_airdata_mqtt_producer_data/tests