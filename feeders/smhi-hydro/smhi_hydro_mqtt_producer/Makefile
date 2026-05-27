.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./smhi_hydro_mqtt_producer_data ./smhi_hydro_mqtt_producer_mqtt_client

install: build
	cd smhi_hydro_mqtt_producer_data && poetry install
	cd smhi_hydro_mqtt_producer_mqtt_client && poetry install
	pip install ./smhi_hydro_mqtt_producer_data ./smhi_hydro_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./smhi_hydro_mqtt_producer_mqtt_client/tests ./smhi_hydro_mqtt_producer_data/tests