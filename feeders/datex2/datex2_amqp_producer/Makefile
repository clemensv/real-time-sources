.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./datex2_amqp_producer_data ./datex2_amqp_producer_amqp_producer

install: build
	cd datex2_amqp_producer_data && poetry install
	cd datex2_amqp_producer_amqp_producer && poetry install
	pip install ./datex2_amqp_producer_data ./datex2_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./datex2_amqp_producer_amqp_producer/tests ./datex2_amqp_producer_data/tests
