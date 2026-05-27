.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./sensor_community_producer_data ./sensor_community_producer_kafka_producer

install: build
	cd sensor_community_producer_data && poetry install
	cd sensor_community_producer_kafka_producer && poetry install
	pip install ./sensor_community_producer_data ./sensor_community_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./sensor_community_producer_kafka_producer/tests ./sensor_community_producer_data/tests