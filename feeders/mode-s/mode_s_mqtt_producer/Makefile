.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./mode_s_mqtt_producer_data ./mode_s_mqtt_producer_mqtt_client

install: build
	cd mode_s_mqtt_producer_data && poetry install
	cd mode_s_mqtt_producer_mqtt_client && poetry install
	pip install ./mode_s_mqtt_producer_data ./mode_s_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./mode_s_mqtt_producer_mqtt_client/tests ./mode_s_mqtt_producer_data/tests