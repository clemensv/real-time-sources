.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./aviationweather_mqtt_producer_data ./aviationweather_mqtt_producer_mqtt_client

install: build
	cd aviationweather_mqtt_producer_data && poetry install
	cd aviationweather_mqtt_producer_mqtt_client && poetry install
	pip install ./aviationweather_mqtt_producer_data ./aviationweather_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./aviationweather_mqtt_producer_mqtt_client/tests ./aviationweather_mqtt_producer_data/tests