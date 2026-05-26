.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./laqn_london_mqtt_producer_data ./laqn_london_mqtt_producer_mqtt_client

install: build
	cd laqn_london_mqtt_producer_data && poetry install
	cd laqn_london_mqtt_producer_mqtt_client && poetry install
	pip install ./laqn_london_mqtt_producer_data ./laqn_london_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./laqn_london_mqtt_producer_mqtt_client/tests ./laqn_london_mqtt_producer_data/tests