.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./imgw_hydro_mqtt_producer_data ./imgw_hydro_mqtt_producer_mqtt_client

install: build
	cd imgw_hydro_mqtt_producer_data && poetry install
	cd imgw_hydro_mqtt_producer_mqtt_client && poetry install
	pip install ./imgw_hydro_mqtt_producer_data ./imgw_hydro_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./imgw_hydro_mqtt_producer_mqtt_client/tests ./imgw_hydro_mqtt_producer_data/tests