.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wallonia_issep_mqtt_producer_data ./wallonia_issep_mqtt_producer_mqtt_client

install: build
	cd wallonia_issep_mqtt_producer_data && poetry install
	cd wallonia_issep_mqtt_producer_mqtt_client && poetry install
	pip install ./wallonia_issep_mqtt_producer_data ./wallonia_issep_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wallonia_issep_mqtt_producer_mqtt_client/tests ./wallonia_issep_mqtt_producer_data/tests