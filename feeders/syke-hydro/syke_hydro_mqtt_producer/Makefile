.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./syke_hydro_mqtt_producer_data ./syke_hydro_mqtt_producer_mqtt_client

install: build
	cd syke_hydro_mqtt_producer_data && poetry install
	cd syke_hydro_mqtt_producer_mqtt_client && poetry install
	pip install ./syke_hydro_mqtt_producer_data ./syke_hydro_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./syke_hydro_mqtt_producer_mqtt_client/tests ./syke_hydro_mqtt_producer_data/tests