.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./billetto_mqtt_producer_data ./billetto_mqtt_producer_mqtt_client

install: build
	cd billetto_mqtt_producer_data && poetry install
	cd billetto_mqtt_producer_mqtt_client && poetry install
	pip install ./billetto_mqtt_producer_data ./billetto_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./billetto_mqtt_producer_mqtt_client/tests ./billetto_mqtt_producer_data/tests