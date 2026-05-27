.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./nina_bbk_mqtt_producer_data ./nina_bbk_mqtt_producer_mqtt_client

install: build
	cd nina_bbk_mqtt_producer_data && poetry install
	cd nina_bbk_mqtt_producer_mqtt_client && poetry install
	pip install ./nina_bbk_mqtt_producer_data ./nina_bbk_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./nina_bbk_mqtt_producer_mqtt_client/tests ./nina_bbk_mqtt_producer_data/tests