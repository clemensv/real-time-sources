.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nepal_bipad_hydrology_mqtt_producer_data ./nepal_bipad_hydrology_mqtt_producer_mqtt_client

install: build
	cd nepal_bipad_hydrology_mqtt_producer_data && poetry install
	cd nepal_bipad_hydrology_mqtt_producer_mqtt_client && poetry install
	pip install ./nepal_bipad_hydrology_mqtt_producer_data ./nepal_bipad_hydrology_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nepal_bipad_hydrology_mqtt_producer_mqtt_client/tests ./nepal_bipad_hydrology_mqtt_producer_data/tests