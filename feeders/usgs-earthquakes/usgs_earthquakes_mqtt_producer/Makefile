.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./usgs_earthquakes_mqtt_producer_data ./usgs_earthquakes_mqtt_producer_mqtt_client

install: build
	cd usgs_earthquakes_mqtt_producer_data && poetry install
	cd usgs_earthquakes_mqtt_producer_mqtt_client && poetry install
	pip install ./usgs_earthquakes_mqtt_producer_data ./usgs_earthquakes_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./usgs_earthquakes_mqtt_producer_mqtt_client/tests ./usgs_earthquakes_mqtt_producer_data/tests