.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ndw_road_traffic_producer_data ./ndw_road_traffic_producer_kafka_producer

install: build
	cd ndw_road_traffic_producer_data && poetry install
	cd ndw_road_traffic_producer_kafka_producer && poetry install
	pip install ./ndw_road_traffic_producer_data ./ndw_road_traffic_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ndw_road_traffic_producer_kafka_producer/tests ./ndw_road_traffic_producer_data/tests