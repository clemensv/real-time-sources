.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./entur_norway_mqtt_producer_data ./entur_norway_mqtt_producer_mqtt_client

install: build
	cd entur_norway_mqtt_producer_data && poetry install
	cd entur_norway_mqtt_producer_mqtt_client && poetry install
	pip install ./entur_norway_mqtt_producer_data ./entur_norway_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./entur_norway_mqtt_producer_mqtt_client/tests ./entur_norway_mqtt_producer_data/tests