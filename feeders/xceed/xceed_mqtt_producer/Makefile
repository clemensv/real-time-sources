.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./xceed_mqtt_producer_data ./xceed_mqtt_producer_mqtt_client

install: build
	cd xceed_mqtt_producer_data && poetry install
	cd xceed_mqtt_producer_mqtt_client && poetry install
	pip install ./xceed_mqtt_producer_data ./xceed_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./xceed_mqtt_producer_mqtt_client/tests ./xceed_mqtt_producer_data/tests