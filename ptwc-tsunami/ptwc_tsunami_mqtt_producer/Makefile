.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ptwc_tsunami_mqtt_producer_data ./ptwc_tsunami_mqtt_producer_mqtt_client

install: build
	cd ptwc_tsunami_mqtt_producer_data && poetry install
	cd ptwc_tsunami_mqtt_producer_mqtt_client && poetry install
	pip install ./ptwc_tsunami_mqtt_producer_data ./ptwc_tsunami_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ptwc_tsunami_mqtt_producer_mqtt_client/tests ./ptwc_tsunami_mqtt_producer_data/tests