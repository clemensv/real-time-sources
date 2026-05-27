.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./chmi_hydro_mqtt_producer_data ./chmi_hydro_mqtt_producer_mqtt_client

install: build
	cd chmi_hydro_mqtt_producer_data && poetry install
	cd chmi_hydro_mqtt_producer_mqtt_client && poetry install
	pip install ./chmi_hydro_mqtt_producer_data ./chmi_hydro_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./chmi_hydro_mqtt_producer_mqtt_client/tests ./chmi_hydro_mqtt_producer_data/tests