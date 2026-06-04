.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./siri_mqtt_producer_data ./siri_mqtt_producer_mqtt_client

install: build
	cd siri_mqtt_producer_data && poetry install
	cd siri_mqtt_producer_mqtt_client && poetry install
	pip install ./siri_mqtt_producer_data ./siri_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./siri_mqtt_producer_mqtt_client/tests ./siri_mqtt_producer_data/tests