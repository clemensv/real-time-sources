.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./irail_amqp_producer_data ./irail_amqp_producer_amqp_producer

install: build
	cd irail_amqp_producer_data && poetry install
	cd irail_amqp_producer_amqp_producer && poetry install
	pip install ./irail_amqp_producer_data ./irail_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./irail_amqp_producer_amqp_producer/tests ./irail_amqp_producer_data/tests
