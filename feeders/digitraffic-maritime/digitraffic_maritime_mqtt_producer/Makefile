.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./digitraffic_maritime_mqtt_producer_data ./digitraffic_maritime_mqtt_producer_mqtt_client

install: build
	cd digitraffic_maritime_mqtt_producer_data && poetry install
	cd digitraffic_maritime_mqtt_producer_mqtt_client && poetry install
	pip install ./digitraffic_maritime_mqtt_producer_data ./digitraffic_maritime_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./digitraffic_maritime_mqtt_producer_mqtt_client/tests ./digitraffic_maritime_mqtt_producer_data/tests