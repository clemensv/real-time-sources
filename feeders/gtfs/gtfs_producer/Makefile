.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gtfs_producer_data ./gtfs_producer_kafka_producer

install: build
	cd gtfs_producer_data && poetry install
	cd gtfs_producer_kafka_producer && poetry install
	pip install ./gtfs_producer_data ./gtfs_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gtfs_producer_kafka_producer/tests ./gtfs_producer_data/tests