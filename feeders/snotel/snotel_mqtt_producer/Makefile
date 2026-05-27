.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./snotel_mqtt_producer_data ./snotel_mqtt_producer_mqtt_client

install: build
	cd snotel_mqtt_producer_data && poetry install
	cd snotel_mqtt_producer_mqtt_client && poetry install
	pip install ./snotel_mqtt_producer_data ./snotel_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./snotel_mqtt_producer_mqtt_client/tests ./snotel_mqtt_producer_data/tests