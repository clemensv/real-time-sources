.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./blitzortung_amqp_producer_data ./blitzortung_amqp_producer_amqp_producer

install: build
	cd blitzortung_amqp_producer_data && poetry install
	cd blitzortung_amqp_producer_amqp_producer && poetry install
	pip install ./blitzortung_amqp_producer_data ./blitzortung_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./blitzortung_amqp_producer_amqp_producer/tests ./blitzortung_amqp_producer_data/tests
