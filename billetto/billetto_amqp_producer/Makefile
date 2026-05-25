.PHONY: build install test

build:
	pip install wheel poetry poetry-plugin-export
	pip wheel -w whl ./billetto_amqp_producer_data ./billetto_amqp_producer_amqp_producer

install: build
	cd billetto_amqp_producer_data && poetry install
	cd billetto_amqp_producer_amqp_producer && poetry install
	pip install ./billetto_amqp_producer_data ./billetto_amqp_producer_amqp_producer
	pip install pytest-asyncio>=0.23.7

test: install
	pytest ./billetto_amqp_producer_amqp_producer/tests ./billetto_amqp_producer_data/tests
