.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gracedb_amqp_producer_data ./gracedb_amqp_producer_amqp_producer

install: build
	cd gracedb_amqp_producer_data && poetry install
	cd gracedb_amqp_producer_amqp_producer && poetry install
	pip install ./gracedb_amqp_producer_data ./gracedb_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gracedb_amqp_producer_amqp_producer/tests ./gracedb_amqp_producer_data/tests
