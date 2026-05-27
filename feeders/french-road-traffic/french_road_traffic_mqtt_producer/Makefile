.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./french_road_traffic_mqtt_producer_data ./french_road_traffic_mqtt_producer_mqtt_client

install: build
	cd french_road_traffic_mqtt_producer_data && poetry install
	cd french_road_traffic_mqtt_producer_mqtt_client && poetry install
	pip install ./french_road_traffic_mqtt_producer_data ./french_road_traffic_mqtt_producer_mqtt_client
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./french_road_traffic_mqtt_producer_mqtt_client/tests ./french_road_traffic_mqtt_producer_data/tests