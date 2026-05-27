.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./noaa_ndbc_mqtt_producer_data ./noaa_ndbc_mqtt_producer_mqtt_client

install: build
	cd noaa_ndbc_mqtt_producer_data && poetry install
	cd noaa_ndbc_mqtt_producer_mqtt_client && poetry install
	pip install ./noaa_ndbc_mqtt_producer_data ./noaa_ndbc_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./noaa_ndbc_mqtt_producer_mqtt_client/tests ./noaa_ndbc_mqtt_producer_data/tests