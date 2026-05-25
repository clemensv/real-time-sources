.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ndl_netherlands_mqtt_producer_data ./ndl_netherlands_mqtt_producer_mqtt_client

install: build
	cd ndl_netherlands_mqtt_producer_data && poetry install
	cd ndl_netherlands_mqtt_producer_mqtt_client && poetry install
	pip install ./ndl_netherlands_mqtt_producer_data ./ndl_netherlands_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ndl_netherlands_mqtt_producer_mqtt_client/tests ./ndl_netherlands_mqtt_producer_data/tests