.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bfs_odl_producer_data ./bfs_odl_producer_kafka_producer

install: build
	cd bfs_odl_producer_data && poetry install
	cd bfs_odl_producer_kafka_producer && poetry install
	pip install ./bfs_odl_producer_data ./bfs_odl_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bfs_odl_producer_kafka_producer/tests ./bfs_odl_producer_data/tests