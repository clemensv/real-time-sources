.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ndw_road_traffic_mqtt_producer_data ./ndw_road_traffic_mqtt_producer_mqtt_client

install: build
	cd ndw_road_traffic_mqtt_producer_data && poetry install
	cd ndw_road_traffic_mqtt_producer_mqtt_client && poetry install
	pip install ./ndw_road_traffic_mqtt_producer_data ./ndw_road_traffic_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ndw_road_traffic_mqtt_producer_mqtt_client/tests ./ndw_road_traffic_mqtt_producer_data/tests