.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nve_hydro_mqtt_producer_data ./nve_hydro_mqtt_producer_mqtt_client

install: build
	cd nve_hydro_mqtt_producer_data && poetry install
	cd nve_hydro_mqtt_producer_mqtt_client && poetry install
	pip install ./nve_hydro_mqtt_producer_data ./nve_hydro_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nve_hydro_mqtt_producer_mqtt_client/tests ./nve_hydro_mqtt_producer_data/tests