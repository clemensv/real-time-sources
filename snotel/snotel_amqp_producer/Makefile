.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./snotel_amqp_producer_data ./snotel_amqp_producer_amqp_producer

install: build
	cd snotel_amqp_producer_data && poetry install
	cd snotel_amqp_producer_amqp_producer && poetry install
	pip install ./snotel_amqp_producer_data ./snotel_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./snotel_amqp_producer_amqp_producer/tests ./snotel_amqp_producer_data/tests
