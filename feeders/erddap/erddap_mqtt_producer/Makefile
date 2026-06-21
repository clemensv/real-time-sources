.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./erddap_mqtt_producer_data ./erddap_mqtt_producer_mqtt_client

install: build
	cd erddap_mqtt_producer_data && poetry install
	cd erddap_mqtt_producer_mqtt_client && poetry install
	pip install ./erddap_mqtt_producer_data ./erddap_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./erddap_mqtt_producer_mqtt_client/tests ./erddap_mqtt_producer_data/tests