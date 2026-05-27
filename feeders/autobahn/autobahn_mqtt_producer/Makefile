.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./autobahn_mqtt_producer_data ./autobahn_mqtt_producer_mqtt_client

install: build
	cd autobahn_mqtt_producer_data && poetry install
	cd autobahn_mqtt_producer_mqtt_client && poetry install
	pip install ./autobahn_mqtt_producer_data ./autobahn_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./autobahn_mqtt_producer_mqtt_client/tests ./autobahn_mqtt_producer_data/tests