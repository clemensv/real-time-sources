.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./french_road_traffic_amqp_producer_data ./french_road_traffic_amqp_producer_amqp_producer

install: build
	cd french_road_traffic_amqp_producer_data && poetry install
	cd french_road_traffic_amqp_producer_amqp_producer && poetry install
	pip install ./french_road_traffic_amqp_producer_data ./french_road_traffic_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./french_road_traffic_amqp_producer_amqp_producer/tests ./french_road_traffic_amqp_producer_data/tests
