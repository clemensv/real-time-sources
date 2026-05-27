.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./aisstream_mqtt_producer_data ./aisstream_mqtt_producer_mqtt_client

install: build
	cd aisstream_mqtt_producer_data && poetry install
	cd aisstream_mqtt_producer_mqtt_client && poetry install
	pip install ./aisstream_mqtt_producer_data ./aisstream_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./aisstream_mqtt_producer_mqtt_client/tests ./aisstream_mqtt_producer_data/tests