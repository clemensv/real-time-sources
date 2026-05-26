.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./dwd_pollenflug_mqtt_producer_data ./dwd_pollenflug_mqtt_producer_mqtt_client

install: build
	cd dwd_pollenflug_mqtt_producer_data && poetry install
	cd dwd_pollenflug_mqtt_producer_mqtt_client && poetry install
	pip install ./dwd_pollenflug_mqtt_producer_data ./dwd_pollenflug_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./dwd_pollenflug_mqtt_producer_mqtt_client/tests ./dwd_pollenflug_mqtt_producer_data/tests