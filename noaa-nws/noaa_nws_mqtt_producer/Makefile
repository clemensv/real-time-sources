.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa_nws_mqtt_producer_data ./noaa_nws_mqtt_producer_mqtt_client

install: build
	cd noaa_nws_mqtt_producer_data && poetry install
	cd noaa_nws_mqtt_producer_mqtt_client && poetry install
	pip install ./noaa_nws_mqtt_producer_data ./noaa_nws_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa_nws_mqtt_producer_mqtt_client/tests ./noaa_nws_mqtt_producer_data/tests