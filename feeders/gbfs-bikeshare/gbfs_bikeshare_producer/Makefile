.PHONY: build install

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gbfs_bikeshare_producer_data ./gbfs_bikeshare_producer_kafka_producer

install: build
	cd gbfs_bikeshare_producer_data && poetry install
	cd gbfs_bikeshare_producer_kafka_producer && poetry install
	pip install ./gbfs_bikeshare_producer_data ./gbfs_bikeshare_producer_kafka_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gbfs_bikeshare_producer_kafka_producer/tests ./gbfs_bikeshare_producer_data/tests