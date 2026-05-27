.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gtfs_rt_producer_data ./gtfs_rt_producer_kafka_producer

install: build
	cd gtfs_rt_producer_data && poetry install
	cd gtfs_rt_producer_kafka_producer && poetry install
	pip install ./gtfs_rt_producer_data ./gtfs_rt_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gtfs_rt_producer_kafka_producer/tests ./gtfs_rt_producer_data/tests