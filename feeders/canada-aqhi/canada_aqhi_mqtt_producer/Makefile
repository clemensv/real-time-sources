.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./canada_aqhi_mqtt_producer_data ./canada_aqhi_mqtt_producer_mqtt_client

install: build
	cd canada_aqhi_mqtt_producer_data && poetry install
	cd canada_aqhi_mqtt_producer_mqtt_client && poetry install
	pip install ./canada_aqhi_mqtt_producer_data ./canada_aqhi_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./canada_aqhi_mqtt_producer_mqtt_client/tests ./canada_aqhi_mqtt_producer_data/tests