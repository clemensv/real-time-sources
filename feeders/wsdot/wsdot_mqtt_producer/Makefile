.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./wsdot_mqtt_producer_data ./wsdot_mqtt_producer_mqtt_client

install: build
	cd wsdot_mqtt_producer_data && poetry install
	cd wsdot_mqtt_producer_mqtt_client && poetry install
	pip install ./wsdot_mqtt_producer_data ./wsdot_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./wsdot_mqtt_producer_mqtt_client/tests ./wsdot_mqtt_producer_data/tests