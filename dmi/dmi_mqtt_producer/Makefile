.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./dmi_mqtt_producer_data ./dmi_mqtt_producer_mqtt_client

install: build
	cd dmi_mqtt_producer_data && poetry install
	cd dmi_mqtt_producer_mqtt_client && poetry install
	pip install ./dmi_mqtt_producer_data ./dmi_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./dmi_mqtt_producer_mqtt_client/tests ./dmi_mqtt_producer_data/tests