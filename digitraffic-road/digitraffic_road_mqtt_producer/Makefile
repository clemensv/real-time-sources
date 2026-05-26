.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./digitraffic_road_mqtt_producer_data ./digitraffic_road_mqtt_producer_mqtt_client

install: build
	cd digitraffic_road_mqtt_producer_data && poetry install
	cd digitraffic_road_mqtt_producer_mqtt_client && poetry install
	pip install ./digitraffic_road_mqtt_producer_data ./digitraffic_road_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./digitraffic_road_mqtt_producer_mqtt_client/tests ./digitraffic_road_mqtt_producer_data/tests