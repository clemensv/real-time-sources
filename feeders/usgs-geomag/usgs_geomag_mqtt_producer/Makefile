.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs_geomag_mqtt_producer_data ./usgs_geomag_mqtt_producer_mqtt_client

install: build
	cd usgs_geomag_mqtt_producer_data && poetry install
	cd usgs_geomag_mqtt_producer_mqtt_client && poetry install
	pip install ./usgs_geomag_mqtt_producer_data ./usgs_geomag_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs_geomag_mqtt_producer_mqtt_client/tests ./usgs_geomag_mqtt_producer_data/tests