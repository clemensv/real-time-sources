.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./environment_canada_amqp_producer_data ./environment_canada_amqp_producer_amqp_producer

install: build
	cd environment_canada_amqp_producer_data && poetry install
	cd environment_canada_amqp_producer_amqp_producer && poetry install
	pip install ./environment_canada_amqp_producer_data ./environment_canada_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./environment_canada_amqp_producer_amqp_producer/tests ./environment_canada_amqp_producer_data/tests
