.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./openaq_mqtt_producer_data ./openaq_mqtt_producer_mqtt_client

install: build
	cd openaq_mqtt_producer_data && poetry install
	cd openaq_mqtt_producer_mqtt_client && poetry install
	pip install ./openaq_mqtt_producer_data ./openaq_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./openaq_mqtt_producer_mqtt_client/tests ./openaq_mqtt_producer_data/tests