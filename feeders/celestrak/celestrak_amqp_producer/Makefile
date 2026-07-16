.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./celestrak_amqp_producer_data ./celestrak_amqp_producer_amqp_producer

install: build
	cd celestrak_amqp_producer_data && poetry install
	cd celestrak_amqp_producer_amqp_producer && poetry install
	pip install ./celestrak_amqp_producer_data ./celestrak_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./celestrak_amqp_producer_amqp_producer/tests ./celestrak_amqp_producer_data/tests
