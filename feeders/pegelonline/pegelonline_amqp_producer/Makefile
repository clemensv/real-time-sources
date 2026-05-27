.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./pegelonline_amqp_producer_data ./pegelonline_amqp_producer_amqp_producer

install: build
	cd pegelonline_amqp_producer_data && poetry install
	cd pegelonline_amqp_producer_amqp_producer && poetry install
	pip install ./pegelonline_amqp_producer_data ./pegelonline_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./pegelonline_amqp_producer_amqp_producer/tests ./pegelonline_amqp_producer_data/tests
