.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./bluesky_amqp_producer_data ./bluesky_amqp_producer_amqp_producer

install: build
	cd bluesky_amqp_producer_data && poetry install
	cd bluesky_amqp_producer_amqp_producer && poetry install
	pip install ./bluesky_amqp_producer_data ./bluesky_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./bluesky_amqp_producer_amqp_producer/tests ./bluesky_amqp_producer_data/tests
