.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./kystverket_ais_mqtt_producer_data ./kystverket_ais_mqtt_producer_mqtt_client

install: build
	cd kystverket_ais_mqtt_producer_data && poetry install
	cd kystverket_ais_mqtt_producer_mqtt_client && poetry install
	pip install ./kystverket_ais_mqtt_producer_data ./kystverket_ais_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./kystverket_ais_mqtt_producer_mqtt_client/tests ./kystverket_ais_mqtt_producer_data/tests