.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ndw_road_traffic_amqp_producer_data ./ndw_road_traffic_amqp_producer_amqp_producer

install: build
	cd ndw_road_traffic_amqp_producer_data && poetry install
	cd ndw_road_traffic_amqp_producer_amqp_producer && poetry install
	pip install ./ndw_road_traffic_amqp_producer_data ./ndw_road_traffic_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ndw_road_traffic_amqp_producer_amqp_producer/tests ./ndw_road_traffic_amqp_producer_data/tests
