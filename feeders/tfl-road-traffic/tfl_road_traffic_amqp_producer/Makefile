.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./tfl_road_traffic_amqp_producer_data ./tfl_road_traffic_amqp_producer_amqp_producer

install: build
	cd tfl_road_traffic_amqp_producer_data && poetry install
	cd tfl_road_traffic_amqp_producer_amqp_producer && poetry install
	pip install ./tfl_road_traffic_amqp_producer_data ./tfl_road_traffic_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./tfl_road_traffic_amqp_producer_amqp_producer/tests ./tfl_road_traffic_amqp_producer_data/tests
