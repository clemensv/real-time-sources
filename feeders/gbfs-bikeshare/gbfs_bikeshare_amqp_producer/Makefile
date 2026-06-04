.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gbfs_bikeshare_amqp_producer_data ./gbfs_bikeshare_amqp_producer_amqp_producer

install: build
	cd gbfs_bikeshare_amqp_producer_data && poetry install
	cd gbfs_bikeshare_amqp_producer_amqp_producer && poetry install
	pip install ./gbfs_bikeshare_amqp_producer_data ./gbfs_bikeshare_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gbfs_bikeshare_amqp_producer_amqp_producer/tests ./gbfs_bikeshare_amqp_producer_data/tests
