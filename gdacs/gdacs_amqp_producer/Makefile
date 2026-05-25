.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./gdacs_amqp_producer_data ./gdacs_amqp_producer_amqp_producer

install: build
	cd gdacs_amqp_producer_data && poetry install
	cd gdacs_amqp_producer_amqp_producer && poetry install
	pip install ./gdacs_amqp_producer_data ./gdacs_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./gdacs_amqp_producer_amqp_producer/tests ./gdacs_amqp_producer_data/tests
