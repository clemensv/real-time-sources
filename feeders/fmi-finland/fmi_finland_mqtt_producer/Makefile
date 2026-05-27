.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./fmi_finland_mqtt_producer_data ./fmi_finland_mqtt_producer_mqtt_client

install: build
	cd fmi_finland_mqtt_producer_data && poetry install
	cd fmi_finland_mqtt_producer_mqtt_client && poetry install
	pip install ./fmi_finland_mqtt_producer_data ./fmi_finland_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./fmi_finland_mqtt_producer_mqtt_client/tests ./fmi_finland_mqtt_producer_data/tests