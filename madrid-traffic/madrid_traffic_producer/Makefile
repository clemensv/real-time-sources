.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./madrid_traffic_producer_data ./madrid_traffic_producer_kafka_producer

install: build
	cd madrid_traffic_producer_data && poetry install
	cd madrid_traffic_producer_kafka_producer && poetry install
	pip install ./madrid_traffic_producer_data ./madrid_traffic_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./madrid_traffic_producer_kafka_producer/tests ./madrid_traffic_producer_data/tests