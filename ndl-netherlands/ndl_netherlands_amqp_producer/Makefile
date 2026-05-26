.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./ndl_netherlands_amqp_producer_data ./ndl_netherlands_amqp_producer_amqp_producer

install: build
	cd ndl_netherlands_amqp_producer_data && poetry install
	cd ndl_netherlands_amqp_producer_amqp_producer && poetry install
	pip install ./ndl_netherlands_amqp_producer_data ./ndl_netherlands_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./ndl_netherlands_amqp_producer_amqp_producer/tests ./ndl_netherlands_amqp_producer_data/tests
