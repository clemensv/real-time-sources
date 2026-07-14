.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./taipei_youbike_mqtt_producer_data ./taipei_youbike_mqtt_producer_mqtt_client

install: build
	cd taipei_youbike_mqtt_producer_data && poetry install
	cd taipei_youbike_mqtt_producer_mqtt_client && poetry install
	pip install ./taipei_youbike_mqtt_producer_data ./taipei_youbike_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./taipei_youbike_mqtt_producer_mqtt_client/tests ./taipei_youbike_mqtt_producer_data/tests